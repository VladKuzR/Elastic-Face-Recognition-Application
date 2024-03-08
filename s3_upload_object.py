import csv
import boto3
import os

s3_client = boto3.client('s3')

def upload_obj_from_csv(filepath, bucket_name):
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            image_key = row[0] 
            result_value = row[1]  

            response = s3_client.put_object(
                Body = result_value,
                Bucket = bucket_name,
                Key = image_key,
                )
            print(response)

def upload_obj_from_folder(folder_name, bucket_name):
    folder_path = folder_name

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path): 
            with open(file_path, 'rb') as file:
                response = s3_client.put_object(
                    Body=file,
                    Bucket='1230868550-in-bucket',
                    Key=filename,
                )
                print(response)