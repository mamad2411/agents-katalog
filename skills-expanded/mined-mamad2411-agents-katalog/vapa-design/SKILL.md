---
name: vapa-design
description: Use when handed a VAPA proposal issue URL and asked to design the solution. Gathers context once (issue, VISION.md, existing repo implementation), decomposes the design space into items (data model, API contracts, frontend flows, error handling, migration, permissions), designs each item interactively with the user, and posts every confirmed design as an issue comment.
disable-model-invocation: true
allowed-tools: Bash(git remote get-url origin) Bash(gh issue view *) Bash(gh issue comment *) Read Write Glob Grep AskUserQuestion
---

# /vapa-design

Design the solution for a VAPA proposal issue **interactively with the user**,
and record every confirmed design decision as a comment on the issue.

Pipeline position:

```
Proposal (vapa-proposal) → Design (vapa-design) → Review (vapa-review) → Exec (vapa-exec) → Audit (vapa-audit)
```

Design happens **before review**, so the review committee evaluates not only
whether the problem is worth solving, but whether the solution holds up. The
confirmed design comments become part of the reviewed contract, and `vapa-exec`
later consumes them as "human decisions already made".

Boundary: `vapa-design` produces the **what** — contract-level design (table
structures, API signatures, interaction flows). `vapa-exec` produces the
**how** — implementation steps, file changes, test strategy. Do not drift into
file-level implementation planning here.

The skill writes issue comments and archives them in the per-issue workspace,
but otherwise changes nothing:

- It never edits the issue body, never changes labels, never touches code.
- It never posts a design the user has not explicitly confirmed.
- It never edits an existing design comment — amendments are new comments.

## Workspace

Design artifacts live in the same per-issue workspace that `vapa-exec` later
uses:

```text
.vapa/vapa-exec-<issue-id>/workspace/
  design/
    <slug>-v<n>.md     # archived body of each confirmed design comment
    summary.md          # archived body of the design summary comment
```

Design usually runs before `vapa-exec`, so it may be the workspace's first
writer. Check whether the workspace exists first: reuse it if it does, create
it if it does not. Add only the `design/` subdirectory — `state.json` and all
other artifacts belong to `vapa-exec`; never create or modify them here.

The issue comments remain the canonical record; the local archive keeps the
design traceable in the repo and lets `vapa-exec` quote confirmed designs
without re-fetching every comment.

## Usage

```
/vapa-design 15
/vapa-design https://github.com/insentek/VAPA/issues/15
```

## Requirements

- `gh` CLI installed and authenticated with **comment** access to the target repo.
- Run from inside a git repo, or set `VAPA_REPO=owner/repo`.

## Execution

### Step 1: Detect repository and issue

Run:

```bash
git remote get-url origin
```

Parse `owner/repo`. If detection fails, ask the user to run from a git repo with
a GitHub origin remote, or set `VAPA_REPO=owner/repo`.

Parse the issue reference from the user's argument — a plain number or a full
issue URL both work.

### Step 2: Gather the full context — once

The point of this step is that design never runs on partial information. Fetch
everything before proposing anything:

1. The complete issue: body, all comments, labels, author.

   ```bash
   gh issue view <ref> --repo <owner/repo> --json number,title,state,author,labels,body,comments
   ```

2. **Existing design comments**: scan the comments for `<!-- vapa-design:` markers.
   Items with a `status=confirmed` marker are settled contract — do not redesign
   them unless the user explicitly asks; when several versions of the same item
   exist, the highest `v=` wins. If a local
   `.vapa/vapa-exec-<issue-id>/workspace/design/` archive exists, read it
   alongside the comments.
3. `VISION.md` from the repository root (if present) — the design must align
   with it; contradictions are raised to the user, never silently resolved.
4. A lightweight codebase survey: the modules the proposal plausibly touches,
   how the codebase already solves similar problems, and reusable assets
   (existing tables, endpoints, components, utilities). Design extends existing
   patterns unless the user approves deviating.

