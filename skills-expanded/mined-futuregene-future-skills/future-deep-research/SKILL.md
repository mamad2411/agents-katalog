---
name: future-deep-research
version: 3.0.1
description: >
  Evidence-driven deep research using web, academic papers and user materials.
  Produce a full research report, a delegated methods brief, or an incremental update;
  trace claims to sources, verify key citations, and report gaps and resource use.
  Use for deep research, literature reviews, industry or technology analysis, research
  reports, and methods research delegated by future-explore. Not for editing this skill
  itself or ordinary single-fact lookups.
metadata:
  requires:
    bins: [future]
  orchestrates:
    - future-web
    - future-paper
    - future-document
    - future-browser
    - future-image
category: methodology
allowed-tools: Bash(future:*)
---

# Deep Research — Find, Read, Verify, Synthesize

Answer the requested questions with traceable evidence within the authorized scope and
budget. A polished report, many URLs, or a model's confidence score is not proof.

## Non-negotiable rules

- Read relevant source content, not just search snippets or generated summaries.
- Distinguish original evidence, secondary analysis, and copies. Agreement between
  reposts is not independent corroboration.
- Resolve, remove, or explicitly qualify unsupported key claims. Do not average a
  failed key citation away with several successful checks.
- Preserve user questions when evidence is missing; search results may refine the
  outline but cannot silently replace the user's objective.
- Respect authorization, data boundaries, and the allocated budget. Return partial
  work when necessary; never silently relax a promised deliverable or invent evidence.

## 1. Establish the research contract

Read `references/delegation.md` at entry, including for standalone work.

Choose independently:
- **Entry:** standalone request or delegated subtask with an existing authorization record.
- **Deliverable:** `report` (full narrative report), `methods` (bounded decision brief),
  or `delta` (update to identified existing work).
- **Depth:** A / B / C, selected below. A narrow question can still require deep reading.

Reuse explicitly confirmed fields. Ask once for missing or changed requirements;
when a new outline changes scope, permissions, cost, or the agreed deliverable, ask
about that change rather than repeating the original strategy/model questionnaire.
Do not treat caller proposals or silence as user authorization.

Record questions, non-goals, sources/data permissions, language, deliverable, depth,
limits, output location, confirmation basis and any pending decisions. Standalone
requests normally receive an A/B/C recommendation and choice unless already specified.
For delegated work, inherit valid approval and the **subtask allocation**, not the
parent's entire budget. Do not launch workers or change models without authorization.

## 2. Select depth and check feasibility

| Depth | Research approach | Full-report reference range |
|---|---|---|
| A — Quick scan | Targeted search, read passages needed for key claims, expose gaps | 5–15 |
| B — Broad research | Compare routes/sources, inspect primary evidence for central claims | 20–40 |
| C — Deep analysis | Deep-read decisive sources, examine methods, counterevidence and limitations | 60–120 |

The full-report citation and source-composition requirements are specified in
`references/reporting.md`; retain their role in preventing thinly sourced reports.
Do not pad a bibliography. For `methods`/`delta`, explicitly agree a question/evidence
coverage contract instead of automatically requiring a full-report bibliography.
Never relabel an underfilled report as a methods brief after the fact.

All depths require key-claim verification. Depth changes breadth and analytical effort,
not permission to fabricate or skip a decisive source. Data analysis is conditional on
relevant data and the question, not mandatory just because C was chosen. Treat duration
as an estimate covering discovery, reading, verification and writing, not a 3-minute promise.

## 3. Collect and map evidence

Read `references/retrieval.md` before collection and `references/evidence.md` before
extraction or verification.

1. Inspect user materials and existing reports first. Record provenance and permitted
   processing. Reuse sufficiently current, relevant, verified evidence; describe reuse
   without claiming a fresh search occurred.
2. Do bounded reconnaissance where coverage is missing: search, open useful sources,
   and identify methods, terms, disagreements and blind spots. A supplied source set
   can support reconnaissance; new web searches are not ceremonial requirements.
3. Map each **user question** to evidence needs and sources. Keep unanswered questions
   in the map. Label newly discovered questions as proposals, and confirm material scope changes.
4. Retrieve the needed passages/full text, recording source cards and versions. Cache
   usable retrievals; refetch only for missing content, changed versions, freshness
   requirements or failed verification. Source length alone is not an adequacy test.
5. Compare original evidence and genuinely distinct analyses. Follow important claims
   to their origin and actively look for counterevidence and applicability limits.

Use the relevant skills rather than duplicating their interfaces:
- `future-web`: search and URL retrieval; `future-paper`: academic search and body text.
- `future-document`: authorized PDF/Word processing; `future-browser`: retrieval fallback.
- `future-image`: authorized OCR/chart reading when needed, not decorative output by default.

## 4. Verify and decide whether to retrieve more

- Maintain a claim-to-evidence record with support, contradiction, uncertainty and
  source lineage. A source's accessibility, authority and support for a particular
  claim are separate questions.
- Check every key claim against the relevant original passages, including qualifications,
  units, dates and conditions. Generated summaries are discovery aids, not substitutes.
- If a key citation fails, repair its support, revise/remove the claim, or label it
  unresolved and restrict the conclusion. Even one failed decisive citation matters.
- Additional citation sampling can check less central material; it cannot replace key
  claim checks at any depth. Disclose what was and was not checked.
- Use the single retrieval budget and retry ledger in `references/retrieval.md`. Stop
  when the agreed coverage is met and further retrieval is unlikely to change the
  answer, or when a limit is reached. Never require three backfill rounds before stopping.

Self-review is a checklist, not a calibrated correctness probability. Do not use a
self-assigned score such as 0.75 as a pass threshold. Independent review, if required by
the contract, must actually happen and its shared dependencies must be disclosed.

## 5. Synthesize, finalize and return

Follow `references/reporting.md` for the chosen deliverable. Explain the reasoning,
trade-offs, evidence strength and remaining unknowns; do not merely stack tables or URLs.

Check the **final written claims**, since drafting can introduce unsupported statements.
Record corrections and the source/claim IDs affected. Only report successful saves
and checks after they occur. Use a unique run/revision suffix as well as a date to avoid
same-day overwrites. Do not overwrite user materials or unrelated reports.

Return the common receipt defined in `references/delegation.md`: artifact paths,
actual scope/depth, coverage, evidence limitations, resource use and stop reason.
A completed retrieval run is not automatically a verified answer or the parent goal's success.

Give concise progress at meaningful transitions: scope/authorization settled, evidence
collected, important gap/conflict, and delivery. Include only real counts. Delegated
progress is addressed to the orchestrator and can be consolidated; do not repeatedly
interrupt the user with a second full workflow.

## Resources

- `references/delegation.md` — entry, inherited approval, subtask limits, reuse and return contract.
- `references/evidence.md` — source cards, lineage, claim verification and failure handling.
- `references/retrieval.md` — tools, cache, browser fallback, privacy, budget and backfill.
- `references/reporting.md` — complete-report requirements and methods/delta deliverables.

## Validation after changing this skill

Run `python3 tests/check_skill.py` offline. With authorized model/tool use, add
`--model <model-id>` for one ephemeral, no-tools decision test; add `--live-source`
for a bounded public-source retrieval check. These checks do not prove end-to-end
research quality, real billing enforcement or multi-worker cancellation behavior.
