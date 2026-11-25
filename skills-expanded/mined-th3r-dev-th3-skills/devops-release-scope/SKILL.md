---
name: devops-release-scope
description: >-
  What goes up in the next release and what is still pending, written for the PM and the customer.
  Diffs `releases/<next>` against what prod runs across every repo of the product, joins the issue
  boards, then writes the PM list ("this round — release X, N items", one `KEY: …` line per
  user-visible change) and checks the PM's customer message against it. Use WHENEVER the work is
  "what's in v1.2.x", "how does release 22 differ from 21", "pending for the next release",
  "release note", "summary for the PM", "check what the PM told the customer", "จะเอาอะไรขึ้น
  release นี้บ้าง", "สรุปให้ PM", or the PM pastes a "fixed + tested, deploying on …" message.
---

# devops-release-scope

One command collects the facts; the agent does the judgement and the wording.

```bash
S=skills/devops/release-scope/scripts
uv run $S/release_scope.py --to v1.2.22 --prod v1.2.21,v1.2.21.1 \
  --repo api=../backend=org/backend --repo web=../frontend=org/frontend \
  --key-regex '(?:PRJ|ISS)-\d+' --mirror-regex '^\[(PRJ-\d+)\]' \
  --board tracker=work/jira/<date>/tracker/issues.json --board mirror=work/release/v1.2.22/mirror.json \
  --out work/release/v1.2.22          # -> scope.md + scope.json   (--selftest checks the joins)
```

Branch names: `--to` / `--prod` without a slash get `--release-prefix` (default `origin/releases/`);
`--dev` defaults to `origin/develop`. Each `--repo` is a local clone with an `origin`; the GitHub
slug is optional and only feeds `gh pr list`.

## 0. Baseline: what prod runs

`--prod` is every branch prod's images were built from. **The owner states this, not git** — a
hotfix branch that was cut but never deployed must not be a base. When the owner says prod moved,
change `--prod`. Never infer it from tags or from what a staging environment runs.

## 1. Refresh the boards

Export each board to JSON before running (Jira REST `search` output, the Rovo `{issues:{nodes}}`
shape, or a JSON list of pages — the script reads all three). A mirror board that copies tickets
from another tracker as `[KEY] summary` is merged onto the source key through `--mirror-regex`.
Pages too big for the context go straight to disk and are combined with `jq -s '.' p1 p2 > all.json`.

## 2. Read scope.md, in this order

1. **lost from prod** must be `0` in every repo. Anything else means the release dropped prod code.
   Stop and report it.
2. **half shipped** means a ticket is in the release in one repo while its code sits only on dev in
   another (a UI filter shipped, the API ignoring it). Always a warning under that item.
3. **PR table**: every row is one change. A row with `new keys: **none**` is either the hotfix
   merge-back (skip it) or a keyless fix. A keyless fix still goes in the list, without a ticket.
4. **pending code**, **open PRs** and **board items** make up the "still pending" part. Read the open
   PRs' base branch: a PR aimed at an older release branch or at dev will not ship by merging.

Details for each line come from the commit subjects (`git log` on the PR) and the ticket summary.
Don't guess what a ticket does from its number.

## 3. The PM list

Write in the team's language (Thai through `kien-thai`). **No section headers**, `:` after the key,
never a middle dot. Each warning is an indented `- ` line under the item it belongs to:

```
this round — release 1.2.22, 11 items

1. PRJ-247: CSV export on every report, dashboard, master data and the orange app — a CSV button beside Excel
5. PRJ-5373: tax report groups rows by tax-point date; figures in the tax, dispatch and daily summary reports change after the release
   - PR #555 of this item carried a "DO NOT MERGE: perf" label and was merged without a timing result …
11. the all-companies tax list no longer times out: 252 s → 2.7 s
```

- One line per user-visible change. Fold retired keys under the key that replaced them. A ticket
  with commits in several repos counts once.
- Say what changes for the user, plus one fact that makes it concrete (a timing, which reports' numbers move).
- Warnings go under their item: half shipped, a PR merged against a "DO NOT MERGE" label, a
  migration that locks tables (read the migration for `ONLINE`).
- The "pending, not in <to>" part comes after, in three groups: code done on dev, open PRs, and
  features on the board. From the board list development features only; leave out plan / test /
  rollout items and bugs unless asked.

## 4. Checking the PM's customer message

- Map every customer line to a PM-list item. A line with no item is a promise the release doesn't keep.
- Check "tested" against the boards. Code merged while its sub-tasks still sit in Testing / Backlog
  is not tested; say which part is and which isn't.
- Name the customer-visible changes the message leaves out: report figures that move, new rules that
  reject a submission that used to pass. Customers who aren't told read these as bugs.
- Never promise a half-shipped item.
- Check which day is meant against today's date and what prod runs.

## Traps

- **Keys are the only link.** Without fixVersions, work committed under another key reads as pending,
  and a ticket with several commits may have only some of them in the release. Check the commits
  before telling the PM something is missing.
- **Two boards disagree.** Statuses on a mirror board are often more current than the source. Quote
  both when they differ.
- `git log releases/<to>..develop` shows hundreds of commits that are cherry-picks of what already
  shipped. Compare keys, never commit counts.
