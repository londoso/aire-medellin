import json
import boto3
import urllib.parse
import urllib3
import os
import awswrangler as wr
from dateutil import parser
    
def get_s3_object(bucket,key):
    client = boto3.client('s3')
    response = client.get_object(Bucket=bucket, Key=key)
    return response

def notify(sub, msg, sns_arn):
    print('Notificando errores por SNS')
    sns = boto3.client('sns')
    sns.publish(
        TopicArn = sns_arn,
        Message = msg,
        Subject = sub
    )

def lambda_handler(event, context):

    batch_size = int(os.environ['BATCH_SIZE'])
    table = os.environ['DYNAMODB_TABLE']
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    eventTime = event['Records'][0]['eventTime']
    event_time_file = parser.isoparse(eventTime)
    
    try:
        data = wr.s3.read_csv(f"s3://{bucket}/{key}",chunksize=batch_size,dtype=object)
        print('eventTime: ',eventTime)
        
        for x in data:
            print('----parte inicia------')
            print(x['user_id'].astype(str).to_list())
            subjectIds = x['user_id'].astype(str).to_list()
            regulateId = request_api(subjectIds)
            save_to_dynamodb(table, regulateId, subjectIds)
            
            print('----parte fin------')
            
        replace_filenames = {key.replace('in/', ''):f"{event_time_file.strftime('%Y%m%d%H%M%S')}.csv"}

        wr.s3.copy_objects(
            paths=[f"s3://{bucket}/{key}"],
            source_path=f"s3://{bucket}/in/",
            target_path=f"s3://{bucket}/processed/",
            replace_filenames=replace_filenames
        )
        
        wr.s3.delete_objects([f"s3://{bucket}/{key}"])
        
        return 'Procesado: ' + key
        
    except Exception as e:
        print(e)
        message = str(e) + '. Please check Cloudwatch Logs.'
        subject = 'Error Lambda [segment_suppress_dev]'
        sns = os.environ['ARN_SNS_ERROR']
        notify(subject, message, sns)
