#!/bin/bash

# install os libraries that are needed
apt-get install libvips -y
apt-get install default-jdk -y
apt-get install texlive-latex-recommended -y
apt-get install texlive-latex-extra -y
apt-get install g++ -y
apt-get install make -y
apt-get install tralics -y
apt-get install wget xfonts-75dpi -y
apt-get install xfonts-base -y
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
apt-get install wkhtmltopdf -y

# install python libraries
pipenv install

