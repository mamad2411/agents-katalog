---
name: cli-forge-prez
metadata:
  author: clement
description: >
  Generate technical presentation decks in Marp Markdown from code, architecture,
  or documentation. Produces speaker-ready slides with notes, dark theme, and CI
  templates for PDF/HTML export. Use when the user mentions 'prez', 'presentation',
  'slides', 'deck', 'talk', 'lightning talk', 'pitch', 'conference talk', 'demo day',
  'speaker notes', 'technical presentation', 'Marp', 'slide deck', or wants to present
  a project, architecture, or design to an audience. Also triggers on 'keynote',
  'meetup talk', 'sprint review prez', 'make slides', 'present this'.
argument-hint: "[file-or-directory-or-topic]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are English. Detect the project's primary language (from README, comments, docs, commit messages). Generate the presentation in that language. If bilingual, ask the user.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

# Presentation Forge — Marp Deck Generator

Generate speaker-ready technical presentation decks from any project artifact — code, architecture docs, ADRs, audit reports, or a plain description.

## Core Principle — Two biological mechanisms

| Mechanism | What it does in nature | What it does in this skill |
|-----------|------------------------|----------------------------|
| **Peacock display** | Minimum viable signal, maximum recognition distance. Each ocelle is a high-contrast circle — one shape, instantly recognized by the peahen from across the clearing | One message per slide, instantly understood from the back of the room. If you must squint (mentally or physically), the signal failed |
| **Pheromone trail** | Ants lay a chemical trail between food and nest; each waypoint reinforces the path. Remove a waypoint and the colony detours; add a false one and ants get lost | The narrative arc is a trail the audience follows slide by slide. Each slide is a waypoint. Remove it: if the trail breaks, it was load-bearing. If nobody notices, it was noise — delete it |

## Input

`$ARGUMENTS` is one of:
- **File or directory**: the skill reads the project and builds a presentation about it
- **Topic description**: "pitch for grob — LLM proxy with audit trail"
- **Empty**: reads the current project root and asks which tier

## Workflow

### Step 0 — Determine tier

Ask the user or take it from arguments. **Do not auto-detect** — presentation context is too varied to infer.

Read `references/tiers.md` for the three tiers:

| Tier | Context | Slides | Duration |
|------|---------|--------|----------|
| **pitch** | Elevator, README hero, hallway | 3-4 | ~2 min |
| **lightning** | Meetup, demo day, sprint review | 6-8 | ~5 min |
| **talk** | Conference, workshop, client prez | 10-12 | ~20 min |

### Step 1 — Reconnaissance

Read the project. Build a mental model of: what it does, who it's for, what problem it solves, what makes it different. Use the shared reconnaissance brief — read `../shared/recon.md` (the same model readme and demo use, so all three tell one story).

### Step 2 — Choose narrative framework

Read `references/slide-structure.md` for frameworks by tier. Default:
- **pitch**: Hook → Solution → Proof → CTA
- **lightning**: SCR (Situation-Complication-Resolution)
- **talk**: 5-Box (What → Why → How → What If → What Next)

### Step 3 — Generate Marp Markdown

Read `references/marp-reference.md` for syntax, themes, and advanced techniques.

**Mandatory rules:**
- Every slide passes the **5-second test** — the audience grasps the message in 5 seconds
- Every slide has **speaker notes** in `<!-- ... -->` comments — not optional
- Headings are **assertions, not labels** (Alley model): `# Pods restart 3x faster with preemption` not `# Preemption`
- **Max 6 words** on visual slides, **max 5 bullet points** on content slides
- Code blocks: **max 8 lines**, highlight the 2-3 lines that matter
- Dark theme by default (better for conference projectors in bright rooms)
- Mermaid diagrams via `cli-forge-schema` handoff when architecture visuals are needed

### Step 4 — Write output files

Write the `.md` file to `docs/slides/{tier}-{name}.md` (or `talks/` if the project convention differs). Standard path, no AI markers.

If the project has CI (GitHub Actions or GitLab CI), suggest the CI template from `references/ci-templates.md` for PDF generation and Pages deployment.

### Step 5 — Quality checklist

Before delivering, verify:

- [ ] Every slide passes the 5-second rule (peacock test)
- [ ] Removing any slide either breaks the narrative trail or proves it was noise
- [ ] Speaker notes present on every slide
- [ ] No slide has > 8 lines of code or > 5 bullet points
- [ ] Opening hook and closing slide form a **callback pair**
- [ ] Dark theme renders well (high contrast, no color-only information)
- [ ] Total slide count matches tier expectation

## Anti-Patterns

Read `references/anti-patterns.md` for the 11 named anti-patterns to detect and avoid during generation (Feature List, Wall of Code, Architecture Astronaut, Demo Gods, Slideument, Curse of Knowledge, Apology Slide, Bibliography, Outline Slide, Font Roulette, Premature Abstraction).

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Architecture diagram needed | `/cli-forge-schema` | Generate Mermaid for embedding in slides |
| Presenting audit results | `/cli-audit-code` or `/cli-audit-doc` | Run the audit first, then present findings |
| Presenting project structure | `/cli-forge-tree` | Generate annotated tree for slides |
| Presenting an HLD/LLD | `/cli-forge-hld` or `/cli-forge-lld` | Generate design doc, then distill into slides |

**Rule:** Recommend, don't auto-execute.

## Rules for the Generator

1. **The slides support the speaker, they don't replace them.** If the deck is readable without a speaker, it's a document — not a presentation.
2. **Concrete before abstract.** Show the specific case, then generalize. Never the reverse.
3. **One idea per slide, one idea per talk (lightning).** A lightning talk with two ideas is two bad talks.
4. **Speaker notes are the real content.** The slides are visual anchors. The notes are what the speaker actually says.
5. **Dark theme by default.** Conference projectors in bright rooms render dark backgrounds with light text better than the inverse.
6. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-forge-schema` | Generates Mermaid diagrams embeddable in Marp slides |
| `cli-forge-readme` | Both generate project descriptions; prez is the oral version, readme is the written one |
| `cli-forge-doc` | Generates docs that can be distilled into slides |
| `cli-forge-hld` / `cli-forge-lld` | Architecture docs → presentation material |
| `cli-audit-code` / `cli-audit-doc` | Audit reports can become presentation content |
