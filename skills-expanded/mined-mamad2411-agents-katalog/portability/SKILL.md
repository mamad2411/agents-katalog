---
name: portability
description: >
  Forge kernel data portability — getting issue data in and out of the local kernel. `forge
  export [--dir] [--dry-run]` writes the kernel backlog to deterministic git-tracked JSONL
  (D16 portability projection); `forge export --import` reads that committed snapshot back
  into the kernel (hydrate). `forge migrate --from beads [--dry-run] [--source <dir>]` imports
  a Beads issue store into the kernel — the onboarding path for users coming from Beads. Use
  when the user says "export the kernel backlog to JSONL", "back up / snapshot the backlog",
  "re-import / hydrate the backlog", "migrate from beads", or "import a beads store". Honesty:
  bare `forge migrate --dry-run` (no `--from`) is v2→v3 preview only; a re-import that applies
  nothing reports "already hydrated". NOT the cloud/backend sync of the kernel (that is `forge
  sync`, cloud-native), NOT a database/schema migration (plan/dev), NOT memory notes (memory),
  NOT syncing a git branch with main (ship).
allowed-tools: Bash, Read, Grep, Glob
terminal: true
---

Moving Forge kernel issue data across a boundary: project the backlog to a git-committable snapshot (and hydrate it back), or import an existing issue store into the kernel. This is data portability — distinct from schema/database migrations and from the cloud backend sync (`forge sync`).

# Export / re-import the backlog

```bash
forge export                     # write the kernel backlog to git-tracked JSONL (deterministic)
forge export --dir <path>        # choose the projection directory
forge export --dry-run           # show what would be written, change nothing
forge export --import            # read the committed JSONL snapshot back INTO the kernel (hydrate)
```

`forge export` is the **D16 portability projection**: a deterministic, git-committable snapshot of the backlog you can review in a diff and carry between machines or checkouts. `forge export --import` is the reverse — it hydrates the kernel from that on-disk snapshot; a re-import that finds everything already present reports "already hydrated" rather than claiming it imported anything.

# Migrate in from Beads (or preview v2→v3)

```bash
forge migrate --from beads [--dry-run]     # import a Beads issue store into the kernel
forge migrate --from beads --source <dir>  # point at exported beads *.jsonl (defaults to auto-detecting .beads/)
forge migrate --dry-run                    # preview the v2→v3 migration (the ONLY supported mode without --from)
```

`forge migrate --from beads` is the **onboarding path for users coming from Beads** — it imports a Beads issue store into the Forge Kernel (`--dry-run` reads + maps only, writing nothing). Without `--from`, migrate is **v2→v3 preview only**: `--dry-run` is required and applying the migration is not yet available.

## Boundaries

- The **cloud/backend sync** of the kernel is `forge sync` (cloud-native) — a different operation; this skill is the local, git-based portability projection.
- A **database/schema** migration (adding a column, altering a table) is application work — that's **plan**/**dev**, not `forge migrate`.
- Persisting a decision or note is **memory** (`forge remember`), not export.
- Syncing a git **branch** with main before a PR is **ship**/**worktree**.
