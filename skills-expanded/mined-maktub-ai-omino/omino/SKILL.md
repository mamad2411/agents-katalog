---
name: omino
description: Keep a long-lived project plan that humans and agents share (Markdown notes in ~/.omino/projects/<id>/, one copy for every worktree). Use when a session starts with an "Omino plan:" brief, when the user types one of the Omino commands (/omino-plan, /omino-next, /omino-ghost, /omino-lock, /omino-hold, /omino-clear; /omino:plan and so on in the Claude Code plugin), or when the user talks about project goals, scope, stages, what to do first, progress, or ideas to revisit later. Reads the plan before answering, records only real decisions and progress, raises deferred ideas when their condition is met, and flags conclusions that changed requirements may have invalidated.
---

# Omino

Omino is a plan made of pieces. Each piece is a Markdown note; stages, workstreams and relations fit the pieces together. You keep it accurate across conversations so the user never has to re-explain intent, and so they can read the plan at any time.

You are the plan's careful clerk, not its owner. The user decides; you record what they decided, with where it came from.

The CLI lives next to this file: `node <this skill's directory>/scripts/omino.mjs <command>`. Below it is written `omino`. Every command accepts `--dir <project>` and `--json`.

## Where the plan lives

The plan is **not inside the working tree**. It lives in `~/.omino/projects/<id>/` (`OMINO_HOME` overrides `~/.omino`), and every worktree and clone of the project on this machine shares that one copy. `omino where` prints the folder; the session brief names it too. Edit notes there with your normal file tools, then `record`. The folder is its own git repository: each `record` is one commit there, so the plan's history never mixes with the project's commits, and you never commit plan files into the project.

Which plan a folder uses is kept in the repository's `.git` on this machine, or, when the user chose to share it, in `.omino.json` at the project root (`{"project": "<id>"}`), committed with their next commit. Never write a project id yourself: the CLI resolves it from the folder, and every `--json` answer names the plan it used (`project.id`). If the brief or a command says the plan was made for a different repository, stop and ask the user before changing the plan; `omino link <id>` is theirs to approve. `omino projects` lists every plan on this machine.

## When a plan is finished

When the user says plainly that the work this plan was for is done, that is the confirmation: run `omino close`. If you only infer it (every stage closed, the goal looks reached), ask once first. A closed plan stays readable, and `record` refuses to change it. When they then start a new piece of work in the same folder, ask what it is for and run `omino init --name <id>`; the folder now uses the new plan, and `omino projects` still lists the old one. `omino close --reopen` undoes it.

## Setting up and upgrading: the user only says yes

The user never runs Omino commands; you do. Everything a machine needs — moving a plan out of an old in-repo `.omino/` (or restoring it from git history if it was already removed), linking the folder to it, letting Claude Code and Codex write to the plan folder, adding hooks for each agent on the machine, updating older copies of this skill — is one command, `omino setup`.

- When the session brief says a one-time setup is needed, or the user asks to set up or upgrade Omino, or your edits to the plan folder are refused: run `omino setup --dry-run`, tell the user in one sentence what will change (name the files), and ask once.
- Setup only touches the agent you are running in. If you are Gemini CLI or Kimi Code CLI, add `--agent gemini` or `--agent kimi` to both the dry run and the real run, so the hooks go to the right place.
- If they agree, run `omino setup` and report what changed in a line or two. If the sandbox blocks it (Codex), request to run that one command with approval instead of asking the user to type it.
- Moving an old in-repo plan: if that repository is the user's own and the plan was shared there before, add `--share` so the link stays in the repository (`.omino.json`, part of their next commit). Commit only when the user asks.
- Never paste commands for the user to run in a terminal.

## Hooks keep the plan from going stale

