# from Github - 2

import boto3
import json
from dateutil.parser import parse
from urllib.parse import unquote_plus

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("hw09-image-metadata")

def lambda_handler(event, context):
    for sqs_message in event['Records']:
        # Print the SQS message to see what it looks like
        print(f"Received SQS message: {sqs_message}")
        
        # Parse the message body from the SQS message
        msg_body = json.loads(sqs_message['body'])
        
        # Attempt to parse the S3 event message, handling potential issues
        try:
            # Check if 'Message' is URL-encoded and decode if necessary
            if 'Message' in msg_body:
                message_to_load = unquote_plus(msg_body['Message'])
            else:
                print("No 'Message' found in msg_body: ", msg_body)
                continue
            
            # The actual message is JSON-stringified in the 'Message' field
            s3_event = json.loads(message_to_load)
            
            # Print the decoded S3 event
            print(f"Decoded S3 event: {s3_event}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from message: {msg_body.get('Message', 'No Message Found')} - Error: {e}")
            continue  # Skip this record and continue with the next one

        # Loop through the record(s) in the S3 event
        for record in s3_event['Records']:
            object_key = record['s3']['object']['key']
            object_size = record['s3']['object']['size']
            event_time = parse(record['eventTime'])

            # Print the values to be written to the database
            print(f"Writing to DynamoDB - FileName: {object_key}, Size: {object_size}, DateModified: {event_time.isoformat()}")

            # Write to DynamoDB
            writeRecordToDynamo(object_key, object_size, event_time)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def writeRecordToDynamo(name, size, dateModified):
    try:
        response = table.put_item(
            Item = {
                "FileName"    : name,
                "Size"        : size,
                "DateModified": dateModified.isoformat()
            }
        )
        # Print response from DynamoDB after writing data
        print(f"DynamoDB response: {response}")
    except Exception as e:
        print(f"Error writing to DynamoDB: {e}")
