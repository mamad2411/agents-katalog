---
name: brain-dump
description: Ultra-frictionless stream-of-consciousness capture for ADHD minds. Accepts raw unstructured text and parses it into discrete vault items — bugs, tasks, features, ideas, business thoughts, personal errands, learning goals, creative sparks. Works across ALL life domains, not just code. Use when the user says "brain dump", "let me dump", "I've been thinking", "dump my thoughts", or invokes /brain-dump. Also use when the user starts streaming multiple unrelated thoughts in rapid succession. The key is ZERO friction — accept anything, sort it out, confirm what was captured.
---

# Brain Dump

Accept a stream of consciousness. Parse it into vault items. Confirm. Done.

**CRITICAL RULE: Do NOT ask questions before capturing. Accept everything first, sort it out, then offer corrections. The user's ADHD brain will move on if you interrupt the flow.**

## Vault Path

`{{VAULT_PATH}}`

## Domain Detection (Per-Item)

Every item gets classified into a **domain** first, then a type. Domain determines which vault folder it routes to.

### Domain keywords (case-insensitive)

**business**: revenue, marketing, pricing, partnership, hire, hiring, sales, invoice, supplier, customer, accountant, tax, ABN, cash flow, profit, expense, quote, contract, stock levels, wholesale, retail, margin, payroll, BAS, GST, bookkeeper, inventory levels, reorder, supplier agreement

**personal**: call, appointment, dentist, doctor, buy, pick up, birthday, gym, car, rego, insurance, house, family, kids, wife, groceries, errands, book in, schedule, renew, pay bill, mechanic, vet, school, pharmacy, plumber, electrician

**learning**: learn, read, article, course, tutorial, look into, research, study, watch, book, podcast, upskill, investigate, explore how, deep dive, training, certification, MDN, docs

**creative**: app idea, side project, what if we built, new product, startup, SaaS, new business, product idea, spin off, monetize, business model, MVP

**dev**: matches any Known Project Keyword below, OR mentions code, bug, deploy, API, endpoint, migration, refactor, test, build, merge, PR, branch, commit, server, database, component, webhook, sync, cron

### Priority order for domain detection:
1. Check if item text matches dev project keywords → domain: `dev`
2. Check if item text matches life domain keywords → that domain
3. If ambiguous between domains, prefer `dev` if in a project CWD, otherwise `general` → routes to `00-Inbox`

## Project Inference (Per-Item, dev domain only)

For items classified as `dev` domain, infer the project:

### Priority order:
1. **Explicit mention**: "on my-project", "in my-project", "for cortex"
2. **Project keyword match**: scan against Known Project Keywords table
3. **Inherit from context**: previous item in same dump named a project and topic continues
4. **CWD fallback**: use CWD mapping if nothing else matches
5. **Last resort**: `general`

### Known Project Keywords

| Keywords (case-insensitive) | Project |
|---|---|
| my-project, help desk, HD | my-project |
| my-project, gun desk, GD, firearm, firearms | my-project |
| flexi, flexible deposits, flex deposits | my-project |
| addons, my-project, flexi addons | my-project |
| banners, shopify banners, my-project | my-project |
| bundles, bundle deals, my-project | my-project |
| cortex | cortex |

### CWD Fallback (only if text-based inference fails)

| CWD contains | Project |
|---|---|
| `{{PROJECT_DIR}}` | my-project |
| `{{PROJECT_DIR}}` | my-project |
| `{{PROJECT_DIR}}` | my-project |
| `{{PROJECT_DIR}}` | my-project |
| `{{PROJECT_DIR}}` | my-project |
| `{{PROJECT_DIR}}` | my-project |
| `my-project` or `gun-desk` | my-project |
| `cortex` | cortex |
| Otherwise | `general` |

## Step 1: Accept Raw Input

The user's message IS the brain dump. Their text after `/brain-dump` is the content.

If the message seems to end mid-thought (trailing "and", "also", incomplete sentence), say:

> Keep going, I'm listening.

Wait for more input. Accumulate all messages until the user signals done: "that's it", "done", "ok go", "process that", or sends a clearly separate instruction.

If the input is complete, proceed immediately — do not prompt for more.

## Step 2: Parse into Discrete Items

Split the stream into individual actionable items. Each item gets **independently classified** — do not assume all items are the same type or domain.

### Splitting rules

Look for:
- **Sentence boundaries** and topic shifts
- **Signal phrases**: "also", "oh and", "another thing", "what about", "I should", "we need to", "bug:", "idea:", "todo:", "feature:", "maybe we could"
- **Batched-prefix patterns**: When the user says "bugs on my-project: X, Y, Z" — parse X, Y, Z as **separate items**, all inheriting the prefix type (bug) and project (my-project). Same for "personal stuff: call dentist, buy milk, renew rego" → 3 separate personal items.
- **Comma/and-separated lists** after a type prefix: "the login is broken, the search is slow, and the export times out" → 3 separate bugs

### Type classification

Each item is independently classified. Do NOT lock into one type for the whole dump.

