import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')

    response = glue.start_job_run(
        JobName='ETL PIPELINE',   
       
    )

    print("Started Glue Job:", response['JobRunId'])
    return {
        'statusCode': 200,
        'body': f"Glue job started successfully with JobRunId: {response['JobRunId']}"
    }