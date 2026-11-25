---
name: gauge
description: Gauge — prove the work is really done before shipping. Pick evidence by the changed files (A the repo's check commands, B open a browser, C steps for a human), then output a Verify table with status VERIFIED/PARTIAL/FAIL · every PR also gets a verdict from a fresh verifier pinned to its patch-id · record every passing item in state and tick "Not done yet" in the open PRs yourself. Use before every commit / PR, when the user runs /pitwall:gauge, "verify", "พิสูจน์ว่าใช้ได้" — /pitwall:lap calls this skill itself · repo values live in .claude/agent-loop.md
user-invocable: true
---

# /pitwall:gauge — proof the work is really done

Read `.claude/agent-loop.md` first (sections checks, level B, repo-specific evidence)

Rules:
1. Evidence must match what you changed — changing price logic but showing only a passing build ≠ verify
2. Attach real output (the summary line of the command), not the word "passed"
3. Can't check it yourself → write "not checked yet" + a specific reason why the agent can't do it itself + numbered steps for a human, each with the result they should see; never count it as passed · "can't check it yourself" = only the 3 wait cases (⏳) that `/pitwall:lap` lists (at the top of `${CLAUDE_PLUGIN_ROOT}/skills/pitwall/playbooks/lap.md`) — do everything else yourself (build the conditions per "states to build" in the profile)
4. A level A item FAIL = the work is not done; do not ship

| Level | Who checks |
|---|---|
| A | the agent can run it itself, headless |
| B | one dev server per checkout — two servers in one checkout share its build output and leak each other's env values into the evidence; a second server needs its own worktree · a wait longer than the browser tool allows per call → poll in short calls, never one long call · the agent can do it if there is a dev server + browser per the profile (browser entry — usually the human's default browser, not Playwright) — use the port / pages / time from the profile · no browser but the profile has a `verification skill` → drive the item with that skill (its Launch → Doctor → Drive → Evidence → Cleanup) · neither → steps for a human · stuck past the time limit → change the method first, don't hand it to a human |
| C | needs a human: real transactions / irreversible actions, the profile's human-only steps (done together as the pair run below), comparing with the design, UX feel |

## Level C together (pair run) — the human only does the human-only steps, the agent drives the whole flow

Use when the user asks to test C together, or when `/pitwall:lap` gauging hits an item that needs a human-only step while the user is present (the profile's browser is connected) · **the human doesn't type along the way** — the agent reads the results from the page itself

1. **Announce once, then start right away**: the list of steps for the whole flow (e.g. connect → sign-in → list → cancel → buy → sweep → switch account) + which step will need which human-only step (wallet popup, 2FA prompt, payment confirm …) · the human's single "go" = approval for the whole flow (don't ask again step by step)
2. **Split the work**: the agent does everything on the web page (navigate, enter prices, click buttons, check results) · the human does only what the agent must not do = the human-only steps in the profile, e.g. confirm / reject in a wallet popup (connect, switch network, sign, transactions) — **the agent must never click in the wallet popup or sign on the human's behalf**
3. **Don't wait for the human to type**: click the button that starts the human-only step, then **poll yourself** every ~5 seconds with lightweight means (`get_page_text` / network / console before a screenshot) until you see the next state — button changes, auth / tx request returns 200, success toast, tx hash, item moves tabs — then move on to the next step yourself
4. **Waiting too long**: 2 minutes with no change → warn in 1 line (in the profile's user language) "Waiting for your confirmation: <what>" then keep polling · 5 minutes → treat the user as away (⏳ case 1 of `/pitwall:lap`) and skip to the steps that don't depend on this one · reject / error → record the result + retry once, then continue
5. **The tail end is all the agent**: steps that need no human-only step (read the result pages, lists, history, filters, balances, links, refresh) the agent does and checks entirely by itself after the transactions finish
6. Bug found mid-flow → note it, don't stop the flow (fix it after the flow ends, unless the bug makes the next step impossible)
7. Flow ends → one Verify table (every step + evidence: transaction / request id, screenshot, response) + list of bugs

## Baseline set (every task that touches code) — level A

Every command in the profile's "checks" section (lint compared against `lintBaseline` in state; no state → compare with the base branch)

## Extra evidence by changed files (`git diff --name-only origin/<base>...HEAD`)

| Changed files | Evidence | Level |
|---|---|---|
| logic with no UI | a unit test covering the new case (none → write one, per the repo's test rules) | A |
| docs | the referenced paths / files / task numbers really exist (`ls`, `git grep`) | A |
| dependency (lockfile) | frozen install, then build | A |
| page / component | open the affected pages through the loop's dev server, screenshot, console errors = 0, compare with before the change | B |
| + rows in the profile's "repo-specific evidence" section | | |

Then add every item of the **task's DoD** as a row in the table, with the right level

## Report (example — use your repo's commands / pages from the profile)

Write it in the profile's language (PR / commit language in a PR body, user language when reporting to the user).

```markdown
## Verify
| Item | Level | Command / method | Result |
|---|---|---|---|
| typecheck | A | `<typecheck command>` | ✅ 0 errors |
| Market page | B | profile browser `<dev server>/<page>` @1366 | ✅ grid shows, console 0 error |
| Real purchase | C | not checked yet — 1. sign in 2. buy 1 item → success + the item shows in the account | ⏳ |

Status: **PARTIAL** — all A passed, 1 C item left
```

- **VERIFIED** = all A and B passed, no C items
- **PARTIAL** = every A and B item you can do yourself passed; only items in the 3 wait cases (⏳) of `/pitwall:lap` or C items are left
- **FAIL** = some A item failed

## Independent verifier — the verdict a PR merges on

The writer's `/pitwall:gauge` is not the verdict (pstack `shipping`: safe = a verdict from an agent that did not write the code) · every PR gets one from a fresh agent, pinned to its head · the single home of the verifier's scope and of the patch-id command — other files point here

**patch-id** of a PR = the stable patch-id of its diff against the merge-base with its base branch (the profile's base, or the parent PR's branch in a stack), **without the files the profile's `git` section lets the agent resolve itself** (plan rows, progress logs — bookkeeping that every sibling PR appends to, so each merge would make the other PRs' verdicts stale for no code change) · a PR that changes only those files → its whole diff:

```bash
git diff $(git merge-base origin/<pr base> <head>) <head> -- . ':(exclude)<resolve-yourself path>' … | git patch-id --stable | cut -d' ' -f1
```

The patch-id changes only when the PR's own hunks or their context lines change outside those files (a new commit, a conflict resolution in code, base editing lines next to the PR's) · a docs conflict resolved per `/pitwall:merge-order` 2b keeps it → every result pinned to the old one is stale · a clean merge / rebase of base over unrelated code and a retarget after the parent merged keep it → the verdict survives

