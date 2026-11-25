---
name: create-rule
description: Add a new rule or instruction to the correct location across the multi-tool architecture. Classifies content, determines placement (AGENTS.md, nested AGENTS.md, reference docs, glob-activated rules, CLAUDE.md), handles deduplication, formatting, and cross-tool sync.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Rule

Add a new rule or instruction to the project's AI instruction system. This skill knows the full multi-tool architecture and places content in the right layer with the right format.

## Instructions

### Step 1: Extract the Rule

Parse the user's input to extract:
- **What** — the behavior, constraint, or pattern to enforce
- **Why** — the consequence when violated (financial loss, data corruption, wasted time, repeated feedback)
- **Correct behavior** — what should happen instead

### Step 2: Determine If You Have Enough Context

Check whether you can confidently answer ALL of these:

1. **Scope**: Does this apply project-wide, to one directory, or across specific file types?
2. **Audience**: Is this for all AI tools or Claude Code only?
3. **Activation**: Should it load always, on-demand, or when specific files are touched?

**If all three are clear** (e.g., an agent providing full context like "add a testing rule about fixture disposal that should trigger when working on test files") — skip to Step 4.

**If any are ambiguous** — proceed to Step 3.

### Step 3: Ask Diagnostic Questions (only when needed)

Ask **only** the questions you cannot answer from context. Do not ask questions whose answer is obvious from the input. Frame each question with the options and a recommended default based on what you already know.

Useful diagnostic questions (pick the ones that actually matter for this case):

- "Does this apply everywhere, or only when working in [specific directory]?"
- "Is this about [specific file types like handlers, tests, configs], or about the project in general?"
- "Is this a coding pattern (how to write code) or a process rule (how to work)?"
- "Should other AI tools (Cursor, Codex) also follow this, or is it Claude-specific?"

One round of questions maximum. If still unclear after answers, make a reasonable judgment call and note your assumption.

### Step 4: Search for Existing Rules First

**The default action is to update an existing rule, not create a new one.** Most lessons refine, extend, or sharpen something that's already partially covered. A new rule entry is the exception.

Read ALL files in the target layer and adjacent layers:
- All files in `.agents/rules/`
- Any topic reference docs in `.agents/*.md`
- `AGENTS.md` (root)
- The nested `AGENTS.md` most relevant to the topic (if applicable)
- `CLAUDE.md` (if potentially Claude-specific)

For each, search for rules that cover the same concept, entity, or pattern — even if the wording is different. Then:

- **Exact duplicate** — already covered. Tell the user and stop.
- **Partial overlap** — the existing rule covers the concept but misses this specific case. **Update the existing rule** to incorporate the new lesson. This is the most common outcome.
- **Wrong file** — a rule exists but in the wrong layer (e.g., a directory-scoped rule in a glob-activated file). Move it to the correct location as part of the update.
- **No overlap** — genuinely new concept not covered anywhere. Only then create a new rule entry.

### Step 5: Classify and Place

Use this decision tree (first match wins):

#### Is it Claude Code-specific?

Content that ONLY applies to Claude Code — skill references, `.claude/` paths, MCP tools, GitHub comment prefix, `ask_human` usage, agents mode behavior.

**→ `CLAUDE.md`** (root, ~22 lines currently)

#### Is it universal knowledge that applies regardless of files touched?

If yes, decide between AGENTS.md (inline) and a reference doc (`.agents/*.md`):

**Inline in AGENTS.md** when:
- It's a brief principle or reminder (1-2 bullet points)
- It's an actionable instruction ("use X, not Y")
- Developers need it top-of-mind every session
- Examples: a one-line "use X not Y" rule, a "Before Implementing" checklist, the project's standard build/test commands

**Reference doc in `.agents/`** when:
- It needs explanation, reasoning, examples, or anti-patterns (more than 2-3 lines)
- It's a collection of related patterns that form a coherent topic
- Developers consult it when implementing, not every session
- The topic already has an existing reference doc to extend
- Examples: architecture patterns, handler separation rules, security patterns, domain-specific safety rules

The pattern is: AGENTS.md carries the brief reminder + a pointer, the reference doc carries the detail. AGENTS.md typically says *"These contain essential rules that apply to all code. Read the relevant file before implementing any feature:"* and lists the relevant `.agents/*.md` files.

**Existing reference docs** (check before creating a new one): list whatever `.agents/*.md` topic files the repository already maintains.

If the content fits an existing reference doc, add it there. Only create a new `.agents/{topic}.md` when the topic is distinct from existing docs, and add a pointer from AGENTS.md.

**→ `AGENTS.md`** for brief inline rules, **→ `.agents/*.md`** for detailed reference material

#### Is it specific to one directory tree?

Only relevant to one project (a host, UI library, or integration directory).

**→ Nested `AGENTS.md`** in that directory. Examples follow the pattern `path/to/scope/AGENTS.md`, e.g. `src/integrations/AGENTS.md`, `apps/web/AGENTS.md`, `services/worker/AGENTS.md`.

Note: Cursor cannot read nested AGENTS.md. If this rule is critical for Cursor users too, use a glob-activated rule file instead.

#### Does it span multiple directories via file name patterns?

Cross-cutting patterns that activate when matching files are read (handlers, tests, configs, etc.).

**→ `.agents/rules/{topic}.md`**

Map to an existing file in `.agents/rules/` if there is a topical fit, or create a new one. A glob-activated rule file looks like:

