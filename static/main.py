import azure.functions as func
from pathlib import Path

PAGE = (Path(__file__).absolute().parent / "main.html").read_bytes()

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(PAGE, mimetype="text/html")
