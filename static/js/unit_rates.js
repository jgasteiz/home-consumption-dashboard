/* global Chart */
(() => {
    const unitRates = JSON.parse(document.getElementById('unit-rates').dataset.unitRates);

    let unitRatesData = [],
        unitRatesLabels = [];
    unitRates.forEach((c) => {
        if (c["valid_from"].indexOf(':00') > -1) {
            unitRatesLabels.push(c["valid_from"]);
        } else {
            unitRatesLabels.push("");
        }
        unitRatesData.push(c["value_inc_vat"]);
    });

    const ctx = document.getElementById('chart');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: unitRatesLabels,
            datasets: [{
                // TODO: make this better...
                backgroundColor: Chart.helpers.color('rgb(153, 102, 255)').alpha(0.5).rgbString(),
                label: 'Pence',
                data: unitRatesData,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
})();
