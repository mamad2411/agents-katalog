---
name: testing-examples
description: High-performance IoC web framework built on Bun runtime with decorator-based dependency injection, achieving 200k-300k requests/sec.
metadata:
  source: llms.txt
  source_url: https://asena.sh/llms-full.txt
  generated: 2026-08-11T10:26:43.083Z
---

# Testing Examples

> High-performance IoC web framework built on Bun runtime with decorator-based dependency injection, achieving 200k-300k requests/sec.

Section: Docs
Source: https://asena.sh/raw/philosophy.md

`Spring Boot` and `Quarkus` have established proven patterns for enterprise application development, but developers transitioning to TypeScript often find themselves reimplementing familiar concepts or adapting to unfamiliar architectures. `AsenaJS` addresses this gap by bringing automatic component discovery and field-based dependency injection to the `Bun` ecosystem.

The framework eliminates boilerplate through automatic scanning of decorator-annotated classes, removing the need for explicit module declarations or manual wiring. Components marked with `@Controller`, `@Service`, or `@Repository` (via the asena-drizzle package) are discovered and registered automatically, allowing developers to focus on business logic rather than configuration. Combined with Bun's native performance characteristics, this delivers both the familiar developer experience of Spring Boot and the speed expected from a modern JavaScript runtime.

`AsenaJS` is designed to make developers familiar with `Spring Boot` and `Quarkus` feel at home in the TypeScript ecosystem. As the framework evolves, we remain committed to this philosophy — bringing more proven patterns from the Java world while maintaining the performance advantages that `Bun` provides and the flexibility of TypeScript.

## Available Resources

### Core Principles

### What Asena Is Not

### Related

- **Get Started**
  - URL: /docs/get-started

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Adapters Overview**
  - URL: /docs/adapters/overview

- **Testing Overview**
  - URL: /docs/testing/overview

- **Roadmap**
  - URL: /docs/roadmap

### Prerequisites

- **Bun**
  - URL: https://bun.sh

### Option 1: With Asena CLI (Recommended)

### Option 2: Manual Setup

### Project Structure

### Next Steps

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **Scheduled Tasks**
  - URL: /docs/concepts/scheduled-tasks

- **Frontend Controller**
  - URL: /docs/concepts/frontend-controller

- **OpenAPI**
  - URL: /docs/packages/openapi

- **Redis**
  - URL: /docs/packages/redis

- **CLI Commands**
  - URL: /docs/cli/commands

- **Examples**
  - URL: /docs/examples

### Common Issues

### Complete REST API

### WebSocket Chat Application

### Authentication with Middleware

### Rate Limiting

### CORS Configuration

### OpenAPI Auto-Documentation

### Redis Caching

### Scheduled Tasks

### Frontend Controller

### Related Documentation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Scheduled Tasks**
  - URL: /docs/concepts/scheduled-tasks

- **Frontend Controller**
  - URL: /docs/concepts/frontend-controller

- **PostProcessor**
  - URL: /docs/concepts/post-processor

- **OpenAPI Package**
  - URL: /docs/packages/openapi

- **Redis Package**
  - URL: /docs/packages/redis

- **Drizzle Package**
  - URL: /docs/packages/drizzle

- **Logger Package**
  - URL: /docs/packages/logger

### Production Applications

### Why These Projects Chose Asena

### Stats & Insights

### Submit Your Project

- **GitHub Issues**
  - URL: https://github.com/AsenaJs/Asena/issues/new

- **Edit on GitHub**
  - URL: https://github.com/AsenaJs/Website/edit/master/docs/showcase.md

- **Link**: **Include This Information**
```markdown
- Project Name: [Name]
- Website: 
- Description: [Brief description]
- GitHub: https://github.com/... (optional)
- Tech Stack: [Technologies used] (optional)
- Asena Features: [Controllers, WebSocket, etc.]
```
  - URL: https://...

