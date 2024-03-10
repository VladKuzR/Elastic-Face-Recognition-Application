import boto3
 
ec2 = boto3.client('ec2')
 
def create_instance(name = 'app-tier-instance-0', type = "t2.micro", security_sroup_id = "sg-0b6bdad554cbf777d"):
    conn = ec2.run_instances(InstanceType=type,
                            MaxCount=1,
                            MinCount=1,
                            ImageId="ami-01066273252204cd9", 
                            KeyName="MyNewKayPair",
                            SecurityGroupIds=[security_sroup_id], 
                            TagSpecifications=[{'ResourceType':'instance',
                                'Tags': [{
                                    'Key': 'Name',
                                    'Value': name }]}],
                            UserData='#!/bin/bash\npython3 /home/ubuntu/AppTier/appTier.py')

    print(conn)

for i in range(19):
    if i<10:
        create_instance(name = f'app-tier-instance-0{i}', security_sroup_id = 'sg-0a831a2b74edf3845')
    else:
        create_instance(name = f'app-tier-instance-{i}', security_sroup_id = 'sg-0a831a2b74edf3845')
