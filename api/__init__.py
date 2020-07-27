import logging
import json

import azure.functions as func
from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Defer the import until triggered so that failure is attached to the response
    try:
        import Functions
    except ModuleNotFoundError:
        # Try the Azure Functions name if the "natural" name was missing
        import __app__.Functions as Functions

    try:
        payload = req.get_json()
    except Exception as ex:
        return func.HttpResponse("Invalid request: {}".format(ex), status_code=400)

    try:
        n = payload["id"]
    except LookupError:
        return func.HttpResponse("Invalid request: no 'id' field", status_code=422)

    try:
        f = getattr(Functions, n)
    except AttributeError:
        return func.HttpResponse("Unknown function: '{}'".format(n), status_code=422)

    args = payload.get("parameters", [])

    ret = f(*args)
    return json.dumps(ret, default=vars)
