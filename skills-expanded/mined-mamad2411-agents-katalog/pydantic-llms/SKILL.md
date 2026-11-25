---
name: pydantic-llms
description: >-
  Reference and APIs for retrieving Pydantic documentation programmatically.
  USE FOR: Pydantic documentation search, data validation, models, settings, V2 migration.
  DO NOT USE FOR: General Python programming questions without Pydantic.
license: MIT
---

# pydantic-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Pydantic documentation articles or concepts.
- **Data Validation & Settings**: Fetching guidelines on Pydantic models, fields, and configuration.
- **Migration**: Retrieving context for migrating from Pydantic V1 to V2.

## WHEN NOT TO USE

- **General Python Development**: Using Python without Pydantic. Use the `python` skill instead.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path for Pydantic.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Fetching `llms-full.txt` without narrowing the scope**. Prefer the index or a targeted document when possible, and filter aggressively if you must use the full file.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Pydantic LLMs Context](https://docs.pydantic.dev/latest/llms.txt)
  USE FOR: Pydantic high-level overview, general usage, core concepts, models, fields, settings, JSON schema, and V2 migration.
- [Pydantic LLMs Full Context](https://docs.pydantic.dev/latest/llms-full.txt)
  USE FOR: Deep dive into all Pydantic features, comprehensive API reference, advanced validation, custom types, performance optimization.
  Note: This file contains the full documentation and MUST be filtered or selectively read due to its large size.
