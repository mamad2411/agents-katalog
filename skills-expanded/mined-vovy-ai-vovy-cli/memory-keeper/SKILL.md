---
name: memory-keeper
description: Use this to record and recall project memory — decisions with their rationale, mistakes with how to avoid repeating them, and hard constraints with the why behind them — via the project_memory MCP tool, stored as plain markdown in .vovy/memory/ and committed with the repo. Record whenever the founder corrects an approach, says "remember this" or "don't do that again", whenever an approach fails and gets abandoned, and whenever a real choice gets made between alternatives. Recall at the start of any non-trivial task, before revisiting a past choice, and whenever the founder asks "why did we" or "have we tried" something. When the founder wants something always or never done, first offer to encode it as a test or automated check; record it as a constraint memory only when it can't be made mechanical. Never record secrets, API keys, or passwords — memory is committed to git.
---

# Memory Keeper

The most valuable context in a project is also the first thing to evaporate: *why* a choice was made, *what* was tried and failed, and *which* rules exist for reasons nobody wrote down. Code shows what exists today; it doesn't show the three approaches that were rejected on the way, and the founder shouldn't have to re-explain them to you every session — or watch you confidently repeat a mistake they already paid for once.

`project_memory` fixes this with plain markdown files in `.vovy/memory/`, committed to git. No account, no server: `git clone` carries the memory to every machine, every teammate, and every AI coding tool the founder uses.

## When to record (do it in the moment, not at the end)

Record **without being asked** when any of these happen:

1. **The founder corrects you.** They rejected your approach or edited your output — the correction *and the reason* is a `mistake` or `decision` entry. This is the highest-value moment; it's also the one most often lost.
2. **An approach fails and gets abandoned.** "Tried X, it broke because Y" as a `mistake`. One sentence of negative evidence saves a future session an hour of rediscovery.
3. **A real choice gets made.** Library picked, architecture settled, tradeoff accepted — a `decision` entry. The rejected alternatives and *why they lost* are the point; the winner is already visible in the code.
4. **The founder states a standing rule.** "Never touch the billing code without asking" — but see the mechanical-first rule below.

Titles are stable handles: re-recording the same title updates the entry instead of duplicating it.

## The structure that makes an entry worth reading later

- **decision** — what was chosen, **what was rejected, and why it lost**. A decision entry without the rejected alternatives is just a changelog line.
- **mistake** — what happened, **why it happened, and how to avoid it next time**. Write it so a future session that never saw the incident can still obey it.
- **constraint** — the rule **and the why behind it**. "No native modules" invites relitigating; "no native modules because the founder's machine must never need a compiler" transfers the judgment to cases nobody anticipated.

## Mechanical first, prose second

When the founder wants something *always* or *never* done, prose memory is the weakest way to keep that promise — it only works if a future session happens to recall and heed it. First offer to make it mechanical: a test that fails, a lint rule, a CI check, a git hook. Record a `constraint` entry only for rules that can't be automated (taste, business context, timing), or as the why-documentation *alongside* the mechanical check.

## When to recall

- **Before starting any non-trivial task**: `recall` with a few words about what you're about to touch. Treat a returned `constraint` as binding and a returned `mistake` as a tripwire, not a suggestion.
- **Before proposing to change or replace something that looks odd.** The odd thing is often load-bearing, and the entry saying why is one recall away. If recall returns nothing, say so and proceed — absence of memory is information too.
- **When the founder asks "why did we..." or "have we tried..."** — answer from recall before answering from guesswork.

## Never record secrets

Memory files are committed to git, where they can end up public. Never put API keys, passwords, tokens, or connection strings in an entry — describe them instead ("the Stripe key in `.env`"). The tool refuses content that looks like a credential; don't work around that refusal, fix the entry.
