---
name: fina-skill-creator
version: 1.0.0
description: Produces a new SKILL.md for the fina- financial-analysis vertical that conforms exactly to the house standard for naming, frontmatter, section order, voice, cross-linking, and pre-publish QC.
author: matrixx0070
tags: [finance, meta, skill-authoring, documentation, standards, style-guide]
capabilities: []
---

# Create a fina- Skill to House Standard

## When to use
Use this when you are writing a brand-new skill for the financial-analysis (`fina-`) vertical and need it to match the established house standard so it sits cleanly beside its siblings. It defines the required naming, frontmatter, section order, voice, and review gate for every `fina-` skill.

**Not for:** authoring the analytical content of a specific skill such as data cleaning (fina-clean-data-xls), workbook construction (fina-xlsx-author), the three-statement model (fina-3-statement-model), valuation (fina-dcf-model), or review work (fina-audit-xls); this meta-skill governs form and standard, not the domain method inside any one skill.

## Method
1. **Name the skill with the `fina-` prefix.** Use lowercase, hyphenated, verb-or-noun descriptive slugs (for example `fina-dcf-model`, `fina-comps-analysis`). The `name` field in frontmatter must match the folder name exactly.
2. **Write the frontmatter in the fixed order.** Emit `name`, `version` (start at `1.0.0`), `description` (one dense sentence stating what the skill produces), `author` (`matrixx0070`), `tags` (a `finance` tag plus several relevant ones), and `capabilities` (an empty array `[]`). Decision point: if you cannot state the deliverable in a single sentence for `description`, the skill's scope is too broad or too vague to publish, so split or sharpen it before writing further.
3. **Follow the mandated section order.** After the H1 title, write exactly: `When to use` (with a `**Not for:**` redirect line), `Method` (numbered, bolded leads, decision points), `Example`, `Pitfalls` (bolded names), `Output format` (fenced block), then `Reference` (multiple `###` subsections). Do not add, drop, or reorder top-level sections.
4. **Write in the second person.** Address the reader as "you" throughout. Give direct instruction, not narration about what the skill does in the abstract.
5. **Keep tool and shell invocations out.** Describe the standard, conventions, formulas, and checks only. Decision point: if a step reads like a command to execute rather than a technique to apply, rewrite it as method and convention, because these skills document how to do the work, not machinery to run.
6. **Cross-link the siblings.** In `When to use` / `Not for:` and wherever scope touches another skill, name the correct sibling (`fina-clean-data-xls`, `fina-xlsx-author`, `fina-3-statement-model`, `fina-dcf-model`, `fina-audit-xls`, `fina-comps-analysis`, `fina-pptx-author`) so a reader is routed to the right place.
7. **Make Reference the substance.** Put the conventions, formula and function tables, and QC checklists here across several `###` subsections; this is where a practitioner actually gets value.
8. **Run the self-review before publishing.** Walk the pre-publish QC checklist and fix any miss before the file is considered done.

## Example
You are creating a sensitivity-analysis skill. You choose the slug `fina-sensitivity-analysis`, set the folder and `name` field to match, and write frontmatter: `version: 1.0.0`, `description: Produces a two-way data-table sensitivity grid over a model's key value drivers with a tornado summary of single-variable impact.`, `author: matrixx0070`, `tags: [finance, sensitivity, modeling, excel, scenario]`, `capabilities: []`. You add the H1, then `When to use` with `**Not for:** scenario switching inside a model (use fina-xlsx-author) or valuation output (use fina-dcf-model).`, a numbered `Method` with two decision points, a worked `Example`, bolded `Pitfalls`, a fenced `Output format`, and a `Reference` with `### Data-table setup`, `### Driver selection`, and `### QC checks`. You then run the QC checklist below and confirm every box before publishing.

