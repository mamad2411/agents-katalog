---
name: dynamodb-patterns
description: "When to activate: DynamoDB, single table design, GSI, LSI, DynamoDB streams, DAX, capacity, AWS NoSQL"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# DynamoDB Patterns

## Single Table Design

```python
# All entities in one table — access pattern drives key design
# PK = partition key, SK = sort key

# Entity types stored together:
# USER#<userId>    | PROFILE           → user profile
# USER#<userId>    | ORDER#<orderId>   → user's orders
# ORDER#<orderId>  | ORDER#<orderId>   → order detail
# PRODUCT#<id>     | PRODUCT#<id>      → product

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('MyApp')

# Write user
table.put_item(Item={
    'PK': f'USER#{user_id}',
    'SK': 'PROFILE',
    'name': 'Alice',
    'email': 'alice@example.com',
    'GSI1PK': f'EMAIL#{email}',   # GSI for email lookup
    'GSI1SK': 'PROFILE',
    'type': 'User'
})

# Write order linked to user
table.put_item(Item={
    'PK': f'USER#{user_id}',
    'SK': f'ORDER#{order_id}',
    'GSI1PK': f'ORDER#{order_id}',
    'GSI1SK': f'ORDER#{order_id}',
    'total': Decimal('99.99'),
    'status': 'pending',
    'created_at': datetime.utcnow().isoformat()
})
```

## GSI and LSI

```python
# Global Secondary Index — different PK, eventual consistency
# Defined at table creation or added later (reads from GSI)

# Query GSI: find user by email
response = table.query(
    IndexName='GSI1',
    KeyConditionExpression=Key('GSI1PK').eq(f'EMAIL#{email}') &
                           Key('GSI1SK').eq('PROFILE')
)

# Query orders by status (GSI2: status + created_at)
response = table.query(
    IndexName='GSI2-status-date',
    KeyConditionExpression=Key('GSI2PK').eq(f'STATUS#pending') &
                           Key('GSI2SK').begins_with('2024-01'),
    Limit=50,
    ScanIndexForward=False  # newest first
)

# Get all orders for a user (base table, sort key prefix)
response = table.query(
    KeyConditionExpression=Key('PK').eq(f'USER#{user_id}') &
                           Key('SK').begins_with('ORDER#'),
    Limit=20,
    ScanIndexForward=False
)
```

## Transactions

```python
# TransactWrite — all-or-nothing across up to 100 items / 4MB
dynamodb_client = boto3.client('dynamodb')

response = dynamodb_client.transact_write(Items=[
    {
        'Update': {
            'TableName': 'MyApp',
            'Key': {'PK': {'S': f'USER#{from_id}'}, 'SK': {'S': 'WALLET'}},
            'UpdateExpression': 'ADD balance :delta',
            'ExpressionAttributeValues': {':delta': {'N': str(-amount)},
                                          ':min': {'N': '0'}},
            'ConditionExpression': 'balance >= :min'
        }
    },
    {
        'Update': {
            'TableName': 'MyApp',
            'Key': {'PK': {'S': f'USER#{to_id}'}, 'SK': {'S': 'WALLET'}},
            'UpdateExpression': 'ADD balance :delta',
            'ExpressionAttributeValues': {':delta': {'N': str(amount)}}
        }
    }
])
```

## Streams and DAX

```python
# DynamoDB Streams → Lambda trigger for event-driven processing
# Lambda receives stream records with NEW and OLD images

def handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']
            # Deserialize from DynamoDB format
        elif record['eventName'] == 'MODIFY':
            old_item = record['dynamodb']['OldImage']
            new_item = record['dynamodb']['NewImage']

# DAX — in-memory cache, microsecond reads
import amazondax
dax_client = amazondax.AmazonDaxClient(endpoints=['dax-cluster.abc.dax-clusters.amazonaws.com:8111'])
# Use dax_client same as boto3 table resource — transparent caching
```

## Capacity Modes

```python
# On-demand: pay per request, scales automatically
# Provisioned: specify RCU/WCU, cheaper at predictable load

# Auto Scaling (CloudFormation)
# TargetValue: 70% utilization
# MinCapacity: 5 WCU, MaxCapacity: 1000 WCU

# Batch operations (up to 25 items per call)
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)
    for key in keys_to_delete:
        batch.delete_item(Key=key)
```

## Design Rules

- Design access patterns first, schema second
- 1 table per service (not per entity)
- GSI max 20 per table; project only needed attributes (`KEYS_ONLY` or `INCLUDE`)
- Use `begins_with` / `between` on SK for hierarchical queries
- Avoid hot partitions: spread writes across partition key space
- TTL attribute for auto-expiry (seconds since epoch)
- Never `Scan` in production — always `Query` with PK