In Claude Code, Codex, Gemini CLI and Kimi Code CLI, the omino plugin (or `omino setup`, which adds them to the user's settings) adds hooks. Without hooks — an agent that reached this skill through AGENTS.md — run `omino brief` at the start of a session yourself; it also carries any one-time setup request. They do nothing in a project without a plan, never call a model, and do three things:

- **Session start:** a short brief appears in your context, starting with `Omino plan:` — the active stage, work in progress, open questions, drafts to confirm, ideas due, comments the user left, and the link to the plan's page. The page service is started if it is not running.
- **Each user message:** comments the user left on the page since you last heard (`Omino: Comments the user left…`), and changes they made there (`Omino: the user changed the plan on the plan page…`). See "The page" below.
- **End of a turn:** if the turn made substantial changes (new files, or many changed lines) and nothing was recorded, you get one reminder. It is a question, not an order: most changes — fixes, wording, refactors, small tweaks — need no plan update. Change the plan only if the user decided something, the direction changed, or a planned item was finished. Otherwise finish without mentioning the plan; never record or flag something just to answer the reminder.

Without hooks (other agents, or hooks not installed), do the same by hand: run `omino brief` at the start of a session, and `omino review` lists the user's comments. The first time you use Omino in an environment, run `omino doctor`; act on what it suggests only with the user's consent.

## Three lenses

Read each turn through three lenses. One turn can touch all three, or none.

- **Intent** — why, what for, within which boundaries. `project.md` plus the "Why" of each note.
- **Arrangement** — what is in scope, in which stage (`level`), in which order, what waits, what is parked as an idea.
- **Progress** — what actually happened, and **who says so** (`source: user | agent | tool | file`).

## Every turn

1. **Classify first.** Is this a new intent, a change of arrangement, real progress — or a question, a discussion, a hypothetical? Only the first three change the plan. When you cannot tell whether the user decided something, ask; do not write.
   "Not yet", "later", "no rush on X", "skip that for now" about an **existing** item is a change of arrangement too: write it into that item's `## Arrangement` (in the user's words), and change its order or `before` if needed. Otherwise the next session will happily start on it.
2. **Read what you need.** At the start of a session, use the brief (from the hook, or `omino brief`); run `omino check --fix` if it reports unrecorded edits. When the user says only "continue" or similar, say in one line what you will do next and why (the brief lists what is next and any "not yet" notes), then start — unless a note says the user wanted to wait on it; then ask. If `review` lists open questions or a draft awaiting confirmation, ask the user about them early in the conversation — once per session, briefly, without blocking what they came to do. Then read `project.md` and the active stage. Afterwards follow only the notes this turn touches and their `requires`, `refs` and recall conditions. Do not re-read the whole plan every turn.
3. **Write or keep.** Edit only the affected notes; keep reasons and history in prose. If nothing changed, write nothing. **Keep what the user said apart from what you add.** Write the user's words as theirs. Anything you add — details of requirements, principles, an order they did not ask for — is a draft: put a `review` line on that note (or put the point under `## Open questions`), and say so in your reply. A note marked `source: user` must not contain things the user never said. Leave out details nobody asked for rather than inventing them.
   Turning what the user said into the plan's structure is writing it down, not inventing: "the first version does A, B and C, C last" becomes a stage with three work items and `before` on the others pointing at C — `source: user`, titles in their words, no `review` needed. Only detail you add on top (exact fields, formats, extra ordering) is a draft.
   Writing the plan is not a request to build it: after recording, ask whether to start, unless the user already said so. **Before creating a note, run `omino find <a few key words>`**: if a note already covers it, change or link that note instead of adding a duplicate. Tie every new idea or decision to what it is about — `refs`, `affects`, `supersedes` or a `recall` condition; a decision about the whole project can use `affects: [project]`. `record` lists new notes that are not linked to anything. After editing, run `omino record "<one-line summary in the user's language>" --source <who> --said "<the user's words that led to it>"`, adding `--session <id>` when you know the conversation's id. It captures the git branch, commit and worktree by itself, refreshes the page and prints a link for each changed note.
   When a work item is being implemented on a branch or worktree, put that branch in its `branch` field.
   If in one turn you change a finished item's requirements **and** implement the change **and** the tests pass, the tests confirm it: record with `--source tool --confirm <id>`. Do not ask the user to re-confirm what a tool just verified. When a decision `affects` items you also updated in the same turn, edit those notes in the same step so they are not flagged for nothing.
   Plan changes are never part of the project's commits: `record` commits them to the plan's own history. Commit the project's code only when the user asks.
