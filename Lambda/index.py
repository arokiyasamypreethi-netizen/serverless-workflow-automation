import json
import boto3
import os

sns = boto3.client('sns')


def lambda_handler(event, context):
    """
    Triggered by SQS. Each record contains a JSON message with
    name, department, and project fields. Extracts the data and
    publishes a formatted summary to SNS, which emails the result.
    """
    for record in event['Records']:
        body = json.loads(record['body'])

        name = body.get("name", "Unknown")
        department = body.get("department", "Unknown")
        project = body.get("project", "Unknown")

        message = f"""
        Processing Successful

        Name: {name}
        Department: {department}
        Project: {project}
        """

        print(message)

        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject="Lambda Processing Completed",
            Message=message
        )

    return {
        "statusCode": 200,
        "body": "Success"
    }