### Step 3: Propose the design-item checklist

From the proposal content and the survey, propose a checklist of design items,
trimmed from this taxonomy:

| Category | Examples |
|---|---|
| Data model | new/altered tables, fields, indexes, relationships |
| API contracts | endpoints, request/response shapes, error codes |
| Frontend interaction flows | screens, navigation, interaction states |
| State machines | lifecycle states and transitions of a key entity |
| Error handling | failure modes at system boundaries, user-facing messages |
| Migration & compatibility | data migrations, backward compatibility, rollout |
| Permissions | who can see/do what, auth boundaries |

Not every category applies to every proposal — a docs proposal may need none, a
backend proposal may need three. Present the proposed checklist to the user
(items, with one line each on why it is needed), let them add or remove items,
and only proceed after they confirm the list. Do not silently grow the list
later; newly discovered design needs are proposed to the user explicitly.

### Step 4: Design item by item

For each confirmed checklist item, in order:

1. **Present**: the relevant current state from the survey, the candidate
   options with trade-offs, and a recommendation with reasoning. Keep it
   concrete — real table columns, real endpoint shapes, real flow steps.
2. **Discuss**: answer questions, revise the proposal. Use AskUserQuestion when
   the choice is genuinely the user's.
3. **Confirm**: only when the user explicitly approves, post the design as an
   issue comment in this format:

   ````
   <!-- vapa-design:item=<slug> status=confirmed v=<n> -->

   ## 🎨 设计确认:<item title>

   <the confirmed design, complete and self-contained>

   ---
   > 已否决的替代方案:<rejected alternatives, one line each with reason>
   ````

   Write the comment body in the issue's dominant language; keep the HTML
   marker in English for machine readability. `<slug>` is a stable kebab-case
   identifier per item (e.g. `data-model`, `api-contract`), and `<n>` starts at
   1.

   Archive the comment body as
   `.vapa/vapa-exec-<issue-id>/workspace/design/<slug>-v<n>.md` (create the
   workspace and `design/` directory first if they do not exist), then post it:

   ```bash
   gh issue comment <ref> --repo <owner/repo> --body-file <archived-file>
   ```

   Keep the archived file after posting — it is the local design record, not a
   temp file.

4. Move to the next item.

Amendments: if the user later changes a confirmed item, post a **new** comment
with the same `item` slug and `v=` incremented. Never edit the old comment —
the version trail is the design history.

### Step 5: Post the design summary

When every checklist item is confirmed, post one summary comment:

- the checklist with each item's status and a link to its design comment;
- open questions deliberately left for review or execution;
- a note that review (`vapa-review`) can now evaluate proposal + design together.

Archive the summary body as `design/summary.md` in the workspace before
posting, same as the per-item comments.

## Output handling

- On success, confirmed designs appear as issue comments; report what was posted.
- On failure of a comment post, keep the confirmed design text in the
  conversation so nothing is lost, show the error, and retry only with the
  user's consent.

## Common Mistakes / Red Flags

- Posting a design comment before the user explicitly confirmed it.
- Editing an existing design comment instead of posting a new version.
- Designing from the issue body alone, without reading the comments, VISION.md,
  or the relevant code.
- Redesigning an item that already has a `status=confirmed` marker without the
  user asking for it.
- Drifting into implementation planning (file lists, step ordering) — that is
  `vapa-exec`'s plan, not design.
- Silently resolving a contradiction with VISION.md or with the proposal's
  stated scope — raise it to the user.
- Growing the design-item checklist mid-session without user approval.
- Designing around an existing pattern the codebase already has, instead of
  extending it.
- Writing comment bodies to the `.vapa/` root, a temp directory, or any
  location other than the workspace `design/` archive — or deleting the
  archive after posting.
- Creating `state.json` or other `vapa-exec` artifacts during design; design
  adds only the `design/` subdirectory to the workspace.
