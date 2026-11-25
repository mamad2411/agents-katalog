---
name: azure-servicebus-toolkit
description: Consolidated toolkit for azure-servicebus. Covers azure-servicebus-py, azure-servicebus-ts, azure-servicebus-dotnet
---
# Azure Servicebus Toolkit

## Core Capabilities
# Azure Servicebus Toolkit

# Azure Service Bus SDK for Python

Enterprise messaging for reliable cloud communication with queues and pub/sub topics.

## Installation

```bash
pip install azure-servicebus azure-identity
```

## Environment Variables

```bash
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
SERVICEBUS_QUEUE_NAME=myqueue
SERVICEBUS_TOPIC_NAME=mytopic
SERVICEBUS_SUBSCRIPTION_NAME=mysubscription
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

credential = DefaultAzureCredential()
namespace = "<namespace>.servicebus.windows.net"

client = ServiceBusClient(
    fully_qualified_namespace=namespace,
    credential=credential
)
```

## Client Types

| Client | Purpose | Get From |
|--------|---------|----------|
| `ServiceBusClient` | Connection management | Direct instantiation |
| `ServiceBusSender` | Send messages | `client.get_queue_sender()` / `get_topic_sender()` |
| `ServiceBusReceiver` | Receive messages | `client.get_queue_receiver()` / `get_subscription_receiver()` |

## Send Messages (Async)

```python
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.identity.aio import DefaultAzureCredential

async def send_messages():
    credential = DefaultAzureCredential()
    
    async with ServiceBusClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        credential=credential
    ) as client:
        sender = client.get_queue_sender(queue_name="myqueue")
        
        async with sender:
            # Single message
            message = ServiceBusMessage("Hello, Service Bus!")
            await sender.send_messages(message)
            
            # Batch of messages
            messages = [ServiceBusMessage(f"Message {i}") for i in range(10)]
            await sender.send_messages(messages)
            
            # Message batch (for size control)
            batch = await sender.create_message_batch()
            for i in range(100):
                try:
                    batch.add_message(ServiceBusMessage(f"Batch message {i}"))
                except ValueError:  # Batch full
                    await sender.send_messages(batch)
                    batch = await sender.create_message_batch()
                    batch.add_message(ServiceBusMessage(f"Batch message {i}"))
            await sender.send_messages(batch)

asyncio.run(send_messages())
```

## Receive Messages (Async)

```python
async def receive_messages():
    credential = DefaultAzureCredential()
    
    async with ServiceBusClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        credential=credential
    ) as client:
        receiver = client.get_queue_receiver(queue_name="myqueue")
        
        async with receiver:
            # Receive batch
            messages = await receiver.receive_messages(
                max_message_count=10,
                max_wait_time=5  # seconds
            )
            
            for msg in messages:
                print(f"Received: {str(msg)}")
                await receiver.complete_message(msg)  # Remove from queue

asyncio.run(receive_messages())
```

## Receive Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `PEEK_LOCK` (default) | Message locked, must complete/abandon | Reliable processing |
| `RECEIVE_AND_DELETE` | Removed immediately on receive | At-most-once delivery |

```python
from azure.servicebus import ServiceBusReceiveMode

receiver = client.get_queue_receiver(
    queue_name="myqueue",
    receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE
)
```

## Message Settlement

```python
async with receiver:
    messages = await receiver.receive_messages(max_message_count=1)
    
    for msg in messages:
        try:
            # Process message...
            await receiver.complete_message(msg)  # Success - remove from queue
        except ProcessingError:
            await receiver.abandon_message(msg)  # Retry later
        except PermanentError:
            await receiver.dead_letter_message(
                msg,
                reason="ProcessingFailed",
                error_description="Could not process"
            )
```

| Action | Effect |
|--------|--------|
| `complete_message()` | Remove from queue (success) |
| `abandon_message()` | Release lock, retry immediately |
| `dead_letter_message()` | Move to dead-letter queue |
| `defer_message()` | Set aside, receive by sequence number |

## Topics and Subscriptions

```python
# Send to topic
sender = client.get_topic_sender(topic_name="mytopic")
async with sender:
    await sender.send_messages(ServiceBusMessage("Topic message"))

# Receive from subscription
receiver = client.get_subscription_receiver(
    topic_name="mytopic",
    subscription_name="mysubscription"
)
async with receiver:
    messages = await receiver.receive_messages(max_message_count=10)
```

## Sessions (FIFO)

