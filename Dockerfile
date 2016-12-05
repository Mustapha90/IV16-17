FROM ubuntu:14.04
MAINTAINER Mustapha Mayo

RUN sudo apt-get -y update

RUN sudo apt-get install -y git

RUN sudo apt-get install -y build-essential python-setuptools python-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

RUN sudo git clone https://github.com/Mustapha90/IV16-17.git
RUN cd IV-1617 && make install_dev 
RUN make migrate
RUN make populate

