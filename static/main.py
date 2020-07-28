import azure.functions as func

PAGE = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>Custom Functions</title>
    <link rel="stylesheet" href="https://static2.sharepointonline.com/files/fabric/office-ui-fabric-core/9.6.1/css/fabric.min.css">
    <script src="https://exceljupyter.azurewebsites.net/agave/external/react-16-12-0/umd/react.development.js"></script>
    <script src="https://exceljupyter.azurewebsites.net/agave/external/react-dom-16-12-0/umd/react-dom.development.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.5/require.min.js"></script>
    <script type="text/javascript" src="https://appsforoffice.microsoft.com/lib/1.1/hosted/office.debug.js"></script>
    <script type="text/javascript" src="https://exceljupyter.azurewebsites.net/agave/custom-function-forwarder.bundle.js"></script>
</head>
    <body>
        <div id="DivApp">
        </div>
        <div id="DivLog">
        </div>
    </body>
</html>"""


def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(PAGE, mimetype="text/html")
