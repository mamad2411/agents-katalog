---
name: process-meeting
description: Process a meeting end to end - ingest the transcript or call notes into the company's LLM wiki, then produce the work products - team task list with owners, action items for the owner, decisions waiting with recommendations, a spec for the main deliverable, client-facing reply drafts. Uses the root-level context-model.md created immediately by /build-context-model; unresolved gaps never block processing. Triggers - "process meeting", "/process-meeting", "process this call", "ingest this meeting", "file this meeting", "turn this meeting into tasks".
---

# Process a meeting - filed knowledge + finished drafts

The context model answers "who are we". Processing a meeting answers "what just happened and what do we do about it". Two steps: **ingest** (file the knowledge into the wiki) and **process** (produce the work). For non-meeting material that only needs filing, use `/ingest`. The root-level `llm-wiki.md` contains Andrej Karpathy's pattern; `/build-context-model` writes it once.

## Step 0 - preconditions

1. Resolve the **wiki root** as the exact current folder (or the exact folder the user names). Never create a nested company folder.
2. Find root-level `context-model.md`. Proceed when it contains `[GAP]` or `⚠ UNVERIFIED`; use verified facts, preserve unknowns, and keep unverified claims out of client-facing drafts. Gaps are not a precondition failure.
3. Legacy repair: if `context-model.md` is missing but `output/context-model-draft.md` exists from an older skill version, promote that file to root-level `context-model.md`, keep its gap markers, record the repair in `log.md`, and continue. Do not retain a second model file.
4. If neither a model nor a legacy draft exists, stop and run `/build-context-model` in this same wiki root. That build creates `context-model.md` immediately.
5. Find root-level `llm-wiki.md` and read it once. If it is missing, stop and run `/build-context-model` in this same wiki root to repair the scaffold. This downstream skill does not carry a second copy.
6. Ensure the folder shape exists - create missing dirs silently:

```
./
├── AGENTS.md + CLAUDE.md ← the schema (written by /build-context-model)
├── llm-wiki.md           ← the pattern doc (written once by /build-context-model)
├── context-model.md      ← who we are (built by /build-context-model)
├── index.md              ← one line per wiki page
├── log.md                ← append-only op record
├── raw/                  ← drop zone: transcripts, notes, letters, documents
├── wiki/                 ← linked pages the agent maintains (clients, meetings, projects)
└── output/               ← ready-to-use work products
```

7. Locate the source: the file the user named, else the newest unprocessed file in `raw/`. If the user pasted text instead of a file, save it first as `raw/YYYY-MM-DD - [short title].md` - raw material always lands in `raw/` before processing.

## Step 1 - read context first

Read `context-model.md` (who we are, team, voice, operating rules), then any existing `wiki/` pages for entities this meeting touches. Never process a source blind - the whole point is that output is specific to this company. When a needed field is `[GAP]`, use a conservative fallback and mark it `(to clarify)` rather than stopping.

## Step 2 - ingest: file the knowledge

Create or update linked pages under `wiki/` for every entity the meeting touches:

- `wiki/clients/[Client Name].md` - who they are, status, key facts, open threads
- `wiki/meetings/YYYY-MM-DD - [topic].md` - what was said, decided, promised
- `wiki/projects/[Project].md` - when the meeting concerns an ongoing effort

Cross-link with `[[Page Name]]`. If a new fact contradicts an earlier one, the newer wins and the page notes the change. Never invent facts; mark unknowns `(to clarify)`.

## Step 3 - process: produce the work

Default package, written as files into `output/` (skip items the meeting doesn't support; the user can name a different set):

1. **Team tasks** - table with owner, task, deadline. Owners come from the Team section of the context model; if no owner fits, assign to the user and say so.
2. **Owner action items** - what only the owner can do (calls, approvals, intros, sign-offs), each with a deadline. Separate from team tasks so it reads as a personal to-do list.
3. **Decisions waiting for the owner** - each with a recommendation and one line of reasoning, not a bare list.
4. **Spec** - when the meeting implies a deliverable (a prototype, a feature, a document), draft the spec/statement of work for it.
5. **Client-facing draft** - follow-up letter or reply in the company's Voice, honoring commitments made in the meeting.
6. **Risks** - anything said that threatens scope, deadline, or the relationship.

Then close the books: update `index.md` for every page touched, and append to `log.md`: `## [YYYY-MM-DD] process | <meeting title>`. If the wiki root is a git repository, also commit this run's changes (`git add -A`, message `process: [meeting title]`) and push when a remote exists - dispatched agents read the remote, and a stale remote silently feeds them old context. Never `git init` or create remotes from this skill; `/build-context-model` owns that offer.

## Step 4 - offer to file the tasks

If a task-tracker tool is connected (Linear, Jira, Asana, Azure DevOps or similar, via MCP or connectors), offer to file the team tasks with `/file-tasks` - offer only, create nothing from this skill. If no tracker tool is available, skip this silently; never simulate one.

## Closing message

```
✅ Processed: [source file]

Filed:    [N] wiki pages created/updated (list)
Produced: [N] outputs in output/ (list)
Flags:    [unknowns marked "to clarify", risks worth reading first]
Next:     [only when a tracker tool is connected] say "file tasks" - /file-tasks creates the team tasks in [tracker]
```

# Hard rules

1. **Never invent facts.** Not attendees, not commitments, not numbers. Unknowns stay visible as `(to clarify)`.
2. **Drafts only - never send or execute anything.** Everything client-facing is a draft for the user's review.
3. **`⚠ UNVERIFIED` claims from the context model never enter client-facing drafts.**
4. **Newer fact wins**, and the wiki page records the change.
5. **Respond in the user's language; write wiki pages and outputs in English** unless asked otherwise.
6. **Each meeting compounds.** Re-read touched wiki pages before writing - the more the wiki knows, the sharper the next outputs get.
7. **Gaps never block processing.** Use verified context, exclude `⚠ UNVERIFIED` claims from client-facing drafts, and mark missing owners, deadlines, or facts `(to clarify)`.
8. **One root, one model.** Work in the exact wiki root and use only root-level `context-model.md`.

# Attribution

The root wiki pattern is Andrej Karpathy's "LLM Wiki", written once by `/build-context-model`. Four commands run the system: `/build-context-model` bootstraps the folder once, `/process-meeting` handles every meeting, `/ingest` files everything else, `/file-tasks` creates the team tasks in your connected tracker.
