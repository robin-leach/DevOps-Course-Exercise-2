#!/bin/bash

terraform init
terraform apply \
  -var="client_id=$CLIENT_ID" \
  -var="client_secret=$CLIENT_SECRET" \
  -var="prefix=$PRODUCTION_ENV_PREFIX" \
  -var="loggly_token=$LOGGLY_TOKEN" \
  -auto-approve

docker push $DOCKER_HUB_USERNAME/todo-app:latest
curl -dH -X POST "$(terraform output -raw webhook_url)"
