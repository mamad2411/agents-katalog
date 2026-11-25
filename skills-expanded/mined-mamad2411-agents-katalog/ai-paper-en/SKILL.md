---
name: ai-paper-en
description: Use when revising English theses or papers in AI systems, AI chips, compilers, computer architecture, or systems engineering for contribution framing, abstract/introduction logic, related-work positioning, method/evaluation chapter organization, natural academic prose, reference-thesis structure, bilingual alignment, bibliography/format checks, or text that is AI-like, too implementation-heavy, code-like, vague, or not publication-ready.
---

# AI Paper En

## Core Principle

Revise as a technical paper coauthor, not as a grammar corrector. First fix the level of abstraction and the contribution story, then rewrite prose, then verify the delivered output in its actual format.

The recurring target style is: clear research problem, concrete gap, what this work introduces, what capability/result it produces, and under what scope the claim holds. Avoid writing the paper as an implementation log.

For AI-system, AI-chip, compiler, architecture, and systems work, keep the argument at the level of abstraction, constraints, method, tool flow, and measured capability. Separate algorithm semantics, program representation, compiler/runtime mapping, hardware/platform constraints, and implementation/verification artifacts instead of mixing them in one paragraph.

## Workflow

1. Read the active source and deliverable structure before editing.
   - Find the master document, included chapters/sections, bibliography sources, image/table sources, exported output, and local instructions.
   - Determine which files affect the user-visible document. Do not spend edits on unused files unless stale text may be reintroduced later.

2. Build the current story before touching prose.
   - Identify the paper object: workload/problem, platform/system, abstraction or method, evaluation setup, and claimed result.
   - Locate abstract, introduction, contribution list, related work, chapter/section roadmaps, conclusion, and relevant figure/table captions.
   - If using a reference paper or thesis, extract its table of contents and section roles first, then map those roles to the current work's own concepts. Do not import topic content or wording.
   - If the user provides meeting notes or advisor feedback, extract reusable requirements rather than paraphrasing the transcript.

3. Revise from high level to low level.
   - Abstract first: use the five-part pattern below.
   - Introduction next: make paragraph topic sentences carry the same logic as the abstract.
   - Related work next: move from "prior work exists" to "classification axes -> existing foundations and gaps -> this work's workflow or capability map."
   - Method sections last: keep technical details where they explain the method, but make the structure carry `background/challenge -> overall framework -> core method -> evaluation -> summary`.

4. Verify after every meaningful edit set using the document's actual format.
   - Regenerate or export the user-visible deliverable when needed.
   - Check format-appropriate build/export diagnostics; do not assume the project is LaTeX.
   - Confirm revised wording appears in the user-visible output, not only in source files.
   - Inspect layout-sensitive pages or objects visually when the user mentioned tables, figures, pagination, captions, or "looks bad".
   - If generated output is separate from the user-facing file, sync it according to the project's convention.

## Abstraction Level Control

Use a pyramid of detail. The same method should be described at different levels in different places:

- Abstract, introduction, and conclusion: research problem, why it is hard, what prior work lacks, what capability this work builds, and what evaluation shows. Avoid backend interfaces, verification infrastructure, code fields, module names, and implementation errands.
- Roadmap and first-page figures: show the paper flow and responsibility split. Do not put low-level debug terms, file/interface names, or too many internal components in the opening figure.
- Method sections: define formal objects, constraints, algorithms, models, and implementation structure only when they explain the method.
- Evaluation sections: give concrete settings, baselines, metrics, and result interpretation. Define comparison objects before comparing them.

When advisor or reviewer feedback is available, translate it into writing rules. Common moves:

- "Too low-level" means move details from abstract/introduction/conclusion into method, evaluation, appendix, or omit them.
- "Not clear" means name the concrete object, constraint, or action instead of using a label-like phrase.
- "Comparison is confusing" means define both comparison objects separately before stating a result.
- "Figure is too detailed" means redraw or rewrite around top-level flow: problem/object -> representation/model -> platform/constraint -> evaluation/result.

## Domain-General Argument Pattern

For AI systems, AI chips, compilers, computer architecture, and systems engineering, convert implementation details into a layered research story:

```text
workload or system problem
-> why existing algorithms/tools/platforms are insufficient
-> abstraction, representation, model, or workflow introduced by this work
-> generation, optimization, verification, or mapping method
-> platform-aware evaluation and measured capability
```

Keep these layers distinct:

- Algorithm or workload semantics: what must remain equivalent or correct.
- Program representation or system abstraction: how the work describes the problem space.
- Optimization or generation method: how designs, schedules, mappings, or configurations are produced.
- Platform or architecture constraints: what memory, compute, communication, parallelism, synchronization, or deployment constraints matter.
- Implementation and verification artifacts: scripts, simulators, RTL hooks, drivers, logs, and test harnesses. These usually belong in method details, appendices, or evaluation setup, not in the abstract or opening motivation.

