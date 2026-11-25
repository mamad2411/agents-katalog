---
name: cursor-weekly-review
description: Produce a weekly synthesis of authored commits with highlights by bugfix, tech debt, and net-new work
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Weekly review

## Trigger

Need a weekly recap of shipped work for status updates, retros, or planning.

## Workflow

1. Determine the current git user email from repo config.
2. Collect authored commits from the last 7-10 days on the primary branch context.
3. Exclude merge commits.
4. Group meaningful changes into 2-5 concise bullets.
5. Add a short classification paragraph covering:
   - likely bug fixes
   - likely tech debt work
   - likely net-new functionality

## Guardrails

- Keep the recap short and executive-readable.
- Base claims only on commit history and diffs.
- If git email is missing, ask the user to set it before proceeding.

## Output

- 2-5 bullet weekly summary
- Brief classification paragraph (bugfix / tech debt / net-new)
