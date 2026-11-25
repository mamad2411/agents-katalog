---
name: azure-messaging-toolkit
description: Consolidated toolkit for azure-messaging. Covers azure-messaging-webpubsubservice-py, azure-messaging-webpubsub-java
---
# Azure Messaging Toolkit

## Core Capabilities
# Azure Messaging Toolkit

# Azure Web PubSub Service SDK for Python

Real-time messaging with WebSocket connections at scale.

## Installation

```bash
# Service SDK (server-side)
pip install azure-messaging-webpubsubservice

# Client SDK (for Python WebSocket clients)
pip install azure-messaging-webpubsubclient
```

## Environment Variables

```bash
AZURE_WEBPUBSUB_CONNECTION_STRING=Endpoint=https://<name>.webpubsub.azure.com;AccessKey=...
AZURE_WEBPUBSUB_HUB=my-hub
```

## Service Client (Server-Side)

### Authentication

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# Connection string
client = WebPubSubServiceClient.from_connection_string(
    connection_string=os.environ["AZURE_WEBPUBSUB_CONNECTION_STRING"],
    hub="my-hub"
)

# Entra ID
from azure.identity import DefaultAzureCredential

client = WebPubSubServiceClient(
    endpoint="https://<name>.webpubsub.azure.com",
    hub="my-hub",
    credential=DefaultAzureCredential()
)
```

### Generate Client Access Token

```python
# Token for anonymous user
token = client.get_client_access_token()
print(f"URL: {token['url']}")

# Token with user ID
token = client.get_client_access_token(
    user_id="user123",
    roles=["webpubsub.sendToGroup", "webpubsub.joinLeaveGroup"]
)

# Token with groups
token = client.get_client_access_token(
    user_id="user123",
    groups=["group1", "group2"]
)
```

### Send to All Clients

```python
# Send text
client.send_to_all(message="Hello everyone!", content_type="text/plain")

# Send JSON
client.send_to_all(
    message={"type": "notification", "data": "Hello"},
    content_type="application/json"
)
```

### Send to User

```python
client.send_to_user(
    user_id="user123",
    message="Hello user!",
    content_type="text/plain"
)
```

### Send to Group

```python
client.send_to_group(
    group="my-group",
    message="Hello group!",
    content_type="text/plain"
)
```

### Send to Connection

```python
client.send_to_connection(
    connection_id="abc123",
    message="Hello connection!",
    content_type="text/plain"
)
```

### Group Management

```python
# Add user to group
client.add_user_to_group(group="my-group", user_id="user123")

# Remove user from group
client.remove_user_from_group(group="my-group", user_id="user123")

# Add connection to group
client.add_connection_to_group(group="my-group", connection_id="abc123")

# Remove connection from group
client.remove_connection_from_group(group="my-group", connection_id="abc123")
```

### Connection Management

```python
# Check if connection exists
exists = client.connection_exists(connection_id="abc123")

# Check if user has connections
exists = client.user_exists(user_id="user123")

# Check if group has connections
exists = client.group_exists(group="my-group")

# Close connection
client.close_connection(connection_id="abc123", reason="Session ended")

# Close all connections for user
client.close_all_connections(user_id="user123")
```

### Grant/Revoke Permissions

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# Grant permission
client.grant_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# Revoke permission
client.revoke_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# Check permission
has_permission = client.check_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)
```

## Client SDK (Python WebSocket Client)

```python
from azure.messaging.webpubsubclient import WebPubSubClient

client = WebPubSubClient(credential=token["url"])

# Event handlers
@client.on("connected")
def on_connected(e):
    print(f"Connected: {e.connection_id}")

@client.on("server-message")
def on_message(e):
    print(f"Message: {e.data}")

@client.on("group-message")
def on_group_message(e):
    print(f"Group {e.group}: {e.data}")

# Connect and send
client.open()
client.send_to_group("my-group", "Hello from Python!")
```

## Async Service Client

```python
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.identity.aio import DefaultAzureCredential

async def broadcast():
    credential = DefaultAzureCredential()
    client = WebPubSubServiceClient(
        endpoint="https://<name>.webpubsub.azure.com",
        hub="my-hub",
        credential=credential
    )
    
    await client.send_to_all("Hello async!", content_type="text/plain")
    
    await client.close()
    await credential.close()
```

