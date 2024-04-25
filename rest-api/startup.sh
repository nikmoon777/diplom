#!/bin/bash

echo "WARN: Сервером используется база данных (tg_scam) PostgreSQL..."
echo "WARN: Если PostgreSQL сервер с базой данных (tg_scam) не запущен на текущем хосте, пожалуйста, прервите выполнение скрипта."
echo "Чтобы продолжить, нажмите ENTER..."
read
echo "Обновляю пакеты..."
sleep 1.5s
sudo apt update
sudo apt install openjdk-17-jdk maven -y
echo "Собираю проект в исполняемый файл..."
sleep 1.5s
mvn clean package
screen -dm -S "scam_server" java -jar ./target/scam-detector-0.0.1-SNAPSHOT.jar