import os
import pymysql
import json

host        = os.environ["DB_HOST"]
user        = os.environ["DB_USERNAME"]
password    = os.environ["DB_PASSWORD"] 
db          = os.environ["DB_NAME"]
    
def lambda_handler(event, context):
        
    # mysql에 접속하는 코드이다.
    connect     = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    cursor = connect.cursor()
    
    student_id = event.get('student_id', '')
    lecture_name = event.get('lecture_name', '')
    # student_name = event.get('student_name', '')
    # student_phone = event.get('student_phone', '')
    # student_email = event.get('student_email', '')
    
    if student_id not in ('',' ', None,'*') and lecture_name not in ('',' ', None,'*'):
        sql = f"select * from enroll Where student_id = '{student_id}' and lecture_name = '{lecture_name}'"
    else:
        sql = "select * from enroll"
        
    print('sql : ', sql)
    cursor.execute(sql)
    
    
    rows = cursor.fetchall()
    result = []
    for idx, row in enumerate(rows):
        student_id = row[0]
        lecture_name = row[1]
        student_name = row[2]
        student_phone = row[3]
        student_email = row[4]
        
        json_data = dict()
        json_data['student_id'] = student_id
        json_data['lecture_name'] = lecture_name
        json_data['student_name'] = student_name
        json_data['student_phone'] = student_phone
        json_data['student_email'] = student_email
        
        # json_data = json.dumps(json_data, ensure_ascii=False)
        
        result.append(json_data)
        print(f"json data {idx} : ", json_data)
        
        # result.append(json.dumps({'student_id': row[0], 'lecture_name': row[1], 'student_name': row[2],'student_phone': row[3],'student_email': row[4]}))
    
    return {
        "statusCode": 200,
        "items" : json.dumps(result),
        "student_id" : event.get('student_id', ''),
        "lecture_name" : event.get('lecture_name', '')

    }    