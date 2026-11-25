---
name: code-category-pointer
description: "Pointer to a library of 18 specialized Code skills. Use when working on code-related tasks."
risk: none
---

# Code Capability Library 🎯

This is a **pointer skill**. The 18 specialized Code skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **c-pro** — Write efficient C code with proper memory management, pointer
- **cpp-pro** — Write idiomatic C++ code with modern features, RAII, smart pointers, and STL algorithms. Handles templates, move semantics, and performance optimization.
- **csharp-pro** — Write modern C# code with advanced features like records, pattern matching, and async/await. Optimizes .NET applications, implements enterprise patterns, and ensures comprehensive testing.
- **elixir-pro** — Write idiomatic Elixir code with OTP patterns, supervision trees, and Phoenix LiveView. Masters concurrency, fault tolerance, and distributed systems.
- **golang-pro** — Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices.
- **haskell-pro** — Expert Haskell engineer specializing in advanced type systems, pure
- **java-pro** — Master Java 21+ with modern features like virtual threads, pattern matching, and Spring Boot 3.x. Expert in the latest Java ecosystem including GraalVM, Project Loom, and cloud-native patterns.
- **javascript-pro** — Master modern JavaScript with ES6+, async patterns, and Node.js APIs. Handles promises, event loops, and browser/Node compatibility.
- **julia-pro** — Master Julia 1.10+ with modern features, performance optimization, multiple dispatch, and production-ready practices.
- **php-pro** — Write idiomatic PHP code with generators, iterators, SPL data
structures, and modern OOP features. Use PROACTIVELY for high-performance PHP
applications.

- **python-pro** — Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices. Expert in the latest Python ecosystem including uv, ruff, pydantic, and FastAPI.
- **ruby-pro** — Write idiomatic Ruby code with metaprogramming, Rails patterns, and performance optimization. Specializes in Ruby on Rails, gem development, and testing frameworks.
- **rust-pro** — Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming.
- **sankhya-dashboard-html-jsp-custom-best-pratices** — This skill should be used when the user asks for patterns, best practices, creation, or fixing of Sankhya dashboards using HTML, JSP, Java, and SQL.
- **scala-pro** — Master enterprise-grade Scala development with functional programming, distributed systems, and big data processing. Expert in Apache Pekko, Akka, Spark, ZIO/Cats Effect, and reactive architectures.
- **typescript-advanced-types** — Comprehensive guidance for mastering TypeScript's advanced type system including generics, conditional types, mapped types, template literal types, and utility types for building robust, type-safe applications.
- **typescript-pro** — Master TypeScript with advanced types, generics, and strict type safety. Handles complex type systems, decorators, and enterprise-grade patterns.
- **unreal-engine-cpp-pro** — Expert guide for Unreal Engine 5.x C++ development, covering UObject hygiene, performance patterns, and best practices.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/code/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/code`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
