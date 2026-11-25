---
name: aws-serverless
description: Building production-ready serverless applications on AWS. Use when working with Lambda, API Gateway, SQS, SNS, DynamoDB Streams, SAM/CDK deployment or optimizing cold starts.
---

# AWS Serverless

Skill para construir aplicaciones serverless production-ready en AWS. Cubre Lambda functions, API Gateway (REST/HTTP/WebSocket), arquitecturas event-driven con SQS/SNS/DynamoDB Streams, modelado DynamoDB, despliegue con SAM/CDK, y optimización de cold starts.

## Principios fundamentales

- Serverless-first: diseñar para ejecución efímera, stateless y event-driven.
- Cada Lambda = una responsabilidad. No monolitos Lambda.
- Inicializar clientes AWS fuera del handler (reutilización en warm starts).
- Usar partial batch failure reporting en SQS/Kinesis/DynamoDB Streams.
- Dead Letter Queues (DLQ) obligatorias en toda cola y suscripción.
- Idempotencia en todo handler que procese eventos (at-least-once delivery).
- Observabilidad desde el día 1: structured logging, tracing, métricas custom.

## Patrones de Lambda Handler

### Node.js Handler (TypeScript)

```typescript
import { Logger } from '@aws-lambda-powertools/logger';
import { Tracer } from '@aws-lambda-powertools/tracer';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';
import type { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from 'aws-lambda';

const logger = new Logger({ serviceName: 'mi-servicio' });
const tracer = new Tracer({ serviceName: 'mi-servicio' });

// Inicializar fuera del handler (warm start reuse)
const client = tracer.captureAWSv3Client(new DynamoDBClient({}));
const docClient = DynamoDBDocumentClient.from(client);
const TABLE_NAME = process.env.TABLE_NAME!;

export const handler = async (
  event: APIGatewayProxyEventV2
): Promise<APIGatewayProxyResultV2> => {
  try {
    const body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    const result = await processRequest(body);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result),
    };
  } catch (error) {
    logger.error('Error processing request', { error });
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};
```

### Python Handler

```python
import json
import os
import logging
import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="mi-servicio")
tracer = Tracer(service="mi-servicio")
metrics = Metrics(namespace="MiApp", service="mi-servicio")

# Inicializar fuera del handler
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    try:
        body = json.loads(event.get('body', '{}'))
        result = process_request(body)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.exception("Error processing request")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

## API Gateway Integration

### HTTP API (recomendado para casos simples)

```yaml
# template.yaml (SAM)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref ItemsTable
        POWERTOOLS_SERVICE_NAME: mi-servicio

Resources:
  HttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      CorsConfiguration:
        AllowOrigins: ["*"]
        AllowMethods: [GET, POST, PUT, DELETE]
        AllowHeaders: ["*"]

  GetItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/get.handler
      Events:
        GetItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items/{id}
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref ItemsTable

  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/create.handler
      Events:
        CreateItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable

  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST
```

### REST API (cuando se necesita validación, throttling, API keys)

```yaml
  RestApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn
      Models:
        CreateItemModel:
          type: object
          required: [name, price]
          properties:
            name: { type: string, minLength: 1 }
            price: { type: number, minimum: 0 }
```

## Patrones Event-Driven

### SQS con Partial Batch Failure

```yaml
Resources:
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/processor.handler
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
            FunctionResponseTypes:
              - ReportBatchItemFailures

  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180  # 6x Lambda timeout
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      MessageRetentionPeriod: 1209600  # 14 días
```

```typescript
// Handler con partial batch failure reporting
import type { SQSEvent, SQSBatchResponse } from 'aws-lambda';

export const handler = async (event: SQSEvent): Promise<SQSBatchResponse> => {
  const batchItemFailures: SQSBatchResponse['batchItemFailures'] = [];

  for (const record of event.Records) {
    try {
      const body = JSON.parse(record.body);
      await processMessage(body);
    } catch (error) {
      console.error(`Failed message ${record.messageId}:`, error);
      batchItemFailures.push({ itemIdentifier: record.messageId });
    }
  }

  return { batchItemFailures };
};
```

### SNS Fan-Out

```yaml
  OrderTopic:
    Type: AWS::SNS::Topic

  EmailNotificationFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/email.handler
      Events:
        SNSEvent:
          Type: SNS
          Properties:
            Topic: !Ref OrderTopic
            FilterPolicy:
              type: [order_confirmed]

  InventoryUpdateFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/inventory.handler
      Events:
        SNSEvent:
          Type: SNS
          Properties:
            Topic: !Ref OrderTopic
