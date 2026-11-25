---
name: blindspot-pass
description: >-
  Surface the user's unknown unknowns before they start work in an unfamiliar
  area (new codebase area, domain, or tool). Produces a read-only blindspot
  briefing plus advice on how to prompt better. Use when the user says
  "blindspot pass", "盲区扫描", "unknown unknowns", asks what they don't know
  or might miss before diving in, says "我刚接手这块代码",
  "开工前帮我看看有什么坑", or merely describes facing unfamiliar territory —
  the statement is the request. Not for finished or pre-merge work (use
  change-quiz), nor for interviewing the user (use interview-me); mixed
  requests start here — brief, then hand off.
---

# Blindspot Pass

Help the user discover their unknown unknowns before work starts. This is a
read-only pass: do not modify any files.

## Workflow

1. **Anchor on the user's starting point.** If not already clear from the
   conversation, ask once — a single short message, at most three
   sub-questions — about their experience with this problem and codebase,
   what they have already decided, and what they plan to do next. If asking
   is not possible (e.g. an unattended/CI run), the user deflects ("just
   go"), or the reply does not answer the questions, state your assumptions
   in one line — folding in whatever they did say — and proceed.
2. **Explore the territory.** Start from the files the task will touch — or,
   when the user is adopting an area rather than doing one task, its entry
   points (public API, main module, README) — and expand outward: direct
   dependencies/dependents, tests, docs, then git history of the touched
   files (not the whole repo). If history is unavailable (tarball, shallow
   clone, fresh repo) or the area is not code, use its changelog, release
   notes, or prior internal write-ups instead. For non-code areas (a SaaS
   tool, a business decision), expand the same way through official docs
   and pricing, adoption and migration post-mortems from other teams, the
   vendor's changelog and viability, and compliance constraints. In large
   codebases, cap this pass at roughly 15-25 file reads/searches: follow
   the 2-3 leads most likely to change the user's approach; if a lead
   stalls (slow search, missing tooling), drop it after one retry; when you
   hit the cap, stop and report, listing unexplored areas explicitly as
   unswept corners. If the domain is unfamiliar to you or fast-moving,
   search the web. Look specifically for things the user did not mention in
   their description of the task.
3. **Report blindspots** directly in the chat response, in the language of the
   conversation (do not create files unless the user asks for a document),
   organized as:
   - **Questions you didn't know to ask** — decisions hidden in this area
     (existing conventions, invariants, feature flags, edge cases; for
     non-code: pricing-tier traps, data-export paths, compliance).
   - **What "good" looks like** — quality bars, reference implementations, or
     prior art the user should calibrate against.
   - **History and potholes** — past attempts, known pitfalls, TODO/FIXME
     landmines, coupling that will bite.
   - **Domain concepts** — if the domain is new to the user, teach the 3-5
     concepts they need to evaluate results (not an encyclopedia).
4. **End with "how to prompt me better":** 3-6 concrete things the user should
   specify in their next prompt now that these blindspots are visible. If
   "what good looks like" surfaced a concrete reference worth copying,
   suggest reference-hunt. If the remaining ambiguities would change the
   approach, can only be decided by the user, the session is interactive,
   and the user has not declined to answer questions, suggest running
   interview-me next; otherwise end after the prompt advice. If the area
   was simple (see Rules), shrink or skip this section.

## Rules

- Prioritize blindspots that would change the user's approach; skip trivia.
- Cite checkable sources: file paths + line numbers, or URLs / commit hashes.
- If the area turns out to be simple with few blindspots, say so plainly
  instead of inventing findings.
