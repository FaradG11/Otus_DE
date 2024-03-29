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

</details>

## Файлы
* **[clickstream.conf](logstash/clickstream.conf)]** - Разработанный файл конфигурации

* **[docker-compose.yml](docker-compose.yml)** - Доработанный файл `docker-compose` для одновременного запуска сервисов **ELK** и выполнения загрузки данных **Logstash** по файлу конфигурации [clickstream.conf](logstash/clickstream.conf).

 

## Результат работы

**Weblog Dashboard**

Распределение запросов с разными кодами ответов (status_code) по времени:

![Weblog Dashboard](https://github.com/FaradG11/Otus_DE/blob/5ceec1e57f7d6f2dfaa801c697f5b7eedd7aa5b4/homework_07_ELK/dashboard.png)