# Much of this code taken from:
# https://docs.aws.amazon.com/lambda/latest/dg/with-s3-tutorial.html

import json
import boto3
# import os
# import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
# import PIL.Image
            
s3_client = boto3.client('s3')

THUMBNAIL_BUCKET = 'hw09-thumbnails'

def lambda_handler(event, context):

    # TODO: you need to determing how to parse the "event" object in order to get the msg_body needed below

    records = json.loads(msg_body)
    for record in records['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        #Use the temp storage in lambda to download the image and resize it
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        #Download the image from S3 (assumes this function has the IAM policy to do so, which in
        #   the Learner Lab it will because LabRole is over-provisioned by design)
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        #Use the original bucket name and key name to create the destination names
        #You can also hardcode the bucket name.
        #But MAKE SURE you do not write the thumbnails back to the orginal bucket!!!!
        #   That would create an infinite loop and get your account locked!
        # THUMBNAIL_BUCKET = '{}-resized'.format(bucket)
        THUMBNAIL_FILE_NAME = 'resized-{}'.format(key)
        s3_client.upload_file(upload_path, THUMBNAIL_BUCKET, THUMBNAIL_FILE_NAME)

    return {
        'statusCode': 200,
        'body': json.dumps('Successful image processing!')
    }

def resize_image(image_path, resized_path):
  with Image.open(image_path) as image:
    image.thumbnail(tuple(x / 2 for x in image.size))
    image.save(resized_path)
            
