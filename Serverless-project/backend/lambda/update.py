import os
import pymysql
import json
import boto3
from PIL import Image, ImageDraw, ImageFont
import qrcode


#mariadb 접속
host        = os.environ["DB_HOST"]
user        = os.environ["DB_USERNAME"]
password    = os.environ["DB_PASSWORD"] 
db          = os.environ["DB_NAME"]

def make_path(student_id, lecture_name):
    path = f"qrcodes/{student_id}/{lecture_name}/qrcode.jpg"
    return path

    
def lambda_handler(event, context):
    connect     = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    cursor = connect.cursor()
    
    
    
    

    
#값 받아오기
    # checker_id = event.get('checker_id','')
    # checker_name = event.get('checker_name','')
    student_id = event.get('student_id', '')
    lecture_name = event.get('lecture_name', '')
    student_name = event.get('student_name', '')
    student_phone = event.get('student_phone', '')
    student_email = event.get('student_email', '')
    BUCKET_NAME = os.environ['BUCKET_NAME']
    ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
    SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
        





#qr 지우기
    
    s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_ACCESS_KEY)
    path = make_path(student_id,lecture_name)
    response = s3.Object(BUCKET_NAME,path).delete()
    # s3_client = boto3.client("s3")
    # response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=path)
    

    



    
#sql
    a = ''
    if student_id and lecture_name:
        sql = "UPDATE enroll SET student_id = %s, lecture_name =%s, student_name =%s, student_phone =%s, student_email =%s WHERE student_id = %s"

        cursor.execute(sql,(student_id,lecture_name,student_name,student_phone,student_email,student_id))
        connect.commit()
        
        sql = "SELECT * from enroll Where student_id = %s and lecture_name=%s"
    
        cursor.execute(sql,(student_id,lecture_name))
    else:
        return print("값을 받아올 수 없습니다")
    if not cursor.fetchall():
        
        return print(f"구문실행오류!!! 값:{cursor.fetchall()}")


    
#  qr 생성
    W, H = (400, 250)    
    
    s3.Bucket(os.environ['BUCKET_NAME']).download_file('fonts/font.otf', '/tmp/font.otf')
    s3.Bucket(os.environ['BUCKET_NAME']).download_file('images/logo.png', '/tmp/logo.png')

    logo = Image.open('/tmp/logo.png') #image logo
    otf = '/tmp/font.otf' #f


    # 2) qr code img
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    
    qr.add_data(student_phone)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # 3) merge
    img = Image.new('RGB', (W, H), color='#fff')
    img.paste(logo, (15, 15), logo)
    img.paste(qr_img, (15, 100))

    # 4) draw
    font_m = ImageFont.truetype(otf, 15)
    font_b = ImageFont.truetype(otf, 20)
    font_B = ImageFont.truetype(otf, 22)

    draw = ImageDraw.Draw(img)

    draw.text((150, 110), f"{student_id}", fill='#000', font=font_b)
    draw.text((150, 140), f'{student_name}', fill='#000', font=font_m)

    draw.rectangle((145, 170, 375, 205), fill='#f0f0f0')
    draw.text((150, 170), 'CONFERENCE PASS', fill='#ed244b', font=font_B)
    
    img.save(f'/tmp/signed.jpg', quality=100)

    key = f'qrcodes/{student_id}/{lecture_name}/qrcode.jpg'
    s3.meta.client.upload_file('/tmp/signed.jpg', os.environ['BUCKET_NAME'], key, ExtraArgs={'ContentType':'image/jpeg'})
    
    
    
    
    
    return {
        'statusCode': 200,
        'event': event,
    }
    
    
    