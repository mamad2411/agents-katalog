---
name: dapr-deployment
description: Master Dapr (Distributed Application Runtime) for building distributed microservices from hello world to professional production systems. This skill covers Dapr's building blocks, sidecar pattern, service invocation, pub/sub, state management, actors, secrets management, and deployment strategies. Use when developing resilient, portable, and microservice-based applications with Dapr.
---

# Dapr (Distributed Application Runtime) Deployment Skill

Master Dapr (Distributed Application Runtime) for building distributed microservices from hello world to professional production systems. This skill covers Dapr's building blocks, sidecar pattern, service invocation, pub/sub, state management, actors, secrets management, and deployment strategies.

## Table of Contents
1. [Dapr Overview](#dapr-overview)
2. [Architecture and Sidecar Pattern](#architecture-and-sidecar-pattern)
3. [Building Blocks](#building-blocks)
4. [Service Invocation](#service-invocation)
5. [Pub/Sub Messaging](#pubsub-messaging)
6. [State Management](#state-management)
7. [Actors](#actors)
8. [Secrets Management](#secrets-management)
9. [Bindings](#bindings)
10. [Configuration Management](#configuration-management)
11. [Dapr CLI Usage](#dapr-cli-usage)
12. [Deployment Strategies](#deployment-strategies)
13. [Production Best Practices](#production-best-practices)

## Dapr Overview

Dapr (Distributed Application Runtime) is a portable, event-driven runtime that makes it easy for any developer to build resilient, stateless, and stateful applications that run on the cloud and edge. It leverages a sidecar architecture to provide a set of building blocks that simplify the development of distributed applications.

### Key Features
- **Portable**: Runs on any environment (Kubernetes, self-hosted, IoT/Edge)
- **Language/Framework Agnostic**: Works with any programming language and framework
- **Event-Driven**: Built-in support for pub/sub messaging patterns
- **Resilient**: Automatic retries, circuit breaking, and distributed tracing
- **Secure**: Built-in service-to-service authentication and transport security

## Architecture and Sidecar Pattern

Dapr uses a sidecar architecture where each application has its own Dapr runtime instance. This approach provides several benefits:

### Sidecar Benefits
- **Separation of Concerns**: Application logic is separate from infrastructure concerns
- **Polyglot Support**: Each application can use different languages and frameworks
- **Independent Scaling**: Applications and Dapr instances can scale independently
- **Platform Agnostic**: Same Dapr APIs work across different hosting environments

### The Translator Analogy: Why Sidecars Abstract Infrastructure

Think of the Dapr sidecar as a universal translator in a multilingual environment. Just as a translator sits between people speaking different languages and enables them to communicate without needing to learn each other's language, the Dapr sidecar sits between your application and various infrastructure components (databases, message queues, etc.).

- **Without Dapr**: Your application needs to understand the specific API, protocol, and configuration of each infrastructure component (e.g., Redis API, RabbitMQ protocol, Azure Storage API).
- **With Dapr**: Your application speaks to the Dapr sidecar using standard HTTP/gRPC APIs, and the sidecar translates these calls to the specific infrastructure component's protocol.

This abstraction allows your application to remain infrastructure-agnostic and focus on business logic rather than infrastructure complexities.

### Architecture Components
- **Application**: Your business logic application
- **Dapr Sidecar (daprd)**: Dapr runtime running alongside the application
- **Components**: Pluggable infrastructure backends (state stores, pub/sub, etc.)

### Dapr Runtime (daprd) Ports

The Dapr sidecar (daprd) exposes standard ports for communication:

- **HTTP Port**: `3500` (default) - For HTTP API calls to Dapr
- **gRPC Port**: `50001` (default) - For gRPC API calls to Dapr
- **Internal gRPC Port**: `50002` (default) - For internal Dapr-to-Dapr communication

These ports can be customized using CLI flags or Kubernetes annotations:
- `--dapr-http-port` for HTTP port
- `--dapr-grpc-port` for gRPC port
- `--internal-grpc-port` for internal gRPC port

### Container Mode vs Process Mode

Dapr can run in two different modes depending on your hosting environment:

#### Process Mode
- **Environment**: Self-hosted (local development, VMs)
- **Description**: Dapr runs as a separate process alongside your application
- **Communication**: Application communicates with Dapr sidecar via localhost
- **Management**: Managed via Dapr CLI (`dapr run`, `dapr init`)
- **Example**: `dapr run --app-id myapp --app-port 3000 node app.js`

#### Container Mode
- **Environment**: Kubernetes, Docker, container orchestrators
- **Description**: Dapr runs as a separate container within the same pod/container group as your application
- **Communication**: Application communicates with Dapr sidecar via localhost (same pod network)
- **Management**: Managed by platform (Kubernetes admission controller injects Dapr sidecar)
- **Example**: Kubernetes pod with Dapr annotations automatically gets a sidecar container injected

### Three Essential Kubernetes Annotations

When deploying Dapr to Kubernetes, these three annotations are essential for basic functionality:

1. **`dapr.io/enabled: "true"`** - Enables Dapr sidecar injection for the pod
2. **`dapr.io/app-id: "<app-id>"`** - Sets the unique application ID for service discovery
3. **`dapr.io/app-port: "<port>"`** - Specifies the port your application is listening on

Example minimal Kubernetes deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"          # Enable Dapr sidecar
        dapr.io/app-id: "myapp"          # Set application ID
        dapr.io/app-port: "3000"         # Set application port
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
```

## Building Blocks

Dapr provides several building blocks for common distributed application patterns:

### Core Building Blocks
1. **Service Invocation**: Service-to-service communication with built-in service discovery
2. **Pub/Sub**: Publish and subscribe messaging patterns
3. **State Management**: Distributed state management with pluggable state stores
4. **Actors**: Virtual actor pattern implementation
5. **Secrets**: Secrets management with pluggable providers
6. **Bindings**: Input/output bindings for external systems
7. **Configuration**: Dynamic configuration management

## Service Invocation

Dapr simplifies service-to-service communication with built-in service discovery, tracing, and resilience features.

### HTTP Service Invocation
```bash
# Invoke a service using Dapr's service invocation
curl -X POST http://localhost:3500/v1.0/invoke/target-app/method/endpoint \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from Dapr"}'
```

### Service Invocation with gRPC
```go
// Go example using gRPC
import "github.com/dapr/go-sdk/client"

client, err := client.NewClient()
if err != nil {
    panic(err)
}
defer client.Close()

resp, err := client.InvokeService(ctx, "target-app", "endpoint", []byte("request"))
if err != nil {
    panic(err)
}
```

### Service Discovery Configuration
```yaml
# Dapr component for service discovery
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: service-discovery-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
```

## Pub/Sub Messaging

Dapr implements the publish-subscribe pattern to enable event-driven architectures.

### Publishing Messages
```bash
# Publish a message to a topic
curl -X POST http://localhost:3500/v1.0/publish/pubsub-name/topic-name \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "12345",
    "amount": 100
  }'
```

### Python SDK Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Publish a message to a topic
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='orders',
        data=json.dumps({'orderId': '12345', 'amount': 100}),
        data_content_type='application/json'
    )
```

### Subscription Endpoint (HTTP)
```python
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def orders_handler():
    content = request.get_json()
    print(f'Received order: {content}')

    # Process the order
    # ...

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(port=5000)
```

### Subscription Component Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

## State Management

Dapr provides a key-value state management API with support for various state stores.

### Saving State
```bash
# Save state to a configured state store
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{
    "key": "user-123",
    "value": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }]'
```

### Python SDK Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Save state
    client.save_state(
        store_name='statestore',
        key='user-123',
        value={'name': 'John Doe', 'email': 'john@example.com'}
    )

    # Get state
    result = client.get_state(store_name='statestore', key='user-123')
    print(f'State: {result.data.decode()}')

    # Delete state
    client.delete_state(store_name='statestore', key='user-123')
```

### State Store Component Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

## Actors

Dapr provides a virtual actor implementation that simplifies stateful service development.

### Actor Registration (.NET)
```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddActors(options =>
    {
        // Register actor types
        options.Actors.RegisterActor<MyActor>();

        // Configure actor settings
        options.ActorIdleTimeout = TimeSpan.FromMinutes(60);
        options.ActorScanInterval = TimeSpan.FromSeconds(30);
        options.DrainOngoingCallTimeout = TimeSpan.FromSeconds(60);
    });
}
```

### Actor State Management (.NET)
```csharp
public class MyActor : Actor, IMyActor
{
    public MyActor(ActorHost host) : base(host)
    {
    }

    public async Task<string> SayAsync(string message)
    {
        // Get previous state
        var previousMessage = await this.StateManager.GetStateAsync<string>("lastmessage");

        // Set new state
        await this.StateManager.SetStateAsync("lastmessage", message);

        return previousMessage ?? "No previous message";
    }
}
```

### Actor Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: actor-config
spec:
  actors:
    actorIdleTimeout: 1h
    actorScanInterval: 30s
    drainOngoingCallTimeout: 1m
    drainRebalancedActors: true
    reentrancy:
      enabled: true
      maxStackDepth: 32
```

## Secrets Management

Dapr provides a secrets management API that abstracts away the underlying secret store.

### Getting Secrets
```bash
# Get a secret from a configured secret store
curl http://localhost:3500/v1.0/secrets/secretstore/my-secret
```

### Python SDK Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get secret
    result = client.get_secret(
        store_name='localsecretstore',
        key='my-secret'
    )
    print(f'Secret value: {result.data["my-secret"]}')
```

### Local Secret Store Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: localsecretstore
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: ./secrets.json
  - name: nestedSeparator
    value: ":"
```

## Bindings

Dapr bindings provide a way to integrate with external systems using input and output bindings.

### Input Binding Example
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/input-binding', methods=['POST'])
def input_binding_handler():
    content = request.get_json()
    print(f'Received from binding: {content}')

    # Process the data
    # ...

    return {'status': 'success'}
```

### Output Binding Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Send data to an output binding
    client.invoke_binding(
        name='output-binding',
        operation='create',
        data=b'{"message": "Hello from Dapr"}'
    )
```

### Binding Component Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-input-binding
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "@every 30s"
```

## Configuration Management

Dapr provides dynamic configuration management for applications.

### Getting Configuration
```bash
# Get configuration items
curl http://localhost:3500/v1.0/configuration/configstore \
  -H "Content-Type: application/json" \
  -d '["key1", "key2"]'
```

## Dapr CLI Usage

### Starting an Application with Dapr
```bash
# Run an application with Dapr sidecar
dapr run --app-id myapp --app-port 3000 --dapr-http-port 3500 node app.js

# Run with specific resources path
dapr run --app-id myapp --resources-path ./components -- node app.js

# Run with custom configuration
dapr run --app-id myapp --config ./config.yaml -- node app.js
```

### Common Dapr CLI Flags
- `--app-id`: Required application ID for service discovery
- `--app-port`: Port your application is listening on
- `--app-protocol`: Protocol for Dapr to talk to your application (http, grpc)
- `--resources-path`: Path for components directory
- `--config`: Dapr configuration file
- `--dapr-http-port`: HTTP port for Dapr to listen on (default: 3500)
- `--dapr-grpc-port`: gRPC port for Dapr to listen on (default: 50001)

### Dapr CLI Commands
```bash
# List running Dapr applications
dapr list

# Stop all Dapr applications
dapr stop --all

# Get Dapr status
dapr status

# Dashboard
dapr dashboard
```

## Deployment Strategies

### Self-Hosted Deployment
```bash
# Install Dapr locally
dapr init

# Run multiple services with Dapr
dapr run --app-id service1 --app-port 3000 --dapr-http-port 3501 node service1.js &
dapr run --app-id service2 --app-port 4000 --dapr-http-port 3502 node service2.js &
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "3000"
        dapr.io/config: "app-config"
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
```

## Production Best Practices

### Security
- Use mutual TLS for service-to-service communication
- Implement proper secret management
- Use namespaces for multi-tenancy
- Regularly update Dapr runtime

### Observability
- Enable distributed tracing
- Monitor Dapr sidecar metrics
- Implement proper logging
- Set up health checks

### Performance
- Optimize component configurations
- Use appropriate state store for your use case
- Configure proper resource limits
- Monitor sidecar performance

### Resilience
- Implement circuit breakers
- Use appropriate retry policies
- Configure timeouts appropriately
- Plan for graceful shutdowns

Mastering these Dapr concepts and patterns will help you build resilient, scalable, and maintainable distributed applications.