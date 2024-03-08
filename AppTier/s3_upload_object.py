import csv
import boto3
import os

s3_client = boto3.client('s3')

def upload_obj_text(key, value, bucket_name):

    response = s3_client.put_object(
        Body = value,
        Bucket = bucket_name,
        Key = key,
        )
    print(response)

def upload_obj_img(key, value, bucket_name):

    response = s3_client.put_object(
        Body = value,
        Bucket = bucket_name,
        Key = key
    )