#!/bin/bash

function random_port {
    local check="do while"

    while [[ -n "$check" ]]; do
        local port=$(( ( RANDOM % 60000 )  + 1025 ))
        check=$(sudo netstat -ap | grep "$port")
    done

    echo "$port"
}

SMILEYCOIN_ID="$(date +%s)"
CONTAINER_NAME="smileycoin-node-${SMILEYCOIN_ID}${SMILEYCOIN_SUFFIX}"
VOLUME_NAME="$CONTAINER_NAME-data"
HOST_PORT="$(random_port)"

docker volume create "$VOLUME_NAME" > /dev/null

docker run \
    -d \
    -p "$HOST_PORT":9332 \
    --mount source="$VOLUME_NAME",destination=/smly-data\
    --name "$CONTAINER_NAME" \
    jokeswar/smileycoin-node > /dev/null

echo ""
echo "INFO:"
echo ""
echo "Container name: $CONTAINER_NAME"
echo "Volume name:    $VOLUME_NAME"
echo "Host Port:      $HOST_PORT"
docker exec "$CONTAINER_NAME" /bin/bash -c 'cat /smly-data/smileycoin.conf' | head -2
echo ""
