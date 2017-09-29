from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from .helper import get_sfp_forecast
import datetime as dt
from .app import BangladeshTbf as app
import urlparse, json, datetime
from django.http import JsonResponse, HttpResponse

@login_required()
def home(request):
    map_layers = []
    layerID = "bangladeshLayers:bangPoint"

    ## Check if the click is done in a map po1nts
    pointID = 0
    riverNm = ''
    if request.method == 'POST' and 'comid' in request.POST:
        pointID = str(request.GET['comid'])
        if pointID == str(59396):
            riverNm = 'Barmaputra'
        else:
            riverNm = 'Ganga'
            pointID == str(61067)
    else:
        pointID = str(61067)
        riverNm = 'Ganga'

    geoserver_engine = app.get_spatial_dataset_service(name='mainGeoserver', as_engine=True)
    response = geoserver_engine.get_layer(layerID, debug=True)

    kmlurl = response['result']['wms']['kml']
    parsedkml = urlparse.urlparse(kmlurl)
    bbox = urlparse.parse_qs(parsedkml.query)['bbox'][0]
    bboxitems = bbox.split(",")
    box_left = float(bboxitems[0])
    box_right = float(bboxitems[2])
    box_top = float(bboxitems[3])
    box_bottom = float(bboxitems[1])
    centerlat = (box_left + box_right) / 2
    centerlong = (box_top + box_bottom) / 2

    geojson_object ={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        88.22671092739853,
                        24.43924635981767
                    ]
                },
                "properties": {
                    "Id": 61067,
                    "comid": 61067
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        89.85729091391491,
                        25.758600164896688
                    ]
                },
                "properties": {
                    "Id": 59396,
                    "comid": 59396
                }
            }
        ]
    }

    geojson_layer = MVLayer(source='GeoJSON',
                            options=geojson_object,
                            legend_title='LEGENDS',
                            legend_extent=[box_left, box_bottom, box_right, box_top],
                            legend_classes=[
                                MVLegendClass('point', 'River Points', fill='#00FF00', stroke='#000000')
                            ],
                            layer_options = {
                                'style': {
                                    'image': {
                                        'circle': {
                                            'radius': 5,
                                            'fill': {'color': '#00FF00'},
                                            'stroke': {'color': '#000000', 'width': 1},
                                        }
                                    }
                                }
                            }
                            )

    map_layers.append(geojson_layer)

    view_options = MVView(
        projection='EPSG:4326',
        center=[centerlat, centerlong],
        zoom=4,
        maxZoom=18,
        minZoom=2
    )
    map_options = MapView(
        height='500px',
        width='100%',
        layers=map_layers,
        legend=True,
        view=view_options
    )
    tbf_plot = plotBack(pointID, riverNm)
    print (tbf_plot)

    context = {'map_options': map_options,'tbf_plot': tbf_plot}
    return render(request, 'bangladesh_tbf/home.html', context)

# def set_default(obj):
#     if isinstance(obj, set):
#         return list(obj)
#     raise TypeError

def plotMap(request):
    comid = request.POST.get("comid", "")
    return_obj = {}

    if comid == str(59396):
        riverNm = 'Barmaputra'
    else:
        riverNm = 'Ganga'
        comid == str(61067)
    return_obj = plotNew(comid, riverNm)
    #return_obj = json.dumps(return_obj)
    # print(" --------------------------- start --------------------------")
    # print(return_obj)
    return HttpResponse(return_obj, content_type='application/json')
    #return JsonResponse(return_obj, safe=False)