### Get Inspired

- **Get Started**
  - URL: /docs/get-started

- **Examples**
  - URL: /docs/examples

- **WebSocket Guide**
  - URL: /docs/concepts/websocket

- **OpenAPI**
  - URL: /docs/packages/openapi

- **Redis**
  - URL: /docs/packages/redis

- **Scheduled Tasks**
  - URL: /docs/concepts/scheduled-tasks

- **CLI Tools**
  - URL: /docs/cli/overview

### Community

- **AsenaJs/Asena**
  - URL: https://github.com/AsenaJs/Asena

- **Report bugs or request features**
  - URL: https://github.com/AsenaJs/Asena/issues

### Related

- **Examples**
  - URL: /docs/examples

- **Roadmap**
  - URL: /docs/roadmap

- **Get Started**
  - URL: /docs/get-started

- **GitHub Repository**
  - URL: https://github.com/AsenaJs/Asena

### ✅ Current Release (v0.10.x)

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Signal handling**
  - URL: /docs/concepts/lifecycle#signal-handling

- **`keepAlive`**
  - URL: /docs/concepts/lifecycle#keepalive-and-headless-workers

- **Liveness and readiness probes**
  - URL: /docs/concepts/lifecycle#health-probes

- **Decorator Inheritance**
  - URL: /docs/concepts/inheritance

- **its own config hook**
  - URL: /docs/guides/error-handling#not-found

- **Uniform error handling**
  - URL: /docs/guides/error-handling#adapter-logging

- **One `HttpException`**
  - URL: /docs/guides/error-handling#throwing-http-exceptions

- **Validation**
  - URL: /docs/concepts/validation

- **Static File Serving**
  - URL: /docs/concepts/static-files

- **multi-pod transport**
  - URL: /docs/concepts/websocket#multi-pod-websocket

- **Ulak**
  - URL: /docs/concepts/ulak

- **Scheduled Tasks**
  - URL: /docs/concepts/scheduled-tasks

- **FrontendController**
  - URL: /docs/concepts/frontend-controller

- **PostProcessor**
  - URL: /docs/concepts/post-processor

- **Graceful Server Shutdown**
  - URL: /docs/concepts/lifecycle#stop-sequence

- **Microservices**
  - URL: /docs/concepts/microservices

- **mockComponent**
  - URL: /docs/testing/mock-component

- **createTestApp**
  - URL: /docs/testing/test-app

- **createWebTest**
  - URL: /docs/testing/web-test

- **strict mode (trailing slash)**
  - URL: /docs/adapters/hono#trailing-slash-strict-mode

- **@asenajs/asena-logger**
  - URL: /docs/packages/logger

- **@asenajs/asena-drizzle**
  - URL: /docs/packages/drizzle

- **@asenajs/asena-openapi**
  - URL: /docs/packages/openapi

- **@asenajs/asena-redis**
  - URL: /docs/packages/redis

- **@asenajs/asena-kafka**
  - URL: /docs/packages/kafka

- **@asenajs/asena-otel**
  - URL: /docs/packages/opentelemetry

- **`asena-config.ts`**
  - URL: /docs/cli/configuration

### 📋 Planned for v1.0

- **shipped in v0.10**
  - URL: /docs/concepts/lifecycle

### 💡 Future Ideas (CLI)

### 🎯 Release Philosophy

### 🤝 Community Involvement

### 📅 Release Schedule

### 🔮 Long-Term Vision

### Related

- **Get Started**
  - URL: /docs/get-started

- **CLI Overview**
  - URL: /docs/cli/overview

- **GitHub Repository**
  - URL: https://github.com/AsenaJs/Asena

- **Examples**
  - URL: /docs/examples

### Quick Start

### The @Controller Decorator

### HTTP Method Decorators

### Working with Request Data

### Sending Responses

### Context API Reference

### Service Injection

### Middleware Integration

### Validation

### Combining Features

