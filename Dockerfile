FROM python:3.8.5-buster as base
RUN pip install "poetry==1.0.10"
COPY . ./app
WORKDIR /app
RUN poetry install

FROM base as production
RUN pip install gunicorn flask
EXPOSE 8000
ENTRYPOINT ["./run-prod.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["./run-dev.sh"]

FROM base as test
# Install Chrome
RUN apt-get update &&\
  apt-get upgrade -y &&\
  curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
  apt-get install ./chrome.deb -y &&\
  rm ./chrome.deb
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
 echo "Installing chromium webdriver version ${LATEST}" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip
ENTRYPOINT [ "poetry", "run", "pytest" ]