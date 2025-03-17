from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

spark = SparkSession.builder \
        .appName("HalifaxAirQuality") \
        .getOrCreate()

client = InfluxDBClient(
            url= config["influxdb"]["url"],#"http://localhost:8086", 
            token= config["influxdb"]["token"], #"yF11xrFLHXDKGXkl-FFACbmjGNvGpX55ApPjjB4494ssIb4SzxwSXGeYlmWUUY5aWRV_tusfSh26DwC40YZBcA==", 
            org= config["influxdb"]["org"]#"halifax_project"
        )
write_api = client.write_api(write_options=SYNCHRONOUS)

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("station", StringType()),
    StructField("pm25", FloatType()),
    StructField("latitude", FloatType()),
    StructField("longitude", FloatType())
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", config["kafka"]["bootstrap_servers"]) \
    .option("subscribe", config["kafka"]["topic"]) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

anomalies = df.filter(col("pm25") > config["thresholds"]["pm25_anomaly"])

def write_to_influxdb(row):
    point = Point("air_quality") \
            .tag("station", row["station"]) \
            .field("pm25", row["pm25"]) \
            .time(row["timestamp"])
    write_api.write(bucket=config["influxdb"]["bucket"], record=point)
    print(f"Stored: {row['timestamp']}, PM2.5: {row['pm25']}")

query = anomalies.writeStream \
        .foreach(write_to_influxdb) \
        .outputMode("append") \
        .start()

query.awaitTermination()