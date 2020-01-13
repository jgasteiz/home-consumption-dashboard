serve:
	./manage.py runserver

load_consumption:
	./manage.py migrate
	./manage.py load_consumption

load_unit_rates:
	./manage.py migrate
	./manage.py load_unit_rates
