---
name: delete-this
description: "Use when a codebase feels heavy, when you suspect dead code, or before adding a feature to a cluttered area. Finds dead branches, unused exports, commented-out blocks, pinned feature flags, and single-use abstractions, proves each is unused before removing it, and stages deletions so each is independently revertible."
---

# Delete This

## The failure mode this fixes

Codebases accrete. Every feature adds; almost nothing subtracts. Agents make this worse — they're trained to produce code, not remove it, so they route around dead code instead of deleting it. The result is a graveyard of commented-out blocks, flags that are always true, abstractions invented for a second caller that never arrived, and TODOs from engineers who left two years ago. Every line of it is read, parsed, and feared by everyone who touches the file.

The best refactor is often a deletion. This skill finds what no longer earns its place and removes it *safely* — proving it's dead before it's gone.

## When to Use This Skill

- A file or module feels heavier than what it does
- Before adding a feature to an already-cluttered area (clear the ground first)
- You see commented-out code, `// TODO (2023)`, or `if (false)` branches
- An abstraction is used by exactly one caller
- A feature flag has been at one value for months

**Don't use when:** you can't yet prove the code is unused, or when "dead" code is actually a public API / plugin surface others depend on. When in doubt, prove first (step 2). For a small dead line you noticed *while editing something else*, don't open a deliberate sweep — that's `boyscout` territory (bounded, in-scope cleanup). This skill is the deliberate, repo-wide hunt.

## Instructions

### 1. Inventory the candidates

Scan the target scope and list deletion candidates by category:
- **Dead branches** — conditions that can't be true (`if (false)`, flags pinned to one value)
- **Unused symbols** — exports, functions, variables with no callers
- **Commented-out code** — version control already remembers it; the comment is noise
- **Single-use abstractions** — interfaces/factories/generics with exactly one implementation or caller
- **Stale markers** — TODOs/FIXMEs older than the problem they describe
- **Orphaned config** — flags, env vars, settings nothing reads
- **Orphaned tests & deps** — tests that only exercise code being deleted; package dependencies nothing imports once the sweep lands

### 2. Prove it's dead (do not skip)

For each candidate, establish *unused* with evidence, not vibes:
- Grep the whole repo (and sibling repos / consumers if it's an export) for references
- Check dynamic access: reflection, string-keyed lookups, DI containers, route tables, serialized config
- Check the build: is it exported from a package's public entry point?
- For dead *branches*, grep isn't proof of runtime death — a reference can exist and never execute. Use runtime evidence where it exists: coverage reports, log/telemetry hits, feature-flag analytics ("evaluated 0 times in 90 days" is proof; "the flag appears in code" is not)
- Check the fence before removing it: if you can't say why the code was added, read `git log`/blame for the commit that introduced it. "Looks pointless" plus a commit message saying "fixes race on concurrent checkout" changes the verdict
- Cross-check the **Untouchables** in `CONTEXT.md` (if present) — public exports, plugin/route surfaces, and dynamic-access points listed there are never deletion candidates, regardless of grep results.
- If you cannot prove it's unused, it is **not** a deletion candidate — move it to a "verify with a human" list instead.

### 3. Stage deletions independently

Group deletions so each is its own revertible commit:
- One concern per commit (`remove unused export X`, not `cleanup`)
- Never mix a deletion with a behavior change — that's how a "cleanup" silently breaks prod
- Order from leaves inward: delete callers' dead usage before the thing they used

### 4. Verify after each removal

After each deletion: typecheck, build, run tests — using the project's actual commands (take them from `CONTEXT.md` if it records a build/typecheck/test command, otherwise detect them). A deletion that breaks the build wasn't dead. Roll back that one and move it to the verify list. If there is no way to typecheck/build/test the change, you cannot verify the removal is safe — treat those candidates as "verify with a human," not "safe to delete."

### 5. Report what and why

For each removal, record *why it was safe* (the evidence from step 2). This is what lets a reviewer approve a deletion PR with confidence.

## Output format

```
SAFE TO DELETE (proven unused)
  - <symbol/block> @ <file:line> — evidence: <grep result / no callers / flag pinned since X>

VERIFY WITH HUMAN (looks dead, can't prove)
  - <symbol/block> @ <file:line> — uncertainty: <dynamic access? public API? external consumer?>

PLAN
  commit 1: <single deletion>
  commit 2: <single deletion>
  ...
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| `git stash`-ing into a comment | Version control already remembers. Commented code rots and lies. |
| Deleting on a hunch | If you can't prove it's unused, you're gambling with prod. Prove or punt. |
| One giant "cleanup" commit | Impossible to review, impossible to bisect, impossible to partially revert. |
| Mixing deletion with a fix | When it breaks, no one can tell which half did it. |
| Keeping code "just in case" | That's what git history is for. Fear-driven retention is how graveyards grow. |

## Mental Model

> Code is a liability, not an asset. The question is never "why delete this?" — it's "what is this still earning?" If the answer is silence, it goes.
