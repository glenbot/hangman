FROM python:3.5.2-slim

# Install some packages
RUN apt-get update
RUN apt-get install -y telnet screen

# Add screenrc
ADD .screenrc /root/.screenrc

# Install requirements
ADD requirements.pip /tmp/requirements.pip
RUN python3 -m pip install -r /tmp/requirements.pip

ADD . /code/hangman
RUN python3 -m pip install -e /code/hangman