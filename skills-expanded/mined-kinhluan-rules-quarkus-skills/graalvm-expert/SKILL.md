---
name: graalvm-expert
description: Expert knowledge for GraalVM, Native Image (AOT), Polyglot runtime, and reflection/resource configuration. Use for native compilation and multi-language JVM questions.
version: 1.1.0
keywords: [graalvm, native-image, aot, polyglot, optimization, jvm]
---

# graalvm-expert

> Keyword: graalvm | Platforms: gemini,claude,codex

High-Performance Polyglot & Native VM Expert Skill - Specialized in GraalVM AOT (Ahead-of-Time) compilation.

## Core Mandates

- **AOT Mindset:** Understand that Native Image has a "Closed-world assumption" (all bytecode must be known at build time).
- **Reflection Discipline:** Mandate `reflection-config.json` for any dynamic class loading or reflection usage.
- **Initialization Policy:** Differentiate between **Build-time initialization** (faster startup, smaller image) and **Runtime initialization** (safer for classes with side effects).
- **Polyglot Strategy:** Leverage GraalVM SDK for high-performance interoperability between Java, JS, Python, and Ruby.

## Native Image Mastery

- **Native Image Agent:** Using `java -agentlib:native-image-agent` to automatically generate configuration files.
- **Resource Management:** Config for `resource-config.json` to include static assets in the native binary.
- **Dynamic Proxy:** Configuring `proxy-config.json` for Java dynamic proxies.
- **Substrate VM:** Understanding memory management and GC options (G1 vs Serial) in native binaries.

## GraalVM + Build Systems

- **Maven/Gradle:** Using the GraalVM Native Build Tools plugins.
- **Bazel Integration:** Configuring `rules_graalvm` and toolchains for hermetic native builds.
- **Quarkus Native:** Troubleshooting Quarkus-specific native image failures (often related to extensions or transitive libraries).

## Optimization & Performance

- **PGO (Profile-Guided Optimization):** Collecting profiles from JIT runs to optimize AOT binaries.
- **Graal JIT:** Using Graal as a replacement for C2 compiler in standard JVM mode for better performance in modern Java.
- **Static Analysis:** Interpreting GraalVM build-time reports (reachability analysis).

## Expert Tips

- Always check `reflect-config.json` if you get `ClassNotFoundException` in a native binary.
- Prefer `quarkus.native.additional-build-args` for passing low-level GraalVM flags.
- Use `--trace-class-initialization` to debug complex initialization order issues.

## 🌐 GraalVM Deep Dives

> **Directive:** Use `web_fetch` to find specific configuration flags or reflection-config.json syntax if a native build fails or requires optimization.

- **Native Image Agent:** [GraalVM Agent Guide](https://www.graalvm.org/latest/reference-manual/native-image/metadata/AutomaticMetadataCollection/) - Automating metadata collection.
- **Reflection Config:** [Reflection Config Reference](https://www.graalvm.org/latest/reference-manual/native-image/metadata/#reflection) - Manual reflection configuration.
- **Dynamic Proxy:** [Dynamic Proxy metadata](https://www.graalvm.org/latest/reference-manual/native-image/metadata/#dynamic-proxy) - Handling interface-based proxies.
- **Static vs Runtime Init:** [Class Initialization in Native Image](https://www.graalvm.org/latest/reference-manual/native-image/optimizations/ClassInitialization/) - Debugging --initialize-at-build-time.

## References

- [GraalVM Native Image Documentation](https://www.graalvm.org/latest/reference-manual/native-image/)
- [Quarkus Native Image Guide](https://quarkus.io/guides/building-native-image)
- [GraalVM GitHub Repository](https://github.com/oracle/graal)

## Skill Interoperability

The **graalvm-expert** 🚀 skill provides the native runtime and AOT compilation expertise for:
- **quarkus-expert** ⚡: Enables building Native Images for Quarkus applications.
It depends on **java-expert** ☕ for understanding reflection and resource configuration.
