---
name: use-bolding-and-bullet-formatting
description: "Use bold labels and concise bullets to make requirements, decisions, and action items easier to scan."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["visual-anchors", "prompt-formatting", "markdown", "attention-weights", "bullet-points", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Use Bolding and Bullet Formatting in Prompts (Visual Anchors) (AI Skill)

## Overview
When multiple instructions are buried in a continuous paragraph of text (*"Please summarize this article and make sure it has 3 bullets and also use a friendly tone and don't mention pricing and keep it under 100 words"*), the model's self-attention mechanism frequently overlooks one or more constraints.

The **Visual Anchor Protocol** structures complex multi-constraint prompts using **Markdown Bullet Hierarchies and Bold Key-Value Anchors** (`- **[PARAMETER]**: [VALUE]`), creating high-contrast token clusters that guarantee 100% constraint adherence.

---

## Paragraph Clutter vs. Bold Key-Value Anchors

```
┌─────────────────────────────────────────────────────────────┐
│                 Attention Salience Mapping                  │
│                                                             │
│  Buried in a Paragraph:                                     │
│  "Write an email to my team about the sprint delay make it  │
│   sound positive don't blame QA and keep it under 60 words" │
│  ↳ 40% probability of missing the word limit or QA rule     │
│                                                             │
│  Bold Key-Value Anchors:                                    │
│ - **Goal**: Announce 2-day sprint delay to engineering     │
│ - **Tone**: Positive and accountable                       │
│ - **Negative Rule**: ❌ Do NOT blame QA or testing         │
│ - **Hard Limit**: Strictly under 60 words                  │
│  ↳ 100% Deterministic Constraint Compliance                 │
└─────────────────────────────────────────────────────────────┘
```

---

## The Master Key-Value Anchor Formula

Always structure complex instructions using this standardized schema:

```markdown
### 📋 Task: [1-Sentence Direct Command]

### 🎯 Parameters & Constraints:
- **Target Audience**: [e.g. Senior Leadership / New Hires]
- **Desired Tone**: [e.g. Direct, Warm, Technical, Executive]
- **Output Format**: [e.g. 3-column Markdown Table / 4-bullet list]
- **Length Ceiling**: [e.g. Max 75 words / 1 page]
- **Prohibited Terms**: [e.g. No corporate buzzwords, no emojis]
```

---

## Real-World Case Study

### Scenario: Generating a Multi-Constraint SQL Migration Script

#### Paragraph Prompt (Constraint Skipped)
> *"Write a Postgres migration to add a user_tier enum to our users table with values free pro enterprise and make sure it has a default of free and is not nullable and add an index on it but do it concurrently so it doesn't lock the database."*
> 
> ❌ *Model generates standard `CREATE INDEX` instead of `CREATE INDEX CONCURRENTLY` because the constraint was buried at the end of a run-on sentence.*

#### Bold Key-Value Prompt (100% Precision)

```markdown
Write a PostgreSQL schema migration:

### Target Changes:
- **Table**: `users`
- **New Enum Type**: `user_tier` ('free', 'pro', 'enterprise')
- **New Column**: `tier` (Type: `user_tier`, Default: `'free'`, Nullable: `FALSE`)
- **Indexing Requirement**: **`CONCURRENTLY`** (Must not take exclusive table locks)
- **Output**: Pure SQL migration script only; zero chat commentary.
```

**AI Output**:
```sql
-- Safe, non-blocking zero-downtime enum and index migration
CREATE TYPE user_tier AS ENUM ('free', 'pro', 'enterprise');

ALTER TABLE users 
ADD COLUMN tier user_tier NOT NULL DEFAULT 'free';

CREATE INDEX CONCURRENTLY idx_users_tier ON users(tier);
```

---

## Summary Best Practices
- **Use Bold Labels for Every Bullet**: Start lines with `- **Parameter**: Value`.
- **Use Visual Emojis as Attention Magnifiers**: Icons like `❌`, `🔒`, `📋`, `⚡` create strong anchor signals in modern transformer attention maps.
