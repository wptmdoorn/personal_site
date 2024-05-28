import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import flask
from dash.dependencies import Input, Output

SOFTWARE_TYPE = "DASH"


def fetch_data(direction):
    uname, pwd = os.getenv('MONGO_USER'), os.getenv('MONGO_PASS')
    uri = f"mongodb+srv://{uname}:{pwd}@traffic.w4hz9eq.mongodb.net/?retryWrites=true&w=majority&appName=traffic"
    client = MongoClient(uri, server_api=ServerApi('1'))
    results = list(client['traffic'][direction].find({}))
    df = pd.DataFrame([(d['time'], int(d['elements'][0]['duration_in_traffic']['value'] / 60)) for d in results],
                      columns=['date', 'duration_min'])
    return df


def page(requests_pathname_prefix: str = None):
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')

    from dotenv import load_dotenv
    load_dotenv()

    dash_app = dash.Dash(__name__, server=server,
                         requests_pathname_prefix=requests_pathname_prefix)

    time_options = [{'label': f'{hour:02d}:00',
                     'value': f'{hour:02d}:00'} for hour in range(24)]

    dash_app.layout = html.Div([
        html.H1(children='Traffic analyzer - commute from home',
                style={'textAlign': 'center'}),
        html.Div([
            html.Label('Select Traffic Direction:'),
            dcc.Dropdown(
                id='direction-dropdown',
                options=[
                    {'label': 'Forward', 'value': 'forward'},
                    {'label': 'Backward', 'value': 'backward'}
                ],
                value='forward'
            ),
            html.Label('Select Time Range:'),
            dcc.Dropdown(
                id='time-range-dropdown',
                options=[
                    {'label': 'Last 24 hours', 'value': '24h'},
                    {'label': 'Last 7 days', 'value': '7d'},
                    {'label': 'Last 30 days', 'value': '30d'}
                ],
                value='7d'
            ),
            html.Label('Select Start Time:'),
            dcc.Dropdown(
                id='start-time-dropdown',
                options=time_options,
                value='00:00'
            ),
            html.Label('Select End Time:'),
            dcc.Dropdown(
                id='end-time-dropdown',
                options=time_options,
                value='23:00'
            ),
        ]),
        dcc.Graph(id='traffic-heatmap')
    ])

    @dash_app.callback(
        Output('traffic-heatmap', 'figure'),
        Input('direction-dropdown', 'value'),
        Input('time-range-dropdown', 'value'),
        Input('start-time-dropdown', 'value'),
        Input('end-time-dropdown', 'value')
    )
    def update_graph(direction, time_range, start_time, end_time):
        df = fetch_data(direction)
        df['date'] = pd.to_datetime(df['date'])

        if time_range == '24h':
            time_filter = pd.Timestamp.now() - pd.Timedelta(hours=24)
        elif time_range == '7d':
            time_filter = pd.Timestamp.now() - pd.Timedelta(days=7)
        elif time_range == '30d':
            time_filter = pd.Timestamp.now() - pd.Timedelta(days=30)

        df = df[df['date'] > time_filter]
        df.index = df['date']
        df = df.apply(pd.to_numeric, errors='coerce').resample(
            '20min', offset='10min').mean()
        df["hourmin"] = df.index.strftime('%H:%M')
        df["weekday"] = df.index.day_name()

        start_time_filter = pd.to_datetime(start_time, format='%H:%M').time()
        end_time_filter = pd.to_datetime(end_time, format='%H:%M').time()

        df = df.between_time(start_time_filter, end_time_filter)

        pivot_df = df.pivot_table(
            index='weekday', columns='hourmin', values='duration_min', aggfunc='mean')

        fig = px.imshow(pivot_df,
                        x=pivot_df.columns, y=pivot_df.index,
                        text_auto=True,
                        labels=dict(x="Time of Day", y="Day of Week", color="Duration (min)"))

        return fig

    return dash_app
