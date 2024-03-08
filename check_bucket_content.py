import boto3

s3 = boto3.client('s3')

response = s3.list_objects(Bucket='1230868550-in-bucket')

for obj in response['Contents']:
    obj_key = obj['Key']
    obj_response = s3.get_object(Bucket='1230868550-out-bucket', Key=obj_key)
    obj_value = obj_response['Body'].read().decode('utf-8')

    print(f"Key: {obj_key}, Value: {obj_value}")