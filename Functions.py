import base64
import pandas
from urllib.parse import quote as urlquote
from urllib.request import urlopen

def countrydata(country : str) -> "Matrix":
    #country = urlquote(country)
    return pandas.read_csv(f"https://excelpythonbase.azurewebsites.net/covidata?country={country}")


def countryplot(country : str):
    #country = urlquote(country)
    with urlopen(f"https://excelpythonbase.azurewebsites.net/covidata?country={country}&output=plot") as u:
        return {
            "data": base64.b64encode(u.read()).decode("ascii"),
            "mimeType": u.getheader("Content-Type"),
        }
