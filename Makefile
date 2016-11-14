# instalar las dependencias
install_dev:
	pip install -r requirements/dev.txt

#Crear la base de datos
migrate:
	python manage.py migrate --noinput

#rellenar la base de datos
populate:
	python populate_db.py

# lanzar tests
test:
	python manage.py test

# Lanzar la aplicación 
run:
	python manage.py runserver
