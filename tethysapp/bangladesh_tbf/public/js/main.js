//Get the select value in the map, extract comid and send to python for the data to plot
$(function() { //wait for page to load
    get_time_seriesNew('58532');
    var mapjs = TETHYS_MAP_VIEW.getMap();
    var vectorLayer = mapjs.getLayers().getArray()[1]
    select_interaction = new ol.interaction.Select({
        layers: [vectorLayer],
    });
    mapjs.addInteraction(select_interaction);

    select_interaction.on('select', function (e) {
        var comid = e.selected[0].get('comid');
        get_time_seriesNew(comid);
    });
});

function myFormat(timestamp) {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];
    var period, t;
    t = new Date(timestamp);
    if (t.getHours() === 0 ) {
        period = monthNames[t.getMonth()] + " " + (t.getDate());
    }
    else {
        period = "";
    }
    // period =  monthNames[t.getMonth()] + " " + (t.getDate() + ", T ") + (t.getHours() + ":") + (t.getMinutes());
    return period;
}

$.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!checkCsrfSafe(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                }
            }
        });

j2Array = function(myData){
    var result = [];
    alert(myData.length)
    // for(var i in mydate)
    //     alert(i);
    //     // result.push([i, json_data [i]]);
}

checkCsrfSafe = function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

getCookie = function (name) {
        var cookie;
        var cookies;
        var cookieValue = null;
        var i;

        if (document.cookie && document.cookie !== '') {
            cookies = document.cookie.split(';');
            for (i = 0; i < cookies.length; i += 1) {
                cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

get_time_seriesNew = function(myID){

    $('.warning').html('');
//      var datastring = $get_time_seriesNew.serialize();
        $.ajax({
            type:"POST",
            url:'/apps/bangladesh-tbf/plotMap/',
            dataType:'json',
            // processData: false,
            // contentType: false,
            data:{
                    'comid': myID,
                },
             "beforeSend": function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success:function(result){
                json_response = result;
                var xVal = [];
                var vMean = [];
                var vstdupper =[];
                var vstdlower = [];
                var vUpper = [];
                var vLower = []
                if (json_response.success == "success")
                {
                    json_response.dateTimewa.forEach(function (element) {

                        // xVal1 = new Date(JSON.stringify(json_response.dateTimewa[i])); //.substring(1,11)));
                        // alert(json_response.dateTimewa[i]);
                        // alert(JSON.stringify(json_response.dateTimewa[i]));
                        xVal.push(element);
                    });

                    for (i in json_response.valuemean) {
                        vMean.push(parseFloat(json_response.valuemean[i]));
                    }

                    for (i in json_response.valuestdupper) {
                        vstdupper.push(parseFloat(json_response.valuestdupper[i]));
                    }

                    for (i in json_response.valuestdlower) {
                        vstdlower.push(parseFloat(json_response.valuestdlower[i]));
                    }

                    for (i in json_response.valueupper) {
                        vUpper.push(parseFloat(json_response.valueupper[i]));
                    }

                    for (i in json_response.valuelower) {
                        vLower.push(parseFloat(json_response.valuelower[i]));
                    }

                    $('.warning').html('');
                    $('#plotter').highcharts({
                        chart: {
                            type:'line',
                            zoomType: 'x'
                        },
                        credits: {
                            enabled: false
                        },
                        tooltip:{
                            shared: true,
                            useHTML: true,
                            formatter: function () {
                                // var s ='<b>' + json_response.display_name + '<br/>';
                                var s = '<h5>' + this.x.replace("T", " T") + '</h5><table>';
                                $.each(this.points, function () {
                                    s += '<tr><td>' + this.series.name + '</td><td>: ' + this.y + '</td></tr>';
                                });
                                s += '</table>'
                                return s;
                            }

                        },
                        title: {
                            text: json_response.display_name,  //+ " values at " +json_response.location,
                            style: {
                                fontSize: '14px'
                            }
                        },
                        xAxis: {
                            categories: xVal,
                            type: 'date',
                            labels: {
                                formatter: function () {
                                    return myFormat(this.value);
                                },
                                rotation: -45,
                                align: 'right'
                            },
                            title: {
                                text: 'Date Time'
                            }
                        },
                        yAxis: {
                            title: {
                                text: "Flow Prediction (cm)" //json_response.units
                            }
                        },
                        exporting: {
                            enabled: true
                        },
                        series: [
                            {
                                data: vUpper,
                                name: "Outer Range Upper"
                            },
                            {
                                data:vMean,
                                name: "Mean",
                                pointPlacement: 'on'
                            },
                            {
                                data: vstdupper,
                                name: "StdDev Range Upper"
                            },
                            {
                                data: vstdlower,
                                name: "StdDev Range Lower"
                            },
                            {
                                data: vLower,
                                name: "Outer Range Lower"
                            }
                        ],


                    });
                }
            },
            error:function(request,status,error){
                $('.warning').html('<b style="color:red">'+error+'. Please select another point and try again.</b>');
            }

        });
};



//function get_time_series(comid) {
//        $.ajax({
//                type: 'POST',
//                url: '',
//                dataType: 'json',
//                data: {
//                    'comid': comid,
//                },
//                success: function(data)
//                {
//                    if(data.is_taken){
//                        alert(data.error_message);
//                        }
//                }
//            })
//        };

get_ts = function(){
        $('.warning').html('');
        var datastring = $get_ts.serialize();

        $.ajax({
            type:"POST",
            url:'/apps/lis-viewer/get-ts/',
            dataType:'HTML',
            data:datastring,
            success:function(result){
                var json_response = JSON.parse(result);
                if (json_response.success == "success"){
                    $('.warning').html('');
                    $('#plotter').highcharts({
                        chart: {
                            type:'area',
                            zoomType: 'x'
                        },
                        title: {
                            text: json_response.display_name + " river ",
                            style: {
                                fontSize: '14px'
                            }
                        },
                        xAxis: {
                            type: 'datetime',
                            labels: {
                                format: '{value:%d %b %Y}',
                                rotation: 45,
                                align: 'left'
                            },
                            title: {
                                text: 'Date'
                            }
                        },
                        yAxis: {
                            title: {
                                text: 'mm'//json_response.units
                            }

                        },
                        exporting: {
                            enabled: true
                        },
                        series: [{
                            data:json_response.values,
                            name: json_response.variable
                        }]

                    });
                }
            },
            error:function(request,status,error){
                $('.warning').html('<b style="color:red">'+error+'. Please select another point and try again.</b>');
            }

        });
    };

