#!/bin/bash

if [[ $# < 3 ]]; then
  echo "Не удалось запустить скрипт с аргументами $0 <TG_SCAM_BOT_TOKEN> <TG_SCAM_BAN_BOT_API_ID> <TG_SCAM_BAN_BOT_API_HASH>"
  exit 1
fi

TG_SCAM_BOT=$1
TG_SCAM_BAN_BOT_API_ID=$2
TG_SCAM_BAN_BOT_API_HASH=$3

export TG_SCAM_BOT
export TG_SCAM_BAN_BOT_API_ID
export TG_SCAM_BAN_BOT_API_HASH

cd ./rest-api/
bash startup.sh
cd ../tg-bot/
bash startup.sh $TG_SCAM_BOT $TG_SCAM_BAN_BOT_API_ID $TG_SCAM_BAN_BOT_API_HASH
