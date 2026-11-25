---
name: figma-email-readiness
description: >
  Audits a Figma file to see whether it is set up well enough for AI to design on-brand,
  build-ready emails in it, and produces a scored report plus a fix list. Run it before using
  email-design on a new file, or whenever AI-made emails come out off-brand or hard to build.
  Use whenever someone asks to audit, score or check a Figma file for email design, or asks
  "is our Figma ready for AI". Read-only: it never edits the file. Triggers on: Figma audit,
  Figma readiness, email setup audit, is my Figma ready, score our Figma file.
---

# Figma Email Readiness

Reads a Figma file, finds the email frames, and scores the file against the setup an AI needs
before it can design emails there:
- a brand kit
- color tokens
- an email type scale
- components
- clean email frames
- the handoff conventions around each email

It writes two files: a report anyone can read, and a fix list someone can work through. The
checklist behind it is [`SETUP.md`](../../SETUP.md).

## Why this exists

AI email design fails for setup reasons more often than for prompt reasons. When colors are
typed by hand, text has no styles and every email is drawn from scratch, the AI has nothing to
reuse and nothing to check itself against, so it guesses. The same gaps slow down every human
designer and every build in the email platform.

## Running it

1. Load the `figma-use` skill. It is required before any `use_figma` call.
2. Take the file key from the Figma URL (`figma.com/design/<fileKey>/...`).
3. Read `scripts/audit.js` and pass the whole file, unchanged, as the `code` argument of
   `use_figma` on that file key. It only reads. If the emails use another width, change
   `CONFIG.emailWidths` in the code you send, not in the file.
4. If check K1 reports 0 local variables, 0 color styles and 0 library variables in use, run
   `search_design_system` with `includeVariables: true` before calling tokens missing. A team
   library can exist without being bound in the emails yet.
5. Do the visual pass (below).
6. Write the two outputs (below).

| CONFIG | Default | Meaning |
|---|---|---|
| `emailWidths` | `[600, 640]` | Frame widths that count as an email |
| `scales` | `[1, 2]` | Also finds emails drawn at 2x (1200 or 1280 px) and reads their sizes at half |
| `minEmailHeight` | `700` | Shorter frames at those widths are cards or components |
| `coverage` | `0.9` | Share of emails that must pass the per-email and handoff checks |
| `maxEmails` | `40` | Larger files are sampled evenly. The report must say so. |

### The visual pass

The script can't judge photos or rendering. Screenshot up to four emails from different pages at
1:1 (`get_screenshot`, `maxDimension` set to the frame height), plus the brand kit page if there
is one. Look for:
- **Products without their branding:** unlabeled jars, blank packaging.
- **Mixed shoots:** photos that look like different shoots or different light.
- **Clipped or overlapping text** the script missed, such as text over images.
- **Placeholder images.**

Visual findings go into the fix list. They don't change the score, and the report says so.

## What it scores

Six areas, 22 checks, weights summing to 100. Each check passes or fails, with no partial
credit, because partial credit flatters. Scores are floored, never rounded up. Every check, its
pass condition and the reasoning are in `references/rubric.md`.

| Area | Weight | What it asks |
|---|---|---|
| Components | 25 | Can the AI assemble emails from reusable pieces? |
| Email frames | 20 | Are the emails built so the email platform can translate them? |
| Brand truth and handoff | 20 | Is the brand written down, and does each email carry its subject, brief and status? |
| Color | 15 | Are colors named tokens or typed by hand? |
| Type | 10 | Is there an email type scale, and is it used? |
| Accessibility and copy | 10 | Does text pass contrast, and is the copy real? |

## Two rules that keep the report honest

**Missing foundations are file-level findings.** No emails at the expected width, no color
tokens, no text styles, no components, no brand kit page: each is reported once at the top.
Never present one missing foundation as hundreds of individual failures.

**Repeated evidence points at a component.** When the same failure shows up in most emails, find
the component it comes from and report it once, as one fix that clears every email. On a real
production file, contrast failed in 40 of 40 sampled emails. It was one footer component with
grey 10.5 px text at 3.2:1: one fix, not forty.

## Grades

| Score | Grade | What it means |
|---|---|---|
| 90 to 100 | Ready | AI can design emails in this file today |
| 75 to 89 | Minor gaps | A short, scoped fix list |
| 55 to 74 | Needs work | A real setup project |
| Under 55 | Not ready | Foundations are missing. Start with the file-level findings. |

## Outputs

Save to the folder the user names, by default `./figma-readiness-<label>/`.

- **`report.md`**: follow `references/report-template.md`. Plain language, short sentences, no
  jargon without a one-line explanation.
- **`fixes.csv`**: columns `area, check, where, what is wrong, fix, scope`, where `where` is page
  / email / node ID and scope is `component`, `file` or `email`. Order the rows by leverage:
  component and file fixes first, then per-email fixes.

## Reference results

- **The Limonaia example** scores 100. It scored 95 until its section components (hero, text
  block, image and text, callout, steps, review, cart line) were added.
- **A real production file** with 265 emails, sampled to 40, scored 54. The gaps were real:
  - one footer causing every contrast failure
  - raw colors and unstyled text in older emails
  - template code shown as copy
  - no inbox preview, brief or status on older pages

## Privacy

Email names, copy and layer names in the result belong to whoever owns the file. Use a
de-identified label on anything you share, and don't commit audit outputs to a public repo.

## What this is not

- **Not a review of one email.** That is `email-design-review`.
- **Not the fix.** It tells you what to set up. [`SETUP.md`](../../SETUP.md) explains how.
- **Never edits the file.** No quick fixes while auditing, even obvious ones. Report them.

## Known limits

- **Components are found by name** (header, footer, button, product, hero, and so on). A file
  with unusual names can under-score C1 and C2. Check the component list in the result before
  calling something missing.
- **Contrast uses the nearest solid background.** Text over photos is skipped and belongs to
  the visual pass.
- **Brand kit coverage is a keyword scan** of a page named like a brand kit. A kit kept outside
  Figma scores as missing. Say so in the report and ask where it lives.
- **Unsubscribe, address, hard line breaks and straight apostrophes are warnings,** not scored.
