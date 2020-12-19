/* global Chart */
(() => {
    const elecConsumption = JSON.parse(document.getElementById('consumption').dataset.elecConsumption);
    const gasConsumption = JSON.parse(document.getElementById('consumption').dataset.gasConsumption);
    const chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };

    let elecConsumptionData = [],
        gasConsumptionData = [],
        elecKwhPriceInPence = [],
        elecAmountPayableInPence = [],
        elecConsumptionLabels = [],
        gasConsumptionLabels = [],
        gasAmountPayableInPence = [];

    elecConsumption.forEach((c) => {
        elecConsumptionLabels.push(`${c["interval_start"]} to ${c["interval_end"]}`);
        elecConsumptionData.push(c["consumption"]);
        elecKwhPriceInPence.push(c["value_inc_vat"]);
        elecAmountPayableInPence.push(c["payable_in_pence"]);
    });
    gasConsumption.forEach((c) => {
        gasConsumptionLabels.push(`${c["interval_start"]} to ${c["interval_end"]}`);
        gasConsumptionData.push(c["consumption"]);
        gasAmountPayableInPence.push(c["payable_in_pence"]);
    });

    // Elec consumption chart
    new Chart(document.getElementById('chart-elec-consumption'), {
        type: 'bar',
        data: {
            labels: elecConsumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.blue).alpha(0.5).rgbString(),
                label: 'kWh used',
                data: elecConsumptionData,
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

    // Gas consumption chart
    new Chart(document.getElementById('chart-gas-consumption'), {
        type: 'bar',
        data: {
            labels: gasConsumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.orange).alpha(0.5).rgbString(),
                label: 'kWh used',
                data: gasConsumptionData,
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

    // Elec unit rates chart
    new Chart(document.getElementById('chart-elec-unit-rates'), {
        type: 'bar',
        data: {
            labels: elecConsumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.red).alpha(0.5).rgbString(),
                label: 'kWh price in pence',
                data: elecKwhPriceInPence,
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

    // Elec payable chart
    new Chart(document.getElementById('chart-elec-payable'), {
        type: 'bar',
        data: {
            labels: elecConsumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.purple).alpha(0.5).rgbString(),
                label: 'Amount payable in pence',
                data: elecAmountPayableInPence,
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

    // Gas payable chart
    new Chart(document.getElementById('chart-gas-payable'), {
        type: 'bar',
        data: {
            labels: gasConsumptionLabels,
            datasets: [{
                backgroundColor: Chart.helpers.color(chartColors.purple).alpha(0.5).rgbString(),
                label: 'Amount payable in pence',
                data: gasAmountPayableInPence,
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
