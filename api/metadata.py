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
        return {"type": "any", "dimensionality": "scalar"}
    kind = _convert_matrix(hint)
    if kind:
        return {"type": kind, "dimensionality": "matrix"}
    kind = _convert_scalar(hint) or "any"
    return {"type": kind, "dimensionality": "scalar"}


def generate_metadata(name, function):
    if not inspect.isfunction(function):
        return {}
    hints = typing.get_type_hints(function, globals())
    params = [
        {"name": k, "description": "", **_convert_hint(hints.get(k))}
        for k in inspect.getfullargspec(function).args
    ]

    return {
        "id": name,
        "name": name,
        "description": getattr(function, "__doc__", None) or "",
        "parameters": params,
        "result": _convert_hint(hints.get("return")),
    }
