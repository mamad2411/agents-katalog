---
name: aws-serverless
description: "Habilidade especializada para construir aplicações serverless prontas para produção na AWS. Abrange funções Lambda, API Gateway, DynamoDB, padrões orientados a eventos SQS/SNS, deployment com SAM/CDK e otimização de cold start."
source: vibeship-spawner-skills (Apache 2.0)
---

# AWS Serverless

## Padrões

### Padrão Lambda Handler

Estrutura apropriada de função Lambda com tratamento de erros

**Quando usar**: ['Qualquer implementação de função Lambda', 'Handlers de API, processadores de eventos, tarefas agendadas']

```javascript
// Node.js Lambda Handler
// handler.js

// Inicializar fora do handler (reutilizado em invocações)
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

// Função handler
exports.handler = async (event, context) => {
  // Opcional: Não esperar pelo event loop estar vazio (Node.js)
  context.callbackWaitsForEmptyEventLoop = false;

  try {
    // Parse da entrada baseado na origem do evento
    const body = typeof event.body === 'string'
      ? JSON.parse(event.body)
      : event.body;

    // Lógica de negócio
    const result = await processRequest(body);

    // Retornar resposta compatível com API Gateway
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    console.error('Erro:', JSON.stringify({
      error: error.message,
      stack: error.stack,
      requestId: context.awsRequestId
    }));

    return {
      statusCode: error.statusCode || 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: error.message || 'Erro interno do servidor'
      })
    };
  }
};

async function processRequest(data) {
  // Sua lógica de negócio aqui
  const result = await docClient.send(new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: { id: data.id }
  }));
  return result.Item;
}
```

```python
# Python Lambda Handler
# handler.py

import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Inicializar fora do handler (reutilizado em invocações)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    try:
        # Parse da entrada
```

### Padrão Integração API Gateway

Integração REST API e HTTP API com Lambda

**Quando usar**: ['Construir REST APIs com suporte em Lambda', 'Precisa de endpoints HTTP para funções']

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

Resources:
  # HTTP API (recomendado para casos simples)
  HttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      CorsConfiguration:
        AllowOrigins:
          - "*"
        AllowMethods:
          - GET
          - POST
          - DELETE
        AllowHeaders:
          - "*"

  # Funções Lambda
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

  # Tabela DynamoDB
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

Outputs:
  ApiUrl:
    Value: !Sub "https://${HttpApi}.execute-api.${AWS::Region}.amazonaws.com/prod"
```

```javascript
// src/handlers/get.js
const { getItem } = require('../lib/dynamodb');

exports.handler = async (event) => {
  const id = event.pathParameters?.id;

  if (!id) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Parâmetro id ausente' })
    };
  }

  const item =
```

### Padrão Event-Driven SQS

Lambda acionada por SQS para processamento assíncrono confiável

**Quando usar**: ['Processamento desacoplado e assíncrono', 'Precisa de lógica de retry e DLQ', 'Processamento de mensagens em lotes']

```yaml
# template.yaml
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
              - ReportBatchItemFailures  # Tratamento de falha parcial de lote

  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180  # 6x timeout Lambda
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      MessageRetentionPeriod: 1209600  # 14 dias
```

```javascript
// src/handlers/processor.js
exports.handler = async (event) => {
  const batchItemFailures = [];

  for (const record of event.Records) {
    try {
      const body = JSON.parse(record.body);
      await processMessage(body);
    } catch (error) {
      console.error(`Falha ao processar mensagem ${record.messageId}:`, error);
      // Reportar este item como falhado (será retentado)
      batchItemFailures.push({
        itemIdentifier: record.messageId
      });
    }
  }

  // Retornar itens falhados para retry
  return { batchItemFailures };
};

async function processMessage(message) {
  // Sua lógica de processamento
  console.log('Processando:', message);

  // Simular trabalho
  await saveToDatabase(message);
}
```

```python
# Versão Python
import json
import logging

logger = logging.getLogger()

def handler(event, context):
    batch_item_failures = []

    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            process_message(body)
        except Exception as e:
            logger.error(f"Falha ao processar {record['messageId']}: {e}")
            batch_item_failures.append({
                'itemIdentifier': record['messageId']
            })

    return {'batchItemFailures': batch_item_failures}
```

## Anti-padrões

### ❌ Lambda Monolítica

**Por que é ruim**: Pacotes de deployment grandes causam cold starts lentos.
Difícil escalar operações individuais.
Atualizações afetam todo o sistema.

### ❌ Dependências Grandes

**Por que é ruim**: Aumenta o tamanho do pacote de deployment.
Desacelera significativamente cold starts.
A maioria do SDK/biblioteca pode estar não utilizada.

### ❌ Chamadas Síncronas em VPC

**Por que é ruim**: Lambdas anexadas a VPC têm overhead de configuração ENI.
Lookups de DNS ou conexões bloqueadas pioram cold starts.

## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|--------|
| Problema | alta | ## Medir sua fase INIT |
| Problema | alta | ## Definir timeout apropriado |
| Problema | alta | ## Aumentar alocação de memória |
| Problema | média | ## Verificar configuração de VPC |
| Problema | média | ## Avisar Lambda para não esperar pelo event loop |
| Problema | média | ## Para uploads de arquivos grandes |
| Problema | alta | ## Usar buckets/prefixos diferentes |