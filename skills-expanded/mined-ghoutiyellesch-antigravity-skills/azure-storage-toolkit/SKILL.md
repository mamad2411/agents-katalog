---
name: azure-storage-toolkit
description: Consolidated toolkit for azure-storage. Covers azure-storage-file-share-ts, azure-storage-queue-py, azure-storage-file-datalake-py, azure-storage-queue-ts, azure-storage-blob-sdk, azure-storage-file-share-py
---
# Azure Storage Toolkit

## Core Capabilities
# Azure Storage Toolkit

# @azure/storage-file-share (TypeScript/JavaScript)

SDK for Azure File Share operations — SMB file shares, directories, and file operations.

## Installation

```bash
npm install @azure/storage-file-share @azure/identity
```

**Current Version**: 12.x  
**Node.js**: >= 18.0.0

## Environment Variables

```bash
AZURE_STORAGE_ACCOUNT_NAME=<account-name>
AZURE_STORAGE_ACCOUNT_KEY=<account-key>
# OR connection string
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
```

## Authentication

### Connection String (Simplest)

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";

const client = ShareServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING!
);
```

### StorageSharedKeyCredential (Node.js only)

```typescript
import { ShareServiceClient, StorageSharedKeyCredential } from "@azure/storage-file-share";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const accountKey = process.env.AZURE_STORAGE_ACCOUNT_KEY!;

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net`,
  sharedKeyCredential
);
```

### DefaultAzureCredential

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";
import { DefaultAzureCredential } from "@azure/identity";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net`,
  new DefaultAzureCredential()
);
```

### SAS Token

```typescript
import { ShareServiceClient } from "@azure/storage-file-share";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const sasToken = process.env.AZURE_STORAGE_SAS_TOKEN!;

const client = new ShareServiceClient(
  `https://${accountName}.file.core.windows.net${sasToken}`
);
```

## Client Hierarchy

```
ShareServiceClient (account level)
└── ShareClient (share level)
    └── ShareDirectoryClient (directory level)
        └── ShareFileClient (file level)
```

## Share Operations

### Create Share

```typescript
const shareClient = client.getShareClient("my-share");
await shareClient.create();

// Create with quota (in GB)
await shareClient.create({ quota: 100 });
```

### List Shares

```typescript
for await (const share of client.listShares()) {
  console.log(share.name, share.properties.quota);
}

// With prefix filter
for await (const share of client.listShares({ prefix: "logs-" })) {
  console.log(share.name);
}
```

### Delete Share

```typescript
await shareClient.delete();

// Delete if exists
await shareClient.deleteIfExists();
```

### Get Share Properties

```typescript
const properties = await shareClient.getProperties();
console.log("Quota:", properties.quota, "GB");
console.log("Last Modified:", properties.lastModified);
```

### Set Share Quota

```typescript
await shareClient.setQuota(200); // 200 GB
```

## Directory Operations

### Create Directory

```typescript
const directoryClient = shareClient.getDirectoryClient("my-directory");
await directoryClient.create();

// Create nested directory
const nestedDir = shareClient.getDirectoryClient("parent/child/grandchild");
await nestedDir.create();
```

### List Directories and Files

```typescript
const directoryClient = shareClient.getDirectoryClient("my-directory");

for await (const item of directoryClient.listFilesAndDirectories()) {
  if (item.kind === "directory") {
    console.log(`[DIR] ${item.name}`);
  } else {
    console.log(`[FILE] ${item.name} (${item.properties.contentLength} bytes)`);
  }
}
```

### Delete Directory

```typescript
await directoryClient.delete();

// Delete if exists
await directoryClient.deleteIfExists();
```

### Check if Directory Exists

```typescript
const exists = await directoryClient.exists();
if (!exists) {
  await directoryClient.create();
}
```

## File Operations

### Upload File (Simple)

```typescript
const fileClient = shareClient
  .getDirectoryClient("my-directory")
  .getFileClient("my-file.txt");

// Upload string
const content = "Hello, World!";
await fileClient.create(content.length);
await fileClient.uploadRange(content, 0, content.length);
```

### Upload File (Node.js - from local file)

```typescript
import * as fs from "fs";
import * as path from "path";

const fileClient = shareClient.rootDirectoryClient.getFileClient("uploaded.txt");
const localFilePath = "/path/to/local/file.txt";
const fileSize = fs.statSync(localFilePath).size;

await fileClient.create(fileSize);
await fileClient.uploadFile(localFilePath);
```

### Upload File (Buffer)

```typescript
const buffer = Buffer.from("Hello, Azure Files!");
const fileClient = shareClient.rootDirectoryClient.getFileClient("buffer-file.txt");

await fileClient.create(buffer.length);
await fileClient.uploadRange(buffer, 0, buffer.length);
```

### Upload File (Stream)

```typescript
import * as fs from "fs";

