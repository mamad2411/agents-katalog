---
name: azure-eventgrid-toolkit
description: Consolidated toolkit for azure-eventgrid. Covers azure-eventgrid-py, azure-eventgrid-dotnet, azure-eventgrid-java
---
# Azure Eventgrid Toolkit

## Core Capabilities
# Azure Eventgrid Toolkit

# Azure Event Grid SDK for Python

Event routing service for building event-driven applications with pub/sub semantics.

## Installation

```bash
pip install azure-eventgrid azure-identity
```

## Environment Variables

```bash
EVENTGRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENTGRID_NAMESPACE_ENDPOINT=https://<namespace>.<region>.eventgrid.azure.net
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.eventgrid import EventGridPublisherClient

credential = DefaultAzureCredential()
endpoint = "https://<topic-name>.<region>.eventgrid.azure.net/api/events"

client = EventGridPublisherClient(endpoint, credential)
```

## Event Types

| Format | Class | Use Case |
|--------|-------|----------|
| Cloud Events 1.0 | `CloudEvent` | Standard, interoperable (recommended) |
| Event Grid Schema | `EventGridEvent` | Azure-native format |

## Publish CloudEvents

```python
from azure.eventgrid import EventGridPublisherClient, CloudEvent
from azure.identity import DefaultAzureCredential

client = EventGridPublisherClient(endpoint, DefaultAzureCredential())

# Single event
event = CloudEvent(
    type="MyApp.Events.OrderCreated",
    source="/myapp/orders",
    data={"order_id": "12345", "amount": 99.99}
)
client.send(event)

# Multiple events
events = [
    CloudEvent(
        type="MyApp.Events.OrderCreated",
        source="/myapp/orders",
        data={"order_id": f"order-{i}"}
    )
    for i in range(10)
]
client.send(events)
```

## Publish EventGridEvents

```python
from azure.eventgrid import EventGridEvent
from datetime import datetime, timezone

event = EventGridEvent(
    subject="/myapp/orders/12345",
    event_type="MyApp.Events.OrderCreated",
    data={"order_id": "12345", "amount": 99.99},
    data_version="1.0"
)

client.send(event)
```

## Event Properties

### CloudEvent Properties

```python
event = CloudEvent(
    type="MyApp.Events.ItemCreated",      # Required: event type
    source="/myapp/items",                 # Required: event source
    data={"key": "value"},                 # Event payload
    subject="items/123",                   # Optional: subject/path
    datacontenttype="application/json",   # Optional: content type
    dataschema="https://schema.example",  # Optional: schema URL
    time=datetime.now(timezone.utc),      # Optional: timestamp
    extensions={"custom": "value"}         # Optional: custom attributes
)
```

### EventGridEvent Properties

```python
event = EventGridEvent(
    subject="/myapp/items/123",            # Required: subject
    event_type="MyApp.ItemCreated",        # Required: event type
    data={"key": "value"},                 # Required: event payload
    data_version="1.0",                    # Required: schema version
    topic="/subscriptions/.../topics/...", # Optional: auto-set
    event_time=datetime.now(timezone.utc)  # Optional: timestamp
)
```

## Async Client

```python
from azure.eventgrid.aio import EventGridPublisherClient
from azure.identity.aio import DefaultAzureCredential

async def publish_events():
    credential = DefaultAzureCredential()
    
    async with EventGridPublisherClient(endpoint, credential) as client:
        event = CloudEvent(
            type="MyApp.Events.Test",
            source="/myapp",
            data={"message": "hello"}
        )
        await client.send(event)

import asyncio
asyncio.run(publish_events())
```

## Namespace Topics (Event Grid Namespaces)

For Event Grid Namespaces (pull delivery):

```python
from azure.eventgrid.aio import EventGridPublisherClient

# Namespace endpoint (different from custom topic)
namespace_endpoint = "https://<namespace>.<region>.eventgrid.azure.net"
topic_name = "my-topic"

async with EventGridPublisherClient(
    endpoint=namespace_endpoint,
    credential=DefaultAzureCredential()
) as client:
    await client.send(
        event,
        namespace_topic=topic_name
    )
```

## Best Practices

