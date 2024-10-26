from flask import Flask
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import numpy as np

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, 
           server=server, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

# Generate sample data (replace with your actual data loading)
def generate_sample_data():
    # เปลี่ยนจาก freq='H' เป็น freq='h'
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='h')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'DATETIMEDATA': dates,
        'PM25': np.random.normal(25, 10, len(dates)),
        'PM10': np.random.normal(40, 15, len(dates)),
        'O3': np.random.normal(30, 8, len(dates)),
        'NO2': np.random.normal(20, 5, len(dates)),
        'Temperature': np.random.normal(25, 3, len(dates)),
        'Humidity': np.random.normal(60, 10, len(dates)),
        'WindSpeed': np.random.normal(10, 3, len(dates))
    })
    
    return data

data_air = generate_sample_data()
data_pred = data_air.copy()  # For this example, we'll use the same data

# AQI calculation functions
def calculate_pm25_aqi(pm25):
    if pm25 <= 12.0:
        return ((50 - 0) / (12.0 - 0) * (pm25 - 0)) + 0
    elif pm25 <= 35.4:
        return ((100 - 51) / (35.4 - 12.1) * (pm25 - 12.1)) + 51
    elif pm25 <= 55.4:
        return ((150 - 101) / (55.4 - 35.5) * (pm25 - 35.5)) + 101
    elif pm25 <= 150.4:
        return ((200 - 151) / (150.4 - 55.5) * (pm25 - 55.5)) + 151
    elif pm25 <= 250.4:
        return ((300 - 201) / (250.4 - 150.5) * (pm25 - 150.5)) + 201
    else:
        return ((500 - 301) / (500.4 - 250.5) * (pm25 - 250.5)) + 301

def get_aqi_status(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Moderate", "yellow"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "orange"
    elif aqi <= 200:
        return "Unhealthy", "red"
    elif aqi <= 300:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "maroon"

# Custom CSS
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    }
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

# Navbar component
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analysis", href="/")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/page-2")),
    ],
    brand="Air Quality Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4"
)

# Main layout
def create_main_layout():
    return dbc.Container([
        navbar,
        
        # Header
        html.H1("Air Quality Dashboard", className="text-primary text-center my-4"),
        
        # Filter Row
        dbc.Row([
            dbc.Col([
                html.Label("Select Parameter"),
                dcc.Dropdown(
                    id='parameter-filter',
                    options=[{'label': col, 'value': col} for col in data_air.columns if col != 'DATETIMEDATA'],
                    value='PM25',
                    className="mb-3"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Date Range"),
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=data_air['DATETIMEDATA'].min(),
                    max_date_allowed=data_air['DATETIMEDATA'].max(),
                    start_date=data_air['DATETIMEDATA'].min(),
                    end_date=data_air['DATETIMEDATA'].max(),
                    className="mb-3"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Chart Type"),
                dcc.Dropdown(
                    id='chart-type',
                    options=[
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Scatter Plot', 'value': 'scatter'}
                    ],
                    value='line',
                    className="mb-3"
                )
            ], md=4)
        ]),
        
        # Cards Row
        dbc.Row([
            # AQI Card
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Air Quality Index (AQI)", className="card-title"),
                        html.Div(id="aqi-value", className="text-center h2"),
                        html.Div(id="aqi-status", className="text-center")
                    ])
                ], className="mb-4")
            ], md=6),
            
            # Weather Card
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Current Weather", className="card-title"),
                        html.Div(id="weather-info", className="text-center")
                    ])
                ], className="mb-4")
            ], md=6)
        ]),
        
        # Main Chart
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id='main-chart')
            ])
        ], className="mb-4"),
        
        # Parameter Comparison Section
        dbc.Card([
            dbc.CardBody([
                html.H4("Parameter Comparison"),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id='param-compare-1',
                            options=[{'label': col, 'value': col} 
                                   for col in data_air.columns if col != 'DATETIMEDATA'],
                            value='PM25',
                            className="mb-2"
                        )
                    ], md=6),
                    dbc.Col([
                        dcc.Dropdown(
                            id='param-compare-2',
                            options=[{'label': col, 'value': col} 
                                   for col in data_air.columns if col != 'DATETIMEDATA'],
                            value='PM10',
                            className="mb-2"
                        )
                    ], md=6)
                ]),
                dcc.Graph(id='comparison-chart')
            ])
        ], className="mb-4"),
        
        # Export Buttons
        dbc.Row([
            dbc.Col([
                dbc.Button("Export Data (CSV)", id="btn-csv", color="primary", className="me-2"),
                dbc.Button("Export Chart (PNG)", id="btn-png", color="secondary"),
                dcc.Download(id="download-data")
            ], className="mb-4")
        ]),
        
        # Alerts Section
        dbc.Card([
            dbc.CardBody([
                html.H4("Air Quality Alerts"),
                dcc.Checklist(
                    id='alert-settings',
                    options=[
                        {'label': ' PM2.5 Alert (>50 µg/m³)', 'value': 'PM25'},
                        {'label': ' PM10 Alert (>100 µg/m³)', 'value': 'PM10'},
                        {'label': ' O3 Alert (>100 ppb)', 'value': 'O3'}
                    ],
                    value=[],
                    className="mb-3"
                ),
                html.Div(id='alerts-display')
            ])
        ])
    ], fluid=True)

