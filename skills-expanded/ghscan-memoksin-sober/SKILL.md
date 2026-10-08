---
description: Propose who on the team takes which SOBER node, by matching each contributor's role and focus against the board. Use when the user asks who should do what, or wants work spread across the team.
argument-hint: "[handles] — or nothing, to use everyone on the project"
---

> **These are tools, not commands.** Everything named in backticks below —
> `board`, `contributors`, `distribute` and the rest — is a tool of the `sober`
> MCP server SOBER installs into this host. Call it as a tool. Never reproduce
> one with `bash`, never read `.sober/` by hand, and never write a script that
> stands in for one: the board you would reconstruct is a guess, and a guess
> with real ids in it is worse than no answer. If a tool is not available, say
> so and stop — `sober --help` on the command line does all of it.

Allocating work is yours because it needs judgement, and it is yours **only as
far as proposing it**. Nothing you write here assigns anybody. The human takes
the plan, or drops it.

Read the team (`contributors`) and the board (`board`). If nobody is on the
project, say so and stop — `contributors add` is one command, and a distribution
across an empty team is nothing.

Match on what is actually there, in this order:

1. **`focus`, against the node's files.** A focus entry that looks like a glob is
   the strongest signal there is: `packages/core/**` against a node predicting
   `packages/core/src/team.ts` is not a judgement call. Use it first.
2. **`focus` as words, and `role`.** Both are free text and both are somebody's
   own description of what they do. Read them as prose, not as keywords.
3. **What the board is waiting on.** A node three others depend on is worth
   giving to whoever can start it now, over the person who fits it slightly
   better and is already on two nodes.

Then `distribute` with the matches. Every one carries `because` — one sentence,
the actual reason: which focus entry it hit, or what about the node made it
theirs. That sentence is the only part of your reasoning that leaves this
conversation. The human may read it tomorrow, on the dashboard, with no memory
of this session.

**Do not propose for a node somebody has claimed.** A claim is a fact and an
assignment is a plan; SOBER passes those over whatever you send, and a proposal
full of them reads as a plan that did not look. Finished nodes likewise.

**Do not spread work evenly for its own sake.** Four nodes to one person and none
to another is the right answer when that is what the board says. Say so.

Show the plan to the user with the reasons, and tell them plainly: nothing is
assigned yet. They take it with `distribute` (`accept: true`), which asks them
directly — the answer is theirs and you cannot give it — or on the command line
with `sober distribute --accept`, or on the dashboard. `drop` is there for a plan
they disagree with, and it takes no answer because it assigns nobody.
