#!/bin/bash

listen()
{
  local temp=$(mktemp)

  while true; do
    if [ "${DEBUG:-false}" = 'true' ]; then echo "Waiting" &> /dev/stderr; fi
    mosquitto_sub -C 1 -h ${MQTT_HOST} -u ${MQTT_USERNAME} -P ${MQTT_PASSWORD} -t "${MQTT_TOPIC}" > ${temp}
    if [ -s ${temp} ] && [ $(jq '.image!=null' ${temp}) = 'true' ]; then
      if [ "${DEBUG:-false}" = 'true' ]; then echo "Displaying" &> /dev/stderr; fi
      curl -qsSL -d @${temp} ${OLED_URL}/display/picture
    else
      if [ "${DEBUG:-false}" = 'true' ]; then echo "Skipping" &> /dev/stderr; fi
    fi
  done
}

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

###
### MAIN
###

OLED_HOST=${OLED_HOST:-127.0.0.1}
OLED_PORT=${OLED_PORT:-7777}
OLED_PROTOCOL=${OLED_PROTOCOL:-http}
OLED_URL=${OLED_URL:-${OLED_PROTOCOL}://${OLED_HOST}:${OLED_PORT}/oled/v1}

MOTION_GROUP=${MOTION_GROUP:-+}
MOTION_CLIENT=${MOTION_CLIENT:-+}
MQTT_HOST=${MQTT_HOST:-127.0.0.1}
MQTT_USERNAME=${MQTT_USERNAME:-username}
MQTT_PASSWORD=${MQTT_PASSWORD:-password}
MQTT_TOPIC=${MQTT_TOPIC:-${MOTION_GROUP}/${MOTION_CLIENT}/+/event/end/+}

missing=$(prerequisites mosquitto_sub curl jq)
if [ -z "${missing:-}" ]; then
  exit $(listen ${*})
else
  echo "Commands: [ ${missing} ] missing; install" &> /dev/stderr
  exit 1
fi
