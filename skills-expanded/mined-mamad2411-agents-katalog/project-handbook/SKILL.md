---
name: project-handbook
description: >
  Maintains a single, plain-English living document (HANDBOOK.md) that always
  reflects how a website or SaaS actually works, so anyone — including a new tech
  team member — can read it and have full context and answers. Use whenever you
  build, change, ship, or explain a feature, or when the user says "document
  this", "update the docs", "write docs for the team", "explain how this works",
  "keep the docs current", or asks a "how does X work / where is X / why isn't X
  working" question about their own project. After building or changing anything,
  update the relevant handbook section and add a changelog line — treat this as
  part of the task, not an extra request. Keep the language simple and the
  structure fixed so it never gets confusing.
---

# Project Handbook — living, plain-English docs

Goal: **one file anyone can read in 10 minutes and understand the whole system.**
Not API reference. Not code comments. The *how it works, why, and where* — kept
current as the project changes.

## The rules (this is what keeps it non-confusing)

1. **One source of truth.** A single `HANDBOOK.md` at the project root. Never
   scatter docs across many files. If the project is large, sections may link to
   deeper notes in `docs/`, but the handbook is always the front door.
2. **Plain language.** Write for a smart teammate who just joined. Expand every
   acronym the first time (e.g. "Payload (the CMS we use)"). No unexplained
   jargon. Short sentences.
3. **Fixed structure.** Always the same 9 sections in the same order (below), so
   readers know exactly where to look. If a section doesn't apply, keep the
   heading and write "N/A" — never delete a heading.
4. **Update as you go.** After building or changing anything, immediately update
   the affected section(s) **and** add a dated line to the Changelog. Do this in
   the same task — do not wait to be asked. Stale docs are worse than none.
5. **Skimmable.** Prefer tables and bullets over walls of text. If a paragraph is
   longer than 4 lines, it's probably too detailed for the handbook.
6. **Capture the WHY and the FLOW, not the obvious.** Don't restate what the code
   plainly shows. Document decisions, tradeoffs, gotchas, and the end-to-end path.
7. **Answer real questions.** When someone asks a question the handbook doesn't
   answer, answer it — then add it to the FAQ so it's answered forever.

## The template (create HANDBOOK.md with exactly these sections)

```markdown
# <Project Name> — Handbook
> The one place that explains how this works. Plain English. Last updated: <YYYY-MM-DD>

## 1. What it is
<2–3 sentences. What problem it solves and for whom. No jargon.>

## 2. How it works (the flow)
<The happy path as numbered plain steps.>
1. A user does X.
2. The app sends it to Y.
3. Y stores it in Z and shows the result.

## 3. The parts
| Part | What it does | Where it lives |
|------|--------------|----------------|
| Web app | The pages users see | `app/` — Next.js |
| CMS | Where content is edited | Payload at `/admin` |
| Database | Where data is stored | Postgres on Azure |

## 4. Run it locally
<Exact commands, in order, that take someone from clone to running.>
```bash
npm install
npm run dev   # opens http://localhost:3000
```

## 5. How it ships (deploy)
<Where production lives, how a change gets there, what triggers a deploy.
Call out any traps — e.g. "prod deploys from GitHub repo A, but dev lives in
GitLab repo B; edits to B do NOT reach prod until synced.">

## 6. Data & integrations
<What data we keep and where. External services we depend on and why.>

## 7. Decisions & gotchas
<Why things are the way they are, and the traps that trip people up.
Format each as: "We do X because Y." or "Watch out: Z.">
- We hand-write DB migrations because the auto-generator produces destructive diffs.
- Watch out: the admin panel is login-gated, so verify UI with offline renders.

## 8. FAQ (for the tech team)
<Real questions, plainly answered. Grow this over time.>
- **How do I add a new page?** …
- **Where are secrets/keys?** …
- **Why isn't my change showing in production?** …

## 9. Changelog
<Newest first. One plain line each: what changed and why.>
- 2026-07-05 — Added the handbook. Sets up single-source docs.
```

## Working process

- **New project / no handbook yet?** Read the codebase enough to fill sections
  1–7 accurately, then create `HANDBOOK.md`. Don't guess — if unsure, mark it
  `TODO: confirm` rather than writing something wrong.
- **After a feature or change:** update the affected section(s) + add a Changelog
  line. Keep edits surgical; don't rewrite the whole file.
- **When asked a question:** answer from the handbook if possible; if it's not
  there, find the answer, give it, and add it to the FAQ (§8).
- **Keep it honest:** if something is broken or half-done, say so in §7 or §8.
  The handbook's value is that people can trust it.

## Optional: make updates automatic across all projects
Suggest adding one line to the user's project `CLAUDE.md`:
> After building or changing a feature, update `HANDBOOK.md` (see the
> project-handbook skill) and add a changelog line.
This makes keeping docs current a standing rule, not a thing to remember.
