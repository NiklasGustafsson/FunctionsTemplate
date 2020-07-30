import base64
import pandas
from urllib.parse import quote as _urlquote
from urllib.request import urlopen as _urlopen

def countrydata(country : str) -> "Matrix":
    """Retrieves model data for a specified region.

    country: Name of the region to retrieve data for
    """
    # Need to ensure we URL encode the string
    #country = _urlquote(country)

    data = pandas.read_csv(f"https://e2efunc.azurewebsites.net/api/covidata?country={country}")
    return data


def countryplot(country : str):
    """Retrieves a plot of model outputs for a specified region.

    country: Name of the region to retrieve data for
    """
    # Need to ensure we URL encode the string
    #country = _urlquote(country)

    with _urlopen(f"https://e2efunc.azurewebsites.net/api/covidata?country={country}&output=plot") as u:
        plot = u.read()
        mime_type = u.getheader("Content-Type")

    # We return images as Base-64 encoded binary
    base64_plot = base64.b64encode(plot)
    # JSON blob requires a str, not bytes
    base64_plot_str = base64_plot.decode("ascii")

    return {
        "data": base64_plot_str,
        "mimeType": mime_type,
    }
