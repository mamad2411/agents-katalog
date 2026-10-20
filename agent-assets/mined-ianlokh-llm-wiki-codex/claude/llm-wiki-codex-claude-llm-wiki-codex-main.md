# Local Wiki Operating Rules (Claude Code)

This repository is a closed, Markdown-only knowledge base. Treat `wiki/**/*.md` as the only authority for factual answers. This file mirrors `AGENTS.md`; the two must stay in sync so the wiki behaves identically under Codex and Claude Code.

> New to any term used here? Plain-language definitions are in [GLOSSARY.md](GLOSSARY.md).

## Non-negotiable boundaries

- While ingesting, linting, or querying, do not go outside this repository — no web browsing, no external services, and no other outside information.
- Enforcement here is by **tool gating**: the role subagents in `.claude/agents/` are given no web tools, and the lint/query roles are given no write tools. Do not work around this by using the main session's broader tools to fetch, or to edit under a read-only role.
- Do not fill gaps from your own memory, general knowledge, or guesswork. If the wiki does not support an answer, say exactly: `Not found in the local wiki.` This applies to every answer taken from the wiki, and to all three roles. There is one narrow exception: once the wiki has been checked and has nothing, the main session may offer to answer from outside the wiki — but only with the user's permission, and never while acting as a role. See Roles and delegation for how that works.
- Back up every real answer with a link to the page it came from. Write it as a relative Markdown link pointing at the plain file path, with no `#anchor` on the end — e.g. `[wiki/concepts/attention.md — Key ideas](wiki/concepts/attention.md)`. Writing it as a link is what makes the citation clickable in the Markdown-rendering desktop apps this serves (Claude Desktop and the Codex/ChatGPT desktop app); leaving off the anchor keeps the target a real path that resolves to the page.
- Keep the repository Markdown-only. The only non-Markdown files allowed are configuration, not code: TOML/YAML under `codex/`, `.codex/agents/`, and `.agents/skills/**/agents/`; the Claude Code config under `.claude/` (`settings.json` and the agent/skill definitions); and a CI check under `.github/workflows/` that only guards repository rules (the skill mirror described under Skills). System tooling that Codex installs under `skills/.system/` is machine-managed and git-ignored, not project content.

## Domain configuration

Everything specific to your subject — the wiki's purpose, the allowed `tags:`, the `confidence` levels, and what counts as an entity vs. a concept — lives in one file, root `DOMAIN.md`. That is the single place you edit to point the wiki at a different subject area. These operating-rule files hold only the general rules that stay the same in every clone; look in `DOMAIN.md` for the subject-specific details, and edit only `DOMAIN.md` to retarget. `DOMAIN.md` is configuration, never evidence, and is never cited. All three roles read it (in both runtimes), so it actually steers their behavior rather than just describing it.

## Corpus contract

The pages the wiki can answer from are **evidence only**; anything that is not citable evidence lives outside `wiki/`.

- `wiki/concepts/` — published pages for ideas, methods, frameworks, or topics (lowercase, hyphenated). **Citable.**
- `wiki/entities/` — published pages for a specific named thing: a person, organization, product, tool, model, or place (lowercase, hyphenated). **Citable.**
- `wiki/sources/` — durable source records backing page claims. **Citable.**
- `wiki/index.md` — Map of Content, navigation only. **Never cite it.**
- `inbox/`, `templates/`, `reports/` — outside `wiki/`. **Never evidence.**

So the rule is simply: **evidence = `wiki/concepts/**`, `wiki/entities/**`, and `wiki/sources/**`.** `wiki/index.md` is the one in-wiki file that is never evidence.

- Before you write a new page, decide its kind: a **concept** explains how an idea or method works; an **entity** describes one named thing. When unsure, put topics in `concepts/` and named things that could carry their own fact-box in `entities/`.
- Every published page opens with a YAML frontmatter block: the keys are the same everywhere (defined in `templates/README.md`), and the allowed values come from `DOMAIN.md`. Frontmatter is information about the page, never evidence — never cite it; answer from the body. It sits above the H1 and does not affect the heading rule.
- Every published concept or entity page has exactly one H1, plus exactly one each of `## Summary`, `## Key ideas`, `## Sources`, `## Related`. Concept and entity pages use the same set; the folder says which kind a page is.
- Every `## Sources` entry links to a record in `wiki/sources/` or another published page, via relative Markdown links.
- Only add new material or make small corrections. Update `wiki/index.md` last, one page at a time.

### Fidelity and aggregation

