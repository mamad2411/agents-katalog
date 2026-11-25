---
name: dissertation-argument-spine
description: Build and audit the controlling argument spine for this dissertation, proposal, literature review, methodology chapter, and major revisions so writing is motivation-led, source-grounded, and not shallow polishing.
---

# Dissertation Argument Spine

Use this skill when the user asks to plan, diagnose, rewrite, or review proposal/chapter writing where the central argument, section logic, evidence boundaries, or supervisor discussion questions matter.

This is a dissertation-focused adaptation of the useful parts of PaperSpine. It is not the full journal-paper, LaTeX, or script-driven PaperSpine pipeline.

## Core Rule

Do not begin substantive drafting until the task has:

1. a source map,
2. a confirmed or explicitly tentative controlling motivation,
3. a dissertation red thread,
4. section-level blueprints,
5. evidence boundaries and `TO CONFIRM` fields.

For formal university documents, also use `dissertation-source-first-gate` before drafting and `dissertation-document-quality-gate` before delivery.

## Current Project Fit

For the user's dissertation, the current working spine is:

> Active learning is valued in higher education but difficult to implement consistently. AI agents may support teachers with planning, adaptation, and reflection, but their acceptability depends on how university teachers perceive usefulness, effort, trust, autonomy, workload, pedagogic identity, and the conditions required for adoption.

Use this as a working spine, not as a final claim. Update it when supervisor feedback or stronger evidence changes the project direction.

Current conceptual lens:

- Use the chosen conceptual lens as a qualitative organising lens for teacher adoption conditions.
- Treat performance expectancy, effort expectancy, social influence, and facilitating conditions as sensitising concepts.
- Pair the chosen conceptual lens with responsible AI and higher education teaching literature where it does not cover trust, autonomy, privacy, hallucination, or pedagogic identity.
- Do not present the chosen conceptual lens as a quantitative model unless the method changes to support that.

## Workflow

1. **Classify the writing task**
   - Proposal, literature review, methodology, interview guide, discussion chapter, supervisor brief, or final dissertation section.
   - If the task is a formal document, identify whether Word output is expected.

2. **Create or refresh a source map**
   - List the source files, LMS/module rules, ethics documents, supervisor notes, literature notes, and user-confirmed facts.
   - Separate confirmed information, inference, and `TO CONFIRM`.
   - Never invent personal details, citations, dates, participants, findings, or institutional requirements.

3. **Confirm the controlling motivation**
   - If the user or existing project files already provide a clear motivation, restate it and mark it as `working-confirmed`.
   - If there are multiple possible motivations, create 2-4 options and ask the user to choose before major writing.
   - Record what the project should not claim.

4. **Build the red thread**
   - Field problem: active learning implementation difficulty.
   - Specific gap: teacher-facing AI-agent support for active learning is not yet sufficiently understood through university teachers' perceptions, concerns, and adoption conditions.
   - Conceptual lens: the chosen conceptual lens-informed adoption conditions, extended by responsible AI and teacher autonomy concerns.
   - Method response: qualitative interviews using an AI-agent concept card where appropriate.
   - Evidence: teacher interviews, concept-card responses, literature, supervisor feedback, ethics-approved materials.
   - Contribution: teacher-informed adoption conditions, design boundaries, and implications for responsible AI-agent support.

5. **Make section blueprints before prose**
   - For each section, state the reader question, section job, evidence needed, claims allowed, and claims to avoid.
   - A section should not be drafted if its job is unclear.
   - For formal proposal, literature review, methodology, manuscript, report, grant, or stakeholder-facing claims, consume the Claim Ledger Lite from `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md` when required. The argument thread must not make a claim stronger than the ledger's `allowed_wording`.

6. **Use a section rationale matrix for important writing**
   - For proposal, chapter, supervisor-facing, or major revision work, create a section rationale matrix before substantial prose.
   - Include the whole-document framework row first.
   - Explain the motivation link, source anchor, planned text move, and final check for each meaningful writing unit.

7. **Use a rewrite matrix for major revisions**
   - For each paragraph/unit, label the action: `KEEP`, `REWRITE`, `SPLIT`, `MERGE`, `MOVE`, `DELETE`, or `ADD`.
   - `ADD` and `KEEP` should not dominate a serious revision.
   - Preserve source-grounded claims and mark unsupported material as `[NEED EVIDENCE]` or `[TO CONFIRM]`.

8. **Run a logic-transfer audit before calling major revision finished**
   - Check whether Introduction, Literature Review, Methodology, Findings, Discussion, and Conclusion still answer the same core problem.
   - Check whether every major claim has a source or a planned empirical evidence route.
   - Check whether the revision changed the argument logic, not only the language.

## Logic Check Structure

For proposal, literature review, methodology, or supervisor-facing planning, audit this chain:

```text
motivation -> gap -> conceptual lens -> research questions -> method -> ethics boundary -> expected contribution
```

A strong chain for the current project should show:

1. why active learning implementation support matters in higher education
2. why AI-agent support must be studied through teachers before design or adoption claims are made
3. how the chosen conceptual lens helps organise adoption conditions
4. where the chosen conceptual lens is insufficient and responsible AI / teacher autonomy literature is needed
5. why interviews and concept-card elicitation fit the evidence needed
6. why the project can produce adoption conditions and design boundaries without building a full prototype

When multiple routes exist, recommend one main route first. Keep alternative routes brief and use them only to clarify the decision.

## Gap Quality Gate

A defensible gap should be:

- specific to university teachers
- specific to AI-agent support for active learning
- connected to perceptions, concerns, and adoption conditions
- feasible to investigate through interviews
- careful about what the study can claim before empirical data exists

## Outputs

Use task-specific files when useful:

- `chapter-plans/ARGUMENT_SPINE.md`
- `chapter-plans/SECTION_BLUEPRINTS.md`
- `chapter-plans/SECTION_RATIONALE_MATRIX.md`
- `chapter-plans/REWRITE_MATRIX.md`
- `chapter-plans/LOGIC_AUDIT.md`
- `research-wiki/TASK_STATE.md`
- `proposal/*`

For templates and tables, read `references/dissertation-spine-templates.md`.

For the migrated PaperSpine-inspired controls, read `references/paperspine-adapted-writing-controls.md` when the task needs section rationale, motivation-thread, revision-matrix, logic-transfer, or artifact-completeness checks.

For PaperSpine components intentionally not migrated yet, read `references/deferred-paper-spine-components.md`.

## Stop Conditions

Stop and ask or mark `TO CONFIRM` when:

- the controlling motivation is unclear or competing motivations exist,
- the user asks for formal wording but source facts are missing,
- a citation or page reference has not been verified,
- the output type is unclear: concept card, design principles, adoption model, feature requirements, or agent specification,
- a proposed claim implies findings that do not exist yet.
