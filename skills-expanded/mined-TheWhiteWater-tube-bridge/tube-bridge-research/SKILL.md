---
name: tube-bridge-research
description: "Operate tube-bridge as a coherent YouTube research system: frame questions, discover sources, select subtitle tracks, classify claims, test competing hypotheses, capture timestamped evidence, build and search local corpora, and report traceable conclusions. Use for evidence-oriented YouTube research, transcript analysis, source comparison, fact-checking, or living corpus work."
---

# Tube Bridge Research

This is the single entry point for the MCP, research method, corpus doctrine, examples, and reusable templates. Treat tube-bridge as one research capability rather than a bag of unrelated tools.

## Select the research mode

- **Quick lookup:** one bounded fact about a source; use explicit language and timestamp provenance without manufacturing hypotheses.
- **Focused study:** one source or tightly bounded question; use FRAME-LOCK and claim classification.
- **Comparative investigation:** disputed, causal, or multi-source question; require source lineage, competing hypotheses, and adversary review.
- **Living corpus:** repeated monitoring; additionally preserve state snapshots, update traces, review intervals, and resolution criteria.

Read [references/methodology/00-research-method.md](references/methodology/00-research-method.md) before a focused, comparative, or living investigation.

## Non-negotiable rules

- Keep OBSERVATION, FACT, SOURCE-CLAIM, INFERENCE, and UNKNOWN distinct.
- Freeze a timestamped `frame_id` before evidence retrieval. Changed questions, standards, applicability, or materiality create a new prospective run; they never rewrite the old verdict.
- Treat a timestamped transcript as tool-observed evidence of what the selected subtitle track renders. Generated, translated, or dubbed text is not automatic proof of exact speech, speaker endorsement, or a world claim.
- Check available subtitle tracks and pass `lang` explicitly whenever the intended language can be established. With `lang=None`, v1.1.0 deterministically stays in the first ASR/default language family and never crosses into an unrelated manual dub; explicit selection still gives stronger provenance.
- Preserve video identity, requested and returned language, track type, timestamp spans, retrieval warnings, and upstream source lineage.
- Count independent observation paths, not videos. Several videos can repeat one origin.
- Verify corpus hits against source transcript text. Similarity scores rank candidates; missing hits do not prove absence.
- For causal or predictive questions, keep competing mechanisms and seek distinguishing evidence.
- Attack the leading explanation before synthesis. Core frame, provenance, confidence, and stopping checks are mandatory-material. A gate PASS means fit to present, not certainly true.
- Do not claim that Corpus v2 hierarchy, dual representation, lexical search, or logical relations exist in the released runtime. Current corpus behavior is flat overlapping-window vector retrieval.
- Do not fabricate unavailable transcripts, speaker identities, frames, provenance, certainty, or narrative glue.

## Canonical workflow

1. **Orient.** On first use or after an upgrade, follow [references/START_HERE.md](references/START_HERE.md).
2. **Frame.** Lock object, current question, process/verdict register, time/language boundary, evidence standard, available-tool verification boundary, non-goals, and stop rule.
3. **Map.** Identify candidate sources, actors, dates, claims, upstream origins, and gaps before writing a conclusion.
4. **Capture.** Select the intended subtitle track and collect timestamped source observations.
5. **Inventory.** Classify material as OBSERVATION, FACT, SOURCE-CLAIM, INFERENCE, or UNKNOWN.
6. **Hypothesize when needed.** Create competing mechanisms with falsifiers and distinguishing predictions for explanatory work.
7. **Retrieve to discriminate.** Search for the evidence most likely to separate branches, not merely more material.
8. **Adversary gate.** Check frame, source lineage, arithmetic, alternatives, actor assumptions, physical feasibility, incentives, and negative-evidence preconditions.
9. **Synthesize.** Answer the locked question with evidence spans, confidence reasons, surviving alternatives, UNKNOWNs, and change conditions.
10. **Update.** Preserve prior state and append an explicit trace when new evidence changes the view.

## Methodology map