## Pitfalls
- **Name/folder mismatch.** If the `name` field does not equal the folder slug, the skill will not resolve. Keep them byte-identical.
- **Reordered sections.** Adding, dropping, or shuffling the mandated sections breaks the house standard and reader expectations. Follow the fixed order exactly.
- **Vague description.** A `description` that does not name the concrete deliverable gives readers no way to pick the skill. State what it produces in one sentence.
- **Third-person drift.** Slipping into "this skill does X" instead of "you do X" reads as marketing, not instruction. Stay in the second person.
- **Embedded tool or shell calls.** Any command-to-run leaks machinery and violates the standard. Describe technique and convention only.
- **Thin Reference.** A skill whose value is only in the prose above `Reference` is underbuilt. Put the tables and checklists that carry the real weight in `Reference`.
- **Orphaned skill.** No cross-links to siblings leaves the skill isolated and readers misrouted. Name the relevant `fina-` siblings.

## Output format
```
/root/sudo-skills/docs/skills/<fina-name>/SKILL.md

---
name: <fina-name>
version: 1.0.0
description: <one dense sentence: what it produces>
author: matrixx0070
tags: [finance, ...]
capabilities: []
---
# <Human Readable Title>
## When to use        (1-2 sentences + **Not for:** redirect)
## Method             (numbered, **bolded leads**, >=2 "Decision point:")
## Example            (concrete worked mini-example)
## Pitfalls           (bulleted, **bolded names**)
## Output format      (fenced deliverable shape)
## Reference          (multiple ### subsections: conventions, tables, QC)
```

## Reference

### Frontmatter fields
| Field | Rule |
|-------|------|
| `name` | lowercase, hyphenated, `fina-` prefix, equals folder slug |
| `version` | starts at `1.0.0`, semver |
| `description` | one dense sentence naming the deliverable |
| `author` | `matrixx0070` |
| `tags` | list including `finance` plus several relevant terms |
| `capabilities` | empty array `[]` |

### Required sections and contents
| Section | Must contain |
|---------|--------------|
| `# Title` | human-readable H1 after frontmatter |
| `## When to use` | 1-2 sentences + a `**Not for:**` line redirecting to siblings |
| `## Method` | numbered list, each step a **bolded lead**, at least two `Decision point:` clauses |
| `## Example` | one concrete worked mini-example |
| `## Pitfalls` | bullets, each a **bolded name.** then the failure prevented |
| `## Output format` | fenced code block showing the deliverable shape |
| `## Reference` | multiple `###` subsections: conventions, formula/function tables, QC checks |

### Voice and style rules
- Second person ("you") throughout; direct instruction.
- No emojis.
- No executable commands, tool calls, or other-skill invocations; describe the standard only.
- Be technically correct and specific; prefer tables for formulas and functions.
- Cross-reference siblings by exact name where scope touches them.

### Sibling skills to cross-link
| Sibling | Covers |
|---------|--------|
| `fina-clean-data-xls` | cleaning/normalizing raw data before modeling |
| `fina-xlsx-author` | authoring an auditable workbook from scratch |
| `fina-3-statement-model` | linked income statement, balance sheet, cash flow |
| `fina-dcf-model` | discounted-cash-flow valuation |
| `fina-comps-analysis` | trading/transaction comparables |
| `fina-audit-xls` | reviewing a finished third-party workbook |
| `fina-pptx-author` | presenting results in a deck |

### Pre-publish QC checklist
| Check | Pass when |
|-------|-----------|
| Slug and `name` match | folder name == `name` field, `fina-` prefix present |
| Frontmatter order and fields | all six fields present in required order, `capabilities: []` |
| Description | one sentence, names concrete deliverable |
| Section set and order | all seven parts present, none reordered |
| Method rigor | numbered, bolded leads, >=2 `Decision point:` clauses |
| Voice | second person throughout, no emojis |
| No invocations | no shell/tool/command references anywhere |
| Cross-links | relevant `fina-` siblings named |
| Reference depth | multiple `###` subsections with tables and QC checks |
