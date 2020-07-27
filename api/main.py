import logging
import json
import sys
import traceback

import azure.functions as func
from pathlib import Path

sys.path.insert(0, str(Path(__file__).absolute().parent))
from metadata import generate_metadata


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Defer the import until triggered so that failure is attached to the response
    try:
        import Functions
    except ModuleNotFoundError:
        # Try the Azure Functions name if the "natural" name was missing
        import __app__.Functions as Functions

    if req.method == "POST":
        try:
            payload = req.get_json()
        except Exception as ex:
            return func.HttpResponse("Invalid request: {}".format(ex), status_code=400)
        return execute_function(Functions, payload)

    return func.HttpResponse(
        json.dumps(get_all_metadata(Functions)),
        mimetype="application/json",
    )


def get_all_metadata(functions):
    """Return the JSON metadata"""
    fns = ((n, getattr(functions, n, None)) for n in dir(functions))
    return {
        "functions": [generate_metadata(n, f) for n, f in fns
                      if f and callable(f) and n[:1] != "_"]
    }


def convert_argument(param, arg):
    """Based on metadata in param, return arg updated for the target function."""
    name = param["name"]
    if param.get("dimensionality") == "matrix":
        # Attempt to convert to pandas dataframe, if pandas is available
        try:
            import pandas
            arg = pandas.DataFrame(arg)
            logging.info("Converted %s", name)
        except ModuleNotFoundError:
            pass
        except Exception:
            logging.exception("Failed to convert %s to pd.DataFrame", name)
    elif param.get("_python_type") == "int":
        # Function expects int, not float, so truncate
        try:
            arg = int(arg)
        except Exception:
            logging.exception("Failed to convert %s to int", name)
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
    # Handle everything else by getting its vars
    return vars(o)


def execute_function(functions, payload):
    try:
        n = payload["id"]
    except LookupError:
        return func.HttpResponse("Invalid request: no 'id' field", status_code=422)

    try:
        f = getattr(functions, n)
    except AttributeError:
        ret = {"error": 2}
    else:
        md = generate_metadata(n, f, tidy=False)
        args = []
        try:
            args = [convert_argument(*i) for i in
                    zip(md.get("parameters", []), payload.get("parameters", []))]

            ret = {"result": f(*args), "error": 0}
        except Exception:
            logging.exception("Error executing %s(%s)", n, args)
            ret = {"error": 1, "result": "".join(traceback.format_exc())}

    return func.HttpResponse(
        json.dumps(ret, default=json_default),
        mimetype="application/json",
    )
