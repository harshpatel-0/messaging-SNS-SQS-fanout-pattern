import boto3
import json

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("hw09-image-metadata")

def lambda_handler(event, context):

    # TODO: you need to figure out how to obtain these three values from the "event" object

    writeRecordToDynamo(object_key, object_size, event_time)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def writeRecordToDynamo(name, size, dateModified):
    try:
        table.put_item(
            Item = {
                "FileName"    : name,
                "size"        : size,
                "dateModified": dateModified
            }
        )
    except Exception as e:
        print("Error writing to DDB", e)