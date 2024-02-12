import boto3
 
ec2 = boto3.client('ec2')
 

conn = ec2.run_instances(InstanceType="t2.micro",
                         MaxCount=1,
                         MinCount=1,
                         ImageId="ami-00ddb0e5626798373", 
                         KeyName="MyNewKayPair", 
                         SecurityGroupIds=["sg-0b6bdad554cbf777d"], 
                         TagSpecifications=[{'ResourceType':'instance',
                               'Tags': [{
                                'Key': 'Name',
                                'Value': 'WebTier' }]}])

print(conn)

instance_id = conn['Instances'][0]['InstanceId']
ec2.create_tags(
    Resources=[instance_id],
    Tags=[{'Key': 'Name', 'Value': 'WebTier Worker'}]
)