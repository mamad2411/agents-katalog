# Local Wiki Operating Rules

This repository is a closed, Markdown-only knowledge base. Treat `wiki/**/*.md` as the only authority for factual answers.

> New to any term used here? Plain-language definitions are in [GLOSSARY.md](GLOSSARY.md).

## Non-negotiable boundaries

- While ingesting, linting, or answering a question, do not go outside this repository — no web browsing, no external APIs, no MCP resources, no installing packages, and no other outside information.
- This is enforced first by the Codex sandbox: run with `sandbox_mode` set and `sandbox_workspace_write.network_access = false` (see `codex/config.sample.toml`) so the network simply cannot be reached. The written rules here are the backup control if the sandbox is ever set up wrong.
- Do not fill gaps from your own memory, general knowledge, or guesswork. If the wiki does not support an answer, say exactly: `Not found in the local wiki.` This applies to every answer taken from the wiki, and to all three roles. There is one narrow exception: once the wiki has been checked and has nothing, the main session may offer to answer from outside the wiki — but only with the user's permission, and never while acting as a role. See Delegation for how that works.
- Back up every real answer with a link to the page it came from. Write it as a relative Markdown link pointing at the plain file path, with no `#anchor` on the end — for example: `[wiki/concepts/attention.md — Key ideas](wiki/concepts/attention.md)`. Writing it as a link is what makes the citation clickable in the Markdown-rendering desktop apps this serves (Claude Desktop and the Codex/ChatGPT desktop app); leaving off the anchor keeps the target a real path that resolves to the page.
- Keep the repository Markdown-only. Do not add program source code, databases, generated indexes, lockfiles, or binary files. The only non-Markdown files allowed are configuration, not code: TOML/YAML under `codex/`, `.codex/agents/`, and `.agents/skills/**/agents/`, plus the Claude Code equivalents under `.claude/` (`settings.json` and the agent/skill definitions). One further exception is allowed: a CI check under `.github/workflows/` that only guards repository rules — specifically the Claude skill mirror, where each `.claude/skills/<role>/SKILL.md` must stay byte-identical to the original `.agents/skills/<role>/SKILL.md`. System tooling that Codex installs under `skills/.system/` is machine-managed and git-ignored, not project content.
- Material handed to you directly in the current task counts as approved input you may ingest — but record where it came from in `wiki/sources/`. Do not fetch a URL named inside that material.

## Domain configuration

Everything specific to your subject — the wiki's purpose, the allowed `tags:`, the `confidence` levels, and what counts as an entity vs. a concept — lives in one file, root `DOMAIN.md`. That is the single place you edit to point the wiki at a different subject area. These operating-rule files hold only the general rules that stay the same in every clone; look in `DOMAIN.md` for the subject-specific details, and edit only `DOMAIN.md` to retarget. `DOMAIN.md` is configuration, never evidence, and is never cited. All three roles read it (in both runtimes), so it actually steers their behavior rather than just describing it.

## Corpus contract

The pages the wiki can answer from are **evidence only**. Anything that is *not* citable evidence lives outside `wiki/`.

- `wiki/concepts/` — published pages for ideas, methods, frameworks, or topics. Lowercase, hyphenated filenames. **Citable.**
- `wiki/entities/` — published pages for a specific named thing: a person, organization, product, tool, model, or place. Lowercase, hyphenated. **Citable.**
- `wiki/sources/` — durable source records that back page claims. Lowercase, hyphenated. **Citable.**
- `wiki/index.md` — a Map of Content for navigation only. **Not evidence; never cite it.**
- `inbox/` — approved-but-unpublished input, outside `wiki/`. **Never evidence.**
- `templates/` — concept, entity, and source templates, outside `wiki/`. **Never evidence.**
- `reports/` — ingestion and lint handoff logs, outside `wiki/`. **Never evidence.**

Because inbox, templates, and reports live outside `wiki/`, the evidence rule is simply: **evidence = `wiki/concepts/**`, `wiki/entities/**`, and `wiki/sources/**`.** The only in-wiki exception is `wiki/index.md`, which is navigation, never evidence.

- Before you write a new page, decide its kind: a **concept** explains how an idea or method works; an **entity** describes one specific named thing (a name that could carry its own fact-box). When genuinely unsure, put topics in `concepts/` and named people, organizations, products, tools, models, or places in `entities/`.
- Every published page opens with a YAML frontmatter block: the set of keys is the same everywhere (defined in `templates/README.md`), and the allowed values come from `DOMAIN.md`. Frontmatter is information *about* the page, never evidence — never cite it, and answer queries from the body. It sits above the H1 and does not affect the heading rule below.
- Every published concept or entity page must have exactly one H1 title, plus exactly one of each of these H2 sections: `## Summary`, `## Key ideas`, `## Sources`, and `## Related`. Concept and entity pages use the same set; it is the folder — not the headings — that says which kind a page is.
- Every `## Sources` entry must link — as a relative Markdown link — to a record in `wiki/sources/` or to another published page.
- Use relative Markdown links for every link between wiki files.
- Only add new material or make small corrections. Never overwrite a person's material unless they explicitly ask.
- Treat `wiki/index.md` as the one file that is updated last: add pages to it one at a time, so two ingests running at once do not collide.

