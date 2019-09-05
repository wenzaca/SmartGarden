///////////////////////// Automated Watering /////////////////////////
const autoSwitch = document.getElementById("autoSwitch");
const manualSwitch = document.getElementById("manualSwitch");

function getStatus() {
    jQuery.ajax({
        url: "/api/status",
        type: "POST",
        success: function (ndata) {
            status = ndata[0].status;
            if (status == "A") {
                autoSwitch.checked = true;
                manualSwitch.disabled = true;
                manualSwitch.checked = false;
            } else if (status == "M" || status == "F") {
                autoSwitch.checked = false;
                manualSwitch.checked = false;
            } else if (status == "O") {
                autoSwitch.checked = false;
                manualSwitch.checked = true;
                manualSwitch.checked = false;
            } else {
                autoSwitch.checked = true;
                manualSwitch.disabled = true;
                manualSwitch.checked = false;
            }
        }
    })
}

function auto() {
    let autoStatus;
    if (autoSwitch.checked) {
        autoStatus = "A";
        manualSwitch.disabled = true;
        manualSwitch.checked = false;
    } else {
        autoStatus = "M";
        manualSwitch.disabled = false;
    }
    // console.log(autoStatus);

    $.ajax({
        url: "changeStatus/" + autoStatus
    })

}

function manual() {
    let manualStatus;
    if (manualSwitch.checked) {
        manualStatus = "O";
    } else {
        manualStatus = "F";
    }
    // console.log(manualStatus);
    $.ajax({
        url: "changeStatus/" + manualStatus
    })
}

function updateSettings() {
    let max_humidity = document.getElementById("humMax").value;
    let max_temperature = document.getElementById("tempMax").value;
    let max_moisture = document.getElementById("soilMax").value;

    let jsonData = JSON.stringify({'humidity': max_humidity, 'temperature': max_temperature, 'moisture': max_moisture})

    jQuery.ajax({
        url: "/api/getMaxData",
        contentType: 'application/json',
        data: jsonData,
        type: 'POST',
        success: function () {
            $('#alert-box-success').show();
            return jsonData;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            $('#alert-box-danger').show();
            console.error(errorThrown)
        }
    })
}


function getSettings() {
    jQuery.ajax({
        url: "/api/getMaxData",
        type: 'GET',
        success: function (ndata) {
            tempValue = ndata.Items[0].temperature;
            humValue = ndata.Items[0].humidity;
            soilValue = ndata.Items[0].moisture;

            $('#humMax').attr("value", humValue);
            $('#tempMax').attr("value", tempValue);
            $('#soilMax').attr("value", soilValue);
        }
    })
}

///////////////////////// Get readings /////////////////////////
function getData() {
    jQuery.ajax({
        url: "/api/getData",
        type: "GET",
        success: function (ndata) {
            tempValue = ndata[0].Items.temperature;
            humValue = ndata[0].Items.humidity;
            soilValue = ndata[0].Items.moisture1;
            lightValue = ndata[0].Items.light;
            timeStamp = ndata[0].datetimeid;
            dateTimeStamp = new Date(Date.parse(timeStamp));

            $('#tempValue').html(tempValue);
            $('#humValue').html(humValue);
            $('#soilValue').html(soilValue);
            $('#lightValue').html(lightValue);
            $('#dateTimeStamp').html(dateTimeStamp.toLocaleTimeString() + " " + dateTimeStamp.toLocaleDateString());
        }
    })
}

/////////////////////// Get Chart data ///////////////////////
function getChartData() {
    jQuery.ajax({
        url: "/api/getChartData",
        type: "GET",
        success: function (ndata) {
            // console.log(ndata)
            const chartData = ndata;
            // console.log("Getting Chart data")

            let tempArr = [];
            let humArr = [];
            let soilArr = [];
            let lightArr = [];
            let timeArr = [];

            try {
                chartData.forEach((e) => {
                    tempArr.push(e.Items.temperature);
                    humArr.push(e.Items.humidity);
                    soilArr.push(e.Items.moisture1);
                    lightArr.push(e.Items.light);

                    let datetime = e.datetimeid;
                    // console.log(datetime);
                    jsdatetime = new Date(Date.parse(datetime));
                    jstime = jsdatetime.toLocaleTimeString();
                    timeArr.push(jstime);
                })


            } catch (e) {

            }
            createGraph(tempArr, timeArr, '#tempChart');
            createGraph(humArr, timeArr, '#humChart');
            createGraph(soilArr, timeArr, '#soilChart');
            createGraph(lightArr, timeArr, '#lightChart');
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {

        }

    })
}


// Charts
function createGraph(data, newTime, newChart) {

    let chartData = {
        labels: newTime,
        series: [data]
    };
    // console.log(chartData);

    let options = {
        axisY: {
            onlyInteger: true
        },
        fullWidth: true,
        width: '100%',
        height: '100%',
        lineSmooth: true,
        chartPadding: {
            right: 50
        }
    };
    try {
        new Chartist.Line(newChart, chartData, options);
    } catch (e) {
        console.error(e)
    }


}

/////////////////////// run functions ///////////////////////
$(document).ready(function () {
    getData();
    getStatus();
    getSettings();
    getChartData();

    setInterval(function () {
        getData();
        getChartData();
    }, 9000);
})
