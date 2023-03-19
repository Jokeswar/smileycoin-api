#!/bin/bash

function random_port {
    local CHECK="do while"

    while [[ ! -z $CHECK ]]; do
        local PORT=$(( ( RANDOM % 60000 )  + 1025 ))
        CHECK=$(sudo netstat -ap | grep $PORT)
    done

    echo $PORT
}

SMILEY_COIN_ID="$(date +%s)"
CONTAINER_NAME="smileycoin-node-${SMILEY_COIN_ID}"
VOLUME_NAME="$CONTAINER_NAME-data"
HOST_PORT="$(random_port)"

docker volume create "$VOLUME_NAME"

docker run \
    -d \
    -p "$HOST_PORT":9332 \
    --mount source="$VOLUME_NAME",destination=/smly-data\
    --name "$CONTAINER_NAME" \
    smileycoin-node
