import json
import boto3
import os

def make_path(student_id, lecture_name):
    path = f"qrcodes/{student_id}/{lecture_name}/qrcode.jpg"
    return path

def lambda_handler(event, context):
    # TODO implement
    
    BUCKET_NAME = os.environ['BUCKET_NAME']
    ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
    SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
    
    records = event['Records']
    
    if records :
        subject = records[0]['Sns']['Subject']
        if subject != 'delete':
            return {"subjectCheck" : False, "success": False}
        
        msg = records[0]['Sns']['Message'].split(', ')

        student_id = msg[0]
        lecture_name= msg[1]
    
        s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_ACCESS_KEY)
        path = make_path(student_id, lecture_name)
        
        response = s3.Object(BUCKET_NAME,path).delete()
    
    return {
        'statusCode': 200,
        'success': True,
        'subjectCheck' : True
    }
