#!/bin/bash

###
### FUNCTIONS
###

## test for commands
has_commands()
{
  if [ "${DEBUG:-false}" = 'true' ]; then echo "${FUNCNAME[0]} ${*}" &> /dev/stderr; fi

  local cmds=${*}
  local missing=()

  for v in ${cmds}; do
    if [ -z "$(command -v ${v})" ]; then
      missing=(${missing[@]:-} ${v})
    fi
  done
  echo "${missing[@]}"
}

## test for group privileges
has_groups()
{
  if [ "${DEBUG:-false}" = 'true' ]; then echo "${FUNCNAME[0]} ${*}" &> /dev/stderr; fi

  local nessed=${*}
  local missing=()
  local has=($(groups ${USER} | awk -F: '{ print $2 }'))

  if [ ${#has[@]} -gt 0 ]; then
    for v in ${need}; do
      local match=false

      for g in ${has[@]}; do
        if [ "${v}" = "${g}" ]; then
          if [ "${DEBUG:-false}" = 'true' ]; then echo "FOUND: ${v}" &> /dev/stderr; fi
          match=true
          break
        fi
      done
      if [ "${match:-false}" = 'false' ]; then
        if [ "${DEBUG:-false}" = 'true' ]; then echo "MISSING: ${v}" &> /dev/stderr; fi
        missing=(${missing[@]:-} ${v})
      fi
    done
  else
    missing=(${need})
  fi
  echo "${missing[@]}"
}

## PRIMARY
server()
{
  if [ "${DEBUG:-false}" = 'true' ]; then echo "${FUNCNAME[0]} ${*}" &> /dev/stderr; fi

  local cmd="python3 ${0%/*}/../spi/python/server.py"

  local pid

  if [ -e "${0##*/}.json" ]; then pid=$(jq -r '.pid' "${0##*/}.json"); else pid='null'; fi
  if [ "${pid:-null}" != 'null' ]; then
     local deets=$(ps ${pid} | tail +2 | egrep "${cmd##*/}")

     if [ ! -z "${deets:-}" ]; then
       if [ "${DEBUG:-false}" = 'true' ]; then echo "Killing existing PID: ${pid} for command: ${cmd##*/}; this: $$" &> /dev/stderr; fi
       kill -9 ${pid} &> /dev/null
     fi
  fi

  ${cmd} ${OLED_HOST} ${OLED_PORT} &> ${0##*/}.out &
  echo '{"name":"'${cmd}'","pid":'"$!"'}'
}

###
### PARAMETERS
###

## DEBUG
if [ -z "${DEBUG:-}" ] && [ -s DEBUG ]; then DEBUG=$(cat DEBUG); fi; export DEBUG=${DEBUG:-false}
if [ -z "${LOG_LEVEL:-}" ] && [ -s LOG_LEVEL ]; then LOG_LEVEL=$(cat LOG_LEVEL); fi; LOG_LEVEL=${LOG_LEVEL:-info}
if [ -z "${LOGTO:-}" ] && [ -s LOGTO ]; then LOGTO=$(cat LOGTO); fi; LOGTO=${LOGTO:-/dev/stderr}
LOG='{"debug":'${DEBUG}',"level":"'"${LOG_LEVEL}"'","logto":"'"${LOGTO}"'"}'

## OLED
if [ -z "${OLED_HOST:-}" ] && [ -s OLED_HOST ]; then OLED_HOST=$(cat OLED_HOST); fi; OLED_HOST=${OLED_HOST:-127.0.0.1}
if [ -z "${OLED_PORT:-}" ] && [ -s OLED_PORT ]; then OLED_PORT=$(cat OLED_PORT); fi; OLED_PORT=${OLED_PORT:-7777}
if [ -z "${OLED_PROTOCOL:-}" ] && [ -s OLED_PROTOCOL ]; then OLED_PROTOCOL=$(cat OLED_PROTOCOL); fi; OLED_PROTOCOL=${OLED_PROTOCOL:-http}
if [ -z "${OLED_URL:-}" ] && [ -s OLED_URL ]; then OLED_URL=$(cat OLED_URL); fi; OLED_URL=${OLED_URL:-${OLED_PROTOCOL}://${OLED_HOST}:${OLED_PORT}/oled/v1}
OLED='{"host":"'${OLED_HOST}'","port":'${OLED_PORT}',"protocol":"'${OLED_PROTOCOL}'","url":"'${OLED_URL}'"}'

## MOTION
if [ -z "${MOTION_GROUP:-}" ] && [ -s MOTION_GROUP ]; then MOTION_GROUP=$(cat MOTION_GROUP); fi; MOTION_GROUP=${MOTION_GROUP:-+}
if [ -z "${MOTION_CLIENT:-}" ] && [ -s MOTION_CLIENT ]; then MOTION_CLIENT=$(cat MOTION_CLIENT); fi; MOTION_CLIENT=${MOTION_CLIENT:-+}
if [ -z "${MOTION_CAMERA:-}" ] && [ -s MOTION_CAMERA ]; then MOTION_CAMERA=$(cat MOTION_CAMERA); fi; MOTION_CAMERA=${MOTION_CAMERA:-+}
MOTION='{"group":"'${MOTION_GROUP}'","client":"'${MOTION_CLIENT}'","camera":"'${MOTION_CAMERA}'"}'

# MQTT
if [ -z "${MQTT_HOST:-}" ] && [ -s MQTT_HOST ]; then MQTT_HOST=$(cat MQTT_HOST); fi; MQTT_HOST=${MQTT_HOST:-127.0.0.1}
if [ -z "${MQTT_PORT:-}" ] && [ -s MQTT_PORT ]; then MQTT_PORT=$(cat MQTT_PORT); fi; MQTT_PORT=${MQTT_PORT:-1883}
if [ -z "${MQTT_USERNAME:-}" ] && [ -s MQTT_USERNAME ]; then MQTT_USERNAME=$(cat MQTT_USERNAME); fi; MQTT_USERNAME=${MQTT_USERNAME:-username}
if [ -z "${MQTT_PASSWORD:-}" ] && [ -s MQTT_PASSWORD ]; then MQTT_PASSWORD=$(cat MQTT_PASSWORD); fi; MQTT_PASSWORD=${MQTT_PASSWORD:-password}
if [ -z "${MQTT_TOPIC:-}" ] && [ -s MQTT_TOPIC ]; then MQTT_TOPIC=$(cat MQTT_TOPIC); fi; MQTT_TOPIC=${MQTT_TOPIC:-${MOTION_GROUP}/${MOTION_CLIENT}/+/event/end/+}
MQTT='{"host":"'${MQTT_HOST}'","port":'${MQTT_PORT}',"username":"'${MQTT_USERNAME}'","password":"'${MQTT_PASSWORD}'","topic":"'${MQTT_TOPIC}'"}'


###
### MAIN
###

missing=$(has_groups i2c spi gpio video)
if [ -z "${missing:-}" ]; then
  missing=$(has_commands python3 curl)
  if [ -z "${missing:-}" ]; then
    echo $(server ${*}) | jq '.endpoints=[{"name":"display/picture","type":"application/json","request":"POST","url":"'${OLED_URL}/display/picture'"}]' | tee ${0##*/}.json
  else
    echo "Commands: [ ${missing} ] missing; install" &> /dev/stderr
    exit 1
  fi
else
  echo "Groups: [ ${missing} ] missing; sudo addgroup ${USER} <group>" &> /dev/stderr
  exit 1
fi
