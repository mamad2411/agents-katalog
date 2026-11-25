---
name: readme-writing
description: Use when writing or improving a project's README — for new repos, hackathon/demo submissions, or rotted setup docs. Trigger whenever the task involves a README.md, project description, "how to run" instructions, or making a repo presentable to reviewers and voters.
---

# Writing a README that doesn't suck

The README is the door to the project. It is the first thing a reviewer opens and the first thing a voter reads before deciding whether to try the demo. Treat it as conversion copy for skimmers, not internal documentation. When you write or revise one, follow the structure below in order and check it against the failure modes at the end.

## Before writing

- Identify the project **type** (web/app, CLI, library, hardware, game). Each type changes the hero asset and quick-start.
- Find the real entry points: the start command, the live URL, the required runtime versions, the env vars. Read the actual config (package.json, Dockerfile, .env.example) instead of guessing.
- Write for a visitor who has never heard of the project or the event it was built for. Never assume the reader knows the context.

## The structure that works

1. **Title + one-sentence description.** The title is the project's name. The next line says what it *is* to a human — not what it does internally, and not a story about the author. Good: "FitTrack — A REST API for tracking workouts, body metrics, and personal records." Bad: "This is my hackathon project! I made an API with FastAPI and SQLModel." Describe the thing, not yourself.
2. **Hero image, GIF, or screenshot.** One visual right after the description, showing the project in action — people skim, and an image turns a skim into curiosity faster than any sentence. Web/app: a clean screenshot or GIF of the main flow. CLI: an asciinema cast or animated GIF of a real session. Hardware: a photo of the assembled build (renders are second-best). Game: a gameplay GIF or key-art frame. If no asset exists, leave a clearly marked placeholder and tell the user exactly what to capture.
3. **The "try it" link.** A bold, impossible-to-miss link to the live demo, even if it repeats the demo field — some people land on the README first. A button-style image link is ideal. Never let the demo link just point back at the repo.
4. **Quick start.** The shortest path from "I want to try this" to "I am trying this." Web: usually just "open the link." CLI: a copy-paste-runnable install command in a code block. Library: the import plus a 5-line example. Game: download link and how to launch. If the quick start runs past three commands, push to default, prebuild, or cut steps.
5. **Features.** 3–7 specific, scannable bullets describing what the project actually does — each ideally verifiable in the demo. Not a marketing pitch. Fewer than three feels thin; more than seven becomes a wall nobody reads.
6. **How to run it locally** (for anything beyond a deploy-only site). Spell out the required language version (e.g. Node 20, Python 3.11), non-language system dependencies (ffmpeg, postgres), environment variables with example values, and the exact start command. Don't make reviewers guess npm vs yarn vs pnpm.
7. **How it works** (optional but recommended). One or two paragraphs on an interesting technical decision or tradeoff — this is where reviewers justify a high "technical depth" score. Explain a choice, don't list libraries. Good: "The diff view runs client-side in Web Workers because main-thread parsing stalled the UI on large files." Bad: "I used React, Tailwind, and Postgres."
8. **Credits / acknowledgements.** People who helped, libraries leaned on heavily, asset packs used. It's the right thing to do and it signals real open-source experience.

## Common mistakes to catch and fix

- Leftover starter-template boilerplate ("This project was bootstrapped with…"). Reviewers see thousands of these — replace it.
- A description that's only "This project is for [event]!" — useless to a visitor who doesn't know the event.
- No images at all. A wall of text loses skimmers in seconds.
- Setup instructions that have rotted. Re-verify every command against the current code before shipping.
- A "demo" link that's actually the GitHub repo.

## One trick

When unsure of shape, open a README from a project the user admires and steal its opening — the first three lines, the first image, the first link. Good READMEs converge on the same shape because that shape works.

## Output rules

- Produce real, runnable content tailored to *this* project — no placeholders except clearly flagged spots where the user must supply an asset or secret.
- Match the project's actual stack and commands; verify against the repo rather than inventing.
- Keep prose tight and direct. Cut filler and self-referential framing.