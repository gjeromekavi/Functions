import azure.functions as func
import logging
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="forecast", methods=["POST"])
def forecast(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for forecasting.')

    try:
        # Parse request body
        req_body = req.get_json()
        forecast_length = req_body.get('forecast_length', 10)  # Default to 10 if not provided

        # Generate dummy time series data
        np.random.seed(0)
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        data = np.random.randn(100).cumsum()

        df = pd.DataFrame(data, index=dates, columns=['value'])

        # Fit a simple forecasting model (Holt-Winters Exponential Smoothing)
        model = ExponentialSmoothing(df['value'], trend='add', seasonal='add', seasonal_periods=12).fit()

        # Forecast the next 'forecast_length' days
        forecast = model.forecast(forecast_length)

        # Create a response dictionary
        response = {
            "forecast_dates": forecast.index.strftime('%Y-%m-%d').tolist(),
            "forecast_values": forecast.values.tolist()
        }

        return func.HttpResponse(body=json.dumps(response), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error in processing the request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
