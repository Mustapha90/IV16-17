#Despliegue en IaaS - Azure Vagrant + Ansible + Fabric

Primero instalamos las herramientas necesarias.

Instalamos Azure-CLI y configuramos las credenciales necesarias para administrar los servicios de Azure
con ``vagrant``

Los pasos seguidos se encuentran en este enlace:

[Instalar Azure-CLI y configurar las credenciales](https://github.com/Mustapha90/IV16-17/blob/documentacion/AzureConfig.md)

Instalamos ``Vagrant`` y el plugin ``vagrant-azure`` necesario para trabajar con ``Azure``

```
$ apt-get install vagrant
$ vagrant plugin install vagrant-azure
```

Instalamos Fabric:

``$ sudo apt-get install fabric``

Instalamos Ansible:

``$ sudo pip install paramiko PyYAML jinja2 httplib2 ansible``

Creamos un fichero ``vars.yml`` que contendrá todas variables con las que vamos a trabajar, este fichero se usará por Vagrant, Ansible y Fabric, el objetivo es separar las variables de los ficheros de despliegue para que luego, facilitar la automatización del proceso entero, he elegido el formato ``.yml`` porque todas las herramientas con las que vamos a trabajar lo soportan.

El fichero ``vars.yml`` tiene estas variables:

```yml
---

#Credenciales de azure

# Ruta absoluta del certificado de azure, previamente generado
mgmt_certificate_path: /path/to/azure_file.pem

# id de la subscripción de azure, necesario para la creación de la MV                  
subscription_id: XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX

# Datos de la máquina virtual que será creada

# Nombre de la MV
vm_name: nombre_maquina

# Nombre de usuario de la MV
vm_user: usuario_maquina

# Contraseña de la MV
vm_password: *******


#Variables de entorno de la app
# Clave secreta (Django SECRET_KEY)
SECRET_KEY: *******

# URL de la base de datos postgres 
DATABASE_URL: postgres://<USER>:<PASSWORD>@<HOST>:<PORT>/<DBNAME>

 
# Variable de entorno que indica que el entorno es de producción
EN_PROD: 1

# Variables para el despliegue
project_name: IV16-17
project_repo: https://github.com/Mustapha90/IV16-17.git
install_root: /srv
static_root: "{{ install_root }}/{{ project_name }}/static"
wsgi_module: tango_with_django_project.wsgi


# Dirección del servidor
server_name: "{{ vm_name }}.cloudapp.net www.{{ vm_name }}.cloudapp.net"


# Dependencias del sistema
system_packages:
  - git
  - nginx
  - gunicorn
  - python-setuptools
  - python-dev
  - build-essential
  - python-pip
  - libpq-dev
```

El despliegue se realizará usando dos servidores web, ``gunicorn`` y ``nginx``, el último se encargará de servir el contenido estático de la aplicación y funcionará como proxy inverso, cualquier otra petición se redirecciona a ``gunicorn``, con esta configuración logramos un buen rendimiento.

Para ello creamos un script ``Upstart`` que será copiado a ``/etc/init/gunicorn.conf`` de la máquina remota, esto permitirá controlar el ``gunicorn`` desde Fabric.

**gunicorn.j2**

```
description "Gunicorn application server handling {{ project_name }}"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid www-data
setgid www-data

# Directorio raíz de la aplicación
chdir {{ install_root }}/{{ project_name }}

#Variables de entorno de la aplicación
env PYTHONPATH={{ install_root }}/{{ project_name }}
env EN_PROD={{ EN_PROD }}
env SECRET_KEY={{ SECRET_KEY }}
env DATABASE_URL={{ DATABASE_URL }}

#Lanzar gunicorn
exec /usr/bin/gunicorn --bind 127.0.0.1:8000 {{ wsgi_module }}:application
```

**nginx.j2**

```
server {
    // Recibir peticiones en el puerto 80 
	listen 80;
	server_name {{server_name}};
	charset utf-8;

    //Ruta de ficheros estáticos
	location /static {
		alias {{ static_root }};
	}

    // Configuración de proxy inverso, redireccionar peticiones al puerto 8000 (gunicorn)
	location / {
		proxy_pass http://localhost:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
}
```
Creamos un fichero ``provision.yml`` para ``ansible``

```
---
- hosts: localhost
  vars_files:
    - vars.yml
  gather_facts: no
  become: yes

  tasks:
    - name: Instalar paquetes del sistema
      apt: pkg={{ item }} update-cache=yes cache_valid_time=3600
      with_items: "{{ system_packages }}"

    - name: Copiar el fichero de configuración de nginx
      template: src=server_config/nginx.j2 dest=/etc/nginx/sites-enabled/{{ project_name }}.conf

    - name: Copiar el fichero de configuración de gunicorn
      template: src=server_config/gunicorn.j2 dest=/etc/init/gunicorn.conf

```

Ansible se encargará de instalar los paquetes del sistema, y copiar los ficheros de configuración ``gunicorn.j2`` y ``nginx.j2`` a la máquina remota, usando la directiva ``template``, las variables que hemos visto en los ficheros de configuración se reemplazaran por su contenido antes de copiar los ficheros.

Creamos un fichero ``Vagrantfile`` con la configuración necesaria para desplegar la máquina virtual:

**Vagrantfile**

```
# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

#Cargar el fichero de variables vars.yml
current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/vars.yml")


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.33.101"
  config.vm.define "localhost" do |l|
    l.vm.hostname = "localhost"
  end

  config.vm.provider :azure do |azure, override|
    azure.mgmt_certificate = File.expand_path(configs['mgmt_certificate_path']) 
    azure.mgmt_endpoint = 'https://management.core.windows.net'
    azure.subscription_id = configs['subscription_id']
    azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_5-LTS-amd64-server-20160809.1-en-us-30GB'
    azure.vm_name = configs['vm_name']
    azure.vm_user = configs['vm_user']
    azure.cloud_service_name = configs['vm_name']  
    azure.vm_password = configs['vm_password']
    azure.vm_location = 'West Europe' 
    azure.ssh_port = '22'

    #Abrir el puerto 80
    azure.tcp_endpoints = '80:80'
  end   

  config.ssh.username = configs['vm_user']
  config.ssh.password = configs['vm_password']

  # Provisionar con ansible
  config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "provision.yml"
    ansible.verbose = "v"
    ansible.host_key_checking = false
  end

end

```

Ahora nos falta un fichero más, ``ansible_hosts`` que contendrá la información necesaria para que ``ansible`` pueda localizar la MV

```
[localhost]
192.168.33.101
```

La IP es la misma que hemos especificado en el fichero Vagrantfile.

Ya tenemos todos los ficheros necesarios para desplegar la máquina virtual.

Descargamos la "Box" de azure:

``$ vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box``

Lanzamos el despliegue:

``$ vagrant up --provider=azure``

![Imagen 1](http://i1210.photobucket.com/albums/cc420/mj4ever001/hitofinal1.png)

## Despliegue remoto con Fabric

Para desplegar la aplicación con Fabric he creado un fichero ``fabfile.py``

```
import os
import yaml
from fabric.contrib.files import exists
from fabric.api import cd, env, run, sudo, task, shell_env

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def loadenv(filepath = os.path.join(__location__, 'vars.yml')):
    """Cargar las variables del fichero vars.yml"""
    with open(filepath, 'r') as f:
        return yaml.load(f)

env.config = loadenv()
env.password = env.config['vm_password']
PROJECT_NAME = env.config['project_name']
PROJECT_ROOT = '%s/%s' % (env.config['install_root'], PROJECT_NAME)
PROJECT_REPO = env.config['project_repo']
host = env.config['vm_user'] + '@' + env.config['vm_name'] + '.cloudapp.net'
env.hosts = [host]
env.environment = 'production'


def get_repo():
    """Clonar el repositorio o actualizarlo si ya existe"""
    if exists(PROJECT_ROOT + '/' + '.git'):
        run('cd %s && git pull origin master' % (PROJECT_ROOT))
    else:
        run('git clone %s %s' % (PROJECT_REPO, PROJECT_ROOT))


def restart_gunicorn():
    "Reiniciar gunicorn"
    sudo('/etc/init.d/gunicorn restart')

def restart_nginx():
    "Reiniciar nginx"
    sudo('service nginx restart')


@task
def deploy(): 
    """Desplegar la aplicacion"""
    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.config['vm_user'], env.config['vm_user'], PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        get_repo()
        with shell_env(EN_PROD='{}'.format(env.config['EN_PROD']), SECRET_KEY='{}'.format(env.config['SECRET_KEY']), DATABASE_URL='{}'.format(env.config['DATABASE_URL'])):
            sudo('make install_prod')
            run('make migrate_')
            run('make populate')
            run('make staticfiles')

    restart_gunicorn()
    restart_nginx()
```

Este fichero permite desplegar la aplicación y también actualizarla y volver a desplegarla si ya ha sido desplegada.

Se ha usado el módulo ``shell_env`` que permite configurar las variables de entorno antes de ejecutar los comandos, por ejemplo ``make migrate`` depende de la variables de entorno ``DATABASE_URL`` para configurar la base de datos.



Para desplegar la aplicación ejecutamos:

``$ fab deploy``

No hace falta especificar el host ni la contraseña de la máquina virtual ya que estos datos y otros se cargan desde el fichero ``vars.yml``

![Imagen 2](http://i1210.photobucket.com/albums/cc420/mj4ever001/hitofinal2.png)

La aplicación se encuentra desplegada en:

[http://proyectoiv1617.cloudapp.net](http://proyectoiv1617.cloudapp.net)

