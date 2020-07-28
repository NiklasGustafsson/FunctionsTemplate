from __future__ import annotations

import azure.functions as func
import logging
import sys

from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from handlers import execute_function, get_all_metadata
del sys.path[0]


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
            return func.HttpResponse(f"Invalid request: {ex}", status_code=400)
        try:
            return func.HttpResponse(
                execute_function(Functions, payload),
                mimetype="application/json",
            )
        except Exception as ex:
            return func.HttpResponse(f"Invalid request: {ex}", status_code=422)


    return func.HttpResponse(get_all_metadata(Functions), mimetype="application/json")
