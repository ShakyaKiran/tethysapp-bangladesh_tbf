
import requests
# Use the API from the NWM Viewer app to get the WaterML text


def get_sfp_forecast(comid, forecasttype):
    request_params = dict(watershed_name='south_asia', subbasin_name='mainland', reach_id=comid,
                          forecast_folder='most_recent', stat_type=forecasttype)
    request_headers = dict(Authorization='Token 1f0505615ed2fbf205b8cee188939ac5b8839524')
    res = requests.get('http://tethys-staging.byu.edu/apps/streamflow-prediction-tool/api/GetForecast/',
                       params=request_params, headers=request_headers)

    # url = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=south_asia&subbasin_name=mainland&reach_id=' + comid + '&start_folder=most_recent&stat_type=' + forecasttype
    # res = requests.get(url, headers={'Authorization': 'Token 72b145121add58bcc5843044d9f1006d9140b84b'}).content
    return res