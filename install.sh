#!/bin/bash

set -e

# Check if running in local development mode
if [ "$LOCAL_DEV" == "1" ]; then
    echo "Running in local development mode"
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip and install Poetry
pip3 install --upgrade pip
pip3 install poetry

# Configure Poetry based on the environment
if [ "$LOCAL_DEV" == "1" ]; then
    poetry config virtualenvs.in-project true
else
    poetry config virtualenvs.create false
fi

# Install dependencies using Poetry
poetry install