- **bug**: "X is broken" / "X doesn't work" / "X crashes" / "X throws an error" / "X is wrong" / "bug:"
- **task**: "we should Y" / "need to Y" / "todo: Y" / "set up" / "add" / "implement" / "migrate" / "refactor" / "call X" / "buy X" / "book in X" / "renew X"
- **feature**: "feature request" / "customers want" / "users should be able to" / "we need a feature for" / "it would be great if users could" / "feature:"
- **idea**: "what if Z" / "maybe we could Z" / "would be cool if" / "I wonder if" / "idea:" / "explore" / "what about"
- **note**: "should we A or B?" / "I decided to" / "remember that" / "note:" / decisions / questions

When the user sets a type context ("here are the bugs", "bugs:"), treat subsequent items as that type **until** the type clearly shifts. But stay flexible — if an item within a "bugs" batch is clearly an idea, classify it as an idea.

### Priority inference

- "critical" / "urgent" / "production" / "breaking" / "customers are" / "today" / "ASAP" → **high**
- "annoying" / "should fix" / "need to" / "important" / "this week" → **medium**
- "would be nice" / "someday" / "maybe" / "what if" / "low priority" / "eventually" → **low**
- Default: **medium** for bugs/tasks/features, **low** for ideas

### Per-item extraction

For each parsed item, extract:
- **raw_text**: exact words from the dump
- **domain**: dev, business, personal, learning, creative
- **type**: bug, task, feature, idea, note
- **priority**: inferred from urgency language
- **project**: inferred per-item (dev domain only; life domains use `general`)
- **summary**: 1-sentence cleaned-up version

**Parse generously.** If something could be 1 item or 2, make it 2. Better to capture too much than miss something. When truly ambiguous, create an inbox item (type: note, domain based on best guess).

## Step 3: Batch Duplicate Check

For each parsed item, search for similar existing items:

```
mcp__vault-index__search_vault(query="{key terms from summary}")
```

If a strong duplicate is found (same type + project + very similar description), note it but **do NOT block creation**. Flag it in the confirmation table with `[DUP?]`. The user can decide.

## Step 4: Create Vault Items

For each parsed item, create a file following vault-capture conventions:

**Filename**: `YYYYMMDD-HHmmss-{type}-{slug}-{NNN}.md`
- slug: kebab-case summary, max 6 words
- NNN: 3-digit counter (001, 002, 003) to prevent filename collisions when creating multiple items

**Smart routing by domain**:

| Domain | Type | Folder |
|---|---|---|
| dev | bug | `01-Bugs/` |
| dev | task | `02-Tasks/` |
| dev | feature | `00-Inbox/` (needs human design decisions) |
| dev | idea | `03-Ideas/` |
| dev | note | `00-Inbox/` |
| business | any | `06-Business/` |
| personal | any | `07-Personal/` |
| learning | any | `08-Learning/` |
| creative | any | `09-Creative/` |
| ambiguous | any | `00-Inbox/` |

**Frontmatter**:
```yaml
---
type: {type}
domain: {domain}
priority: {priority}
project: {project or "general"}
module: ""
agent: human
status: open
branch: n/a
created: {ISO 8601 timestamp}
updated: {ISO 8601 timestamp}
complexity: {low|medium|high, only for dev bugs and tasks}
blocked-by: []
related: []
tags:
  - brain-dump
---
```

**Body**:
```markdown
## Summary
{cleaned-up 1-sentence summary}

## Raw Capture
> {exact words from the brain dump}
```

Write all files, then re-index ONCE:

```
mcp__vault-index__index_vault(incremental=true)
```

## Step 5: Confirm with Summary Table

Present a compact confirmation:

```
Captured {N} items from your brain dump:

| # | Domain   | Type    | Project  | Priority | Routed To   | Summary                    | Flag   |
|---|----------|---------|----------|----------|-------------|----------------------------|--------|
| 1 | dev      | bug     | my-project | high     | 01-Bugs     | PO approval fails on...    |        |
| 2 | personal | task    | general  | medium   | 07-Personal | Call the accountant        |        |
| 3 | learning | idea    | general  | low      | 08-Learning | Look into Rust for APIs    |        |
| 4 | creative | idea    | general  | low      | 09-Creative | SaaS for gun dealers       |        |
| 5 | business | task    | general  | medium   | 06-Business | Review supplier pricing    | [DUP?] |

Anything I got wrong? "fix 3: it's a dev task for cortex" / "delete 2" / "looks good" / or just move on.
```

## Step 6: Accept Corrections (optional)

If the user offers corrections, apply them:

- **"fix N: {change}"** — update the item (re-read, edit frontmatter/content, re-write, re-index)
- **"delete N"** — remove the file, re-index
- **"merge N and M"** — combine into one item, delete the other, re-index
- **"move N to {project}"** — update project field, re-index
- **"N is a bug not a task"** — change type, re-route to correct folder if needed, re-index
- **"N is personal not business"** — change domain, re-route to correct folder, re-index
- **"looks good"** / no response / moves on — done, no action needed

After corrections, show the updated table.

## Design Principles

1. **Zero friction** — never ask before capturing. The flow must not be interrupted.
2. **Parse generously** — when in doubt, create an item. Deleting is easier than remembering.
3. **Per-item intelligence** — each item gets its own domain, type, project, and priority. Don't assume uniformity.
4. **Life is not just code** — business, personal, learning, and creative items are first-class citizens.
5. **Tag everything** — all brain-dump items get the `brain-dump` tag so they can be filtered later.
6. **Respect the vault schema** — reuse the exact same frontmatter format as vault-capture for consistency.
7. **One re-index** — batch all file creation, then index once at the end.
