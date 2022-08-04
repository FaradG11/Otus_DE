# Домашнее задание: Анализ веб-логов с помощью ELK

## Задание
Цель задания:
1. Написать конфигурацию Logstash clickstream.conf для загрузки данных файла weblog.csv в ElasticSearch.
2. Построить отчет в Kibana, показывающий распределение запросов с разными кодами ответов (status_code) по времени.

<details><summary><strong>Инструкция по заданию</strong></summary><br>

1. Клонируйте репозиторий [elk_demo](https://github.com/Gorini4/elk_demo)
2. Зайдите в эту директорию и разверните инфраструктуру, выполнив команду:<br><br>
    ```Bash 
    docker-compose up
    ```
3. Отредактируйте файл `clickstream.conf`
4. Загрузите данные веб-логов, выполнив команду:<br><br>
    ```Bash 
    ./load_data.sh
    ```
5. Перейдите по адресу http://localhost:5601 и создайте отчет (dashboard), показывающий распределение запросов с разными кодами ответов (status_code) по времени.

## Файлы
* **[clickstream.conf](logstash/clickstream.conf)]** - Разработанный файл конфигурации

* **[docker-compose.yml](docker-compose.yml)** - Доработанный файл `docker-compose` для одновременного запуска сервисов **ELK** и выполнения загрузки данных **Logstash** по файлу конфигурации [clickstream.conf](logstash/clickstream.conf).


## Инструкция по запуску 
1. Развернуть инфраструктуру сервисов **ELK**, выполнив команду:<br><br>
    ```Bash 
    docker-compose -f docker-compose.yml up
    ```
2. После загрузки всех сервисов - перейти по адресу http://localhost:5601
3. Импортировать настройки и сохраненные объекты в **Kibana**.<br>
    Для этого необходимо выполнить следующие шаги:
    * Перейти в настройки:  `Management -> Kibana -> Saved Objects`
    * Выполнить импорт файла `kibana.ndjson`, с включенными опциями `Check for existing objects` и `Automatically overwrite conflicts`
    * После выполнения импорта можно запускать на выполнение **Weblog Dashboard**, из списка сохраненных объектов или из раздела **Kibana**.
4. По завершению работы, выполнить команду:<br><br>
    ```Bash 
    docker-compose -f docker-compose.yml down
    ```
   

## Результат работы

**Weblog Dashboard**
