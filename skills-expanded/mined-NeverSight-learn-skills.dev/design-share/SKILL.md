---
name: design-share
description: Publish a runnable prototype and return a shareable link. Prepares the prototype to run, starts/serves it (or deploys), and hands back a URL plus run instructions for review. Use when the user says "share the prototype", "give me a link", "publish this", "let the team see it", "deploy the preview", or is ready to circulate a prototype for feedback. Final stage of the Product Design set.
---

# Design — Share

Get the prototype in front of reviewers with a working link + clear run notes. Final handoff stage. The goal is that someone who wasn't involved can open it, know what to look at, and leave useful feedback — without you in the room.

## When to use
- A QA'd prototype is ready to circulate for feedback.
- "Share it", "give me a link", "publish", "let the team see it".
- Handing off to stakeholders for review/sign-off.

## When NOT to use
- The prototype hasn't passed `design-qa` (especially HIGH items) — fix or explicitly flag first.
- It's not runnable yet → `design-prototype`.

## Inputs
- The **QA'd prototype** (path).
- **Share method**: local serve, tunnel, or deploy to a host.
- **Host/account constraints** — ask before deploying anywhere external.

## Workflow
1. **Confirm it runs clean**: install + build + start. Fix any breakers before sharing.
2. **Pick the share method**:
   - **Local** — serve on a port; give the localhost URL + start command (good for solo/local review).
   - **Tunnel** — expose local via a tunnel; only if the user wants external access right now.
   - **Deploy** — push to a preview host (Vercel/Netlify/etc.). **Only with explicit user go-ahead**, since it sends code off-machine.
3. **Write a review note**: what to look at, the happy path to click, known stubs/TODOs, where to leave feedback.
4. **Return** the link + run instructions + review note.

## Worked example
```
method: local serve (user wants to review on their machine)
preflight: `npm install` ok, `npm run build` clean, `npm run dev` boots :5173 ✓
deliverable:
  link: http://localhost:5173
  run:  `npm install && npm run dev`
  review this: complete the onboarding happy path (Welcome → Template → Name → Dashboard);
               check the empty-name error and the loading state on "Create"
  known stubs: templates are 3 fixtures; "Create" writes to in-memory store (no real API yet)
  feedback: leave notes in #design-review or as comments on the Figma frame
```
(If deploy was requested: confirm host, check for secrets/env files, deploy, return the live URL + same review note.)

## Quality bar
- The link actually works and the app boots from a clean clone (you verified install→build→run).
- The reviewer is told exactly what to click and what's stubbed — no guessing.
- Any unresolved QA items are surfaced honestly, not hidden.
- For deploys: confirmed with the user, and no secrets/env files published.

## Common pitfalls
- **Sharing something that doesn't boot** — always run install→build→start from clean first.
- **Deploying without consent** — external deploy/tunnel sends code off-machine; that's a high-impact action requiring explicit go-ahead. Flag if the repo may contain secrets.
- **Publishing secrets** — check for `.env`, keys, credentials before any deploy.
- **No review guidance** — a bare link with no "look at this" yields vague feedback.
- **Hiding known issues** — silently sharing a prototype with HIGH QA failures wastes reviewers' trust.

## Handoff
This is the terminal stage. Feedback typically loops back to `design-prototype` (changes) or `design-ideate` (rethink). If the prototype is approved, it becomes the reference for engineering build-out.

## Tooling
Local serve needs the project's dev server only. Tunnel/deploy needs the relevant CLI (and user consent). No special tool for the review note — it's written guidance.
