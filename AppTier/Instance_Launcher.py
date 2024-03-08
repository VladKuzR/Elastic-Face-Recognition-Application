import boto3
 
ec2 = boto3.client('ec2')
 
def create_instance(name = 'app-tier-instance-0', type = "t2.micro", security_sroup_id = "sg-0b6bdad554cbf777d"):
    conn = ec2.run_instances(InstanceType=type,
                            MaxCount=1,
                            MinCount=1,
                            ImageId="ami-00ddb0e5626798373", 
                            KeyName="MyNewKayPair",
                            SecurityGroupIds=[security_sroup_id], 
                            TagSpecifications=[{'ResourceType':'instance',
                                'Tags': [{
                                    'Key': 'Name',
                                    'Value': 'app-tier-instance-0' }]}])

    print(conn)

create_instance(security_sroup_id = 'sg-0a831a2b74edf3845')