### Best Practices

### Related Documentation

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Inheritance**
  - URL: /docs/concepts/inheritance

- **Context API**
  - URL: /docs/concepts/context

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Hono Adapter**
  - URL: /docs/adapters/hono

### What is a Service?

### Creating a Service

### Using Services in Controllers

### Service Dependencies

### Layered Architecture

### Service Patterns

### Service Scopes

### Lifecycle Hooks

### String-based vs Class-based Injection

### @Service Decorator API

### Asena-Specific Best Practices

### Testing Services

### Related Documentation

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Controllers**
  - URL: /docs/concepts/controllers

- **Ulak - WebSocket Messaging System**
  - URL: /docs/concepts/ulak

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Drizzle ORM**
  - URL: /docs/packages/drizzle

- **Testing Guide**
  - URL: /docs/guides/testing

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Inheritance**
  - URL: /docs/concepts/inheritance

- **Repository Pattern**
  - URL: /docs/packages/drizzle

- **Testing Strategies**
  - URL: /docs/guides/testing

### What is Dependency Injection?

### Basic Injection with @Inject

### Injection with Expressions

### Strategy Pattern with @Strategy

### Lifecycle Hooks

### Service Scopes

### Injecting into Different Components

### Reaching the container from outside

- **`@OnStart`**
  - URL: /docs/concepts/lifecycle

- **Inheritance**
  - URL: /docs/concepts/inheritance

### Complete Example

### Best Practices

### Related Documentation

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Services**
  - URL: /docs/concepts/services

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **Service Scopes**
  - URL: /docs/concepts/services#service-scopes

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware**
  - URL: /docs/concepts/middleware

### `@OnStart`

### `@OnStop`

### Where the hooks sit

### Ordering rules

- **Inheritance**
  - URL: /docs/concepts/inheritance

### Failure policy

### Who takes part

### Stopping the server

### Signal handling

### `keepAlive` and headless workers

### Health probes

### `server.resolve()`

### Upgrading from 0.9.x

### Related

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection#lifecycle-hooks

- **PostProcessor**
  - URL: /docs/concepts/post-processor

- **Microservices**
  - URL: /docs/concepts/microservices#graceful-shutdown

- **Inheritance**
  - URL: /docs/concepts/inheritance

- **Scheduled Tasks**
  - URL: /docs/concepts/scheduled-tasks

### What is Middleware?

### Creating Middleware

### Middleware Levels

### Common Middleware Patterns

### Built-in Middleware

### Middleware with Dependency Injection

### Middleware Execution Order

### Stopping Middleware Chain

### Best Practices

### Related Documentation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Validation**
  - URL: /docs/concepts/validation

- **Configuration**
  - URL: /docs/guides/configuration

- **Validation**
  - URL: /docs/concepts/validation

- **Context API**
  - URL: /docs/concepts/context

- **Configuration**
  - URL: /docs/guides/configuration

### What is Context?

### Quick Start

### Core Properties

### Request Data Methods

### Response Methods

### Cookie Management

### State Management

### WebSocket Support

### Streaming

### Advanced Methods

### Common Patterns

### Utility Methods

### Adapter-Specific Features

### API Reference

### Best Practices

### Related Documentation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware**
  - URL: /docs/concepts/middleware

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Hono Adapter**
  - URL: /docs/adapters/hono

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Error Handling**
  - URL: /docs/guides/error-handling

### Installation

### Why Use Validation?

### Quick Start

### ValidationService API

### Validation Hooks

### Validation Error Responses

### Integration with Controllers

### Zod Schema Definition

### Asena-Specific Best Practices

### ValidationSchema Types

### Complete Example

### Related Documentation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware**
  - URL: /docs/concepts/middleware

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Context API**
  - URL: /docs/concepts/context

- **Zod Documentation**
  - URL: https://zod.dev

- **Middleware**
  - URL: /docs/concepts/middleware

