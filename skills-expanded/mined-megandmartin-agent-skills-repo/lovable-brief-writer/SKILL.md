---
name: lovable-brief-writer
description: Turn a rough feature idea into a paste-ready Lovable prompt — goal, screens, data, states, edge cases, and an explicit do-not-touch list. Use when the user says "write a Lovable prompt", "brief for this feature", "tell Lovable to build", "spec this screen", or is about to paste vague instructions into an AI app builder. Don't use for writing the database migration behind the feature — use supabase-migration-writer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Lovable, Prompting, Product Spec]
    related_skills: [supabase-migration-writer, vercel-deploy-check, docs-readme-writer, bug-triage-protocol]
---

# Lovable Brief Writer

Converts "add a dashboard where users see their stuff" into a brief an AI builder can execute in one shot. The quality bar: every screen named, every piece of data sourced, every state designed (loading/empty/error, not just happy), and a fence around what must not change. Vague prompts cost credits and break working features; this skill exists so neither happens.

## When to Use

- User has a feature idea and is about to prompt Lovable (or any AI app builder — the format transfers).
- A previous Lovable prompt produced the wrong thing or broke something adjacent.
- User wants one feature spec'd tightly enough to build without follow-up questions.
- **Not for:** the SQL/schema behind the feature — use `supabase-migration-writer`. Not for verifying the deployed result — use `vercel-deploy-check`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Interrogate the idea | 6 questions: who / what job / which screens / what data / what states / what's off-limits |
| Snapshot current schema | `supabase db dump --schema public -f schema.sql` or list tables in the dashboard |
| Word-count the brief | `wc -w brief.md` (aim 150–400 words; over 500 → split into two prompts) |
| One feature per prompt | If the brief needs "and also…", cut it — that's prompt #2 |
| Save the brief | `briefs/$(date +%Y-%m-%d)-<feature>.md` so prompts are reusable and diffable |

## Procedure

1. **Precheck** — confirm you know the app's current state: what exists, what stack (Lovable default is React + Tailwind + Supabase), and what the user considers "working — don't break". If you can't name what must not change, ask before writing.
2. **Interrogate** — answer the 6 questions from Quick Reference from the user's description; ask only for genuine gaps. Nail the single sentence: "After this ships, a [user] can [do job] from [screen]."
3. **Scope to one feature** — a brief with two features is two briefs. Cut ruthlessly; note the cut items as "later prompts" so nothing is lost.
4. **Draft** — fill the Output Template. Sharp edges to enforce:
   - **Data** names real tables/columns (from the schema snapshot), or explicitly says "create table X — see migration" and pairs with `supabase-migration-writer`.
   - **States** covers loading, empty (first-run, with a helpful CTA — not a blank div), error (what the user sees and can do), and success.
   - **Edge cases** = at least 3 concrete ones (long names, zero items, slow network, logged-out visit, duplicate submit).
   - **Do NOT touch** lists working features, auth flow, existing routes, styling system, env/config — anything the builder might "helpfully" refactor.
5. **Review with the user** — walk them through it in 30 seconds: goal sentence, screen list, fence list. Adjust; this is cheaper than a wasted build round.
6. **Deliver** — the brief as one paste-ready block, plus a save path (`briefs/...`). Remind: paste as a single message; if Lovable asks clarifying questions, answer from the brief, don't improvise new scope.

## Output Template

```
## Feature: <name>

**Goal:** After this ships, a <user> can <job> from <screen>. Success = <observable result>.

**Screens & routes**
- /dashboard — <what's on it, what's clickable, where clicks lead>
- /dashboard/item/[id] — <same>

**Data**
- Reads: projects (id, name, created_at) — already exists
- Writes: inserts into projects on <action>
- Auth: page requires login; users see only their own rows (RLS already enforces this — do not add client-side filtering as a substitute)

**States**
- Loading: skeleton cards, no layout shift
- Empty: "No projects yet" + [New project] button
- Error: inline message "Couldn't load projects — Retry", no blank screen
- Success: <what the user sees>

**Edge cases**
- <case → expected behavior> (≥3)

**Do NOT touch**
- <auth flow / route X / component Y / global styles / env config>

**Out of scope (later prompts):** <cut items>
```

## Pitfalls

- **Happy-path-only brief** — builder ships a screen that white-screens on empty data. Recovery: never deliver a brief whose States section has fewer than 4 entries; empty state is the one users hit first.
- **Missing do-not-touch fence** — Lovable "improves" the login page while adding a dashboard. Recovery: always fence; if something adjacent did break, prompt exactly "restore <feature> to its previous behavior; change nothing else", and use Lovable's version history to revert rather than patching forward.
- **Data section written from imagination** — brief references columns that don't exist; builder invents a divergent schema. Recovery: snapshot the real schema first; if the table doesn't exist yet, say so explicitly and create it via `supabase-migration-writer` before or alongside the build.
- **Mega-brief (3 features, 900 words)** — builder does 60% of each. Recovery: split by the "and also" rule; ship prompts sequentially, verifying each before the next.
- **Brief lives only in the chat** — next month the prompt is unrecoverable and the rebuild diverges. Recovery: save every brief to `briefs/` with a dated filename.

## Verification

- [ ] Goal is one sentence with an observable success condition
- [ ] Exactly one feature; cuts logged as later prompts
- [ ] Every screen has a route; every route says what's on it
- [ ] Data section matches the real schema or explicitly creates new tables
- [ ] Loading / empty / error / success all specified
- [ ] Do NOT touch list present and specific
- [ ] Brief saved to briefs/ with today's date
