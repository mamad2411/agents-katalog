---
name: dev-task-loop
description: >
  Use when the user wants to process a backlog of dev tickets end-to-end with a known project / branch / merge target / task tracker / design reference workflow, but without committing to any specific platform (Jira / Linear / GitHub Issues / Notion / Figma / Zeplin / etc.). Trigger on requests like 「幫我跑任務」、「照我的流程把 backlog 做完」、「review failed 的全部處理掉」、「用我那套開發流程做事」、"work through my task list", "run my dev loop", "process my tickets end-to-end". Always asks the user up-front for project root, working branch, merge target, task list location, design reference location, and how to mark a task done — then loops through tickets implementing → verifying → committing → opening PR → merging → syncing → updating the tracker. Never bake in platform-specific API calls; figure those out at run time from the user's answers.
---

# Dev Task Loop

A general-purpose loop for working through a dev backlog. The skill is intentionally platform-agnostic — it commits to **a workflow**, not to any specific tracker / VCS host / design tool.

---

## Core principle

**Ask first, then loop.** Six upfront questions establish the working context. After that, run a tight per-ticket loop until the user stops you or the backlog is empty.

Do not assume Jira, GitHub, Figma, or any other vendor unless the user names them in their answers.

---

## Phase 0 — Establish workflow context

Before doing anything, call `AskUserQuestion` with all six questions in **one** call. Do not start work until all are answered.

The six questions (Traditional Chinese — translate if the user is writing in English):

1. **哪個專案？** — root path or repo identifier. Example answers: `/Users/me/Documents/myapp`, `org/repo`, "monorepo, packages/web".
2. **在哪個分支開發？** — working branch (where new commits land). Example: `tim`, `dev`, `feature/foo`.
3. **開發完合併到哪？** — merge target. Example: `main`, `develop`, `release/v2`.
4. **任務清單在哪？** — where the backlog lives + how to filter for "ready to work". Example: "Jira project HTLIFE, status = Review Failed, assignee = me", "GitHub issues label:bug", "Notion DB X filter Y", "this markdown file at TODO.md".
5. **示意圖／設計在哪？** — design reference, or "no design needed". Example: "Figma file URL", "screenshots in /docs/mocks/", "no design — text spec only".
6. **完成後任務頁面要怎麼操作？** — definition-of-done actions on the task page. Example: "comment 已修正 @reviewer, set status to 審核中", "close the issue, leave PR link", "tick the checkbox in the markdown file".

For each option list in `AskUserQuestion`, include the most likely choices the user has named in past sessions plus a free-text fallback (the harness adds "Other" automatically).

Store the six answers as the **workflow contract** for the rest of the session. Re-read them mentally before every phase.

---

## Phase 1 — Pull the backlog

Using the answer to question 4, fetch the list of tickets that match the user's "ready to work" filter.

How you do this depends on what they named:

| Tracker style | Approach |
|---|---|
| REST API with session cookie (Jira Cloud, Linear, Asana, etc.) | Navigate to the tracker once in the browser MCP, then call its REST endpoints via `javascript_tool` against the open tab — the session cookie carries auth. |
| GitHub / GitLab | Try the platform CLI (`gh issue list`, `glab issue list`) first; fall back to web automation if missing. |
| Markdown / Google Doc / Notion table | Read the file or the URL; parse the rows that match the filter. |
| User-named ad hoc list | Read whatever they pointed you at. |

Cache the result as a list of task IDs + one-line summaries. Show the list to the user and ask which one to start with (or "from the top").

---

## Phase 2 — Per-ticket loop

For each ticket, run these steps in order. **Do not skip verification.**

**Browser is the default lens.** Open the task page in the browser to read it (so you see screenshots / inline images QA attached), and open the affected route in the browser to verify the fix. Source-level inspection and TypeScript checks are supporting evidence, not replacements.

### 2.1 Read the task

- **Open the task page in the browser** (Chrome MCP / browser automation). Don't rely on a REST-only fetch alone — QA usually attaches screenshots, recordings, or inline images that only render in the web UI, and you'll miss them if you only call the API.
- Once the page is open you can still call the tracker's REST endpoints via `javascript_tool` against that tab to pull the description text cleanly.
- If the tracker supports "struck-through" / "resolved" formatting (e.g. Jira ADF `strike` mark), filter those out — they represent already-handled items.
- Scroll through any attachments. If QA included a screenshot of the broken UI, read it.
- Quote the actionable items back to the user (in your own words, short).

### 2.2 Reference the design

- If question 5 names a design source, open it before coding.
- If the design is a Figma frame or screenshot, look at it directly — do not implement from memory of similar pages.
- If the design is ambiguous, ask the user before guessing.

### 2.3 Confirm working branch

```bash
git -C <project> status
git -C <project> branch --show-current
```

Make sure you're on the working branch from question 2. If `git status` shows uncommitted leftovers from a previous task, surface them and ask before continuing.

### 2.4 Implement

- Search for the relevant files. Reuse existing components / patterns instead of inventing new ones.
- Make the minimum edit that fixes the described problem. Do not "drive-by refactor" unrelated code.
- Match the project's existing style: indent, import order, file layout, naming.

