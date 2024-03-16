import botocore
import boto3

ec2 = boto3.client('ec2')
def create_instance(name='app-tier-instance-0', instance_type="t2.micro", security_group_id="sg-0b6bdad554cbf777d"):
    try:
        conn = ec2.run_instances(
            InstanceType=instance_type,
            MaxCount=1,
            MinCount=1,
            ImageId="ami-07d9b9ddc6cd8dd30",  # Specify your desired AMI ID
            KeyName="MyNewKayPair",  # Specify your existing key pair name
            SecurityGroupIds=[security_group_id],  # Ensure the security group is configured correctly
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'VolumeSize': 8,
                        'Encrypted': True  # Specify that the volume should be encrypted
                    }
                }
            ],
            HibernationOptions={'Configured': True},  # Enable hibernation
            TagSpecifications=[{'ResourceType':'instance',
                                'Tags': [{'Key': 'Name', 'Value': name}]}]
        )
        print("Instance created successfully.")
    except botocore.exceptions.ClientError as e:
        print(f"Error creating instance: {e.response['Error']['Message']}")

# Call the function with corrected parameters
create_instance(name='app-tier-instance-010', security_group_id='sg-0a831a2b74edf3845')