const fileClient = shareClient.rootDirectoryClient.getFileClient("streamed.txt");
const readStream = fs.createReadStream("/path/to/local/file.txt");
const fileSize = fs.statSync("/path/to/local/file.txt").size;

await fileClient.create(fileSize);
await fileClient.uploadStream(readStream, fileSize, 4 * 1024 * 1024, 4); // 4MB buffer, 4 concurrency
```

### Download File

```typescript
const fileClient = shareClient
  .getDirectoryClient("my-directory")
  .getFileClient("my-file.txt");

const downloadResponse = await fileClient.download();

// Read as string
const chunks: Buffer[] = [];
for await (const chunk of downloadResponse.readableStreamBody!) {
  chunks.push(Buffer.from(chunk));
}
const content = Buffer.concat(chunks).toString("utf-8");
```

### Download to File (Node.js)

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
await fileClient.downloadToFile("/path/to/local/destination.txt");
```

### Download to Buffer (Node.js)

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
const buffer = await fileClient.downloadToBuffer();
console.log(buffer.toString());
```

### Delete File

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
await fileClient.delete();

// Delete if exists
await fileClient.deleteIfExists();
```

### Copy File

```typescript
const sourceUrl = "https://account.file.core.windows.net/share/source.txt";
const destFileClient = shareClient.rootDirectoryClient.getFileClient("destination.txt");

// Start copy operation
const copyPoller = await destFileClient.startCopyFromURL(sourceUrl);
await copyPoller.pollUntilDone();
```

## File Properties & Metadata

### Get File Properties

```typescript
const fileClient = shareClient.rootDirectoryClient.getFileClient("my-file.txt");
const properties = await fileClient.getProperties();

console.log("Content-Length:", properties.contentLength);
console.log("Content-Type:", properties.contentType);
console.log("Last Modified:", properties.lastModified);
console.log("ETag:", properties.etag);
```

### Set Metadata

```typescript
await fileClient.setMetadata({
  author: "John Doe",
  category: "documents",
});
```

### Set HTTP Headers

```typescript
await fileClient.setHttpHeaders({
  fileContentType: "text/plain",
  fileCacheControl: "max-age=3600",
  fileContentDisposition: "attachment; filename=download.txt",
});
```

## Range Operations

### Upload Range

```typescript
const data = Buffer.from("partial content");
await fileClient.uploadRange(data, 100, data.length); // Write at offset 100
```

### Download Range

```typescript
const downloadResponse = await fileClient.download(100, 50); // offset 100, length 50
```

### Clear Range

```typescript
await fileClient.clearRange(0, 100); // Clear first 100 bytes
```

## Snapshot Operations

### Create Snapshot

```typescript
const snapshotResponse = await shareClient.createSnapshot();
console.log("Snapshot:", snapshotResponse.snapshot);
```

### Access Snapshot

```typescript
const snapshotShareClient = shareClient.withSnapshot(snapshotResponse.snapshot!);
const snapshotFileClient = snapshotShareClient.rootDirectoryClient.getFileClient("file.txt");
const content = await snapshotFileClient.downloadToBuffer();
```

### Delete Snapshot

```typescript
await shareClient.delete({ deleteSnapshots: "include" });
```

## SAS Token Generation (Node.js only)

### Generate File SAS

```typescript
import {
  generateFileSASQueryParameters,
  FileSASPermissions,
  StorageSharedKeyCredential,
} from "@azure/storage-file-share";

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);

const sasToken = generateFileSASQueryParameters(
  {
    shareName: "my-share",
    filePath: "my-directory/my-file.txt",
    permissions: FileSASPermissions.parse("r"), // read only
    expiresOn: new Date(Date.now() + 3600 * 1000), // 1 hour
  },
  sharedKeyCredential
).toString();

const sasUrl = `https://${accountName}.file.core.windows.net/my-share/my-directory/my-file.txt?${sasToken}`;
```

### Generate Share SAS

```typescript
import { ShareSASPermissions, generateFileSASQueryParameters } from "@azure/storage-file-share";

const sasToken = generateFileSASQueryParameters(
  {
    shareName: "my-share",
    permissions: ShareSASPermissions.parse("rcwdl"), // read, create, write, delete, list
    expiresOn: new Date(Date.now() + 24 * 3600 * 1000), // 24 hours
  },
  sharedKeyCredential
).toString();
```

## Error Handling

```typescript
import { RestError } from "@azure/storage-file-share";