### 2.5 Verify

**UI changes MUST be verified in a real browser before moving on. Type-check passing is not enough — pixels lie.**

Run the verification appropriate to what changed:

- **UI change (any visible HTML/CSS/component edit)** — **mandatory browser check**:
  - Use the Preview MCP if a dev server is already running, or the Chrome MCP against the deployed environment the user named.
  - **Navigate to the actual affected route**, not just the homepage.
  - Verify the change is visible: layout, colors, spacing, copy, interactive states (hover, focus, disabled).
  - For mobile-specific tickets: resize the preview to `mobile` preset (375×812) and re-check.
  - For per-tenant / per-company / per-role behavior: ideally log in as the affected role; at minimum verify the route doesn't error.
  - If you can't open a browser session (no preview running, no logged-in tab), **stop and tell the user** — don't guess "looks fine from the source."
- **TypeScript / build signal**: `pnpm tsc --noEmit` (or `tsc`, `npx tsc`) in the relevant package. Ignore pre-existing baseline errors; flag only new ones. This is *necessary but not sufficient* for UI work.
- **Unit / integration tests**: run the test command from `package.json` / `pyproject.toml` / etc. if the project has them for the touched module.
- **Backend-only change**: `curl` / `httpie` against the local API if running, otherwise rely on type + test signal.

### 2.6 Commit

```bash
git -C <project> add <specific files only>
git -C <project> commit -m "$(cat <<'EOF'
<type>(<scope>): <short subject> (<TICKET-ID>)

Why: <one or two sentences on the problem>
Fix: <one or two sentences on the change>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
git -C <project> push origin <working-branch>
```

Never `git add -A` / `git add .` — stage by path so secrets and stray files don't sneak in.

### 2.7 Open a PR / merge request

Use whatever VCS host the project lives on:

- GitHub: `gh pr create` if installed; otherwise navigate to `https://github.com/<repo>/compare/<merge-target>...<working-branch>?expand=1` in the browser MCP and submit the form.
- GitLab: `glab mr create` or the equivalent web form.
- Bitbucket / Gitea / self-hosted: web automation.

Title = the commit subject. Body = the commit body verbatim.

### 2.8 Merge

The user's earlier sessions almost always include "merge it" — confirm once per session, then proceed without re-asking each ticket. If the user has said CI red is OK, don't block on red checks; merge anyway.

Merge strategy: prefer a real merge commit (`--no-ff`) so the PR shows up in the graph. Locally:

```bash
git -C <project> fetch origin
git -C <project> checkout <merge-target>
git -C <project> pull origin <merge-target>
git -C <project> merge --no-ff <working-branch> -m "Merge pull request #<n> from <fork>/<working-branch>"
git -C <project> push origin <merge-target>
```

### 2.9 Sync the working branch

```bash
git -C <project> checkout <working-branch>
git -C <project> rebase <merge-target>
git -C <project> push origin <working-branch> --force-with-lease
```

Use `--force-with-lease`, never raw `--force`.

### 2.10 Mark the task done

**Open the task page in the browser first**, then run the actions the user named in question 6. Common patterns:

- **Tracker REST API** (Jira Cloud, Linear, etc.): once the tracker tab is open, you can POST via `javascript_tool` against it — the session cookie carries auth. After the API calls, eyeball the page to confirm the comment is visible and the status badge changed.
- **Web UI only** (no REST or no API access): click the comment box, type the message (including any @mention), submit; then open the status dropdown and pick the target state. Take a screenshot or read the page back to confirm.
- **Markdown checklist / Notion table**: edit the file or row, commit (for markdown) or save (for Notion). For markdown, ship the doc edit in a separate small commit.

Confirm with the user: "Comment posted, status moved to X — next ticket?"

---

## Phase 3 — Between tickets

After each ticket, summarise in **two lines**:

- One line about what shipped (file count + change essence).
- One line about tracker state ("HTLIFE-X 已留言 + 審核中").

Then ask the user which ticket to take next, or "從下一張開始" if they want auto-pace.

---

## Recovery / safety rules

- **Browser verification is not optional for UI tickets.** If you can't open a browser to inspect, escalate before continuing.
- **Stop and report** if `git status` shows unexpected files you didn't author — never blindly stash or reset.
- **Never** modify `.env*` files or anything outside the project root the user named in question 1.
- **Never** push with `--force` (use `--force-with-lease`).
- **Never** skip hooks (`--no-verify` / `--no-gpg-sign`) unless the user explicitly says so.
- **If a fix attempt fails twice**, stop and re-read the task description out loud to the user — you may have misunderstood the requirement. Re-open the ticket in the browser and look at the attached screenshots again.
- **Pre-existing baseline errors** in test files / unrelated modules are not yours to fix during a ticket loop. Note them and move on.

---

## Skill stops when

- The user says stop / 停 / 夠了.
- The backlog filter returns zero items.
- You've made 3 ticket-completing rounds without user input and want to confirm pace.

When stopping, output:

- How many tickets shipped this session.
- Which tickets remain (with the user's filter applied).
- Anything that needs the user's attention (e.g. CI red on Azure, design ambiguity left unresolved, a ticket that's blocked on someone else).