```python
# Send with session
message = ServiceBusMessage("Session message")
message.session_id = "order-123"
await sender.send_messages(message)

# Receive from specific session
receiver = client.get_queue_receiver(
    queue_name="session-queue",
    session_id="order-123"
)

# Receive from next available session
from azure.servicebus import NEXT_AVAILABLE_SESSION
receiver = client.get_queue_receiver(
    queue_name="session-queue",
    session_id=NEXT_AVAILABLE_SESSION
)
```

## Scheduled Messages

```python
from datetime import datetime, timedelta, timezone

message = ServiceBusMessage("Scheduled message")
scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=10)

# Schedule message
sequence_number = await sender.schedule_messages(message, scheduled_time)

# Cancel scheduled message
await sender.cancel_scheduled_messages(sequence_number)
```

## Dead-Letter Queue

```python
from azure.servicebus import ServiceBusSubQueue

# Receive from dead-letter queue
dlq_receiver = client.get_queue_receiver(
    queue_name="myqueue",
    sub_queue=ServiceBusSubQueue.DEAD_LETTER
)

async with dlq_receiver:
    messages = await dlq_receiver.receive_messages(max_message_count=10)
    for msg in messages:
        print(f"Dead-lettered: {msg.dead_letter_reason}")
        await dlq_receiver.complete_message(msg)
```

## Sync Client (for simple scripts)

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=DefaultAzureCredential()
) as client:
    with client.get_queue_sender("myqueue") as sender:
        sender.send_messages(ServiceBusMessage("Sync message"))
    
    with client.get_queue_receiver("myqueue") as receiver:
        for msg in receiver:
            print(str(msg))
            receiver.complete_message(msg)
```

## Best Practices

1. **Use async client** for production workloads
2. **Use context managers** (`async with`) for proper cleanup
3. **Complete messages** after successful processing
4. **Use dead-letter queue** for poison messages
5. **Use sessions** for ordered, FIFO processing
6. **Use message batches** for high-throughput scenarios
7. **Set `max_wait_time`** to avoid infinite blocking

## Reference Files

| File | Contents |
|------|----------|
| references/patterns.md | Competing consumers, sessions, retry patterns, request-response, transactions |
| references/dead-letter.md | DLQ handling, poison messages, reprocessing strategies |
| scripts/setup_servicebus.py | CLI for queue/topic/subscription management and DLQ monitoring |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Service Bus SDK for TypeScript

Enterprise messaging with queues, topics, and subscriptions.

## Installation

```bash
npm install @azure/service-bus @azure/identity
```

## Environment Variables

```bash
SERVICEBUS_NAMESPACE=<namespace>.servicebus.windows.net
SERVICEBUS_QUEUE_NAME=my-queue
SERVICEBUS_TOPIC_NAME=my-topic
SERVICEBUS_SUBSCRIPTION_NAME=my-subscription
```

## Authentication

```typescript
import { ServiceBusClient } from "@azure/service-bus";
import { DefaultAzureCredential } from "@azure/identity";

const fullyQualifiedNamespace = process.env.SERVICEBUS_NAMESPACE!;
const client = new ServiceBusClient(fullyQualifiedNamespace, new DefaultAzureCredential());
```

## Core Workflow

### Send Messages to Queue

```typescript
const sender = client.createSender("my-queue");

// Single message
await sender.sendMessages({
  body: { orderId: "12345", amount: 99.99 },
  contentType: "application/json",
});

// Batch messages
const batch = await sender.createMessageBatch();
batch.tryAddMessage({ body: "Message 1" });
batch.tryAddMessage({ body: "Message 2" });
await sender.sendMessages(batch);

await sender.close();
```

### Receive Messages from Queue

```typescript
const receiver = client.createReceiver("my-queue");

// Receive batch
const messages = await receiver.receiveMessages(10, { maxWaitTimeInMs: 5000 });
for (const message of messages) {
  console.log(`Received: ${message.body}`);
  await receiver.completeMessage(message);
}

await receiver.close();
```

### Subscribe to Messages (Event-Driven)

```typescript
const receiver = client.createReceiver("my-queue");

const subscription = receiver.subscribe({
  processMessage: async (message) => {
    console.log(`Processing: ${message.body}`);
    // Message auto-completed on success
  },
  processError: async (args) => {
    console.error(`Error: ${args.error}`);
  },
});

// Stop after some time
setTimeout(async () => {
  await subscription.close();
  await receiver.close();
}, 60000);
```

### Topics and Subscriptions

```typescript
// Send to topic
const topicSender = client.createSender("my-topic");
await topicSender.sendMessages({
  body: { event: "order.created", data: { orderId: "123" } },
  applicationProperties: { eventType: "order.created" },
});

