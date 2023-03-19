#!/bin/bash

docker run --name mongo \
            -p "${MONGODB_PORT}":27017 \
            -e "MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}" \
            -e "MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_USERNAME}" \
            -d \
            mongo:5.0.15
