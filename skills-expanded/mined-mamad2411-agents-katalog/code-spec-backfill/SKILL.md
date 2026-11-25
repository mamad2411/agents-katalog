---
name: code-spec-backfill
description: >
  Backfill function-level contracts (docstrings, type annotations) where missing.
  Report unresolvable gaps with misuse scenarios. Incremental by default (state-driven).
---

**STATE_FILE** = `specs/.code-spec-backfill/state.yaml` tracks per-file review freshness:

# Code Spec Backfill

Constructive first, diagnostic second. Write the contract where you can infer it. Report what you can't resolve.

# Core Heuristic

Only act on a gap if you can write a plausible incorrect usage that a senior engineer might write based on the function's public interface. The misuse scenario IS the quality gate — if no one would get burned, it's not a gap worth addressing.

**Misuse scenario format:** `[caller_assumption] × [actual_behavior] → [consequence]`

Example: `"Returns empty list when no results" × "Raises NoResultError" → "Caller crashes on valid empty-result case"`

# Hard Boundaries

- NEVER modify behavior — only add/improve documentation and type annotations.
- NEVER weaken existing contracts (e.g. broadening a type hint to accept None).
- Unexported/private members: only if explicitly scoped.

## No-Tautology Rule

A docstring that restates the function signature adds no value. Do not write docstrings that merely echo parameter names, types, or the function name as prose.

**Tautological (do not write):**
```python
def get_user(user_id: int) -> User:
    """Get a user by user ID.

    Args:
        user_id: The user ID.

    Returns:
        The user.
    """
```

**Valuable (write this):**
```python
def get_user(user_id: int) -> User:
    """Fetch user from database. Raises UserNotFoundError if no user exists
    with this ID. Result is cached for the duration of the request."""
```

The test: does the docstring tell you something you couldn't already read from the signature? If not, skip it.

# Spec Clarity Assessment

**Adequate (skip):**
- Docstring with behavioral contract (return semantics, exceptions, side effects)
- Clear name + full type hints + small body where behavior is obvious

**Gap (apply core heuristic):**
- No docstring + (unclear name OR incomplete types OR non-trivial body)
- Vague docstring ("Process the data", "Handle the request")
- Type hints that lie (`-> float` but sometimes returns `None`)
- Undocumented side effects (mutation, exceptions, caching)

# Scope Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| Incremental (default) | no flags | State-driven: detect stale + unreviewed, batch of 10 |
| Files | `--files <path>` or `--module <dir>` | Targeted audit, ignores state |

## State File Format

```yaml
version: 1
last_run: 2026-02-20
files:
  internal/blackboard/lock.go:
    sha: a1b2c3d
    reviewed: 2026-02-15
    status: current       # current | stale | unreviewed
  internal/agent/builder.go:
    sha: e4f5g6h
    reviewed: 2026-02-15
    status: stale          # file changed since review
  internal/cli/init.go:
    status: unreviewed     # new file, never analyzed
```

# Workflow

## Incremental Mode (default)

```
1. UPDATE STATE
   - git log since last_run → list touched files
   - New files → add as "unreviewed"
   - Changed files (SHA differs) → mark "stale"
   - Deleted files → remove from state
   - If no stale/unreviewed files → report "all current" and stop

2. SELECT BATCH
   - Pick up to 10 stale/unreviewed files (stale first — regressions before new ground)
   - List batch to user before proceeding

3. FOR EACH FILE IN BATCH
   - List public callables
   - For each target: assess spec clarity (adequate or gap)
   - If adequate → skip
   - If gap → apply core heuristic (write misuse scenario)
   - Can't write misuse scenario → not a real gap, skip

4. FOR EACH CONFIRMED GAP — decide path:
   a. Can infer contract from code + call sites + tests?
      → BACKFILL: write docstring and/or fix type annotations
      → Apply no-tautology rule — skip if docstring would only restate signature
      → If inferred from code body only (no call sites, no tests): flag ⚠️ for review
   b. Behavior is ambiguous (multiple valid interpretations)?
      → REPORT: record gap with misuse scenario in report

5. OUTPUT
   - Backfilled: docstrings/annotations added to source files
   - Reported: unresolvable gaps per references/report-format.md

6. UPDATE STATE
   - Set reviewed files to status: current, sha: current HEAD sha, reviewed: today
   - Report remaining stale/unreviewed count
   - Ask user to review backfilled changes
```

## Files Mode

```
1. List public callables in specified paths
2–5. Same as incremental steps 3–5 (assess → backfill/report → output)
```

State file is not consulted or updated in Files mode.

# When to Use

- Regularly (incremental) — "catch up on contract debt since last run"
- After a commit or PR — run incremental, changed files will be stale
- Auditing a module — use Files mode for targeted sweep
- Before onboarding — "will a new developer understand these APIs?"

For feature-level specifications (product specs, user stories), use the spec-backfill skill instead.

# Constraints

- Language-agnostic. The workflow applies to any language with doc conventions.
- Incremental mode: self-batching (10 files per run). No scope guard needed.
- Files mode: if >50 targets, ask user to narrow scope.

# Stop Conditions

- Max 3 attempts per target to write misuse scenario — if can't, not a gap
- >80% of targets flagged as gaps → pause, heuristic may be too loose
- 0% gaps → report as confidence signal or heuristic too strict (state which and why)

# Integration

- **Testing skill**: Misuse scenarios are essentially test cases in prose. If a misuse scenario is particularly dangerous (silent-corruption), consider writing it as an actual test via black-box-red-testing.
- **white-box-red-testing**: White-box produces `specification-gap` findings. This skill resolves them — natural pipeline: white-box finds gaps → code-spec-backfill backfills or reports.
- **spec-backfill**: This skill handles function-level contracts. spec-backfill handles feature-level specifications. They complement, not overlap.