1. **Use CloudEvents** for new applications (industry standard)
2. **Batch events** when publishing multiple events
3. **Include meaningful subjects** for filtering
4. **Use async client** for high-throughput scenarios
5. **Handle retries** — Event Grid has built-in retry
6. **Set appropriate event types** for routing and filtering

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.Messaging.EventGrid (.NET)

Client library for publishing events to Azure Event Grid topics, domains, and namespaces.

## Installation

```bash
# For topics and domains (push delivery)
dotnet add package Azure.Messaging.EventGrid

# For namespaces (pull delivery)
dotnet add package Azure.Messaging.EventGrid.Namespaces

# For CloudNative CloudEvents interop
dotnet add package Microsoft.Azure.Messaging.EventGrid.CloudNativeCloudEvents
```

**Current Version**: 4.28.0 (stable)

## Environment Variables

```bash
# Topic/Domain endpoint
EVENT_GRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENT_GRID_TOPIC_KEY=<access-key>

# Namespace endpoint (for pull delivery)
EVENT_GRID_NAMESPACE_ENDPOINT=https://<namespace>.<region>.eventgrid.azure.net
EVENT_GRID_TOPIC_NAME=<topic-name>
EVENT_GRID_SUBSCRIPTION_NAME=<subscription-name>
```

## Client Hierarchy

```
Push Delivery (Topics/Domains)
└── EventGridPublisherClient
    ├── SendEventAsync(EventGridEvent)
    ├── SendEventsAsync(IEnumerable<EventGridEvent>)
    ├── SendEventAsync(CloudEvent)
    └── SendEventsAsync(IEnumerable<CloudEvent>)

Pull Delivery (Namespaces)
├── EventGridSenderClient
│   └── SendAsync(CloudEvent)
└── EventGridReceiverClient
    ├── ReceiveAsync()
    ├── AcknowledgeAsync()
    ├── ReleaseAsync()
    └── RejectAsync()
```

## Authentication

### API Key Authentication

```csharp
using Azure;
using Azure.Messaging.EventGrid;

EventGridPublisherClient client = new(
    new Uri("https://mytopic.eastus-1.eventgrid.azure.net/api/events"),
    new AzureKeyCredential("<access-key>"));
```

### Microsoft Entra ID (Recommended)

```csharp
using Azure.Identity;
using Azure.Messaging.EventGrid;

EventGridPublisherClient client = new(
    new Uri("https://mytopic.eastus-1.eventgrid.azure.net/api/events"),
    new DefaultAzureCredential());
```

### SAS Token Authentication

```csharp
string sasToken = EventGridPublisherClient.BuildSharedAccessSignature(
    new Uri(topicEndpoint),
    DateTimeOffset.UtcNow.AddHours(1),
    new AzureKeyCredential(topicKey));

var sasCredential = new AzureSasCredential(sasToken);
EventGridPublisherClient client = new(
    new Uri(topicEndpoint),
    sasCredential);
```

## Publishing Events

### EventGridEvent Schema

```csharp
EventGridPublisherClient client = new(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey));

// Single event
EventGridEvent egEvent = new(
    subject: "orders/12345",
    eventType: "Order.Created",
    dataVersion: "1.0",
    data: new { OrderId = "12345", Amount = 99.99 });

await client.SendEventAsync(egEvent);

// Batch of events
List<EventGridEvent> events = new()
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new OrderData { OrderId = "12345", Amount = 99.99 }),
    new EventGridEvent(
        subject: "orders/12346",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new OrderData { OrderId = "12346", Amount = 149.99 })
};

await client.SendEventsAsync(events);
```

### CloudEvent Schema

```csharp
CloudEvent cloudEvent = new(
    source: "/orders/system",
    type: "Order.Created",
    data: new { OrderId = "12345", Amount = 99.99 });

cloudEvent.Subject = "orders/12345";
cloudEvent.Id = Guid.NewGuid().ToString();
cloudEvent.Time = DateTimeOffset.UtcNow;

await client.SendEventAsync(cloudEvent);

// Batch of CloudEvents
List<CloudEvent> cloudEvents = new()
{
    new CloudEvent("/orders", "Order.Created", new { OrderId = "1" }),
    new CloudEvent("/orders", "Order.Updated", new { OrderId = "2" })
};

await client.SendEventsAsync(cloudEvents);
```

