install:
	pip install -r requirements.txt
test:
	python manage.py test
populate:
	python populate_rango.py
execute:
	python manage.py runserver



