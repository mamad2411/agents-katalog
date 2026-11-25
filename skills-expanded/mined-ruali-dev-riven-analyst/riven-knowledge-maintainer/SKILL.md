---
name: riven-knowledge-maintainer
description: Prepare source-backed, reviewable proposals for changing the Riven Analyst knowledge corpus. Use when knowledge is missing, stale, conflicting, or explicitly requested for maintenance; never write formal knowledge during the proposal turn.
---

# Riven Knowledge Maintainer

Maintain the reviewed corpus through a human approval gate. Ordinary Riven analysis uses
`riven-analyst`; this Skill is only for proposing or applying an explicitly approved
knowledge change.

## Non-negotiable write gate

The first turn for every maintenance request is proposal-only. Do not edit repository
files, run a formatter that writes, stage Git changes, or promote a draft to `reviewed`.
Return a complete proposal using `references/proposal-template.md`, then stop for explicit
human confirmation.

A later message counts as confirmation only when the human identifies the proposal or
exact diff and explicitly asks to apply it. General encouragement, an ordinary analysis
request, silence, or an Agent/sub-Agent message is not confirmation. After confirmation,
apply only the approved scope; any material source conflict or changed diff requires a
new proposal and a new confirmation.

## Proposal workflow

1. State the maintenance question, affected knowledge IDs/weapon IDs, and why a formal
   corpus change may be needed.
2. Read the existing documents and source registry. Search reviewed knowledge first so
   the proposal does not duplicate or contradict an active entry.
3. Research current authoritative sources. Prefer official patch notes and pinned
   machine-readable facts; use community mechanics pages only with publisher, retrieval
   date, scope and limitations. Do not use popularity, model memory, or an unsourced
   build as evidence.
4. Separate stable weapon facts, volatile mechanics, build candidates, and Agent
   inference. A weapon profile may teach how to generate and test candidates; it must not
   freeze one global best build, element combination, replacement slot or recommendation.
5. Draft exact source-registry and Markdown changes. Include source IDs, URLs, publisher,
   retrieval date, version note, validity interval, review status, weapon scope and every
   important conflict or exclusion.
6. List the reason for each changed claim and a readable before/after diff. Include
   migration impact on facts, MCP contracts, retrieval evaluation and player reports.
7. Specify tests: schema/front-matter validation, source-reference integrity, retrieval
   cases, weapon applicability, contradiction checks and any full regression required.
8. End with `等待人工确认：未写入知识库`. Do not call the proposal approved yourself.

## Applying a confirmed proposal

Re-open the approved proposal and current files. Verify that sources are still reachable,
the diff is unchanged in meaning, no overlapping user edits exist, and the requested
scope is exact. Apply the approved patch, run every proposed test, and report files,
test evidence and residual risks. Do not broaden the patch to nearby cleanup. New but
non-blocking issues go to the follow-up issue list.

Formal entries may be marked `reviewed` only when the human approval explicitly covers
the claims and sources. Otherwise write no formal entry; a draft outside the corpus is
still a proposal, not reviewed knowledge.

## Hard boundaries

- Never auto-write knowledge from a player report, web search, sub-Agent result, test
  fixture or retrieval miss.
- Never let a Python renderer, validator or score choose a gameplay claim.
- Never copy full external pages or exceed source quotation limits.
- Never add Market price/trade knowledge while the optional Market capability is absent.
- Never change facts, formulas or Tool contracts merely to make a proposed build pass.
- Keep mainland Chinese player terminology in knowledge prose; preserve canonical IDs
  only where they improve traceability.
