---
name: harvest-sessions
description: Sweep recent Claude Code and Codex sessions into one reviewed secondbrain pull request.
compatibility: Requires local Claude Code or Codex transcripts, Python 3, Git, GitHub CLI access, and a wkentaro/secondbrain checkout.
disable-model-invocation: true
---

# Harvest sessions (one tick)

One pass over every session newer than the watermark, then stop. acron owns
recurrence; never schedule yourself.

This is the unattended backstop for the capture rule in the global `AGENTS.md`:
that rule fires in the moment and depends on an agent noticing, so it misses
whatever nobody noticed. This pass reads the transcripts those sessions left
behind and files what they should have filed.

State lives in a watermark file, so a tick is idempotent: a quiet day costs one
scan and exits.

## Rails

- **An empty pass is a success.** Most days produce nothing durable. Report
  "nothing to capture", stamp the watermark, and exit. Manufacturing a page to
  justify the run poisons the second brain with material the user will learn to
  scroll past — one real capture a week beats seven padded ones.
- **Open a pull request; never commit to `main`.** Every capture is a judgement
  call made without the user in the room, so the user gets the veto.
- **Redact before writing.** The digest script strips known secret shapes, but
  it cannot recognise a novel one. Re-read every line you are about to commit
  for credentials, tokens, customer names, and third-party personal data.
- **Cite the transcript, do not copy it.** Reference the session path; the raw
  transcript already lives under `~/.claude` or `~/.codex` and does not belong
  in the repository.
- **Touch only `wkentaro/secondbrain`.** Never edit, commit to, or open issues
  against a source repository this pass merely read about.

## The capture test

A candidate earns a page when it is **durable** and **unrecoverable**.

**Durable** — it will still be true and still be wanted in six months:

- A root cause that took real work to find, and the symptom that pointed to it.
- A decision, what it beat, and the constraint that settled it.
- A measured number: a benchmark, a cost, a limit, a timing.
- Third-party behaviour that contradicts its own documentation.
- A workaround, plus the constraint forcing it.
- A policy or preference the user stated that applies beyond the session.

**Unrecoverable** — reading the repository at `HEAD` would not tell you. Skip
anything a diff, a commit message, a changelog, or `--help` already carries.

Judge the two independently and reject on either. When a candidate is
borderline, reject it; the watermark moves on and a genuinely durable fact
resurfaces in a later session.

## 0. Preflight

- Set `SKILL_DIR` to this skill's own directory, so the commands below run
  wherever the skill is installed:

```sh
SKILL_DIR=<the base directory named when this skill was invoked>
```

- `cd` to the secondbrain checkout. Abort if the working tree is dirty.
- Read `CLAUDE.md` and the target domain's `CLAUDE.md`. They own frontmatter,
  page types, wikilinks, and the `_log.md` convention; this skill does not
  restate them.
- Snapshot the tick start so sessions that begin mid-run are not skipped:

```sh
mkdir -p ~/.local/state/secondbrain-harvest
touch ~/.local/state/secondbrain-harvest/.tick
```

## 1. List candidates

```sh
python3 "$SKILL_DIR"/scripts/digest_sessions.py --list
```

With no watermark yet it falls back to a 24-hour window. Zero sessions listed
ends the tick — jump to step 5.

## 2. Judge

```sh
python3 "$SKILL_DIR"/scripts/digest_sessions.py
```

Each digest holds the human turns and the agent's prose replies, with reasoning
and tool traffic dropped. Apply the capture test to every digest and write down
a verdict for each, so the count of judged sessions matches the count listed in
step 1. Re-read the full transcript with `--only <path>` when a digest is
suggestive but too thin to decide.

## 3. Route

Route each survivor by the global `AGENTS.md` work-artifact rules. Most land as
a curated page or an edit to an existing one inside a `secondbrain` topic
folder. Prefer **editing an existing page** over adding one: grep the domain for
the concept first, and only create a page when nothing covers it. A survivor
that is really an open task belongs in an issue, not a page.

## 4. Write

Follow the repository's `ingest` procedure. Every capture cites its session
path inline. Cross-link both directions, update the topic `index.md` when a
page is new, and append one line per capture to the domain's `_log.md`.

## 5. Commit and open the pull request

Nothing captured: stamp the watermark and report the count of sessions judged.
Otherwise:

- Branch: `harvest/YYYY-MM-DD`.
- Commit per the global git rules, splitting by capture when there are several.
- Open the PR with `gh`. The body lists each capture as one unwrapped line —
  what it claims, and the session it came from — plus the number of sessions
  judged and rejected, so the user can audit the filter rather than trust it.
- Stop at the open PR. The user merges.

Stamp the watermark last, once the PR is open:

```sh
mv ~/.local/state/secondbrain-harvest/.tick ~/.local/state/secondbrain-harvest/watermark
```

Leaving the watermark unstamped after a failed tick is correct — the next run
re-judges the same window rather than losing it.

## Report

```text
Judged: <count>; rejected: <count and session paths>
Captured: <claim> — <literal source transcript path>
Changed: <secondbrain paths>
Redaction before commit: checked credentials, secrets, customer names, and third-party personal data
PR: <branch and URL>; body includes captures and judged/rejected counts
Watermark: <advanced from .tick after an empty pass or successful PR; otherwise unchanged, and why>
Source repositories: untouched
Failure: <failed action>; recovery: <branch or commit>  # only on failure
```
