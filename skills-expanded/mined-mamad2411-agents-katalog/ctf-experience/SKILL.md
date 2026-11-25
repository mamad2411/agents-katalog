---
name: ctf-experience
description: Use when pi needs to capture, consult, or update reusable CTF solving experience rather than solve a single challenge from scratch. Best for post-solve retrospectives, recurring pivot signals, dead-loop breakers, tool-order lessons, routing lessons, and cross-challenge heuristics such as when to test Wiener attack, when to treat a protocol as framed before encrypted, or when to prefer structure-driven analysis over blind factoring.
---

# CTF Experience

## Overview

Use this skill as the long-lived repository for reusable CTF lessons. Keep the body lean, store durable patterns in `references/patterns.md`, and prefer generalized signals over challenge-local artifacts.

## Workflow

1. Decide whether the lesson is durable.
   Keep only lessons that would plausibly change behavior in multiple future challenges.
2. Strip challenge-local detail.
   Remove exact payloads, hostnames, ports, creds, addresses, and constants unless they reveal a general rule.
3. Convert the lesson into a compact pattern.
   Use the schema `Signal -> Why It Matters -> Default Action -> Stop Condition`.
4. Patch the smallest reusable surface.
   Add or refresh the relevant section in [references/patterns.md](references/patterns.md).
   This file is local-only (gitignored): on a fresh clone it will not exist — create it
   (with a minimal header) before the first append; missing file is normal, not an error.
5. Prefer lookup-friendly wording.
   Write so another pi instance can quickly scan for trigger signals and immediately act.

## Reading Strategy

- Start with [references/patterns.md](references/patterns.md).
- Read only the section matching the current failure mode or pivot signal.
- If a new lesson clearly survives generalization, append it to that file instead of creating a separate retrospective document.

## Guardrails

- Do not store full writeups here.
- Do not store secrets, flags, creds, or target-specific artifacts.
- Do not turn one unusual challenge into a universal rule without a clear trigger signal.
- If the lesson belongs inside a narrower specialist skill and would directly change its default workflow, patch that specialist skill first and keep only a short cross-reference here if needed.
