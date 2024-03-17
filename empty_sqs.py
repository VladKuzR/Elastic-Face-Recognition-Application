import boto3
import base64

req_q = boto3.client('sqs')

response = req_q.get_queue_attributes(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
    AttributeNames=['ApproximateNumberOfMessages']
)
print('Request Queue:' ,int(response['Attributes']['ApproximateNumberOfMessages']))

for i in range(int(response['Attributes']['ApproximateNumberOfMessages'])):
    received_message = req_q.receive_message(
        QueueUrl = 'https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue'
    )
    handler = received_message['Messages'][0]['ReceiptHandle']
    req_q.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-req-queue',
        ReceiptHandle=handler
    )

response = req_q.get_queue_attributes(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
    AttributeNames=['ApproximateNumberOfMessages']
)
print('Response Queue:' ,int(response['Attributes']['ApproximateNumberOfMessages']))

for i in range(int(response['Attributes']['ApproximateNumberOfMessages'])):
    received_message = req_q.receive_message(
        QueueUrl = 'https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue'
    )
    handler = received_message['Messages'][0]['ReceiptHandle']
    req_q.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/533267346617/1230868550-resp-queue',
        ReceiptHandle=handler
    )

