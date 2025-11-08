import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_RAW_PATH', 'S3_PROCESSED_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

S3_RAW_PATH = args['S3_RAW_PATH']
S3_PROCESSED_PATH = args['S3_PROCESSED_PATH']

print(f"Reading data from: {S3_RAW_PATH}")
print(f"Writing data to: {S3_PROCESSED_PATH}")

try:
    raw_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(S3_RAW_PATH)

    raw_df.printSchema()

except Exception as e:
    print(f"Error reading data from S3: {e}")
    job.commit()
    sys.exit()

deduplicated_df = raw_df.dropDuplicates()
print(f"Original Row Count: {raw_df.count()}, Deduplicated Row Count: {deduplicated_df.count()}")

cleaned_df = deduplicated_df.na.fill(value='Unknown', subset=['customer_name'])
cleaned_df = cleaned_df.na.drop()

final_processed_df = cleaned_df.select(
    col("id").cast("string").alias("record_id"),
    col("customer_name"),
    col("order_value").cast("double"),
    col("order_date").cast("timestamp"),
    col("region"),
    col("status")
)

final_processed_df.printSchema()

try:
    final_processed_df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(S3_PROCESSED_PATH)

    print(f"Successfully wrote {final_processed_df.count()} records to {S3_PROCESSED_PATH}")

except Exception as e:
    print(f"Error writing data to S3: {e}")
    job.commit()
    sys.exit()

job.commit()
print("Glue ETL Job Completed Successfully.")