try {
  await shareClient.create();
} catch (error) {
  if (error instanceof RestError) {
    switch (error.statusCode) {
      case 404:
        console.log("Share not found");
        break;
      case 409:
        console.log("Share already exists");
        break;
      case 403:
        console.log("Access denied");
        break;
      default:
        console.error(`Storage error ${error.statusCode}: ${error.message}`);
    }
  }
  throw error;
}
```

## TypeScript Types Reference

```typescript
import {
  // Clients
  ShareServiceClient,
  ShareClient,
  ShareDirectoryClient,
  ShareFileClient,

  // Authentication
  StorageSharedKeyCredential,
  AnonymousCredential,

  // SAS
  FileSASPermissions,
  ShareSASPermissions,
  AccountSASPermissions,
  AccountSASServices,
  AccountSASResourceTypes,
  generateFileSASQueryParameters,
  generateAccountSASQueryParameters,

  // Options & Responses
  ShareCreateResponse,
  FileDownloadResponseModel,
  DirectoryItem,
  FileItem,
  ShareProperties,
  FileProperties,

  // Errors
  RestError,
} from "@azure/storage-file-share";
```

## Best Practices

1. **Use connection strings for simplicity** — Easiest setup for development
2. **Use DefaultAzureCredential for production** — Enable managed identity in Azure
3. **Set quotas on shares** — Prevent unexpected storage costs
4. **Use streaming for large files** — `uploadStream`/`downloadToFile` for files > 256MB
5. **Use ranges for partial updates** — More efficient than full file replacement
6. **Create snapshots before major changes** — Point-in-time recovery
7. **Handle errors gracefully** — Check `RestError.statusCode` for specific handling
8. **Use `*IfExists` methods** — For idempotent operations

## Platform Differences

| Feature | Node.js | Browser |
|---------|---------|---------|
| `StorageSharedKeyCredential` | ✅ | ❌ |
| `uploadFile()` | ✅ | ❌ |
| `uploadStream()` | ✅ | ❌ |
| `downloadToFile()` | ✅ | ❌ |
| `downloadToBuffer()` | ✅ | ❌ |
| SAS generation | ✅ | ❌ |
| DefaultAzureCredential | ✅ | ❌ |
| Anonymous/SAS access | ✅ | ✅ |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Queue Storage SDK for Python

Simple, cost-effective message queuing for asynchronous communication.

## Installation

```bash
pip install azure-storage-queue azure-identity
```

## Environment Variables

```bash
AZURE_STORAGE_ACCOUNT_URL=https://<account>.queue.core.windows.net
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient

credential = DefaultAzureCredential()
account_url = "https://<account>.queue.core.windows.net"

# Service client
service_client = QueueServiceClient(account_url=account_url, credential=credential)

# Queue client
queue_client = QueueClient(account_url=account_url, queue_name="myqueue", credential=credential)
```

## Queue Operations

```python
# Create queue
service_client.create_queue("myqueue")

# Get queue client
queue_client = service_client.get_queue_client("myqueue")

# Delete queue
service_client.delete_queue("myqueue")

# List queues
for queue in service_client.list_queues():
    print(queue.name)
```

## Send Messages

```python
# Send message (string)
queue_client.send_message("Hello, Queue!")

# Send with options
queue_client.send_message(
    content="Delayed message",
    visibility_timeout=60,  # Hidden for 60 seconds
    time_to_live=3600       # Expires in 1 hour
)

# Send JSON
import json
data = {"task": "process", "id": 123}
queue_client.send_message(json.dumps(data))
```

## Receive Messages

```python
# Receive messages (makes them invisible temporarily)
messages = queue_client.receive_messages(
    messages_per_page=10,
    visibility_timeout=30  # 30 seconds to process
)

for message in messages:
    print(f"ID: {message.id}")
    print(f"Content: {message.content}")
    print(f"Dequeue count: {message.dequeue_count}")
    
    # Process message...
    
    # Delete after processing
    queue_client.delete_message(message)
```

## Peek Messages

```python
# Peek without hiding (doesn't affect visibility)
messages = queue_client.peek_messages(max_messages=5)

for message in messages:
    print(message.content)
```

## Update Message

```python
# Extend visibility or update content
messages = queue_client.receive_messages()
for message in messages:
    # Extend timeout (need more time)
    queue_client.update_message(
        message,
        visibility_timeout=60
    )
    
    # Update content and timeout
    queue_client.update_message(
        message,
        content="Updated content",
        visibility_timeout=60
    )
```

## Delete Message

```python
# Delete after successful processing
messages = queue_client.receive_messages()
for message in messages:
    try:
        # Process...
        queue_client.delete_message(message)
    except Exception:
        # Message becomes visible again after timeout
        pass
```

## Clear Queue

```python
# Delete all messages
queue_client.clear_messages()
```

## Queue Properties

```python
# Get queue properties
properties = queue_client.get_queue_properties()
print(f"Approximate message count: {properties.approximate_message_count}")

# Set/get metadata
queue_client.set_queue_metadata(metadata={"environment": "production"})
properties = queue_client.get_queue_properties()
print(properties.metadata)
```

## Async Client

```python
from azure.storage.queue.aio import QueueServiceClient, QueueClient
from azure.identity.aio import DefaultAzureCredential

