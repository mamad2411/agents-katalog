---
name: vault-conventions
description: The house rules for THIS specific Obsidian vault (Danniel's) — the filing decisions, folder map, and conventions that say where an incoming note goes and how to write it. Use whenever capturing, writing, filing, converting, or routing any note into the vault (project notes, requirement docs turned into notes, meeting notes, daily notes, reusable patterns) so it lands in the right place with the right frontmatter and tags. Encodes the per-employer PARA nesting under Work/ with employer-scoped context (each employer's 3 Resources/ is its reusable reference layer), and the capture-vs-reference rule for Daily Notes/ and Meetings/ with on-demand promotion. Overrides the generic obsidian-vault skill wherever they differ; defers to obsidian-vault for maintenance workflows and to the official obsidian:* skills for authoring syntax.
---

# Vault conventions — this vault's house rules

The vault-specific policy layer for the vault at
`/Users/dannielibor/Documents/Obsidian Vault`. Where the generic `obsidian-vault`
skill knows how a *good* vault works in general, this skill knows how *this* vault
has decided to work. When you are about to write, file, or route a note here,
consult this first so it lands correctly.

## Precedence — how this fits the other skills

- **This skill wins on vault-specific decisions** — where a note goes, what
  frontmatter it carries, which tag marks it, how capture streams are handled.
  When it conflicts with a generic default, follow this skill.
- **Defer to `obsidian-vault`** for the *how* of maintenance — link hygiene, MOC
  build/refresh, orphan detection, frontmatter normalization, dedupe/rename, the
  link-safe move checklist. This skill sets policy; that skill executes it.
- **Defer to the official `obsidian:*` skills** for authoring syntax —
  `obsidian:obsidian-markdown` (wikilinks, callouts, properties, tags),
  `obsidian:obsidian-bases` (`.base`), `obsidian:json-canvas` (`.canvas`). Never
  restate syntax here.

## The vault map

```
Obsidian Vault/
├── CLAUDE.md                    vault guide for Claude Code
├── Work/                        career history + active work (memory + project KB)
│   ├── SN Aboitiz Power Group/  current employer — per-employer PARA inside
│   │   ├── 1 Projects/          deep project notes (business rules live here)
│   │   ├── 2 Areas/
│   │   ├── 3 Resources/         the employer's reusable reference — patterns,
│   │   │                        stack conventions, playbooks (used_in: links)
│   │   └── 4 Archive/
│   ├── _Past Employers/         former employers, preserved with their PARA sets
│   ├── Career Journey.md  ·  Work.md
├── Personal/                    single PARA set + Personal Documents/
├── Daily Notes/                 * capture stream — foldered YYYY/MM-Month
├── Meetings/                    * capture stream — foldered YYYY/MM-Month, company: key
├── Dashboard/                   Home + Claude Code status integration
└── _inbox/  ·  _templates/  ·  _attachments/
```

`*` = layers being established. If a survey doesn't find `Meetings/` or the dated
subfolders yet, **create them to this spec** rather than treating the vault as
convention-less. The per-employer nesting under `Work/` is deliberate and correct
— do not flatten it to satisfy textbook PARA. **There is no vault-level knowledge
layer by design** (a `Knowledge/` folder was tried and removed 2026-07-06):
context is employer-scoped, and each employer's `3 Resources/` is its reference
layer. Do not recreate a vault-level one.

## The three goals this vault serves

1. **Long-term memory** of all past and current work → `Work/`.
2. **Knowledge base** of every project worked on → project notes under each
   employer's `1 Projects/` (and `4 Archive/` when done).
3. **Reusable reference** across an employer's projects, pulled on demand only →
   that employer's `3 Resources/`.

All three goals live inside `Work/` — context never crosses employer boundaries.
A coding session wired to a repo (see the `project-context` skill) reads only its
employer's folder plus the capture streams filtered to that employer.

## Where a note goes — the decision

Ask in this order (full tree in `references/filing-decisions.md`):

1. **Is it a raw capture** (something said/decided today, unprocessed)? →
   `Daily Notes/` or `Meetings/`. It is a *log*, not reference. Do not file raw
   captures as reference notes.
2. **Is it about a specific project?** → that employer's
   `1 Projects/<Project>/`. Deep technical project notes live here.
3. **Is it a reusable pattern/convention/playbook** proven across more than one
   of an employer's projects? → that employer's `3 Resources/`. Link it back to
   the projects that used it via `used_in:`.
4. **Is it employment admin** (contract, payslip, onboarding)? → that employer's
   `3 Resources/`.
5. **Personal?** → `Personal/`.
6. **Unsure / quick dump?** → `_inbox/`, to be filed later.

## Capture vs. reference — the core mental model

`Daily Notes/` and `Meetings/` are **capture streams**: fast, chronological,
mostly ephemeral, written before you know what matters. They are raw material, not
reference. Project notes and each employer's `3 Resources/` are **reference**:
curated, topic-shaped, written with hindsight so future-you can reuse them.
Capture entries should name (or tag) the employer/project they belong to — meeting
notes carry a `company:` frontmatter key — so employer-scoped sessions can find
them.

**Promotion is on demand, not a ritual.** The preferred path is to write durable
material (a decision, a rule, a pattern that worked) *directly* into its permanent
home — the project note's Business Rules or the employer's `3 Resources/` —
either by hand or via a `project-context`-wired coding session's write-back. When
something does land in a capture stream first (a meeting decision, a daily-note
insight), promote it when you notice it or when asked: lift it into the right
employer's project note or `3 Resources/`, leaving the capture note in place as
the timestamped record. There is no scheduled sweep and no special carry-forward
tag — keepers are found by reading the capture note (or its `## Decisions`
heading), not by tag query.

## Frontmatter conventions

- **Project notes** carry rich frontmatter — observed keys: `tags`, `company`,
  `client`, `end_client`, `role`, `status` (`active`/`completed`), `stack`,
  `repo`, `created`, `updated`. Start from `_templates/Project.md`.
- **Daily notes** from `_templates/Daily Note.md`; **meeting notes** from
  `_templates/Meeting.md`.
- **Employer reference notes** (patterns/conventions/playbooks in `3 Resources/`)
  carry a type tag (`pattern`/`stack`/`playbook`) and a `used_in:` list of
  `[[wikilinks]]` to that employer's projects that prove the pattern.
- **Meeting notes** carry a `company:` key naming the employer, so
  employer-scoped sessions can filter the capture stream.
- **MOC/index notes** are named after their folder and tagged `moc`, embedding a
  Dataview (or Bases) query rather than a hardcoded list.

## References

- **`references/filing-decisions.md`** — the full where-does-it-go decision tree,
  the meeting-note lifecycle, the requirement-PDF-to-notes workflow, on-demand
  promotion, and the employer reference-note types with the `used_in:` convention.

For authoring syntax defer to the official `obsidian:*` skills; for maintenance
workflows defer to `obsidian-vault`.