# Prediction layout
def create_prediction_layout():
    return dbc.Container([
        navbar,
        html.H1("Air Quality Predictions", className="text-primary text-center my-4"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Select Parameter"),
                dcc.Dropdown(
                    id='parameter-filter-predict',
                    options=[{'label': col, 'value': col} 
                            for col in data_pred.columns if col != 'DATETIMEDATA'],
                    value='PM25',
                    className="mb-3"
                )
            ], md=4)
        ]),
        
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id='prediction-chart')
            ])
        ], className="mb-4"),
        
        dbc.Card([
            dbc.CardBody([
                html.H4("Prediction Statistics"),
                html.Div(id='prediction-stats')
            ])
        ])
    ], fluid=True)

# App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/page-2':
        return create_prediction_layout()
    return create_main_layout()

@app.callback(
    [Output("aqi-value", "children"),
     Output("aqi-status", "children")],
    [Input("parameter-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_aqi(parameter, start_date, end_date):
    if parameter != "PM25":
        return "Select PM2.5 for AQI", ""
    
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    current_pm25 = filtered_data["PM25"].iloc[-1]
    aqi = int(calculate_pm25_aqi(current_pm25))
    status, color = get_aqi_status(aqi)
    
    return f"Current AQI: {aqi}", html.Div(f"Status: {status}", 
                                          style={'color': color, 'fontWeight': 'bold'})

@app.callback(
    Output("weather-info", "children"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_weather(start_date, end_date):
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    current_temp = filtered_data["Temperature"].iloc[-1]
    current_humidity = filtered_data["Humidity"].iloc[-1]
    current_wind = filtered_data["WindSpeed"].iloc[-1]
    
    return html.Div([
        html.Div([
            html.I(className="fas fa-thermometer-half me-2"),
            f"Temperature: {current_temp:.1f}°C"
        ], className="mb-2"),
        html.Div([
            html.I(className="fas fa-tint me-2"),
            f"Humidity: {current_humidity:.1f}%"
        ], className="mb-2"),
        html.Div([
            html.I(className="fas fa-wind me-2"),
            f"Wind Speed: {current_wind:.1f} m/s"
        ])
    ])

@app.callback(
    Output("main-chart", "figure"),
    [Input("parameter-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("chart-type", "value")]
)
def update_main_chart(parameter, start_date, end_date, chart_type):
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    if chart_type == "line":
        fig = px.line(filtered_data, x="DATETIMEDATA", y=parameter,
                     title=f"{parameter} Over Time")
    elif chart_type == "bar":
        fig = px.bar(filtered_data, x="DATETIMEDATA", y=parameter,
                    title=f"{parameter} Over Time")
    else:  # scatter
        fig = px.scatter(filtered_data, x="DATETIMEDATA", y=parameter,
                        title=f"{parameter} Over Time")
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=parameter,
        template="plotly_white"
    )
    
    return fig

@app.callback(
    Output("comparison-chart", "figure"),
    [Input("param-compare-1", "value"),
     Input("param-compare-2", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_comparison_chart(param1, param2, start_date, end_date):
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    # ลบ option trendline="ols" ออก
    fig = px.scatter(filtered_data, x=param1, y=param2,
                    title=f"Correlation between {param1} and {param2}")
    
    fig.update_layout(
        xaxis_title=param1,
        yaxis_title=param2,
        template="plotly_white"
    )
    
    return fig

@app.callback(
    Output("prediction-chart", "figure"),
    Input("parameter-filter-predict", "value")
)
def update_prediction_chart(parameter):
    # Using the last 7 days of data as "predictions" for this example
    last_week = data_pred.tail(168)  # 24 * 7 = 168 hours
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=last_week['DATETIMEDATA'],
        y=last_week[parameter],
        name='Historical',
        line=dict(color='blue')
    ))
    
    # Simulated predictions (adding random variation)
    future_dates = pd.date_range(
        start=last_week['DATETIMEDATA'].iloc[-1] + pd.Timedelta(hours=1),
        periods=24,
        freq='H'
    )
    last_value = last_week[parameter].iloc[-1]
    predictions = last_value + np.random.normal(0, 2, 24)
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predictions,
        name='Predicted',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title=f"{parameter} - Historical and Predicted Values",
        xaxis_title="Date",
        yaxis_title=parameter,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output("prediction-stats", "children"),
    Input("parameter-filter-predict", "value")
)
def update_prediction_stats(parameter):
    # Calculate some basic statistics for the predictions
    last_value = data_pred[parameter].iloc[-1]
    avg_value = data_pred[parameter].mean()
    std_value = data_pred[parameter].std()
    
    stats = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Current Value", className="card-title"),
                        html.P(f"{last_value:.2f}", className="card-text text-primary h3")
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Average", className="card-title"),
                        html.P(f"{avg_value:.2f}", className="card-text text-success h3")
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Standard Deviation", className="card-title"),
                        html.P(f"{std_value:.2f}", className="card-text text-info h3")
                    ])
                ])
            ])
        ])
    ]
    
    return stats

