---
name: pitwall
description: Single entry point of the agent loop — reads the request (Thai / English), picks a playbook, then does it with evidence. Use when the user runs /pitwall:pitwall or says "ใส่คิว", "ลุย", "ออกรถ", "ทำ 1 งาน", "หยุดหลังจบงานนี้", "หยุดเดี๋ยวนี้", "merge ตัวไหนก่อน", "แก้บั๊ก", "เทสด้วยกัน", "เปิด task", "ผมย้ำอะไรบ่อย", "วางแผน", "สัมภาษณ์ผม", "แบ่ง phase", "ให้ทำเอง", "งานไหน agent ทำได้", "PR ไหนพร้อม" · repo values live in .claude/agent-loop.md
user-invocable: true
---

# pitwall

The skill holds no repo-specific values: everything that belongs to the repo (base, check commands, browser, human-only steps, tracker, plan, recipes for building states) lives in the profile `.claude/agent-loop.md` · no profile → only `init`, `doctor` and `verify-setup` run; every other request stops with "this repo has not set up pitwall yet — run `/pitwall:init`" · never guess values the profile should hold

**pitwall dir** = `${CLAUDE_SKILL_DIR}` (this skill's folder: `playbooks/`, `principles/`, `scripts/`) · every `playbooks/…`, `principles/…`, `scripts/…` path in this skill and in the playbooks is relative to it, and `<pitwall dir>` in a command means this path

**Update check** (the lead, once per session, not a subagent): `bash scripts/update-check.sh` · it prints a line → pass it on to the user in the profile's user language, with the command as is, then carry on with the request

## Rules you cannot skip

In the report, state which rule changed which decision

1. **Prove it against the real thing** — the real page / request / value, not a stand-in · typecheck passing does not mean the UI works
2. **A check the agent can run itself must never be handed to a human** — ⏳ is allowed only for "the 3 wait cases (⏳)" at the top of `playbooks/lap.md` (`1 human-only step while the user is away` · `2 needs the dev env after merge` · `3 environment unusable`), with a specific reason
3. **Ask everything once, up front; never mid-round** — questions that belong to the human are asked with AskUserQuestion as tick boxes, in the profile's user language, recommended option first, marked with the profile's recommended marker · labels a user reads without knowing pitwall: the concrete value (`Thai`, not "the language you write in"), no internal words (profile, row, level B) · every option is a full answer, picked with one click: the free-text box (Other) is always there, so never an option that says "tell me in Other"; gather every point of the task into a single round (before `/pitwall:drive` = briefing in `playbooks/queue.md`)
4. **Loop work uses the 3-step ladder** (next section) — every task that runs through the `queue` / `drive` / `lap` playbooks (including `/pitwall:lap` typed by the user) · work outside the loop that the user orders directly (edit files as told, answer questions) uses "Direct work" below
5. **Humans merge**, except under `merge: auto`: the lap's PR sync merges into the dev branch (the base) through `<pitwall dir>/scripts/merge-pr.mjs`, only when every gate passes · agents never run `gh pr merge` · never merge anywhere else, force-push, or touch branches the profile forbids
6. **Lessons become structure first** — script / lint / test / CI > a step in a playbook > text in rules > memory · writing the same instruction a second time = it should be a check
7. **Record decisions when you make them** — a row in the task's `decisions.tsv` (state folder), not written back at the end
8. **Speak the user's language** — read the profile `language` section before your first message, and write every line the user sees in its user language: progress lines between steps, the drive start message, relayed subagent results, round reports, not only questions · slash commands (`/pitwall:drive`), wakeup prompts (`/loop /pitwall:lap`), playbooks and subagent reports are English and say nothing about the language the user wants

## The 3-step ladder (loop / autopilot)

When you hit a fork during a run that has no answer in state (`answers`):

| Step | Use when | What to do |
|---|---|---|
| 1 Try it | the answer can be seen by running something (what an endpoint returns, shape, behavior, layout, timing) | run / prototype in a throwaway branch, then decide from the result · put the result in the PR · **read-only, or on local / testnet only** — never write data on a shared backend, no transactions, never touch anything on the "Always park" list |
| 2 Default + record | reversible, and there is a default in the rules / playbook (port = follow the source, existing behaviour = keep as is, UI = closest to the existing one) | follow the default · a row in `decisions.tsv` · PR section **Decisions to confirm** (one line each: option taken / other options / where to change it) · continue |
| 3 Park | on the "Always park" list, or no safe default | park as usual (`playbooks/lap.md`) + keep the question to ask as tick boxes next round |

**Classify before parking or asking** (the one definition — `/pitwall:queue` and `/pitwall:lap` point here) · **lists first**: an item on "Always park" / "Never default either" is parked / asked even when it can be run — a prototype only attaches evidence to the question, never answers it · *observable* = a fact a run reveals (what X does: behavior, timing, output, what an endpoint returns), not a choice (which X it should be) → step 1, the prototype result goes with the decision, not a question for the human · *not decidable by experiment* (business rule, backend / third-party value, design with no design file or source, a plan open question) → park in the run / ask in the briefing · a plateau is not a stop: change method before parking (`playbooks/lap.md` §4)

**Always park** (never use a default): money / price / fee · permissions / security / user data · deletes / irreversible · backend / third-party values not yet provided (placeholder only where the plan allows)

**Never default either** ("Never guess about" in "Direct work") if briefing has not answered it → park: business rules (limit, expiry, eligibility), API contract shape, which variant / environment / tenant a feature applies to, new design with no design file or source to compare against · the default "UI closest to the existing one" applies only to UI that has an existing version / source to anchor to

## Direct work (outside the loop)

Work the user gives directly while present: **below 95% sure of the approach → stop and ask before acting** — state what you understood, what you are unsure of, the options, and the one you lean toward and why · ask when unsure which file / pattern to use, when the task reads two ways, before an architectural decision (new file, new state, new pattern), before a refactor, before deleting or rewriting working code

**Never guess about**: business rules (pricing, limits, eligibility) · API contracts (endpoints, payloads, response shapes) · design decisions (layout, spacing, colours) with no design reference · which variant / environment / tenant a feature applies to · whether to create a new file or change an existing one

At 95%: a clear bug with an obvious cause, a pattern that already exists in the repo, a repo rule that covers the case, a change the user described in detail → go ahead

## Choose a playbook

Open a todo list whose first steps are the chosen playbook's steps, copied word for word · steps you don't do stay in the list with `skip: <reason>` — **cannot be skipped**: checking, reviewing, gauging (`/pitwall:gauge`), repro before / after the fix in `bug-fix` · a resumed `/pitwall:lap` round does not copy again, it uses the existing todo

| Request | playbook |
|---|---|
| plan the project / interview me / split into phases / open the next phase / a decision changed / `/pitwall:plan` | `playbooks/plan.md` — spec + plan rows, docs-only PR |
| queue it / briefing / which tasks can the agent do / `/pitwall:queue` | `playbooks/queue.md` (ends with briefing) |
| go / drive off / let it work on its own / `/pitwall:drive` | `playbooks/drive.md` — build and prove the whole queue, humans merge |
| do 1 task / `/pitwall:lap` | `playbooks/lap.md` |
| stop after this task / `/pitwall:stop` | `playbooks/stop.md` |
| stop now / `/pitwall:brake` | `playbooks/brake.md` |
| which to merge first / which PR is ready / `/pitwall:merge-order` | `playbooks/merge-order.md` |
| what do I keep repeating / `/pitwall:secretary` | `playbooks/secretary.md` |
| set this repo up / `init` | `playbooks/init.md` |
| is the profile complete / `doctor` | `playbooks/doctor.md` |
| make a skill that drives the app (no browser for level B, a Godot game) / `/pitwall:verify-setup` | `playbooks/verify-setup.md` — writes `.claude/skills/verify-<app>/`, runs it once |
| test together / pair run / verify / `/pitwall:gauge` | the `pitwall:gauge` skill (pair run section) |
| open a task / `/pitwall:ticket` | the `pitwall:ticket` skill |
| inside `/pitwall:lap`, by task type: fix a bug / refactor that must stay identical / bring a number down / bring over from another branch | `bug-fix.md` / `move-only.md` / `ratchet.md` / `port.md` |
| fix a bug (direct request) | `playbooks/bug-fix.md` (its steps replace `feature.md` steps 3–6), then `/pitwall:gauge` and `playbooks/opening-a-pr.md` |
| build / add / change a feature (direct request) | `playbooks/feature.md` |
| open a PR for this branch (direct request) | `/pitwall:gauge`, then `playbooks/opening-a-pr.md` |
| read-only question (how does it work / why / are you sure) | `playbooks/investigation.md` |
| matches no row | design a task-specific playbook in the todo list (every step ends with a check) **ending with `/pitwall:gauge` and `playbooks/opening-a-pr.md`**, and say so in the report |

Requests may come in the user's language; the Thai trigger phrases in the description map to the same rows.

Commands: each playbook has its own shortcut skill — `/pitwall:plan`, `/pitwall:queue`, `/pitwall:drive`, `/pitwall:lap`, `/pitwall:stop`, `/pitwall:brake`, `/pitwall:merge-order`, `/pitwall:secretary`, `/pitwall:init`, `/pitwall:doctor`, `/pitwall:verify-setup` — which invokes this skill with the playbook name as the first argument · a first argument that names a row → that playbook · anything else (`/pitwall:pitwall <request in words>`, or a request with no command) routes by the table · `/pitwall:gauge` and `/pitwall:ticket` are separate skills of this plugin

## principles (`principles/`)

Ways of thinking from pstack (MIT, Lauren Tan — source at the top of every file, license in `principles/LICENSE-pstack`, which also covers the playbooks adapted from pstack: `feature`, `investigation`, `opening-a-pr`, `verify-setup`) · read the whole file before using it · in the report / PR, state which principle changed which decision, and cite only files actually read this round

| Use when | principle |
|---|---|
| fixing a bug / chasing a root cause | `fix-root-causes`, `attack-the-premise` (already fixed twice on the same assumption) |
| before saying it's done | `prove-it-works` · a number you measured yourself → `explain-the-number` |
| before writing logic / crossing functions | `foundational-thinking`, `model-the-domain`, `boundary-discipline`, `type-system-discipline` (adapted) |
| a new requirement on an existing design | `redesign-from-first-principles` · no example to anchor to → `exhaust-the-design-space` |
| UX / feature scope | `experience-first` |
| refactor / task order / several PRs | `subtract-before-you-add`, `sequence-verifiable-units`, `minimize-reader-load` |
| work a tool could repeat | `build-the-lever` · a lesson that needs repeated reminders → `encode-lessons-in-structure` |
| handing work to a subagent / context is full | `guard-the-context-window` |
| loop / resume / several writers to the same place | `make-operations-idempotent`, `separate-before-serializing-shared-state` |
| wanting to ask the human mid-round | `never-block-on-the-human` (adapted to pitwall's briefing + ladder) |

Names the originals cite that this repo does not have: "**show-me-your-work** skill" = the task's `decisions.tsv` (`playbooks/lap.md`) · "**<name>** principle skill" = the file `principles/<name>.md`

Principles a repo turns off are listed in the profile section `repo rules`, with the reason · a repo rule that covers the same ground as a principle wins where it is more specific

## Profile contract (`.claude/agent-loop.md`)

Required sections · a playbook that needs a section that is missing → stop and say which section is missing

| Section | Holds |
|---|---|
| repo | name, state path per OS, the checkout the loop uses |
| git | base, branches never to touch, `merge: human \| auto` (optional — missing = `human`; `auto` fits only a repo whose base is the dev branch) and `dev branch` (the base again under `auto`, or `none`), branch / commit / PR name patterns, hooks, files the agent may resolve conflicts in itself |
| checks | level A commands (install, typecheck, lint + baseline, test, build, any extra repo checks), PR-body check (optional) |
| level B | dev server + port rules (`port: fixed \| free` — optional, missing = `fixed` · `fixed`: the backend allows one origin, one task at a time holds the dev server · `free`: each worktree runs its own server on a spare port), browser, pages, viewport, time per method, human-only steps (what only a human may click: wallet popup, 2FA, payment confirm …), (optional) verification skill, upkeep cadence |
| states to build | recipes for producing the states to test, or a pointer to the file that holds them |
| repo-specific evidence | file pattern → extra evidence + level |
| plan (optional) | plan folder, reading order, row format, where open questions go, rows not to queue, playbook per row type, (optional) spec file and question bank files for `/pitwall:plan` |
| tracker (optional — missing = `none`) | `tracker: clickup \| github \| none` · for `clickup`: location, tag (+ optional server / game tags), QA, meaning of each status, naming, (optional) sprint groups and work not tracked · for `github` (GitHub Issues): agent label, the `in progress` / `review` / `pending` labels, QA login, `milestone: current \| none`, naming (both in the `pitwall:ticket` skill) · `none` = no tasks, the PR is the record |
| agents per task | subagent type + model per role (`code role`, `verifier`), review panel, domain checklist files, `parallel: <n>` (optional, missing = 1: at most n tasks at once, each in its own worktree when n > 1) |
| repo rules | rules files in use, principles turned off (with the reason) |
| multi-machine (optional) | state hand-off branch |
| permissions | allow / deny for the machine that runs the loop |
| language | user language (questions, reports, recommended marker), PR / commit language, tracker comment language |

## Report

Language comes from the profile `language` section, not fixed — it governs every message to a human, not only reports (user language for the user · PR / commit language for PRs · tracker language for tracker comments); no profile → the language the user wrote in · result first · every claim has evidence or a label (checked / inferred / guessed) · full PR links
