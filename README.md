
# 🚀AWS-Serverless-LakeFlow

This repository provides the code and configuration details for implementing an **end-to-end serverless ETL (Extract, Transform, Load) data pipeline** using Amazon Web Services (AWS).

## 💡 Project Overview

The primary goal of this pipeline is to automatically process raw CSV files uploaded to an **S3 bucket**, perform necessary data transformations (cleaning, deduplication), and load the final, transformed data into a **curated data layer** ready for reporting and analytics.

<img width="598" height="540" alt="image" src="https://github.com/user-attachments/assets/2367a4db-72f3-42fe-be95-bb63a0a27901" />

---

## 🏗️ Architecture and Step-by-Step Implementation

The pipeline is structured into the following 11 key stages:

### 1. Setup Data Source (Amazon S3)
* An **S3 bucket** is created for storage.
* Data is organized into **raw (Bronze)**, **processed (Silver)**, and **curated (Gold)** folders.
* **Raw CSV data files** are initially uploaded to the `raw/` folder.

### 2. Configure AWS Lambda Trigger
* An **AWS Lambda function (Python)** is created.
* It is configured with an **S3 Event Trigger**.
* Upon a **new CSV file upload**, the Lambda automatically executes and uses **boto3** to call `start_job_run()` and trigger the AWS Glue Job.

### 3. Build and Configure AWS Glue ETL Job
* An **AWS Glue ETL Job** is created (using PySpark).
* The **transformation logic** performs tasks such as:
    * Reading CSV files from the S3 `raw/` folder.
    * **Dropping duplicates**.
    * **Cleaning null values**.
    * **Formatting data**.
* The transformed data is written back to the **S3 processed (Silver)** folder in CSV format.

### 4. Add AWS Glue Crawler (Schema Detection)
* An **AWS Glue Crawler** is configured.
* It automatically scans the **processed (Silver)** data folder.
* It updates the **Glue Data Catalog** to detect the schema and make the data queryable.

### 5. Implement Data Load to Target (Curated Layer)
* The final **validated and transformed data** is loaded into the **S3 curated (Gold)** folder.
* This layer serves as the final, reliable source for **analytics and reporting**.

### 6. Configure Amazon EventBridge (Orchestration)
* An **EventBridge Rule** is set up to track Glue Job events.
* Targets include:
    * **AWS Glue**: To automate or monitor job runs.
    * **Amazon CloudWatch**: To record and centralize detailed logs.

### 7. Setup CloudWatch for Monitoring
* Used to monitor all **Lambda and Glue logs**.
* Tracks job metrics and execution time.
* **CloudWatch Alarms** are created to alert specifically on **job failures**.

### 8. Configure SNS for Notifications
* An **Amazon SNS (Simple Notification Service) Topic** is integrated.
* It sends **email alerts** when the Glue Job **succeeds** or **fails/throws an error**.

### 9. Enable Job Scheduling (EventBridge Scheduler)
* **EventBridge Scheduler** is configured to automatically trigger the pipeline at fixed intervals (daily/hourly).
* This ensures data refresh happens without manual intervention.

### 10. Add Data Validation and Analytics
* **AWS Athena**: Used to run SQL queries directly on the processed data stored in S3.
* **Amazon QuickSight**: Integrated for creating **dashboards and visual analytics** using the curated (Gold) dataset.

### 11. End-to-End Testing and Monitoring
* Test CSV files are uploaded to verify the trigger mechanism and ETL logic.
* Job success/failure notifications are verified via email (through SNS).
* Complete pipeline logs are monitored in **CloudWatch** for comprehensive end-to-end visibility.

---

## 🛠️ Prerequisites

* AWS Account
* AWS CLI configured
* Basic understanding of Python/PySpark (for Glue Job)
* Knowledge of the `boto3` library (for Lambda)

---
