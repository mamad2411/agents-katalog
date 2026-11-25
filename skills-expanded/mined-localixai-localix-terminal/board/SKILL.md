---
name: board
description: "Plan and track work on a kanban board the person watches in the llxterm window (Backlog, Todo, Doing, Review, Done, Discarded), and hand cards to subagents: for a task of several parts, work the person wants to follow or accept piece by piece, or parallel subagents that must not do the same thing twice."
user-invocable: false
allowed-tools: Bash(llxterm window:*), Bash(llxterm guide:*)
---

# llxterm: the board

The project's open cards, as they are now (nothing: none open):

!`llxterm window --board 2>&1`

```sh
llxterm window '{"action": "open", "kind": "board"}'
llxterm window '{"action": "interact", "tab": "b1", "op": "add", "cards": [{"title": "Cart button overlaps on mobile", "note": "Done when it does not overlap at iPhone SE."}]}'
llxterm window '{"action": "interact", "tab": "b1", "op": "take", "card": "c3"}'
llxterm window '{"action": "interact", "tab": "b1", "op": "review", "card": "c3", "note": "Moved the button to a sticky footer; checked at iPhone SE and Pixel 8."}'
```

One card in Doing each; only the person accepts into Done. Subagents: start one `llxterm:worker`
per card that touches its own files, its prompt naming the card and its name on the board ("take
c3; your name on the board: cart-button"). `llxterm guide board` has the columns, every op, how
to plan cards and hand them to workers.
