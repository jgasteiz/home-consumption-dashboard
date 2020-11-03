/* global Chart */
(() => {
    const consumption = JSON.parse(document.getElementById('consumption').dataset.consumption);
    const chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };

    let consumptionData = [],
        kwhPriceInPence = [],
        amountPayableInPence = [],
        consumptionLabels = [];

    consumption.forEach((c) => {
        consumptionLabels.push(`${c["interval_start"]} to ${c["interval_end"]}`);
        consumptionData.push(c["consumption"]);
        kwhPriceInPence.push(c["value_inc_vat"]);
        amountPayableInPence.push(c["payable_in_pence"]);
    });

    // Consumption chart
    new Chart(document.getElementById('chart-consumption'), {
        type: 'bar',
        data: {
            labels: consumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.blue).alpha(0.5).rgbString(),
                label: 'kWh used',
                data: consumptionData,
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

    // Unit rates chart
    new Chart(document.getElementById('chart-unit-rates'), {
        type: 'bar',
        data: {
            labels: consumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.red).alpha(0.5).rgbString(),
                label: 'kWh price in pence',
                data: kwhPriceInPence,
                borderWidth: 1,
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

    // Payable chart
    new Chart(document.getElementById('chart-payable'), {
        type: 'bar',
        data: {
            labels: consumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.purple).alpha(0.5).rgbString(),
                label: 'Amount payable in pence',
                data: amountPayableInPence,
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
