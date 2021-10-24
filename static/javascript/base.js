$(document).ready(function(){
    $("#btn").click(function() {
        $(".sidebar").toggleClass("active");
    });

    $("#log-out").click(function() {
        $(".logout-popup").toggleClass("is-visible");
    });

    $("#goback-panel").click(function()  {
        $(".logout-popup").toggleClass("is-visible");
    });
    // some pages do not use the chart, so we will avoid loading the code
    if (document.getElementById("line-chart") != null) {
        updateStockChart();
    }
});

var ctx = (document.getElementById("line-chart") != null) ? document.getElementById("line-chart").getContext("2d") : null;
setInterval(function() {
    updateStockChart();
}, 60000);

function updateStockChart() {
    // some pages do not use the chart, so we will avoid loading the code on a null
    if (document.getElementById("line-chart") == null) {
        return; // stop trying to update data into a missing chart
    }
    $.getJSON($SCRIPT_ROOT + '/mypinnedticker', function(data) {
        var lineChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Price",
                        data: data.close,
                        fill: true,
                        lineTension: 0.1,
                        backgroundColor: 'rgba(27, 25, 52, 0.8)'
                    }
                ]
            },
            options: {
                responsive: false,
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'xy',
                        }
                    }
                }
            }
        });
    });
}