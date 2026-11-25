---
name: project-memory-writing
description: "Write and update atomic project memories in .agent_lessons/ — YAML frontmatter schema (tags, status, scope, confidence, author, backlinks), vault location, search-before-create, and pinning cited line numbers to a commit."
triggers:
  - "save a finding as a memory"
  - ".agent_lessons"
  - "project memory frontmatter"
  - "before delivering final result"
  - "memory line numbers stale"
version: 1.1.2
---

# Project Memory Writing Guide

Project memories are atomic facts, stored as markdown files in `.agent_lessons/` vaults. Write them so the next agent can find and understand them instantly.

## Vault location

Each project has its own vault:
- **Workspace (global):** `AgentWorkspace/.agent_lessons/` — cross-project or general findings
- **Project vaults:** `<project-repo>/.agent_lessons/` — findings specific to that project (e.g. `Strata/.agent_lessons/`, `llama.cpp/.agent_lessons/`)

**Rule of thumb:** if the finding is only true for one project, put it in that project's vault. If it's cross-project (e.g. a framework pattern), put it in the workspace vault. When in doubt, workspace.

## Frontmatter schema (YAML)

```yaml
---
tags: [compression, logging, tail-sync]              # REQUIRED: 3-5 tags for categorization
scope: [global, strata]                               # REQUIRED: vault default + project tags (union rule)
aliases: [log-tail-invariant]                         # OPTIONAL: discoverability via grep/search
related: [[compression-pool-desync-fix]]             # OPTIONAL: Obsidian-style backlinks
status: active                                        # OPTIONAL: active | superseded | archived (default: active)
superseded_by: [[new-canonical]]                      # present iff status: superseded
supersedes: [[old-lesson]]                           # on the survivor, iff it replaces an older memory
confidence: verified                                  # REQUIRED: verified | likely | unconfirmed | deprecated
author: orchestrator_Maine_20260917_222359.jsonl     # REQUIRED: JSONL log filename of the creating agent
contributors:                                         # OPTIONAL: agents who substantially updated this file
  - coder_worker1_20260918_103045.jsonl
last_validated: 2026-11-11                            # OPTIONAL: ISO date of last audit/re-verification
---
```

### Field semantics

| Field | Purpose |
|---|---|
| `status:` | **Lifecycle state.** Drives the de-index filter: only `superseded` and `archived` are excluded from hinting. Everything else (including `active`, missing, or legacy free-form values) stays active. |
| `confidence:` | **Epistemic state.** How well-supported the fact is. `deprecated` means the fact no longer holds, but the file stays on disk and greppable. |
| `scope:` | **Eligibility.** Which project contexts this memory is relevant to. Union of vault default + project tags. `global` means always eligible. |
| `related:` | **Backlinks.** Bidirectional in practice — linking a new memory to an existing one makes it discoverable from the existing one. |
| `hub:` | **Set by consolidation, not by the writer.** Indicates which summary hub this leaf belongs to. You do not set this field manually. |

### `status:` vs `confidence:` — when to use which

- **`status: superseded`** — a *newer, better* memory replaces this one. The old file stays on disk but is de-indexed (hidden from hints). Add `superseded_by: [[new-file]]`.
- **`status: archived`** — historically interesting but no longer actionable (e.g. the code it describes was removed). De-indexed.
- **`confidence: deprecated`** — the *fact itself* no longer holds, but there's no single replacement memory. The file stays active (still hinted) so agents know the fact was once true.
- **`confidence: unconfirmed`** — speculative, needs verification.

## Search before creating

Before writing a new memory, search the relevant `.agent_lessons/` vault(s) to avoid duplicates: grep key terms (component name, error type). Search **every** vault that could hold the fact — a project repo and the workspace often each have their own, and the same fact may already exist in the other. If you find a related existing memory, update it instead of creating a duplicate. If distinct but related, create the new one and add a `[[related-memory]]` backlink.

## Pin every cited line number to a commit

**Line numbers in a memory go stale silently.** A memory written against commit A is read months later against commit B, and every `file:line` in it is now wrong — usually by a large, uniform offset, which looks authoritative and is therefore trusted.

- State the pin **in the body**, not just implicitly: "At `<repo>` @ `<full SHA>`:" before the first citation. A memory without a pin is a claim about no tree in particular.
- Prefer **symbol-anchored** citations over pure line numbers where possible: `has_stage_parts` (`file.cpp:798-802`) — the name survives drift, the number does not.
- When **reading** a memory, treat its line numbers as stale until you re-verify them against the current tree. Re-derive from the symbol.
- When **updating** a memory after the tree moves, add a dated addendum with the new SHA rather than silently rewriting the numbers.

## Updating existing memories

- **Adding new info:** edit the file and append your finding with context. Add your JSONL log filename to `contributors:` if you made a substantial update.
- **Contradictory info:** add a note explaining the conflict; update `confidence:` if needed.
- **Superseded by a newer memory:** set `status: superseded` + `superseded_by: [[new-memory]]` on the old file; add `supersedes: [[old-memory]]` on the new file. The old file stays on disk (greppable) but is de-indexed from hints.
- **Fact no longer holds (no single replacement):** set `confidence: deprecated` with an explanation. The file stays active.
- **Stale code reference:** if the cited symbol/path no longer exists in the live tree, set `status: archived` and write the grep command + date in the body.
- **Don't delete old memories** — add clarifying context or de-index them.

## Content guidelines

- **One atomic fact per file**; name files descriptively in kebab-case (e.g. `compression-tail-invariant.md`).
- Start with a clear statement of the fact; include evidence (code refs, line numbers — pinned, see above).
- Use `[[backlinks]]` to connect related memories; keep it concise — quick reference, not narrative.
- Set `scope:` correctly: a file in the Strata vault with no project tags gets `scope: [strata]`; a workspace file tagged `strata` gets `scope: [global, strata]`.

## When to create a memory

Root-cause analysis completed, architecture decision made, or non-obvious behavior discovered — anything you'd want the next agent working on this project to know immediately.

## Tips

- A memory that says "X is blocked by guard Y at `:10444`" is dangerous without a pin: the guard may have moved or been removed. Say "guard Y (`generate.cpp:10444` at SHA …)" or state the guard's *name* and let the reader grep it.
- Negative findings are high-value memories and need their proof method recorded: "field X appears **zero** times in file.cpp (whole-file grep)" is re-checkable; "the format does not support X" is not.
- Link a memory to the report file it feeds, so the full analysis is reachable from the atomic fact and vice versa.
- `status:` and `confidence:` are orthogonal: a memory can be `status: active` + `confidence: deprecated` (the fact was true but is now outdated, still hinted so agents know) or `status: superseded` + `confidence: verified` (the fact was solid, but a better memory replaced it, de-indexed).
- **Vault frontmatter is NOT strict-YAML on purpose.** `related:`/`superseded_by:`/`supersedes:` use Obsidian `[[...]]` backlinks, and the schema's inline `#` comments are also not strict-YAML; both fail `yaml.safe_load` but the AC memory indexer parses them correctly. If a self-check `yaml.safe_load` on a memory file raises a parse error pointing at a `[[...]]` or `#`-comment line, that is the **existing** vault syntax, not a defect you introduced — do NOT quote/escape it to "fix" it, which breaks the indexer's link extraction. Compare against an unmodified backup to confirm the offending line pre-exists your edit, and validate only the lines YOU added (e.g. a new `contributors:` block) for well-formedness.
