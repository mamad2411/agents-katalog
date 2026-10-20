---
name: asyncapi-specs-basics
description: >
  AsyncAPI specifications for owned event-driven APIs: channels, operations, messages,
  schemas (JSON Schema/Avro), servers/bindings (Kafka, AMQP, MQTT, WebSocket), and
  versioning. Use when documenting or reviewing pub/sub contracts — not for attacking
  message brokers you do not operate.
---

# AsyncAPI Specs Basics

## Scope And Authorization

- **In scope:** Event APIs, brokers, and gateways you own or document under authorization.
- **Out of scope:** Unauthorized discovery/flooding of third-party brokers.
- Treat credentials in `servers` as secrets — use variables, not plaintext passwords in git.
- Prefer contract-first or contract-alongside for consumers; keep examples redaction-safe.
- Pair codegen/tooling with `code-quality-standards`; Avro evolution with `avro-compat-rules`.

## When To Use

- Writing `asyncapi.yaml` for Kafka/Rabbit/NATS/MQTT/WebSocket APIs.
- Aligning producers/consumers on message payload and headers.
- Generating docs, types, or stubs from AsyncAPI.
- Reviewing channel naming, security schemes, and bindings.
- Versioning event contracts across breaking changes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| OpenAPI/REST only | API docs skill / OpenAPI skill |
| Avro FULL/FORWARD/BACKWARD detail | `avro-compat-rules` |
| Broker security misconfig | Redis/Kafka security skills as applicable |
| WebSocket security testing | `websocket-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Meaning |
| --- | --- |
| AsyncAPI version | Spec version (2.x / 3.x — field shapes differ) |
| servers | Broker URLs + protocol + security |
| channels | Topics/queues/routes events flow through |
| operations | publish/subscribe (2.x) or send/receive (3.x) |
| messages | Payload + headers + content type |
| schemas | JSON Schema, Avro, Protobuf refs |
| bindings | Protocol-specific metadata (kafka key, amqp exchange) |

## Minimal AsyncAPI 2.6 Sketch

```yaml
asyncapi: 2.6.0
info:
  title: Orders Events
  version: 1.1.0
  description: Owned order domain events
defaultContentType: application/json
servers:
  production:
    url: kafka://kafka.example.internal:9092
    protocol: kafka
    description: Internal cluster
    security:
      - saslScram: []
channels:
  order.created.v1:
    description: Fired when an order is created
    subscribe:
      operationId: onOrderCreated
      summary: Consumers react to new orders
      message:
        $ref: '#/components/messages/OrderCreated'
    bindings:
      kafka:
        topic: order.created.v1
        partitions: 12
components:
  securitySchemes:
    saslScram:
      type: scramSha256
  messages:
    OrderCreated:
      name: OrderCreated
      title: Order created
      contentType: application/json
      headers:
        type: object
        properties:
          correlation_id:
            type: string
            format: uuid
      payload:
        $ref: '#/components/schemas/OrderCreatedPayload'
  schemas:
    OrderCreatedPayload:
      type: object
      required: [order_id, customer_id, total_cents, currency]
      additionalProperties: false
      properties:
        order_id:
          type: string
          format: uuid
        customer_id:
          type: string
        total_cents:
          type: integer
          minimum: 0
        currency:
          type: string
          enum: [USD, EUR]
```

## Workflow

### 1. Confirm scope and success criteria

1. Record brokers, protocols, domains, consumers, ownership.
2. Success: published AsyncAPI validates; channels match real topics; schemas enforce required fields; security schemes documented without secret leakage.
3. Choose AsyncAPI major version team standard (2.x vs 3.x).

### 2. Inventory real events

```bash
# Examples — adjust to broker
kafka-topics.sh --list --bootstrap-server "$BOOTSTRAP"
# or rabbit
rabbitmqctl list_queues name
# existing docs
find . -name 'asyncapi*.y*ml'
```

1. List producers, consumers, and message types per channel.
2. Capture sample payloads (redact PII).
3. Note headers used for tracing/auth.

### 3. Baseline

1. If OpenAPI exists for related HTTP, map dual-protocol entities carefully.
2. Export current schemas (Avro subjects, JSON Schema registry).
3. Validate samples against draft schemas.

### 4. Author and structure the spec

1. One AsyncAPI file per bounded context (or modular `$ref` structure).
2. Stable channel names; include version suffix in topic or payload `schema_version`.
3. Document message examples under `examples` with fake data.
4. Bindings: set kafka keys, partitions guidance, amqp routing keys as needed.
5. Security: SASL, mTLS, OAuth2 client credentials — reference vault-managed secrets via variables:

```yaml
servers:
  production:
    url: kafka://{host}:{port}
    protocol: kafka
    variables:
      host:
        default: kafka.example.internal
      port:
        default: "9092"
```

**Lint/validate:**

```bash
npx -y @asyncapi/cli validate asyncapi.yaml
# or studio for review
npx -y @asyncapi/cli generate fromTemplate asyncapi.yaml @asyncapi/html-template -o dist/asyncapi
```

### 5. Verify with evidence

```bash
npx -y @asyncapi/cli validate asyncapi.yaml
# Contract test: sample payload vs schema (ajv / registry compatibility)
# Consumer can deserialize production sample (lab) successfully
```

1. Diff topic list vs channels — no silent orphans without owners.
2. Breaking change process: new channel version or compat mode (see Avro skill).
3. Redact secrets from published HTML docs.

### 6. Observe and harden

1. CI gate: `asyncapi validate` on PR.
2. Schema registry compatibility checks for Avro/JSON.
3. Deprecation policy for old channels.

### 7. Hand off

1. Publish docs URL; CODEOWNERS for the spec.
2. Onboarding: how to add a message + example + consumer.
3. Cross-link broker ACLs and `avro-compat-rules`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Channels | Explicit versioned topics | One mega `events` dump |
| Schemas | required + additionalProperties false | free-form object only |
| Secrets | variables + vault | password in servers.url |
| Examples | realistic fake data | live customer payloads |
| Evolution | compat policy | silent field reuse/type change |
| Tooling | CI validate | wiki prose only |

## Output Checklist

- [ ] Brokers, protocols, domains recorded
- [ ] Channels/operations match production topics
- [ ] Messages and schemas complete with required fields
- [ ] Security schemes documented without secret leakage
- [ ] Bindings filled for primary protocol
- [ ] `asyncapi validate` passes in CI
- [ ] Examples redacted; docs published
- [ ] Versioning/compat policy linked
- [ ] `code-quality-standards` applied if codegen ships

## Rules

- Owned event systems only.
- Specs are contracts — breaking changes need consumer communication.
- Never commit broker passwords or live PII samples.
- Prefer modular `$ref` over single unmaintainable file as systems grow.
- Focus on AsyncAPI modeling; detailed Avro compat and broker exploits elsewhere.