Common contribution axes:

- Abstraction/model: formalizes a workload, execution process, memory behavior, dataflow, mapping, or hardware constraint.
- Search/generation/optimization: produces valid candidates, schedules, mappings, code, configurations, or design points.
- Analysis/evaluation: estimates cost, checks correctness, explains bottlenecks, or compares alternatives.
- System integration: connects layers of a toolchain or hardware/software stack when that integration creates a research capability, not merely an implementation pipeline.

Common evaluation claims:

- Correctness or equivalence: generated results preserve required semantics or interface behavior.
- Coverage or expressiveness: the method represents more workloads, patterns, mappings, or constraints.
- Performance, cost, or resource result: latency, throughput, energy, memory traffic, area, utilization, compile/search time, or deployment cost.
- Ablation or attribution: which part of the abstraction, model, optimization, or platform correction causes the result.
- Model accuracy: estimates match simulator, hardware, trace, or baseline measurements within stated scope.

## Abstract Pattern

Use this five-part structure:

1. What this work studies.
2. Why the problem is difficult.
3. What prior work can do and what remains insufficient.
4. What this work introduces to address the gap.
5. What the evaluation shows, with honest scope qualifiers.

Keep the abstract at the highest abstraction level. Do not insert implementation interfaces, verification environments, field names, low-level modules, or backend plumbing unless they are the actual research contribution.

Prefer capability-level phrasing:

```text
This work addresses the problem from three levels: problem modeling, design-space representation, and platform-aware evaluation.
```

Too low-level for an abstract:

```text
The implementation connects the simulator backend, verification harness, and low-level interface scripts.
```

When the user says "say how I solve it", avoid turning the abstract into a section inventory. Phrase the solution as a chain of capabilities:

```text
First, the work defines an execution model that constrains the design space. Second, it embeds these constraints into an intermediate representation, scheduling expression, or mapping description so that design points can be generated, checked, and exported. Third, it builds a platform-aware evaluation method to filter feasible designs and compare their costs.
```

Use explicit scope phrases such as `under the evaluated workloads`, `in our simulator-backed setting`, `on the tested platforms`, or `within the modeled cost components`.

## Contribution Framing

Avoid defensive or assembly-like framing:

```text
This work does not replace prior methods; instead, it combines A, B, and C into one framework.
```

Prefer gap-to-capability framing:

```text
Prior work provides foundations for A, B, and C, but it does not directly support X in this setting. This work introduces ... so that ... can be generated, checked, compared, or explained.
```

A strong contribution sentence should answer:

- Existing foundation: what prior work already provides.
- Remaining limitation: what is still hard in this setting.
- Work capability: what new model, representation, optimization, evaluation, or check is formed.
- Observable result: what can now be generated, screened, compared, measured, or explained.
- Domain layer: whether the contribution is about semantics, representation, optimization, mapping, platform constraints, or evaluation evidence.

Do not overuse vague nouns such as `framework`, `pipeline`, `unification`, `platform awareness`, `capability boundary`, or `insight`. If used, immediately state what concrete capability they produce.

## Natural Academic English

When text feels AI-like, code-like, too low-level, or obscure, diagnose which failure it is:

- Inflated abstraction: replace label-like nouns with the concrete object, constraint, or action.
- Code translation: replace field names and underscores with paper concepts.
- Over-compression: split one dense claim into what is compared, under what condition, and what changes.
- Low-level leakage: move implementation details out of abstract/introduction/conclusion.
- Defensive framing: state what the work enables instead of what it is not.
- Unsupported overclaiming: add scope qualifiers or move the claim to future work.

Use these replacement patterns:

| Avoid | Prefer |
| --- | --- |
| semantic invariance | preserving equivalent outputs; preserving interface behavior |
| materialized intermediate | writing and rereading the intermediate result |
| spill-and-fill | writing data beyond on-chip capacity and reading it back later |
| X dimension / X side / X stage | concrete object: input length, output channel, timestep, batch, tile row/column, producer/consumer position |
| return code is 0 | usually omit from paper prose |
| `*_level`, `*_deps`, `resident_*`, `mapping/arch` | scheduling level, dependency relation, resident data, mapping, platform description |
| model-style baseline plus platform-aware compensation | state what the baseline estimates, then state which platform costs are added |

Avoid raw code identifiers, monospaced formatting, and literal field names in academic prose unless the identifier is a formal artifact under discussion. Keep mathematical symbols and defined method names where necessary.

## Reference Thesis Or Paper Logic

When learning from another thesis or paper, extract only organization logic, section function, and rhetorical moves. Do not copy topic-specific wording, examples, technical claims, figure content, or domain framing. Translate the structure into the current work's own objects.

Reusable pattern:

