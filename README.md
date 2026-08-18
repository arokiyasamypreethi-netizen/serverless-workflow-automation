# Serverless Workflow Automation — AWS

An event-driven serverless pipeline built entirely with AWS managed services and provisioned as Infrastructure as Code using CloudFormation. A message dropped into an SQS queue automatically triggers a Lambda function, which processes the data and sends an email notification via SNS — with CloudWatch monitoring Lambda execution and alarming on errors.

## Architecture

```
JSON message → SQS Queue → Lambda (extracts data) → SNS Topic → Email notification
                                    ↓
                            CloudWatch Logs + Alarm (monitors errors)
```

## AWS Services Used
- **Amazon SQS** — receives incoming JSON messages, acts as the Lambda event source
- **AWS Lambda** (Python) — processes each message, extracts fields, publishes results to SNS
- **Amazon SNS** — delivers email notifications on successful processing
- **Amazon CloudWatch** — logs Lambda execution and alarms if errors occur (≥1 error within a 5-minute window)
- **AWS CloudFormation** — provisions all resources (Lambda, SQS, SNS, IAM Role, Event Source Mapping, CloudWatch Alarm) automatically from a single template — no manual console clicking

## Deployment

1. Deploy the stack, passing your notification email as a parameter:
```
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name ServerlessAutomationWorkflow \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides NotificationEmail=you@example.com
```

2. Confirm the SNS email subscription (AWS sends a confirmation link to the address provided).

3. Send a test message to the SQS queue (via AWS Console → SQS → Send message, or the CLI):
```json
{
  "name": "Preethi",
  "department": "Physics",
  "project": "Serverless Workflow Automation"
}
```

4. Within seconds, the Lambda function processes the message and an email notification arrives via SNS.

## Verified Working
- CloudFormation stack deployed successfully — `CREATE_COMPLETE` — creating all 7 resources in one pass
- Lambda correctly triggered by SQS messages, confirmed via CloudWatch Logs showing successful `REPORT` entries
- Email notification delivered end-to-end, containing the extracted name/department/project fields
- CloudWatch Alarm configured and tested to fire on Lambda errors

## Files
- `template.yaml` — the full CloudFormation template (all resources)
- `lambda/index.py` — the Lambda function code, extracted for readability (inlined in the actual template's `ZipFile` property)

## Notes
This project was built and fully tested on AWS, then the stack was deliberately deleted afterward to avoid ongoing costs from long-running Lambda/SQS/SNS resources — a routine cost-management practice, not a sign the project doesn't work. The template above is the exact, real, deployed configuration (resource names match the CloudFormation console output at the time it was running), and can be redeployed identically at any time.

## Tech used
AWS Lambda, SQS, SNS, CloudWatch, CloudFormation (IaC), Python, IAM
