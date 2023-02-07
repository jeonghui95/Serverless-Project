import json
import boto3
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

def lambda_handler(event, context):


    #S3
    s3 = boto3.resource('s3')

    records = event['Records']
    if records : 
        msg = records[0]['Sns']['Message'].split(', ')
        print("msg", "*"*20)
        print(msg)

        student_id = msg[0]
        lecture_name= msg[1]
        student_name= msg[2]
        student_phone= msg[3]
        student_email= msg[4]
    
        
        #3. image build
        W, H = (400, 250)

        # 1) logo img
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

        draw.text((150, 110), student_id, fill='#000', font=font_b)
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
