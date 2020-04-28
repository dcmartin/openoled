#!/bin/bash

prerequisites()
{
  local commands=${*}
  local missing=()

  for v in ${commands}; do
    if [ -z "$(command -v ${v})" ]; then
      missing=(${missing[@]:-} ${v})
    fi
  done
  echo "${missing[@]}"
}

server()
{
  local cmd='python3 server.py'

  local pids=($(ps alxwww | egrep "${cmd}" | egrep -v grep | awk '{ print $1 }'))
  if [ ${#pids[@]} -gt 0 ] && [ ${pids} != 0 ]; then kill -9 ${pids[@]} &> /dev/stderr; fi

  export \
    OLED_HOST=${OLED_HOST} \
    OLED_PORT=${OLED_PORT} \
    && \
    ${cmd} &> /dev/null &
  echo '{"pid":'"$!"'}'
}

###
### MAIN
###

OLED_HOST=${OLED_HOST:-127.0.0.1}
OLED_PORT=${OLED_PORT:-7777}
OLED_PROTOCOL=${OLED_PROTOCOL:-http}
OLED_URL=${OLED_URL:-${OLED_PROTOCOL}://${OLED_HOST}:${OLED_PORT}/oled/v1}

if [ "${USER:-}" != 'root' ]; then echo "Run as root; sudo ${0} ${*}" &> /dev/stderr; exit 1; fi

missing=$(prerequisites python3 curl)
if [ -z "${missing:-}" ]; then
  echo $(server ${*}) | jq '.op="POST"|.url="'${OLED_URL}/display/picture'"'
else
  echo "Commands: [ ${missing} ] missing; install" &> /dev/stderr
  exit 1
fi

