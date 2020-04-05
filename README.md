# Home Consumption Dashboard

![Screenshot](https://imgur.com/KrEhCGI.png)

## Disclaimer

The code on this repo will only work if you're an Octopus Energy customer and 
you're a customer of the Agile tariff: https://octopus.energy/agile/.

That's because this repo will try to use Octopus Energy API for fetching your daily half hourly
unit rates and consumption, which will only be available if you're an Agile customer.

## How to get this up and running

### Install dependencies and create db

```shell script
# Create a virutal env, install the requirements and create the db.
mkvirtualenv home-consumption-dashboard
pip install -r requirements.txt
./manage.py migrate
```

### Fill in environment variables

```shell script
# Copy the example env file to .env
cp .env.example .env
```

Fill in the following variables with values from your Octopus Energy account dashboard - these
can be found in the developer section: https://octopus.energy/dashboard/developer/.

```dotenv
API_KEY=
MPAN=
METER_SERIAL_NUMBER=
PRODUCT_CODE=
TARIFF_CODE=
```


### Populate consumption and unit rates data

```shell script
make load_consumption
make load_unit_rates
```

### Run the server

```shell script
make serve
```
