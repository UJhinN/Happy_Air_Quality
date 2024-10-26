# Air Quality Analytics Dashboard

This is an interactive web application built with Dash and Plotly for monitoring and analyzing air quality metrics. The dashboard provides real-time visualization of various air quality parameters, weather conditions, and predictive analytics.

## Features

- **Real-time Air Quality Monitoring**
  - View current AQI (Air Quality Index) status
  - Monitor multiple air quality parameters (PM2.5, PM10, O3, NO2)
  - Track temperature, humidity, and wind speed

- **Interactive Data Visualization**
  - Line charts, bar charts, and scatter plots
  - Parameter comparison and correlation analysis
  - Customizable date range selection
  - Export data to CSV format

- **Predictive Analytics**
  - View future air quality predictions
  - Analysis of historical trends
  - Statistical insights and metrics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/UJhinN/Happy_Air_Quality.git
cd Happy_Air_Quality
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Required Packages

- Flask
- Dash
- pandas
- plotly
- dash-bootstrap-components
- numpy

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

## Dashboard Components

### Analysis Page
- **Parameter Selection**: Choose from various air quality metrics
- **Date Range Filter**: Select specific time periods for analysis
- **Chart Type Selection**: Switch between different visualization types
- **AQI Display**: Real-time Air Quality Index with status indicator
- **Weather Information**: Current temperature, humidity, and wind speed
- **Parameter Comparison**: Correlation analysis between different metrics
- **Alert System**: Customizable alerts for parameter thresholds

### Prediction Page
- **Future Trends**: View predicted values for selected parameters
- **Statistical Analysis**: Track key statistics and variations
- **Historical Comparison**: Compare predictions with historical data

## Data Format

The application expects data with the following columns:
- DATETIMEDATA: Timestamp
- PM25: PM2.5 levels
- PM10: PM10 levels
- O3: Ozone levels
- NO2: Nitrogen dioxide levels
- Temperature: Temperature in Celsius
- Humidity: Relative humidity percentage
- WindSpeed: Wind speed in m/s

## Customization

You can modify the following aspects of the dashboard:
- Alert thresholds in the `update_alerts` callback
- AQI calculation parameters in the `calculate_pm25_aqi` function
- Chart types and visualization options
- Prediction model parameters


## member
นายสุธินันท์ รองพล 6610110341

นายณัฐดนัย ชูกูล 66110110475


