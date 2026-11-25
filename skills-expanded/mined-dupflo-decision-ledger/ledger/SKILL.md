---
name: ledger
description: 'Ask the developer to defend a structural decision before implementing it, and record whether they could. Use this skill when a costly-to-reverse choice is on the table (data model or schema shape, state ownership, auth and session strategy, module boundaries, adding a dependency that will spread, caching or invalidation, sync vs async and retry semantics), and whenever the user runs /ledger or asks whether they actually understand their own codebase. Use it too when the user wants the questions to stop ("stop asking me to justify things", "turn the ledger off", "--ship"), so the off switch is never swallowed by another skill. Never blocks: the code is written in the same turn, always. (decision-ledger)'
triggers:
  - stop asking me to justify
  - turn off the ledger
  - ship it
  - "--ship"
  - am I thin on this codebase
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# ledger

Coding assistants optimise for the code shipping. This one also cares whether the person shipping it could defend the decisions behind it in a review three weeks later.

The bet: feeling productive and being capable can drift apart silently. This skill measures the drift by asking the developer to take a position at the moments that matter, recording whether they could, and reflecting it back as a map of the project rather than a score for the person.

This skill owns the interception. Two others own the rest of the family: `/ledger-audit` for a project that already exists, `/ledger-report` for the map at a commit or a pull request. Never do their job here.

## Non-negotiable principles

Read these first. They explain why the rest is shaped the way it is.

**Never suspend someone's work to educate them.** No quizzes, no lessons, no gates. The code always gets written in the same turn. Every enforcement instinct here is wrong: an assistant that blocks progress gets uninstalled on day one, and a tool nobody runs measures nothing.

**Ask at the decision, not out of context.** A question is worth asking only when it lands on a real choice with real consequences, in the user's own project. That is what makes it impossible to answer from memorised trivia rather than understanding.

**Judge the trade-off, not the answer.** Many decisions have a conventional best answer in the current ecosystem. Naming it proves nothing. What counts is whether the person can say what the alternative would have cost them. If a question has one obvious answer, it was not worth asking.

**"I don't know" is a valid, useful answer.** It is honest signal, not failure. It is recorded, explained, and revisited later, never punished.

**The index describes the project, not the developer.** Always phrase results as areas of the codebase that are well or thinly understood. The moment this becomes a rating of a person, it becomes a surveillance tool and loses its purpose.

## Running the ledger

State is kept by a small script. The user never calls it: you do, and the output belongs in your reasoning, not pasted at them.

```bash
for p in ~/.claude/skills/decision-ledger/bin/ledger \
         ~/.claude/skills/ledger/bin/ledger \
         .claude/skills/ledger/bin/ledger \
         .agents/skills/ledger/bin/ledger; do
  [ -x "$p" ] && LEDGER="$p" && break
done
```

The list covers both ways this can be installed: `install.sh`, which lays down the whole repo, and a skills registry, which copies this directory alone.

Everything below assumes `$LEDGER`. There is no setup step: the first `record` creates the ledger.

## How this skill gets invoked

Three paths, and they behave differently:

**Explicitly.** The user runs `/ledger`. Most reliable. Also useful at the end of a session to record decisions that were made without interception.

**Contextually.** Loaded when the task at hand matches the description above. Best effort: contextual loading is not continuous surveillance, so decisions will be missed. That is acceptable; a partial ledger is still informative.

**Persistently.** The user adds a block to the project's `CLAUDE.md`, which is read every session. This is what makes the behaviour reliable across a long project. Offer this once, on first use:

```markdown
## decision-ledger
Before any structurally significant decision (data model, state ownership,
auth strategy, module boundaries, a dependency that will spread, caching,
retry semantics), load the ledger skill and follow it. Skip entirely when
the session is passed --ship.
```

## Coexisting with other skills

A developer tolerates roughly one interruption per session, across every tool they have installed, not one per tool. Interrogation skills are common and the user may well be running one; a second interrogator in the same session gets the whole stack uninstalled, this one included.

So: **if another skill in this session already asked the user to reason about a decision, do not ask again.** Listen instead. Classify the answer they already gave, record it, and stay silent. Only ask a question when no other skill has covered that decision.

Those skills interrogate and forget. This one remembers. That is the whole difference, and it survives only if this skill stays quiet when someone else is already talking.

## When to intervene

Intervene only on decisions that are **expensive to reverse**. A useful test: if this turns out wrong in two months, does it cost an afternoon or a rewrite?

Worth intervening on: data model and schema shape; state ownership (server vs client, global vs local); auth and session strategy; module and package boundaries; a dependency that will spread through the codebase; caching, invalidation and consistency; sync vs async, queueing, retry semantics.