A source record is a **faithful record of the input**, not a summary of it. The summarizing and simplifying happens later, on the concept/entity pages built on top — never by throwing away details in the source record itself. This is true for every kind of input: an article, a report, a news digest, a document, or a dataset.

- **Break it apart before you summarize.** *First* split each approved input into its separate, meaningful claims, and record each as its own bullet under a source record's `## What it asserts`, keeping the specifics that make a claim answerable — names, dates, quantities, and who said it — and its status (reported, rumored, confirmed, or established fact). Leave out filler: ads, navigation, markup, tracking, decorative captions.
- **Lose nothing important.** Any fact a reader could reasonably ask about must be recoverable from a source record. Boiling a multi-item input down to topic labels ("covers hardware rumors, pricing, and litigation") produces a table of contents, not evidence, and is a defect.
- **Match the level of detail to the input.** An input of N separate items yields N groups of claims, not one. Record the input's size and shape in the source record's `## Origin` (e.g. "a 17-story news digest", "a 200-row dataset") so that coverage is visible to a reader — and to linting, which cannot see the original input.
- **A bundled input never becomes one catch-all page.** When an input bundles many separate items (a news digest, a feed, a multi-finding report, a dataset), it becomes one source record capturing *all* items, plus a separate concept or entity page for each item substantial enough to fill the page schema. Lesser items stay citable as claims in the source record — do not manufacture thin stub pages, and do not create a single page whose `## Key ideas` is a list of unrelated topics.

## Roles and delegation (subagents)

Three subagents in `.claude/agents/` mirror the Codex roles. Invoke them with the Task tool.

Hand wiki work to the matching role instead of doing it yourself — even when the request needs only one role:

- A question to answer from the wiki → `wiki-query`. Do not answer wiki questions yourself. `wiki-query` is the only worker locked to read-only and to the wiki alone, and you give up that safeguard if you answer directly.
- A request to add, update, ingest, or process material → `wiki-ingest`. It finds its own approved input, so hand it off even when nothing is attached to the message — do not stall to ask for a paste.
- A request to check or audit the wiki → `wiki-lint`.

When a task needs more than one role (for example: ingest this note, lint it, then answer a question), hand each part to its role in turn rather than doing any of it yourself.

What to do when the wiki has no answer: when `wiki-query` replies `Not found in the local wiki.`, pass that reply on as-is first — do not quietly replace it with outside knowledge. After that, the main session (only the main session, never a role) may judge whether the question can be answered from general knowledge or current information. If it can, the main session may say so and offer such an answer — but it must not browse the web or bring in outside facts until the user explicitly agrees, and it must label any such answer as coming from outside the wiki, not from it.

| Role | Subagent | Tools granted | Enforces |
| --- | --- | --- | --- |
| Ingestion | `wiki-ingest` | Read, Write, Edit, Glob, Grep | Can write the corpus; no web |
| Linting | `wiki-lint` | Read, Glob, Grep | Read-only; reports findings |
| Query | `wiki-query` | Read, Glob, Grep | Read-only; wiki-only answers |

Ordering: ingestion must finish before linting the same page, and linting should pass before that page is queried. Only independent pages may be processed in parallel. Never point two writing subagents at the same page. Subagents must not spawn further subagents.

## Skills

The canonical skills live in `.agents/skills/{wiki-ingest,wiki-lint,wiki-query}/SKILL.md`, which Codex discovers automatically by location. Claude Code only reads skills under `.claude/skills/`, and git symlinks are not portable to Windows checkouts, so `.claude/skills/{wiki-ingest,wiki-lint,wiki-query}/SKILL.md` are **committed real-file copies** (mirrors) of the canonicals — not symlinks.

**Invariant:** each `.claude/skills/<role>/SKILL.md` must stay byte-identical to `.agents/skills/<role>/SKILL.md`. Edit the canonical under `.agents/skills/`, then copy it over the mirror:
- macOS/Linux: `cp .agents/skills/<role>/SKILL.md .claude/skills/<role>/SKILL.md`
- Windows PowerShell: `Copy-Item .agents/skills/<role>/SKILL.md .claude/skills/<role>/SKILL.md -Force`

`.github/workflows/skill-mirror.yml` enforces this on every push and pull request: it fails, with the exact copy command, if a mirror drifts from its canonical or is replaced by a symlink. The Claude subagents in `.claude/agents/` load their role skill by name via the `skills:` frontmatter field (which preloads the mirror from `.claude/skills/`), so no in-agent path reference is needed.
