---
name: oracle
description: >-
  Second-model review pattern: bundle a prompt plus relevant files and send to
  a separate model for cross-validation, debugging, design checks, or independent
  analysis. Use when you want an opinion from a different model than the one
  currently running — debugging hard problems, validating architecture decisions,
  or getting a fresh read on a refactor.
metadata:
  version: "0.3.0"
  attribution: "pattern adapted from steipete/agent-skills (oracle)"
---

# Oracle — Second-Model Review

Bundle your prompt + relevant files into one "one-shot" request and send to
another model. Treat all outputs as **advisory**: verify against the codebase
and tests before acting.

## When to use

- Stuck on a hard bug and want a second opinion without sharing full context
- Architecture decision that benefits from a fresh model's read
- Refactor plan you want cross-validated before executing
- Any situation where model A is too familiar with the problem to see it clearly

## Approaches

### Option A: `code2prompt` (recommended)

Rust CLI — single binary, token counting, git integration, Handlebars templates.

```bash
cargo install code2prompt
```

```bash
# Bundle dir → clipboard (default)
code2prompt src/

# Save to file
code2prompt src/ --output-file /tmp/bundle.txt

# Include/exclude patterns (glob)
code2prompt src/ --include "*.rs" --exclude "*.test.rs"

# Show token count before sending
code2prompt src/ --tokens

# Include git diff in bundle
code2prompt . --diff

# Custom Handlebars template
code2prompt src/ --template templates/review.hbs
```

Project-level config: `.c2pconfig` at repo root.

Run `code2prompt --help` for full flag reference. TUI available for interactive selection.

### Option B: Agent tool with model override

Within Claude Code, spawn a subagent on a different model tier:

```javascript
// In a Workflow script
const review = await agent(
  `Review this design: <context>. Question: <question>`,
  { model: 'opus', label: 'second-opinion' }
)
```

## Writing a high-signal prompt

Any second-model review starts with **zero** project knowledge.
Include everything needed to answer cold:

1. **Project briefing** — stack, build/test commands, platform constraints
2. **Where things live** — key directories, entrypoints, config files
3. **Exact question** — what you tried, the error text verbatim
4. **Constraints** — "don't change X", "must keep public API", "perf budget"
5. **Desired output** — "return patch plan", "list risky assumptions", "give 3 options with tradeoffs"

### Exhaustive prompt pattern (long investigations)

When the problem may need multiple rounds, write a prompt that stands alone:

- **Top**: 6–30 sentence project briefing + current goal
- **Middle**: concrete repro steps + exact errors + what you already tried
- **Bottom**: all context files needed (entrypoints, configs, key modules, docs)

Make the prompt re-runnable — the model has no memory of prior exchanges.

## Discipline

- **Tight file set**: fewest files that contain the truth. Whole-repo dumps add noise, not signal.
- **No secrets**: never attach `.env`, key files, auth tokens. Redact before sending.
- **Advisory only**: verify outputs against the actual codebase before acting. The model cannot run your tests.