```markdown
---
description: "What this rule covers"
paths:
  - "**/*Handler*"
  - "src/{topic}/**"
globs:
  - "**/*Handler*"
  - "src/{topic}/**"
---
```

If no existing file fits, create a new rule file.

#### Is it a workflow, not a constraint?

Multi-step process → tell the user this needs a skill (`.agents/skills/`), not a rule.

#### Must it be enforced 100%?

Deterministic enforcement → tell the user to configure a hook in `settings.json`. Rules are probabilistic; hooks are deterministic.

### Step 6: Write the Rule

Use the exact format for the target destination:

---

#### Format: `.agents/rules/*.md` (glob-activated rule file)

Frontmatter + markdown sections. `paths:` and `globs:` values are identical.

```markdown
---
description: "One-line summary of what this rule file covers"
paths:
  - "**/*Handler*"
  - "**/*Request*"
globs:
  - "**/*Handler*"
  - "**/*Request*"
---

# Title

Brief intro sentence referencing relevant docs.

## Rule Name

Rule text with reasoning ("because ..."). One concern per section. Concrete wrong-vs-right examples for judgment calls. Reference docs when detailed explanation exists elsewhere.
```

---

#### Format: `AGENTS.md` (root, always-loaded)

Plain markdown. No frontmatter. Brief — every line costs context window for every session across every tool.

```markdown
## Section Name

- Bullet point with reasoning. Keep to 1-2 lines per rule.
- Another rule. Reference detailed docs: see `docs/path/to/guide.md`.
```

---

#### Format: `CLAUDE.md` (Claude Code-specific)

Plain markdown. No frontmatter. Only Claude-specific content.

```markdown
## Section Name

Description of Claude-specific behavior or tooling reference.
```

---

#### Format: `.agents/*.md` (reference doc)

Plain markdown. No frontmatter. Starts with a title and one-line description. Detailed sections with reasoning.

```markdown
# Title

One-line description — read before implementing [topic]. Referenced from root AGENTS.md.

## Rule Name

Detailed explanation with reasoning, context, and examples. These are longer than rule file entries because they serve as reference material.
```

---

#### Format: Nested `AGENTS.md` (directory-scoped)

Plain markdown. No frontmatter. Project-specific conventions with sections.

```markdown
# Project Name

Brief description of this project's purpose and architecture.

## Section Name

Directory-specific rules and conventions. Can be longer than root AGENTS.md since it only loads when working in this directory.

## Scar Tissue

### Specific Bug or Pattern Name

Explanation of what went wrong, why, and the correct approach. These are lessons learned from incidents specific to this project.
```

---

#### Style Rules (all formats)

- **No emphasis markers** — no NEVER, MUST, CRITICAL, ALWAYS in caps. Use normal phrasing with reasoning.
- **Include "because"** — explain the motivation so the AI can generalize. A rule that names a failure mode and the safer alternative is far more useful than a bare directive.
- **One concern per rule** — don't combine unrelated instructions in one section.
- **Concrete examples for judgment calls** — show wrong vs right when the rule requires design judgment.
- **Reference docs** when detailed explanation exists elsewhere — "See `docs/path/to/guide.md`" avoids duplication.

Place the rule in a logical position within the file — group with related rules, not at the bottom.

### Step 7: Sync (if `.agents/rules/` was modified)

After writing or updating any file in `.agents/rules/`, always run `just ai-sync` to regenerate the tool-specific copies:
- `.claude/rules/*.md` — Claude Code format (`paths:` frontmatter only)
- `.cursor/rules/*.mdc` — Cursor format (`globs:` + `description:` + `alwaysApply:`)

This step is mandatory — do not skip it or leave it for the user. The agent must run the sync command itself as part of the workflow.

Not needed for AGENTS.md, CLAUDE.md, nested AGENTS.md, or reference docs — those are read directly by the tools without any sync step.

### Step 8: Summarize

```
Action: {Updated existing rule | Created new rule | Moved rule to correct layer}
File: {path}
Layer: {Root AGENTS.md | CLAUDE.md | Nested AGENTS.md | Reference doc | Glob-activated rule}
Rule: {one-line summary}
Visibility: {which tools see it — e.g., "All tools" or "Claude only" or "Claude + Cursor + Copilot"}
Sync: {ran just ai-sync | not needed}
```

## Cross-Tool Reference

How each tool discovers instructions and rules:

| Tool | Instructions | Rules | Nested AGENTS.md? |
|------|-------------|-------|--------------------|
| Claude Code | `CLAUDE.md` → `@AGENTS.md` | `.claude/rules/*.md` (`paths:`) | Yes (via CLAUDE.md wrapper) |
| Cursor | `AGENTS.md` natively | `.cursor/rules/*.mdc` (`globs:`) | No |
| Codex | `AGENTS.md` via config | No rules system | Yes (concatenates all) |
| Copilot | `AGENTS.md` + `.claude/rules/` | `.claude/rules/` natively | Yes |
| OpenCode | `AGENTS.md` natively | Via instructions glob config | Yes |

## Critical Rules

- **Update before create** — the default outcome is updating an existing rule. Only create a new entry when the concept is genuinely not covered anywhere.
- AGENTS.md must stay tool-agnostic. Claude-specific content goes in CLAUDE.md only.
- `.agents/rules/` is exclusively for cross-cutting glob patterns. Directory-scoped content goes in nested AGENTS.md.
- No always-loaded rule files. Universal content goes in AGENTS.md or reference docs.
- Always run `just ai-sync` after editing `.agents/rules/`.
- If a rule file exceeds ~50 rules, warn and suggest splitting.
