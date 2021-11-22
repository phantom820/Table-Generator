FROM scratch
ADD ubuntu-18.04-minimal-cloudimg-amd64-root.tar.xz /

# install things
RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install libreoffice -y
RUN apt-get install libvips -y
RUN apt-get install default-jdk -y
RUN apt-get install texlive-latex-recommended -y
RUN apt-get install g++ -y
RUN apt-get install make -y
RUN apt-get install tralics -y
RUN apt-get update
RUN pip3 install --upgrade pip
# python dependencies
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# entrypoint
CMD ["bash"]

