---
name: benchwarmers
description: Get second, third and fourth opinions from a Benchwarmers collection of models (its MCP tools list_collections, ask, verdict). Use for an independent adversarial review ("where does this guarantee break"), checking edge cases, or an exhaustive enumeration over real files ("list every place X happens"), and whenever the user asks to consult the bench, a panel or a collection. Not for design decisions, which stay with you.
---

# Benchwarmers

A Benchwarmers server answers one prompt with every model in a **collection**
at once: its members, plus explorer seats it fills with the models whose
evidence is stalest. Every answer comes back under its own seat and model, with
a call id. Your verdicts on those answers decide which models it seats next
time, so using the bench and measuring it are the same act.

The tools are served by a running Benchwarmers itself, at its `/mcp`
(`BENCHWARMERS_URL`, default `http://127.0.0.1:8122`; a gateway key in
`BENCHWARMERS_KEY` where the server asks for one). If the tools are missing,
or the `benchwarmers` server shows as failed in `/mcp`, Benchwarmers is not
running: tell the user; do not work around it.

## When to ask

- **Adversarial review**: a diff, a function, a protocol, a claimed invariant.
  "Where does this break? What input makes it wrong?"
- **Exhaustive enumeration over real text**: every caller, every place a value
  is written, every branch that skips a check.
- **Edge cases** you may have missed.

Not for designing the thing, choosing between approaches, or making the
decision. Keep the reasoning and the decisions; use the panel to find what
you missed.

## How

1. **Ask a collection, not a favourite model.** `list_collections` says what
   each is for (description, tags, members, context window). The explorer
   rotation is what keeps the roster from narrowing to the two models that
   were good last month. Use `with` only to seat a model the user named. Ad
   hoc collections are not listed: they are expensive and run when the user
   names one, so ask it then, and never otherwise.
2. **Make the prompt stand alone.** Seats cannot read files: include the code,
   the diff, the file contents, with paths and line numbers, and the exact
   question. Keep it within the collection's context window. Leave out
   anything that should not leave this machine (secrets, private data).
3. **Verify before acting on anything a seat says.** Open the real source and
   check each claim. Seats have found real dead code and untested invariants,
   and have also agreed, three at once, on a security hole that did not exist.
   Agreement is not evidence; they fail together.
4. **Name every seat that answered**, by model and seat (member, explorer,
   stand-in for a held member), including those that errored or returned nothing useful. Two seats finding
   the same thing independently is a much stronger claim than one, and that
   is only visible if both are named.
5. **Send a verdict per seat you judged** with `verdict`: its call id,
   `useful`, a short note, and the claims it got right in `real` and the
   untrue ones in `false`, one sentence each. The claims feed routing and the
   "confidently wrong" record; a note alone does not. Put what disproved the
   false claims in `evidence` (a file:line, a command and its output): you can
   be wrong about a seat too, so without it they cost the model nothing. Set
   `caught` when the seat found something you had not; that count is what
   says the second opinions are worth asking for.

An **empty reply from a reasoning model** is almost always its token budget
(reasoning counts against `max_tokens`), not incapacity: say so, and judge it
as not useful without a `false` claim. A seat that errored needs no verdict.
A seat marked `late` was still answering when the panel stopped waiting:
name it too. Its answer goes to the dashboard, not to you, so it needs no
verdict from you; if the Stop hook lists it later, say so in one line.

`merged: true` returns one reconciled answer instead of every answer; every
seat is still called and listed with its call id, and the merge has its own.
Use it only when the user wants one answer; judging seats needs their own.
