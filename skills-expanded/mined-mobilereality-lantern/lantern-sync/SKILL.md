---
name: lantern-sync
description: Use when you finish a change in a project that has a `.lantern/` map and must keep that map true, or record the pull request in it — "update the Lantern map", "record the PR in Lantern", "write the reasons for my uncommitted changes", "open my changes in Lantern with the reasons", "is the map still true", "which files does this branch need re-mapped", or right after a merge or before handing a delegate's branch over. Re-maps exactly the files the change touched (changed, added, or pointing at something removed or renamed), gates that with a script, and writes the PR record `.lantern/prs/<id>.pr` so the Lantern app can show the pull request. Also the orchestrator's check that a delegate's branch carries a true map. It never maps a whole project (that is `lantern-setup`) and never writes outside `.lantern/`; it does not commit or push on its own. When the change is made by a delegate under an orchestrator, `lantern-delegate` sequences these commands; this skill stays the reference for what each does.
---

# Lantern sync — keep the map true, record the PR

In Codex, read `references/codex.md` now; it replaces the model and dispatch details below.

(The Lantern app copies this skill and `lantern-setup` into a project's `.claude/skills/`; elsewhere run
`pnpm run install-skills -- <project-dir>` in the Lantern repo.) This skill runs the setup skill's
scripts from the folder beside it (`../lantern-setup`: a sibling in the Lantern repo's `skills/`, or
in a project's `.claude/skills/`) and fails with a clear message when there is none, e.g. a copy of
this folder on its own. You also need `lantern-setup` there to read its `SKILL.md` for the
re-mapping procedure. The sibling `lantern-plan` is optional: with it, `pr` can tick plan items and `verify`
checks plan files (`pr --plan`, `verify`); without it, those two options say so and everything else runs.

`lantern-setup` builds the map once. This skill is the per-change half: the change that finishes
with the map still true, and a pull request record that lands with the code.
`$S` = this skill's folder; `$L` = the `lantern-setup` folder. Run from the **project root**.

## Use it when / do not

- **Use:** a change (yours or a delegate's) is done and the project has `.lantern/map/`; someone
  asks whether the map is still true; the PR just opened and must be recorded; you are an
  orchestrator checking a delegate's branch.
- **Also:** someone asks for the reasons of their uncommitted changes, or of a branch with no pull
  request ("write the reasons for my changes", "open it in Lantern with the reasons"): `local`
  below, then `lantern --compare` to open it. Only when asked, never on your own.
- **Do not:** map a whole project or heal a large backlog of drift (`lantern-setup` refresh);
  write anything outside `.lantern/`; mark files `~ + -` (claims are not used); run without
  `.lantern/map/` (the scripts stop and say so).

## The six commands

`node $S/scripts/sync.mjs <command>`; each prints a short report and takes `--json`.

| command | does | exit |
|---|---|---|
| `status [--base <b>]` | Drift of the map against the working tree: records **changed** (hash mismatch), files **new**/unmapped, records **gone**. With `--base`, also the change set `<b>...HEAD` (added, modified, removed; a rename is a removal plus an addition), and the PR records present. Warns when some map or section files still carry `#model` and others do not (a map stripped by hand; run `migrate-model.mjs` for the whole map). | always 0 |
| `finish --base <b> [--model <your exact id>] [--include-drift]` | Deterministically deletes the records and text keys of files that no longer exist (and a map file, with its `lang/` files, that becomes empty). Then prints the **work list**: the files to re-map, each with the hash to record and why. Writes nothing else. Does not commit. | 0; 2 on a model outside the policy or bad input |
| `pr [<id> --url <u> --title <t>] --base <b> [--branch <br>] [--summary <s>] [--reason <path>=<reason>]... [--reason-file <json>] [--order <path>]... [--order-file <json>] [--flow-file <json>] [--describe-file <json>] [--plan <slug> --item <id>]...` | Writes `.lantern/prs/<id>.pr` (grammar: `$L/references/format.md`, "Pull requests"), checks it with `$L/scripts/prs.mjs`. `#head` is the last commit that touched anything outside `.lantern/`. Refuses to overwrite a record of another branch, or to add a second record for one branch. Reasons: `--reason <path>=<reason>` (repeatable) and `--reason-file` (a JSON object `{"<path>": "<reason>"}`) give one line per changed file (max 160 characters; whitespace is folded to single spaces; an empty reason removes it; a path that is not in the change set, an over-long reason or a control character exits 2). Reasons already in the record are kept when it is rewritten. **Every changed file needs a reason: `pr` refuses (exit 1, listing the files, writing nothing) while any lacks one.** Lockfiles, images, fonts, minified, snapshot and generated files get a default one-line reason automatically. Review order: `--order <path>` (repeatable, first = review first) and `--order-file` (a JSON array of paths) write one `#order` line per file; either replaces the recorded order (`--order-file '[]'` clears it), none keeps it when the record is rewritten; a path outside the change set or named twice exits 2; a partial order is fine. Flow: `--flow-file` (a JSON array of stories `{"title", "steps": [{"kind", "text"}], "below": [...]}`, a consequence being `{"kind": "consequence", "old", "new"}`; any step may add `"files": ["<changed path>", ...]`, at most six, each a file of this change set, written as `#file` lines under the step; grammar and limits in `$L/references/format.md`, "Pull requests") writes the `#story` / `#step` / `#below` lines after the reasons; `[]` clears it, none keeps the recorded flow, and anything that does not validate exits 2 and writes nothing. Description: `--describe-file` (a JSON object `{"what": [...], "before": [...], "after": [...], "verified": [...]}`, every key optional, each entry a plain-words line of at most 400 characters, at most 8 per key; markers, `delegate:cost` and table rows are refused) writes `#describe` lines after `#summary`; `{}` clears it, none keeps the recorded one, invalid input exits 2 and writes nothing. Plan ticks: `--plan <slug>` with one or more `--item <id>` writes a `#plan <slug> <item>` line per item right after the description (`$L/references/format.md`, "Plans"); it refuses (exit 1, nothing written) a plan that is not in `.lantern/plans/` or an item the plan lacks, a re-run keeps the recorded ticks unless `--plan` is given again, and it needs `lantern-plan` beside this skill. Does not commit or push. **A branch with no host PR:** called without `<id>`, `--url` and `--title` (and with every other argument as above) it writes the same record, key the branch name, to `.lantern/local/<branch, / as __>.branch` (header `lantern-branch 1`, `$L/references/format.md`, "Local comparisons"): that folder is ignored by git, so the record is never staged by `git add .lantern` and never reaches a merge; `pr` also copies it into the main checkout's `.lantern/local/` when run in a linked worktree (adopting it removes that copy), and `carry` redoes that copy. A later `pr <id> --url ... --title ...` for the same branch **adopts** it: reasons, order, flow, description and plan ticks are kept (arguments still override), `.lantern/prs/<id>.pr` is written and the local file is removed. **A map-only PR is recorded like any other:** when nothing changed outside `.lantern/` but the map did (a seed, a refresh), the record has no file lines, a default `#summary Lantern map only: no source file changed`, and `#head` is the last source commit in the history (the merge base when there is none); a branch that changed nothing at all is still refused. | 0; 1 refused; 2 bad input |
| `dismiss <id>...` | For each id deletes `.lantern/prs/<id>.pr` if it exists and inserts the id into `.lantern/prs/dismissed` (created with its header `lantern-prs-dismissed 1`), unique and sorted, idempotent. Exit 2 on an invalid id. Only merged or declined PRs should be dismissed: the CLI cannot know a PR's state. Never commits or pushes; commit it like any map change. `pr <id>` refuses (exit 1) a dismissed id; `status` shows `dismissed: N`; `verify` fails on a malformed file. A deleted record that ticked a plan item is named in a `warning:` (the tick leaves with the record; mark the item verified first). | 0; 2 bad input |
| `tidy --base <b> [--dry-run]` | After a seed PR merged: deletes the **untracked** `.lantern/` files in the working tree whose content is identical to `<b>`'s (the copy the checkout was seeded from), prunes the directories that empties, and keeps every untracked file that differs or that `<b>` lacks. Never touches a tracked file. `status --base` names the candidates (`stray:` line, `untrackedDuplicates` in `--json`). Run it after `git fetch origin`, before the pull that would otherwise refuse to overwrite them. | 0 |
| `local --base <b> [--head <br>] [--reason <path>=<reason>]... [--reason-file <json>]` | Reasons for a comparison that has **no pull request**: the uncommitted working tree against where it left `<b>` (default), or a branch `<br>` against `<b>`. Same reasons as `pr`, by `$L/references/reason.md` (`{"<path>": "<reason>"}`; lockfiles and assets get a default), written to `.lantern/local/<b>__<br>.reason` with each file's version, so editing a file retires its reason until it is written again. The folder carries its own `.gitignore`: it is never committed and `verify` ignores the `.reason` files in it. Partial is fine: the Lantern app offers to write the rest itself. Use the same `<b>` the person sees in Lantern (`origin/main`, not `main`, when that is the chip). Then `lantern --compare <b>[..<br>]` opens it. A branch that has all of a PR's parts (order, flow, description, plan ticks) but no PR is `pr` without `<id>`, not this. | 0; 1 nothing differs or no reason; 2 bad input |
| `carry --from <worktree> --branch <br>` | Run in the project checkout: copies the branch record `pr` (no `<id>`) wrote in `<worktree>/.lantern/local/` into this checkout's `.lantern/local/` (creating its ignoring `.gitignore`), after parsing it: exit 1 when there is none, it is malformed or it records another branch. `pr` (no `<id>`) already mirrors the record into the main checkout when run in a linked worktree, and `verify` is red while that copy is missing or differs; run this before removing the worktree when it is. The copy is never committed. | 0; 1 refused; 2 bad input |
| `verify --base <b> [--require-pr] [--require-reason] [--require-order] [--require-flow] [--branch <br>]` | The gate. Exit 1 when the change set touches a mapped source file whose record is stale or missing, when a removed file still has a record, when `validate.mjs . --settled` fails, when a `.pr` record is malformed, or when the source has uncommitted changes. `--require-pr` also fails without a record for this branch (a `.lantern/prs/*.pr` record, or the local `.lantern/local/*.branch` record of a branch with no PR, read from the working tree it runs in) whose `#head` and file list match the branch, and when the branch adds a `#model` line or `"model"` field to a `.lantern/` file that had none. A changed file in this branch's record without a reason (lockfiles, assets and generated files excepted) is always a failure naming the files; `--require-reason` also fails without a record. Likewise a changed file with no `#order` position is a `warning:` and `--require-order` fails on it. A malformed flow in any record is always a failure; `--require-flow` also fails this branch's record when it has no flow (a map-only record, with no file lines, is exempt). A flow in which no step has a `#file` is a `warning:`. The `[vocabulary]` warnings `validate.mjs` prints (a feature named after a platform or system, an unlisted or near-duplicate `ext:` id) are surfaced as `warning:` lines and never fail it; so are the `[relations]` warnings (a platform with gateway files, or an infra platform, that relates to no other platform). With a `.lantern/areas`, `areas.mjs check --allow-unassigned` runs too: each failed rule reason and each feature under "To assign" is an `[areas]` `warning:`, never a failure; no file, no output. With a `.lantern/plans/`, `lantern-plan`'s `plan.mjs check --all` runs too: an error in a plan this branch changed fails it, in any other plan it is a `warning:`; a record that ticks a plan or an item that is not there is a `warning:` and never fails it. | 0 green; 1 red |

The change set is what is **committed** on the branch since `<b>`, excluding `.lantern/`: commit the
code before `finish`. `<b>` is the branch the PR targets (`origin/<b>` is tried when `<b>` is not
local). `finish` lists a file when its record is missing or stale, when a mapped file's relation or
`#see-also` points at a removed or renamed file, or when a relation's `#symbol` is gone from a
changed target. The map records no model, so a file another agent mapped is listed only when it
changed. It notes sections that cite a touched file. Drift the change did not cause is reported, not
listed, unless `--include-drift`.

**Markdown is a node like code.** A `SKILL.md`, `protocol.md`, reference, agent, command or
`CLAUDE.md` that `lantern-setup` maps (its "Which markdown is mapped") has a record like any source
file, so a change to it is stale until re-mapped, `finish` lists it, `verify` checks it and the PR
record lists it with its node. A `skill` file whose `@` target was removed or renamed, or whose
`#symbol` is gone, is listed too. Re-map it as setup does: `refs.mjs` for the candidates, then judge
(`$L/SKILL.md`, "Skill files and references"). Markdown the rules do not map (a project README, docs)
is never on a work list. On a map made before markdown was mapped, the markdown files show in
`status` as new/unmapped drift and `verify` fails on them until they are healed (`--include-drift` up
to 10 files, otherwise a `lantern-setup` refresh), exactly as for any file nobody mapped yet.

## Reasons without a pull request

Solo work has no PR to record, so the reasons that `pr` writes into `.lantern/prs/` have nowhere to
go. When a person asks for them (never unasked), do the one step `pr` would have done for the why,
and nothing else of the PR flow:

1. List the change: `git diff --name-only <b>... -- . ':!.lantern'` plus `git ls-files --others --exclude-standard`
   for the working tree, or `git diff --name-only <b>...<br>` for a branch.
2. Write `.ai/tmp/reason.json` as for `pr`: one entry per file, by `$L/references/reason.md`.
3. `node $S/scripts/sync.mjs local --base <b> [--head <br>] --reason-file .ai/tmp/reason.json`.
4. `lantern --compare <b>[..<br>]` opens the Lantern app on that comparison with the reasons under
   each file. Do not commit `.lantern/local/`; the map update, if also asked for, is the finish loop
   above as usual (it works on the working tree), committed on its own.

A finished branch (a delegate's, in local mode or with no PR wanted) is different: it gets everything a PR
gets, by step 6 of "The delegate flow" with `pr` called without `<id>`, `--url` and `--title`. That record
is local too (`.lantern/local/<branch>.branch`, never committed); `verify` takes the same flags on it.

## Model — the same policy as setup

Re-mapping is mapping: **Sonnet, Opus or Fable of any version, or the exact id `gpt-6-astra`** (`node $L/scripts/model.mjs floor`, `check <id>`)
does it, exactly as in `$L/SKILL.md` ("Model"). On the Codex route (`--provider codex`) `gpt-<version>-sol` (recommended 6.1), `gpt-<version>-astra` (recommended 6) and `gpt-<version>-terra` (no recommended version) of any version pass too. Sonnet 5.5, Opus 5.5 and Fable 5.1 or newer are
recommended: `finish --model <your exact id>` on an older version prints a one-line note and goes
ahead. `finish` exits 2 on a model outside the policy (Haiku, an unknown id). Then, do not re-map: dispatch the listed files to a `lantern-mapper` worker (its brief
is in `$L/SKILL.md`, "Where work is dispatched") or stop and say what is needed. Records other
agents wrote stay as they are unless they are on the work list.

## The delegate flow

1. **Before you start:** `node $S/scripts/sync.mjs status`. Drift here was not yours; note it.
2. **Do the work** and commit the code. Scratch goes to `.ai/tmp/` (gitignored), never a tracked path.
3. **Finish the map** — the loop:
   1. `node $S/scripts/sync.mjs finish --base <target> --model <your exact id>`
   2. Re-map **exactly the listed files** by `$L/SKILL.md` Procedure step 3 (read each file in full,
      write its record with the listed hash, texts in `lang/<primary>/`, drop keys of relations that
      are gone, delete other-language keys whose primary text changed), and re-check listed sections'
      evidence. Files not on the list are not touched.
   3. `node $L/scripts/validate.mjs . --settled` must exit 0. Fix, do not skip. The re-map keeps
      `$L/SKILL.md`'s three vocabulary rules: a feature is a capability, never a platform, channel
      or vendor; an `ext:` target is an outside system, never a library. It also keeps its
      "Relations that cross platforms": a network call into this repository is a relation to the
      handler file, a build or deploy file is a relation to the service's entry, and nothing is
      written when the target does not resolve to exactly one file. Reuse an id from
      `.lantern/features` and `.lantern/systems`, never edit either, run `node $L/scripts/systems.mjs
      add <id> --text "<short>"` for a genuinely new system, and report any feature the change needs
      that does not exist (except a feature your own change adds or renames: declare its id in
      `.lantern/features` by Edit; rename one with `node $L/scripts/retag.mjs . retag-feature <old> <new>`). When `.lantern/areas` exists and the change adds or renames a feature,
      place it under the area it belongs to, or add an area when none fits (the setup skill's
      "Areas loop" naming rules), by Edit in this PR; `node $L/scripts/areas.mjs . check
      --allow-unassigned` must exit 0. If the feature fits no area or placing it would break
      `check` (an eighth area), rebuild the areas in this PR: only the setup skill's "Areas loop"
      (`propose`, write, `check`, blind `lookup`, at most 3 rounds), regrouping the existing features
      plus the new one, never the full retag; it costs a few model calls (`areas.mjs . lookup run
      --out .ai/tmp/areas`: one short no-tools call per feature, no subagent readers). Only if the loop fails within the cap leave the existing tree untouched and the
      feature out of it ("To assign"); never delete the tree or wait for a person. Report
      `AREAS: rebuilt <old ids> -> <new ids>`, `AREAS: placed <feature> in <area>` or
      `AREAS: to assign <feature> (<reason>)`, and say in the PR record's why or flow for
      `.lantern/areas` what changed in plain words. After the code is green and before the first map `finish`,
      fetch `origin` and merge the PR target into the branch (no force, no rebase; through the
      identity wrapper when one is declared; a conflict outside `.lantern/` goes back to the green loop), re-run `check
      --allow-unassigned` and re-place your own features if the tree changed underneath; a conflict in
      `.lantern/areas` or `areas.json` takes the target's version, then re-places only your features.
   4. Run `finish` again. **Repeat from 3.2 until it prints `WORK LIST EMPTY`.**
   If `status` in step 1 showed drift, heal it in this PR with `--include-drift` (say so in the PR
   body) only when changed plus new/unmapped is up to 10 files (`gone` records are pruned by `finish` anyway); otherwise stop and tell the orchestrator.
4. **Commit the map:** `git add .lantern` (that path by name, never `-A`), then
   `git commit -m "chore: update the Lantern map"`. Only `.lantern/` may be in it.
5. **Push and open the PR** with the host skill (`lantern-bitbucket` or `lantern-github`). Read the PR id
   off the URL it prints. The task being to open a PR, branch, commit, push and open it: do not ask
   first whether to commit or push.
6. **Record the PR:**
   `node $S/scripts/sync.mjs pr <id> --url <pr url> --title "<title>" --base <target> [--summary "<one line>"] --reason-file .ai/tmp/reason.json --order-file .ai/tmp/order.json --flow-file .ai/tmp/flow.json --describe-file .ai/tmp/describe.json`
   with a reason for every changed file, written from your own diff by `$L/references/reason.md`
   (`{"src/a.ts": "Rejects a negative pid before it reaches kill()"}`; `--reason <path>=<reason>` does one file). The Lantern app shows it under the file. `order.json` is a JSON array of every changed path in the best order to review them: the file that carries the core idea or contract first, then the logic that uses it, then wiring/IPC/UI, then tests, then map, docs and generated files last; the app numbers the files and steps through them in that order. `flow.json` is the PR's flow in plain words for the Flow view (`lantern-delegate`'s `protocol.md` says how to write it). Then `git add .lantern/prs/<id>.pr`, `git commit -m "chore: record pull request #<id> in the Lantern map"`
   (the second commit touches only `.lantern/`, so no hash goes stale) and a **plain** `git push` of
   your own branch. Never `--force`.
7. **Later code commits on the same branch** (review fixes): repeat steps 3-4, then re-run step 6's
   `pr` with the same arguments (same id and branch: it rewrites the record) and commit and push it.
   `#head` must follow the code, or `verify --require-pr` fails. Existing reasons are kept; a file
   added since needs its own `--reason` and a place in `--order-file`.
8. Finish with `node $S/scripts/sync.mjs verify --base <target> --require-pr --require-reason --require-order --require-flow`: green before you report.

When the local branch differs from the pushed one (a delegate on `worktree-agent-<id>` pushes as
`<type>/<slug>`), pass `--branch <type>/<slug>` to both `pr` and `verify`.

**Stacked branches.** `<target>`/`--base` may be another task's pushed, unmerged branch (a map
refresh, a previous task): the change set is `<that branch>...HEAD`, so the record lists only this
PR's files and `#base` names the branch below. Retarget the PR onto the real target when the one below
merges, and rewrite nothing else.

**A record for a PR that is already open** (made without a delegate, or one that lost its record) is
made in a temporary worktree on the PR branch, with no merge and no checkout in the main checkout:

```bash
git fetch origin
git worktree add --detach .ai/tmp/pr-<id> origin/<type>/<slug>
node $S/scripts/sync.mjs pr <id> --url <url> --title "<title>" --base <target> --branch <type>/<slug> --reason-file .ai/tmp/reason.json --order-file .ai/tmp/order.json --root .ai/tmp/pr-<id>
node $S/scripts/sync.mjs verify --base <target> --branch <type>/<slug> --require-pr --require-reason --require-order --root .ai/tmp/pr-<id>
git -C .ai/tmp/pr-<id> add .lantern/prs/<id>.pr
git -C .ai/tmp/pr-<id> commit -m "chore: record pull request #<id> in the Lantern map"
git -C .ai/tmp/pr-<id> push origin HEAD:refs/heads/<type>/<slug>   # plain, never forced
git worktree remove .ai/tmp/pr-<id>
```

`--branch` is required because the worktree is detached. The commit touches only `.lantern/`. This
is the orchestrator's path from the main checkout; a delegate never uses `git -C`.

## The orchestrator flow

- **Before dispatch:** `node $S/scripts/sync.mjs status` on the checkout the delegate will branch from.
  Drift there is inherited by every delegate: heal it first with a `lantern-setup` refresh, or
  tell the delegate to use `--include-drift`.
- **On handover:** in the delegate's branch (a worktree of it is fine)
  `node $S/scripts/sync.mjs verify --base <target> --require-pr`. Red → back to the delegate with the
  printed problems. Green means the map is true for the change and the PR record is **in the
  branch** (`git show --stat HEAD` names `.lantern/prs/<id>.pr`). It does not review the map's
  content: a fresh hash on a wrong description passes, which is why re-reading is a rule below.

## Rules

- **Never map on a model outside the policy.**
- **The map records no model, so never write a `#model` line or a `"model"` field.** Leave an
  existing one exactly as it is, even in a file you are editing; only `$L/scripts/migrate-model.mjs`
  removes them, once for the whole map, in its own commit, after the team has updated the skill.
  `status` and `verify` warn on a partly migrated map.
- **Never bump a hash without re-reading the file.** A fresh hash on an old description is the one
  lie the format cannot catch. A carried-over gotcha or `#see-also` is re-judged, not kept.
- **`.lantern/` is the only thing written.** No source comments, no annotations. Stage it by name;
  never `git add -A`.
- **No commit or push by the scripts.** You commit, in the two steps above, and push only your own
  branch, plainly.
- **Scratch to `.ai/tmp/`**, gitignored in the project; check first.
- **No secrets in records** — purposes describe what a value is for, never the value.
- **The PR record lists changed files, not their content.** State is never stored; do not edit it
  by hand.
