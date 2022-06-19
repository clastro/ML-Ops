from pyspark.sql import SparkSession

spark = SparkSession.builder \
                    .master('local[*]') \
                    .appName('first application') \
                    .getOrCreate()

spark.stop() #spark 종료