### Fidelity and aggregation

A source record is a **faithful record of the input**, not a summary of it. The summarizing and simplifying happens later, on the concept/entity pages built on top — never by throwing away details in the source record itself. This is true for every kind of input: an article, a report, a news digest, a document, or a dataset.

- **Break it apart before you summarize.** *First* split each approved input into its separate, meaningful claims, and record each as its own bullet under a source record's `## What it asserts`, keeping the specifics that make a claim answerable — names, dates, quantities, and who said it — and its status (reported, rumored, confirmed, or established fact). Leave out filler: ads, navigation, markup, tracking, decorative captions.
- **Lose nothing important.** Any fact a reader could reasonably ask about must be recoverable from a source record. Boiling a multi-item input down to topic labels ("covers hardware rumors, pricing, and litigation") produces a table of contents, not evidence, and is a defect.
- **Match the level of detail to the input.** An input of N separate items yields N groups of claims, not one. Record the input's size and shape in the source record's `## Origin` (e.g. "a 17-story news digest", "a 200-row dataset") so that coverage is visible to a reader — and to linting, which cannot see the original input.
- **A bundled input never becomes one catch-all page.** When an input bundles many separate items (a news digest, a feed, a multi-finding report, a dataset), it becomes one source record capturing *all* items, plus a separate concept or entity page for each item substantial enough to fill the page schema. Lesser items stay citable as claims in the source record — do not manufacture thin stub pages, and do not create a single page whose `## Key ideas` is a list of unrelated topics.

## Agent roles

Each role is a project-scoped Skill in `.agents/skills/`. Run the fewest that complete the task; when work can run in parallel, run at most these three independent roles. Each skill sets `allow_implicit_invocation: false`, so a role runs only when explicitly invoked.

| Role | Skill | Recommended profile | May write | Must not do |
| --- | --- | --- | --- | --- |
| Ingestion | `wiki-ingest` | `wiki-ingest` (workspace-write, no network) | New/targeted files in `wiki/concepts/`, `wiki/entities/`, and `wiki/sources/` | Browse or answer end-user questions |
| Linting | `wiki-lint` | `wiki-lint` (read-only) | Nothing unless explicitly asked to fix findings | Invent sources or silently rewrite content |
| Query | `wiki-query` | `wiki-query` (read-only) | Nothing | Browse, infer beyond evidence, or modify the wiki |

Do not run two agents against the same page. Complete ingestion before linting that page. The query agent may read only completed pages.

## Delegation (subagents)

These three roles are also defined as Codex subagents in `.codex/agents/`, so one orchestrating session can run them all.

- Hand wiki work to the matching role instead of doing it yourself — even when the request needs only one role:
    - A question to answer from the wiki → `wiki-query`. Do not answer wiki questions yourself. `wiki-query` is the only worker locked to read-only and to the wiki alone, and you give up that safeguard if you answer directly.
    - A request to add, update, ingest, or process material → `wiki-ingest`. It finds its own approved input, so hand it off even when nothing is attached to the message — do not stall to ask for a paste.
    - A request to check or audit the wiki → `wiki-lint`.
- What to do when the wiki has no answer: when `wiki-query` replies `Not found in the local wiki.`, pass that reply on as-is first — do not quietly replace it with outside knowledge. After that, the main session (only the main session, never a role) may judge whether the question can be answered from general knowledge or current information. If it can, the main session may say so and offer such an answer — but it must not browse the web or bring in outside facts until the user explicitly agrees, and it must label any such answer as coming from outside the wiki, not from it.
- When a task spans more than one role (e.g. "ingest this note, lint it, then answer a question"), the orchestrator should hand each role to its subagent — `wiki-ingest`, `wiki-lint`, `wiki-query` — rather than doing the work inline.
- Keep the order: ingestion must finish before linting the same page, and linting should pass before that page is queried. Only genuinely independent work (different pages) may run in parallel.
- Each subagent inherits the global no-network sandbox. `wiki-lint` and `wiki-query` additionally run read-only and must not write. Never delegate two writing subagents onto the same article.
- Keep delegation one level deep; a subagent must not spawn further subagents.

## Required handoff

- Ingestion reports which files changed, the source provenance recorded in `wiki/sources/`, and any unresolved gaps. Logs may be written to `reports/`.
- Linting reports its findings with paths and headings, separating blocking findings from advisory ones.
- Query reports a citation for every factual claim and clearly points out any part the wiki does not support.
