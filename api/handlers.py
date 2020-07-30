import json
import logging
import sys
import traceback

from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from metadata import generate_metadata
del sys.path[0]

def get_all_metadata(functions):
    """Return the JSON metadata"""
    fns = ((n, getattr(functions, n, None)) for n in dir(functions))
    return json.dumps({
        "functions": [generate_metadata(n, f) for n, f in fns
                      if f and callable(f) and n[:1] != "_"]
    })


def convert_argument(param, arg):
    """Based on metadata in param, return arg updated for the target function."""
    name = param["name"]
    tp = param.get("_python_type")
    if tp:
        # Function expects a particular type
        try:
            arg = tp(arg)
        except Exception:
            logging.exception("Failed to convert %s to %r", name, tp)
    elif param.get("dimensionality") == "matrix":
        # Attempt to convert to pandas dataframe, if pandas is available
        try:
            import pandas
            arg = pandas.DataFrame(arg)
            logging.info("Converted %s", name)
        except ModuleNotFoundError:
            pass
        except Exception:
            logging.exception("Failed to convert %s to pd.DataFrame", name)
    return arg


def json_default(o):
    """Handle unhandled JSON values"""
    # Convert pandas.DataFrame to lists
    try:
        tolist = o.values.tolist
    except AttributeError:
        pass
    else:
        return tolist()
    # Handle everything else by returning its repr
    return repr(o)


def execute_function(functions, payload):
    try:
        n = payload["id"].casefold()
    except LookupError:
        raise LookupError("no 'id' field")

    fmap = getattr(functions, "__fmap", None)
    if fmap is None:
        fmap = {k.casefold(): getattr(functions, k) for k in dir(functions)}
        functions.__fmap = fmap

    try:
        f = fmap[n]
    except AttributeError:
        ret = {"error": 2}
    else:
        md = generate_metadata(n, f, tidy=False)
        args = []
        try:
            args = [convert_argument(*i) for i in
                    zip(md.get("parameters", []), payload.get("parameters", []))]

            r = f(*args)
            ret = {"error": 0, "result": r}
        except Exception:
            logging.exception("Error executing %s(%s)", n, args)
            ret = {"error": 1, "result": "".join(traceback.format_exc())}

    return json.dumps(ret, default=json_default)
