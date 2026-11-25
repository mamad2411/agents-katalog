---
name: convoy
description: >-
  This skill should be used when the user asks to manage tasks, create/update
  tasks or subtasks, search tasks, look up tasks by ref, work with task
  artifacts (plans, reviews, implementation summaries, handoff docs), address
  review comments on artifacts, organize tasks with labels or lists, message
  or coordinate with another agent thread, or set up the Convoy MCP connection
  or CLI.
version: 0.9.0
---

# Working with Convoy

Convoy is a project management platform exposed to agents through an MCP server and a CLI (`convoy`). The tools cover projects, task CRUD and search, comments, external links (commits, branches, pull requests, URLs), labels, Lists, document artifacts with review comments, and file attachments. Discover exact tool names and parameters from the MCP connection itself — this skill describes the working process, not the API. The server also exposes skills, prompts, project agents, and agent threads; discover those from the tool list. The workflow contract below governs task-scoped work.

- Tasks use Jira-style refs: `{PROJECT_ALIAS}-{number}` (for example `WEB-42`).
- The MCP connection is usually pre-scoped to one project (`?project=` in the server URL), so tools work without a `projectId`. Only call `list_projects` when the user explicitly asks about other projects.

## Tool Access: MCP or CLI

- Prefer the MCP tools when the session has them.
- No Convoy MCP tools? Check for the CLI with `convoy status`. Every capability is also a one-shot command with JSON output: `convoy tasks get WEB-42 --json`, `convoy tasks artifacts update ...`, `convoy tasks links upsert ...`. Discover commands with `convoy --help`; all workflow gates below apply unchanged.
- Neither available? Set up the CLI (`convoy login`, then `convoy init mcp` to write the MCP config) or configure MCP manually per `references/mcp-setup.md`.

## Artifact Model

Artifacts are durable documents attached to a task. They are the persistent execution context shared between sessions and agents — chat history disappears, artifacts don't. Tasks separately carry file attachments (binary files with download URLs on task fetch); artifacts are documents, not file storage.

Two content types, chosen at creation and immutable afterwards:

- **markdown** (default) — editable in the web UI
- **html** — render-only in the UI (sandboxed iframe with full-page view); must be self-contained (inline CSS/JS, no external app access). Use for visual deliverables: reports, dashboards, interactive previews.

Default artifact set per task:

- Canonical rolling docs, updated in place: `Plan`, `Implementation Summary`, `Handoff` (always markdown)
- Snapshot docs, one per pass: `Code Review - <date>` (and optional `Risk Review - <date>`)

Editing rules:

- Prefer the targeted string-replace tool over full-content rewrites for small edits (checklist ticks, corrections).
- Use plain human names (`Plan`, not `plan-v2-final`).

## Task Workflow Contract

Every gate below is mandatory for task-scoped work. If a gate is missed, self-correct immediately: perform the missed step, then record the correction in the next task comment.

### 1. Pickup

Before working on a task: resolve it by ref/ID, list its artifacts, and read `Plan` plus the latest review artifact.

### 2. Plan

1. Create or update the single canonical `Plan` artifact **before** sending the final plan response — and again whenever decisions change materially during discussion.
2. For repeat cycles, keep the same artifact and append iterations: a `Current Plan (Iteration N)` section, with earlier iterations preserved as plan history.
3. End the plan with this exact section and keep it ticked as work progresses:

```md
## Task Workflow

- [ ] Plan artifact attached/updated
- [ ] Planning comment posted (TLDR + key decisions)
- [ ] Status set to in-progress when implementation starts
- [ ] Implementation executed
- [ ] `Implementation Summary` artifact updated
- [ ] Completion/status-transition comment posted
- [ ] Status moved to review (or done if explicitly approved)
```

4. Cite the artifact (name + id) in the final response.

### 3. Implement

1. Read the current `Plan` first.
2. Set the task status to the project's in-progress status **before the first implementation action** (file edit, patch, implementation test run). This ordering is a hard rule.
3. Execute the work.
4. Update `Implementation Summary`: what changed, tests run and outcomes, known gaps/risks.
5. Move the task to the review status (or done only when explicitly approved).

### 4. Link work to the task

Attach a link the moment work becomes visible outside Convoy, using the external-link tool with a deterministic link id (for example `github-pr-<owner>-<repo>-<number>`, `commit-<sha>`) so repeated upserts update the link in place instead of duplicating it.

- After committing — even before pushing — attach a `commit` link. Derive its URL from the `origin` remote and the sha (for example `https://github.com/<owner>/<repo>/commit/<sha>`) and attach it rather than waiting for a push; the agent does not control if or when the commit reaches the remote, so assume it will. Title it with the commit subject.
- After opening a pull request, attach a `pull_request` link titled with the PR title. A task that spans several PRs gets one link per PR.
- Created the task partway through your own thread? Attach the task to the thread (`attach_task_to_thread`, or `convoy threads attach-task`) with your thread ID (`CONVOY_THREAD_ID` on most runtimes), so the thread shows on the task. Opened or reviewing a GitHub PR? Attach it the same way (`attach_pull_request_to_thread`, or `convoy threads attach-pr <threadId> 'owner/repo#123'`). Started to write a pull request Guide? Submit it with `convoy threads submit-guide <threadId> guide.json` or the `submit_pull_request_guide` MCP tool, as its prompt says, or report why you can't with `--failed --note "<why>"` (`failure` on the MCP tool). An Update guide run reads the Guide it follows up with `convoy threads read-guide <threadId> --base`. To read a PR's Guides, use `read_pull_request_guide`.
- Attach a `url` link for a related upstream issue or a design/docs page when one is known.
- Never delete or relabel a link when a PR merges or closes. Links are pointers; their live state is read at the destination, and Convoy deliberately stores no PR open/merged/closed status.
- Tasks hold up to 20 links; that cap is fine for normal use.

