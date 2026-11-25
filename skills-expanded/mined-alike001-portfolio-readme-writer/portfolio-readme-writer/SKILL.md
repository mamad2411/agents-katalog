---
name: portfolio-readme-writer
description: Write a polished, ship-ready README for a finished project. Two modes — personal portfolio projects (recruiter audience, clean & confident voice) and hackathon submissions (judge audience, punchy voice with problem statement, demo link, track alignment, team section). Use whenever the user is preparing to publish, push, or share a finished project — phrases like "write a README", "add docs", "document this project", "make this look professional", "prep for portfolio", "hackathon submission", "make this repo look good", or any time a finished project needs a public-facing description, even if the word "README" isn't said. Especially trigger when the user mentions pushing to GitHub, submitting to a hackathon, or sharing a project link.
---

# portfolio-readme-writer

A README writer for finished projects. Two modes — **personal** (portfolio/side project, recruiter audience) and **hackathon** (submission, judge audience). Different audiences, different shapes.

The goal is a README that makes someone trust the project in 30 seconds. Recruiters trust clarity and craft. Judges trust impact and polish. This skill writes for the right one.

## When to invoke

- User is about to push a finished project to GitHub
- User is preparing a hackathon submission
- User says "write a README", "document this", "make this look professional"
- User mentions a portfolio piece, project showcase, or repo cleanup
- User has a working project with no README, or a sparse one

## When NOT to invoke

- User is mid-build (no finished thing to document yet — wait until it works)
- User wants API documentation, contributor docs, or technical specs (different audience, different doc)
- User wants a code walkthrough or tutorial post

## Workflow

### Step 1 — Determine mode

Ask: **"Is this a personal/portfolio project or a hackathon submission?"** unless the context already makes it obvious (they mentioned a hackathon by name, or the repo has a `hackathons/` folder, or they said "judges").

Mode determines:
- Which template to follow (`references/personal-template.md` or `references/hackathon-template.md`)
- Voice (clean & confident vs punchy)
- What inputs to collect from the user

### Step 2 — Read the repo first

Before asking the user anything else, derive what you can from the project itself. The user shouldn't type things you can figure out:

- **Project name** — from `package.json` `name`, `Cargo.toml`, `pyproject.toml`, or the repo directory name
- **Stack** — inferred from:
  - `package.json` dependencies (React, Next, Vue, Express, viem, ethers, etc.)
  - `Dockerfile` and `docker-compose.yml` presence
  - `contracts/*.sol` → Solidity / smart contracts
  - `hardhat.config.*` or `foundry.toml` → web3 framework
  - `app/` or `pages/` directory → Next.js
  - `prisma/` → Prisma ORM
  - `requirements.txt` / `pyproject.toml` → Python
- **Project structure** — `ls -la` at root, then one level into key dirs
- **Existing README** — read it if it exists; you'll need it for the diff in Step 5
- **Existing assets** — look for `screenshots/`, `docs/`, `*.png`, `*.gif`, `demo.mp4` in the repo to reference in the README
- **License + open-source signals** — `LICENSE` file presence

### Step 3 — Collect missing inputs (batched)

Ask the user only for what you cannot derive. **Batch all questions in one message** — do not ping-pong.

**For both modes, ask:**
- One-line pitch (the hook — what is this in 10-15 words, no fluff)
- Quick-start commands (clone → install → run)
- Live URL if deployed (optional)

**Personal mode also asks:**
- Any caveats worth noting (ephemeral state, prerequisites, known limitations)

**Hackathon mode also asks (these are non-optional — judges look for them):**
- Hackathon name + year
- Track(s) entered, and sponsor(s) the project targets
- Problem statement (one paragraph — what pain does this solve, who has it, why now)
- Demo video link (required — judges watch this first; if missing, tell the user to record one before submitting)
- Team members (names + roles + GitHub/socials)
- Future roadmap (3-5 bullets — judges score on "would this survive past the hackathon")

### Step 4 — Generate the README

Read the matching template:
- Personal mode → `references/personal-template.md`
- Hackathon mode → `references/hackathon-template.md`

Follow the section order from the template. Apply the voice rules from `references/style.md`. No emojis. No "What I learned" section.

If the repo has multiple services or a notable architecture (smart contract + frontend, multi-container compose, microservices), include a small ASCII architecture diagram. For a single-process app, skip the diagram — it adds nothing.

### Step 5 — Write to file (with safety check)

Target: `README.md` at the repo root.

**If a README already exists:**
1. Show the user a unified diff of what would change (`diff -u old new` style)
2. Ask: "OK to overwrite? (y/n)"
3. Only write on explicit `y`

**If no README exists:**
Write directly.

After writing, tell the user the file path and suggest they preview it (e.g., `glow README.md` if available, or just open in their editor / view on GitHub after pushing).

## What this skill does NOT do

Scope discipline. The skill writes the README. That's it.

- Does not push to GitHub
- Does not generate screenshots, GIFs, or videos
- Does not write `CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`, or other docs
- Does not deploy the project
- Does not modify code

If the user asks for any of these, treat it as a separate task. Don't bloat the skill.

## Why these rules exist

- **Two modes, different voices** — recruiters skim for "is this person good?"; judges skim for "did this team build something real and aligned to the prizes?". One tone serves neither audience well.
- **Read the repo first** — asking the user what stack they used when `package.json` is right there feels broken. Friction kills usage.
- **Batch the questions** — one prompt with five questions feels efficient; five prompts with one question each feels like an interrogation.
- **Diff before overwrite** — the worst failure mode is silently destroying a README the user spent an hour on. Always show the change.
- **No "What I learned"** — that section belongs in a blog post, not a project README. Recruiters and judges don't care about your learning journey; they care about the work.
- **No emojis** — this skill targets people who want their work to look professional. Emojis read younger. The user explicitly chose this.
