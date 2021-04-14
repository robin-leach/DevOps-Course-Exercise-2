#!/bin/bash

docker push $DOCKER_HUB_USERNAME/todo-app:latest
curl -dH -X POST "https://\$todo-app-rtl:aGoprJpovo6eCt6eJzbakEAcENNvSRRoxcP9iyAbNnSvXv7Bdxip5icaFRzt@todo-app-rtl.scm.azurewebsites.net/docker/hook"
