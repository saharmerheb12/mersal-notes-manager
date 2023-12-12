import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

CHARSET = "UTF-8"
SENDER= os.environ["SENDER"]
RECIPIENT= os.environ["RECIPIENT"]
SES_REGION= os.environ["SES_REGION"]
SUBJECT_TEMPLATE= os.environ["SUBJECT_TEMPLATE"]
EMAIL_TEMPLATE_PATH = './assets/email_template.txt'
EMAIL_TEMPLATE = Path(EMAIL_TEMPLATE_PATH).read_text()

def send(objectKey, downloadPath):

    orderId = objectKey.split('.')[0]
    subject = SUBJECT_TEMPLATE.replace('#order-id#',orderId)
    body = EMAIL_TEMPLATE.replace('#pre-signed-url#', downloadPath).replace('#order-id#',orderId)

    client = boto3.client('ses', region_name=SES_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        print("Email sent! Message ID:",response['MessageId'])
        return True
