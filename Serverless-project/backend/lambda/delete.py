import mysql.connector
import sys
import boto3
import os
import json

def make_delete_sql(student_id, lecture_name):
    sql = "DELETE FROM enroll WHERE student_id = {0} AND lecture_name = '{1}'".format(student_id, lecture_name)
    return sql
    

def lambda_handler(event, context):
    
    # 1. 환경 변수 자원 찾기
    ENDPOINT = os.environ['ENDPOINT']
    PORT = os.environ['PORT']
    USER = os.environ['USER']
    REGION = os.environ['REGION']
    DBNAME = os.environ['DBNAME']
    PASSWD = os.environ['PASSWD']
    print('Success 1')
    
    # 2. 데이터 자료 찾기
    student_id = event.get('student_id', '')
    lecture_name = event.get('lecture_name','')
    print('Success 2')
    
    # 3. 필수 데이터 유무 확인
    if student_id in ('',' ',None) or lecture_name in ('',' ',None):
        return {
            'success': False,
            'level' : 3
        }
    print('Success 3')
        
    # 4. sql 문 생성
    sql = make_delete_sql(student_id, lecture_name)
    print('Success 4 : ', sql)
    
    # 5. sql 연결 및 삭제
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME)
        cur = conn.cursor(buffered=True)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        return {
            "success" : False,
            'level' : 5
        }
    print('Success 5')
        
    # 6. SNS 전달
    sns = boto3.resource('sns')
    topic = sns.Topic(os.environ['SNS_ARN'])
    response = topic.publish(
        Message=f'{student_id}, {lecture_name}',
        Subject = "delete"
    )
    print("success6")

    return {
        'statusCode': 200,
        'success': True,
        'sql' : sql,
        'sns' : response
    }
