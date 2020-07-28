import inspect
import sys
import typing

NumberMatrix = typing.NewType("NumberMatrix", typing.Any)
StringMatrix = typing.NewType("StringMatrix", typing.Any)
AnyMatrix = typing.NewType("AnyMatrix", typing.Any)
Matrix = typing.NewType("Matrix", typing.Any)


def _convert_matrix(hint):
    if hint is NumberMatrix:
        return {"type": "number", "dimensionality": "matrix"}
    if hint is StringMatrix:
        return {"type": "string", "dimensionality": "matrix"}
    if hint in {Matrix, AnyMatrix}:
        return {"dimensionality": "matrix"}
    pd = sys.modules.get("pandas")
    if pd:
        if hint is pd.DataFrame:
            return {"dimensionality": "matrix", "_python_type": pd.Dataframe}
    np = sys.modules.get("numpy")
    if np:
        if hint is np.ndarray:
            return {"dimensionality": "matrix", "_python_type": np.ndarray}


def _convert_scalar(hint):
    if hint is typing.Any:
        return {}
    if hint in {int, typing.SupportsIndex, typing.SupportsInt}:
        return {"type": "number", "_python_type": int}
    if hint in {float, typing.SupportsFloat}:
        return {"type": "number", "_python_type": float}
    if hint in {bool}:
        return {"type": "boolean", "_python_type": bool}
    if hint in {str, typing.AnyStr, typing.Text}:
        return {"type": "string", "_python_type": str}


def _convert_hint(hint):
    if not hint:
        return {}
    kind = _convert_matrix(hint)
    if kind is not None:
        return kind
    return _convert_scalar(hint) or {}


def _dedent(s):
    min_indent = None
    for i, line in enumerate(s.splitlines()):
        if i == 0:
            # Skip the first line. In doc strings, this is
            # rarely indented.
            continue
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if min_indent is None or indent < min_indent:
            min_indent = indent
    if not min_indent:
        return s
    return "\n".join(
        (line if not i else line[min_indent:] if len(line) > min_indent else "")
        for i, line in enumerate(s.splitlines())
    )


def _find_doc(lines, name):
    parts = None
    for line in lines:
        if parts is None:
            if not line.startswith(name):
                continue
            line = line[len(name):].lstrip()
            if line.startswith(":"):
                line = line.lstrip(":").lstrip()
                parts = [line]
        elif line:
            parts.append(line)
        else:
            break
    if parts:
        return " ".join(parts)


def _tidy_metadata(md):
    return {k: v for k, v in md.items() if k[:1] != "_" and v}


def generate_metadata(name, function, tidy=True):
    if name[:1] == "_" or not inspect.isfunction(function):
        return {}

    doc = _dedent(getattr(function, "__doc__", None) or "")
    doc_lines = [s.strip() for s in doc.splitlines()]

    hints = typing.get_type_hints(function, globals())
    params = [
        {
            "name": k,
            "description": _find_doc(doc_lines, k),
            **_convert_hint(hints.get(k))
        }
        for k in inspect.getfullargspec(function).args
    ]

    if tidy:
        params = [_tidy_metadata(md) for md in params]

    md = {
        "id": name,
        "name": name,
        "description": doc,
        "parameters": params,
        "result": _convert_hint(hints.get("return")),
    }
    if tidy:
        md = _tidy_metadata(md)
    return md