- **Error Handling**
  - URL: /docs/guides/configuration

- **Context API**
  - URL: /docs/concepts/context

### Quick Start

### Configuration

### Lifecycle Hooks

### Examples

### Best Practices

### Common Use Cases

### Troubleshooting

### Related

- **Controllers**
  - URL: /docs/concepts/controllers.md

- **Middleware**
  - URL: /docs/concepts/middleware.md

- **Context**
  - URL: /docs/concepts/context.md

### Creating a WebSocket Service

### WebSocket Lifecycle Methods

### Socket API

### Built-in Room Management

### Broadcasting

### WebSocket Middleware

### Using WebSocket in Services

### Real-World Example: Notification System

### Error Handling

### Multi-Pod WebSocket

### Best Practices

### Breaking Circular Dependencies with Ulak

### Related Documentation

- **Ulak - WebSocket Messaging System**
  - URL: /docs/concepts/ulak

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Hono Adapter**
  - URL: /docs/adapters/hono

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

### Key Features

### Quick Start

### Core Features

### Decorators

### Event Patterns

### Advanced Usage

### Examples

### Best Practices

### Troubleshooting

### Related

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection.md

- **Inheritance**
  - URL: /docs/concepts/inheritance.md

- **Services**
  - URL: /docs/concepts/services.md

- **Ulak**
  - URL: /docs/concepts/ulak.md

### Key Features

### Quick Start

### Headless Mode

### Delivery Semantics

- **start hooks run from `server.start()`**
  - URL: /docs/concepts/lifecycle#onstart

### Multiple Named Transports

### Graceful Shutdown

### InMemoryTransport (Development & Testing)

### Distributed Tracing

### Error Handling

### Writing a Custom Transport

### Comparison with the In-Process Event System

### Related

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Inheritance**
  - URL: /docs/concepts/inheritance

### The Problem

### The Solution

### Getting Started

### Three Ways to Use Ulak

### API Reference

### Error Handling

### Lifecycle Management

### Best Practices

### Testing

### Advanced Examples

### Migration Guide

### Type Definitions

### See Also

- **WebSocket**
  - URL: /docs/concepts/websocket.md

- **Microservices**
  - URL: /docs/concepts/microservices.md

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection.md

- **Services**
  - URL: /docs/concepts/services.md

- **MockComponent**
  - URL: /docs/testing/mock-component.md

### Quick Start

### @Schedule Decorator

### AsenaSchedule Interface

### Dependency Injection

### CronRunner Service

### Real-World Examples

### Best Practices

### Related Documentation

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Configuration**
  - URL: /docs/guides/configuration

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Redis**
  - URL: /docs/packages/redis

### Quick Start

### @FrontendController Decorator

### @Page Decorator

### How It Works

### Multiple Pages

### HTML File Structure

### FrontendController vs Controller

### Production Build

### Best Practices

### Related Documentation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Static File Serving**
  - URL: /docs/concepts/static-files

- **Middleware**
  - URL: /docs/concepts/middleware

- **Configuration**
  - URL: /docs/guides/configuration

- **Controllers**
  - URL: /docs/concepts/controllers

- **Static File Serving**
  - URL: /docs/concepts/static-files

- **Middleware**
  - URL: /docs/concepts/middleware

### When to Use PostProcessor

### Quick Start

### ComponentPostProcessor Interface

### @PostProcessor Decorator

### Lifecycle

- **`@OnStart`**
  - URL: /docs/concepts/lifecycle

### Two Modes of Operation

### Real-World Example: OpenAPI PostProcessor

### Bootstrap Priority

### Dependency Injection in PostProcessors

### @OnStart vs @PostProcessor

### Best Practices

### Related Documentation

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **OpenAPI**
  - URL: /docs/packages/openapi

- **Configuration**
  - URL: /docs/guides/configuration

