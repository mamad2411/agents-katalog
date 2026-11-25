---
name: good-first-issue-batch
description: File a batch of contributor-ready GitHub issues from the seeds backlog, re-verifying every candidate against HEAD first so no dead issue reaches a contributor. Activate for prompts like "file some good first issues", "open a batch of GFIs", "publish backlog issues to GitHub", "find contributor-ready work", or after an audit that surfaced contributor-sized items.
---

# Protocol: Good-First-Issue Batch

You turn seeds backlog rows into GitHub issues a stranger can actually pick up.
The hard part is not writing them. It is proving they are still real.

## The failure this skill exists to prevent

On 2026-08-07 six issues were bulk-filed straight from seeds rows. Within four
hours a contributor commented on #808 that the work was already merged — it had
been fixed in PR #774 four days *before* the issue was filed. Two more issues in
the same batch (#806, #807) turned out to be half-dead. Nobody noticed because
the seeds rows still said `open`, and the seeds rows still said `open` because
the PRs that killed them were about something else entirely.

**A tracker row is a lead, not evidence.** Its age, its `open` status, and its
description are all things a human wrote once and never revisited. The only
evidence that a bug is real is the bug, in the code, at HEAD, today.

## 1. Operating principles

- **Re-derive every claim from HEAD.** Never copy a defect description from the
  seeds row into the GitHub body. Open the file, confirm the defect, and write
  the body from what you just read.
- **Verify bullets independently.** A three-bullet issue is three issues wearing
  a trenchcoat. One bullet dying does not kill the others, and one bullet
  surviving does not vindicate the rest. Grade each separately.
- **Line numbers are always stale.** Every `file:line` in an old row has drifted.
  Re-resolve all of them; cite what you actually saw.
- **A dead issue costs more than no issue.** A contributor who burns an evening
  on already-merged work may not come back. When verification is ambiguous,
  leave the row in seeds rather than publishing a maybe.
- **Never file for volume.** Six solid issues beat twenty speculative ones.
  There is no quota.

## 2. Gather candidates

Pull open seeds rows that are plausibly contributor-sized and self-contained:

```bash
sd list --status open --format compact
sd search "<theme>" --format compact
```

Good raw candidates are bounded in blast radius, need no cluster access or live
credentials to reproduce, and have an obvious done condition. Drop anything
needing a running k8s deployment, a GitHub App token, or judgement about product
direction.

Skip rows that already carry a GitHub back-link — they are filed:

```bash
python3 -c "
import json
for line in open('.seeds/issues.jsonl'):
    d = json.loads(line)
    gh = (d.get('extensions') or {}).get('github')
    if gh and d.get('status') == 'open':
        print(d['id'], '-> #' + str(gh['issue']))
"
```

## 3. Verify each candidate against HEAD — the load-bearing phase

Run all four checks on every candidate. Fan these out with subagents when the
batch is larger than three or four; each candidate is independent.

### 3a. Does the defect literally still exist?

Read the code the row names. Not the row's summary of the code — the code. If
the row cites a symbol, confirm the symbol is still there and still wrong:

```bash
rg -n "<symbol>" src/
git log --diff-filter=A --format="%h %ad %s" --date=short -- <path-it-names>
```

If the row references a gate (`check:dups`, `check:size`, `check:debt`), run it.
A passing gate means the grandfather entry the issue wanted deleted is already
gone. That is exactly how #808 died: `resolveTargetDir` had been extracted to
`src/cli/commands/target-dir.ts`, and `bun run check:dups` reported all ten
allowlist pairs still matched, with nothing stale to remove.

### 3b. Born-dead check: was it fixed before it was filed?

Compare the row's `createdAt` against the history of the files it names.

```bash
git log --format="%h %ad %s" --date=short --since=<row createdAt> -- <paths>
git log -S'<symbol>' --format="%h %ad %s" --date=short
```

The killers are almost never PRs that mention the issue. They are sweeps —
"single-source truth sweep", "dedup pass", "consolidate X" — that fix a small
defect as collateral and close nothing. Read the diff of any sweep-shaped PR
touching the same files since the row was written.

### 3c. Deletion check: does the thing the issue improves still exist?

An issue asking for better UI on a feature that was later deleted is not a bug,
it is an archaeology exhibit. Confirm every state, field, route, and component
the row depends on is still live:

```bash
rg -n "<state-or-field-name>" src/core/wire.ts src/db/schema/ src/ui/src/
```

Zero hits across the schema and the UI means the feature is gone. Item 4 of #806
asked for paused-run context on the spectator view; `paused` had already been
removed from `RUN_STATES` and its columns dropped by migrations 0034/0028 when
the plot pass (pl-3a79) retired the whole pause mechanism.

### 3d. Adjacent-fix check: did another tracker id fix half of it?

Multi-bullet rows rot unevenly. Search for the *behaviour* the bullet wants, not
the tracker id — the PR that delivered it was filed under a different id and
will not mention this row:

```bash
rg -n "<config-knob-or-constant-the-bullet-asks-for>" src/
git log --oneline --all -S'<constant>' | head
```

#807 claimed the event-stream lifetime was unlimited. It had been capped at four
hours by default since PR #693, filed under warren-3995, which never touched
warren-a676. Only the `idleTimeout` bullet was still true.

### Grade and act

| Grade | Meaning | Action |
|---|---|---|
| **LIVE** | Every bullet reproduced at HEAD | File it |
| **PARTIAL** | Some bullets dead | Rewrite to the surviving bullets, then file. Record what died and why |
| **DEAD** | No bullet survives | Do not file. Close the seeds row citing the commit or PR that fixed it |

For every DEAD row, close it with the evidence rather than leaving it to rot:

```bash
sd close <seeds-id>
```

## 4. Write the body

Structure, in order:

1. **The defect**, as a live `file:line` claim you personally re-read this
   session. One or two sentences per bullet.
2. **The fix direction** — enough to remove ambiguity, not so much that it is
   just a diff in prose. Name the in-repo precedent to copy (`Projects.tsx:90`
   already routes its empty-state hint through `useOperatorHint` — copy that
   shape) rather than describing the pattern abstractly.
3. **Scope boundaries.** Say what is explicitly out of scope so the PR does not
   sprawl. Name the tests that will need updating.
4. **Getting started.** `AGENTS.md` covers setup and conventions. Run
   `bun run check:all` before pushing — warnings count as failures.
5. **`Tracked internally as \`<seeds-id>\`.`**

If you rewrote a PARTIAL row, append a dated `**Revised YYYY-MM-DD.**` note
saying which bullets died and what killed them. A contributor who finds the old
description in a search result needs to know it was retired deliberately.

Write for someone with no repo context. Expand internal shorthand: "the reap
path", "the wire vocabulary", and tracker ids mean nothing to a first-timer.
Read `.claude/skills/ste-writing/SKILL.md` conventions if the prose is drifting
toward marketing register.

## 5. File with linkage in both directions

The 2026-08-07 batch wrote GitHub → seeds but never seeds → GitHub, so a later
`sd close` had no way to reach GitHub. Always write both.

```bash
gh issue create \
  --title "<specific, defect-shaped title>" \
  --body-file <path> \
  --label "good first issue,help wanted,type/bug,area/ui,priority/P3,effort/small"
```

Then immediately record the back-link on the seeds row:

```bash
sd update <seeds-id> --extensions '{"github":{"issue":<N>,"url":"https://github.com/jayminwest/warren/issues/<N>"}}'
```

Label vocabulary is fixed by `.github/labels.yml` — one `type/`, one or more
`area/`, one `priority/`, one `effort/`. Never invent a label; `sync-labels.yml`
will drop it. Reserve `good first issue` for `effort/small` work with a single
obvious approach; `help wanted` alone is right for anything larger.

## 6. Report

Give the user a table of every candidate with its grade and the evidence that
decided it, the URLs filed, and the seeds rows closed as DEAD. State the batch
size and say plainly if verification shrank it — "filed 4 of 9 candidates; 3
were already fixed, 2 were ambiguous and left in seeds" is the useful sentence.

## 7. Keeping a filed batch honest

Issues rot after filing too, by the same mechanisms. Before pointing a
contributor at an existing issue, or roughly monthly, re-run section 3 over the
open GitHub issues and their linked seeds rows. When a row and its GitHub issue
diverge, the code is the tiebreaker — never the tracker, and never the more
recently edited of the two.