```text
introduction contribution story
-> related work as classification and positioning
-> method sections with local evaluation where appropriate
-> conclusion by the same contribution axes
```

Before using a reference:

1. Extract the table of contents and major section headings with the file-appropriate extractor or existing extracted text.
2. Label every section by role: background, challenge, classification axis, method overview, core abstraction, integration, experiment, summary, conclusion, future work.
3. Build a role map from reference sections to current sections.
4. Rewrite using only the role map. If a sentence depends on the reference's topic, it should not be transferred.
5. After restructuring, check section counts, roadmap text, cross-references, figure/table numbering, and conclusion references.

## Introduction And Contributions

Use this shape:

```text
research background and challenge
-> research motivation
-> main contributions and their relationships
-> paper organization
```

The contribution section should first recap the challenges and motivation, then state that the contributions correspond to those challenges. Each contribution should contain:

- research object or abstraction;
- proposed framework, method, or model;
- capability enabled by that method;
- evaluation result or observable effect.

Do not write contributions as a list of modules implemented. Use a relationship figure or table when there are multiple contribution axes. The figure/table should show how challenges, contributions, sections, and evaluation evidence correspond.

The organization paragraph should state the overall reading order first, then give a concise roadmap. Each section description should explain its role in the argument, not summarize internal implementation details.

## Related Work Closure

Do not let related work end as a literature catalog. Use this progression:

```text
announce classification dimensions
-> review work by those dimensions
-> identify useful foundations and remaining gaps
-> present this work's abstraction, workflow, or capability map
```

Useful dimensions include technique route, system layer, development stage, hardware/software boundary, task type, evaluation target, or capability requirement. Choose dimensions that help the current paper argue for its method.

End the section with a bridge to the method. It should answer:

- What common abstraction or problem formulation this work will use.
- How the next sections divide responsibilities.
- Why this workflow follows from the related-work gaps.

When useful, include a compact table with columns like `Dimension / Existing foundation and limitation / This work`.

## Method And Evaluation Structure

For each method section or chapter, prefer this order unless the current paper has a strong reason to differ:

```text
section intro: where this part sits in the whole paper
-> technical background and concrete challenge
-> overall framework or structure
-> core abstraction/model/method
-> analysis, optimization, generation, verification, or integration
-> evaluation results
-> section summary where appropriate
```

The section intro should connect to the paper-wide workflow and preview the abstraction and framework before details. It should not start with code-level implementation facts.

When the work has several distinct methods, consider placing evaluation near each method rather than using one late standalone evaluation section. This is useful when each method makes a separate claim and needs immediate evidence.

Use the evaluation pattern:

```text
evaluation results
-> experimental setup
-> result subsections grouped by claims
-> interpretation of why the result changes
```

Only fold a standalone evaluation section into method sections after checking whether each method has enough evidence, whether roadmap text must change, and whether cross-references and figure/table numbering remain correct.

Evaluation prose should state the question first, then settings, then results. Do not only report numbers. Explain which part of the method causes the difference and what the result does or does not prove.

## Figures And Tables

Treat figures and tables as part of the argument.

- A page containing only one table or an orphaned caption is a layout problem, not just a source-format problem.
- If a table compares contributions, prefer columns like `Dimension / Existing foundation and limitation / This work`.
- If table headers are visually off, check alignment in the rendered output, not only the source table definition.
- If numeric differences matter, show enough decimals to make the claim visible, but do not overstate small differences.
- If a figure's axis or label says one thing and the surrounding paragraph says another, update one of them so they match.

For tables that must stay near explanatory text, use the local document pattern for keeping captions and table bodies together. After changes, inspect the rendered page to catch caption/body splits.

## Format And Bibliography Checks

For format-review tasks:

- Convert/extract requirement documents safely; do not edit paper files unless asked.
- Report as `needs change`, `passes`, and `cannot judge automatically`.
- Exclude front matter the user explicitly says they will add later.
- Check page count, blank pages, page numbering, section starts, abstracts, table/figure captions, references, and format-specific warnings.

For bibliography:

- Compare citations that appear in the user-visible document with bibliography entries available to the document.
- Account for inactive sections, hidden appendices, and format-specific "include all references" settings.
- Report unused, missing, and visibly unresolved references separately.

## Completion Checklist

Before saying the revision is done:

- Source search shows disliked phrases are gone or intentionally retained.
- Bilingual abstracts are aligned in meaning and abstraction level when both exist.
- Roadmap, section count, labels, and references match the current structure.
- The document has been regenerated/exported when needed, and the command or tool completed successfully.
- Format-specific diagnostics show no new unresolved references, citation issues, export failures, or layout warnings that affect the requested work.
- Extracted text, rendered preview, or direct document inspection confirms the revised wording appears in the user-visible document.
- Layout-sensitive pages or objects have been checked visually when the user mentioned tables, figures, pagination, captions, or "looks bad".