### Publishing to Event Grid Domain

```csharp
// Events must specify the Topic property for domain routing
List<EventGridEvent> events = new()
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new { OrderId = "12345" })
    {
        Topic = "orders-topic"  // Domain topic name
    },
    new EventGridEvent(
        subject: "inventory/item-1",
        eventType: "Inventory.Updated",
        dataVersion: "1.0",
        data: new { ItemId = "item-1" })
    {
        Topic = "inventory-topic"
    }
};

await client.SendEventsAsync(events);
```

### Custom Serialization

```csharp
using System.Text.Json;

var serializerOptions = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
};

var customSerializer = new JsonObjectSerializer(serializerOptions);

EventGridEvent egEvent = new(
    subject: "orders/12345",
    eventType: "Order.Created",
    dataVersion: "1.0",
    data: customSerializer.Serialize(new OrderData { OrderId = "12345" }));

await client.SendEventAsync(egEvent);
```

## Pull Delivery (Namespaces)

### Send Events to Namespace Topic

```csharp
using Azure;
using Azure.Messaging;
using Azure.Messaging.EventGrid.Namespaces;

var senderClient = new EventGridSenderClient(
    new Uri(namespaceEndpoint),
    topicName,
    new AzureKeyCredential(topicKey));

// Send single event
CloudEvent cloudEvent = new("employee_source", "Employee.Created", 
    new { Name = "John", Age = 30 });
await senderClient.SendAsync(cloudEvent);

// Send batch
await senderClient.SendAsync(new[]
{
    new CloudEvent("source", "type", new { Name = "Alice" }),
    new CloudEvent("source", "type", new { Name = "Bob" })
});
```

### Receive and Process Events

```csharp
var receiverClient = new EventGridReceiverClient(
    new Uri(namespaceEndpoint),
    topicName,
    subscriptionName,
    new AzureKeyCredential(topicKey));

// Receive events
ReceiveResult result = await receiverClient.ReceiveAsync(maxEvents: 10);

List<string> lockTokensToAck = new();
List<string> lockTokensToRelease = new();

foreach (ReceiveDetails detail in result.Details)
{
    CloudEvent cloudEvent = detail.Event;
    string lockToken = detail.BrokerProperties.LockToken;
    
    try
    {
        // Process the event
        Console.WriteLine($"Event: {cloudEvent.Type}, Data: {cloudEvent.Data}");
        lockTokensToAck.Add(lockToken);
    }
    catch (Exception)
    {
        // Release for retry
        lockTokensToRelease.Add(lockToken);
    }
}

// Acknowledge successfully processed events
if (lockTokensToAck.Any())
{
    await receiverClient.AcknowledgeAsync(lockTokensToAck);
}

// Release events for retry
if (lockTokensToRelease.Any())
{
    await receiverClient.ReleaseAsync(lockTokensToRelease);
}
```

### Reject Events (Dead Letter)

```csharp
// Reject events that cannot be processed
await receiverClient.RejectAsync(new[] { lockToken });
```

## Consuming Events (Azure Functions)

### EventGridEvent Trigger

```csharp
using Azure.Messaging.EventGrid;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;

public static class EventGridFunction
{
    [FunctionName("ProcessEventGridEvent")]
    public static void Run(
        [EventGridTrigger] EventGridEvent eventGridEvent,
        ILogger log)
    {
        log.LogInformation($"Event Type: {eventGridEvent.EventType}");
        log.LogInformation($"Subject: {eventGridEvent.Subject}");
        log.LogInformation($"Data: {eventGridEvent.Data}");
    }
}
```

### CloudEvent Trigger

```csharp
using Azure.Messaging;
using Microsoft.Azure.Functions.Worker;

public class CloudEventFunction
{
    [Function("ProcessCloudEvent")]
    public void Run(
        [EventGridTrigger] CloudEvent cloudEvent,
        FunctionContext context)
    {
        var logger = context.GetLogger("ProcessCloudEvent");
        logger.LogInformation($"Event Type: {cloudEvent.Type}");
        logger.LogInformation($"Source: {cloudEvent.Source}");
        logger.LogInformation($"Data: {cloudEvent.Data}");
    }
}
```

