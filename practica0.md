##Práctica 0

###Prerequisitos

- [x] 	Haber rellenado en la hoja de cálculo correspondiente la equivalencia entre nombre real y nick en GitHub

- [x]	Haber cumplimentado los objetivos de la primera sesión


#### Edición del perfil

En nuestra cuenta Github, elegimos la opción "Profile" y editamos los siguientes campos:

Name

Company

Location 

#### Creación de par de claves y subida a Github

1. Generamos las claves:

``ssh-keygen -t rsa -b 4096 -C "mj4ever001@gmail.com"``

2. Copiamos la clave y la añadimos a Github en la página "SSH and GPG Keys" mediante la opción "New SSH Key"

3. Comprobamos la conexión:

``ssh -T git@github.com"``

``Hi Mustapha90! You've successfully authenticated, but GitHub does not provide shell access.``


#### Configuración del nombre y dirección de correo electrónico

Para que aparezcan en los commits el nombre y correo ejecutamos las siguientes órdenes:

``git config --global user.name "Mustapha Mayo" ``

``git config --global  user.email "mj4ever001@gmail.com"``

#### Creación del repositorio

En el apartado repositorios de nuestra cuenta Github pulsamos el botón "New", rellenamos el nombre del repositorio, añadimos la licencia **GNU General Public License v3.0**, marcamos la opción para añadir el fichero README.md, y por último elegimos un fichero .gitignore adecuado para nuestro proyecto y terminamos la creación del repositorio.

#### Creación de milestone y issues
En github creamos un milestone para la entrega de la práctica 0 y creamos varios issues para este milestone.
En la página de mi proyecto, se pueden ver los diferentes issues que se han abierto y cerrado correctamente. 


#### Realizar el fork del repositorio de la asignatura

En el repositorio de la asignatura en Github (JJ/IV16-17) pulsamos el botón fork


#### Clonar el repositorio del proyecto
Ejecutamos el siguiente comando:

``git clone git@github.com:Mustapha90/IV16-17.git``

Ya tenemos una copia local del proyecto donde podemos hacer modificaciones y posteriormente hacer commits.

#### Creamos una rama donde irá la entrega de la práctica 0
Creamos la rama:

``git checkout -b hito0``

Hacemos un push:

``git push origin rama0``

Para cambiar entre ramas usamos la siguiente orden:

``git checkout "rama"``

#### Subida de la documentación de la práctica 0
En este apartado explicaremos como se realizan los commits y como se cierran los issues.

Cambiamos a la rama de la práctica 0:

``git checkout hito0``

Añadimos el fichero de la práctica 0:

``git add practica0.md``

Hacemos un commit y cerramos los issues #1 y #3:

``git commit -m "documentaćión de práctica añadida close #1 close #3"``

Hacemos un push:

``git push origin hito0``

#### Entrega de la práctica

Por último realizamos un pull request para entregar la práctica
