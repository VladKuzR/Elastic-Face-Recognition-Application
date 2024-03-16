import boto3
import time
from queue import Queue
import threading
import pickle

EC2 = boto3.client('ec2')
stopped_instances = Queue()
running_instances = Queue()
SQS = boto3.client('sqs')
activation_flag = 0

def start_instances(instance_id):
    response = EC2.start_instances(InstanceIds=[instance_id])
    print('Launcing an Instance')
         
    #time.sleep(1) 

def stop_instances(instance_id):
        response = EC2.stop_instances(
            InstanceIds=[instance_id],
            Hibernate=True)
        print('Stopping an Instance')
        time.sleep(10)
        
     

def elastic_controller():

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

    activation_flag = 0
    for i in range(len(response['Reservations'])):
            stopped_instances.put(response['Reservations'][i]['Instances'][0]['InstanceId'])
    while True:
        try:
            
            with open('/home/devcontainers/Cloud_Computing/WebTier/activation.pkl', 'rb') as f:
                incoming_sig = str(pickle.load(f))
                print(f'Incoming Signal is {incoming_sig}')
                print(f'Activation Code Init is {activation_code_init}')

                if activation_code_init != incoming_sig:
                    activation_flag = 1
                    activation_code_init = incoming_sig
                else:
                    activation_flag = 0
        except:
            activation_code_init = '0'


        if activation_flag == 1:
            if not stopped_instances.empty():
                try:
                    first_item = stopped_instances.queue[0]
                    start_instances(first_item)
                    stopped_instances.get()
                    running_instances.put(first_item)
                except:
                    stopped_instances.put(stopped_instances.get()) 

            else:
                print('All instances are running')
                time.sleep(10)
        else:
            if not running_instances.empty():
                try:
                    first_item = running_instances.queue[0]
                    stop_instances(first_item)
                    running_instances.get()
                    stopped_instances.put(first_item)
                    if running_instances.empty():
                        print('All instances are stopped')
                except:
                    running_instances.put(running_instances.get())
        if activation_flag == 0:
            time.sleep(2)
        else:
            time.sleep(0.1)



elastic_controller()