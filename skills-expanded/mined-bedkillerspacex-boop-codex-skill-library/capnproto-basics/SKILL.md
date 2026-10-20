---
name: capnproto-basics
description: >
  Cap'n Proto basics for owned services: schema (.capnp), codegen, RPC capability
  model, packing/framing, versioning, and security limits on untrusted messages. Use
  when adopting Cap'n Proto serialization/RPC, capnp compile, or capability-based
  interfaces — not for attacking third-party Cap'n Proto services without authorization.
---

# Capnproto Basics

## Scope And Authorization

- **In scope:** Schemas and services you own; lab RPC between your components.
- **Out of scope:** Unauth fuzzing/production DoS of third-party systems; capability token theft attacks outside RoE.
- Treat untrusted network input as hostile — set traversal limits.
- Pair with `code-quality-standards` and general RPC security practices.

## When To Use

- Choosing Cap'n Proto for zero-copy serialization or capability RPC.
- Defining `.capnp` schemas, codegen for C++/Rust/Go/other supported langs.
- Evolving schemas with compatibility (IDs, new fields).
- Hardening parsers against malicious deeply nested messages.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Protobuf/gRPC ecosystem | `protobuf-grpc-reverse-engineering` / gRPC skills |
| CBOR tokens | `cbor-web-tokens` |
| Generic protocol reverse | `protocol-reverse-engineering` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Schema | `.capnp` with `struct`, `interface`, enums |
| Field IDs | Numeric ordinals; do not renumber lightly |
| Codegen | `capnp compile -o<lang>` |
| Messages | Segments; optional packing |
| RPC | Promise pipelining; capability references |
| Security | Trust boundaries; size limits; no ambient authority |

## Workflow

### 1. Confirm scope and success criteria

1. Languages, transport (TCP, Cap'n Proto RPC, custom), trust model (mTLS?).
2. Success: schema compiled; round-trip tests; versioning policy; untrusted parse limits verified.
3. Decide if you need RPC or serialization only.

### 2. Install toolchain

```bash
capnp --version
# Language plugins per official docs (e.g. capnpc-rust, C++ toolchain)
```

1. Pin `capnp` compiler version in CI.
2. Generate into `gen/` or package-appropriate paths; do not hand-edit generated code.

### 3. Write schema

```capnp
@0xdbb9ad1ab7ec8c6d;  # unique file id (capnp id)

struct User @0x8c5a1c2f0e9b7d64 {
  id @0 :UInt64;
  name @1 :Text;
  email @2 :Text;
  # add new fields with new ordinals only
  active @3 :Bool = true;
}

interface Directory @0x9f3e2a1b0c8d7654 {
  lookup @0 (name :Text) -> (user :User);
  # capabilities: return interfaces for least privilege
}
```

1. Run `capnp id` to generate unique IDs for files/types as required.
2. Prefer explicit ordinals; never reuse ordinals for different meaning.
3. Use groups/unions carefully for optional variants.

### 4. Codegen and integrate

```bash
capnp compile -oc++ user.capnp
# Rust example pattern
capnp compile -orust:src/gen user.capnp
```

1. Build library wrapping encode/decode.
2. For RPC, follow language-specific capability server bootstrap patterns.
3. Transport security: mTLS or ssh-like secure channel — Cap'n Proto is not encryption by itself.

### 5. Versioning and compatibility

| Change | Safe? |
| --- | --- |
| Add field with new ordinal + default | Usually yes for readers ignoring unknowns |
| Rename field (same ordinal) | Wire ok; code churn |
| Change field type same ordinal | **Breaking** |
| Reuse ordinal for new meaning | **Breaking / dangerous** |
| Delete field | Readers must tolerate absence |

1. Contract tests between versions in CI.
2. Document minimum reader/writer versions per deployment.

### 6. Security hardening

1. Set message size / traversal / nesting limits on untrusted inputs (language API specific).
2. Do not deserialize into privileged actions without authz on capabilities.
3. Capability discipline: hand out only narrow interfaces; revoke on disconnect.
4. Fuzz parsers in lab with size caps.
5. Avoid trusting `Text` as path/SQL without validation.

```text
# Checklist for untrusted blob
- max bytes accepted at transport
- max segments / depth
- time budget parse
- authn before side effects
```

### 7. Verify and hand off

```bash
# Schema parse
capnp compile -o- schema.capnp >/dev/null
# Unit: encode/decode golden vectors
# Integration: old client + new server
```

1. Document schema ownership and review rules (like API review).
2. Apply `code-quality-standards` to wrappers and RPC handlers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IDs | Stable unique ordinals | Renumber fields casually |
| Trust | Limits on untrusted parse | `mmap` whole file unbounded |
| RPC | Narrow capabilities | One mega interface god-object |
| Security | mTLS transport | Cleartext Internet RPC |
| Codegen | CI pin compiler | Random host plugin versions |
| Compat | Add-only fields | Type change same ordinal |

## Output Checklist

- [ ] Toolchain version pinned
- [ ] Schemas with unique IDs authored
- [ ] Codegen integrated in build
- [ ] Round-trip and compatibility tests
- [ ] Transport auth documented
- [ ] Untrusted message limits set
- [ ] Capability/authz model reviewed for RPC
- [ ] Versioning policy written
- [ ] `code-quality-standards` applied

## Rules

- Cap'n Proto is not a substitute for transport encryption or authentication.
- Treat schema ordinals as public API surface.
- Enforce parse limits on untrusted data.
- Authorized services only.
- Prefer Protobuf/gRPC skills when that is the stack in use.
