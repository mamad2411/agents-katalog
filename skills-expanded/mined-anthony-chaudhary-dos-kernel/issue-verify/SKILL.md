---
name: issue-verify
description: Adjudicate a GitHub issue's "this is resolved" claim from witnesses the claimant didn't author — then close it carrying the evidence, or refuse with the typed gap. Use when an issue looks already-solved, after landing a fix that should have closed one, or to sweep open issues for silently-resolved ones.
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, PowerShell
argument-hint: "[issue-number | --sweep] [--dry-run]"
output_root: none
---

# Issue-verify — close issues from evidence, not narration

> **An issue is a CLAIM; closing it is BELIEVING the claim.** The kernel's one
> rule, aimed at the tracker: never set a belief bit from what anyone *says* —
> set it from a read-back the claimant didn't author. This skill is the
> `dos-witness-claim` pattern pointed at GitHub issues: extract the checkable
> effects, witness each on the right rung, stamp the fold with the kernel's
> admission verdict, and only then actuate the close. Worked example:
> [#1](https://github.com/anthony-chaudhary/dos-kernel/issues/1) — two
> env-authored witnesses (a green Actions run conclusion + the TestPyPI
> registry's own JSON), one non-recurrence triage, one `dos reward … → ACCEPT`,
> one evidenced close.

**Layering.** Dev tooling that operates ON the repo (the `/release` tier) — it
names a vendor (`gh`/GitHub), so it lives in `.claude/skills/`, never
`src/dos/skills/` (a shipped SKP skill names no vendor or host). If the
screenplay proves out, the promotion path is the usual lift: parameterize the
tracker, move the shape into the SKP.

**Public-repo note.** Every comment this skill posts is a public document — no
dev-machine paths, hostnames, or private-process prose (the
route-privacy-at-authoring-time rule applies to issue comments too).

**The disciplines** (the JUDGE-rung hedges, applied to triage):

- **Deterministic-first** — a witness is a command output or a registry
  read-back, never your impression of the thread.
- **Fail-to-abstain** — a witness you cannot gather (command errors, endpoint
  down, no witness exists for the claim) is `none`, NEVER `confirm`. No close
  without a confirming witness.
- **Forgeable ⇒ structurally ignored** — a "fixed!" comment, a commit
  *subject*, a `> **Status:**` line are claimant-authored bytes: they may
  select *which* witness to gather, never BE the witness. If the best you have
  is forgeable, pass `--forgeable` to `dos reward` and watch it ABSTAIN — that
  is the structure working, not a gap.
- **Advisory until the one actuation** — read-only throughout; the single
  mutation is the close + its evidence comment. Never edit an issue body,
  never delete, never close on a REJECT or ABSTAIN fold.

**When NOT to use the manual close at all:** if the resolving fix is a commit
you are *about to land* in this repo, put `Fixes #N` in the commit body and let
the merge close the issue — the tracker then records the closing commit as the
witness (the repo's issues-workflow convention). This skill's manual close is
for the other three cases: a fix that already landed without the reference, a
fix that lives *outside* this repo's git (an external service's config — the
#1 case), or an issue dissolved by an environment change.

## Step 1: Snapshot the claim

```bash
gh issue view <N> --json number,title,body,state,createdAt,comments
```

- `state: CLOSED` → idempotent: report "already closed", stop.
- `--sweep` → `gh issue list --state open --json number,title` and run Steps
  1–5 per issue; render one verdict row each; actuate only the ACCEPTs.

## Step 2: Extract the checkable effects

From the body (and any proposed fix in it), enumerate the EFFECTS that would be
true **iff** the issue is resolved — each as `{claim, rung, gather-command}`.
If the body proposes a fix, the compound claim is "that fix was applied AND the
failure mode no longer reproduces." Pick each claim's witness rung:

| Rung | The claim is about… | The witness (env-authored) |
|---|---|---|
| **git** | a code/doc change in this repo | `git merge-base --is-ancestor <sha> origin/master` for landing; `dos verify --workspace . <PLAN> <PHASE>` where a ship-stamp exists; `dos commit-audit --workspace . <sha>` for subject-vs-diff honesty of the claimed fixing commit |
| **run** | CI / pipeline behavior | `gh run list` / `gh run view --json conclusion,jobs` — the Actions `conclusion` field, never the run's own log narration |
| **read-back** | an external effect (registry, endpoint, published artifact) | fetch the authoritative state, e.g. `Invoke-RestMethod https://test.pypi.org/pypi/<pkg>/json` — the registry's bytes, not anyone's report of them |
| *(none)* | taste, intent, future work | no witness exists → the claim is UNWITNESSABLE → ABSTAIN |

## Step 3: Gather the witnesses

Run each gather-command and record the raw fact (run ID + conclusion, SHA +
ancestry bit, registry field + timestamp). A command that errors or returns
ambiguity records `none` for that claim — fail-to-abstain, do not retry your
way to a `confirm`.

## Step 4: The non-recurrence check (newest evidence wins)

A confirming witness *older* than the latest contrary signal proves nothing.
Search for the failure signature in evidence **newer** than the claimed fix
(later runs of the same workflow, later issue comments, later commits):

- Same defect recurring → the fix did not hold → the fold is **refute**.
- A *different* defect in the same surface → note it explicitly in the close
  comment ("not a recurrence — distinct failure, distinct issue") and, if it
  matters, open/point to its own issue. Do not let an unrelated red block a
  witnessed close, and do not let a witnessed close bury an unrelated red.
  (#1's worked example: the later `publish.yml` failure was the CI-green gate
  refusing a red candidate — the TestPyPI leg was `skipped`, not failed.)

## Step 5: Fold and stamp the verdict

Fold the per-claim witnesses (ALL must confirm to accept — conjunctive, like
every kernel floor), then stamp the fold with the kernel's admission verdict:

```bash
dos reward --claim --witness confirm    # every claim witnessed-confirmed → ACCEPT
dos reward --claim --witness refute     # any claim witnessed-refuted     → REJECT_POISON
dos reward --claim --witness none       # any claim unwitnessable         → ABSTAIN
# only-forgeable evidence? add --forgeable and it ABSTAINs by construction
```

| Fold | Verdict | Actuation |
|---|---|---|
| all confirmed | **ACCEPT** | close, carrying the evidence (Step 6) |
| any refuted | **REJECT_POISON** | comment the refuting evidence, leave OPEN |
| any unwitnessable | **ABSTAIN** | leave OPEN; tell the operator exactly which witness is missing and what would produce it |

## Step 6: Actuate (skip on `--dry-run` — print the would-be comment instead)

Only on ACCEPT, one mutation:

```bash
gh issue close <N> --comment "<evidence comment>"
```

The comment is the artifact — it must let a future reader re-derive the verdict
without trusting you. Shape (the #1 close is the reference rendering):

```
Verified resolved — adjudicated the DOS way: the claim is corroborated by
read-backs the claimant didn't author, not by narration.

**Witness 1 — <rung>.** <the raw fact, with run-ID / SHA / URL>
**Witness 2 — <rung>.** <…one block per claim…>

Kernel verdict: `dos reward --claim --witness confirm` → **ACCEPT**.
<one line on WHY this rung and not another, if non-obvious>

<non-recurrence note: what newer evidence was checked, and why any later
failure is a distinct defect, with its pointer>
```

On REJECT_POISON, the same shape with the refuting witness and **no close**.
On ABSTAIN, no comment by default — report to the operator instead (a public
"couldn't verify" comment adds noise, not evidence).

## Step 7: Report

- Per issue: `#N — ACCEPT (closed) / REJECT_POISON (left open: <refuting
  fact>) / ABSTAIN (left open: <missing witness>)`.
- Any non-recurrence findings that deserve their own issue.
- On `--sweep`: the verdict table, plus how many opens were not adjudicated
  and why.
