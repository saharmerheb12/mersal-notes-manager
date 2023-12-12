import os
import json
import boto3
import urllib.parse
from email_manager import send

expiresIn= os.environ["QR_PRESIGNED_URL_EXPIRY"]

def handler(event, context):
    try:
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        bucket_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['bucket']['name'], encoding='utf-8')

        s3 = boto3.client("s3")

        # Generate a pre-signed S3 URL.
        presigned_url = s3.generate_presigned_url(
                        "get_object",
                        Params= {"Bucket": bucket_name, "Key": object_key},
                        ExpiresIn= expiresIn,
                        )

        success = send(object_key, presigned_url)
        return {
            "statusCode": 200,
            "emailSent": success
        }
    except Exception as e :
        print('exception',e)
        return {
            "statusCode": 400
        }

