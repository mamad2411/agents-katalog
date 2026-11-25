---
name: online-research
description: Research a question against external sources, bypassing the local-library check.
disable-model-invocation: true
---

# familiar — Online Research

The user has explicitly selected external research. Apply `CORE-GROUND` by identifying external
claims and citing their sources; do not load unrelated local or extension libraries merely to
justify the selected route.

## Context contract

- **Required context:** `.familiar/core/voice.md`, `.familiar/core/plain-language.md`, `.familiar/core/file-handling.md`, the research question and an active external-retrieval capability
- **Conditional context:** project scope for terms or exclusions, and prior research pages only when checking freshness or change.
- **Excluded context:** Other projects, undeclared extension content, and project areas not required or conditionally triggered here.
- **Updates:** `nothing` unless the user says to file — then one page in `3-Knowledge/` and one gap task in `4-Trackers/tasks.md`
- **Capabilities:** file-read, file-write, external-retrieval. Optional capabilities must degrade as the procedure states.
- **Completion:** The answer or filed page distinguishes retrieved findings, source owners, access dates, locators, and unresolved retrieval gaps.


The route selection covers only the question asked. Later questions return to normal route
selection.

## Procedure

1. **Dispatch `web-lookup`**, not raw `WebSearch`/`WebFetch` in this session. The agent is
   domain-neutral — say in the dispatch who the primary-source owner is for what's being asked (the
   agency, the journal, the public registry, the statistical office: the body that owns the fact, not
   a write-up of it). Running the search in this session instead keeps every fetched page resident in
   context for the rest of the conversation; the agent's isolated context is what makes it affordable.
2. Answer from the agent's returned quotes, **citing each claim** with source and locator (URL plus
   section, page, or table). Do not paraphrase a quote into something smoother — the agent already
   gives you verbatim text with citations attached.
3. **Read COVERAGE and GAPS before answering.** A `not-retrievable` item is not a finding; say so
   rather than treating silence as absence. **Flag what you could not verify** — a gap stated is
   useful, a gap closed by inference is a fabrication (`CORE-NO-FABRICATION`).
4. **A document the agent could not fetch (paywall, JS-rendered page) is a real gap, not a signal to
   route around it with ad-hoc tooling in this session.** Say what was not retrievable and why; ask
   the user before trying a manual workaround.
5. **Offer to file — do not file.** Ask once, in one line, whether the finding is worth keeping.
   Default is no: most research answers a question in the moment and does not deserve a page.

## If the user says yes, file it

Use `3-Knowledge/_page-template.md` and stamp the exact model ID, reasoning effort, and generation
date per `file-handling.md` → AI runtime provenance. A host that does not expose a runtime value is
recorded as `not exposed`, never guessed.

One page into `3-Knowledge/`, named per `file-handling.md` → Naming and copies, added to
`_knowledge-index.md`. Mark it **external-sourced** in the title line so it is never mistaken for a
page compiled from the project's own documents.

Mandatory first line of the page:

> **Why external:** <what was asked, and why the local library does not answer it>

If the finding you filed carries any `not-retrievable` item, also file **one** task in
`4-Trackers/tasks.md` per `file-handling.md` → Grounding and provenance — a filed page with an unresolved
retrieval gap needs a tracked blocker, the same as any other external-sourced page. Carry the
`url` field from the agent's `FINDING` block into the page's Gaps section for every such item
(`file-handling.md` → Grounding and provenance) — the reason alone ("paywalled", "402") does not tell a
human what to open by hand to retrieve it.

That line is the audit trail, and it tells the maintainer when a document is missing from an
installed extension's knowledge library.

## Guardrails

- If the local library plainly *does* cover the question, say so in one line and let the user decide
  before you search. Invoking this skill is the user's judgement, not a licence to skip a source that
  exists.
- Do not give regulatory, legal or financial advice — report what the source says (`bootstrap.md` → CORE-GROUND).
- Use the shape and language declared by the project (`voice.md` → Default).
- A `web-lookup` finding without a verbatim quote and URL is unsourced. Mark it `[verify]`
  (`voice.md` → Uncertainty marker) rather than presenting it at the same confidence as a quoted
  one, and say how many you left.
