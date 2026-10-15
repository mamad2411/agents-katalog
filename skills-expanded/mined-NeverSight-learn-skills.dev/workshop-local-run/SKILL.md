---
name: workshop-local-run
description: Use when an HR workshop student cannot open a local HTML or Next.js prototype, Node.js is missing, npm run dev fails, the project folder is wrong, localhost will not load, a port is in use, or the Agent is about to build/run a workshop prototype and must check the computer first. Also use for standalone "Node not installed" / "npm run dev 不行" help when the student did not start a product skill.
---

# Workshop local-run

Open the student's local HTML or Next.js prototype in a browser. The student does not use the terminal.

This skill does not write PRDs, change MVP functions, edit product code, or deploy (no GitHub / Vercel / Supabase).

When a product skill is already running, keep that product skill in charge of stages. This skill only checks and starts the local prototype.

## Required references

Before running commands, read:

- `references/checks.md` — OS detect, Node, folder, port, install, open browser
- `references/errors.md` — error text → one student sentence

## Caller handshake

If invoked from `hr-workshop-mvp-flow` or a Group wrapper, use what they passed:

| Field | Meaning | If missing |
|---|---|---|
| `mode` | `preflight` or `repair` | Detect: student confirmed a plan → `preflight`; student said it will not run → `repair` |
| `kind` | `html` or `nextjs` | Detect from files (below) |
| `projectDir` | Folder that contains the app | Search from `pwd` for `package.json` with a `dev` script, or a workshop `.html` |
| `successPath` | Path to open after Next.js starts (e.g. `/login`) | `/` unless the running app's routes show a better first page |

Do not assume Group 6 paths (`talent-mapping-next`, `/login`) unless that instructor wrapper is explicitly active.

## Two entry points, one core

**Preflight** — student confirmed the HTML or Next.js plan. Run the core loop before writing app files or running `npm`. If class is `Ready`, say one sentence that they can start, then return to the product skill.

**Repair** — student says it will not open, nothing happens, terminal error, or blank page. Same core loop; then open the page.

Standalone prompts such as `Node 沒裝` or `npm run dev 不行` use **Repair**.

## Core loop

1. Read-only checks from `references/checks.md`. Do not change the computer yet.
2. Detect OS. Ask which computer only if detection is unreliable.
3. Detect `kind` (HTML vs Next.js).
4. Classify the machine (below).
5. Explain in plain language. Ask permission before any install, long download, admin prompt, or `npm install`.
6. Agent runs the command. Never ask the student to type terminal commands.
7. Verify by opening the page. Success is the page, not exit code 0.

## Detect kind

- `package.json` with a `dev` script → `nextjs`
- Workshop single `.html` and no Node app to run for this step → `html`
- Both → one question: which to open now
- Neither → class `Wrong folder`. Stop. Tell the student to use File → Open Folder on the project folder. Do not invent a project.

## Classification

Label exactly one:

| Class | When |
|---|---|
| Ready | HTML file exists, or Next.js has Node 20+, correct folder, `node_modules` (or install not needed yet in preflight), and no blocking error |
| Missing Node | `nextjs` and `node` is missing or too old |
| Wrong folder | `pwd` is not the app folder; no `package.json` / no target `.html` |
| No admin / company-locked | Needed install failed without admin, and user-level install also failed |
| Port in use | A dev server is already listening |
| Network / proxy | `npm install` failed with network errors |
| Unknown | Anything else. Stop. Send to instructor |

Do not give every student the same `npm install` script. Branch on the class.

## HTML success

Agent finds the correct `.html` and opens it (`checks.md`). Not blank, not file-not-found. Do not ask the student to hunt in Finder. Node is not required.

## Next.js success

All of:

1. Node 20 or newer
2. Working directory is the folder that contains `package.json` (not the course parent)
3. `node_modules` present, or Agent ran `npm install` after permission
4. Dev server running — reuse if already up; never start a second one
5. Browser opens `http://localhost:<port><successPath>` using the port printed in the terminal (`3000` or `3001`, not hard-coded if the log differs)

## Missing Node

Explain: "Node is the tool that lets this web app run on your computer." Ask permission.

- Admin available → official installer in `checks.md`
- No admin → user-level install in `checks.md`
- After install → new shell, re-check `node -v`
- Still failing → class `No admin / company-locked`. Stop. Name that class. Ask them to get the instructor. Do not pretend `npm run dev` worked.

## Interaction

- One question at a time. Prefer choices. Do not ask what you can detect.
- Exception to "Agent runs commands": a system permission window. Explain what they will see and which button to press. Wait until they say they clicked it. Never collect the computer password in chat. Never ask for API keys.
- Pause before Node install, multi-minute download, admin prompt, long `npm install`.
- Summarize command output. Do not ask them to paste the terminal.
- Translate errors with `references/errors.md`.
- Define Node, npm, folder, port, dependency in one sentence when first used.
- On success, only the next student action: open this URL, or "The HTML file is open in your browser."
- Mirror the student's language.
- Repair failed → name the class, send to instructor, stop. Do not edit MVP code.

## Do not

- Do not write or revise a PRD
- Change the 5 MVP functions
- Change product code to make the environment work
- Deploy, push to GitHub, or configure Vercel/Supabase
- Install Docker, Homebrew as a bundle, or tools this prototype does not need
- Start a second `npm run dev`