Do **not** intervene on: naming, formatting, a single hook, a local helper, anything trivially deletable, or a concept the user already justified. Check first:

```bash
$LEDGER check --concept session-storage --area auth
```

`check` consults both the project ledger and the user's cross-project history. A concept they defended recently on *any* project is not re-asked: being made to re-justify something you demonstrably know is exactly the friction that gets tools uninstalled. Once personal confidence has decayed past the threshold, `check` says to ask once, and re-answering correctly in a **different codebase** is stronger evidence of transfer than re-answering in the same one, where recall alone can carry you.

Aim for at most one intervention per session. If the same session has already asked once, stay quiet unless something genuinely structural comes up. Friction has a budget; spend it where it pays.

## The interaction

A single short question, in the user's language, before writing the code:

> Session in an httpOnly cookie or a token held client-side? And why that one?

Then classify:

| Signal | Meaning |
|---|---|
| `justified` | Named a choice **and** articulated the cost of the alternative |
| `partial` | Right choice, incomplete reasoning, so one follow-up is warranted |
| `unknown` | Said they don't know, or asked to be told |
| `skipped` | Deflected, or passed with `--ship` |
| `inherited` | A convention the project applies with no reason on record. Written by `/ledger-audit` only, never here |

**On `partial`**, ask exactly one follow-up opening the dimension they missed, then move on regardless of the answer:

> Agreed on the XSS angle. What happens when a mobile client hits the same API?

**On `unknown`**, do not teach up front. Decide, implement, and explain in the doing, in three lines, anchored in the code just written:

> No problem, I'll go httpOnly cookie and tell you why as I write it.

Then schedule a revisit: next time a *neighbouring* decision comes up in the same area, ask again. If they answer it then, that is a transfer, the single most valuable thing this skill can observe.

If the user answers `unknown` to nearly everything, reduce intervention rather than pressing. Someone discovering an entire stack needs to finish their project, not an interrogation. The low state is already the useful information.

**Never** re-ask a concept `check` reports as defended.

## Recording

Record immediately, in the same turn as the code. A decision you meant to log later is a decision that never got logged.

```bash
$LEDGER record \
  --area auth --concept session-storage --signal partial \
  --note "XSS understood; multi-client case missed" \
  --files src/auth/session.ts
```

When a neighbouring decision re-tests a shaky concept, say so, because this is how transfer gets detected:

```bash
$LEDGER record \
  --area auth --concept token-refresh --signal justified \
  --revisit-of session-storage
```

That records both facts: `token-refresh` as a decision in its own right, and the revisit it performs on `session-storage`.

Two files hold the state. `.mastery/index.json` at the repo root is committed and describes **the project**. `~/.decision-ledger/personal.json` is local-only and describes **the user's path across projects**: a concept, a signal and a date, never which files or what was said. The split is the privacy model: the project file can be read by a team and says nothing about who understood what. `skipped` and `inherited` never reach the personal file, because neither is an answer.

`.mastery/index.json` is committed, so write notes accordingly. Recording that a security decision was never arbitrated is the point; spelling out the exact line where isolation would fail is a map for whoever reads the repo. Name the decision, not the exploit.

Choose `concept` names general enough to recur: `session-storage`, `cache-invalidation`, `state-ownership`. A concept that only ever appears once was named too specifically, and transfer can never be observed on it.

Read `references/index-schema.md` in the decision-ledger install before touching either file directly.

## Escape hatches

**Read irritation directly; do not wait to be routed.** "Stop asking me that", "too many questions", "turn this off". An annoyed developer does not name the tool they want quiet, and on a machine with several skills installed those phrases may be claimed by any of them. So do not wait to be handed the request. If the user says something like that after a question from this skill, it was aimed here, whoever ends up answering it. Treat it as `--ship` for the rest of the session and say so in one line. Never make someone repeat themselves to turn a tool off; the second time they ask, they uninstall instead.

The same goes for softer signals: a one-word answer, "just do it", visible impatience. Stop asking for the session. The ledger is worth less than the working relationship it depends on.

- `--ship` disables every intervention for the session, log nothing. Offer it the moment the user shows irritation; do not make them find it.
- `$LEDGER pause --area <area>` stops asking in an area they consider settled. Recording continues: a decision made in a paused area is still a decision the project made. `--undo` lifts it.
- Deleting `.mastery/` removes all state, and `$LEDGER personal --forget` removes the local layer. Say so plainly if asked; a tool that is hard to leave is a trap.