async def queue_operations():
    credential = DefaultAzureCredential()
    
    async with QueueClient(
        account_url="https://<account>.queue.core.windows.net",
        queue_name="myqueue",
        credential=credential
    ) as client:
        # Send
        await client.send_message("Async message")
        
        # Receive
        async for message in client.receive_messages():
            print(message.content)
            await client.delete_message(message)

import asyncio
asyncio.run(queue_operations())
```

## Base64 Encoding

```python
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

# For binary data
queue_client = QueueClient(
    account_url=account_url,
    queue_name="myqueue",
    credential=credential,
    message_encode_policy=BinaryBase64EncodePolicy(),
    message_decode_policy=BinaryBase64DecodePolicy()
)

# Send bytes
queue_client.send_message(b"Binary content")
```

## Best Practices

1. **Delete messages after processing** to prevent reprocessing
2. **Set appropriate visibility timeout** based on processing time
3. **Handle `dequeue_count`** for poison message detection
4. **Use async client** for high-throughput scenarios
5. **Use `peek_messages`** for monitoring without affecting queue
6. **Set `time_to_live`** to prevent stale messages
7. **Consider Service Bus** for advanced features (sessions, topics)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Data Lake Storage Gen2 SDK for Python

Hierarchical file system for big data analytics workloads.

## Installation

```bash
pip install azure-storage-file-datalake azure-identity
```

## Environment Variables

```bash
AZURE_STORAGE_ACCOUNT_URL=https://<account>.dfs.core.windows.net
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

credential = DefaultAzureCredential()
account_url = "https://<account>.dfs.core.windows.net"

service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
```

## Client Hierarchy

| Client | Purpose |
|--------|---------|
| `DataLakeServiceClient` | Account-level operations |
| `FileSystemClient` | Container (file system) operations |
| `DataLakeDirectoryClient` | Directory operations |
| `DataLakeFileClient` | File operations |

## File System Operations

```python
# Create file system (container)
file_system_client = service_client.create_file_system("myfilesystem")

# Get existing
file_system_client = service_client.get_file_system_client("myfilesystem")

# Delete
service_client.delete_file_system("myfilesystem")

# List file systems
for fs in service_client.list_file_systems():
    print(fs.name)
```

## Directory Operations

```python
file_system_client = service_client.get_file_system_client("myfilesystem")

# Create directory
directory_client = file_system_client.create_directory("mydir")

# Create nested directories
directory_client = file_system_client.create_directory("path/to/nested/dir")

# Get directory client
directory_client = file_system_client.get_directory_client("mydir")

# Delete directory
directory_client.delete_directory()

# Rename/move directory
directory_client.rename_directory(new_name="myfilesystem/newname")
```

## File Operations

### Upload File

```python
# Get file client
file_client = file_system_client.get_file_client("path/to/file.txt")

# Upload from local file
with open("local-file.txt", "rb") as data:
    file_client.upload_data(data, overwrite=True)

# Upload bytes
file_client.upload_data(b"Hello, Data Lake!", overwrite=True)

# Append data (for large files)
file_client.append_data(data=b"chunk1", offset=0, length=6)
file_client.append_data(data=b"chunk2", offset=6, length=6)
file_client.flush_data(12)  # Commit the data
```

### Download File

```python
file_client = file_system_client.get_file_client("path/to/file.txt")

# Download all content
download = file_client.download_file()
content = download.readall()

# Download to file
with open("downloaded.txt", "wb") as f:
    download = file_client.download_file()
    download.readinto(f)

# Download range
download = file_client.download_file(offset=0, length=100)
```

### Delete File

```python
file_client.delete_file()
```

## List Contents

```python
# List paths (files and directories)
for path in file_system_client.get_paths():
    print(f"{'DIR' if path.is_directory else 'FILE'}: {path.name}")

# List paths in directory
for path in file_system_client.get_paths(path="mydir"):
    print(path.name)

# Recursive listing
for path in file_system_client.get_paths(path="mydir", recursive=True):
    print(path.name)
```

## File/Directory Properties

```python
# Get properties
properties = file_client.get_file_properties()
print(f"Size: {properties.size}")
print(f"Last modified: {properties.last_modified}")

# Set metadata
file_client.set_metadata(metadata={"processed": "true"})
```

## Access Control (ACL)

```python
# Get ACL
acl = directory_client.get_access_control()
print(f"Owner: {acl['owner']}")
print(f"Permissions: {acl['permissions']}")

# Set ACL
directory_client.set_access_control(
    owner="user-id",
    permissions="rwxr-x---"
)

# Update ACL entries
from azure.storage.filedatalake import AccessControlChangeResult
directory_client.update_access_control_recursive(
    acl="user:user-id:rwx"
)
```

## Async Client

```python
from azure.storage.filedatalake.aio import DataLakeServiceClient
from azure.identity.aio import DefaultAzureCredential

