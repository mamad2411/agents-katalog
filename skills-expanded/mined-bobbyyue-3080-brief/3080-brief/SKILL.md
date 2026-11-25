---
name: 3080-brief
description: Create a new source-grounded decision brief in Feishu/Lark, Word/docx, Markdown or self-contained HTML; default to source format. Include a reader-fit Pyramid opening, one editable or auditable visual covering at least 80% of value-weighted non-appendix claims, and a key-question table. Use for 3080-brief, 3080 brief, 3080skill, 读者视角总结, 3080总结, 3080summary, 3080-onepager, or reader-perspective/cross-functional briefs requesting a 30-second takeaway and one-picture summary. Do not use for editing or polishing sources, generic summary without a 3080/reader/visual requirement, or standalone whiteboard styling. Preserve the source and ground claims in it.
---

# 3080 Brief

**30-second judgment, 80% in one picture**

## Output Contract

Open with `TLDR`, containing exactly three core units:

1. **一句话 / one-sentence judgment**: one highest-level judgment on the first line, followed only when needed by 1–3 short evidence, action, or boundary lines; the whole unit must work within 30 seconds.
2. **一张图 / one-picture summary**: one auditable visual covering at least 80% of value-weighted non-appendix claims; Feishu/Lark uses an editable whiteboard.
3. **一个表 / one key-question table**: 3–5 source-grounded questions with `问题 / 结论 / 为什么` or `Question / Conclusion / Why`.

Title the new artifact `3080 Brief｜原文标题`. Put a compact source link near the top without a standalone source heading.

## Core Contract

When goals conflict, apply: source truth → explicit user requirements → reader comprehension → 30-second judgment → one-picture 80% understanding → visual polish.

