# Audit Context Building

**Audit Context Building** is a skill developed by Omar Inuwa that enables systematic code comprehension before security analysis begins.

## Core Purpose

This methodology focuses on establishing "deep architectural context through ultra-granular code analysis." Rather than jumping to vulnerability discovery, it prioritizes building a foundational understanding of how code systems actually work.

## Methodology

The skill operates through three sequential phases:

1. **Initial Orientation** maps the system's structural elements
2. **Ultra-Granular Function Analysis** examines code semantically with attention to data flows across functions
3. **Global System Understanding** reconstructs system state and trust boundaries

## What It Explicitly Does NOT Do

This is intentionally scoped as a context-building tool only. It deliberately avoids vulnerability identification, solution proposals, proof-of-concept development, and severity assessment. Those activities belong to subsequent audit phases.

## Hallucination Prevention

The methodology incorporates safeguards: maintaining logical consistency when new evidence emerges, avoiding speculative reasoning, and continuously cross-referencing findings against the actual codebase.

## Integration

The skill connects to related audit tools like `issue-writer`, `differential-review`, and `spec-compliance`, which leverage the contextual foundation this skill establishes.