// Receive from subscription
const subscriptionReceiver = client.createReceiver("my-topic", "my-subscription");
const messages = await subscriptionReceiver.receiveMessages(10);
```

## Message Sessions

```typescript
// Send session message
const sender = client.createSender("session-queue");
await sender.sendMessages({
  body: { step: 1, data: "First step" },
  sessionId: "workflow-123",
});

// Receive session messages
const sessionReceiver = await client.acceptSession("session-queue", "workflow-123");
const messages = await sessionReceiver.receiveMessages(10);

// Get/set session state
const state = await sessionReceiver.getSessionState();
await sessionReceiver.setSessionState(Buffer.from(JSON.stringify({ progress: 50 })));

await sessionReceiver.close();
```

## Dead-Letter Handling

```typescript
// Move to dead-letter
await receiver.deadLetterMessage(message, {
  deadLetterReason: "Validation failed",
  deadLetterErrorDescription: "Missing required field: orderId",
});

// Process dead-letter queue
const dlqReceiver = client.createReceiver("my-queue", { subQueueType: "deadLetter" });
const dlqMessages = await dlqReceiver.receiveMessages(10);
for (const msg of dlqMessages) {
  console.log(`DLQ Reason: ${msg.deadLetterReason}`);
  // Reprocess or log
  await dlqReceiver.completeMessage(msg);
}
```

## Scheduled Messages

```typescript
const sender = client.createSender("my-queue");

// Schedule for future delivery
const scheduledTime = new Date(Date.now() + 60000); // 1 minute from now
const sequenceNumber = await sender.scheduleMessages(
  { body: "Delayed message" },
  scheduledTime
);

// Cancel scheduled message
await sender.cancelScheduledMessages(sequenceNumber);
```

## Message Deferral

```typescript
// Defer message for later
await receiver.deferMessage(message);

// Receive deferred message by sequence number
const deferredMessage = await receiver.receiveDeferredMessages(message.sequenceNumber!);
await receiver.completeMessage(deferredMessage[0]);
```

## Peek Messages (Non-Destructive)

```typescript
const receiver = client.createReceiver("my-queue");

// Peek without removing
const peekedMessages = await receiver.peekMessages(10);
for (const msg of peekedMessages) {
  console.log(`Peeked: ${msg.body}`);
}
```

## Key Types

```typescript
import {
  ServiceBusClient,
  ServiceBusSender,
  ServiceBusReceiver,
  ServiceBusSessionReceiver,
  ServiceBusMessage,
  ServiceBusReceivedMessage,
  ProcessMessageCallback,
  ProcessErrorCallback,
} from "@azure/service-bus";
```

## Receive Modes

```typescript
// Peek-Lock (default) - message locked until completed/abandoned
const receiver = client.createReceiver("my-queue", { receiveMode: "peekLock" });
await receiver.completeMessage(message);   // Remove from queue
await receiver.abandonMessage(message);    // Return to queue
await receiver.deferMessage(message);      // Defer for later
await receiver.deadLetterMessage(message); // Move to DLQ

// Receive-and-Delete - message removed immediately
const receiver = client.createReceiver("my-queue", { receiveMode: "receiveAndDelete" });
```

## Best Practices

1. **Use Entra ID auth** - Avoid connection strings in production
2. **Reuse clients** - Create `ServiceBusClient` once, share across senders/receivers
3. **Close resources** - Always close senders/receivers when done
4. **Handle errors** - Implement `processError` callback for subscription receivers
5. **Use sessions for ordering** - When message order matters within a group
6. **Configure dead-letter** - Always handle DLQ messages
7. **Batch sends** - Use `createMessageBatch()` for multiple messages

## Reference Documentation

For detailed patterns, see:

- Queues vs Topics Patterns - Queue/topic patterns, sessions, receive modes, message settlement
- Error Handling and Reliability - ServiceBusError codes, DLQ handling, lock renewal, graceful shutdown

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.Messaging.ServiceBus (.NET)

Enterprise messaging SDK for reliable message delivery with queues, topics, subscriptions, and sessions.

## Installation

```bash
dotnet add package Azure.Messaging.ServiceBus
dotnet add package Azure.Identity
```

**Current Version**: v7.20.1 (stable)

## Environment Variables

```bash
AZURE_SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
# Or connection string (less secure)
AZURE_SERVICEBUS_CONNECTION_STRING=Endpoint=sb://...
```

## Authentication

### Microsoft Entra ID (Recommended)

```csharp
using Azure.Identity;
using Azure.Messaging.ServiceBus;

