
import requests
# import numpy
import datetime as dt
# import netCDF4
# import matplotlib.pyplot as plt
# import os

# Use the API from the NWM Viewer app to get the WaterML text


def get_sfp_forecast(comid, forecasttype):

    url = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=south_asia&subbasin_name=mainland&reach_id=' + comid + '&start_folder=most_recent&stat_type=' + forecasttype
    res = requests.get(url, headers={'Authorization': 'Token 72b145121add58bcc5843044d9f1006d9140b84b'}).content
    return res