```

### DynamoDB Streams

```yaml
  StreamProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/stream.handler
      Events:
        DDBStream:
          Type: DynamoDB
          Properties:
            Stream: !GetAtt OrdersTable.StreamArn
            StartingPosition: TRIM_HORIZON
            BatchSize: 100
            MaximumBatchingWindowInSeconds: 5
            FunctionResponseTypes:
              - ReportBatchItemFailures
            FilterCriteria:
              Filters:
                - Pattern: '{"eventName": ["INSERT", "MODIFY"]}'
```

## Step Functions (orquestación)

```yaml
  OrderStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      DefinitionUri: statemachine/order.asl.json
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref ValidateOrderFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref ProcessPaymentFunction
        - DynamoDBCrudPolicy:
            TableName: !Ref OrdersTable
```

## Optimización de Cold Starts

### Estrategias generales

| Estrategia | Impacto | Complejidad |
|---|---|---|
| Minimizar bundle size | Alto | Bajo |
| Lazy loading de dependencias | Medio | Bajo |
| Inicializar clientes fuera del handler | Alto | Bajo |
| Aumentar memoria (más CPU) | Medio | Bajo |
| Provisioned Concurrency | Alto | Medio |
| SnapStart (Java) | Alto | Bajo |
| Evitar VPC si no es necesario | Alto | Bajo |

### Node.js específico

```typescript
// ✅ Lazy loading para dependencias pesadas
let heavyLib: typeof import('heavy-lib') | undefined;

const getHeavyLib = async () => {
  if (!heavyLib) {
    heavyLib = await import('heavy-lib');
  }
  return heavyLib;
};

// ✅ Tree shaking: importar solo lo necesario
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';  // ✅
// import AWS from 'aws-sdk';  // ❌ SDK v2 completo
```

### Python específico

```python
# ✅ Lazy loading
_s3_client = None

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client('s3')
    return _s3_client
```

### Configuración de memoria

```bash
# Usar AWS Lambda Power Tuning para encontrar el sweet spot
# https://github.com/alexcasalboni/aws-lambda-power-tuning
sam deploy --template-file power-tuning.yaml
```

## Seguridad Serverless

- IAM: least privilege por función. Usar SAM policy templates.
- No hardcodear secretos. Usar SSM Parameter Store o Secrets Manager.
- Validar todo input del evento.
- CORS restrictivo en producción (no `*`).
- API keys + usage plans para rate limiting en REST API.
- Cognito o Lambda authorizers para autenticación.

## Anti-patrones

- ❌ Lambda monolítico con múltiples responsabilidades.
- ❌ Dependencias pesadas que inflan el bundle (SDK v2 completo, ORM pesados).
- ❌ Crear clientes AWS dentro del handler (nuevo cliente por invocación).
- ❌ No usar DLQ en colas SQS ni suscripciones SNS.
- ❌ Ignorar partial batch failure reporting (reprocesar todo el batch).
- ❌ Timeout de Lambda > VisibilityTimeout de SQS (mensajes duplicados).
- ❌ Llamadas síncronas en cadena entre Lambdas (usar Step Functions).
- ❌ VPC sin necesidad real (agrega latencia al cold start).
- ❌ `console.log` sin estructura (imposible de filtrar en CloudWatch Insights).
- ❌ No tener idempotencia en handlers event-driven.

## Checklist de revisión Serverless

- [ ] Cada Lambda tiene una sola responsabilidad.
- [ ] Clientes AWS inicializados fuera del handler.
- [ ] Partial batch failure reporting habilitado en SQS/Kinesis/Streams.
- [ ] DLQ configurada en todas las colas y suscripciones.
- [ ] Idempotencia implementada donde aplica.
- [ ] Structured logging con Powertools.
- [ ] Tracing activo (X-Ray o Powertools Tracer).
- [ ] IAM least privilege por función.
- [ ] Input validado en cada handler.
- [ ] Cold start medido y optimizado.
- [ ] Timeout y memoria configurados según carga real.
- [ ] Tests unitarios y de integración.
