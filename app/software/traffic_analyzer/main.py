import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import flask

SOFTWARE_TYPE = "DASH"


def page(requests_pathname_prefix: str = None):
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')

    from dotenv import load_dotenv
    load_dotenv()

    uname, pwd = os.getenv('MONGO_USER'), os.getenv('MONGO_PASS')
    uri = f"mongodb+srv://{uname}:{pwd}@traffic.w4hz9eq.mongodb.net/?retryWrites=true&w=majority&appName=traffic"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    results = list(client['traffic']['forward'].find({}))

    df = pd.DataFrame([(d['time'],
                        int(d['elements'][0]['duration_in_traffic']['value'] / 60)) for d in results],
                      columns=['date', 'duration_min'])

    df.index = df['date']
    df = df.apply(pd.to_numeric, errors='coerce').resample(
        '20min', offset='10min').mean()
    df["hourmin"] = df.index.strftime('%H:%M')
    df["weekday"] = df.index.day_name()

    pivot_df = df.pivot_table(
        index='weekday', columns='hourmin', values='duration_min', aggfunc='mean'
    )

    dash_app = dash.Dash(__name__, server=server,
                         requests_pathname_prefix=requests_pathname_prefix)

    fig = px.imshow(pivot_df,
                    x=pivot_df.columns, y=pivot_df.index,
                    text_auto=True,
                    labels=dict(x="Time of Day", y="Day of Week",
                                color="Duration (min)"))

    dash_app.layout = html.Div([
        html.H1(children='Dash App', style={'textAlign': 'center'}),
        html.H1('Hi!'),
        dcc.Graph(figure=fig)
    ])

    return dash_app
