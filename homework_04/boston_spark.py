"""Homework N4 DE course.
Write a path for row data as an argument of function:
 $SPARK_HOME/bin/spark-submit ~../boston_spark.py '/home/user/../foldername/'"""


import sys
import os.path
from pyspark.sql import SparkSession, functions as f
spark = SparkSession.builder.\
    master("local[*]").\
    appName('boston_crime').\
    getOrCreate()

PATH = sys.argv[1]

CSV_FILE = 'crime.csv'
OFFENSE_CODES = 'offense_codes.csv'
df = spark.read.csv(os.path.join(PATH,CSV_FILE), header=True)
codes = spark.read.csv(os.path.join(PATH,OFFENSE_CODES), sep=',', header=True)

# delete the part after "-" and whitespaces in offense description

codes = codes.withColumn('NAME', f.regexp_replace('NAME', r'\-.*', ''))
codes = codes.withColumn('NAME', f.rtrim(codes.NAME))


# drop all rows without district

df = df.na.drop(subset="DISTRICT")
df = df.withColumn('OFFENSE_CODE', f.regexp_replace('OFFENSE_CODE', r'^0+', ''))

# collect 3 frequent crime type
offense_table = codes.join(df, codes.CODE == df.OFFENSE_CODE, 'right').\
    select(df.INCIDENT_NUMBER, codes.NAME, df.DISTRICT)
offense_table = offense_table.groupby(['DISTRICT', 'NAME']).\
    agg(f.count('INCIDENT_NUMBER').alias('count')).orderBy('DISTRICT', f.desc('count'))
offense_table = offense_table.groupby('DISTRICT').\
    agg(f.collect_list('NAME').alias("Collect")).withColumn("frequent_crime_types", f.slice('Collect', 1, 3))


main_query = df.groupby('DISTRICT').agg(f.countDistinct("INCIDENT_NUMBER").alias("crimes_total"),
                                        f.avg('Lat').alias('lat'),
                                        f.avg('Long').alias('lng'),
                                        )

group_by_month = df.groupby('DISTRICT', 'YEAR', 'MONTH').agg(f.countDistinct('INCIDENT_NUMBER').alias('by_moth'))

median = group_by_month.groupby('DISTRICT').\
    agg(f.percentile_approx(col='by_moth', percentage=0.5, accuracy=1000000).alias("crimes_monthly"))

# offense_table.show()
# main_query.show()
# median.show()

result = main_query.join(median, 'DISTRICT', 'inner').join(
        offense_table, 'DISTRICT', 'inner'
                ).select(
                        [main_query.DISTRICT, main_query.crimes_total, median.crimes_monthly,
                         offense_table.frequent_crime_types, main_query.lat, main_query.lng]
            )

# result.show()

result.write.parquet(os.path.join(PATH, 'boston_crime_view.parquet'))
print('-----===== SUCCESS!!! =====----- \n', os.path.join(PATH, 'boston_crime_view.parquet'), '  CREATED')