@app.callback(
    Output("alerts-display", "children"),
    [Input("alert-settings", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_alerts(alert_settings, start_date, end_date):
    if not alert_settings:
        return "No alerts selected"
    
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    alerts = []
    thresholds = {
        "PM25": 50,
        "PM10": 100,
        "O3": 100
    }
    
    for param in alert_settings:
        if param in filtered_data.columns:
            max_value = filtered_data[param].max()
            if max_value > thresholds[param]:
                alerts.append(
                    dbc.Alert(
                        f"Warning: {param} reached {max_value:.1f} (Threshold: {thresholds[param]})",
                        color="danger",
                        className="mb-2"
                    )
                )
    
    if not alerts:
        return dbc.Alert("No threshold violations detected", color="success")
    
    return alerts

@app.callback(
    Output("download-data", "data"),
    Input("btn-csv", "n_clicks"),
    [State("parameter-filter", "value"),
     State("date-range", "start_date"),
     State("date-range", "end_date")],
    prevent_initial_call=True
)
def export_data(n_clicks, parameter, start_date, end_date):
    if n_clicks is None:
        return None
    
    mask = (
        (data_air["DATETIMEDATA"] >= start_date)
        & (data_air["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data_air.loc[mask]
    
    return dcc.send_data_frame(
        filtered_data.to_csv,
        "air_quality_data.csv",
        index=False
    )

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link {
                color: white !important;
            }
            .card {
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .metric-value {
                font-size: 2rem;
                font-weight: bold;
            }
            .export-button {
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)