- Create a new output. Never edit, overwrite, reorder, comment on, clean up, rename, move, or change permissions on the source.
- Match output type to input type unless explicitly overridden: Feishu/Lark → new Feishu/Lark doc; Word/docx → new `.docx`; Markdown → new Markdown; HTML → new self-contained HTML. Ask only when type/support is materially ambiguous.
- Use the source's primary language unless the user explicitly requests another output language. Conversation, interface, request, or locale language is not an override. Apply the decision to title, TLDR, table, body, and visual.
- Exclude source appendix / 附录 / Appendix content unless the user explicitly includes it.
- Source-back every number, conclusion, risk, and recommendation. Preserve material denominator, period, sample, scope, significance, confidence, and metric definition. Mark unsupported gaps `原文未提供` / `not provided in the source` or `推断` / `inference`.
- Rebuild the narrative around what readers must understand, trust, decide, or do. Do not compress the source mechanically or impose a fixed body order; put decision implication before implementation detail unless implementers are the explicit audience.
- Every rendered brief must carry the mandatory `reading_path` contract in [reading-layout-contract.md](references/reading-layout-contract.md): lock visible answers, section questions and density before prose. Full body is the default; validation and Reader/Source judgments enforce completeness across formats, Fast and scoped delivery, without length quotas.
- Titles, headings and leads name the object and supported fact, question, change, condition, tradeoff, or impact. Keep decisive qualifiers nearby; record it in the existing object-action/result map without inventing outcomes or forcing contrast.
- Keep prompts, internal process/method language, style names, tool notes, and placeholders out of the artifact. Machine restrictions and semantic colors live in [config/3080-brief.json](config/3080-brief.json).
- Implement user writing requirements; do not repeat or paraphrase them as claims, headings, captions, or visual labels. Use the existing [context review](references/context-value.md#instructioncontent-boundary) for instruction echoes; preserve necessary methods, evidence limits, and explicitly requested reader-facing content, including the named TLDR format.
- Keep generated time, owner, version, location, permissions, and sharing defaults unless requested or operationally required.
- Use `lark-doc` for Feishu docs, `documents:documents` for Word, `lark-whiteboard` for live Feishu preview, and `beautiful-feishu-whiteboard` for Feishu style selection.

## Conditional Routing

Read references as needed.

| Need | Read / run |
| --- | --- |
| Resolve output format or conversion | [output-format-rules.md](references/output-format-rules.md) |
| Create Feishu output or diagnose dependencies | `scripts/check_dependencies.py --mode feishu --json`; read [dependency-and-installation.md](references/dependency-and-installation.md) only on BLOCKED/SKIP/FAIL |
| Inventory sources and claims | [source-inventory-template.md](references/source-inventory-template.md), [claim-ledger.schema.json](references/claim-ledger.schema.json); add [evidence-and-risk-rules.md](references/evidence-and-risk-rules.md) for material data, experiment, causal, metric, or risk claims |
| Plan batch execution and review readiness | [execution-efficiency.md](references/execution-efficiency.md); run `scripts/validate_review_readiness.py` before independent review |
| Draft/revise content | [source-faithful-expression.md](references/source-faithful-expression.md), [direct-expression.md](references/direct-expression.md); add [reader-optimization.md](references/reader-optimization.md) for clarity/jargon failures and [expression-anti-patterns.md](references/expression-anti-patterns.md) for concrete signals |
| Lock opening answers before prose | [required-reader-answers.md](references/required-reader-answers.md): reader/context/task, reading surface and all P0 answers; bind replay receipt in readiness |
| Plan the cross-section reading path | [reading-layout-contract.md](references/reading-layout-contract.md); create the required `reading_path` object before rendering any format |
| Plan the brief and visual | [brief.schema.json](references/brief.schema.json), [visual-spec.schema.json](references/visual-spec.schema.json), [visual-pattern-library.md](references/visual-pattern-library.md), [theme-selection.md](references/theme-selection.md); add [semantic-color-system.md](references/semantic-color-system.md) for directional values/statuses |
| Build target-specific visuals | Feishu: [whiteboard-patterns.md](references/whiteboard-patterns.md), [feishu-doc-output.md](references/feishu-doc-output.md); HTML: [html-visualization.md](references/html-visualization.md) |
| Consider bitmap/image generation | Read [image2-auxiliary-rules.md](references/image2-auxiliary-rules.md) before sending any content |
| Run or resume review | First candidate: [visual-blind-replay.md](references/visual-blind-replay.md), HTML [full-page-visual-replay.md](references/full-page-visual-replay.md), [blind-reader-replay.md](references/blind-reader-replay.md), then [review-loop.md](references/review-loop.md). Changed candidate: [scoped-revalidation.md](references/scoped-revalidation.md) before retry |

## Runtime

Use `standard` by default. `fast` requires explicit user choice: retain source, language, relation, assertion, TLDR, coverage and visual checks; disclose skipped audits/replays. Use `strict` for requested rigor or material resources, policy, causal claims, risk or broad rollout; add exact P0/P1 relation replay and configured reader escalation. See [review-loop.md](references/review-loop.md) for modes and retry limits.

1. **Route**: determine source/output type, language override, scope, constraints, and artifact lanes. For multiple briefs, follow the efficiency contract. For Feishu, check dependencies before fetch/write; installation or authentication needs separate approval.
2. **Ground**: inspect material non-appendix evidence before prose. Build `source_inventory.md`, untranslated `source_non_appendix.md`, P0/P1 excerpts and `claim_ledger.json`, retaining language, exclusions, sufficiency, identity, evidence ceilings, protected relations, data, risks/actions and omissions. Lock all P0 answers; reopen sources only for gaps/disputes. Initialize a `functional` run per [writing-lifecycle.md](references/writing-lifecycle.md).
3. **Clarify**: before drafting, ask up to three blocking questions only when ambiguity can change the main conclusion, metric meaning/scope, risk boundary, audience, next action, language, or protected relation. For non-blocking gaps, use explicit missing-source/inference labels. Shorten thin-source output instead of making it appear rich.
4. **Draft**: create `brief.json` per [brief.schema.json](references/brief.schema.json); create its mandatory `reading_path`: one reader decision, one question and density per section. Lock required answers in `expression_plan`. Use a source-shaped Pyramid opening and judgment headings. At each unit, bind `expression_review` to text; compare direct alternatives and repeated framing, preserving necessary negatives and TLDR units. Give supported answers with decisive conditions and explanations.
5. **Visualize**: map `visual_spec.json` blocks to claims before drawing. Choose one content-fit relationship and allowed theme, without a silent default. Meet weighted coverage and retain every P0. Use quantitative encoding when three or more quantitative claims exist or numbers determine the conclusion; disclose unreliable extraction. Keep semantic colors consistent. Generated images are private-safe inspiration, never final evidence. HTML needs reviewed `html_design.json` and an auditable native-SVG fallback.
6. **Gate and readiness**: create authorized native previews, measure the whole candidate and disposition signals in-run; inspect actual layout. Run checks before review:

```bash
scripts/validate_claim_ledger.py claim_ledger.json
scripts/preflight_check.py DRAFT --source-inventory source_inventory.md --claim-ledger claim_ledger.json
scripts/check_expression_quality.py DRAFT --claim-ledger claim_ledger.json --non-appendix-source source_non_appendix.md
scripts/check_coverage.py claim_ledger.json --visual-spec visual_spec.json
scripts/validate_visual_spec.py visual_spec.json claim_ledger.json
scripts/validate_brief.py brief.json visual_spec.json
```

Validate with `validate_whiteboard.sh` or `validate_html_output.py`. HTML requires the canonical composer, locked contract, build receipt and geometry audit. Fix failures, run the replays below, then validate readiness with the answer receipt; missing/stale evidence blocks audit.

### 7. Stabilize Comprehension Before Audit

Review before audit: picture replay must understand every P0; Primary reads extracted opening with a bound receipt; HTML needs geometry and full-page replay. Use `reader_value` v6 [scan-reading](references/scan-reading.md), direct alternatives, cumulative burden, contextual deletion and source/reader attribution. Disclose Fast self-checks.
Every mode requires [defensive-expression](references/defensive-expression.md) and [context v5](references/context-value.md#answer-selection-and-ending): bind answer, selection and ending judgments to the brief/visual. Missing, pending or revise blocks completion, even with zero phrase issues. Keep review narration private.

### 8. Run The Final Independent Audit

Send the ready candidate to Reader, Source and Visualization concurrently; register batches and raw results in the same run. After edits, use before/after manifests and `plan_review_scope.py` to reuse unaffected PASS results. Stop at scoped pass; rerun all only when required. After three completed batches with current failure, return a labeled draft and ask for direction.

### 9. Verify And Deliver

Inspect authorized Feishu/Word previews, native XML and live boards. HTML uses `html_runtime_contract.py` and `build_html_brief.py ... --design-plan html_design.json --contract ... --receipt ...`. Before checked delivery verify HTML, receipt, geometry, rich/fallback views, full-page replay, unchanged source, format/language, citations, TLDR, coverage, theme/colors, accessibility, hashes and dependencies.

## Delivery

Start [managed execution](references/writing-execution.md) before units, binding packets, raw returns and [checked delivery](references/checked-delivery.md) to the task. Fast stays self-checked. See [host integration](references/host-integration.md) for the `host_delivery.py` adapter and calibration. Return links and limits; CLI notices last.
