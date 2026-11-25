---
name: md-audit
description: "Semantic audit of human-facing markdown (README, CONTRIBUTING, SECURITY, docs/**, package READMEs) for claims the repo no longer satisfies, after scripts/audit-markdown.mjs. Use weekly from the docs-audit routine, or after a refactor that moved user-facing surfaces."
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, TodoWrite
---

# Markdown Audit (semantic pass)

A broken link is a lookup. A false sentence is a judgement — and it is the more
expensive of the two, because it reads as authoritative right up until someone
runs the command and it fails.

This skill audits the half of documentation rot that no script can settle:
whether the prose is still **true**.

## Boundaries — read before starting

Three passes exist and they do not overlap. Staying inside this one is what
keeps the weekly routine cheap.

| Pass                         | Owns                                                                        | Cadence |
| ---------------------------- | --------------------------------------------------------------------------- | ------- |
| `scripts/audit-markdown.mjs` | Broken links, stale directory trees — anything decidable by `fs.existsSync` | weekly  |
| **this skill (`/md-audit`)** | Human-facing prose: claims about commands, flags, paths, ports, behaviour   | weekly  |
| `/claude-md-improver`        | Agent-instruction files: `CLAUDE.md`, `AGENTS.md`, `.claude/rules/*`        | monthly |

**Do not audit `CLAUDE.md`, `AGENTS.md`, or `.claude/rules/*`** — those belong to
`/claude-md-improver` and duplicating it wastes a run and produces conflicting
PRs. **Do not re-report broken links or tree entries** — the mechanical pass
already fixed or reported them; if you see one, it is a known-unfixable the
script deliberately left for a human.

## Scope

In scope, in rough priority order:

1. `README.md` — the highest-traffic doc, and the one that drifts fastest.
2. `CONTRIBUTING.md`, `SECURITY.md`, `docs/**/*.md` (excluding date-prefixed
   snapshots under `docs/plans/` and `docs/design/` — those are records).
3. `apps/*/README.md`, `services/*/README.md`, `packages/*/README.md`.

## Process

### Step 0: Confirm the mechanical pass is clean

```bash
node scripts/audit-markdown.mjs
```

If it reports findings, note them and move on — do not fix them here. A
`stale-tree-entry` left standing usually means the tree needs a human decision
about what the structure _should_ be, which is a legitimate finding for your
report but not a link you can repair.

### Step 1: Extract checkable claims

Read each in-scope doc and pull out every sentence that asserts something
verifiable. A claim is checkable when you can name the command, file, symbol, or
output that would prove it false. Typical shapes:

- **Commands** — `pnpm foo`, `mbe bar`, `node scripts/baz.mjs`. Does the script
  exist in the relevant `package.json`? Does the subcommand exist in the CLI?
- **Flags and options** — is `--max-budget` still parsed? Was it renamed?
- **Ports, URLs, env var names** — do they match the service's own config?
- **Counts and inventories** — "9 subagents", "6 levels", "three modes". Count
  the real thing.
- **Described behaviour** — "X falls back to Y on failure". Read the code path.
- **Named files and directories in prose** (not links — the script has those).

Sentences that are merely vague, verbose, or stylistically weak are **not**
findings. If you cannot phrase it as _"the doc says X, but X is false because
&lt;evidence&gt;"_, drop it.

### Step 2: Verify each claim against the repo

Verify with the repo, not memory. `grep` the script name, read the
`package.json`, run the `--help`. Cite the evidence in the finding — a claim
marked false without evidence is just a different false claim.

Prefer reading `origin/main` (`git show origin/main:<path>`) when the local
checkout may be behind — a stale checkout produces confident, wrong findings.

### Step 3: Fix what is unambiguous, report what is not

- **Fix directly** when the true statement is obvious: a renamed script, a
  changed port, a count that is off by a known amount.
- **Report without fixing** when the correct replacement is a decision: a
  documented workflow that no longer exists at all, a section describing a
  removed feature, guidance that contradicts a newer ADR.

Keep every edit minimal and in the doc's existing voice. Do not restructure a
document, rewrite headings, or "improve" prose that is merely plain — the diff
should be readable as a list of corrections.

### Step 4: Verify the docs still build and format

```bash
node scripts/audit-markdown.mjs
pnpm check:prettier
```

Note: files written via Bash skip the formatting hook. If `check:prettier`
disagrees with your local run, see `.claude/rules/gotchas.md` — the local
prettier config silently falls back to defaults.

### Step 5: Open a PR

One PR per run, titled `docs: correct stale claims in <area>`. The body lists
each correction as `doc says X → actually Y (evidence)`, plus a separate
**Needs a decision** section for the reported-not-fixed findings.

If nothing was found, say so and open no PR — a no-op week is a good week, and
an empty PR costs a review.

## Rules

- Evidence or it is not a finding.
- Never touch the instruction files owned by `/claude-md-improver`.
- Never rewrite a date-prefixed snapshot under `docs/plans/` or `docs/design/`:
  those record what was believed on that date, and "correcting" one destroys the
  record.
- Prefer three well-evidenced corrections to thirty speculative ones.