## Parsing Events

### Parse EventGridEvent

```csharp
// From JSON string
string json = "..."; // Event Grid webhook payload
EventGridEvent[] events = EventGridEvent.ParseMany(BinaryData.FromString(json));

foreach (EventGridEvent egEvent in events)
{
    if (egEvent.TryGetSystemEventData(out object systemEvent))
    {
        // Handle system event
        switch (systemEvent)
        {
            case StorageBlobCreatedEventData blobCreated:
                Console.WriteLine($"Blob created: {blobCreated.Url}");
                break;
        }
    }
    else
    {
        // Handle custom event
        var customData = egEvent.Data.ToObjectFromJson<MyCustomData>();
    }
}
```

### Parse CloudEvent

```csharp
CloudEvent[] cloudEvents = CloudEvent.ParseMany(BinaryData.FromString(json));

foreach (CloudEvent cloudEvent in cloudEvents)
{
    var data = cloudEvent.Data.ToObjectFromJson<MyEventData>();
    Console.WriteLine($"Type: {cloudEvent.Type}, Data: {data}");
}
```

## System Events

```csharp
// Common system event types
using Azure.Messaging.EventGrid.SystemEvents;

// Storage events
StorageBlobCreatedEventData blobCreated;
StorageBlobDeletedEventData blobDeleted;

// Resource events
ResourceWriteSuccessEventData resourceCreated;
ResourceDeleteSuccessEventData resourceDeleted;

// App Service events
WebAppUpdatedEventData webAppUpdated;

// Container Registry events
ContainerRegistryImagePushedEventData imagePushed;

// IoT Hub events
IotHubDeviceCreatedEventData deviceCreated;
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `EventGridPublisherClient` | Publish to topics/domains |
| `EventGridSenderClient` | Send to namespace topics |
| `EventGridReceiverClient` | Receive from namespace subscriptions |
| `EventGridEvent` | Event Grid native schema |
| `CloudEvent` | CloudEvents 1.0 schema |
| `ReceiveResult` | Pull delivery response |
| `ReceiveDetails` | Event with broker properties |
| `BrokerProperties` | Lock token, delivery count |

## Event Schemas Comparison

| Feature | EventGridEvent | CloudEvent |
|---------|----------------|------------|
| Standard | Azure-specific | CNCF standard |
| Required fields | subject, eventType, dataVersion, data | source, type |
| Extensibility | Limited | Extension attributes |
| Interoperability | Azure only | Cross-platform |

## Best Practices

1. **Use CloudEvents** — Prefer CloudEvents for new implementations (industry standard)
2. **Batch events** — Send multiple events in one call for efficiency
3. **Use Entra ID** — Prefer managed identity over access keys
4. **Idempotent handlers** — Events may be delivered more than once
5. **Set event TTL** — Configure time-to-live for namespace events
6. **Handle partial failures** — Acknowledge/release events individually
7. **Use dead-letter** — Configure dead-letter for failed events
8. **Validate schemas** — Validate event data before processing

## Error Handling

```csharp
using Azure;

