#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"/.. || exit 1

gunicorn -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app
