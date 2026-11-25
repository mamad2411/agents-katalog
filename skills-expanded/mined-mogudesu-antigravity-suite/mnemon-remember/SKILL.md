---
name: mnemon-remember
description: >-
  Distil the current conversation into durable memory. Use when the user says remember this, keep this, don't
  forget, from now on, or asks you to save what was just decided — and after a turn that produced a decision,
  a preference, a measurement or a correction worth keeping.
---

# Remember what matters

## 1. Collect candidates from the conversation

Scan the recent turns for facts that will still be true and useful in a week:

| Keep | Skip |
| --- | --- |
| Stated preferences, conventions, working agreements | Anything the user asked as a one-off question |
| Decisions and their reasons | Restatements of what a file already says |
| Corrections to something you previously believed | Values that change every run (timestamps, counts) |
| Measurements, versions, constraints, deadlines | Secrets, tokens, credentials, personal data |
| Entity relationships: who owns what, what depends on what | Your own suggestions the user never accepted |

Also keep the *corrections*: "not X, use Y" is the highest-value memory there is.

## 2. Trim each candidate to one sentence

One fact, one sentence, self-contained. Resolve pronouns: write "the deployment uses pnpm", not "it uses pnpm". Keep the user's own terms for things they named.

## 3. Search before saving

For each candidate run `memory_recall` (`action: "search"`) with its key terms. If an existing memory already says it, do not save it again — the same fact in two places is how a memory store starts lying.

## 4. Save, and let the deduplication decide

Call `memory_save` (`action: "remember"`) for each fact. It answers:

- `added` — new fact stored.
- `merged` — near-identical to an existing memory; the wording was merged, no duplicate was created.
- `duplicate` — already stored; nothing was written.

For a stable preference about the user, prefer `memory_profile` with `action: "set_user"` so it is resident from SessionStart. For a fact that only the next turn needs, use `action: "set_memory"` (or `memory_save` with `action: "journal"`).

## 5. Report the receipt

Answer with one short line per fact, naming where it went, for example:

```
Saved: "Deploys use pnpm" → space toolchain (mem_1f2e3d4c5b)
Merged: "Node pinned to 24.19.0" → space toolchain (added the pnpm detail)
Already known: "Prefers Conventional Commits" — nothing written
```

## 6. When a fact contradicts an existing memory

Do not overwrite silently. Show the user both wordings and propose one of:

1. `memory_manage` (`action: "update"`) — the new statement replaces the old one.
2. `memory_manage` (`action: "forget"`) — the old fact is retired (soft delete, recoverable).
3. Both kept — only when they are true of different scopes, such as two projects.

Apply only what the user picks, then re-run `memory_admin` (`action: "audit"`) to confirm no contradiction is left.
