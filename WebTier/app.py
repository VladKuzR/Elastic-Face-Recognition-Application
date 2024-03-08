from flask import Flask, request, jsonify
import base64
import boto3
import threading

app = Flask(__name__)


@app.route('/', methods=['POST'])
def send_to_appTier():
    if 'inputFile' not in request.files:
        return "No file provided", 400
    image = request.files['inputFile'].read()
    filename = request.files['inputFile'].filename


    SQS = boto3.client('sqs')


    readyToSendImage = '[eqgbplf]'.join([filename, base64.b64encode(image).decode('utf-8')])

    response = SQS.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        MessageBody=readyToSendImage,
    )

    while True:
        response = SQS.get_queue_attributes(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
            AttributeNames=['ApproximateNumberOfMessages']
        )
        if (int(response['Attributes']['ApproximateNumberOfMessages'])) >= 1:
            received_message = SQS.receive_message(
                QueueUrl = 'https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue'
            )
            try:
                # Deleting Message
                handler = received_message['Messages'][0]['ReceiptHandle']
                SQS.delete_message(
                    QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                    ReceiptHandle=handler
                )
                filename = received_message.split('[eqgbplf]')[0]
                prediction = received_message.split('[eqgbplf]')[1]
                return f'{filename}:{prediction}' 
            except:
                print('error of message receprion')   
    
        

def elastic_controller():
    return False

if __name__ == '__main__':
    app.run(debug=True, threaded = True)