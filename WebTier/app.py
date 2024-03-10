from flask import Flask, request, jsonify
import base64
import boto3
import threading
import time
from queue import Queue

app = Flask(__name__)

request_queue = Queue()
prediction_object = {}

lock = threading.Lock()

@app.route('/', methods=['POST'])
def send_to_appTier():
    if 'inputFile' not in request.files:
        return "No file provided", 400
    image = request.files['inputFile'].read()
    filename = request.files['inputFile'].filename
    print(filename)

    

    print("-----------Вся Очередь",list(request_queue.queue))

    # Используем блокировку для синхронизации
    SQS = boto3.client('sqs')

    readyToSendImage = '[eqgbplf]'.join([filename, base64.b64encode(image).decode('utf-8')])

    response = SQS.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        MessageBody=readyToSendImage,
        )
    print(response)
    
    with lock:
        request_queue.put(filename.split('.')[0])
        print('siiiiiiiiiize', request_queue.qsize())    
        
        while True:
            """ response = SQS.get_queue_attributes(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                AttributeNames=['ApproximateNumberOfMessages']
            )
            print('IMPORTANT!!!!!', int(response['Attributes']['ApproximateNumberOfMessages']))
            # if (int(response['Attributes']['ApproximateNumberOfMessages'])) >= 1: """
            
            received_message = SQS.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
                VisibilityTimeout=0,
                MaxNumberOfMessages=1
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
                    print("-----------Вся Очередь----------", list(request_queue.queue))
                    print('----------Все Предсказания-------------', prediction_object)
                    del prediction_object[first_element]
                    return f'{request_queue.get()}:{prediction}'

            time.sleep(0.5)
                    
                    # Количество сообщений становится равным нулю почему-то

    
        

def elastic_controller():
    return False

if __name__ == '__main__':
    app.run(debug=True, threaded = True)