import s3_upload_object
import face_recognition as fr
import boto3
import base64
from io import BytesIO
import time

SQS = boto3.client('sqs')

def handle_request():
    received_message = SQS.receive_message(
        QueueUrl = 'https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds = 20, 
        VisibilityTimeout = 0
    )
    if 'Messages' in received_message:
        handler = received_message['Messages'][0]['ReceiptHandle']
        SQS.delete_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
            ReceiptHandle=handler
        )

        filename = received_message['Messages'][0]['MessageAttributes']['filename']['StringValue']
        image_string = received_message['Messages'][0]['Body']
        unique_id = received_message['Messages'][0]['MessageAttributes']['UUID']['StringValue']
        decoded_image = BytesIO(base64.b64decode(image_string))

        recognition_result = fr.face_match(decoded_image, '/home/devcontainers/Cloud_Computing/AppTier/data.pt')[0]

        s3_upload_object.upload_obj_img(key = filename, value = image_string, bucket_name = '1230868550-in-bucket')

        s3_upload_object.upload_obj_text(key = filename.split('.')[0], value = recognition_result, bucket_name = '1230868550-out-bucket')

        response = SQS.send_message(
            QueueUrl = 'https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
            MessageBody = recognition_result,
            MessageAttributes={
            'filename': {
                'StringValue': filename,
                'DataType': 'String'
            },
            'UUID': {
                'StringValue': unique_id,
                'DataType': 'String'
            }}
        )
        print(response)

while True:
    print('Listening SQS')
    handle_request()   