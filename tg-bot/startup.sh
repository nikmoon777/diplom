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

echo "Начинаю обновление пакетов..."
sleep 1.5s
sudo apt update
echo "Установка пакетов для работы с Python 3.10..."
sleep 1.5s
sudo apt install python3.10 python3.10-venv python3-pip -y
echo "Следующим шагом будет установка зависимостей..."
echo "Загрузка зависимостей происходит в глобальный репозиторий хоста, если вы хотите использовать venv, пожалуйста, прервите выполнение скрипта."
echo "Чтобы продолжить, нажмите ENTER..."
read
echo "Установка зависимостей проекта"
sleep 1.5s
pip install -r "requirements.txt"
screen -dm -S "main_scam_bot" python main.py
screen -dm -S "ban_scam_bot" python ban_bot.py
