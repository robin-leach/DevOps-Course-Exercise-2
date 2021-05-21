FROM python:3.8.5-buster as base
RUN pip install "poetry==1.0.10"
COPY . ./app
WORKDIR /app
RUN poetry config virtualenvs.create false --local && \
  poetry install

FROM base as production
CMD poetry run gunicorn -b 0.0.0.0:${PORT} 'app:create_app()'

FROM base as development
EXPOSE 5000
ENTRYPOINT ["./scripts/run-dev.sh"]

FROM base as test
RUN apt-get update &&\
  apt-get upgrade -y &&\
  curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
  apt-get install ./chrome.deb -y &&\
  rm ./chrome.deb
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
 echo "Installing chromium webdriver version ${LATEST}" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip
ENTRYPOINT [ "poetry", "run", "pytest" ]
