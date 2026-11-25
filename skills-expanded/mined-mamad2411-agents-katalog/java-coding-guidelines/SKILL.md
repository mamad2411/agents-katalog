---
name: "java-coding-guidelines"
description: "Enforces Java Coding Guidelines for code review, generation, and refactoring. Invoke when writing Java code, reviewing Java PRs, fixing Java style issues, or when user mentions coding standards, Java conventions, or Chinese Java development norms."
---

# Java Coding Guidelines

Core rules from Java Coding Guidelines v1.7.1. Apply when writing, reviewing, or refactoring Java code.

| Section | Reference | When to Read |
|---------|-----------|-------------|
| Naming | `references/naming-conventions.md` | Naming classes, methods, variables, packages, constants |
| OOP | `references/oop-conventions.md` | POJOs, equals/hashCode, inheritance, casting |
| Collection & Concurrency | `references/collection-concurrency.md` | Collections, thread pools, locks, concurrent utilities |
| Exception, Logging & Control | `references/exception-logging-control.md` | Exceptions, logging, control flow |
| Format, Comments & Structure | `references/format-comments-structure.md` | Formatting, comments, project structure |
| Unit Test & Security | `references/unit-test-security.md` | Testing, security |

## How to Apply

### Writing New Code
Read relevant reference → follow naming → apply OOP rules → handle exceptions & logging → write tests.

### Reviewing Code
Read reference for each area → verify rules → categorize: **Mandatory** (must fix) / **Recommended** (should fix) / **Reference** (nice to have).

### Refactoring Code
Fix Mandatory first → naming consistency → thread-unsafe patterns → exception handling & logging.