async def datalake_operations():
    credential = DefaultAzureCredential()
    
    async with DataLakeServiceClient(
        account_url="https://<account>.dfs.core.windows.net",
        credential=credential
    ) as service_client:
        file_system_client = service_client.get_file_system_client("myfilesystem")
        file_client = file_system_client.get_file_client("test.txt")
        
        await file_client.upload_data(b"async content", overwrite=True)
        
        download = await file_client.download_file()
        content = await download.readall()

import asyncio
asyncio.run(datalake_operations())
```

## Best Practices

1. **Use hierarchical namespace** for file system semantics
2. **Use `append_data` + `flush_data`** for large file uploads
3. **Set ACLs at directory level** and inherit to children
4. **Use async client** for high-throughput scenarios
5. **Use `get_paths` with `recursive=True`** for full directory listing
6. **Set metadata** for custom file attributes
7. **Consider Blob API** for simple object storage use cases

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# @azure/storage-queue (TypeScript/JavaScript)

SDK for Azure Queue Storage operations — send, receive, peek, and manage messages in queues.

## Installation

```bash
npm install @azure/storage-queue @azure/identity
```

**Current Version**: 12.x  
**Node.js**: >= 18.0.0

## Environment Variables

```bash
AZURE_STORAGE_ACCOUNT_NAME=<account-name>
AZURE_STORAGE_ACCOUNT_KEY=<account-key>
# OR connection string
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
```

## Authentication

### DefaultAzureCredential (Recommended)

```typescript
import { QueueServiceClient } from "@azure/storage-queue";
import { DefaultAzureCredential } from "@azure/identity";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const client = new QueueServiceClient(
  `https://${accountName}.queue.core.windows.net`,
  new DefaultAzureCredential()
);
```

### Connection String

```typescript
import { QueueServiceClient } from "@azure/storage-queue";

const client = QueueServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING!
);
```

### StorageSharedKeyCredential (Node.js only)

```typescript
import { QueueServiceClient, StorageSharedKeyCredential } from "@azure/storage-queue";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const accountKey = process.env.AZURE_STORAGE_ACCOUNT_KEY!;

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
const client = new QueueServiceClient(
  `https://${accountName}.queue.core.windows.net`,
  sharedKeyCredential
);
```

### SAS Token

```typescript
import { QueueServiceClient } from "@azure/storage-queue";

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME!;
const sasToken = process.env.AZURE_STORAGE_SAS_TOKEN!;

const client = new QueueServiceClient(
  `https://${accountName}.queue.core.windows.net${sasToken}`
);
```

## Client Hierarchy

```
QueueServiceClient (account level)
└── QueueClient (queue level)
    └── Messages (send, receive, peek, delete)
```

## Queue Operations

### Create Queue

```typescript
const queueClient = client.getQueueClient("my-queue");
await queueClient.create();

// Or create if not exists
await queueClient.createIfNotExists();
```

### List Queues

```typescript
for await (const queue of client.listQueues()) {
  console.log(queue.name);
}

// With prefix filter
for await (const queue of client.listQueues({ prefix: "task-" })) {
  console.log(queue.name);
}
```

### Delete Queue

```typescript
await queueClient.delete();

// Or delete if exists
await queueClient.deleteIfExists();
```

### Get Queue Properties

```typescript
const properties = await queueClient.getProperties();
console.log("Approximate message count:", properties.approximateMessagesCount);
console.log("Metadata:", properties.metadata);
```

### Set Queue Metadata

```typescript
await queueClient.setMetadata({
  department: "engineering",
  priority: "high",
});
```

## Message Operations

### Send Message

```typescript
const queueClient = client.getQueueClient("my-queue");

// Simple message
await queueClient.sendMessage("Hello, World!");

// With options
await queueClient.sendMessage("Delayed message", {
  visibilityTimeout: 60, // Hidden for 60 seconds
  messageTimeToLive: 3600, // Expires in 1 hour
});

// JSON message (must be string)
const task = { type: "process", data: { id: 123 } };
await queueClient.sendMessage(JSON.stringify(task));
```

### Receive Messages

```typescript
// Receive up to 32 messages (default: 1)
const response = await queueClient.receiveMessages({
  numberOfMessages: 10,
  visibilityTimeout: 30, // 30 seconds to process
});

for (const message of response.receivedMessageItems) {
  console.log("Message ID:", message.messageId);
  console.log("Content:", message.messageText);
  console.log("Dequeue Count:", message.dequeueCount);
  console.log("Pop Receipt:", message.popReceipt);
  
  // Process the message...
  
  // Delete after processing
  await queueClient.deleteMessage(message.messageId, message.popReceipt);
}
```

### Peek Messages

Peek without removing from queue (no visibility timeout).

```typescript
const response = await queueClient.peekMessages({
  numberOfMessages: 5,
});

