# messaging-SNS-SQS-fanout-pattern
Implement a Fan-Out pattern using AWS. Utilize an SNS Topic with two SQS subscribers, each triggering a dedicated Lambda function. The first Lambda function generates thumbnails for uploaded images (PNG, JPG, JPEG) and saves them to an S3 bucket. The second Lambda function records the metadata of image files in a DynamoDB table.
