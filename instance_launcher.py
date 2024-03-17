import boto3
 
ec2 = boto3.client('ec2')
 
def create_instance(name = 'app-tier-instance-0', type = "t2.micro", security_sroup_id = "sg-0b6bdad554cbf777d"):
    conn = ec2.run_instances(InstanceType=type,
                            BlockDeviceMappings=[
                                {
                                    'DeviceName': '/dev/sda1',
                                    'Ebs': {
                                        'VolumeSize': 8,
                                        'Encrypted': True
                                    },
                                },
                            ],
                            MaxCount=1,
                            HibernationOptions={
                                'Configured': True
                            },
                            MinCount=1,
                            ImageId="ami-0198766f17476c1f6", #ami-07d9b9ddc6cd8dd30", #ami-00cb4f8cf920095e3", 
                            KeyName="MyNewKayPair",
                            SecurityGroupIds=[security_sroup_id], 
                            TagSpecifications=[{'ResourceType':'instance',
                                'Tags': [{
                                    'Key': 'Name',
                                    'Value': name }]}])

    print(conn)


for i in range(20):
    if i<9:
        create_instance(name = f'app-tier-instance-0{i+1}', security_sroup_id = 'sg-0a831a2b74edf3845')
    else:
        create_instance(name = f'app-tier-instance-{i+1}', security_sroup_id = 'sg-0a831a2b74edf3845')