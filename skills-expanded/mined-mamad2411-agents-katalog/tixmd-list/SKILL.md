---
name: tixmd-list
description: List all tixmd tickets with status, title, labels, and progress. Use when the user wants to see the project board, check ticket statuses, or find tickets by status or label.
---

# /tixmd-list

List all tickets on the tixmd board.

## Instructions

1. Run the `tixmd list` CLI command to get all tickets:

```bash
npx tixmd list
```

2. If the user wants to filter by status, use the `--status` flag:

```bash
npx tixmd list --status <status>
```

Valid statuses: `spike`, `blocked`, `ready`, `doing`, `done`.

3. Present the results to the user. Explain what each status means if this appears to be their first time using tixmd:
   - **spike** `?` — needs exploration, no acceptance criteria yet
   - **blocked** `!` — has criteria but depends on unfinished tickets
   - **ready** `○` — ready to be picked up
   - **doing** `◐` — work in progress (some criteria checked)
   - **done** `●` — all criteria completed

4. If no tickets are found, let the user know the board is empty and suggest creating tickets with `/tixmd-new` or generating spikes with `/tixmd-project-spikify`.
