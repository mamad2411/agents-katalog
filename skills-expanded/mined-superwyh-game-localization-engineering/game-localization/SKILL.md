---
name: game-localization
license: MIT
description: Localize game projects through text extraction, terminology and character guidance, translation and naturalness review, guarded resource integration, language QA, and detailed developer reports. Use for full projects, incremental updates, translation audits, or game translation post-editing; enable complex-script and compliance checks only for the requested scope.
---

# Game Localization Engineering

Deliver traceable translations, importable resources, evidence of checks actually performed, and a detailed developer review report. All required execution rules, tools, and examples are included locally. Scripts use Python 3.10+ standard libraries without network access. The executing agent translates using project context. The project supplies its editor, compiler, fonts, and runtime.

English is the maintained primary edition. The [documentation index](docs/README.md) provides installation and usage guides in 20 language and regional editions; detailed engineering references remain in English. The [Chinese companion guide](docs/zh-CN/guide.md) provides extended operating instructions. Documentation language does not select the game's target languages. Report language is also independent: set `report_language` to `en` (default) or `zh-CN`. Write decisions and review notes in that language; preserve game strings, IDs, and evidence.

## Start and select modules

Read [workflow](references/workflow.md), [translation and review](references/translation.md), and [reporting](references/reporting.md). Inspect project instructions, the existing pipeline, and user edits. Record the authoritative source language/revision, selected language/script/region combinations, engine/package versions, resource types, and delivery scope.

Derive targets from the request and project; do not select every listed language. If direction or targets are missing, inventory first and clarify before bulk translation. Do not ask again for choices already provided. A text-only assignment does not authorize restructuring the localization framework.

| Trigger | Read | When outside scope |
|---|---|---|
| Selected languages/regions | Relevant [locale profiles](references/locale-profiles.md) | Do not translate unselected languages |
| Translation drafting, review, or requests to remove translationese or an assistant-like voice | [Naturalness and post-editing](references/naturalness.md); use its examples for difficult decisions | Keep good text; do not infer authorship or optimize detector scores |
| RTL, shaping, dictionary segmentation, vertical text, special input, or actual UGC needs | Relevant [complex-script checks](references/complex-scripts.md) | Record exclusion; do not run a global script matrix |
| Extraction, integration, parameters, markup | [Formats and CLI](references/formats.md) | Prefer a verified existing project adapter |
| Source/guidance updates or returned review tables | [Incremental and review exchange](references/incremental-and-review.md) | Do not treat returned rows as approvals |
| Archive/image/binary inventory or measured scenario coverage | [Resource coverage](references/resource-coverage.md) | Keep ordinary text-only work within its requested scope |
| Engine integration | Relevant [engine branch](references/engines.md) | Do not install unrelated engines |
| Delivery validation | Baseline and triggered [LQA cases](references/lqa.md) | Explain skipped checks; never label them passed |
| Requested compliance or specified market release review | Selected regions/platforms/mechanics in [compliance](references/compliance.md) | Default `off`; language does not imply country |
| Conflicting, outdated, uncertain evidence | [Evidence and decision rules](references/knowledge-boundaries.md) | Record unsupported conclusions as unresolved |

## Execution loop

1. **Baseline.** Inventory IDs, file hashes, syntax, context, and audiovisual dependencies. Test an unchanged round trip, then a small loop with menus, parameterized dialogue, and a critical asset.
2. **Language assets.** Build concept-based terminology and character × addressee × story-stage voice records. Separate UI, instructions, dialogue, subtitles, store copy, and legal text. Include examples, counterexamples, and exceptions.
3. **Translation and review.** Work on complete messages, branches, and puzzle dependency groups. Establish source meaning, edit idiom/register, read as target-language text, then recheck facts, agents, negation, conditions, numbers, uncertainty, and game function against the source. Preserve intentional voice and clues. Record before/after and reasons for substantive edits; proofread and reconcile scenes. Resolve context gaps without inventing facts; continue independent entries. Distinguish self-review from native/developer review.
4. **Deterministic checks.** Check ID sets, source revisions, parameter types/bindings, tags, numbers/units, omissions, intentional empty strings, and protected literals. Use real parsers for complex messages. Regex, counts, and glyph coverage do not prove syntax, layout, or runtime correctness.
5. **Staging and integration.** Stage separately and inspect additions, changes, removals, and nontext fields. Continue authorized integration with recovery records. Stop affected overwrites and reconcile if source or destination changes. Translation does not itself authorize publication, rating submissions, or messages to others.
6. **Validation and repair.** Perform applicable import, build, runtime, linguistic, accessibility, and enabled compliance checks. Retest fixes. Complete independent work when an environment is missing; report limits without inventing a pass.
7. **Developer report.** On completion, partial completion, or stopping, deliver a detailed report, full source/target comparison, significant decisions, issues/evidence, unperformed checks, and specific developer actions. Delivery is incomplete without these.

## Local tools

Read the [configuration contract](references/formats.md), then adapt the [example configuration](assets/project.example.json). `SKILL`, `PROJECT`, and `RUN` mean actual paths; quote them as required by the shell.

```text
python -X utf8 SKILL/scripts/l10n.py inventory --project PROJECT --out inventory.json
python -X utf8 SKILL/scripts/l10n.py extract --config project.json --run RUN
python -X utf8 SKILL/scripts/l10n.py qa --run RUN
python -X utf8 SKILL/scripts/l10n.py stage --run RUN
python -X utf8 SKILL/scripts/l10n.py apply --run RUN
python -X utf8 SKILL/scripts/l10n.py report --run RUN
```

The CLI directly supports flat JSON maps and CSV/TSV. Other formats require native export or project adapters. Staging requires current review records for every selected entry, not every language or jurisdiction. Complete substantive `review-notes.json` content before the final report. Static checks, language review, integration, builds, runtime, and developer signoff are separate states.

For updates, use `refresh --previous OLD_RUN --config project.json --run NEW_RUN`; inspect stale entries, original translation bases and retained orphans. Bind relevant project terminology/voice files with `guidance_files` so their changes invalidate affected reviews. Use `review-export`/`review-import` for external CSV review, with truthful reviewer identity. Use `coverage-init`/`coverage-check` only when resource/scene accounting is needed. Their detailed contracts and examples are in the two references above.

Use the [verification guide and example resources](references/validation.md) when first integrating. CLI `stage`, `apply`, `rollback`, `refresh`, review exchange and `coverage-check` attempt reporting after success or reportable failure; complete the human judgments and regenerate the final version. The reporting-only override `report --run RUN --language zh-CN` changes report presentation without changing the game or baseline.

## Engineering invariants

- Preserve internal keys, branch indices, control codes, asset references, parameter identities, story facts, and functional values. Translations are not identifiers.
- Review regional adaptations as whole sentences. Software style guides do not define every character's voice. Do not infer gender or identity from names.
- Scope compliance to applicable cases. Do not automatically remove plot, soften profanity, change mechanics, or claim approval. Separate recommendations from changes made.
- Record fonts, translation, voice tracks, subtitles, format locale, and distribution regions separately. Fallback does not fix missing translation. Source/context changes invalidate old review.
- Batch by scene/chapter and save progress/context until authorized work is complete. Length does not justify omitted branches; sampling is not full coverage.
