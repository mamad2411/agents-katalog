---
name: "BrainX V6"
description: |
  Persistent vector memory engine for OpenClaw agents.
  Stores, searches, curates, and optionally injects contextual memories using
  PostgreSQL, pgvector, and OpenAI embeddings. Includes the BrainX OpenClaw
  plugin for optional runtime wiki digest, JIT recall, working memory,
  advisories, and conservative failure capture.
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["psql", "node"]
      env: ["DATABASE_URL", "OPENAI_API_KEY"]
    primaryEnv: "DATABASE_URL"
user-invocable: true
---

# BrainX V6

Use BrainX when an OpenClaw agent needs durable memory, semantic recall, cross-session context, shared knowledge, or memory diagnostics.

## Runtime Split

- **BrainX skill / CLI**: durable memory, retrieval, lifecycle, doctor, cron jobs, knowledge sync, backup/restore, evaluations.
- **BrainX plugin**: optional OpenClaw runtime bridge for wiki digest, working memory, JIT recall, tool advisories, failure capture, and legacy bridge fallback.
- **LLM**: reasoning layer. BrainX supplies context; it does not replace judgment.

## Trust Model

BrainX memory is advisory.

- Prefer live evidence from code, logs, tests, runtime, database state, screenshots, and direct user corrections.
- Use verified memories first.
- Treat hypotheses and changelog memories as context, not authority.
- Exclude obsolete memories from bootstrap and recall surfaces.
- Keep write-path runtime features disabled until explicitly enabled.

## Setup

Required environment:

```bash
DATABASE_URL=postgresql://brainx:change-me@127.0.0.1:5432/brainx
OPENAI_API_KEY=your-openai-api-key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIMENSIONS=1536
```

Install:

```bash
npm install
chmod +x brainx
psql "$DATABASE_URL" -f sql/v3-schema.sql
for file in sql/migrations/*.sql; do psql "$DATABASE_URL" -f "$file"; done
./brainx doctor --full
```

## Core Commands

```bash
./brainx add "memory text" --type note --context project:example --importance 6
./brainx search --query "what should I remember?" --limit 5
./brainx inject "task context to enrich"
./brainx doctor --full --json
./brainx fix
./brainx metrics
./brainx runtime-report
./brainx knowledge-locate --query "deployment checklist"
```

## Plugin Config

Start conservative:

```json
{
  "plugins": {
    "entries": {
      "brainx": {
        "enabled": true,
        "config": {
          "wikiDigest": true,
          "jitRecall": false,
          "workingMemory": false,
          "toolAdvisories": false,
          "captureToolFailures": false,
          "bootstrapMode": "off",
          "captureOutboundMode": "off"
        }
      }
    }
  }
}
```

Enable JIT recall, working memory, advisories, and write-path capture only after privacy and retention rules are clear for the target installation.

## Feature Groups

- Persistent vector memory with PostgreSQL + pgvector
- Semantic search and contextual injection
- Intelligent memory classification
- Hot/warm/cold lifecycle management
- Deduplication, contradiction detection, and supersede chains
- PII scrubbing and sensitivity controls
- Verification states: `verified`, `hypothesis`, `changelog`, `obsolete`
- Quality scoring and feedback loops
- Memory distillation and fact extraction
- Knowledge vault import, sync, and location
- Cross-agent learning with trust gates
- Context packs and wiki digest
- Runtime working memory and JIT recall
- Pre-action advisories
- Conservative tool-failure capture
- Doctor, auto-fix, metrics, and runtime reports
- Backup and restore scripts
- Eval dataset generation and retrieval tests

## Public Distribution Rules

- Do not publish `.env`, database dumps, backups, runtime memory, tool-failure payloads, private knowledge vaults, or local workspace state.
- Do not hardcode private agent names, host paths, or user-specific operating context.
- Keep examples generic and portable.
- Keep secrets in environment variables only.