try
{
    await client.SendEventAsync(cloudEvent);
}
catch (RequestFailedException ex) when (ex.Status == 401)
{
    Console.WriteLine("Authentication failed - check credentials");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Authorization failed - check RBAC permissions");
}
catch (RequestFailedException ex) when (ex.Status == 413)
{
    Console.WriteLine("Payload too large - max 1MB per event, 1MB total batch");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Event Grid error: {ex.Status} - {ex.Message}");
}
```

## Failover Pattern

```csharp
try
{
    var primaryClient = new EventGridPublisherClient(primaryUri, primaryKey);
    await primaryClient.SendEventsAsync(events);
}
catch (RequestFailedException)
{
    // Failover to secondary region
    var secondaryClient = new EventGridPublisherClient(secondaryUri, secondaryKey);
    await secondaryClient.SendEventsAsync(events);
}
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.Messaging.EventGrid` | Topics/Domains (this SDK) | `dotnet add package Azure.Messaging.EventGrid` |
| `Azure.Messaging.EventGrid.Namespaces` | Pull delivery | `dotnet add package Azure.Messaging.EventGrid.Namespaces` |
| `Azure.Identity` | Authentication | `dotnet add package Azure.Identity` |
| `Microsoft.Azure.WebJobs.Extensions.EventGrid` | Azure Functions trigger | `dotnet add package Microsoft.Azure.WebJobs.Extensions.EventGrid` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.Messaging.EventGrid |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.messaging.eventgrid |
| Quickstart | https://learn.microsoft.com/azure/event-grid/custom-event-quickstart |
| Pull Delivery | https://learn.microsoft.com/azure/event-grid/pull-delivery-overview |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/eventgrid/Azure.Messaging.EventGrid |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Event Grid SDK for Java

Build event-driven applications using the Azure Event Grid SDK for Java.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-eventgrid</artifactId>
    <version>4.27.0</version>
</dependency>
```

## Client Creation

### EventGridPublisherClient

```java
import com.azure.messaging.eventgrid.EventGridPublisherClient;
import com.azure.messaging.eventgrid.EventGridPublisherClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

// With API Key
EventGridPublisherClient<EventGridEvent> client = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildEventGridEventPublisherClient();

// For CloudEvents
EventGridPublisherClient<CloudEvent> cloudClient = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildCloudEventPublisherClient();
```

### With DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

EventGridPublisherClient<EventGridEvent> client = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildEventGridEventPublisherClient();
```

### Async Client

```java
import com.azure.messaging.eventgrid.EventGridPublisherAsyncClient;

EventGridPublisherAsyncClient<EventGridEvent> asyncClient = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildEventGridEventPublisherAsyncClient();
```

## Event Types

| Type | Description |
|------|-------------|
| `EventGridEvent` | Azure Event Grid native schema |
| `CloudEvent` | CNCF CloudEvents 1.0 specification |
| `BinaryData` | Custom schema events |

## Core Patterns

### Publish EventGridEvent

```java
import com.azure.messaging.eventgrid.EventGridEvent;
import com.azure.core.util.BinaryData;

EventGridEvent event = new EventGridEvent(
    "resource/path",           // subject
    "MyApp.Events.OrderCreated", // eventType
    BinaryData.fromObject(new OrderData("order-123", 99.99)), // data
    "1.0"                      // dataVersion
);

client.sendEvent(event);
```

### Publish Multiple Events

```java
List<EventGridEvent> events = Arrays.asList(
    new EventGridEvent("orders/1", "Order.Created", 
        BinaryData.fromObject(order1), "1.0"),
    new EventGridEvent("orders/2", "Order.Created", 
        BinaryData.fromObject(order2), "1.0")
);

client.sendEvents(events);
```

### Publish CloudEvent

```java
import com.azure.core.models.CloudEvent;
import com.azure.core.models.CloudEventDataFormat;

CloudEvent cloudEvent = new CloudEvent(
    "/myapp/orders",           // source
    "order.created",           // type
    BinaryData.fromObject(orderData), // data
    CloudEventDataFormat.JSON  // dataFormat
);
cloudEvent.setSubject("orders/12345");
cloudEvent.setId(UUID.randomUUID().toString());

cloudClient.sendEvent(cloudEvent);
```

### Publish CloudEvents Batch

```java
List<CloudEvent> cloudEvents = Arrays.asList(
    new CloudEvent("/app", "event.type1", BinaryData.fromString("data1"), CloudEventDataFormat.JSON),
    new CloudEvent("/app", "event.type2", BinaryData.fromString("data2"), CloudEventDataFormat.JSON)
);

cloudClient.sendEvents(cloudEvents);
```

### Async Publishing

```java
asyncClient.sendEvent(event)
    .subscribe(
        unused -> System.out.println("Event sent successfully"),
        error -> System.err.println("Error: " + error.getMessage())
    );

// With multiple events
asyncClient.sendEvents(events)
    .doOnSuccess(unused -> System.out.println("All events sent"))
    .doOnError(error -> System.err.println("Failed: " + error))
    .block(); // Block if needed
