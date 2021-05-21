#!/bin/bash

# Create and enable a virtual environment
python -m venv env
source env/bin/activate

# Install required packages
poetry install

# Create a .env file from the .env.template
cp -n .env.template .env