- **OpenAPI**
  - URL: /docs/packages/openapi

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Services**
  - URL: /docs/concepts/services

### The rule, in one sentence

### What is inherited

### `@Implements` is inherited; the component name is not

### Guards follow the routes they protect

### How overrides resolve

### Conflicts that fail the build

### Inherited handlers are logged at startup

### Practical pattern: a shared platform package

### Related

- **Controllers**
  - URL: /docs/concepts/controllers

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Microservices**
  - URL: /docs/concepts/microservices

- **Event System**
  - URL: /docs/concepts/event-system

- **Drizzle**
  - URL: /docs/packages/drizzle

### What is an Adapter?

### Available Adapters

### Performance Comparison

### Feature Comparison

### Choosing the Right Adapter

### Quick Start Comparison

### Context API

### Migration Between Adapters

### Advanced Adapter Configuration

### Creating Custom Adapters

### Recommendations

### Related Documentation

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Hono Adapter**
  - URL: /docs/adapters/hono

- **Context API**
  - URL: /docs/concepts/context

- **Middleware Guide**
  - URL: /docs/concepts/middleware

- **Ergenecore features**
  - URL: /docs/adapters/ergenecore

- **Hono adapter usage**
  - URL: /docs/adapters/hono

- **Context API**
  - URL: /docs/concepts/context

### What is Ergenecore?

### Why Choose Ergenecore?

### Installation

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

- **Zod**
  - URL: https://zod.dev

### Quick Start

### Factory Functions

### Built-in Middleware

### Performance & Architecture

### Ergenecore-Specific Features

### Best Practices

### Troubleshooting

### Related Documentation

- **Adapters Overview**
  - URL: /docs/adapters/overview

- **Hono Adapter**
  - URL: /docs/adapters/hono

- **Context API**
  - URL: /docs/concepts/context

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Configuration**
  - URL: /docs/guides/configuration

- **Context API**
  - URL: /docs/concepts/context

- **Middleware patterns**
  - URL: /docs/concepts/middleware

- **Validation strategies**
  - URL: /docs/concepts/validation

### What is Hono Adapter?

### Why Choose Hono Adapter?

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

- **Hono**
  - URL: https://hono.dev

- **Zod**
  - URL: https://zod.dev

### Quick Start

### Factory Function

### Built-in Middleware

### Hono-Specific Features

### Migrating from Standalone Hono

### Testing

### Best Practices

### Troubleshooting

### Related Documentation

- **Adapters Overview**
  - URL: /docs/adapters/overview

- **Ergenecore Adapter**
  - URL: /docs/adapters/ergenecore

- **Context API**
  - URL: /docs/concepts/context

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **Testing Guide**
  - URL: /docs/guides/testing

- **Hono Documentation**
  - URL: https://hono.dev/

- **Context API**
  - URL: /docs/concepts/context

- **Middleware patterns**
  - URL: /docs/concepts/middleware

- **@Override decorator**
  - URL: /docs/concepts/middleware#override-decorator

### Installation

- **Bun**
  - URL: https://bun.sh

### Quick Start

### Using Logger in Your Application

### AsenaLogger API

### Log Levels

### Output Format

### Real-World Examples

### Custom Winston Configuration

### Best Practices

### Related Documentation

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Configuration**
  - URL: /docs/guides/configuration

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Winston Documentation**
  - URL: https://github.com/winstonjs/winston

- **Error Handling**
  - URL: /docs/guides/configuration

- **Middleware patterns**
  - URL: /docs/concepts/middleware

- **Services architecture**
  - URL: /docs/concepts/services

### Features

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

- **drizzle-orm**
  - URL: https://orm.drizzle.team

### Supported Databases

### Quick Start

### @Database Decorator API

### @Repository Decorator API

### @Drizzle Decorator API

### Database Configuration

### Repository Methods

### Advanced Queries

### Multiple Databases

### Transactions

### Best Practices

