---
name: grill
description: >-
  Stress-test a plan or idea with pointed questions asked one at a time, each with a recommended
  answer, until more answers would not change the work; then write a short spec and a ticket list with
  what blocks what. The short version: use for "poke holes in this plan and give me tickets", "quick
  stress-test before I build", or before a build whose request leaves real choices open. For a long,
  open-ended interview with no spec at the end ("grill me", "grill me relentlessly"), use `grilling`.
---

# Grill

A plan fails on the question nobody asked. This skill asks those questions, one at a time, and turns
the answers into something an agent can build from.

## When it applies

- A build or change where two sensible readings would lead to different work.
- A plan, design or idea the user wants challenged before committing to it.
- A vague issue or request that needs to become a spec and tickets.

Skip it when the request is already precise. Build instead.

## Procedure

### 1. Read before you ask

Read the plan, the issue and the code it touches. Any fact you can look up (what the code does now,
which library is in use, what a config holds) is yours to find, not the user's to answer. Use a
subagent for the lookups if your host has them.

### 2. List the open decisions

Write, privately, every decision the plan depends on. Rank them by how much work changes with the
answer. Drop any whose answers would all lead to the same work.

### 3. Ask one question at a time

Ask the highest-ranked open decision first. Each question:

```
Q3. <the decision, one sentence>
Why it matters: <what changes in the work, one line>
Options: A) ... B) ... C) ...
Recommended: B, because <one line>
```

Wait for the answer. Then re-rank: an answer often settles or creates other decisions. Never ask
something a previous answer already decided.

Push back once when an answer conflicts with an earlier one or with the code. Name the conflict and
ask which wins.

### 4. Stop at the right point

Stop when every decision left would not change what gets built, or the user says stop. Usually that
is 4-10 questions. Say "That's enough to build from" and move on.

### 5. Write the spec

```
Goal: <one sentence: who gets what>
Decisions: <each answer, one line each>
Out of scope: <what this will not do>
Done when: <checkable acceptance criteria, one per line>
Open: <anything still unknown, and the default you'll use>
```

### 6. Write the tickets

Split the work into tickets an agent can finish in one session. Prefer thin slices that work end to
end over one ticket per layer.

```
T1  <title>  blocked by: none   done when: <check>
T2  <title>  blocked by: T1     done when: <check>
T3  <title>  blocked by: none   done when: <check>
```

Say which tickets can start now in parallel. Write them to a file or the user's tracker only if asked.

## Rules

- One question per message. A wall of questions gets skimmed.
- Every question carries a recommended answer, so "yes" is a valid reply.
- Ask about decisions, never about facts you could check.
- No spec until the questions stop changing the work.
