FROM ubuntu:14.04
MAINTAINER Mustapha Mayo

ENV EN_DOCKER=true

RUN sudo apt-get -y update

RUN sudo apt-get install -y git

RUN sudo apt-get install -y build-essential python-setuptools python-dev libpq-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

RUN sudo git clone https://github.com/Mustapha90/IV16-17.git

EXPOSE 8000

WORKDIR IV16-17
RUN make install_prod

ENTRYPOINT ["./docker_entrypoint.sh"]





