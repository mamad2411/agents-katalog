---
name: axiom
description: AxiomCore front door - onboarding and module management. Actions - start (first-run setup, scaffolds the workspace), activate <module> (M2-voice, M2-brand, M3, M4), deactivate <module>, tier <simple|advanced>, language <code>, status, overview. Run start in any new folder to set up the system.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/axiom <action> <arguments>`.

If the requested action is ambiguous or contradictory, do NOT guess: flag it and ask for clarification before executing.

This skill owns `axiom-config.md` — all other skills read it, only this skill writes it. Templates used below ship in this skill folder: `claude-kernel-template.md`, `soul-template.md`, `brand-config-template.md`, `axiom-config-template.md`, `getting-started-template.md`.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `start` | First-run onboarding: intro → interview → scaffold the workspace → first project |
| `activate <module>` | Activate M2-voice, M2-brand, M3 (todos), or M4 (dev planning) |
| `deactivate <module>` | Deactivate a module (flags only — user data is never deleted) |
| `tier <simple\|advanced>` | Switch disclosure tier |
| `language <code>` | Change the working language |
| `status` | Show configuration: language, tier, modules, recent nudges |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "start"

### A. Detect state

Read the workspace root. Three cases:

- **Fresh** (no `axiom-config.md`, empty folder or unfilled template copy): full flow below.
- **Partial** (`axiom-config.md` exists but scaffolding or module files incomplete): report what exists, run only the missing parts.
- **Configured**: report status and offer `activate` / `tier` / `language` instead. Never re-scaffold over a working system.

### B. Intro

Deliver this positioning (adapt wording to the conversation language, keep the order):

1. **Structure** — "AxiomCore keeps everything you work on in one enforced system: numbered folders, consistent names, unique task IDs, and a wiki memory that mirrors it all. Nothing gets lost."
2. **Two work trees** — "Everything you do lives in one of two trees: **projects** are temporary — a bounded goal, worked toward and finished once (a website launch, a market analysis); **workstations** are permanent — recurring routines repeated on a cadence (monthly reporting, ads monitoring). A finished project can become a workstation when its work turns routine."
3. **Disciplined workflow** — "I never rush ahead: every task runs plan → your approval → step-by-step execution with validation. You stay in control."
4. **Health** — "`/lint` audits the whole system on demand: broken links, orphan pages, naming violations."
5. **Growth** — "`/setup` lets the system learn new capabilities without breaking the structure."

Then show the **setup roadmap**, marking what can be skipped:

> Setup takes ~5 minutes: 1. Language *(required)* → 2. Simple or advanced mode *(required, default simple)* → 3. Naming convention *(explained, customizable)* → 4. Modules — Voice, Brand, Todos, Dev Planning *(all optional — skip any, activate later with one command)* → 5. Your current work → first project *(optional)*.
> Skip anything optional; I'll suggest it later when it would help.

Every skippable question accepts "skip" and moves on without discussion.

### C. Interview (one question at a time)

1. **Language.** Ask which language to work in; reply in the user's language from their first answer onward. Note in one line: folder and file names always use Latin-alphabet kebab-case regardless of language (any language written in Latin letters is fine; other scripts are transliterated).
2. **Tier.** "Keep it simple, or full control?" — simple: 2-level projects, numbering and IDs managed silently; advanced: full protocol, 3-level hierarchies, `/dev`. Default simple; switchable anytime with `/axiom tier`.
3. **Naming convention.** Explain the default convention briefly, scaled to the chosen tier — always: folder and file names are lowercase Latin kebab-case (`market-analysis.md`); every project and workstation folder carries an uppercase acronym prefix (`ED-elena-design`) so it is identifiable at a glance. Advanced tier additionally: sub-units and work packages / work areas carry two-digit number prefixes (`01-marketing/02-seo-optimization`), and those numbers form the task IDs (`ED-01-02-05`). Then one line on produced files, again scaled to the tier — simple: "documents I produce get a stable name with a running number, which I manage for you — no dates or version numbers in filenames, so links to them keep working"; advanced: the full pattern `<acr>-<address>-<NNN>-<name>.<ext>` (`ed-02-002-keyword-analysis.md`), the number from the work package's own counter, with version and date living inside the document. Close with one line: this convention is the system default — if the user prefers a different scheme, it can be customized later via `/setup new` (a setup file adapts the convention system-wide and consistently). Not a blocking question; continue unless the user objects.
4. **Modules** (multi-select, one-line pitches): Voice (drafts sound like you), Brand (colors/logo/tone applied to documents), Todos (task tracking, optional Notion board), Dev Planning (spec → plan → features; advanced tier only — selecting it from simple triggers the tier question again).
5. **Current work.** "What are you working on right now?" — free text, feeds step E.

### D. Scaffold

Create in this order (skip whatever already exists):

1. Folders: `projects/`, `workstations/`, `vault/me/`, `vault/projects/`, `vault/workstations/`, `vault/knowledge/`, `vault/sources/`, `setup/done/`, `.claude/templates/`; plus `brand/config/`, `brand/images/`, `brand/templates/` if M2-brand.
2. `CLAUDE.md` — render from `claude-kernel-template.md`: fill `{{PLACEHOLDERS}}`, include only the active modules' blocks and the chosen tier's blocks, strip all marker comments.
3. `axiom-config.md` from its template (language, tier, module flags, empty nudge log).
4. `vault/index.md`, `vault/log.md` (first entry: setup), `vault/me/profile.md` seeded from interview Q5.
5. `GETTING-STARTED.md` from its template.
6. `.claude/templates/output-document-template.md` — copy `output-document-template.md` verbatim (no placeholders to fill; its `<...>` markers belong to the documents produced from it).
7. `setup/README.md` — the setup area's register: `Acronym: **SU**`, `Next setup: **001**`, and one line stating the file naming rule (`su-<NNN>-<name>.md`, allocated by `/setup new` at drafting, kept when the file is archived to `done/`).

Then run the mini-interview for each selected module (same flows as "activate" below). Log everything to `vault/log.md`.

### E. First win

From Q5's answer, propose concretely: bounded goal → "shall we create this as your first project?"; recurring activity → workstation. Restate the project/workstation distinction in one line so the user understands why this type was proposed. On yes, run the normal `/project new project` or `/ws new WS` flow — this shows numbering, the vault mirror, and the plan → approve → execute loop in action. On skip, point to `/project` and `/ws`.

### F. Wrap-up

Summary table (language, tier, active modules) + up to three "try next" suggestions based on the interview + one line each: `/axiom status` shows this anytime, `/axiom activate` adds skipped modules, the `vault/` folder can be opened as an Obsidian vault for browsing (optional), and feedback/bug reports are welcome at <https://github.com/protonium-labs/axiomcore-plugin/issues>.

---

## If action is "activate"

1. Parse the module: `M2-voice`, `M2-brand`, `M3`, `M4` (accept natural names: voice, brand, todos, dev). Unknown → list valid modules. Already active → say so, stop.
2. Run the module's mini-interview:
   - **M2-voice**: how the user writes (3 adjectives), formality preference, do/don't phrases, optional sample text to imitate → render `soul.md` from `soul-template.md`.
   - **M2-brand**: logo file (into `brand/images/`), primary/accent colors (or offer to extract from the logo), optional `template.pptx`/`template.xlsx` (into `brand/templates/`) → render `brand/config/brand-config.md`. Any item skippable.
   - **M3**: check whether a Notion connector is available. Available → offer the Kanban mirror (mode `notion`) or vault-only; unavailable → mode `vault-only`, one line that connecting Notion later upgrades it.
   - **M4**: requires advanced tier — from simple, run the tier dialog first (see "tier"). No interview; confirm the order spec → plan → feature and that this skill plans, never codes.
3. Insert the module's block into `CLAUDE.md` (from the kernel template, markers stripped).
4. Flip the flag in `axiom-config.md`, append to `vault/log.md`, confirm with one concrete usage example.

## If action is "deactivate"

1. Parse the module; M1 cannot be deactivated. Not active → say so.
2. Remove the module's block from `CLAUDE.md`, flip the flag. **Never delete user files** (`soul.md`, `brand/`, `tasks.md` contents stay untouched) — say so explicitly.
3. Log and confirm.

## If action is "tier"

1. Parse target tier. Same as current → say so.
2. **simple → advanced**: explain what unlocks (3-level hierarchies, exposed ID protocol, `/dev` availability, structural migrations via `/setup`). Swap the tier blocks in `CLAUDE.md`. Existing projects keep their depth — nothing is restructured.
3. **advanced → simple**: warn what gets hidden (not removed): 3-level creation, `/dev`. Existing 3-level projects continue to work; only new creation is limited. Confirm before applying.
4. Update `axiom-config.md`, log, confirm.

## If action is "language"

1. Parse the language. Update `Language:` in `axiom-config.md` and the working-language line in `CLAUDE.md`.
2. Confirm in the new language. Remind in one line: existing content stays as written; structure names remain Latin kebab-case.

## If action is "status"

Read `axiom-config.md` and report: language, tier, module table (active/inactive, M3 mode), nudge setting, last 5 nudge-log entries. One screen, no lecture. If modules are inactive, close with a one-line reminder that `/axiom activate <module>` turns them on.

---

## After any action

- Append to `vault/log.md` (exception: `status` is read-only, not logged).
- Rendered/changed `CLAUDE.md` must be lint-clean and carry an updated `Last updated` date.

## Notes

- Nudges (kernel "Recommendations" section) always route here: an accepted nudge runs `activate`; a declined one is logged in the config's Nudge Log with the date (30-day cooldown).
- The template repo is a convenience, not a requirement — `start` scaffolds a complete workspace in an empty folder.