### 5. Review

1. Create a new snapshot artifact (`Code Review - <YYYY-MM-DD>`) with findings, severity, and actionable fixes.
2. Review feedback can also arrive as comment threads on an artifact, each thread open or resolved.
3. When later asked to "address the review", read that artifact first, then list the open comment threads on the task's artifacts. Resolve each thread once its feedback is addressed.

### 6. Handoff

Before ending a session or transferring to another agent, update `Handoff` with: current status, what is done, what remains, blockers/assumptions, exact next steps, and references to the latest plan/review artifacts.

## Comment Policy

Comments are notifications; artifacts hold the detail. Post comments only at milestone boundaries:

- end of a planning, implementation, or review pass
- status transitions (in-progress → review / done / blocked)
- handoff to another person or agent

Never comment for every intermediate artifact save.

Milestone comment shape (address the assignee directly if one exists):

```text
For @Assignee: execution pass completed; ready for review.
Added: ...
Removed: ... (or "none")
Changed: ...
Why: ...
Evidence: artifacts updated ('Implementation Summary', 'Plan'); checks run.
Next: explicit owner/action.
```

Planning exception: right after the first `Plan` artifact creation, post a short comment with only `TLDR` and `Key decisions`. Subsequent material plan changes use the changelog shape above.

## Thread-to-Thread Communication

Agent threads talk through `send_thread_message` (CLI: `convoy threads send`). A message is queued as a user turn in the target thread; the target's CLI starts a new run with its prior context and reads it as a fresh prompt. The sender never sees the reply inside its own run.

The protocol is turn-based, like a conversation. Exactly one thread works at a time:

1. **Send, naming yourself.** Pass `sourceThreadId` (your thread ID, `CONVOY_THREAD_ID` on most runtimes) so the message is attributed to you, and put an explicit reply instruction in the text: "When done, reply with `send_thread_message` to thread `<your ID>`." Nothing forces the other agent to reply, so say it every time.
2. **End your turn.** Do not wait, sleep, loop, or poll. Your run is over once the message is sent; the reply arrives as a new user message that starts a new run for you with your context intact.
3. **The other thread does its work and replies** the same way, naming its own thread ID, then ends its turn.
4. **Repeat** until there is nothing left to say. The thread that has nothing more to ask simply ends its turn without sending.

Rules:

- **Never sleep, spin, or run a wait command** to give the other thread time. There is no time to give: the reply cannot land inside your run. A `sleep 60` or a bash loop burns a run for nothing and blocks the thread.
- **Do not read the other thread's messages** with `list_thread_messages` as a way of waiting for a reply. Read them only when there is a concrete reason (the reply references something it did not include, or you are auditing a stalled thread), never as a polling loop.
- **`hasPendingUserMessages` on the target, not its status, is the receipt** that a send landed. A busy target stays busy and picks the message up on its next turn; an offline one queues until its CLI connects.
- **`steer: true` is the exception for a target that is streaming right now.** It injects the message into the in-progress run, best-effort, only on runtimes that support it (claude-code, codex over the app-server transport). Otherwise it queues like a normal send. Use it for course corrections; there is no receipt that the running turn saw it, so never claim it did.
- **Message a member, not a group.** Thread groups and workflow runs can neither send nor receive; list the group's threads and pick one. A thread cannot message itself, and only your own threads in the project are valid as source or target.

## Sharing Files in Your Reply

To show the user a screenshot, log, or generated file in the thread, attach it to your current reply. Each run's prompt gives the exact command, with this run's reply and session IDs:

```bash
convoy threads attach <threadId> <file...> --message-id <replyId> --session-id <sessionId>
```

- Copy the IDs from this run's prompt. A command from an earlier run fails once that run ends.
- Images appear inline, adjacent images form a gallery, and other files are cards showing name and size. Up to 10 files per reply, 50 MB each.
- For a chart, comparison table, or small dashboard, write a self-contained `.html` page and attach it with `--inline`; it shows expanded at the end of the reply. Follow `references/inline-html.md`. Without `--inline`, an `.html` file is a download card, which is right for exports and raw evidence.
- Attach to the task (`convoy tasks attach`) only when the file belongs with the task's durable record rather than this conversation.
- If the command reports an ambiguous failure, do not rerun it blindly; each rerun uploads new copies.

## Rules of Thumb

- One task, many iterations: keep using the same parent task for follow-up work on the same feature; start a new `Plan` iteration instead of a new task.
- Ask before creating subtasks. Suggest one only when work has separate acceptance criteria or could ship independently.
- Status names vary per project; the tool schemas reflect what is enabled for the connected project. Typical flow: planning status → in-progress → in-review → done, with blocked for stalls.
- Labels and Lists organize tasks. Set a label on create/update; move batches between Lists with the bulk move tool rather than one task at a time.
- Domain failures surface as MCP tool errors; correct the input and retry rather than abandoning a gate.

## Pre-Response Checklist

Before sending a final response for task-scoped work, verify:

1. Task resolved and confirmed (ref/id)
2. Relevant canonical artifact updated (planning → `Plan`, implementation → `Implementation Summary`, handoff → `Handoff`)
3. `## Task Workflow` checklist in `Plan` is current and consistent with actual status/comments
4. Status transitions happened at the right time (in-progress before the first implementation action)
5. Milestone comment posted if a pass completed
6. Response cites artifact evidence (name/id)