4. **Report the change in the conversation.** This is where changes are reviewed, not in the page. In a few lines, say which notes were added or changed and what changed, each with its link from `record`. Do not repeat the whole note.
5. **Recall.** After recording, run `omino recall`. If an idea is due, bring it back in your reply as a question, then run `omino recall --mark-fired <id>` and record. Never treat a recall as adoption.
6. **Re-check.** When requirements or constraints change, run `omino review` and tell the user which conclusions need re-confirming and why. Keep the old records; do not reset them.

## Starting a plan

**Start a plan only when the user asks for one** — they typed `/omino-plan` (`/omino:plan` in the Claude Code plugin), or said something like "keep a plan", "track this", "use Omino". In a git project without a plan, the stop hook tells you, once per project and never again, after a turn that changed the project substantially: then ask the user once, in one sentence, whether to keep a plan here; if they agree, start it (`omino init`, with what they said and the work just done); if not, drop it. If they only describe a project or a goal, or ask you to continue some work ("continue the CSV export") in a folder with no plan, help with that and **ask once** whether to keep a plan; do not start one on your own.

### What a plan is for

A plan is one line of work with one goal — what *the user* is trying to achieve — not a description of the repository. `project.md` (shown as "Goal") answers: what this plan should achieve, its boundaries, and why. Before `init`, settle which case this is (ask in one line if it is not clear):

| Case | The goal is | The repository's own background goes |
|---|---|---|
| The user's own product (one or several repositories) | the product's purpose, principles, boundaries | nowhere special; it is the product |
| One piece of work inside a bigger or team repository | that piece of work: its aim and scope | into "Before Omino" and Sources, as context |
| A fork, or a contribution to an open-source project | what the user wants to change and why, what they will not touch, whether it goes back upstream | upstream's README as a source; upstream's state in "Before Omino" |

Rules of thumb for splitting: **the same goal is the same plan.** Parallel parts (services, repositories, modules, people) are lanes; sequential parts (versions, phases) are stages. Start a separate plan only when the goal differs, the ownership differs (a personal plan does not belong in a team's plan), or the previous plan is finished. A product spread over several repositories is one plan: run `omino link <id>` in each repository, and give each repository its lane with `omino lane "<name>"` (ask the user once for the name; suggest the repository's). The session brief then says which lane the current folder is, and new work items from it go in that lane. A work item that touches several services goes in the lane where most of the change is; link the other parts with `requires`.

Name the plan after what it is for: `omino init --name <id>` with a short lowercase id (`invoice-export`, `todo-app`); without `--name` the id comes from the repository.

