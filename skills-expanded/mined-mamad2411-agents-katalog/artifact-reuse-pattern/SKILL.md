---
name: artifact-reuse-pattern
description: "Update an existing plan or state artifact in place when the same document needs to track progress across multiple agent turns."
category: efficiency
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["artifacts", "state-management", "mutation", "implementation-plan", "walkthrough", "token-optimization"]
tools: ["claude", "cursor", "gemini", "codex", "lmstudio"]
---

# Persistent Living Artifact Mutation Pattern

## Overview
When executing multi-phase engineering tasks, poorly designed agents generate new markdown files for every status update (*`plan_v1.md`*, *`plan_v2.md`*, *`revised_plan.md`*, *`final_summary.md`*). 

Creating duplicate files pollutes repository search indices, degrades RAG vector embeddings, confuses subagents with conflicting historical drafts, and wastes thousands of generation tokens.

The **Persistent Living Artifact Pattern** enforces a single canonical document per domain (e.g. `implementation_plan.md`, `walkthrough.md`) and updates it via **in-place differential edits** (`replace_file_content`), maintaining a pristine single source of truth.

---

## Duplicate Proliferation vs. Single Living Artifact

```
┌─────────────────────────────────────────────────────────────┐
│                 Artifact Lifecycle Comparison               │
│                                                             │
│  Duplicate Proliferation (Anti-Pattern):                    │
│  • Turn 1: `write_to_file("plan_v1.md")` (800 tokens)       │
│  • Turn 5: `write_to_file("plan_v2.md")` (950 tokens)       │
│  • Turn 12: `write_to_file("final_plan.md")` (1,100 tokens) │
│  ↳ 3 duplicate files in repo, 2,850 tokens billed           │
│                                                             │
│  Single Living Artifact (Living Mutation Pattern):          │
│  • Turn 1: `write_to_file("implementation_plan.md")`        │
│  • Turn 5: `replace_file_content("implementation_plan.md")` │
│    ↳ Mutates only the completed phase (45 tokens!)          │
│  • Turn 12: Updates verification status in place            │
│  ↳ 1 canonical file, 92% fewer mutation tokens billed       │
└─────────────────────────────────────────────────────────────┘
```

---

## The 3 Canonical Agent Artifacts

In standard agentic frameworks (Antigravity IDE, Claude Code, Cursor), maintain strictly 3 canonical state documents in the artifact directory:

| Artifact | Purpose | Lifecycle State |
| :--- | :--- | :--- |
| **`implementation_plan.md`** | Technical architecture, step-by-step roadmap, open questions, and verification gates. | Updated in-place as each milestone completes. |
| **`walkthrough.md`** | Final user-facing demo, completed changes diffs, validation logs, and media recordings. | Appended/updated as milestones pass verification. |
| **`scratch/notes.md`** | Temporary scratchpad for ephemeral CLI outputs or quick math. | Disposable; never referenced in user plans. |

---

## In-Place Mutation Recipe

When updating task completion status in `implementation_plan.md`, never rewrite the entire document. Use targeted chunk replacement:

```markdown
<!-- TARGET CONTENT IN implementation_plan.md -->
- [ ] **Phase 2: Database Schema Migration** (Pending)

<!-- REPLACEMENT CONTENT -->
- [x] **Phase 2: Database Schema Migration** (Completed - Migration `20260822_auth` deployed)
```

### Agent Tool Call Example:
```json
{
  "TargetFile": "/path/to/artifacts/implementation_plan.md",
  "Instruction": "Mark Phase 2 as completed and record migration ID",
  "Description": "Update implementation plan milestone status in-place",
  "StartLine": 42,
  "EndLine": 45,
  "TargetContent": "- [ ] **Phase 2: Database Schema Migration** (Pending)",
  "ReplacementContent": "- [x] **Phase 2: Database Schema Migration** (Completed - Migration `20260822_auth` deployed)",
  "AllowMultiple": false
}
```

---

## Metadata Synchronization Standard

Whenever mutating a user-facing artifact, synchronize its `ArtifactMetadata` object to inform the IDE UI without triggering redundant chat messages:

```json
{
  "ArtifactMetadata": {
    "UserFacing": true,
    "RequestFeedback": false,
    "Summary": "Updated implementation plan: Phase 2 database migration completed successfully. Proceeding to Phase 3 API endpoints."
  }
}
```

---

## Benchmark Metrics

| Metric | Ephemeral Re-Creation | Living Mutation Pattern | Improvement |
| :--- | :--- | :--- | :--- |
| **Tokens per Plan Update** | ~900 tokens (Full rewrite) | ~60 tokens (Chunk edit) | **93.3% Reduction** |
| **Repository File Clutter** | 6-10 duplicate `.md` files | 1 canonical file | **Clean Repo State** |
| **RAG / Context Ambiguity** | High (Multiple conflicting plans) | Zero (Single source of truth) | **100% Determinism** |

---

## Agent Operational Directive
> **MANDATORY**: Autonomous agents must NEVER create versioned duplicate artifacts (e.g. `plan2.md`, `summary_new.md`). Always locate the existing canonical document and mutate it in-place.
