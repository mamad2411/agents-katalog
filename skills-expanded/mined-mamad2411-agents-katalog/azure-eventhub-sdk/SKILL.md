---
name: azure-eventhub-sdk
description: Consolidated Azure Event Hubs SDK skill for high-throughput event ingestion and processing across Dotnet, Java, Python, Rust, and TypeScript.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Azure Event Hubs SDK (Multi-Language)

This skill consolidates Azure Event Hubs streaming capabilities across all supported languages.

## Core Concepts

Event Hubs is a big data streaming platform and event ingestion service.
- **Producers**: Send events to an event hub. Events are typically sent in batches to improve throughput.
- **Consumers**: Read events from an event hub. Consumers use a consumer group to read the stream.
- **Partitions**: Event Hubs divides the stream into partitions for scalability.
- **Checkpointing**: Consumers must keep track of their progress (checkpoints) in Blob Storage to resume reading if they crash.

## Cross-Language Best Practices

1. **Authentication**: Use `DefaultAzureCredential`.
2. **Batching**: Always use `EventDataBatch` (or language equivalent) to send events to maximize throughput and avoid message size limits.
3. **Event Processor**: For consuming, use the robust `EventProcessorClient` (or equivalent) rather than low-level receivers. The processor handles partition load balancing, checkpointing, and error recovery automatically.
4. **Checkpoint Store**: Use Azure Blob Storage for checkpointing state across consumer instances.

## Language-Specific Package References

### Python
- **Install**: `pip install azure-eventhub azure-eventhub-checkpointstoreblob-aio azure-identity`
- **Key Classes**: `EventHubProducerClient`, `EventHubConsumerClient`, `BlobCheckpointStore`

### TypeScript / Node.js
- **Install**: `npm install @azure/event-hubs @azure/eventhubs-checkpointstore-blob @azure/identity`
- **Key Classes**: `EventHubProducerClient`, `EventHubConsumerClient`, `ContainerClient` (for checkpointing)

### Java
- **Install**: `com.azure:azure-messaging-eventhubs`, `com.azure:azure-messaging-eventhubs-checkpointstore-blob`
- **Key Classes**: `EventHubProducerClient`, `EventProcessorClientBuilder`

### .NET (C#)
- **Install**: `Azure.Messaging.EventHubs`, `Azure.Messaging.EventHubs.Processor`
- **Key Classes**: `EventHubProducerClient`, `EventProcessorClient`

### Rust
- **Install**: `azure_messaging_eventhubs`
- **Key Classes**: `ProducerClient`, `ConsumerClient`
