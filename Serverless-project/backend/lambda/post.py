import mysql.connector
import sys
import boto3
import os
import json

def make_sql(student_id, lecture_name, student_name, student_phone, student_email):
    sql = f"INSERT INTO enroll VALUES ({student_id},'{lecture_name}','{student_name}','{student_phone}','{student_email}')"
    return sql
    
def lambda_handler(event, context):
    client = boto3.client('rds')
    
    ENDPOINT = os.environ['ENDPOINT']
    PORT = os.environ['PORT']
    USER = os.environ['USER']
    REGION = os.environ['REGION']
    DBNAME = os.environ['DBNAME']
    PASSWD = os.environ['PASSWD']
    
    student_id = event.get('student_id', '')
    lecture_name = event.get('lecture_name', '')
    student_name = event.get('student_name', '')
    student_phone = event.get('student_phone', '')
    student_email = event.get('student_email', '')
    
    if student_id in ('',' ',None) or lecture_name in ('',' ',None):
        return {
            'success': False
        }
        # TODO: write code...
    
    sql = make_sql(student_id, lecture_name, student_name, student_phone, student_email)
    print("sql : ", sql)
    
    # sql 연결 및 삽입
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME)
        cur = conn.cursor(buffered=True)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        return {
            "success" : False
        }
        
    # 토픽 리소스 생성 및 sns 전송
    sns = boto3.resource('sns')
    topic = sns.Topic(os.environ['SNS_ARN'])
    print("success1")
    response = topic.publish(
        Message=f'{student_id}, {lecture_name}, {student_name}, {student_phone}, {student_email}'
    )
    print("success2")
   

    
    
    return {
        'statusCode': 200,
        'event' : event,
        "success" : True,
        "topic1" : response
    }