### Related Documentation

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Inheritance**
  - URL: /docs/concepts/inheritance

- **Configuration**
  - URL: /docs/guides/configuration

- **Drizzle ORM Documentation**
  - URL: https://orm.drizzle.team/

- **Services**
  - URL: /docs/concepts/services

- **Testing**
  - URL: /docs/guides/testing

### Features

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

- **Zod**
  - URL: https://zod.dev

### Quick Start

### How It Works

### Validator Mapping

### @Hidden Decorator

### Configuration

### Swagger UI

### Best Practices

### Related Documentation

- **Validation**
  - URL: /docs/concepts/validation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware**
  - URL: /docs/concepts/middleware

- **Configuration**
  - URL: /docs/guides/configuration

- **request validation**
  - URL: /docs/concepts/validation

- **Controllers**
  - URL: /docs/concepts/controllers

- **Middleware patterns**
  - URL: /docs/concepts/middleware

### Features

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

### Quick Start

### How Auto-Tracing Works

### OtelService API

### OtelTracingMiddleware

### Shutdown

### Configuration

### Sampling

### Route Exclusion

### Outgoing Request Context Propagation

### Microservice Messaging Instrumentation

### Testing

### Best Practices

### Related Documentation

- **PostProcessor**
  - URL: /docs/concepts/post-processor

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Configuration**
  - URL: /docs/guides/configuration

- **Middleware**
  - URL: /docs/concepts/middleware

- **Services**
  - URL: /docs/concepts/services

- **Sampling**
  - URL: #sampling

### Features

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

### Quick Start

### Adapter Selection

### API Reference

### Configuration

### Multi-Pod WebSocket Transport

### Microservice Transport (Redis Streams)

- **write idempotent handlers**
  - URL: /docs/concepts/microservices#idempotent-handlers

- **Reply loss across an outage**
  - URL: #reply-loss-across-an-outage

### Best Practices

### Related Documentation

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Microservices**
  - URL: /docs/concepts/microservices

- **Configuration**
  - URL: /docs/guides/configuration

- **Services**
  - URL: /docs/concepts/services

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **WebSocket**
  - URL: /docs/concepts/websocket

- **multi-pod transport**
  - URL: /docs/concepts/websocket#multi-pod-websocket

- **Services**
  - URL: /docs/concepts/services

- **microservice layer**
  - URL: /docs/concepts/microservices

### Features

### Installation

- **Bun**
  - URL: https://bun.sh

- **@asenajs/asena**
  - URL: https://github.com/AsenaJs/Asena

- **kafkajs**
  - URL: https://kafka.js.org

### Quick Start

### Service Client

### Microservice Transport

- **write idempotent handlers**
  - URL: /docs/concepts/microservices#idempotent-handlers

### External Topics (interop)

- **messageId dedup**
  - URL: /docs/concepts/microservices#idempotent-handlers

### Best Practices

### Troubleshooting

### Client Roadmap

- **bun#4290**
  - URL: https://github.com/oven-sh/bun/issues/4290

- **broker-tracked delivery attempts**
  - URL: #delivery-attempts

### Related Documentation

- **Microservices**
  - URL: /docs/concepts/microservices

- **Redis**
  - URL: /docs/packages/redis

- **OpenTelemetry**
  - URL: /docs/packages/opentelemetry

### What is Asena CLI?

### Key Features

### Getting Started

### Documentation

- **Installation**
  - URL: /docs/cli/installation

- **Commands**
  - URL: /docs/cli/commands

- **Configuration**
  - URL: /docs/cli/configuration

- **Examples**
  - URL: /docs/cli/examples

### Requirements

### Related Resources

- **Get Started Guide**
  - URL: /docs/get-started

- **Adapters Overview**
  - URL: /docs/adapters/overview

- **CLI Examples**
  - URL: /docs/cli/examples

- **Install the CLI**
  - URL: /docs/cli/installation

