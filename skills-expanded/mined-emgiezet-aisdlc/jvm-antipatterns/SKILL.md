---
name: jvm-antipatterns
description: Forbidden JVM (Java/Kotlin) patterns — JDBC injection, insecure deserialization, weak random, trust-all TLS, Jackson misconfiguration.
paths: ["**/*.java","**/*.kt","**/*.kts"]
user-invocable: false
---

# JVM (Java / Kotlin) anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-JVM-SEC-001 — Use `PreparedStatement` with `?` placeholders; never concatenate user data into SQL strings.
- AP-JVM-SEC-002 — Avoid `ObjectInputStream` on external data; use JSON/Protobuf or a deserialization filter.
- AP-JVM-SEC-003 — Use `ProcessBuilder(List.of("prog", arg1, arg2))` with separate args; never exec a string with user data.
- AP-JVM-SEC-004 — Use `SecureRandom` for tokens and session IDs; `java.util.Random` is for simulations only.
- AP-JVM-SEC-005 — Never implement a no-op TrustManager; use the default TrustManagerFactory with a valid KeyStore.
- AP-JVM-SEC-006 — Never call `enableDefaultTyping`; use a registered subtype safelist with `@JsonSubTypes`.

## Errors
- AP-JVM-PERF-001 — Use `JOIN FETCH` or an entity graph to eager-load associations; avoid lazy access in loops.
- AP-JVM-MAINT-001 — Catch the specific exception; log with context and rethrow or handle; never swallow silently.
- AP-JVM-MAINT-002 — Throw typed exceptions from library code; never call `System.exit` outside `main`.

Details for any ID: `reference/<ID>.md`
