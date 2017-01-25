#!/bin/bash

#Actualizar apt
sudo apt-get update

#Instalar vagrant
sudo apt-get install -y vagrant

#Instalar el plugin vagrant-azure
sudo vagrant plugin install vagrant-azure

#Instalar pip
sudo apt-get install -y python-pip

#Actualizar pip
pip install -U pip

#Instalar ansible
sudo pip install paramiko PyYAML jinja2 httplib2 ansible

#Instalar fabric
sudo apt-get install -y fabric

# Creación y provisionamiento de la máquina virtual con vagrant y ansible
sudo vagrant up --provider=azure


#Despliegue y ejecución de la aplicación con fabric
sudo fab deploy

