# instalar las dependencias de desarrollo/test
install_dev:
	pip install -r dev_requirements.txt

install_prod:
	pip install -r requirements.txt

#Crear la base de datos
migrate:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
    
#rellenar la base de datos
populate:
	python populate_db.py

# lanzar tests
test:
	python manage.py test

run_prod:
	python manage.py collectstatic --noinput
	gunicorn tango_with_django_project.wsgi --log-file -

# Lanzar la aplicación 
run:
	python manage.py collectstatic --noinput
	python manage.py runserver

# Desplegar la aplicación en Heroku
deploy:
	heroku apps:create --region eu
	heroku addons:create heroku-postgresql:hobby-dev
	heroku config:set SECRET_KEY=`openssl rand -base64 32`
	git push heroku master
	heroku run python manage.py migrate --noinput
	heroku run python populate_db.py
	heroku open
