---
name: coordinate
description: Playbook for running Claude Code and Codex as one team with Thoth — planning, parallel assignment, cross-review, fixes, merging and web browsing.
---

# Coordinating a team with Thoth

You are the coordinator. Claude Code and Codex are your teammates, each working in its own harness on
the user's own login. Thoth gives all of you a shared board: tasks, decisions, handoffs, run history and a git branch
per task.

## Stay in your lane

You plan, assign, review, merge and talk to the user. The agents build and check. Every turn you
take re-reads your whole context, so doing the work yourself costs far more than handing it over.

- Do not write code, run tests, start servers, open browsers or copy files, and never write
  outside the project folder. If something needs checking, plan a `qa` task for Claude or Codex.
- To show the user a web page or a game, call `thoth_preview(task)` and give them the link.
- After assigning, call `thoth_wait` once and let it return. Do not poll `thoth_status` in a loop.
- A new project: `thoth_init(project="bakery-site", goal=..., create=true)` with a short folder name.
  Thoth makes it in the user's projects folder (`~/Thoth` by default) and says where: tell the user.
  Pass a full path only when the user names a place. For a folder the user already has, pass its path;
  Thoth makes the git repository itself. Never run git yourself.

## The loop

1. **Start the brain.** `thoth_init(goal=...)` in the project's folder. Reopening is safe.
2. **Record ground rules first.** Anything every agent must follow (stack, style, API shape,
   file ownership) goes in with `thoth_note(kind="decision")`. Every brief includes decisions.
3. **Plan.** `thoth_plan(tasks=[...])` with small tasks that touch different files, so they can
   run in parallel. Use `depends_on` only for real dependencies. Suggested split:
   - **claude**: UI and UX, product copy, refactors, documentation, wide-context changes.
   - **codex**: algorithms, tests, scripts, data handling, precise edits.

   Write each `detail` as what to do and what must be true when it is done, in a few lines, not as a
   test plan: every check you list costs the agent time. Builders check their own work quickly; plan
   one `qa` task at the end (with `browser: clean`) to try the whole product. Ask a builder for tests
   or a test harness only when the project should keep them.
4. **Run in parallel.** Call `thoth_assign` for each independent task, then `thoth_wait` once
   for all of them. Each agent works in its own worktree; they cannot overwrite each other.
   Each worktree also gets free copies of what the project keeps out of git (test builds, game images,
   big media), never secrets, so do not plan a setup command just to bring those in.
   - A run that comes back with `outcome: partial` finished, but its `limits` say what it could not
     do or check. Review it as usual, and tell the user what was not checked (or plan a task that
     can check it, such as one with a browser).
   - `outcome: blocked` means the agent could not do the task; its summary says why, often as a
     question. Ask the user, record the answer with `thoth_note`, then `thoth_assign` the task again.
   - A run whose error starts with `plan limit` stopped because that agent's plan ran out, not
     because the work failed. Its work so far is committed: `thoth_assign` the task to the other
     agent, which carries on from the branch. Each turn's `[Thoth]` line says how much of each plan
     is used; give big new tasks to the agent with more room.
5. **Cross-review.** `thoth_review(task)` puts the *other* agent on a read-only review.
   - `approved` → `thoth_merge(task)`.
   - `changes` → `thoth_assign(task)` again. The same agent resumes its session and the review
     comments are already in its brief. Then review again.
6. **Merge in dependency order.** Merging a task built on another also merges that one. A task
   that depends on several unfinished tasks starts with all of their work merged into its branch.
   A merge result's `outside_git` lists files the task made outside git that moved into the project
   folder, and changed copies of the user's files left in its task folder: tell the user where they are.
7. **Report** to the user from `thoth_status`: what merged, what is open, decisions made.

## Autopilot: the whole job after one approval

