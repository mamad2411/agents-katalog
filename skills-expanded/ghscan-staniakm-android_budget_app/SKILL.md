# Trello Agent Skill

## Goal

This skill defines how an AI agent should operate a Trello board for the `InternetApi` project.

## Agent Responsibilities

The agent may:
- create cards from technical tasks,
- update descriptions and checklists,
- move cards across workflow lists,
- add status comments,
- mark tasks as done when acceptance criteria are met.

The agent must not:
- delete cards without explicit instruction,
- close/archive the board,
- change board member permissions.

## Required Configuration

Before working, the agent must have access to:
- `TRELLO_API_KEY`
- `TRELLO_TOKEN`
- `TRELLO_BOARD_ID`

Optional:
- `TRELLO_DEFAULT_LABEL_TECH_DEBT`
- `TRELLO_DEFAULT_LABEL_BUG`
- `TRELLO_DEFAULT_LABEL_FEATURE`

## Board Workflow

Current board (`Projekty`) lists used by this project:
1. `TODO`
2. `IN PROGRESS`
3. `TESTING`
4. `DONE`

Transition rules for current board:
- new card goes to `TODO`,
- work started: move `TODO -> IN PROGRESS`,
- implemented and ready for validation: move `IN PROGRESS -> TESTING`,
- accepted: move `TESTING -> DONE`.

Canonical workflow:
- `TODO -> IN PROGRESS -> TESTING -> DONE`.

## Task Card Format

### Title

`[PRIORITY] Short verb + object`

Example:
- `[P1] Clean up Gradle dependencies`

### Description

Each card description should include:
1. `Goal`
2. `Scope`
3. `Implementation Steps`
4. `Acceptance Criteria`
5. `Risks`

### Checklist

Checklist must map 1:1 to implementation steps.

Example:
- [ ] Inventory duplicate dependencies
- [ ] Remove duplicates
- [ ] Run compile
- [ ] Update progress documentation

## Status Comment Standard

Comment format:

`STATUS: <IN_PROGRESS|BLOCKED|DONE> | TASK: <id/name> | NEXT: <next step>`

Example:

`STATUS: IN_PROGRESS | TASK: TASK-01 | NEXT: remove unused navigation dependencies`

## Status Update Rules

After each meaningful change, the agent should:
1. update checklist item states,
2. add a status comment,
3. move the card according to current board flow (`TODO`/`TESTING`/`DONE` if available).

## Definition of DONE

A card is `DONE` when:
- all checklist items are complete,
- acceptance criteria are satisfied,
- required build/tests passed,
- final status comment is added.

## Final Comment Template

`STATUS: DONE | TASK: <id/name> | RESULT: <1-2 sentences> | VERIFY: <command or verification method>`

## Minimal API Operation Set (Reference)

The agent should support:
- create card,
- list cards from list,
- update card description,
- add checklist and checklist items,
- mark checklist item complete,
- move card across lists,
- add card comment.

## Example Trello REST API Operations

These examples assume Trello REST API v1.

### 1) Get board lists

```bash
curl "https://api.trello.com/1/boards/{boardId}/lists?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
```

Purpose: read list IDs for `TODO`, `IN PROGRESS`, `TESTING`, and `DONE`.

### 2) Create a card

```bash
curl --request POST \
  --url "https://api.trello.com/1/cards" \
  --data-urlencode "key=${TRELLO_API_KEY}" \
  --data-urlencode "token=${TRELLO_TOKEN}" \
  --data-urlencode "idList=<TODO_LIST_ID>" \
  --data-urlencode "name=[P1] Clean up Gradle dependencies" \
  --data-urlencode "desc=Goal:\n...\n\nScope:\n...\n\nAcceptance Criteria:\n..."
```

### 3) Add checklist to card

