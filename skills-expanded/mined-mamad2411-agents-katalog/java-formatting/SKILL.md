---
name: java-formatting
description: MIND CTI Java code formatting and style rules. Covers indentation, braces, imports, annotations, line length, and SonarQube compliance. Auto-loads for any Java file.
paths: "**/*.java"
user-invocable: false
---

# Java Formatting — MIND CTI Code Style

> MIND CTI company-wide standard — auto-loaded for all Java files.

## When This Applies

This skill applies to **every `.java` file**. It is not user-invocable — it loads automatically as background knowledge when editing Java files.

## Core Principles

1. **Consistency over preference** — Follow the existing style within a file. Don't reformat surrounding code.
2. **Readability at a glance** — Formatting should make the code structure obvious.
3. **Minimal diffs** — Formatting changes should not pollute git history. Do not reformat files you're not functionally changing.

## Quick Reference — Key Rules

1. **4 spaces** for indentation. No tabs.
2. **Opening brace** on the same line as the statement.
3. **Max line length**: 120 characters (soft limit), 150 (hard limit).
4. **One blank line** between methods. Two blank lines before the first method.
5. **No wildcard imports** (`import java.util.*`).
6. **Imports ordered**: `java.*`, blank line, `javax.*`/`jakarta.*`, blank line, third-party, blank line, `com.mind.*`.
7. **Always use braces** for `if`, `else`, `for`, `while` — even single-line bodies.
8. **Annotations**: one per line, above the element.
9. **Spaces around operators**: `a + b`, not `a+b`. Space after commas: `method(a, b)`.
10. **No trailing whitespace**.

## Detailed Reference

- For indentation, blank lines, line length, and wrapping → [whitespace-and-indentation.md](docs/whitespace-and-indentation.md)
- For brace style, switch formatting, and block rules → [braces-and-blocks.md](docs/braces-and-blocks.md)
- For import ordering, wildcards, and static imports → [imports.md](docs/imports.md)
- For annotation placement and ordering → [annotations.md](docs/annotations.md)
- For SonarQube rules and suppression handling → [sonar-rules.md](docs/sonar-rules.md)

## MIND CTI Specific Notes

- **V10.00 legacy** code may use different formatting (tabs, different brace style). When editing legacy files, **match the existing style** in that file. Do not reformat.
- **Modern projects** (git/) should follow these rules consistently.
- **IDE settings**: These rules align with IntelliJ IDEA defaults with minor adjustments. Teams should share `.editorconfig` or IntelliJ code style XML.
