---
name: think-before-coding-surface-assumptions
description: Before implementing, surface assumptions, present multiple interpretations, and stop to ask when something is unclear. Use whenever a user request has ambiguous scope, fields, format, or behavior.
category: engineering
version: 1.0.0
version_origin: extracted
tags: [llm-behavior, planning, clarification, anti-assumption]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/forrestchang/andrej-karpathy-skills.git
source_ref: main
source_commit: c9a44ae835fa2f5765a697216692705761a53f40
source_project: andrej-karpathy-skills
source_path: skills/karpathy-guidelines/SKILL.md
imported_at: 2026-04-18T08:26:22Z
---

# Think Before Coding — Surface Assumptions

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Derived from Andrej Karpathy's observation that LLMs "make wrong assumptions on your behalf and just run along with them without checking."

## When to use
- User request has ambiguous scope (all users? filtered subset?).
- Multiple valid interpretations of the verb (e.g., "make it faster" → latency vs. throughput vs. perceived speed).
- Critical fields, formats, file paths, or privacy implications are unstated.
- You caught yourself reaching for a default without evidence.

## How to apply
1. **State assumptions explicitly.** "I'll assume X because Y — correct me if that's wrong."
2. **Enumerate interpretations** when two or more are plausible. Let the user pick.
3. **Push back** when a simpler approach exists than what was asked for.
4. **Stop when confused.** Name what's unclear. Ask one precise question.

## Checklist before writing code
- [ ] Scope is defined (what's in, what's out).
- [ ] Format / fields / success shape are stated.
- [ ] Ambiguous verbs have been disambiguated.
- [ ] Known tradeoffs surfaced (effort, risk, reversibility).

## Anti-patterns
- Silently picking one interpretation of "export users" and shipping it.
- Adding caching, indexes, and async "just in case" when user said "make it faster."
- Swallowing confusion and guessing because asking feels like friction.
