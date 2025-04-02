#!/bin/bash

# validations
error() {
  local messages=("$@")
  for message in "${messages[@]}"; do
    echo "$message" >&2
  done
  exit 1
}


help() {
  echo "Usage: $0 -c build|start|stop|restart|shell"
  echo "   or: $0 -h"
  echo
  echo "Arguments:"
  echo "  -c  run command (build|start|stop|restart|shell)"
  echo "  -h  show help"
  exit 0
}
usage() {
  error "Usage: $0 -c build|start|stop|restart|shell or: $0 -h"
}

OPTSTRING="c:h"

while getopts ${OPTSTRING} opt; do
  case ${opt} in
    h)
      help
      ;;
    c)
      COMMAND=${OPTARG}
      if [[ "$COMMAND" != "build" && "$COMMAND" != "start" && "$COMMAND" != "stop" && "$COMMAND" != "restart" && "$COMMAND" != "shell" ]]; then
        echo "Unexpected value -c ${COMMAND}"
        usage
      fi
      ;;
    :)
      error "Option -${OPTARG} requires an argument."
      ;;
    ?)
      error "Invalid option: -${OPTARG}."
      ;;
  esac
done

if [[ -z "${COMMAND}" ]]; then
    usage
fi

# get script directory

SCRIPT_PATH="${BASH_SOURCE:-$0}"
ABS_SCRIPT_PATH="$(realpath "${SCRIPT_PATH}")"
ABS_DIRECTORY="$(dirname "${ABS_SCRIPT_PATH}")"
ROOT_DIRECTORY=${ABS_DIRECTORY}
DATA_DIR=${ROOT_DIRECTORY}/.data
RTP_DIR=${ROOT_DIRECTORY}/app/rpt
OUTPUT_DIR=${ROOT_DIRECTORY}/app/output

if [ ! -d "${RTP_DIR}" ]; then
  mkdir -p ${RTP_DIR}
fi

if [ ! -d "${OUTPUT_DIR}" ]; then
  mkdir -p ${OUTPUT_DIR}
fi

if [ ! -d "${DATA_DIR}" ]; then
  mkdir -p ${DATA_DIR}
fi

if [[ ! -d "${DATA_DIR}/.vscode-server" ]]; then
    mkdir -p ${DATA_DIR}/.vscode-server
fi

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
cp ${ROOT_DIRECTORY}/docker/group ${DATA_DIR}/group
echo "user:x:${GROUP_ID}:" >> ${DATA_DIR}/group
cp ${ROOT_DIRECTORY}/docker/passwd ${DATA_DIR}/passwd
echo "user:x:${USER_ID}:${GROUP_ID}:user:/tmp:/bin/bash" >> ${DATA_DIR}/passwd

if [[ "$COMMAND" == "build" ]]; then
    docker compose -f ${ROOT_DIRECTORY}/docker/docker-compose.yml build
elif [[ "$COMMAND" == "start" ]]; then
    docker compose -f ${ROOT_DIRECTORY}/docker/docker-compose.yml up
elif [[ "$COMMAND" == "stop" ]]; then
    docker compose -f ${ROOT_DIRECTORY}/docker/docker-compose.yml down
elif [[ "$COMMAND" == "restart" ]]; then
    docker compose -f ${ROOT_DIRECTORY}/docker/docker-compose.yml restart
elif [[ "$COMMAND" == "shell" ]]; then
    docker compose -f ${ROOT_DIRECTORY}/docker/docker-compose.yml -f ${ROOT_DIRECTORY}/docker/docker-compose-shell.yml up
fi