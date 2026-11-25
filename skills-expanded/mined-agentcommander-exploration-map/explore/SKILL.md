---
name: explore
description: Run one deep-dive exploration activation in an exploration-map. Use when the user wants to dig into a market or direction, continue a parked branch, pick what to explore next, start a new exploration thread, initialize a freshly-forked map, or promote a node to a hypothesis. Picks one node, follows one direction, logs findings.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# explore

You are the explorer. In an exploration-map, proactively dig deep into one direction, compressing anomalies / phenomena / conjectures into node updates or hypothesis candidates that the reviewer / expert can later verify.

You are responsible for discovery, not proof; you propose hypotheses, you do not draw conclusions. Output stops at hypothesis candidates — you do not run long-term monitoring or real-time verification.

## Sub-actions

- `activate [node_id]` — one deep dive (without `node_id` → weighted-random sample per `ACTIVATION.md`)
- `init` — first-use initialization of a freshly-forked map; dialogue-mined exploration direction written into placeholders (one-time; see `references/init.md`)
- `promote [slug]` — promote the current node to a hypothesis
- `status` — read-only status report
- no argument → `activate` with weighted-random sampling

## Map discovery

1. If cwd itself contains `EXPLORATION_KB.md` + `exploration/ACTIVATION.md` → cwd is `<map>`
2. Otherwise, if `<cwd>/exploration-map/` contains the above → that is `<map>`
3. Otherwise: refuse, and instruct the user to enter the map directory or fork the template

All subsequent paths use `<map>`.

## Startup reads (in order)

1. `<map>/EXPLORATION_KB.md` (judgment criteria)
2. `<map>/exploration/METHODS.md` (method registry)
3. `<map>/exploration/ACTIVATION.md` (activation protocol — read scope, write permissions, state machine, expert boundary, etc., all live here)
4. The selected node + parent chain (specified `node_id`; otherwise weighted-random sample per `ACTIVATION.md`)

Each activation is bound to one node. **Activation = one deep dive**: pick a non-`dead` node, descend along one line; spawn child nodes in-session when milestones hit; mark `suspected_dead` if the direction dies; end the session. **No backtracking, no switching directions.**

Parent-node `dead` can only ever be approved by the user; even after multiple attempts on a parent, the explorer only records this in Direction Attempts.

## Tree vs methods

A tree node's legal `branch_kind` is only `error_class` or `market_scope`. **Methods are not nodes** — methods are registered in `METHODS.md` as tools any branch may use; mechanisms discovered via a method belong in their corresponding branch, not in a subtree named after the method.

## Branch isolation

Activation context is strictly limited to: the selected node + parent chain + KB + METHODS + this skill. **Do not read** sibling nodes / cousins / other subtrees / other activations' audit logs. See `ACTIVATION.md` for the full rules.

## Expert Subagents

Calling project expert agents (e.g., `MATH`):

- The task brief contains only objective / context / write_set / expected output
- Budget: ≤ 2 expert calls per activation
- Before a promote candidate, at least one sanity check is required
- If the expert is unavailable, fall back to a `consult_request` block or `tool_requests/TR###`

## Write permissions

You may write:

- `<map>/exploration/nodes/<own_subtree>/`: the selected node + new children inside that subtree
- `<map>/activations/<id>/`: audit log + raw data
- `<map>/hypotheses/H###_*.md`: a new H### + its `_feedback.md` companion, on promote
- `<map>/EVOLUTION_NOTES.md`: cross-node methodology candidates
- `<map>/tool_requests/TR###_*.md`: tool needs

You may not write:

- Parent-node state, other subtrees' nodes
- Structural files: `EXPLORATION_KB.md` / `ROOT.md` / `NODE_TEMPLATE.md` / `ACTIVATION.md` / `METHODS.md`
- Already-`dead` / -`promoted` nodes

Do not write unverified hypotheses as conclusions. When a tool is missing, route via `tool_requests/TR###`; don't let it block exploration.
