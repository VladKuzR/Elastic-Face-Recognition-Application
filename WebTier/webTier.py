import boto3
import base64
from flask import Flask, request
import uuid
import pickle


app = Flask(__name__)

SQS = boto3.client('sqs')

EC2 = boto3.client('ec2')
prediction_dict = {}

@app.route('/', methods=['POST'])
def send_to_appTier():
    if 'inputFile' not in request.files:
        return "No file provided", 400
    image = request.files['inputFile'].read()
    filename = request.files['inputFile'].filename

    unique_id = str(uuid.uuid4())

    response = SQS.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        MessageBody=base64.b64encode(image).decode('utf-8'),
        MessageAttributes={
        'filename': {
            'StringValue': filename,
            'DataType': 'String'
        },
        'UUID': {
            'StringValue': unique_id,
            'DataType': 'String'
        }
    })
    print(response)

    while True:
        with open('activation.pkl', 'wb') as file:
                pickle.dump(str(uuid.uuid4()), file)
        received_message = SQS.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                MaxNumberOfMessages=1,
                MessageAttributeNames=['All'],
                WaitTimeSeconds = 0, 
                # VisibilityTimeout = 20
            )
        if 'Messages' in received_message:
            handler = received_message['Messages'][0]['ReceiptHandle']
            SQS.delete_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                ReceiptHandle=handler
            )
            unique_id_received = received_message['Messages'][0]['MessageAttributes']['UUID']['StringValue']
            if unique_id_received not in prediction_dict:
                prediction_dict[unique_id_received] = received_message['Messages'][0]['Body']
                print(prediction_dict)
        if unique_id in prediction_dict:
            predicted_name = prediction_dict[unique_id]
            del prediction_dict[unique_id]
            return f'{filename}:{predicted_name}'


if __name__ == '__main__':
    app.run(debug=True, threaded = True)