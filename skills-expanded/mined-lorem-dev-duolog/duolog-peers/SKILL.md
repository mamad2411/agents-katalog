---
name: duolog-peers
description: Use only in a project that has .duolog/config.yaml. List the running duolog peers and delegate runs, or switch the person's Rex view to one, when the person asks which run or to see one.
metadata:
  duolog-version: "1.11.1"
---

Stop unless this project has `.duolog/config.yaml`.

# See duolog peers

Use when the person asks which peers or delegate runs run, or to see one.

- Which run: run `duolog runs --long`, one table with a `peer` or
  `delegate` column; pass on its lines. `duolog runs --snapshot` prints the
  same as one JSON line.
- Show one: run `duolog watch --tab <id>` only when the person asks; pass on
  its one line. For a peer it is `duolog peer view <id>`. Tell them to look
  and not to type in that tab. A run's tab closes when the run ends.
- Never run `duolog watch` or `duolog peer show` without `--tab`, or
  `duolog runs tail`, and never work around their refusal: they keep a
  peer's screen and a worker's stream out of your context. The refusal
  guards against accidents. It is not a barrier: getting past it would take
  a workaround on purpose.
- `duolog statusline` is for Claude Code's status line; do not run it.

This skill costs one model turn. In Claude Code, the person can skip it with
`! duolog runs --long` or the `/duolog-pane` pane. In Codex, run these
commands outside the sandbox.