```bash
curl --request POST \
  --url "https://api.trello.com/1/checklists" \
  --data-urlencode "key=${TRELLO_API_KEY}" \
  --data-urlencode "token=${TRELLO_TOKEN}" \
  --data-urlencode "idCard=<CARD_ID>" \
  --data-urlencode "name=Implementation"
```

### 4) Add checklist item

```bash
curl --request POST \
  --url "https://api.trello.com/1/checklists/<CHECKLIST_ID>/checkItems" \
  --data-urlencode "key=${TRELLO_API_KEY}" \
  --data-urlencode "token=${TRELLO_TOKEN}" \
  --data-urlencode "name=Run :app:compileDebugKotlin"
```

### 5) Mark checklist item done

```bash
curl --request PUT \
  --url "https://api.trello.com/1/cards/<CARD_ID>/checkItem/<CHECKITEM_ID>?key=${TRELLO_API_KEY}&token=${TRELLO_TOKEN}&state=complete"
```

### 6) Add status comment

```bash
curl --request POST \
  --url "https://api.trello.com/1/cards/<CARD_ID>/actions/comments" \
  --data-urlencode "key=${TRELLO_API_KEY}" \
  --data-urlencode "token=${TRELLO_TOKEN}" \
  --data-urlencode "text=STATUS: IN_PROGRESS | TASK: TASK-01 | NEXT: run compile"
```

### 7) Move card across lists

```bash
curl --request PUT \
  --url "https://api.trello.com/1/cards/<CARD_ID>" \
  --data-urlencode "key=${TRELLO_API_KEY}" \
  --data-urlencode "token=${TRELLO_TOKEN}" \
  --data-urlencode "idList=<TESTING_LIST_ID>"
```

## Agent Setup (Step by Step)

### Step 1: Generate Trello credentials

1. Open Trello developer page and create an `API Key`.
2. Generate a `Token` with read/write permissions for cards.
3. Get the target `Board ID`.

### Step 2: Set environment variables

PowerShell example:

```powershell
$env:TRELLO_API_KEY="<your_api_key>"
$env:TRELLO_TOKEN="<your_token>"
$env:TRELLO_BOARD_ID="<your_board_id>"
```

Bash example:

```bash
export TRELLO_API_KEY="<your_api_key>"
export TRELLO_TOKEN="<your_token>"
export TRELLO_BOARD_ID="<your_board_id>"
```

### Step 3: Verify access

```bash
curl "https://api.trello.com/1/members/me?key=${TRELLO_API_KEY}&token=${TRELLO_TOKEN}"
```

If response includes member data, setup is valid.

### Step 4: Validate workflow lists

Ensure the board contains:
- `TODO`
- `IN PROGRESS`
- `TESTING`
- `DONE`

## How to Use This Skill in Practice

### Scenario A: Create cards from task document

1. Agent reads `docs/AI_IMPLEMENTATION_TASKS.md`.
2. Agent creates one card per `TASK-*` in `TODO`.
3. Agent copies `Goal`, `Scope`, `Steps`, `Acceptance Criteria`, `Risks` into description.
4. Agent adds checklist with a 1:1 mapping to implementation steps.

### Scenario B: Update status after each iteration

After each implementation iteration, the agent:
1. checks completed checklist items,
2. posts a `STATUS: ...` comment,
3. moves card according to workflow if criteria are met.

### Scenario C: Close task

1. Agent verifies all checklist items are complete.
2. Agent posts final `STATUS: DONE ...` comment with verification command.
3. Agent moves card to `DONE`.

## Quick Prompt for the Agent

Use this command to force skill-based behavior:

```text
Use guidelines from docs/TRELLO_AGENT_SKILL.md. Read tasks from docs/AI_IMPLEMENTATION_TASKS.md, create/update Trello cards, add checklists, and update status after every implementation step.
```

## Practical Notes

- Do not duplicate cards for the same task.
- One technical task = one card.
- If a task is large, create sub-cards using prefixes, e.g., `TASK-05.1`, `TASK-05.2`.
