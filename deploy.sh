#!/bin/bash

docker push $DOCKER_HUB_USERNAME/todo-app:latest
docker tag robinleach/todo-app:latest registry.heroku.com/rtl-todo-app/web
docker push registry.heroku.com/rtl-todo-app/web
heroku container:release web -a rtl-todo-app