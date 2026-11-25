---
name: android-binary-static-analysis
description: "Use when statically inspecting Android APKs and splits."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Android, APK, DEX, Static Analysis, Reverse Engineering, Networking]
    related_skills: [codebase-inspection]
---

# Android Binary Static Analysis

Reconstruct an Android application's behavior from locally supplied APKs and split APKs. Prefer reproducible, evidence-linked analysis over string-only conclusions. This workflow is for authorized local artifacts; follow the user's limits on network access, authentication, and secrets.

## When to Use

- Inspecting a base APK plus ABI, density, language, or feature splits
- Reconstructing startup, dependency injection, networking, discovery, authentication, or data-model flows
- Finding where URLs and request parameters are built and how responses propagate
- Comparing an official binary's actual schema against a local client implementation
- Working without JADX or apktool when Android SDK tools are available

## Required Output Discipline

Classify important conclusions explicitly:

- **FACT** — directly demonstrated by an artifact, instruction, annotation, field type, or call chain
- **INFERENCE** — the evidence supports it, but an execution path or runtime value remains unobserved
- **UNKNOWN** — not established yet; state the missing evidence needed

For every FACT, preserve:

1. APK/split and extracted file path
2. class and method/function
3. relevant instruction, annotation, constant, or field mapping
4. the propagation step it proves

Never print passwords, tokens, client secrets, private keys, or session material. Record sensitive values as `[REDACTED]` while preserving the class/method and purpose.

## Workflow

### 1. Inventory before decompilation

For every APK/split, record absolute path, size, SHA-256, package/version, split name and role, and ZIP entry categories. Use the base APK for application code and manifest, then identify which splits add native code, resources, or feature DEX. Do not assume every split is relevant.

### 2. Extract without destroying provenance

Create a versioned analysis directory outside the original artifacts. Preserve one subdirectory per APK and keep generated reports separate.

Useful local tools:

- `aapt dump badging`, `aapt dump xmltree`, `aapt dump resources`
- Android SDK `apkanalyzer manifest`, `apkanalyzer dex packages`, `apkanalyzer dex code`
- `strings -a` for DEX and native libraries
- ZIP extraction for assets, DEX, and `lib/<abi>/*.so`
- `readelf`, `nm`, and `objdump` when native symbols/imports matter

Do not stop because JADX or apktool is unavailable. SDK tools plus smali are sufficient for many flow reconstructions.

### 3. Search broadly, then follow references

Search hosts, URLs, paths, GraphQL documents, MQTT addresses, networking SDKs, AWS/OAuth/Firebase configuration, endpoint/region/pool identifiers, DTOs, generated adapters, query classes, and Room schemas. Strings identify candidates, not behavior. Promote a candidate to FACT only after tracing its caller, annotations, or data flow.

### 4. Recover code under R8/ProGuard

For a target class:

```text
apkanalyzer dex code --class fully.qualified.Class base.apk
```

Read together:

- Kotlin `Metadata.d2`, which often preserves parameter/property names
- field descriptors and constructor assignment order
- generated Moshi/Gson adapters
- coroutine `invokeSuspend`
- Retrofit annotations and signatures
- callers and downstream consumers

When a method is obfuscated, prove its meaning through return type and field access rather than guessing from its letter.

### 5. Obtain a searchable smali corpus

For cross-references, disassemble the DEX containing the application package. If the SDK baksmali JAR has no executable manifest, invoke its main class with all required SDK library JARs on the Java classpath. Build the recursive JAR classpath programmatically and run:

```text
com.android.tools.smali.baksmali.Main disassemble classesN.dex -o baksmaliN/
```

Then search invocation sites such as `Lpackage/Model;->getter()Ljava/lang/String;` to reveal which discovered values feed Cognito, Apollo, MQTT, firmware, analytics, or storage.

### 6. Reconstruct networking as a propagation graph

Build the graph in order:

```text
Application startup
→ DI/provider or platform setup
→ discovery/config request
→ response adapter/model
→ local cache
→ AWS/OAuth/client configuration
→ HTTP/GraphQL client construction
→ login/token acquisition
→ authorization interceptor
→ query class
→ response model/mapper
→ persistence/domain model
```

For each request establish URL construction, method/path, parameters, headers and their origins, body model, response adapter, and retry/redirect/cache/region behavior.

### 7. Prove token semantics by tracing types

Do not label an opaque token as access or ID token from position alone. Trace the SDK session's typed fields, token-container constructor order, getter selected by the interceptor, and final header attachment. Distinguish application identifiers from secrets, but redact credential-like values unless disclosure is explicitly necessary.

### 8. Extract generated GraphQL documents exactly

Generated Apollo classes often retain complete query/mutation/fragment strings in DEX. Extract exact documents, deduplicate them, and separate queries from mutations. Verify resolver names, variables/types/defaults, pagination, response fields, and fragments. Never infer a schema from a pre-existing local client when the binary provides the exact operation; compare and flag every mismatch before network use.

### 9. Verification gates

Before concluding:

- confirm every relevant split was inspected
- compare hosts from resources, DEX, assets, and native libraries
- verify annotations and coroutine call sites
- verify DTO mappings from adapters or generated documents
- distinguish startup initialization from lazy construction
- identify cached versus freshly fetched configuration
- run local tests after any implementation changes

Static analysis cannot establish live values, account-specific MFA policy, server pagination limits, or current endpoint behavior. Leave those UNKNOWN until an authorized minimal runtime probe.

## Pitfalls

- A URL string does not prove the request path or caller.
- Kotlin metadata, typed fields, adapters, and constructor order can recover one-letter R8 methods.
- Generated adapters are often the clearest serialized-field map.
- Extract exact GraphQL documents before trusting a local client schema.
- Do not call discovery “public” if it requires an authorization value; classify it before sending anything.
- Verify generated file counts/content and downstream consumers before reporting completion.
- Preserve token location and use but redact its value.

## Supporting References

- See `references/apk-network-reconstruction-case.md` for a worked example covering Retrofit discovery, dynamic AWS configuration, Cognito SRP selection, Apollo authorization, and exact GraphQL extraction.