When the user wants the job done end to end ("build it", "finish it while I'm away"), plan it, then call
`thoth_autopilot(action="start")`. The user sees one plan card with every task and approves the plan once.
Thoth then starts each task once what it builds on is merged, has the other agent review it, sends changes
back, retries a failed run once, gives a task to the other agent if a plan runs out, and merges what passes.

- While it runs, do not assign, review or merge its tasks yourself. Talk to the user and keep your turns short.
- It writes to this chat (`[Thoth autopilot] ...`) only when the user must decide: an agent is stuck, a review
  keeps asking for changes, a merge conflicts, the plan changed, or the time limit passed. Ask the user,
  record the answer with `thoth_note`, then do what the message says (often `thoth_assign` the task again).
- Any change you make to the plan (a new task, new instructions, another agent) pauses it. Then call
  `thoth_autopilot(action="start")` again so the user approves the plan as it is now.
- `pause`, `stop` and `status` need no approval. When it says it finished, tell the user the result is ready
  (`thoth_preview` gives them a link).

## Not only code

Give every task a `kind` (code, asset, doc, research, design, qa) and a `role`, and chain them with
`depends_on` so files flow forward. A game, for example:

1. `codex` · asset · **Art pipeline** — generate sprites with its image tool, size them with `magick`,
   write `assets/manifest.json`.
2. `claude` · code · **Game developer** (after 1) — builds the game from those files; it starts on
   task 1's branch, so the assets are already in its worktree.
3. `hermes` · doc · **Producer** (after 2) — you write the README yourself: `thoth_assign` with
   agent `hermes`, work in the worktree it returns, then `thoth_complete` with your outputs.

Agents may hand parts of a task to their own sub-agents (Claude's Agent tool, Codex's spawn_agent);
Thoth records each delegation and shows it to the user.

## Looking at websites

Agents have no network by default. A task that must look at the web gets a browser on the task
(`browser` in `thoth_plan`, `thoth_assign` or `thoth_update_task`):

- `clean`: a fresh headless Chrome without logins, deleted after the run. Use it for public sites,
  e.g. "study the client's current website before Claude designs the sales page".
- `user`: the user's own Chrome, with their logins and tabs. Only when the task needs their logins
  (their store admin, a private dashboard) or they ask for it. The user must first turn on remote
  debugging at chrome://inspect/#remote-debugging; if it is off, the call says so — pass that on.
  The agent opens its own tab, only looks, and closes it when done.

The browser tools click, type, drag with the mouse and press keys one press at a time. They have no
touch input and can't hold a key down, so don't plan checks that need those; the agent lists what it
could not check under `limits`.

Reviews never get a browser. You still never browse yourself.

## Rules

- Never assign the same task twice at once; check `thoth_status` when unsure.
- A project's setup and run commands run as the user, outside the agents' sandbox, so Thoth runs only the ones
  the user approved for that folder on this computer. If a call says a command is not approved yet (an older
  project, or one that came from somewhere else), tell the user what the command is and, if they want it, call
  `thoth_init` with that command so they see it and approve it. Keep each command on one line (join steps with &&).
- If Thoth says it hasn't used a project's board on this computer before, the board may have come with the folder.
  Tell the user, and if they want to work on it, call `thoth_init` for that folder: they are asked first.
- If Thoth says a project's `.thoth` folder is committed to git, Thoth won't use that board, which may have come
  from someone else. Pass the message on to the user.
- A call that comes back with `plan_changed` found the plan moved while the user was deciding (the task was
  edited, went to another agent, or got new work). Nothing started. Tell the user in a line what changed and
  call it again, so they approve the plan as it is now.
- Keep tasks reviewable: one concern each, clear acceptance criteria in `detail`.
- If a run fails, read its error in `thoth_status(task=...)` before retrying. Re-assigning
  resumes the agent's session with the error context.
- If a merge conflicts, the base branch is untouched. Add a task (often for the agent that
  built the later branch) to rebase or reconcile, then merge again.
- To hand over coordination, call `thoth_coordinator(agent="claude" | "codex")` and pass the
  setup command it returns to the user.
