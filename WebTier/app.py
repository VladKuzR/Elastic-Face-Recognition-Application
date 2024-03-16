from flask import Flask, request, jsonify
import base64
import boto3
import threading
import time
from queue import Queue
import asyncio
import pickle

app = Flask(__name__)

request_queue = Queue()
prediction_object = {}
SQS = boto3.client('sqs')
lock = threading.Lock()
EC2 = boto3.client('ec2')



@app.route('/', methods=['POST'])
def send_to_appTier():
    if 'inputFile' not in request.files:
        return "No file provided", 400
    image = request.files['inputFile'].read()
    filename = request.files['inputFile'].filename
    

    print(filename)

    

    print("-----------Вся Очередь",list(request_queue.queue))

    # Используем блокировку для синхронизации


    readyToSendImage = '[eqgbplf]'.join([filename, base64.b64encode(image).decode('utf-8')])

    response = SQS.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        MessageBody=readyToSendImage,
        )
    print(response)
    request_queue.put(filename.split('.')[0])

    with lock:
        print('siiiiiiiiiize', request_queue.qsize())    
        
        while True:
            with open('queue_data.pkl', 'wb') as f:
                pickle.dump(request_queue.qsize()-1, f)

            received_message = SQS.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                VisibilityTimeout=0,
                MaxNumberOfMessages=1,
            )
            print('Message Reception')
            try:
                handler = received_message['Messages'][0]['ReceiptHandle']
                SQS.delete_message(
                    QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                    ReceiptHandle=handler
                )
                filename = received_message['Messages'][0]['Body'].split(']eqgbplf')[0]
                prediction = received_message['Messages'][0]['Body'].split(']eqgbplf')[1]
                if filename not in prediction_object:
                    prediction_object[filename] = prediction
                    print('prediction is', prediction)
                    print('-----------------------', prediction_object)
                    
            except:
                print('error of message reception')

            if not request_queue.empty():
                first_element = request_queue.queue[0]
                if first_element in prediction_object:
                    prediction = prediction_object[first_element]
                    filename = request_queue.get()
                    print("-----------Вся Очередь----------", list(request_queue.queue))
                    print('----------Все Предсказания-------------', prediction_object)
                    if request_queue.empty():
                        prediction_object.clear()
                    return f'{filename}:{prediction}'
            else:
                time.sleep(3) 
            time.sleep(0.1)   



if __name__ == '__main__':
    app.run(debug=True, threaded = True)