## Client Operations

| Operation | Description |
|-----------|-------------|
| `get_client_access_token` | Generate WebSocket connection URL |
| `send_to_all` | Broadcast to all connections |
| `send_to_user` | Send to specific user |
| `send_to_group` | Send to group members |
| `send_to_connection` | Send to specific connection |
| `add_user_to_group` | Add user to group |
| `remove_user_from_group` | Remove user from group |
| `close_connection` | Disconnect client |
| `connection_exists` | Check connection status |

## Best Practices

1. **Use roles** to limit client permissions
2. **Use groups** for targeted messaging
3. **Generate short-lived tokens** for security
4. **Use user IDs** to send to users across connections
5. **Handle reconnection** in client applications
6. **Use JSON** content type for structured data
7. **Close connections** gracefully with reasons

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Web PubSub SDK for Java

Build real-time web applications using the Azure Web PubSub SDK for Java.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-webpubsub</artifactId>
    <version>1.5.0</version>
</dependency>
```

## Client Creation

### With Connection String

```java
import com.azure.messaging.webpubsub.WebPubSubServiceClient;
import com.azure.messaging.webpubsub.WebPubSubServiceClientBuilder;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .connectionString("<connection-string>")
    .hub("chat")
    .buildClient();
```

### With Access Key

```java
import com.azure.core.credential.AzureKeyCredential;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .credential(new AzureKeyCredential("<access-key>"))
    .endpoint("<endpoint>")
    .hub("chat")
    .buildClient();
```

### With DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

WebPubSubServiceClient client = new WebPubSubServiceClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint("<endpoint>")
    .hub("chat")
    .buildClient();
```

### Async Client

```java
import com.azure.messaging.webpubsub.WebPubSubServiceAsyncClient;

WebPubSubServiceAsyncClient asyncClient = new WebPubSubServiceClientBuilder()
    .connectionString("<connection-string>")
    .hub("chat")
    .buildAsyncClient();
```

## Key Concepts

- **Hub**: Logical isolation unit for connections
- **Group**: Subset of connections within a hub
- **Connection**: Individual WebSocket client connection
- **User**: Entity that can have multiple connections

## Core Patterns

### Send to All Connections

```java
import com.azure.messaging.webpubsub.models.WebPubSubContentType;

// Send text message
client.sendToAll("Hello everyone!", WebPubSubContentType.TEXT_PLAIN);

// Send JSON
String jsonMessage = "{\"type\": \"notification\", \"message\": \"New update!\"}";
client.sendToAll(jsonMessage, WebPubSubContentType.APPLICATION_JSON);
```

### Send to All with Filter

```java
import com.azure.core.http.rest.RequestOptions;
import com.azure.core.util.BinaryData;

BinaryData message = BinaryData.fromString("Hello filtered users!");

// Filter by userId
client.sendToAllWithResponse(
    message,
    WebPubSubContentType.TEXT_PLAIN,
    message.getLength(),
    new RequestOptions().addQueryParam("filter", "userId ne 'user1'"));

// Filter by groups
client.sendToAllWithResponse(
    message,
    WebPubSubContentType.TEXT_PLAIN,
    message.getLength(),
    new RequestOptions().addQueryParam("filter", "'GroupA' in groups and not('GroupB' in groups)"));
```

### Send to Group

```java
// Send to all connections in a group
client.sendToGroup("java-developers", "Hello Java devs!", WebPubSubContentType.TEXT_PLAIN);

// Send JSON to group
String json = "{\"event\": \"update\", \"data\": {\"version\": \"2.0\"}}";
client.sendToGroup("subscribers", json, WebPubSubContentType.APPLICATION_JSON);
```

### Send to Specific Connection

```java
// Send to a specific connection by ID
client.sendToConnection("connectionId123", "Private message", WebPubSubContentType.TEXT_PLAIN);
```

### Send to User

```java
// Send to all connections for a specific user
client.sendToUser("andy", "Hello Andy!", WebPubSubContentType.TEXT_PLAIN);
```

### Manage Groups

