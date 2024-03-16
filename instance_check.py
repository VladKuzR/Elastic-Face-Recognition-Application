from flask import Flask, request, jsonify
import base64
import boto3
import threading
import time
from queue import Queue

EC2 = boto3.client('ec2')
stopped_instances = Queue()
running_instances = Queue()

response = EC2.describe_instances(
            Filters=[
                {
                    'Name': 'instance.group-id',
                    'Values': [
                        'sg-0a831a2b74edf3845',
                    ]
                },
            ],
        )
instances_present = []
for i in range(len(response['Reservations'])):
        instances_present.append(response['Reservations'][i]['Instances'][0]['InstanceId'])


for instance_id in instances_present[:20]:
    response = EC2.start_instances(
        InstanceIds=[instance_id],
    )
    time.sleep(2)

