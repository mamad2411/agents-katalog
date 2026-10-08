---
name: harness-coding-smoke
description: Deterministic fixture used to verify the Skill.md-native Harness Kernel contract.
license: MIT
---

# Harness Coding Smoke Fixture

This fixture exists to test the Harness Kernel contract, schema, planning, evidence, and verdict pipeline.

It is intentionally executed only through `FakeRuntime` in normal CI. A passing run proves that the local contract machinery is implemented; it does **not** prove live sandbox isolation, a real Coding Agent invocation, or compatibility with an external `skill` executable.
