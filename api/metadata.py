import inspect
import typing

NumberMatrix = typing.NewType("NumberMatrix", typing.Any)
StringMatrix = typing.NewType("StringMatrix", typing.Any)
AnyMatrix = typing.NewType("AnyMatrix", typing.Any)

def _convert_matrix(hint):
    if hint is NumberMatrix:
        return "number"
    if hint is StringMatrix:
        return "string"
    if hint is AnyMatrix:
        return "any"


def _convert_scalar(hint):
    if not hint or hint is typing.Any:
        return "any"
    if hint in {int, float, typing.SupportsFloat, typing.SupportsIndex, typing.SupportsInt}:
        return "number"
    if hint in {bool}:
        return "boolean"
    if hint in {str, typing.AnyStr, typing.Text}:
        return "string"


def _convert_hint(hint):
    if not hint:
        return {}
    kind = _convert_matrix(hint)
    if kind is not None:
        return {"type": kind, "dimensionality": "matrix"}
    kind = _convert_scalar(hint)
    return {"type": kind}


def _tidy_metadata(md):
    return {k: v for k, v in md.items() if v}


def generate_metadata(name, function):
    if not inspect.isfunction(function):
        return {}
    hints = typing.get_type_hints(function, globals())
    params = [
        {"name": k, "description": None, **_convert_hint(hints.get(k))}
        for k in inspect.getfullargspec(function).args
    ]

    params = [_tidy_metadata(md) for md in params]

    md = {
        "id": name,
        "name": name,
        "description": getattr(function, "__doc__", None) or "",
        "parameters": params,
        "result": _convert_hint(hints.get("return")),
    }
    md = _tidy_metadata(md)
    return md