def plotNew(id, riverNm):
    dateraw = []
    datemean = []
    valuemean = []
    valuestdupper = []
    valuestdlower = []
    valuelower = []
    valueupper = []
    return_obj = {}

    comid = id  # Ganges
    forecasttype = 'mean'

    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)

    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuemean.append(parser[1].split('<')[0])
    for e in dateraw:
        mydate = dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S")
        datemean.append(mydate)

    forecasttype = 'std_dev_range_upper'
    dateraw = []
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdupper.append(parser[1].split('<')[0])

    forecasttype = 'std_dev_range_lower'
    dateraw = []
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdlower.append(parser[1].split('<')[0])

    forecasttype = 'outer_range_upper'
    dateraw = []
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valueupper.append(parser[1].split('<')[0])

    forecasttype = 'outer_range_lower'
    dateraw = []
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuelower.append(parser[1].split('<')[0])

        # datemean.append((e))
    # print (datemean)
    # discharge_time_series = []
    # formatter_string = "%m/%d/%Y"
    # counter = 0
    # for item in datemean:
    #     discharge_time_series.append([item, float(valuemean[counter])])
    #     counter = counter + 1

    return_obj["valuestdlower"] = (valuestdlower)
    return_obj["valuestdupper"] = (valuestdupper)
    return_obj["valueupper"] = (valueupper)
    return_obj["valuelower"] = (valuelower)
    return_obj["valuemean"] = (valuemean)
    return_obj["success"] = "success"
    return_obj["display_name"] = riverNm
    return_obj["dateTimewa"] = (datemean)



    # print (discharge_time_series)
    # tbf_plot = TimeSeries(
    #     engine='highcharts',
    #     title=riverNm,
    #     y_axis_title='Discharge',
    #     y_axis_units='cms',
    #     series=[
    #         {
    #             'name': 'Mean',
    #             'color': '#0066ff',
    #             'data': discharge_time_series,
    #         },
    #     ],
    #     width='100%',
    #     height='300px'
    # )
    return JsonResponse(return_obj) #discharge_time_series

    # context = {
    #
    #     'tbf_plot': tbf_plot
    # }
    # return render(request, 'bangladesh_tbf/Ganges.html', context)


def ganges(request):
    print ("SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFE andDDDDDDDDDDDDDDDDDDDDDDD sound")
    dateraw = []
    datemean = []

def plotBack(id, riverNm):
    dateraw = []
    datemean = []
    valuemean = []
    datehighres = []
    valuehighres = []
    datestdupper = []
    valuestdupper = []
    datestdlower = []
    valuestdlower = []
    dateupper = []
    valueupper = []
    datelower = []
    valuelower = []
    # This is where you can change the input and rerun to get a different stream, forecast configuration, and time
    # You can identify different COMID's from the NHDPlus or use the NWM Forecast Viewer App at https://apps.hydroshare.org/apps/
    # This is my stream at location x
    #mean
    comid = id  #Ganges
    #comid = '59396'  #BArmaPura
    #comid = '63610'
    forecasttype = 'mean'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    #print (watermlstring)
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuemean.append(parser[1].split('<')[0])
    for e in dateraw:
        datemean.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #high_res
    dateraw = []

    forecasttype = 'high_res'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    #print (watermlstring)
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuehighres.append(parser[1].split('<')[0])
    for e in dateraw:
        datehighres.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #std_dev_range_upper
    dateraw = []

    forecasttype = 'std_dev_range_upper'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdupper.append(parser[1].split('<')[0])
    for e in dateraw:
        datestdupper.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #std_dev_range_lower
    dateraw = []

    forecasttype = 'std_dev_range_lower'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdlower.append(parser[1].split('<')[0])
    for e in dateraw:
        datestdlower.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #outer_range_upper
    dateraw = []

    forecasttype = 'outer_range_upper'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valueupper.append(parser[1].split('<')[0])
    for e in dateraw:
        dateupper.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #outer_range_lower
    dateraw = []

    forecasttype = 'outer_range_lower'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuelower.append(parser[1].split('<')[0])
    for e in dateraw:
        datelower.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))

        # Configure the time series Plot View

    discharge_time_series = []
    formatter_string = "%m/%d/%Y"
    counter  = 0
    for item in datemean:
       # mytime = (dt.datetime.strptime(item, "%Y-%m-%dT%H:%M:%S"))
        discharge_time_series.append([item, float(valuemean[counter])])
        counter = counter + 1


    tbf_plot = TimeSeries(
            engine='highcharts',
            title=riverNm,
            y_axis_title='Discharge',
            y_axis_units='cms',
            series=[
                {
                    'name': 'Mean',
                    'color': '#0066ff',
                    'data': discharge_time_series,
                },
            ],
            width='100%',
            height='300px'
        )
    return tbf_plot

    # context = {
    #
    #     'tbf_plot': tbf_plot
    # }
    # return render(request, 'bangladesh_tbf/Ganges.html', context)