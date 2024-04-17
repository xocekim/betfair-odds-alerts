from flask import Flask, render_template
from playhouse.flask_utils import FlaskDB
from requests import Session

BETFAIR_URL = 'https://api.betfair.com/exchange/betting/json-rpc/v1'


# setup flask and db
app = Flask(__name__)
app.config.from_object('config')
db = FlaskDB(app)


# setup betfair requests
bf = Session()
bf.headers.update({'X-Application': app.config.get('BETFAIR_APPID'), 'X-Authentication': app.config.get('BETFAIR_SSOID')})
print(bf.headers)

# betfair api functions
def bf_get_event_types() -> dict:
    ''' returns betfair event types dict '''
    json_req = {'jsonrpc': '2.0', 'method': 'SportsAPING/v1.0/listEventTypes', 'params': {'filter':{ }}, 'id': 1}
    resp = bf.post(BETFAIR_URL, json=json_req)
    event_types = {}
    for et in resp.json()['result']:
        event_types[et['eventType']['name']] = et['eventType']['id']
    print(event_types)
    return event_types


@app.route('/')
def index():
    return render_template('index.html', event_types=bf_get_event_types())
