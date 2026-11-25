---
name: agent-resume
description: Guide for using the `resumy` CLI to create tailored resume PDFs end to end. Use when a user wants to turn raw background information, an existing resume, or a target job description into resume copy and a final PDF; when an agent should collect candidate background first, collect the target JD second, tailor the resume truthfully, and run `resumy generate pdf`; or when troubleshooting browser-based PDF export in this repository.
---

# Agent Resume

## Overview

Guide the user from raw career information to a final PDF created with `resumy`. Collect background information first, collect the target job description second, tailor truthful resume copy third, then render the output with the CLI.

## Workflow

1. Collect candidate background first.
   Ask for basics, experience, projects, education, skills, links, and any output preferences.
   If the user already has an existing resume, profile, notes, or portfolio, extract facts from that artifact instead of re-asking everything.
2. Collect the target JD second.
   Ask for the full job description text, or at least the role summary, required skills, domain, and responsibilities.
3. Tailor the resume copy.
   Read `references/intake-and-tailoring.md` when you need the intake checklist, JD analysis steps, or rewrite rules.
   Reframe the user's real experience to match the job's priorities without inventing facts.
4. Map the tailored content into CLI flags.
   Read `references/resumy-cli.md` when you are ready to build the command.
   Use `resumy templates` if you need to inspect themes. Prefer `professional` unless the user asks for another style.
5. Render and verify.
   Run `resumy generate pdf ...`.
   Add `--html-output` when you want a debuggable HTML artifact.
   Follow the Playwright and browser fallback notes in `references/resumy-cli.md` if PDF export fails.
6. Deliver the result.
   Share the PDF path, summarize how the resume was tailored to the JD, and note any assumptions or missing facts that still need confirmation.

## Interaction Pattern

- Start with candidate background before asking for the JD if both are missing.
- After background intake, explicitly ask for the target JD.
- After you have both, decide whether the user would benefit from a short tailoring plan before rendering. For higher-stakes applications, show the plan first. For straightforward requests, go straight to drafting and rendering.
- Keep follow-up questions focused. Prefer grouped prompts over long interrogations.
- Preserve truthfulness. Never invent employers, dates, metrics, degrees, tools, or responsibilities.

## Rendering Rules

- Keep the most relevant experience and projects near the top.
- Trim weak or redundant bullets instead of overfilling the page.
- Use JD terminology only when it matches the user's real background.
- Prefer concise, impact-oriented bullets over generic responsibility lists.
- Use `--section-order` when the user's story benefits from emphasizing projects, education, or custom sections.

## References

- `references/intake-and-tailoring.md`: use for candidate intake, JD analysis, and resume-copy rewriting.
- `references/resumy-cli.md`: use for command construction, theme selection, output flags, and PDF troubleshooting.
