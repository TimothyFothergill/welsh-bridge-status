from bs4 import BeautifulSoup
from dataclasses import dataclass
from flask import Flask, jsonify

from urllib.request import urlopen
import urllib.request

app = Flask(__name__)

_SOURCE_URL = "https://nationalhighways.co.uk/travel-updates/the-severn-bridges/"
_BRIDGE_STATUS_CLASS = "severn-crossing-status__heading"
_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

@dataclass
class BridgeStatus():
    status: int
    description: str

@app.route("/")
def get_statuses():
    resp = wales_bridge_statuses()
    return jsonify(resp)

def wales_bridge_statuses():
    responses = []
    request = urllib.request.Request(_SOURCE_URL, headers=_HEADERS)
    with urlopen(request) as response:
        soup = BeautifulSoup(response, 'html.parser')
        for anchor in soup.find_all('div', {"class":_BRIDGE_STATUS_CLASS}):
            result = (str)(anchor).find("Open -")
            if(result != -1):
                responses.append(BridgeStatus(1,(str)(anchor).split("Open - ")[1].removesuffix("</div>")))
            else:
                responses.append(BridgeStatus(0,(str)(anchor).removeprefix("<div class=\"severn-crossing-status__heading\">").removesuffix("</div>")))
    return responses

resps = wales_bridge_statuses()

if __name__ == "__main__":
    from os import environ
    app.run(debug=False, host="0.0.0.0", port=environ.get("PORT", 5000))
