# instalar las dependencias
install:
	pip install -r requirements.txt
# lanzar tests
test:
	python manage.py test
#rellenar la base de datos
populate:
	python populate_rango.py
# Lanzar la aplicación 
execute:
	python manage.py runserver
#Crear la base de datos (sqlite3)
createdb:
	python manage.py migrate --noinput