```

### Custom Event Data Class

```java
public class OrderData {
    private String orderId;
    private double amount;
    private String customerId;
    
    public OrderData(String orderId, double amount) {
        this.orderId = orderId;
        this.amount = amount;
    }
    
    // Getters and setters
}

// Usage
OrderData order = new OrderData("ORD-123", 150.00);
EventGridEvent event = new EventGridEvent(
    "orders/" + order.getOrderId(),
    "MyApp.Order.Created",
    BinaryData.fromObject(order),
    "1.0"
);
```

## Receiving Events

### Parse EventGridEvent

```java
import com.azure.messaging.eventgrid.EventGridEvent;

// From JSON string (e.g., webhook payload)
String jsonPayload = "[{\"id\": \"...\", ...}]";
List<EventGridEvent> events = EventGridEvent.fromString(jsonPayload);

for (EventGridEvent event : events) {
    System.out.println("Event Type: " + event.getEventType());
    System.out.println("Subject: " + event.getSubject());
    System.out.println("Event Time: " + event.getEventTime());
    
    // Get data
    BinaryData data = event.getData();
    OrderData orderData = data.toObject(OrderData.class);
}
```

### Parse CloudEvent

```java
import com.azure.core.models.CloudEvent;

String cloudEventJson = "[{\"specversion\": \"1.0\", ...}]";
List<CloudEvent> cloudEvents = CloudEvent.fromString(cloudEventJson);

for (CloudEvent event : cloudEvents) {
    System.out.println("Type: " + event.getType());
    System.out.println("Source: " + event.getSource());
    System.out.println("ID: " + event.getId());
    
    MyEventData data = event.getData().toObject(MyEventData.class);
}
```

### Handle System Events

```java
import com.azure.messaging.eventgrid.systemevents.*;

for (EventGridEvent event : events) {
    if (event.getEventType().equals("Microsoft.Storage.BlobCreated")) {
        StorageBlobCreatedEventData blobData = 
            event.getData().toObject(StorageBlobCreatedEventData.class);
        System.out.println("Blob URL: " + blobData.getUrl());
    }
}
```

## Event Grid Namespaces (MQTT/Pull)

### Receive from Namespace Topic

```java
import com.azure.messaging.eventgrid.namespaces.EventGridReceiverClient;
import com.azure.messaging.eventgrid.namespaces.EventGridReceiverClientBuilder;
import com.azure.messaging.eventgrid.namespaces.models.*;

EventGridReceiverClient receiverClient = new EventGridReceiverClientBuilder()
    .endpoint("<namespace-endpoint>")
    .credential(new AzureKeyCredential("<key>"))
    .topicName("my-topic")
    .subscriptionName("my-subscription")
    .buildClient();

// Receive events
ReceiveResult result = receiverClient.receive(10, Duration.ofSeconds(30));

for (ReceiveDetails detail : result.getValue()) {
    CloudEvent event = detail.getEvent();
    System.out.println("Event: " + event.getType());
    
    // Acknowledge the event
    receiverClient.acknowledge(Arrays.asList(detail.getBrokerProperties().getLockToken()));
}
```

### Reject or Release Events

```java
// Reject (don't retry)
receiverClient.reject(Arrays.asList(lockToken));

// Release (retry later)
receiverClient.release(Arrays.asList(lockToken));

// Release with delay
receiverClient.release(Arrays.asList(lockToken), 
    new ReleaseOptions().setDelay(ReleaseDelay.BY_60_SECONDS));
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.sendEvent(event);
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
}
```

## Environment Variables

```bash
EVENT_GRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENT_GRID_ACCESS_KEY=<your-access-key>
```

## Best Practices

1. **Batch Events**: Send multiple events in one call when possible
2. **Idempotency**: Include unique event IDs for deduplication
3. **Schema Validation**: Use strongly-typed event data classes
4. **Retry Logic**: Built-in, but consider dead-letter for failures
5. **Event Size**: Keep events under 1MB (64KB for basic tier)

## Trigger Phrases

- "Event Grid Java"
- "publish events Azure"
- "CloudEvent SDK"
- "event-driven messaging"
- "pub/sub Azure"
- "webhook events"

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