string fullyQualifiedNamespace = "<namespace>.servicebus.windows.net";
await using ServiceBusClient client = new(fullyQualifiedNamespace, new DefaultAzureCredential());
```

### Connection String

```csharp
string connectionString = "<connection_string>";
await using ServiceBusClient client = new(connectionString);
```

### ASP.NET Core Dependency Injection

```csharp
services.AddAzureClients(builder =>
{
    builder.AddServiceBusClientWithNamespace("<namespace>.servicebus.windows.net");
    builder.UseCredential(new DefaultAzureCredential());
});
```

## Client Hierarchy

```
ServiceBusClient
├── CreateSender(queueOrTopicName)      → ServiceBusSender
├── CreateReceiver(queueName)           → ServiceBusReceiver
├── CreateReceiver(topicName, subName)  → ServiceBusReceiver
├── AcceptNextSessionAsync(queueName)   → ServiceBusSessionReceiver
├── CreateProcessor(queueName)          → ServiceBusProcessor
└── CreateSessionProcessor(queueName)   → ServiceBusSessionProcessor

ServiceBusAdministrationClient (separate client for CRUD)
```

## Core Workflows

### 1. Send Messages

```csharp
await using ServiceBusClient client = new(fullyQualifiedNamespace, new DefaultAzureCredential());
ServiceBusSender sender = client.CreateSender("my-queue");

// Single message
ServiceBusMessage message = new("Hello world!");
await sender.SendMessageAsync(message);

// Safe batching (recommended)
using ServiceBusMessageBatch batch = await sender.CreateMessageBatchAsync();
if (batch.TryAddMessage(new ServiceBusMessage("Message 1")))
{
    // Message added successfully
}
if (batch.TryAddMessage(new ServiceBusMessage("Message 2")))
{
    // Message added successfully
}
await sender.SendMessagesAsync(batch);
```

### 2. Receive Messages

```csharp
ServiceBusReceiver receiver = client.CreateReceiver("my-queue");

// Single message
ServiceBusReceivedMessage message = await receiver.ReceiveMessageAsync();
string body = message.Body.ToString();
Console.WriteLine(body);

// Complete the message (removes from queue)
await receiver.CompleteMessageAsync(message);

// Batch receive
IReadOnlyList<ServiceBusReceivedMessage> messages = await receiver.ReceiveMessagesAsync(maxMessages: 10);
foreach (var msg in messages)
{
    Console.WriteLine(msg.Body.ToString());
    await receiver.CompleteMessageAsync(msg);
}
```

### 3. Message Settlement

```csharp
// Complete - removes message from queue
await receiver.CompleteMessageAsync(message);

// Abandon - releases lock, message can be received again
await receiver.AbandonMessageAsync(message);

// Defer - prevents normal receive, use ReceiveDeferredMessageAsync
await receiver.DeferMessageAsync(message);

// Dead Letter - moves to dead letter subqueue
await receiver.DeadLetterMessageAsync(message, "InvalidFormat", "Message body was not valid JSON");
```

### 4. Background Processing with Processor

```csharp
ServiceBusProcessor processor = client.CreateProcessor("my-queue", new ServiceBusProcessorOptions
{
    AutoCompleteMessages = false,
    MaxConcurrentCalls = 2
});

processor.ProcessMessageAsync += async (args) =>
{
    try
    {
        string body = args.Message.Body.ToString();
        Console.WriteLine($"Received: {body}");
        await args.CompleteMessageAsync(args.Message);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error processing: {ex.Message}");
        await args.AbandonMessageAsync(args.Message);
    }
};