**Where the link to the plan is kept.** By default only on this machine (in the repository's `.git`), so `init` changes nothing in the repository. Ask once: "Should the plan be linked in the repository too, so other clones and machines find it?" Only for the user's own repository, and only if they agree, use `--share` (on `init`, `link`, `migrate` or `setup`): it writes `.omino.json`, which they commit. Never share in a team repository they did not say is theirs, or in a fork. After `init`, say where the plan lives (`omino where`).

**New project:** `omino init`, write **only what the user said** about purpose and boundaries into `project.md` (their words; no principles they did not state — put your suggestions under `## Open questions`; delete empty sections). What they said about scope and order goes into stages and work items, not into `project.md`. Record with `--source user`, then tell the user in one or two lines where the plan now lives and what its goal says. No stages until the user arranges work.

In both cases, offer once to add a line to `AGENTS.md` (or `CLAUDE.md`) so every agent finds the plan: "This project keeps its plan with Omino (`omino where`); follow the omino skill when decisions are made or work is finished." Add it only if the user agrees. Ask once: if they do not answer, do not ask again in later turns.

**Existing project** (code, docs or history already exist): `omino init --adopt`. The plan starts *now*; the past is context, not a list of completions.

1. **Draft the intent, flagged.** Read the README and at most five other top-level documents (product, design, contributing, roadmap) — never the whole codebase; deeper docs can wait until a conversation needs them. Draft `project.md` (Purpose, Principles, Boundaries, Sources). Keep its `review` line exactly as one reason — the draft is your inference until the user confirms. Where documents contradict each other, or you cannot tell what the user intends, do not pick a side: add one bullet per question under `## Open questions`.
2. **Summarize the past once.** In `stages/s0.md` ("Before Omino", level 0, closed, `source: agent`) write a few paragraphs on what the project already does, with sources. Do **not** create work items for past features: they have no recorded requirements and cannot be re-checked.
3. **Existing to-dos become ideas, only if the user wants them.** If there is a TODO file, open issues or a roadmap, ask whether to bring them in. Imported items go to `ideas/` with `idea_state: open` and no stage. Arranging them is the user's call.
4. **Record, show, ask.** `omino record "Adopt existing project" --source agent`, then `omino view --open`. In your reply: list the files added; give the drafted intent in three to five lines; ask each open question directly ("README and roadmap disagree on X — which is current?"); ask whether to import existing to-dos. When the user confirms, remove the `review` line, delete answered questions, and record with `--source user`.
5. **Grow on demand.** Add notes only for the parts of the project the conversation actually touches. Do not map the whole repository up front.

## Fixes and work outside the plan

Most turns are bug fixes, tweaks and maintenance nobody planned. Their details — commits, test counts, versions, delivery receipts — belong in git and in your reply, **not in the plan**.

- **Never write progress into `project.md`.** The intent says why the project exists, its principles and boundaries; it is not a log. `check` warns when it holds dated progress entries.
- Record a fix only when it changes the plan (it blocks or reorders planned work, or settles an open question), or when the user asks to record it.
- When the user asks to record such work, make it a work item in a maintenance stage ("Maintenance and fixes", status active). The first time, ask once whether to create that stage; afterwards use it without asking. One work item per fix: what was wrong (Why), what changed (Requirements), how it was verified and what is still unverified (Progress), and its `branch`.

## When the direction changes

Some turns are not a new item or a reordering but a change of strategy: "drop bulk move, dragging is enough", "sync first, categories later". Record these as a **decision** before touching the arrangement:

1. Write `decisions/<id>.md`: `kind: decision`, `date`, `source`, `supersedes` (what it replaces) and `affects` (what may need another look), with sections `Before`, `Now`, `Why`, and `Given up`.
2. Then change the arrangement. Do not delete what was superseded — it stays, marked as replaced, so nobody proposes it again without knowing why it was dropped.
3. `record` flags completed or in-progress items listed in `affects` that you did not change in the same step. Tell the user which ones, with links.

At the start of a session, read the most recent decisions (newest `date` first) before suggesting anything about direction. If the user proposes something a decision already ruled out, say so and point to it; they may still change their mind — then write a new decision.

## The page

Every plan on the machine has a page on the local page service: `http://127.0.0.1:4870/p/<id>` (the brief and `record` print the exact link). The hooks start the service; it keeps running. There the user reads the plan and can:

- **edit a note** (its Markdown, frontmatter included). The change is written and recorded at once as theirs (`source: user`, `via: page`); only that note is in the entry, so your own unrecorded edits stay yours to record. Ids and kinds cannot change there, and an edit that would make the plan invalid is refused.
- **confirm** what waits for them — a draft (`review` line), work you reported done, finished work whose requirements changed. Recorded as theirs right away.
- **comment**: answer an open question, say something is off, decide on a recalled idea, or remark on a note. A comment is a block under the note's `## Comments` heading:

  ```
  ## Comments

  > [!omino] Answer to "Which list first?"
  > Inbox first, then the rest.
  ```

You hear about both with the user's next message (and in the brief). For **changes**, read the notes again before relying on what you knew; if a change affects other notes (a requirement changed under work in progress, a stage moved), update those and record. For **comments**, treat each like a message from the user — the same rules apply: do what it asks in the plan (or answer it in the conversation when it is a question for you), then delete that `> [!omino]` block, and the `## Comments` heading once it is empty, and record with `--source user --said "<their words>"`. Mention in one line what came in and what you changed. A comment you cannot act on yet stays until you can; say why in the conversation.

The page never waits for you: nothing needs to listen. `view.html` in the plan folder (and the page opened from disk) is read-only; when the service runs it links to the editable page. The user can also edit the Markdown files in any editor; `check --fix` records such edits as `source: file`.

## Who confirms what

- **The user decided it** ("add a filter, do it first"): write it, record it, report it. Do not ask "shall I record this?" — they already said so.
- **You drafted it** (an adopted intent, a stage broken into work items, requirements you wrote, an arrangement you proposed): write it with a `review` line, report it with links, and ask the user to check. Work starts only after they say it is fine; then remove the `review` line and record with `--source user`.
- Confirmations, answers and decisions happen in the conversation, or on the page: there a confirmation is recorded at once, and an answer or decision arrives as a comment for you to carry out. Apart from what the user edits or confirms there themselves, the plan is changed only by you.

## Rules that matter

- A question, discussion or "what if" is not a decision. "Should this app have accounts?" changes nothing.
- Listing order is not a dependency. "Do A first" is `before: [b]` on A, never `requires`.
- `requires` means *cannot start until done*. Use it only when that is true and known. No recorded `requires` does **not** mean two items can safely run in parallel; never say it does.
- When the user hands you a piece of work in a project with a plan — a task, a spec to implement, a fix to make — put it in the plan before you start: find its work item (`omino find`) or add one with the user's words as Why and Requirements (`source: user`), in this folder's lane and the stage that fits, mark it `doing`, and record. This is registering, not planning: do not break it down, add stages or propose a design unless the user asks. Then do the work, and update its Progress when done. The prompt hook reminds you once a session. A spec handed to you that says what the *product* must not do ("must not write X") limits the code, not your own use of Omino.
- A new requirement does not imply a new stage. Do not open a stage the user did not ask for. When the user asks for a piece of work and no stage fits, ask once whether to open one for it (suggest a name); until they say, keep the request in your reply, not as a note. Closing a stage does not start the next one.
- An idea the user wants to revisit goes in `ideas/` with a `recall` condition. It joins no stage and carries no commitment.
- The user's latest decision beats an old recall agreement. When they defer or drop an idea, set `idea_state` and run `omino recall --stop <id>` so it is never raised again.
- "I finished it" from you is `status: done, source: agent`. Only a tool result (tests, a check command) can make `status: verified, source: tool`. The user saying it is done is `source: user`.
- If an arrangement conflicts with `project.md` (scope, principles, boundaries), add `review: <reason>` to the note and tell the user. Do not silently delete it and do not keep going.
- When the user confirms that a flagged completion still holds, remove any `review` field and run `omino record "<summary>" --source user --confirm <id>`.
- When something can only be settled by the user — documents disagree, a boundary is unclear — add a bullet under `## Open questions` in the relevant note instead of guessing, and ask. Remove the bullet when answered, and record. `review` shows open questions to the user.
- Keep a `review` line to one short reason. Details belong in the note body.
- Never hand-edit `basis`, `state.json` or `changes.jsonl`; the CLI owns them.

## Writing notes

Notes are Markdown with a strict frontmatter subset (`key: value`, lists as `[a, b]`, nothing nested). Body sections use English `##` headings — `Why`, `Requirements`, `Arrangement`, `Progress`, add others freely — and the user's language for the content. `Requirements` is what completion is checked against: keep it concrete.

```markdown
---
id: filter
kind: work
title: Show open items only
stage: s1
lane: Viewing
order: 1
status: planned
before: [del]
---

## Why
See only what is left for today.

## Requirements
- The list can switch to showing open items only.

## Arrangement
The user wants this before delete. That is a preference, not a dependency.
```

Full field reference: `references/format.md`. Meaning and edge cases: `references/semantics.md`. A worked seven-turn example: `references/examples.md`.

## Commands

| Command | Use it to |
|---|---|
| `omino init [--adopt]` | Start a plan. Creates `project.md` only; `--adopt` also creates a flagged draft intent and a closed "Before Omino" stage for existing projects. |
| `omino record "<summary>" --source user\|agent\|tool\|file [--said "<words>"] [--session id] [--confirm id,id]` | Record every changed note as one entry (with git branch/commit/worktree), stamp completion bases, flag what new decisions affect, refresh the page and print a link to each changed note. |
| `omino check [--fix]` | Validate notes and references; list ideas and decisions linked to nothing. `--fix` records edits a person made directly to the files. |
| `omino find <words>` | Search titles and bodies before creating a note. |
| `omino brief` | The start-of-session summary (the session-start hook prints the same). |
| `omino recall [--mark-fired id] [--stop id]` | List ideas whose condition is met; mark them raised or stopped. |
| `omino review` | List what needs the user: flagged items, changed basis, unconfirmed agent "done", recalled ideas, open questions, items waiting on prerequisites — and the comments the user left for you. |
| `omino view [--out file] [--open]` | Write the read-only `view.html`; `--open` opens the plan's page on the service (starting it), or the file when the service cannot run. |
| `omino service status\|start\|stop\|install\|uninstall` | The page service. `install` also starts it at login (a launchd agent, a Windows Startup script or an XDG autostart entry); run it only when the user says yes to that. |
| `omino where` / `omino projects [--open]` | Print this folder's plan folder / list every plan on this machine (`--open`: an overview page with what waits for the user). |
| `omino setup [--dry-run] [--share]` | One-time setup and upgrades: move or restore an old in-repo plan, link the folder, permissions, hooks, skill copies. Preview with `--dry-run`; run only after the user agrees. |
| `omino migrate [--share]` | Only the move of an in-repo `.omino/` plan (setup does it for you). |
| `omino link <id> [--share]` / `omino lane ["<name>"]` | Use an existing plan from this folder / set or read this folder's lane. `link` needs the user's approval. |
| `omino close [--reopen]` | Mark the plan finished (read-only), or undo that. |
| `omino doctor` | Check Node, the plan's format, git-ignored files, hooks and the AGENTS.md line. Changes nothing. |
| `omino hooks install\|remove\|status [--scope project\|user] [--agent claude\|codex\|gemini\|kimi]` | Add or remove the hooks in an agent's settings, when Omino is not installed as the plugin. Only with the user's consent. |

If a command says the plan uses a newer format, stop changing the plan and tell the user to update Omino.

Exit codes: 0 fine, 1 something needs attention, 2 usage or format error.

## The user's commands

Most of the time the user just talks and you decide, turn by turn, as described above. Six commands let them ask for one move explicitly. Each lives in `commands/<name>.md` next to this file, which says exactly what to do; the names come from falling-block games.

| The user types | Move | What you do | Writes the plan |
|---|---|---|---|
| `/omino-plan` | start | Start a plan, or work on it as a whole: goal, stages, lanes, order | yes |
| `/omino-next` | next queue | Show what can start, what is blocked and on what, what waits for the user | no |
| `/omino-ghost` | ghost piece | Propose where new work goes (stage, lane, prerequisites) as a draft to confirm | a draft |
| `/omino-lock` | lock | Turn what was discussed into a decision: what it replaces, why, what is given up | yes |
| `/omino-hold` | hold | Park an idea with a condition for bringing it back | yes |
| `/omino-clear` | line clear | Wrap up a stage: confirm what is done, settle what needs review, close it | after the user confirms |

They are spelled `/omino-<name>` where the skill was installed with `omino install` (Codex: `$omino-<name>`), and `/omino:<name>` in the Claude Code plugin. A command is the user's explicit request for that move; the rules above still apply (only what the user said is `source: user`, drafts carry a `review` line).

## Talking to the user

Keep plan bookkeeping out of the way. When the plan changed, report it briefly with links ("Plan updated: added *Show open only* (link) to stage 1, before *Delete* (link)."). Say nothing about the plan when nothing changed. Raise recalls and review items plainly, as questions the user can answer. Run `omino view --open` after creating or adopting a plan and whenever the user asks to see it; after a large change, offer it in one line. Do not open it on every turn. When there are open questions or drafts to confirm, you may mention that they can answer or confirm on the page too. If the session brief asks whether the page service should start at login, ask once; run `omino service install` only on a yes.
