---
name: quarkus-debug
description: Expert skill for deep debugging of Quarkus applications, covering Dev Mode, Reactive patterns (Mutiny), Native Image (AOT) issues, and Build-time (Augmentation) troubleshooting.
version: 1.0.0
keywords: [quarkus, debug, troubleshooting, mutiny, reactive, native-image, augmentation, jpda, gdb, lldb]
---

# quarkus-debug

> Keyword: quarkus-debug | Platforms: gemini,claude,codex

Expert AI Agent Skill for **Quarkus Debugging** - Advanced techniques for diagnosing and fixing issues across the entire Quarkus lifecycle, from development mode to native executables.

## Core Mandates

- **Dev Mode First:** Always leverage `quarkus:dev` for immediate feedback and live reload.
- **Context-Aware Debugging:** Distinguish between Imperative (Blocking) and Reactive (Event Loop) contexts.
- **Binary Parity:** Ensure behavior consistency between JVM mode and Native Image mode.
- **Augmentation Insight:** Distinguish between build-time (deployment) and run-time errors.
- **No-Block Rule:** Never block the Event Loop during debugging unless using specific thread-aware tools.

---

## 🛠 Debugging Domains

### 1. Development Phase (Dev Mode)
- **JPDA/Remote Debug:** Default port `5005`. Use `quarkus.debug.host` and `quarkus.debug.port` to customize.
- **Dev UI (`/q/dev`):** 
    - Inspect **CDI Beans**, **Configuration**, and **Extension** status.
    - Use the **Arc** extension UI to debug dependency injection issues.
    - **Continuous Testing:** Debug tests as they run in the background.
- **Hot Reload Issues:** If changes don't reflect, check `quarkus.live-reload.password` or ClassLoader isolation settings.

### 2. Reactive & Asynchronous (Mutiny)
- **Stack Trace Unwrapping:** Reactive stack traces are often unhelpful. Use `.onFailure().invoke(Throwable::printStackTrace)` or Mutiny's infrastructure tools.
- **Context Propagation:** 
    - Debug `ContextNotActiveException` by ensuring `DuplicatedContext` is propagated correctly.
    - Use `quarkus.arc.context-propagation.enabled=true`.
- **Event Loop Blocking:** Enable `quarkus.vertx.warning-exception-time` to detect long-running tasks blocking the Event Loop.
- **Mutiny Infrastructure:** Use `Infrastructure.setCanClearThreadLocals(false)` carefully to debug ThreadLocal issues.

### 3. Native Executables (GraalVM AOT)
- **AOT Issues:** Most native errors are due to **Reflection**, **Resources**, or **Dynamic Proxies** missing from `reflect-config.json`.
- **GraalVM Agent:** Run in JVM mode with the agent to auto-generate configs:
  ```bash
  java -agentlib:native-image-agent=config-output-dir=./config -jar target/*-runner.jar
  ```
- **Native Debugging:** Build with `-H:GenerateDebugInfo=1` and use **GDB** or **LLDB**.
- **Static vs Runtime Init:** Debug `InitializerError` by checking `quarkus.native.additional-build-args=--trace-class-initialization=...`.

### 4. Build-Time (Augmentation)
- **BuildStep Failure:** If the build fails during "Augmenting phase", it's a `deployment` issue. 
- **Log Verbosity:** Use `-Dquarkus.log.level=DEBUG` during build to see extension internal logs.
- **Bytecode Inspection:** Inspect generated classes in `target/quarkus-app/lib/main/` or using tools like `javap`.
- **Bazel (rules_quarkus):**
    - Debug augmentation by running with `--sandbox_debug --verbose_failures`.
    - Investigate `QuarkusBootstrap` by checking the generated `quarkus-bootstrap.json`.

---

## 🔍 Troubleshooting Workflows

### ClassLoader & Dependency Conflicts
- **Issue:** `ClassCastException` or `NoClassDefFoundError` in Dev Mode.
- **Solution:** Quarkus uses a multi-layered ClassLoader. Check if a library is being loaded by the "Runtime ClassLoader" but expected by the "Base ClassLoader". 
- **Action:** Use `quarkus.class-loading.parent-first-artifacts` to force specific libraries to the parent ClassLoader.

### Database & Dev Services
- **Issue:** Testcontainers/Dev Services fail to start.
- **Action:** Check Docker connectivity. Inspect logs using `docker logs <container_id>`. Use `quarkus.datasource.devservices.port` to pin ports for external inspection.

### Memory Leaks in Dev Mode
- **Issue:** `OutOfMemoryError` after several hot reloads.
- **Action:** Often caused by static fields or threads not being shut down by an extension. Use **JFR (Java Flight Recorder)** to profile:
  ```bash
  mvn quarkus:dev -Dquarkus.profile=dev -Djava.arg.1=-XX:StartFlightRecording=filename=recording.jfr
  ```

---

## 🌐 Troubleshooting Sources

> **Directive:** When dealing with cryptic reactive stack traces or native crashes, use `web_fetch` on these specialized troubleshooting guides.

- **Reactive Diagnostics:** [Mutiny Infrastructure Guide](https://smallrye.io/smallrye-mutiny/latest/guides/infrastructure/) - Clear ThreadLocals and debug handlers.
- **Native Crash Analysis:** [GraalVM Native Image Diagnostics](https://www.graalvm.org/latest/reference-manual/native-image/guides/diagnose-problems/) - Debugging native executables.
- **Context Propagation:** [SmallRye Context Propagation Guide](https://smallrye.io/smallrye-context-propagation/latest/) - Dealing with ThreadLocal loss in async code.
- **OTel Tracing:** [Quarkus OpenTelemetry Guide](https://quarkus.io/guides/opentelemetry) - Tracing requests across microservices.

## 📚 References & Tools

- [Quarkus - Debugging Guide](https://quarkus.io/guides/debugging)
- [Mutiny - Troubleshooting Guide](https://smallrye.io/smallrye-mutiny/latest/guides/troubleshooting/)
- [GraalVM - Native Image Debugging](https://www.graalvm.org/latest/reference-manual/native-image/debugging-and-diagnostics/)
- [rules_quarkus - Integration Troubleshooting](https://github.com/kinhluan/rules_quarkus#troubleshooting)

## Skill Interoperability

The **quarkus-debug** 🔍 skill is an advanced troubleshooting layer built on:
- **java-expert** ☕: JVM internals, JFR, and basic JPDA.
- **quarkus-expert** ⚡: CDI, Augmentation, and Dev Mode internals.
- **vertx-expert** 🌀: Event Loop and non-blocking I/O debugging.
- **graalvm-expert** 🚀: AOT compilation and native runtime issues.
- **rules-quarkus** 🔧: Bazel-specific augmentation and orchestration.
