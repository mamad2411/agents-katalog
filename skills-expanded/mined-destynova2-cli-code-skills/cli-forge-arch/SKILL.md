---
name: cli-forge-arch
metadata:
  author: clement
description: "Router for architecture design. Detects whether the user needs an HLD or LLD and delegates to the appropriate skill. Use when the user says 'design doc', 'architecture', or is ambiguous about HLD vs LLD. For explicit HLD requests, use cli-forge-hld directly. For explicit LLD requests, use cli-forge-lld directly."
argument-hint: "[system-name-or-description]"
context: fork
agent: general-purpose
---

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the document in that language. If the project is bilingual, ask the user which language to use before proceeding.

**Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

# Arch Router — HLD / LLD Dispatcher

This skill has been split into two focused skills. Route the user's request accordingly:

## Routing Table

| Signal in user's request | Delegate to |
|--------------------------|-------------|
| "HLD", "system design", "architecture", "C4 context/container", "capacity", "back-of-envelope", "ATAM", "Gate review", "design proposal" | **`/cli-forge-hld`** |
| "LLD", "detailed design", "class diagram", "sequence diagram", "API spec", "DB schema", "component design", "STRIDE", "threat model" | **`/cli-forge-lld`** |
| "design doc", "tech spec" (ambiguous) | Ask the user: "Do you want a **high-level design** (system architecture, C4 L1-L2, capacity estimation, ADRs) or a **low-level design** (class diagrams, API contracts, DB schemas, sequence diagrams)?" |
| Both mentioned | Produce HLD first, then LLD for each key container |

## What changed

The original `cli-forge-arch` combined HLD and LLD in a single skill. This caused issues:
- Users asking for HLD got LLD-level detail (class diagrams, DB schemas) they didn't need
- Users asking for LLD got HLD-level context (system diagrams, capacity) that was redundant
- The skill was too large to produce focused, high-quality output

**New skills:**
- **`cli-forge-hld`** — C4 L1-L2, capacity estimation, ADRs, ATAM tradeoff analysis, deployment architecture
- **`cli-forge-lld`** — C4 L3-L4, class/sequence/state diagrams, API contracts, DB schemas, STRIDE, testability

The `references/` directory is preserved here for backward compatibility but the canonical references now live in each skill's own `references/` directory.
