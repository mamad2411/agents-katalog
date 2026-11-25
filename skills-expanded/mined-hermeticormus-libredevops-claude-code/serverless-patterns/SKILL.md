---
name: serverless-patterns
description: "Serverless patterns: a production Lambda configuration in Terraform, Serverless Framework and SAM templates, EventBridge rules that trigger Lambda, and DynamoDB single-table design. Use when building or deploying event-driven AWS workloads."
---

# Serverless Patterns

Lambda deployment, API Gateway, SQS event-driven patterns, Step Functions, and cold start optimization.

## Lambda with Terraform (Production Config)

```hcl
# Lambda function with X-Ray, VPC, and provisioned concurrency
resource "aws_lambda_function" "payment_processor" {
  function_name = "payment-processor"
  handler       = "handler.handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda.arn

  # Build artifact (use CI/CD to keep current)
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  # Or from ECR (container image Lambda)
  # package_type = "Image"
  # image_uri    = "${aws_ecr_repository.lambda.repository_url}:latest"

  timeout     = 30     # Seconds
  memory_size = 512    # MB (also affects CPU allocation proportionally)

  environment {
    variables = {
      TABLE_NAME   = aws_dynamodb_table.payments.name
      QUEUE_URL    = aws_sqs_queue.results.url
      POWERTOOLS_SERVICE_NAME = "payment-processor"
      LOG_LEVEL    = "INFO"
    }
  }

  # X-Ray tracing
  tracing_config {
    mode = "Active"
  }

  # VPC config (needed to access RDS, ElastiCache)
  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.lambda.id]
  }

  # Dead letter queue for async invocations
  dead_letter_config {
    target_arn = aws_sqs_queue.lambda_dlq.arn
  }

  reserved_concurrent_executions = 100  # Limit blast radius
}

# Provisioned concurrency on an alias (eliminates cold starts)
resource "aws_lambda_alias" "prod" {
  name             = "prod"
  function_name    = aws_lambda_function.payment_processor.function_name
  function_version = aws_lambda_function.payment_processor.version
}

resource "aws_lambda_provisioned_concurrency_config" "prod" {
  function_name                  = aws_lambda_function.payment_processor.function_name
  qualifier                      = aws_lambda_alias.prod.name
  provisioned_concurrent_executions = 5
}

# IAM: least-privilege execution role
resource "aws_iam_role" "lambda" {
  name = "payment-processor-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda" {
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = ["xray:PutTraceSegments", "xray:PutTelemetryRecords"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem"]
        Resource = aws_dynamodb_table.payments.arn
      },
      {
        Effect   = "Allow"
        Action   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
        Resource = aws_sqs_queue.input.arn
      },
      # For VPC: attach the AWS managed policy
      {
        Effect = "Allow"
        Action = ["ec2:CreateNetworkInterface", "ec2:DescribeNetworkInterfaces", "ec2:DeleteNetworkInterface"]
        Resource = "*"
      }
    ]
  })
}
```

## Serverless Framework / SAM Template

```yaml
# template.yaml (AWS SAM)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.12
    Timeout: 30
    MemorySize: 512
    Tracing: Active
    Environment:
      Variables:
        POWERTOOLS_SERVICE_NAME: !Ref AWS::StackName
        LOG_LEVEL: INFO
    Layers:
      - !Sub arn:aws:lambda:${AWS::Region}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-x86_64:4

Resources:
  PaymentApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn
      AccessLogSetting:
        DestinationArn: !GetAtt ApiLogGroup.Arn

  ProcessPaymentFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.handler
      CodeUri: src/payment/
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref PaymentsTable
        - SQSSendMessagePolicy:
            QueueName: !GetAtt ResultsQueue.QueueName
      Events:
        ApiEvent:
          Type: HttpApi
          Properties:
            Path: /payments
            Method: POST
            ApiId: !Ref PaymentApi
        SqsEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt InputQueue.Arn
            BatchSize: 10
            FunctionResponseTypes:
              - ReportBatchItemFailures

  PaymentsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      TableName: payments
      AttributeDefinitions:
        - AttributeName: payment_id
          AttributeType: S
      KeySchema:
        - AttributeName: payment_id
          KeyType: HASH
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
```

## EventBridge Rule -> Lambda

```hcl
# Trigger Lambda on S3 event via EventBridge
resource "aws_cloudwatch_event_rule" "s3_upload" {
  name           = "s3-image-upload"
  event_bus_name = "default"

  event_pattern = jsonencode({
    source      = ["aws.s3"]
    detail-type = ["Object Created"]
    detail = {
      bucket = { name = [aws_s3_bucket.uploads.id] }
      object = { key = [{ suffix = ".jpg" }, { suffix = ".png" }] }
    }
  })
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule           = aws_cloudwatch_event_rule.s3_upload.name
  target_id      = "ProcessImage"
  arn            = aws_lambda_function.image_processor.arn

  # Dead letter for failed EventBridge deliveries
  dead_letter_config {
    arn = aws_sqs_queue.event_dlq.arn
  }

  retry_policy {
    maximum_event_age_in_seconds = 3600
    maximum_retry_attempts       = 2
  }
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_processor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_upload.arn
}
```

## DynamoDB Single-Table Design

```python
# Single-table: all entities in one table, overloaded keys
# PK = entity type + ID, SK = sort key for hierarchies

# Entity types in one table:
# USER#usr_123        | PROFILE           -> user profile
# USER#usr_123        | ORDER#ord_456     -> user's order
# ORDER#ord_456       | PAYMENT#pay_789   -> order's payment
# PRODUCT#prod_101    | METADATA          -> product info

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('app-table')

# Write a user
table.put_item(Item={
    "PK": "USER#usr_123",
    "SK": "PROFILE",
    "email": "user@example.com",
    "created_at": "2024-01-15T10:00:00Z",
    "GSI1PK": "EMAIL#user@example.com",  # GSI for email lookup
    "GSI1SK": "USER#usr_123"
})

# Get all orders for a user (single-table query)
response = table.query(
    KeyConditionExpression=Key("PK").eq("USER#usr_123") & Key("SK").begins_with("ORDER#")
)

# Get user by email (GSI query)
response = table.query(
    IndexName="GSI1",
    KeyConditionExpression=Key("GSI1PK").eq("EMAIL#user@example.com")
)
```
