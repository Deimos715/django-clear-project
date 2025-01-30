#!/bin/bash


echo "Информация о ветке"
git branch -a
git rev-parse --abbrev-ref HEAD

echo "Обновляем ветки"
git prune
git reset --hard HEAD
git add --all
git fetch
git pull origin

echo "(requirements) Нажмите 'y', чтобы установить из requirements.txt. Нажмите Enter, чтобы пропустить."
read input
if [ "$input" = "y" ]; then
  echo "Запуск зависимостей."
  pip3 install -r requirements.txt
  python3 manage.py migrate
else
  echo "Пропущено установку зависимостей."
fi

echo "(migrate) Нажмите 'y', чтобы установить миграции в БД. Нажмите Enter, чтобы пропустить."
read input
if [ "$input" = "y" ]; then
  echo "Запуск миграций."
  python3 manage.py migrate
fi