for (const message of response.peekedMessageItems) {
  console.log("Message ID:", message.messageId);
  console.log("Content:", message.messageText);
  // Note: No popReceipt - cannot delete peeked messages
}
```

### Update Message

Extend visibility timeout or update content.

```typescript
// Receive a message
const response = await queueClient.receiveMessages();
const message = response.receivedMessageItems[0];

if (message) {
  // Update content and extend visibility
  const updateResponse = await queueClient.updateMessage(
    message.messageId,
    message.popReceipt,
    "Updated content",
    60 // New visibility timeout in seconds
  );
  
  // Use new popReceipt for subsequent operations
  console.log("New pop receipt:", updateResponse.popReceipt);
}
```

### Delete Message

```typescript
// After receiving
const response = await queueClient.receiveMessages();
const message = response.receivedMessageItems[0];

if (message) {
  await queueClient.deleteMessage(message.messageId, message.popReceipt);
}
```

### Clear All Messages

```typescript
await queueClient.clearMessages();
```

## Message Processing Patterns

### Basic Worker Pattern

```typescript
async function processQueue(queueClient: QueueClient): Promise<void> {
  while (true) {
    const response = await queueClient.receiveMessages({
      numberOfMessages: 10,
      visibilityTimeout: 30,
    });

    if (response.receivedMessageItems.length === 0) {
      // No messages, wait before polling again
      await sleep(5000);
      continue;
    }

    for (const message of response.receivedMessageItems) {
      try {
        await processMessage(message.messageText);
        await queueClient.deleteMessage(message.messageId, message.popReceipt);
      } catch (error) {
        console.error(`Failed to process message ${message.messageId}:`, error);
        // Message will become visible again after timeout
      }
    }
  }
}

async function processMessage(content: string): Promise<void> {
  const task = JSON.parse(content);
  // Process task...
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

### Poison Message Handling

```typescript
const MAX_DEQUEUE_COUNT = 5;

async function processWithPoisonHandling(
  queueClient: QueueClient,
  poisonQueueClient: QueueClient
): Promise<void> {
  const response = await queueClient.receiveMessages({
    numberOfMessages: 10,
    visibilityTimeout: 30,
  });

  for (const message of response.receivedMessageItems) {
    if (message.dequeueCount > MAX_DEQUEUE_COUNT) {
      // Move to poison queue
      await poisonQueueClient.sendMessage(message.messageText);
      await queueClient.deleteMessage(message.messageId, message.popReceipt);
      console.log(`Moved message ${message.messageId} to poison queue`);
      continue;
    }

    try {
      await processMessage(message.messageText);
      await queueClient.deleteMessage(message.messageId, message.popReceipt);
    } catch (error) {
      console.error(`Processing failed (attempt ${message.dequeueCount}):`, error);
    }
  }
}
```

### Batch Processing with Visibility Extension

```typescript
async function processBatchWithExtension(queueClient: QueueClient): Promise<void> {
  const response = await queueClient.receiveMessages({
    numberOfMessages: 1,
    visibilityTimeout: 60,
  });

  const message = response.receivedMessageItems[0];
  if (!message) return;

  let popReceipt = message.popReceipt;

  // Start visibility extension timer
  const extensionInterval = setInterval(async () => {
    try {
      const updateResponse = await queueClient.updateMessage(
        message.messageId,
        popReceipt,
        message.messageText,
        60 // Extend by another 60 seconds
      );
      popReceipt = updateResponse.popReceipt;
    } catch (error) {
      console.error("Failed to extend visibility:", error);
    }
  }, 45000); // Extend every 45 seconds

  try {
    await longRunningProcess(message.messageText);
    await queueClient.deleteMessage(message.messageId, popReceipt);
  } finally {
    clearInterval(extensionInterval);
  }
}
```

## Message Encoding

By default, messages are Base64 encoded. You can customize this:

```typescript
import { QueueClient } from "@azure/storage-queue";

// Custom encoder/decoder for plain text
const queueClient = new QueueClient(
  `https://${accountName}.queue.core.windows.net/my-queue`,
  credential,
  {
    messageEncoding: "text", // "base64" (default) or "text"
  }
);

// Or with custom encoder
const customQueueClient = new QueueClient(
  `https://${accountName}.queue.core.windows.net/my-queue`,
  credential,
  {
    messageEncoding: {
      encode: (message: string) => Buffer.from(message).toString("base64"),
      decode: (message: string) => Buffer.from(message, "base64").toString(),
    },
  }
);
```

## SAS Token Generation (Node.js only)

### Generate Queue SAS

```typescript
import {
  QueueSASPermissions,
  generateQueueSASQueryParameters,
  StorageSharedKeyCredential,
} from "@azure/storage-queue";

const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);

