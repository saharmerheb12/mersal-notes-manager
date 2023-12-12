import os
import json
import boto3
import urllib.parse

from qr_manager import generate


def handler(event, context):

    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8').split('.')

    success, local_path, local_name = generate(object_key[0],object_key[1])

    if success == True:
        s3 = boto3.client("s3")
        bucket_name = os.environ["QR_BUCKET"]

        result = s3.upload_file(local_path, bucket_name, local_name)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "key": local_name,
                "result": result
            })
        }
    else:
        error = local_path
        return {
            "statusCode": 400,
            "error": error
        }

