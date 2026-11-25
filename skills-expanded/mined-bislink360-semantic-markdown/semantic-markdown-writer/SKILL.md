---
name: semantic-markdown-writer
description: Create and edit Semantic Markdown (.smd) documents (PRDs, ADRs, RFCs/design docs, runbooks, API references, status reports, meeting notes, postmortems, release notes, OKRs, onboarding guides, test plans, PR descriptions, specs and plans) with templates and a validator that fixes mistakes. Use it whenever the user asks to write, draft, create, convert, restructure or update a .smd file, asks for a spec/PRD/ADR/runbook/status report "in smd" or "semantic markdown", wants a Markdown doc converted to .smd, or wants a document that both people and AI agents will read.
---

# Writing Semantic Markdown (.smd)

`.smd` is Markdown plus a small, validated vocabulary: callouts, decisions, risks, API blocks, tasks with owners and due dates, KPIs, diagrams, and audience blocks. **People** read it in a styled preview, **AI agents** through a compact "agent view". Write for both.

Tool (Node 22+, no install): `node <this-skill-dir>/scripts/smd.cjs <command>` (or `smd` if it's on PATH).

## Workflow

1. **Start from a template** when one fits: `smd init docs/name.smd --template prd --title "Saved searches"` (today's date filled in; raw files in `assets/templates/`).

   | Request | Template |
   |---|---|
   | Product requirements, feature spec | `prd` |
   | Architecture/technical decision | `adr` |
   | Design proposal, RFC, tech spec | `rfc` |
   | On-call / operational procedure | `runbook` |
   | Endpoint reference | `api` |
   | Weekly/monthly update | `status-report` |
   | Meeting summary with actions | `meeting-notes` |
   | Incident review | `postmortem` |
   | Release announcement, upgrade guide | `release-notes` |
   | Objectives and key results | `okrs` |
   | New team member guide | `onboarding` |
   | Test scope, strategy and cases | `test-plan` |
   | Pull request description | `pr-description` |
   | Spec-driven work for an agent: spec → plan → tasks | `spec`, `plan`, `tasks` |

   Otherwise start from front matter + headings. For a status report on work tracked in `.smd` docs, draft it with `smd report docs/ --since 2026-09-01 -o docs/status.smd --title "Checkout squad"` (or `--since <git-ref>`): tasks done and added, open and overdue tasks, decisions and high-impact risks, each linked. Then write the summary and cut what doesn't matter.

2. **Fill it with real content.** Delete sections that don't apply; never leave placeholders such as `—`, `@owner` or `YYYY-MM-DD`. If you don't know a value, ask, or leave a `:::question` that says what's missing.

3. **Format, validate and fix:** `smd fmt docs/name.smd`, then `smd validate docs/name.smd --fix`. `fmt` changes only layout. `--fix` repairs what has one clear repair (typos in names and values, colors, `yes`/`no` booleans, date formats, unclosed `:::` or fences at the end). Fix the rest yourself from each error's line:column, message and rule code. **A document is done only at 0 errors.**

4. **Check what agents will see:** `smd agent docs/name.smd --brief`, then a partial view of the sections an agent would read (`--section "Requirements"`). Look at what each view leaves out, and at any `Not satisfied … for people only` line: a required dependency that agents can't see. If it's long, move narrative into `{agent=skip}` sections or `:::human` blocks, never an instruction agents need.

## Spend tokens on meaning

Output tokens cost about 5× input tokens. Write meaning: decisions, risks, tasks, `:::agent` rules, `{agent=skip}` on narrative. Leave colors, badges and layout (tabs, columns, cards) to people unless asked. The syntax reference is split by topic: read `references/syntax.md` (a short index), then only the topic file for the construct you're unsure of, and let `smd validate --fix` catch the rest.

## Rules you must follow

1. **Front matter first:** `smd: 2` (new documents; keep an existing document's value), `title`, a precise one- or two-sentence `summary`, `status` (`draft` · `review` · `approved` · `deprecated` · `archived`), `owners`, `updated` (`YYYY-MM-DD`). Don't repeat the title as a `# H1`; start at `##`. Another language adds `lang:` (`de`, `es`, `fr`, `ja`, `pt`, `zh`, or a tag like `pt-BR`).
2. **Blocks** are `:::name{attrs} Title` … `:::`. Attributes go directly after the name, no space. A bare `:::` closes the innermost block. Write outer containers with more colons (`::::tabs`).
3. **Only known names.** Blocks: `note` `info` `tip` `success` `warning` `danger` `question` `details` `card` `box` `tabs`/`tab` `columns`/`column` `steps` `timeline` `figure` `glossary` `quote` `decision` `risk` `risk-matrix` `changelog` `api` `agent` `human` `include` `requirement` `constraint` `acceptance` `assumption` `evidence` `non-goals` `example` `limitation` `deprecated` `comment` `suggestion`. Inline: `:badge` `:status` `:priority` `:due` `:metric` `:progress` `:kbd` `:mention` `:ref`, and in spec v2 `:depends` `:since`.
4. **Values exactly as specified:** decision `status` proposed · accepted · rejected · superseded · deprecated; risk `impact`/`likelihood` low · medium · high · critical; api `method` GET, POST… and a required `path`; priority P0–P4; dates `YYYY-MM-DD`. Figures, glossary, quotes and changelogs have their own forms (`syntax/figures-and-notes.md`, `syntax/project.md`).
5. **Named colors only** (red orange amber yellow green teal cyan blue indigo purple pink gray muted accent) unless a brand hex is required.
6. **Tasks:** `- [ ] Verb-first task :priority[P1] @owner :due[2026-10-15]`, one owner where possible.
7. **Code:** give fences a language; embed real source with `file="../src/x.ts" lines="10-24"` (empty body) instead of pasting it. Shared text goes in one file, pulled in with `:::include` (`syntax/developer.md`).
8. **Diagrams:** ```` ```mermaid ```` with a valid first line (`flowchart LR`, `sequenceDiagram`, `gantt`, …).
9. **Facts that repeat** (version, product name, date) go in the front matter once and appear as `{{version}}`. Quote versions (`version: "2.10"`; `syntax/inline.md`).
10. **Spec v2 shows text as written:** straight quotes stay straight (type `—` or add `typography: true`), only `https://…`, `www.…` and e-mail addresses become links, any `:name[…]` is a directive (`\:name[…]` is text). Don't change an `smd: 1` document's value while editing; `smd migrate FILE --to 2` moves it (`syntax/spec-v2.md`).

## Writing for both audiences

`references/style-guide.md` covers this in depth. In short:

- **Meaning over decoration.** Use `:::warning`, `:::danger` or `:::decision` for things that matter. Color must never be the only signal.
- **Hard constraints for implementers go in one `:::agent` block** near the end. Agents receive an agent-visible one even when they read a single section. One inside an `{agent=skip}` section or a `:::human` block is hidden with it.
- **Narrative, history and research go under `## Background {agent=skip}` or in `:::human`.** People still see it; agents never do, even when a read names that section, and no outline or task, risk or decision list mentions it. A `:::danger`, `:::constraint`, `:::requirement` or `:::agent` block inside it stays hidden too (`audience/rule-in-skip` and `container/agent-in-skip` warn), because the audience marker wins over the block kind.
- **Never let token savings hide an instruction agents need.** Keep operative instructions, applicable constraints, prerequisites and agent-relevant dangers outside `{agent=skip}` and `:::human`. Split a short visible warning or rule from its long human-only rationale instead of exposing the whole background. Use the ids, `scope`, `applies-to` and `depends-on` the syntax already has; there is no severity syntax, and `agent=skip` has no other form (no `agent=skip true`).
- **Keep what you hide on purpose.** A diagnostic only points at a hidden rule; you decide whether agents need it. Don't promote every hidden rule, and don't move content the user didn't ask you to change.
- **Unresolved decisions go in `:::question`**, with who decides and by when; the interim fallback goes in the `:::agent` block.
- **Requirements, constraints and acceptance criteria get their own blocks with ids** (`:::requirement{#R1}`, `:::constraint{#C1 scope=document}`, `:::acceptance{#AC1 verifies=R1}`), not tables. See `references/syntax/requirements.md`.
- **When a document is under review, propose changes as suggestions** (`smd review suggest <file> <id> --text … --by …`) instead of editing reviewed text. See `references/syntax/review.md`.
- **Headings name the content** ("Requirements", "API", "Rollout") because agents select sections by heading.