const sasToken = generateQueueSASQueryParameters(
  {
    queueName: "my-queue",
    permissions: QueueSASPermissions.parse("raup"), // read, add, update, process
    startsOn: new Date(),
    expiresOn: new Date(Date.now() + 3600 * 1000), // 1 hour
  },
  sharedKeyCredential
).toString();

const sasUrl = `https://${accountName}.queue.core.windows.net/my-queue?${sasToken}`;
```

### Generate Account SAS

```typescript
import {
  AccountSASPermissions,
  AccountSASResourceTypes,
  AccountSASServices,
  generateAccountSASQueryParameters,
} from "@azure/storage-queue";

const sasToken = generateAccountSASQueryParameters(
  {
    services: AccountSASServices.parse("q").toString(), // queue
    resourceTypes: AccountSASResourceTypes.parse("sco").toString(),
    permissions: AccountSASPermissions.parse("rwdlacupi"),
    expiresOn: new Date(Date.now() + 24 * 3600 * 1000),
  },
  sharedKeyCredential
).toString();
```

## Error Handling

```typescript
import { RestError } from "@azure/storage-queue";

try {
  await queueClient.sendMessage("test");
} catch (error) {
  if (error instanceof RestError) {
    switch (error.statusCode) {
      case 404:
        console.log("Queue not found");
        break;
      case 400:
        console.log("Bad request - message too large or invalid");
        break;
      case 403:
        console.log("Access denied");
        break;
      case 409:
        console.log("Queue already exists or being deleted");
        break;
      default:
        console.error(`Storage error ${error.statusCode}: ${error.message}`);
    }
  }
  throw error;
}
```

## TypeScript Types Reference

```typescript
import {
  // Clients
  QueueServiceClient,
  QueueClient,

  // Authentication
  StorageSharedKeyCredential,
  AnonymousCredential,

  // SAS
  QueueSASPermissions,
  AccountSASPermissions,
  AccountSASServices,
  AccountSASResourceTypes,
  generateQueueSASQueryParameters,
  generateAccountSASQueryParameters,

  // Messages
  DequeuedMessageItem,
  PeekedMessageItem,
  QueueSendMessageResponse,
  QueueReceiveMessageResponse,
  QueueUpdateMessageResponse,

  // Queue
  QueueItem,
  QueueGetPropertiesResponse,

  // Errors
  RestError,
} from "@azure/storage-queue";
```

## Message Limits

| Limit | Value |
|-------|-------|
| Max message size | 64 KB |
| Max visibility timeout | 7 days |
| Max time-to-live | 7 days (or -1 for infinite) |
| Max messages per receive | 32 |
| Default visibility timeout | 30 seconds |

## Best Practices

1. **Use DefaultAzureCredential** — Prefer AAD over connection strings/keys
2. **Always delete after processing** — Prevent duplicate processing
3. **Handle poison messages** — Move failed messages to a dead-letter queue
4. **Use appropriate visibility timeout** — Set based on expected processing time
5. **Extend visibility for long tasks** — Update message to prevent timeout
6. **Use JSON for structured data** — Serialize objects to JSON strings
7. **Check dequeueCount** — Detect repeatedly failing messages
8. **Use batch receive** — Receive multiple messages for efficiency

## Platform Differences

| Feature | Node.js | Browser |
|---------|---------|---------|
| `StorageSharedKeyCredential` | ✅ | ❌ |
| SAS generation | ✅ | ❌ |
| DefaultAzureCredential | ✅ | ❌ |
| Anonymous/SAS access | ✅ | ✅ |
| All message operations | ✅ | ✅ |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Blob Storage SDK (Multi-Language)

This skill provides unified guidance for Azure Blob Storage across Python, Java, Rust, and TypeScript.

## Client Hierarchy (Universal)

Regardless of the language, the Blob Storage SDK follows a strict hierarchy:
1. **BlobServiceClient**: Account-level operations.
2. **ContainerClient**: Container-level operations (create, list blobs).
3. **BlobClient**: Single blob operations (upload, download, delete).

## Cross-Language Best Practices

1. **Authentication**: Use `DefaultAzureCredential` from the identity package instead of connection strings.
2. **Async/Context Managers**: Use async clients and context managers/`using` blocks where applicable to ensure proper connection pooling and cleanup.
3. **Chunking & Concurrency**: Configure chunk sizes and `max_concurrency` (or equivalent) for large file uploads/downloads.
4. **Memory Efficiency**: Prefer stream reading (`readinto()`, streams, pipes) over reading entire blobs into memory (`readall()`).
5. **Overwrites**: Be explicit when overwriting blobs (e.g., `overwrite=True` in Python).
6. **Hierarchical Listing**: Use `walk_blobs()` or `by_page()` with delimiters to list blobs like a file system.

## Language-Specific Package References

### Python
- **Install**: `pip install azure-storage-blob azure-identity`
- **Key Classes**: `BlobServiceClient`, `ContainerClient`, `BlobClient`

### TypeScript / Node.js
- **Install**: `npm install @azure/storage-blob @azure/identity`
- **Key Classes**: `BlobServiceClient`, `ContainerClient`, `BlockBlobClient`

### Java
- **Install**: `com.azure:azure-storage-blob`, `com.azure:azure-identity`
- **Key Classes**: `BlobServiceClient`, `BlobContainerClient`, `BlobClient`

### Rust
- **Install**: `azure_storage_blobs`
- **Key Classes**: `BlobServiceClient`, `ContainerClient`, `BlobClient`

---

# Azure Storage File Share SDK for Python

Manage SMB file shares for cloud-native and lift-and-shift scenarios.

## Installation

```bash
pip install azure-storage-file-share
```

## Environment Variables

```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...
# Or
AZURE_STORAGE_ACCOUNT_URL=https://<account>.file.core.windows.net
```

## Authentication

### Connection String

```python
from azure.storage.fileshare import ShareServiceClient

service = ShareServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
)
```

### Entra ID

```python
from azure.storage.fileshare import ShareServiceClient
from azure.identity import DefaultAzureCredential

service = ShareServiceClient(
    account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
    credential=DefaultAzureCredential()
)
```

## Share Operations

### Create Share

```python
share = service.create_share("my-share")
```

### List Shares

```python
for share in service.list_shares():
    print(f"{share.name}: {share.quota} GB")
```

### Get Share Client

```python
share_client = service.get_share_client("my-share")
```

### Delete Share

```python
service.delete_share("my-share")
```

## Directory Operations

### Create Directory

```python
share_client = service.get_share_client("my-share")
share_client.create_directory("my-directory")

# Nested directory
share_client.create_directory("my-directory/sub-directory")
```

### List Directories and Files

```python
directory_client = share_client.get_directory_client("my-directory")

for item in directory_client.list_directories_and_files():
    if item["is_directory"]:
        print(f"[DIR] {item['name']}")
    else:
        print(f"[FILE] {item['name']} ({item['size']} bytes)")
```

### Delete Directory

```python
share_client.delete_directory("my-directory")
```

## File Operations

### Upload File

```python
file_client = share_client.get_file_client("my-directory/file.txt")

# From string
file_client.upload_file("Hello, World!")

# From file
with open("local-file.txt", "rb") as f:
    file_client.upload_file(f)

# From bytes
file_client.upload_file(b"Binary content")
```

### Download File

```python
file_client = share_client.get_file_client("my-directory/file.txt")

# To bytes
data = file_client.download_file().readall()

# To file
with open("downloaded.txt", "wb") as f:
    data = file_client.download_file()
    data.readinto(f)

# Stream chunks
download = file_client.download_file()
for chunk in download.chunks():
    process(chunk)
```

### Get File Properties

```python
properties = file_client.get_file_properties()
print(f"Size: {properties.size}")
print(f"Content type: {properties.content_settings.content_type}")
print(f"Last modified: {properties.last_modified}")
```

### Delete File

```python
file_client.delete_file()
```

### Copy File

```python
source_url = "https://account.file.core.windows.net/share/source.txt"
dest_client = share_client.get_file_client("destination.txt")
dest_client.start_copy_from_url(source_url)
```

## Range Operations

### Upload Range

```python
# Upload to specific range
file_client.upload_range(data=b"content", offset=0, length=7)
```

### Download Range

```python
# Download specific range
download = file_client.download_file(offset=0, length=100)
data = download.readall()
```

## Snapshot Operations

### Create Snapshot

```python
snapshot = share_client.create_snapshot()
print(f"Snapshot: {snapshot['snapshot']}")
```

### Access Snapshot

```python
snapshot_client = service.get_share_client(
    "my-share",
    snapshot=snapshot["snapshot"]
)
```

## Async Client

```python
from azure.storage.fileshare.aio import ShareServiceClient
from azure.identity.aio import DefaultAzureCredential

async def upload_file():
    credential = DefaultAzureCredential()
    service = ShareServiceClient(account_url, credential=credential)
    
    share = service.get_share_client("my-share")
    file_client = share.get_file_client("test.txt")
    
    await file_client.upload_file("Hello!")
    
    await service.close()
    await credential.close()
```

## Client Types

| Client | Purpose |
|--------|---------|
| `ShareServiceClient` | Account-level operations |
| `ShareClient` | Share operations |
| `ShareDirectoryClient` | Directory operations |
| `ShareFileClient` | File operations |

## Best Practices

1. **Use connection string** for simplest setup
2. **Use Entra ID** for production with RBAC
3. **Stream large files** using chunks() to avoid memory issues
4. **Create snapshots** before major changes
5. **Set quotas** to prevent unexpected storage costs
6. **Use ranges** for partial file updates
7. **Close async clients** explicitly

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
