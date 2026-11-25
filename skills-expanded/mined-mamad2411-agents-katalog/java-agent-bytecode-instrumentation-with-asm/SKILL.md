---
name: java-agent-bytecode-instrumentation-with-asm
description: Build a JVM agent using ASM's ClassFileTransformer to inject profiling/monitoring hooks into application classes via pluggable visitor chains
category: backend
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [java, jvm, apm, instrumentation, asm, bytecode]
confidence: high
---

# Java Agent Bytecode Instrumentation with ASM

Apply this skill when you need to observe or modify JVM behavior without touching application source — APM tracing, security policy enforcement, test coverage, feature flag injection.

## Pattern

1. Package as a `-javaagent:<jar>` premain JAR with `Premain-Class` in `MANIFEST.MF` and `Can-Retransform-Classes: true`.
2. Register a `ClassFileTransformer` whose `transform(...)` dispatches per-target-class to composable ASM `ClassVisitor` chains (one visitor per concern: field add, method wrap, try/catch injection).
3. Gate each visitor with a class-name / annotation / interface filter — don't visit everything; it's expensive and fragile.
4. Handle JDK-dynamic classes separately (lambdas, method handles). Scouter uses a dedicated `LambdaFormTransformer`.
5. Expose a config (flags, allow-list, hook-level) so unsafe hooks (async, lambda) can be disabled in production if they conflict with other agents.

## Evidence

- `scouter.agent.java/src/main/java/scouter/agent/AgentTransformer.java` — main dispatch
- `scouter.agent.java/src/main/java/scouter/agent/asm/AddFieldASM.java` — visitor example
- `scouter.agent.java/src/main/java/scouter/agent/LambdaFormTransformer.java` — lambda handling
- `scouter.agent.java/readme.md`

## Pitfalls

- Lambda forms and synthetic classes bypass normal hooks. Always add a lambda-form transformer.
- Spring proxy classes conflict with naive class-name matchers — use runtime interface checks.
- Multi-agent conflicts: if your hooks wrap the same methods as another agent, order matters. Document compat.

## Related knowledge

- `asm-based-classloader-instrumentation-caveats` (pitfall)
- `trace-context-async-execution-propagation` (pitfall)