- **Learn CLI Commands**
  - URL: /docs/cli/commands

- **Try the Examples**
  - URL: /docs/cli/examples

### Prerequisites

- **Bun runtime**
  - URL: https://bun.sh

### Install Asena CLI

### Verify Installation

### Update Asena CLI

### Uninstall

### Troubleshooting

### Next Steps

- **Create your first project**
  - URL: /docs/cli/examples

- **Learn CLI commands**
  - URL: /docs/cli/commands

- **Configure your project**
  - URL: /docs/cli/configuration

- **CLI Overview**
  - URL: /docs/cli/overview

- **CLI Commands**
  - URL: /docs/cli/commands

- **Get Started Guide**
  - URL: /docs/get-started

### Installation

### asena create

### asena generate

- **Suffix Configuration**
  - URL: /docs/cli/suffix-configuration

### asena dev start

### asena build

### asena init

### Command Reference

### Related Documentation

- **Configuration**
  - URL: /docs/cli/configuration

- **Suffix Configuration**
  - URL: /docs/cli/suffix-configuration

- **CLI Examples**
  - URL: /docs/cli/examples

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **WebSocket**
  - URL: /docs/concepts/websocket

- **CLI Configuration**
  - URL: /docs/cli/configuration

- **CLI Examples**
  - URL: /docs/cli/examples

- **Controllers**
  - URL: /docs/concepts/controllers

### defineConfig Helper

### Configuration Options

### Default Configuration

### Configuration Properties

### Build Options Reference

### Environment-Specific Configuration

### Advanced Build Options

### Configuration Examples

### Bun Bundler Options

### Best Practices

### Troubleshooting

### .asena/config.json

### Related Documentation

- **CLI Commands**
  - URL: /docs/cli/commands

- **Suffix Configuration**
  - URL: /docs/cli/suffix-configuration

- **CLI Examples**
  - URL: /docs/cli/examples

- **Deployment**
  - URL: /docs/guides/deployment

- **Bun Bundler**
  - URL: https://bun.com/docs/bundler

- **CLI Commands**
  - URL: /docs/cli/commands

- **Deployment**
  - URL: /docs/guides/deployment

- **CLI Examples**
  - URL: /docs/cli/examples

### What are Suffixes?

### Configuration File

### Default Suffixes

### Configuration Options

### Examples

### Best Practices

### Configuration Comparison

### Manual Configuration

### Related Commands

### Related Documentation

- **CLI Configuration**
  - URL: /docs/cli/configuration

- **CLI Commands**
  - URL: /docs/cli/commands

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **CLI Commands**
  - URL: /docs/cli/commands

- **Controllers**
  - URL: /docs/concepts/controllers

### Prerequisites

- **Bun runtime**
  - URL: https://bun.sh

### Step 1: Install Asena CLI

### Step 2: Create a New Project

### Step 3: Verify Project Setup

### Step 4: Create a Controller

### Step 5: Create a Service

### Step 6: Build for Production

### Project Structure

### Next Steps

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **Middleware**
  - URL: /docs/concepts/middleware

- **Database integration**
  - URL: /docs/packages/drizzle

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Production**
  - URL: /docs/guides/deployment

- **CLI Commands**
  - URL: /docs/cli/commands

- **CLI Configuration**
  - URL: /docs/cli/configuration

- **Get Started Guide**
  - URL: /docs/get-started

- **Adapters**
  - URL: /docs/adapters/overview

### Quick Start

### API Reference

### serveOptions() Method

### onError() Method

### onNotFound() Method

### globalMiddlewares() Method

### transport() Method

### Complete Example

### Technical Details

- **`@OnStart`**
  - URL: /docs/concepts/lifecycle

### Best Practices

### Troubleshooting

### Related Documentation

- **Middleware**
  - URL: /docs/concepts/middleware

- **Error Handling**
  - URL: /docs/guides/error-handling

