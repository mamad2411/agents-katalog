---
name: flatbuffers-basics
description: >
  Use FlatBuffers for zero-copy serialization: schema (.fbs) design, codegen, builder
  vs table access, versioning/compatibility, and security bounds on untrusted buffers.
  Use when choosing FlatBuffers vs Protobuf, implementing owned game/mobile/telemetry
  pipelines, or reviewing parsers that trust file/network FlatBuffer payloads.
---

# FlatBuffers Basics

## Scope And Authorization

- **In scope:** schemas and parsers in systems you own; authorized protocol reviews.
- **Out of scope:** crafting malicious buffers against third-party services without permission.
- Treat network-sourced buffers as untrusted—verify size and nesting limits.
- Redact production payloads containing PII from samples.
- Pair implementation with `code-quality-standards`.

## When To Use

- Need **zero-copy** reads of structured binary (games, mobile IPC, high-FPS telemetry).
- Designing `.fbs` schemas with `table`/`struct`, unions, vectors.
- Evolving schemas without breaking old readers (defaults, new fields).
- Comparing to Protobuf/JSON for performance and safety tradeoffs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Protobuf/gRPC schema RE | `protobuf-grpc-reverse-engineering` |
| General protocol RE | `protocol-reverse-engineering` |
| gRPC security | related API skills |
| Cap’n Proto / other | catalog-specific if present |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Schema | `.fbs` compiled by `flatc` to language code |
| struct | Fixed layout, no vtable; good for small inline data |
| table | Optional fields, vtable, forward/back compat patterns |
| Builder | Serialize into buffer; finish root |
| Accessor | Read without full parse/unpack (zero-copy) |
| Object API | Optional convenience unpack—copies; not always zero-copy |

## FlatBuffers vs Protobuf (quick)

| Concern | FlatBuffers | Protobuf |
| --- | --- | --- |
| Access | Random access / zero-copy | Decode to objects typically |
| Size | Often larger headers/vtables tradeoffs | Dense varints |
| Schema evolution | Add fields with defaults carefully | Field numbers discipline |
| RPC ecosystem | Less central than gRPC+proto | gRPC native |
| Untrusted input | Manual verifier essential | Parser robustness still required |

## Workflow

### 1. Confirm scope and success criteria

1. Producers/consumers languages; max message size; trust boundary (file, IPC, network).
2. Success: schema documented; codegen in CI; verifier used on untrusted data; compat test matrix.
3. Decide if Object API allowed (simplicity vs copies).

### 2. Design schema

```fbs
// example.fbs
namespace app.events;

table Player {
  id:ulong;
  name:string;
  score:int = 0;
  inventory:[Item];
}

table Item {
  def_id:uint;
  qty:ushort = 1;
}

root_type Player;
```

```bash
flatc --python --go --cpp -o gen example.fbs
```

1. Prefer `table` for evolvable messages; `struct` for tight fixed records.
2. Avoid huge nested vectors without size budgets.
3. Document `root_type` and file identifier if used (`file_identifier`).

### 3. Implement build and read paths

```python
# Illustrative Python-style builder/access — APIs vary by language binding
import flatbuffers
# from gen.example import Player, Item
# builder = flatbuffers.Builder(1024)
# ... create strings/vectors, Player.Start/Add/End, builder.Finish(root)
# buf = builder.Output()
# player = Player.Player.GetRootAs(buf, 0)
# player.Name()
```

1. Keep builders short-lived; reuse carefully if threadlocal.
2. Do not hand-edit generated code.

### 4. Secure untrusted buffers

```text
Before GetRootAs:
  - enforce max buffer length
  - run Verifier / equivalent with max depth and table count
  - reject on verify failure
Never trust length fields without verifier
```

1. Fuzz parsers with malformed offsets (owned harness)—see `fuzzing-libfuzzer-basics` for binary fuzzing depth.
2. Align with `file-access-vuln` if buffers map files.

### 5. Versioning and compatibility

1. Add new optional fields only; do not reuse field ids/slots carelessly.
2. Golden-file tests: old buffer → new reader; new buffer → old reader (if required).
3. Consider explicit `schema_version` field for logic changes that defaults cannot express.

### 6. Verify with evidence

```bash
flatc --version
# Roundtrip test in CI
# Verifier rejects truncated buffer
```

| Test | Expect |
| --- | --- |
| Roundtrip | Field equality |
| Truncation | Verify fail |
| Huge declared vector | Reject under limits |
| Old payload | Still readable |

### 7. Hand off

1. Publish `.fbs` as source of truth; codegen step in README.
2. Document max sizes and verifier settings.
3. Apply `code-quality-standards` for wrappers around generated code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Untrusted I/O | Verifier + size cap | `GetRootAs` on network bytes raw |
| Schema | Versioned `.fbs` in git | Only checked-in generated code drift |
| Evolution | Additive fields | Reinterpret field meanings silently |
| Choice | FlatBuffers for random access need | FlatBuffers “because binary” when proto+gRPC fits better |
| Fuzzing | Malformed offset corpus | Only happy-path unit tests |
| Secrets | Avoid putting keys in buffers logs | Log full payloads |

## Output Checklist

- [ ] Use-case fit vs Protobuf documented
- [ ] `.fbs` schema reviewed
- [ ] Codegen in build/CI
- [ ] Builder/read examples tested
- [ ] Verifier + max size on untrusted paths
- [ ] Compatibility tests
- [ ] Fuzz or adversarial cases considered
- [ ] `code-quality-standards` applied

## Rules

- Owned systems; adversarial testing only with authorization.
- Zero-copy is not zero-validation—always verify untrusted buffers.
- Prefer schema discipline over ad-hoc binary structs.
- Route gRPC/Protobuf RE to specialized skills; keep focus on FlatBuffers usage and safe parsing.
