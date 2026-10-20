---
allowed-tools: Read, Glob, Grep, Bash(ls*), Task, Agent, Skill
description: Route questions to matched experts, synthesize answers, debate contradictions
argument-hint: [question] [context] [changed_files]
---

# Expert Orchestrator — Consult

Route a question to the right domain experts based on file patterns and domain tags, synthesize their answers, and resolve contradictions via one-round debate.

## Variables

QUESTION: $1
CONTEXT: $2
CHANGED_FILES: $3

## Instructions

- IMPORTANT: This is a consultation task — DO NOT write, edit, or create any files
- Maximum 3 experts consulted per question
- Debate is only triggered if contradictions are found AND matched experts <= 3

## Workflow

### 1. Discover Experts

- Glob `.claude/commands/experts/*/expertise-meta.yaml`
- For each expertise-meta.yaml, read `domain_tags` and `file_patterns` (these are small metadata-only files, ~50 lines)
- Build a registry: `{ name, domainTags[], filePatterns[] }`
- NOTE: Do NOT read the full `expertise.yaml` files at this stage — only read metadata for matching

### 2. Match Experts

- If CHANGED_FILES is provided (comma-separated paths), match each path against each expert's `file_patterns` globs (prefix match: `convex/**` matches any path starting with `convex/`)
- Also check if QUESTION keywords match any expert's `domain_tags`
- Collect matched experts (deduplicated). If no matches found, select all experts.
- Cap at 3 experts maximum.

### 3. Consult Matched Experts (parallel)

For each matched expert, invoke `/experts:{name}:question` with:
- Argument 1: QUESTION
- Argument 2: CONTEXT (if provided)

Use the Task tool to run consultations in parallel. Collect all responses.

### 4. Synthesize

Read all expert responses. Identify:
- **Areas of agreement**: constraints, patterns, invariants all experts align on
- **Contradictions**: where experts disagree on approach, constraints, or patterns

### 5. Debate Contradictions (conditional)

If contradictions found AND matched experts <= 3:
- Send one follow-up round to conflicting experts via Task tool
- Each expert is informed of the other's position and asked to reconcile
- Read responses and attempt consensus
- If no consensus, flag as unresolved

### 6. Return Structured Response

Output this exact format:

```
## Expert Consultation

**Experts consulted:** {comma-separated expert names}
**Changed files matched:** {files to expert mapping, or "none provided"}

### Guidance

{synthesized guidance from all experts, contradictions resolved or flagged}

### Contradictions

{any unresolved contradictions with both positions stated, or "none"}

### Expert Advice Summary

{one-paragraph summary of the key constraints and patterns the implementation must follow}
```

## Step Summary

- status: pass | fail
- action: <one line describing what was consulted>
- decision: <one line — key routing choice>
- blockers: <one line, or "none">
- files_changed: none
- expert_consulted: <comma-separated expert names>
- expert_advice_summary: <one-line summary of key guidance>
