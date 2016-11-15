# instalar las dependencias
install_dev:
	pip install -r requirements/dev.txt

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

# Lanzar la aplicación 
run:
	python manage.py runserver

deploy:
	heroku apps:create --region eu
	heroku addons:create heroku-postgresql:hobby-dev
	heroku config:set SECRET_KEY=`openssl rand -base64 32`
	git push heroku master
	python manage.py migrate --noinput
	python populate_db.py
	heroku open
