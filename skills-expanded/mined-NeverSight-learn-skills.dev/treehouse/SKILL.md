---
name: treehouse
description: "Operate a pool of reusable git worktrees through the treehouse CLI: lease an isolated worktree non-interactively, read pool state, return a lease, and reclaim slots with prune or destroy. Use whenever work needs an isolated checkout, a pool is full, a slot is stuck dirty or leased, or a worktree path under a .treehouse/ directory needs explaining."
user-invocable: false
---

# treehouse

Pool manager for reusable git worktrees (and, with the opt-in jj backend, Jujutsu workspaces).
A pool slot is a real worktree of the clone that created it, reset and handed back out instead of being recreated.

Every command takes `--help`, and per-subcommand help is good; this skill only covers what `--help` cannot know.
Set `TREEHOUSE_NO_UPDATE_CHECK=1` in scripted use so the update-available banner stays out of captured output.

## When to reach for it

- Need an isolated checkout for a parallel agent, a build, or a risky experiment: lease one with `treehouse get --lease`. Never `git worktree add` by hand into a directory a pool manages.
- Already sitting in a worktree handed to you: use treehouse only to *read* state. Ordinary git commands (branch, commit, push) are unchanged inside a slot.
- One-off scratch clone that nothing else shares: plain `git clone` or `git worktree add` is simpler. A pool earns its keep when slots are acquired and released repeatedly.
- Bare `treehouse` with no arguments is **not** a status probe. It is an alias for `get`, so it acquires a slot and opens an interactive subshell. Use `treehouse status` to look.

## Workflows

All command output below was reproduced against `treehouse v2.1.0`.

**Read a pool without touching it.** Run from the clone that owns the pool, not from inside a slot (see Fleet conventions).

```bash
treehouse status          # human table: name, status, path, holder or processes
treehouse status --json   # machine-readable; the only structured read in the CLI
```

**Lease a worktree non-interactively.** This is the agent path: no subshell, path on stdout, banners on stderr.

```bash
WT=$(treehouse get --lease --lease-holder my-task-id)   # stdout is the path alone
treehouse get --lease --json --lease-holder my-task-id  # path + lease_id + holder + timestamp
```

A lease is process-independent: it survives with zero processes in the worktree, and nothing reclaims it automatically. Always pair an acquire with a return.

**Return a lease safely.** Use the conditional form when another agent might hold the slot by now; it refuses rather than stealing.

```bash
LID=$(treehouse status --json | jq -r '.[] | select(.name=="1") | .lease_id')
treehouse return --if-lease-id "$LID" "$WT"   # exit 1 if the lease moved on
treehouse return --force "$WT"                # unconditional; discards uncommitted work
```

`--force` resolves the pool that actually contains an absolute path, so it works after a pool has been re-rooted. `return` is idempotent: returning an already-returned slot exits 0.

**Diagnose a full pool.** Exhaustion is the common failure, and the error already carries the numbers.

```bash
treehouse get --lease
# all 3 worktrees are in use or dirty (max_trees = 3). Run 'treehouse status' to see details, ...
treehouse status   # which slots are leased, dirty, in-use, or damaged
```

A `dirty` slot is not reusable and is never auto-cleaned. Either commit and push the work, or reclaim the slot with `treehouse return --force <path>`, which discards it.

**Reclaim slots, dry-run first.** Both `prune` and `destroy` are dry-run unless `--yes`, and both refuse anything risky by default.

```bash
treehouse prune                              # dry run: stale, clean, merged, unleased slots only
treehouse destroy <pool-dir> --all           # dry run: same disposable set, grouped by skip reason
treehouse destroy <pool-dir> --all --yes     # removes only the disposable set
treehouse destroy <path> --include-leased --yes   # a leased slot, one exact path, never via --all
```

The skip lines name the exact flag that would include each class (`--include-unlanded`, `--include-in-use`, `--include-leased`), so read the dry run before adding a flag. A bulk skip exits 0; a single named target that gets skipped exits 1.

**Exercise a lifecycle command safely.** Never rehearse destroy, prune, or a config change on a pool other agents are in. Build a throwaway one:

```bash
mkdir -p /tmp/th-scratch/repo && cd /tmp/th-scratch/repo
git init -q -b main . && git commit -q --allow-empty -m init
printf 'max_trees = 3\nroot = "/tmp/th-scratch/pool"\n' > treehouse.toml
WT=$(treehouse get --lease --lease-holder scratch)   # ... exercise here ...
treehouse return --force "$WT"                       # release before destroying: --all skips leased slots
treehouse destroy /tmp/th-scratch/pool/.treehouse/<pool> --all --yes
```

Clean up only the scratch pool you created.

## Fleet conventions

**Pools are keyed by origin URL, not by clone.** The pool directory is `<root>/.treehouse/<repo-basename>-<sha256(origin-url)[0:6]>/<slot>/<repo-basename>`, and `root` defaults to `$HOME`. Every clone of one remote on the box therefore shares a pool unless a clone pins its own `root` in `treehouse.toml`. Firstmate pins each project clone to its home (`bin/fm-treehouse-pin.sh`), which is what keeps one home's slots out of another's.

**Run pool commands from the owning clone.** Inside a pooled worktree, the pinned `treehouse.toml` is usually absent, so treehouse resolves the default `$HOME` root and reports a *different* pool. Measured on this box: the same slot reads `available` in an unpinned pool from inside the worktree, and `in-use` from the clone that owns it. `cd` to the clone (`git rev-parse --git-common-dir` names it) before reading or mutating.

**Pools are shared live state.** Other agents are working in slots right now. `destroy`, `prune --yes`, `return --force`, and editing a live `treehouse.toml` are all destructive to someone else's in-flight work. Treat every lifecycle command against a pool you did not create as requiring a human decision.

**Crewmates do not provision their own worktrees.** Firstmate leases a slot and hands you the path; extra worktrees go through `bin/fm-lease-extra-worktree.sh` so teardown can return them. Leasing directly leaks a slot that nothing will reclaim, and leaked leases accumulate until the pool hits `max_trees` and spawns fail.

**`TREEHOUSE_DIR` is an output, not a setting.** Treehouse exports it into the subshell it opens to name the acquired worktree. Setting it does not steer pool resolution; only `treehouse.toml` does.

## Non-goals

- Not a git wrapper. Branching, committing, and pushing inside a slot are plain git; treehouse only owns the slot's lifecycle.
- No structured output beyond `status --json` and `get --lease --json`. Errors are unstructured stderr lines and every failure exits 1, so branch on the message, not on a code. `docs/axi-retrofit-spec.md` in this repository specifies the fix.
- Not a scheduler or a daemon. Nothing expires a lease, garbage-collects a dirty slot, or runs in the background; every state change is a command someone ran.
- Not a flag reference. Use `--help`.
