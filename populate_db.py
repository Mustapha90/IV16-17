# coding=utf-8

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Bares, Tapas


def populate():
    python_cat = add_cat('LOS DIAMANTES')

    add_page(cat=python_cat,title="Boquerones")

    add_page(cat=python_cat,title="Empanada gallega")

    add_page(cat=python_cat,title="Gazpacho andaluz")

    django_cat = add_cat("EL MINOTAURO")

    add_page(cat=django_cat,title="Pimientos del piquillo")

    add_page(cat=django_cat,title="Pulpo a la gallega")

    add_page(cat=django_cat,title="Gambas al ajillo")

    frame_cat = add_cat("BABEL WORLD FUSIÓN")

    add_page(cat=frame_cat,title="Calamares fritos")

    add_page(cat=frame_cat,title="Patatas bravas")

    # Print out what we have added to the user.
    for c in Bares.objects.all():
        for p in Tapas.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, views=0):
    p = Tapas.objects.get_or_create(category=cat, title=title)[0]
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Bares.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