```java
// Add connection to group
client.addConnectionToGroup("premium-users", "connectionId123");

// Remove connection from group
client.removeConnectionFromGroup("premium-users", "connectionId123");

// Add user to group (all their connections)
client.addUserToGroup("admin-group", "userId456");

// Remove user from group
client.removeUserFromGroup("admin-group", "userId456");

// Check if user is in group
boolean exists = client.userExistsInGroup("admin-group", "userId456");
```

### Manage Connections

```java
// Check if connection exists
boolean connected = client.connectionExists("connectionId123");

// Close a connection
client.closeConnection("connectionId123");

// Close with reason
client.closeConnection("connectionId123", "Session expired");

// Check if user exists (has any connections)
boolean userOnline = client.userExists("userId456");

// Close all connections for a user
client.closeUserConnections("userId456");

// Close all connections in a group
client.closeGroupConnections("inactive-group");
```

### Generate Client Access Token

```java
import com.azure.messaging.webpubsub.models.GetClientAccessTokenOptions;
import com.azure.messaging.webpubsub.models.WebPubSubClientAccessToken;

// Basic token
WebPubSubClientAccessToken token = client.getClientAccessToken(
    new GetClientAccessTokenOptions());
System.out.println("URL: " + token.getUrl());

// With user ID
WebPubSubClientAccessToken userToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions().setUserId("user123"));

// With roles (permissions)
WebPubSubClientAccessToken roleToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .addRole("webpubsub.joinLeaveGroup")
        .addRole("webpubsub.sendToGroup"));

// With groups to join on connect
WebPubSubClientAccessToken groupToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .addGroup("announcements")
        .addGroup("updates"));

// With custom expiration
WebPubSubClientAccessToken expToken = client.getClientAccessToken(
    new GetClientAccessTokenOptions()
        .setUserId("user123")
        .setExpiresAfter(Duration.ofHours(2)));
```

### Grant/Revoke Permissions

```java
import com.azure.messaging.webpubsub.models.WebPubSubPermission;

// Grant permission to send to a group
client.grantPermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));

// Revoke permission
client.revokePermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));

// Check permission
boolean hasPermission = client.checkPermission(
    WebPubSubPermission.SEND_TO_GROUP,
    "connectionId123",
    new RequestOptions().addQueryParam("targetName", "chat-room"));
```

### Async Operations

```java
asyncClient.sendToAll("Async message!", WebPubSubContentType.TEXT_PLAIN)
    .subscribe(
        unused -> System.out.println("Message sent"),
        error -> System.err.println("Error: " + error.getMessage())
    );

asyncClient.sendToGroup("developers", "Group message", WebPubSubContentType.TEXT_PLAIN)
    .doOnSuccess(v -> System.out.println("Sent to group"))
    .doOnError(e -> System.err.println("Failed: " + e))
    .subscribe();
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.sendToConnection("invalid-id", "test", WebPubSubContentType.TEXT_PLAIN);
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
}
```

## Environment Variables

```bash
WEB_PUBSUB_CONNECTION_STRING=Endpoint=https://<resource>.webpubsub.azure.com;AccessKey=...
WEB_PUBSUB_ENDPOINT=https://<resource>.webpubsub.azure.com
WEB_PUBSUB_ACCESS_KEY=<your-access-key>
```

## Client Roles

| Role | Permission |
|------|------------|
| `webpubsub.joinLeaveGroup` | Join/leave any group |
| `webpubsub.sendToGroup` | Send to any group |
| `webpubsub.joinLeaveGroup.<group>` | Join/leave specific group |
| `webpubsub.sendToGroup.<group>` | Send to specific group |

## Best Practices

1. **Use Groups**: Organize connections into groups for targeted messaging
2. **User IDs**: Associate connections with user IDs for user-level messaging
3. **Token Expiration**: Set appropriate token expiration for security
4. **Roles**: Grant minimal required permissions via roles
5. **Hub Isolation**: Use separate hubs for different application features
6. **Connection Management**: Clean up inactive connections

## Trigger Phrases

- "Web PubSub Java"
- "WebSocket messaging Azure"
- "real-time push notifications"
- "server-sent events"
- "chat application backend"
- "live updates broadcasting"

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
