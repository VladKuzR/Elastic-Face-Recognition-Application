import boto3
 
ec2 = boto3.client('ec2')
 
def create_instance(name = 'app-tier-instance-0', type = "t2.micro", security_sroup_id = "sg-0b6bdad554cbf777d"):
    conn = ec2.run_instances(InstanceType=type,
                            MaxCount=1,
                            MinCount=1,
                            ImageId="ami-0a2dab5f832df3025", 
                            KeyName="MyNewKayPair",
                            SecurityGroupIds=[security_sroup_id], 
                            TagSpecifications=[{'ResourceType':'instance',
                                'Tags': [{
                                    'Key': 'Name',
                                    'Value': name }]}])

    print(conn)


for i in range(19):
    if i<9:
        create_instance(name = f'app-tier-instance-0{i+1}', security_sroup_id = 'sg-0a831a2b74edf3845')
    else:
        create_instance(name = f'app-tier-instance-{i+1}', security_sroup_id = 'sg-0a831a2b74edf3845')
