## Домашнее задание: Сборка витрины данных на PySpark

### Задание

В этом задании предлагается собрать статистику по криминогенной обстановке в разных районах Бостона.

В качестве исходных данных используется датасет https://www.kaggle.com/AnalyzeBoston/crimes-in-boston

Цель задания - разработать программу построения витрины.

Программа должна запускаться через spark-submit.
Пути к данным и к результату должны передаваться в качестве аргументов вызова.

### Что было сделано:
1. Загрузка данныхх
2. Проверка данных на корректность. Очистка дупликатов
3. Собрана витрина по следующим метрикам:

- crimes_total - общее количество преступлений в этом районе;
- crimes_monthly - медиана числа преступлений в месяц в этом районе; 
- frequent_crime_types - три самых частых crime_type за всю историю наблюдений в этом районе, объединенных через запятую с одним пробелом “, ” , расположенных в порядке убывания частоты; 
- crime_type - первая часть NAME из таблицы offense_codes, разбитого по разделителю “-” (например, если NAME “BURGLARY - COMMERICAL - ATTEMPT”, то crime_type “BURGLARY”); 
- lat - широта координаты района, рассчитанная как среднее по всем широтам инцидентов; 
- lng - долгота координаты района, рассчитанная как среднее по всем долготам инцидентов.
4. Сохранение витрины в файл в формате  .parquet в папке path/to/output_folder