processor.ProcessErrorAsync += (args) =>
{
    Console.WriteLine($"Error source: {args.ErrorSource}");
    Console.WriteLine($"Entity: {args.EntityPath}");
    Console.WriteLine($"Exception: {args.Exception}");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync();
// ... application runs
await processor.StopProcessingAsync();
```

### 5. Sessions (Ordered Processing)

```csharp
// Send session message
ServiceBusMessage message = new("Hello")
{
    SessionId = "order-123"
};
await sender.SendMessageAsync(message);

// Receive from next available session
ServiceBusSessionReceiver receiver = await client.AcceptNextSessionAsync("my-queue");

// Or receive from specific session
ServiceBusSessionReceiver receiver = await client.AcceptSessionAsync("my-queue", "order-123");

// Session state management
await receiver.SetSessionStateAsync(new BinaryData("processing"));
BinaryData state = await receiver.GetSessionStateAsync();

// Renew session lock
await receiver.RenewSessionLockAsync();
```

### 6. Dead Letter Queue

```csharp
// Receive from dead letter queue
ServiceBusReceiver dlqReceiver = client.CreateReceiver("my-queue", new ServiceBusReceiverOptions
{
    SubQueue = SubQueue.DeadLetter
});

ServiceBusReceivedMessage dlqMessage = await dlqReceiver.ReceiveMessageAsync();

// Access dead letter metadata
string reason = dlqMessage.DeadLetterReason;
string description = dlqMessage.DeadLetterErrorDescription;
Console.WriteLine($"Dead letter reason: {reason} - {description}");
```

### 7. Topics and Subscriptions

```csharp
// Send to topic
ServiceBusSender topicSender = client.CreateSender("my-topic");
await topicSender.SendMessageAsync(new ServiceBusMessage("Broadcast message"));

// Receive from subscription
ServiceBusReceiver subReceiver = client.CreateReceiver("my-topic", "my-subscription");
var message = await subReceiver.ReceiveMessageAsync();
```

### 8. Administration (CRUD)

```csharp
var adminClient = new ServiceBusAdministrationClient(
    fullyQualifiedNamespace, 
    new DefaultAzureCredential());

// Create queue
var options = new CreateQueueOptions("my-queue")
{
    MaxDeliveryCount = 10,
    LockDuration = TimeSpan.FromSeconds(30),
    RequiresSession = true,
    DeadLetteringOnMessageExpiration = true
};
QueueProperties queue = await adminClient.CreateQueueAsync(options);

// Update queue
queue.LockDuration = TimeSpan.FromSeconds(60);
await adminClient.UpdateQueueAsync(queue);

// Create topic and subscription
await adminClient.CreateTopicAsync(new CreateTopicOptions("my-topic"));
await adminClient.CreateSubscriptionAsync(new CreateSubscriptionOptions("my-topic", "my-subscription"));

// Delete
await adminClient.DeleteQueueAsync("my-queue");
```

### 9. Cross-Entity Transactions

```csharp
var options = new ServiceBusClientOptions { EnableCrossEntityTransactions = true };
await using var client = new ServiceBusClient(connectionString, options);

ServiceBusReceiver receiverA = client.CreateReceiver("queueA");
ServiceBusSender senderB = client.CreateSender("queueB");

ServiceBusReceivedMessage receivedMessage = await receiverA.ReceiveMessageAsync();

using (var ts = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
{
    await receiverA.CompleteMessageAsync(receivedMessage);
    await senderB.SendMessageAsync(new ServiceBusMessage("Forwarded"));
    ts.Complete();
}
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ServiceBusClient` | Main entry point, manages connection |
| `ServiceBusSender` | Sends messages to queues/topics |
| `ServiceBusReceiver` | Receives messages from queues/subscriptions |
| `ServiceBusSessionReceiver` | Receives session messages |
| `ServiceBusProcessor` | Background message processing |
| `ServiceBusSessionProcessor` | Background session processing |
| `ServiceBusAdministrationClient` | CRUD for queues/topics/subscriptions |
| `ServiceBusMessage` | Message to send |
| `ServiceBusReceivedMessage` | Received message with metadata |
| `ServiceBusMessageBatch` | Batch of messages |

## Best Practices

1. **Use singletons** — Clients, senders, receivers, and processors are thread-safe
2. **Always dispose** — Use `await using` or call `DisposeAsync()`
3. **Dispose order** — Close senders/receivers/processors first, then client
4. **Use DefaultAzureCredential** — Prefer over connection strings for production
5. **Use processors for background work** — Handles lock renewal automatically
6. **Use safe batching** — `CreateMessageBatchAsync()` and `TryAddMessage()`
7. **Handle transient errors** — Use `ServiceBusException.Reason`
8. **Configure transport** — Use `AmqpWebSockets` if ports 5671/5672 are blocked
9. **Set appropriate lock duration** — Default is 30 seconds
10. **Use sessions for ordering** — FIFO within a session

## Error Handling

```csharp
try
{
    await sender.SendMessageAsync(message);
}
catch (ServiceBusException ex) when (ex.Reason == ServiceBusFailureReason.ServiceBusy)
{
    // Retry with backoff
}
catch (ServiceBusException ex)
{
    Console.WriteLine($"Service Bus Error: {ex.Reason} - {ex.Message}");
}
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.Messaging.ServiceBus` | Service Bus (this SDK) | `dotnet add package Azure.Messaging.ServiceBus` |
| `Azure.Messaging.EventHubs` | Event streaming | `dotnet add package Azure.Messaging.EventHubs` |
| `Azure.Messaging.EventGrid` | Event routing | `dotnet add package Azure.Messaging.EventGrid` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.Messaging.ServiceBus |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.messaging.servicebus |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/servicebus/Azure.Messaging.ServiceBus |
| Troubleshooting | https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/TROUBLESHOOTING.md |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