| Need | Canonical resource |
|---|---|
| End-to-end modes, FRAME-LOCK, inventory, hypotheses, synthesis, and state updates | [references/methodology/00-research-method.md](references/methodology/00-research-method.md) |
| Claim classes, source lineage, independence, provenance, negative evidence, and corpus admissibility | [references/methodology/01-evidence-protocol.md](references/methodology/01-evidence-protocol.md) |
| Five attacks, audit verdicts, stop rules, updates, resolution, and calibration | [references/methodology/02-adversary-gates.md](references/methodology/02-adversary-gates.md) |

## Operational and corpus references

| Need | Canonical resource |
|---|---|
| Why the plugin is one bounded research system | [references/00-operating-model.md](references/00-operating-model.md) |
| Select among the 17 source-tree MCP tools | [references/10-tool-selection.md](references/10-tool-selection.md) |
| Capture the intended subtitle source safely | [references/20-source-capture.md](references/20-source-capture.md) |
| Implement the frozen Corpus v2 authority, versioning, and rebuild contract | [references/30-corpus-storage.md](references/30-corpus-storage.md) |
| Apply the executable Corpus v2 SQLite DDL | [assets/contracts/corpus-v2-schema.sql](assets/contracts/corpus-v2-schema.sql) |
| Design normalization and semantic processing within the frozen storage envelope | [references/40-corpus-processing.md](references/40-corpus-processing.md) |
| Choose direct, vector, temporal, or hybrid retrieval | [references/50-retrieval.md](references/50-retrieval.md) |
| Benchmark processing and retrieval changes | [references/60-evaluation.md](references/60-evaluation.md) |
| Resolve common operational questions | [references/FAQ.md](references/FAQ.md) |
| Interpret shared terminology | [references/GLOSSARY.md](references/GLOSSARY.md) |

## Worked examples

These examples are synthetic and teach method rather than asserting real-world facts:

- [references/examples/01-one-video-source-capture.md](references/examples/01-one-video-source-capture.md) — explicit subtitle language and SOURCE-CLAIM separation.
- [references/examples/02-shared-origin-is-not-independence.md](references/examples/02-shared-origin-is-not-independence.md) — three videos, one upstream origin.
- [references/examples/03-absence-is-not-negative-evidence.md](references/examples/03-absence-is-not-negative-evidence.md) — why an absent corpus hit remains UNKNOWN.

## Templates

| Artifact | Template |
|---|---|
| Bound question and evidence contract | [assets/templates/research-brief.md](assets/templates/research-brief.md) |
| Canonical living session state | [assets/templates/research-state.md](assets/templates/research-state.md) |
| Source, claim, lineage, and timestamp record | [assets/templates/evidence-ledger.md](assets/templates/evidence-ledger.md) |
| Competing mechanisms and distinguishing predictions | [assets/templates/hypothesis-matrix.md](assets/templates/hypothesis-matrix.md) |
| Independent method audit | [assets/templates/adversary-gate.md](assets/templates/adversary-gate.md) |
| Immutable old-view → new-view trace | [assets/templates/update-record.md](assets/templates/update-record.md) |
| Evidence-led final answer | [assets/templates/final-synthesis.md](assets/templates/final-synthesis.md) |
| Multi-source comparison | [assets/templates/source-comparison.md](assets/templates/source-comparison.md) |
| Retrieval and processing benchmark | [assets/templates/corpus-evaluation.md](assets/templates/corpus-evaluation.md) |

## Completion gate

Before presenting a consequential conclusion, confirm:

- FRAME-LOCK still describes the answer being delivered;
- every decisive statement has a claim class and provenance;
- source lineage and actual independence have been checked;
- timestamp and subtitle-track provenance are retained;
- competing explanations received a distinguishing test where the question required them;
- corpus hits returned to source text and missing hits were not treated as absence without an observation contract;
- arithmetic, actor assumptions, physical constraints, and incentives survived adversarial review;
- confidence, surviving alternatives, UNKNOWNs, and stop conditions are explicit;
- current runtime behavior is not confused with the frozen but not-yet-implemented Corpus v2 contract.