- **WebSocket**
  - URL: /docs/concepts/websocket

- **CLI Configuration**
  - URL: /docs/cli/configuration

- **Middleware patterns**
  - URL: /docs/concepts/middleware

- **Error Handling**
  - URL: /docs/guides/error-handling

- **WebSocket**
  - URL: /docs/concepts/websocket

### Why Error Handling Matters

### Philosophy

### Basic Error Handling

### Global Error Handler

### Custom Error Classes

### Not Found

### Validation Errors

### Best Practices

### Common Patterns

### Related

- **Middleware**
  - URL: /docs/concepts/middleware

- **Validation**
  - URL: /docs/concepts/validation

- **Logger Package**
  - URL: /docs/packages/logger

- **Context API**
  - URL: /docs/concepts/context

### Quick Start

### Graceful Shutdown and Probes

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle#signal-handling

- **Health probes**
  - URL: /docs/concepts/lifecycle#health-probes

### Related Documentation

- **CLI Build Command**
  - URL: /docs/cli/commands#build

- **CLI Configuration**
  - URL: /docs/cli/configuration

- **Server Configuration**
  - URL: /docs/guides/configuration

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

### Bun Test Runner

### Automatic Dependency Mocking

### Two Levels of Testing

### Import Path

### What You Can Test

### Main Testing Utilities

### Advanced Features

### How It Works

### Next Steps

- **MockComponent API**
  - URL: /docs/testing/mock-component

- **Examples**
  - URL: /docs/testing/examples

- **Bun Test Documentation**
  - URL: https://bun.sh/docs/cli/test

### Quick Start

### API Reference

- **MockComponentOptions**
  - URL: #mockcomponentoptions

### Advanced Usage Patterns

### Technical Details

### Related

- **Testing Overview**
  - URL: /docs/testing/overview

- **createTestApp**
  - URL: /docs/testing/test-app

- **createWebTest**
  - URL: /docs/testing/web-test

- **Examples**
  - URL: /docs/testing/examples

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Bun Test Documentation**
  - URL: https://bun.sh/docs/cli/test

### Options

### Replacing components with mocks

### Fluent HTTP assertions

### Cleanup

### Dispatch modes

### The container

### Known behaviours

- **`@OnStart` and `@OnStop` run for real.**
  - URL: /docs/concepts/lifecycle

### Related

- **Component Lifecycle**
  - URL: /docs/concepts/lifecycle

- **createWebTest**
  - URL: /docs/testing/web-test

- **MockComponent API**
  - URL: /docs/testing/mock-component

- **Testing Overview**
  - URL: /docs/testing/overview

### Options

### What runs for real

### The `mocks` object

### Mock shape

### Promoting a mock back to the real thing

### Explicit overrides

### Known behaviours

- **start hook**
  - URL: /docs/concepts/lifecycle

### Related

- **createTestApp**
  - URL: /docs/testing/test-app

- **MockComponent API**
  - URL: /docs/testing/mock-component

- **Testing Overview**
  - URL: /docs/testing/overview

### Testing Controllers

### Testing Services

### Testing WebSockets

### Testing Middleware

### Integration Testing Patterns

### Related

- **Testing Overview**
  - URL: /docs/testing/overview

- **MockComponent API**
  - URL: /docs/testing/mock-component

- **createTestApp**
  - URL: /docs/testing/test-app

- **createWebTest**
  - URL: /docs/testing/web-test

- **Dependency Injection**
  - URL: /docs/concepts/dependency-injection

- **Controllers**
  - URL: /docs/concepts/controllers

- **Services**
  - URL: /docs/concepts/services

- **WebSocket**
  - URL: /docs/concepts/websocket

- **Middleware**
  - URL: /docs/concepts/middleware

## Additional Resources (Optional)

### Step 7: Add Middleware (Optional)

## How to Use This Skill

Reference these resources when working with Testing Examples.