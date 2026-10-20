---
name: deserialization-safe-formats
description: >
  Defensive guidance for safe interchange formats and deserializers: prefer JSON, Protobuf,
  and schema-bound codecs over pickle, native Java serialization, BinaryFormatter-class APIs,
  and unrestricted YAML load. Use when choosing or hardening serializers, reviewing untrusted
  payload parsers, configuring allowlists/ObjectInputFilters/safe loaders, migrating off native
  object graphs, or remediating insecure deserialization without exploit gadgets.
---

# Deserialization Safe Formats

## Scope And Authorization

- **In scope:** Owned services and libraries; authorized remediation of deserialization findings.
- **Out of scope:** Using “safe format” work as cover to weaken authZ; deploying untested migrations to prod without rollback.
- Prefer dual-read/dual-write or versioned message formats during migration.
- Redact production payloads used in test fixtures.
- Pair with `deserialization-insecure` / `deserialization-gadget-awareness` for assessment; `code-quality-standards` for implementation.

## When To Use

- Replacing `pickle`, Java `Serializable` wire format, `BinaryFormatter`, `Marshal`, or `unserialize` for untrusted data.
- Choosing Protobuf/JSON Schema/Avro/Thrift for new APIs and queues.
- Hardening interim loaders with allowlists and safe YAML/JSON settings.
- Defining org standards: “no native object serialization across trust boundaries.”

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Finding sinks / pentest methodology | `deserialization-insecure` |
| Gadget chain awareness | `deserialization-gadget-awareness` |
| JSON Schema design detail | `json-schema-design` |
| Protobuf/gRPC reverse engineering | `protobuf-grpc-reverse-engineering` |
| XXE when using XML | `xxe-xml-external-entity` |
| Code quality baseline | `code-quality-standards` |

## Format preference (untrusted data)

| Preference | Formats / APIs | Notes |
| --- | --- | --- |
| Preferred | JSON + schema validation; Protobuf; often Avro/Thrift with schema registry | Explicit fields; no code execution on parse |
| Careful | XML with hardened parser; YAML `safe_load` only | Disable XXE/Dyna; no arbitrary tags |
| Avoid for untrusted | `pickle`, `shelve`, Java serialization, `BinaryFormatter`, `Marshal.load`, PHP `unserialize`, `yaml.load` unsafe, `ObjectInputStream` | Gadget / code exec risk |
| Not a silver bullet | JSON with polymorphic type recovery (`@class`, default typing) | Can reintroduce gadget-like behavior |

## Workflow

### 1. Confirm scope and success criteria

1. List channels: HTTP APIs, cookies, sessions, message buses, caches, files, RPC.
2. Success: untrusted channels use schema-bound formats; dangerous APIs gated or gone; tests prove rejects.
3. Rollback: keep readers for old format during migration window with expiry.

### 2. Inventory unsafe serializers

```bash
rg -n "pickle\\.loads|ObjectInputStream|BinaryFormatter|unserialize\\(|Marshal\\.load|yaml\\.load\\(|enableDefaultTyping|JsonTypeInfo|ObjectMapper.*activateDefaultTyping" .
```

1. Classify each: untrusted / trusted-same-process / legacy offline only.
2. Trusted-same-process still risky if memory corruption or multi-tenant—prefer safe formats everywhere practical.

### 3. Select target format per channel

| Channel | Typical choice |
| --- | --- |
| Public HTTP API | JSON + OpenAPI/JSON Schema or Protobuf |
| Service mesh RPC | Protobuf/gRPC |
| Queue events | Avro/Protobuf + schema registry; version field |
| Browser state | Opaque server-side session id; or signed JWT *without* embedded code graphs |
| Config files | JSON/TOML/YAML safe_load; never pickle configs from users |

### 4. Implement safe decoding patterns

```python
# Python — good
import json
from pydantic import BaseModel, ValidationError

class Order(BaseModel):
    id: str
    qty: int

def parse_order(blob: str) -> Order:
    return Order.model_validate_json(blob)

# Python — bad
# pickle.loads(blob)
# yaml.load(blob)  # use yaml.safe_load if YAML required
```

```java
// Java — prefer Jackson/Gson into concrete DTOs without default typing
// objectMapper.readValue(json, OrderDto.class);
// Avoid ObjectInputStream on untrusted bytes
// If legacy temporary: ObjectInputFilter allowlist of DTO names only
```

```csharp
// Prefer System.Text.Json with explicit types
// var order = JsonSerializer.Deserialize<OrderDto>(json);
// Do not use BinaryFormatter for untrusted data
```

```php
// Prefer json_decode with assoc + schema validation
// Avoid unserialize on user input; if unavoidable: allowed_classes options carefully
```

```yaml
# YAML: only safe loaders
# Python: yaml.safe_load
# Reject tags that construct objects
```

### 5. Interim hardening when migration is slow

1. **Allowlist types** (Java JEP 290 / `ObjectInputFilter`; .NET serialization binders).
2. **HMAC/AEAD** integrity on blobs—helps tampering, **not** a substitute if decrypt-then-unsafe-deserialize still runs attacker graphs after key theft or confused deputy.
3. **Strip polymorphic type info** from JSON mappers.
4. **Network egress** restrictions reduce some gadget impact; still migrate formats.
5. Document expiry date for interim controls.

### 6. Migration steps

1. Introduce v2 schema; producers dual-write or switch with feature flag.
2. Consumers accept v1+v2; metrics on v1 rate.
3. Block v1 after threshold; remove unsafe code paths; add CI `rg` guardrails.
4. Rotate any keys that protected old blobs if compromise suspected.

### 7. Verify

```bash
# CI guardrail examples
! rg -n "pickle\\.loads\\(|BinaryFormatter|ObjectInputStream" src/ || echo "forbidden API"
# Contract tests: unexpected fields / oversized payloads rejected
pytest tests/test_order_schema.py
```

1. Re-test former attack path from `deserialization-insecure`.
2. Fuzz length/limits to avoid DoS (billion laughs in XML/YAML—configure parser limits).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| New API | Protobuf/JSON DTO | Pickle over HTTP |
| YAML config | `safe_load` | `yaml.load` + user file |
| Jackson | Concrete types | Default typing enabled |
| Migration | Versioned dual-read | Hard cut without rollback |
| Interim | Allowlist + expiry | Denylist forever |
| Crypto | AEAD + safe format | Encrypt pickle and call it fixed |

## Output Checklist

- [ ] Unsafe serializer inventory complete
- [ ] Target format chosen per channel
- [ ] Schema/validation implemented
- [ ] Polymorphic typing disabled where applicable
- [ ] Interim filters documented with expiry if needed
- [ ] Migration/dual-read plan executed or ticketed
- [ ] CI guards against forbidden APIs
- [ ] Retest of old sink path clean
- [ ] Parser resource limits set
- [ ] `code-quality-standards` applied

## Rules

- Safe structure + schema validation for all untrusted inputs.
- Encryption does not make native deserialize safe.
- Prefer deleting unsafe APIs over maintaining gadget allowlists forever.
- XML/YAML still need parser hardening (XXE, aliases, size limits).
- Focus on defensive formats and migration; assessment is neighbor skills.
