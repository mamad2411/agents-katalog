---
name: kotlin-backend
description: >
  Kotlin backend engineering conventions. Use together with the `kotlin` skill.
---

# Libraries

- Prefer Kotlin-first libraries where practical: Ktor, coroutines, kotlinx.serialization, Exposed, etc., unless I explicitly ask otherwise.
- Use `logback-classic` for logging. Always provide a default logging configuration in resources with a readable pattern.
