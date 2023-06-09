#!/bin/bash

function help() {
    echo ""
    echo "smly-cli.sh submit <username> <amount> | smly-cli.sh [--help|-h]"
    echo ""
    echo "  username - the Moodle id of the student"
    echo "  amount - floating point value for the reward (e.g: 10, 10.5)"
    echo ""
    echo "smly-cli.sh info"
    echo ""
    echo "  Will return avaialble funds and the address of the wallet associated with the API key provided through"
    echo "  the 'SMILEYCOIN_API_KEY' environment variable"
    echo ""
    echo "Before running you must set '\$SMILEYCOIN_ENDPOINT' and '\$SMILEYCOIN_API_KEY' environment variables"
    echo ""
    echo "  SMILEYCOIN_ENDPOINT - the http(s) address of the smileycoin API (e.g: http://localhost:8000, make sure there are no trailing '/')"
    echo "  SMILEYCOIN_API_KEY - the API key provided by the infrastructure team that indentifies you smileycoin wallet"
    echo ""

    exit 0
}

function fail() {
    echo "$1"
    exit 1
}

[ $# -eq 0 ] && help
if [ "$1" = '-h' ] || [ "$1" = '--help' ] ; then
    help
fi

function submit() {
    local USERNAME="$1"
    local AMOUNT="$2"

    [ -n "$SMILEYCOIN_ENDPOINT" ] || fail "The environment variable '\$SMILEYCOIN_ENDPOINT' is not set"
    [ -n "$SMILEYCOIN_API_KEY" ] || fail "The environment variable '\$SMILEYCOIN_API_KEY' is not set"
    [ -n "$USERNAME" ] || fail "No username argument given"
    [ -n "$AMOUNT" ] || fail "No amount argument given"

    curl "$SMILEYCOIN_ENDPOINT/api/v1/users/$USERNAME/rewards" \
        -X POST -H "X-API-Key:$SMILEYCOIN_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "{\"amount\":$AMOUNT}"
}

function info() {
    [ -n "$SMILEYCOIN_ENDPOINT" ] || fail "The environment variable '\$SMILEYCOIN_ENDPOINT' is not set"
    [ -n "$SMILEYCOIN_API_KEY" ] || fail "The environment variable '\$SMILEYCOIN_API_KEY' is not set"

    curl "$SMILEYCOIN_ENDPOINT/api/v1/wallets" \
        -X GET -H "X-API-Key:$SMILEYCOIN_API_KEY"
}

argument="$1"
shift

if [ "$argument" = 'submit' ] ; then
    submit "$@"
elif [ "$argument" = 'info' ] ; then
    info "$@"
fi
