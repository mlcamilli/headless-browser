FROM ubuntu:14.04.4
RUN apt-get update --fix-missing
RUN apt-get install -y chromium-browser python3-pip python3-dev git firefox
RUN apt-get install -y unzip wget xvfb nodejs-legacy npm
RUN wget http://chromedriver.storage.googleapis.com/2.19/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/bin/
RUN chmod a+x /usr/bin/chromedriver
RUN npm install -g phantomjs
RUN pip3 install git+https://github.com/mlcamilli/headless-browser.git#egg=headless-browser==0.0.3