When: after the writer's `/pitwall:gauge`, on the committed head, before `gh pr create` (`${CLAUDE_PLUGIN_ROOT}/skills/pitwall/playbooks/opening-a-pr.md` section 2) · again for an agent PR with no verdict or a stale one (`${CLAUDE_PLUGIN_ROOT}/skills/pitwall/playbooks/lap.md` sync item 0)

1. **Lead**: clean tree, `git rev-parse HEAD` = the head, compute the patch-id, record the writer's pair-run results at it (next section item 1) · human-only-step items with no pair-run entry at this patch-id: user present → pair run first (section "Level C together"), away → they stay ⏳ case 1 · spawn a **fresh** agent of the profile's `verifier` row (`agents per task`) — read-only, per `${CLAUDE_PLUGIN_ROOT}/agents/pitwall-agent.md` "As a verifier"
2. **Prompt holds only**: the task text (plan row + DoD / tracker description / the user's request) · the diff (the patch-id command before the `|`, base filled in) + head SHA + patch-id · this file + the profile sections checks, level B, states to build, repo-specific evidence · the FAIL rows of the previous verdict and its head, when this run follows a FAIL re-brief (item 4) · state `verified` entries with `method: "pair run"`, the same `patchId` and the same `pr` or `branch` (any level) · a re-verify of a PARTIAL PR whose "Not done yet" boxes are all ticked since (`${CLAUDE_PLUGIN_ROOT}/skills/pitwall/playbooks/lap.md` section 10): also the `verified` entries at this patch-id for this PR behind its ticked boxes, any `method` · the Always park question (item 3) — **never** the writer's brief, `decisions.tsv`, review table or Verify table
3. **Verifier**: picks its own rows (baseline set + extra evidence by changed files + the task's DoD), re-runs set A and drives every level B row at the head · human-only-step items: **never asks the human for one** — a pair-run entry from the prompt is the result (row says `pair run <at>`), none → ⏳ case 1 · a ticked-box entry from a re-verify prompt (item 2) is the result of an item the verifier cannot run itself the same way (row says `<method> <at>`) · returns a Verify table + status (VERIFIED / PARTIAL / FAIL) · **Always park question**, answered in every run whatever the status, always over the whole PR diff (merge-base … head, the item 2 diff), also in a FAIL re-brief run that checks only the delta for everything else: does the diff touch money / price / fee, permissions / security, user data, or deletes / irreversible actions? → one line under the Verify table, `Always park: none` or `Always park: <topic>, … — <file:line>, …` · a topic found is never a FAIL by itself: it keeps the PR for a human merge (`merge: auto`) · the lead records the line in every run, FAIL included (next section item 1) · **what may FAIL** — only (a) a set A item, (b) a DoD item not met, (c) a rule of the spec / plan that the task implements, wrong in the code or with no test that fails when the rule breaks, (d) a repo rule (profile `repo rules` files) the diff breaks · anything else (style, a later row's work, an extra test, an edge case the spec does not name, an agent default) is an INFO line, never a FAIL · **every gap in one pass**: list all the FAIL items the verifier finds, not the first one, since the re-brief (item 4) fixes them all at once
4. **FAIL** (an A item, or a B row that is not ⏳) → record one `item: "verdict"` entry with `evidence: "FAIL"` at this patch-id (next section item 1) · inside the loop: back to `coding` with the verifier's rows (one re-brief, as in `checking`), new commit, continue from `checking` (the normal steps after it), then a fresh verifier whose prompt also holds the FAIL rows and the head they failed at: it re-runs set A, checks those rows and the diff since that head, and does not reopen the rest, which the first verifier already passed (a new FAIL needs a line in the new commits) — except the Always park question, which still covers the whole PR diff (item 3) · fails again → park · outside the loop: stop and report
5. **Pass** → record (next section) its ✅ rows + one `item: "verdict"` entry (`evidence` = the status) · the PR body's Verify table carries the verifier row (`opening-a-pr.md` section 4)

## Record results + tick the PR yourself (every run — don't wait to be asked)

Passing results must reach the PR on their own, whether the test ran in `/pitwall:lap`, a pair run, a `/pitwall:gauge` the user asked for, another session or another machine — the human doesn't have to tell you to go tick

1. **Record** every ✅ B / C item and every verifier verdict in state (path in the profile; no file → create `{ "verified": [] }`): `verified += { pr, branch, headSha, patchId, method: "pair run" | "writer" | "verifier", verifier, item: "<item — game / flow / screen size>" | "verdict", level, evidence: "<short: tx hash / request 200 / screenshot / VERIFIED / PARTIAL / FAIL>", at: "<YYYY-MM-DD>" }` · `headSha` / `patchId` = the committed head that was tested (patch-id command above) · `method` = how it ran: `pair run` (with the human doing the human-only steps), `writer` (the lead's own `/pitwall:gauge`), `verifier` (the independent verifier) · `verifier` = who ran it: `main` or `<subagent> <model>` · `pr` = null until `gh pr create`, then fill it · a result from an uncommitted tree (writer gauging in `/pitwall:lap`) → record it after the commit with that commit's `headSha` / `patchId` only when the commit adds nothing but the `/pitwall:lap` `docs` step to the tested tree, else run it again · don't record items that are ⏳ / ❌ — the one exception is a verdict FAIL · the verifier's Always park line (every verifier run) → `{ …, method: "verifier", item: "always-park", level: "A", evidence: "none" | "<the topics and file:line it named>" }` at the same `headSha` / `patchId` — `${CLAUDE_PLUGIN_ROOT}/skills/pitwall/scripts/merge-gate.mjs` passes a PR under `merge: auto` only on `evidence: "none"` at the PR's current patch-id · the profile has a "multi-machine" section → **send** the state
2. **Tick only the PR with the same patch-id**: `gh pr list --author "@me" --state open --json number,title,headRefName,headRefOid,baseRefName,body` → skip PRs whose head is a destination branch (`<base> → release`) → `git fetch origin -q` → patch-id of each PR's current head (`origin/<baseRefName>`, `headRefOid`) → the entry's `patchId` equals it **and** its `pr` (or `branch`) is that PR → in the "Not done yet (before merge)" section, the `- [ ]` items that talk about the same thing as the passing item (game + flow match, not just similar words) → replace with `- [x] ✅ local <at> @<7-char headSha> — <evidence>` then `gh pr edit <n> --body-file` · each PR in a stack needs its own result — a result never counts for another PR · **untick** the other way, on every re-verify and after any push to a PR that has a verdict: a `- [x] ✅ … @<sha>` box in "Not done yet" whose `@<sha>` has a patch-id (its state entry, or the command above at that sha) ≠ the current one → back to `- [ ] ⏳ case <1–3>: <reason>` and put `[PARTIAL]` back at the start of the title
3. **PR opened later** (`${CLAUDE_PLUGIN_ROOT}/skills/pitwall/playbooks/opening-a-pr.md` or splitting a branch into a stack): before `gh pr create`, the `verified` entries whose `patchId` = the patch-id of the head being opened and whose `branch` is this branch → ✅ rows in the Verify table; those items stay out of "Not done yet"
4. "Not done yet" has no `- [ ]` left and the title starts with `[PARTIAL]` → `gh pr edit <n> --title "<title without [PARTIAL]>"`
5. Report in 1 line (in the profile's user language): `Ticked: #101 (C list+cancel), #102 … · Still open: <item>` — then the `/pitwall:merge-order` result moves on its own

Never tick an item whose result has a patch-id other than the PR's current head · a "dev env after merge" item cannot be ticked from local · delete `verified` entries once every PR of that branch has merged (sync at the start of a `/pitwall:lap` round)

## When verify misses

A human finds a bug that the Verify table says passed → don't just fix the bug: add a test or add a row to the profile (repo-specific evidence) so the next round catches it by itself — fix the car, not the finish line
