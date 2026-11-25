---
name: agent-orchestration
description: Decide which research project skills to use for each task, whether the task should be handled by one agent or split across multiple subagents, and how to coordinate outputs safely.
---

# Agent Orchestration

Use this skill at the start of non-trivial research tasks, especially when the user asks for planning, reviewing, literature work, source ingestion, formal drafting, compliance/ethics review, LMS/portal analysis, or multi-part project updates.

## Core Rule

First classify the task. Then choose skills. Then decide whether subagents are useful and allowed.

For the Production Window, this is automatic for every user task. Do not wait for the user to name a skill. For simple chat answers, route silently and answer directly. For substantial research work, formal drafting, source ingestion, Word output, or stakeholder-facing material, state the selected skills briefly before acting and record the routing in the Production run receipt.

Use `research-project-adapter` when the project type is unclear or when adapting this starter kit to a non-dissertation profile.

The user may grant project-level standing permission for the agent to decide whether subagents are useful. This permission does not mean subagents should be used automatically. Use them only when they materially improve quality, speed, independent review, or parallel research. If the work is narrow, sensitive, or a single-document edit, handle it locally.

Before drafting any formal document, use `dissertation-source-first-gate`. Extract known factual fields from source files. Do not invent names, emails, dates, institutional contacts, supervisor/PI/client details, signatures, participant facts, datasets, results, administrative requirements, journal/funder/client requirements, marking criteria, grade-band standards, LMS requirements, deadlines, word counts, or submission rules. If a field is not found in the source material, mark it `TO CONFIRM`.

Before substantive cross-stage work, apply `research-wiki/STAGE_CONTINUITY_PROTOCOL.md` when both conditions hold: (A) the task changes, designs, restates, translates, formalises, or produces a high-risk deliverable class such as method plan, compliance material, fieldwork instrument, analysis plan, stakeholder-facing decision memo, or formal section draft; and (B) `research-wiki/STAGE_GRAPH.md` lists upstream dependencies or the task references prior decisions, accepted outputs, source-of-record files, source maps, or checkpoints. Citation-only edits, formatting/layout fixes, typo repair, file moves, bookkeeping, and source summaries without design/formal-claim output do not trigger the gate.

Use `scripts/stage_recall_policy.py` or the runtime preflight `recall_decision` as the token-aware recall controller. Tier 0 means no project recall; Tier 1 anchor scan; Tier 2 pointer lookup; Tier 3 targeted Stage Continuity Capsule; Tier 4 full upstream audit or pause. This controller manages context budget only. It never overrides Stage Continuity A+B, source-first, compliance, citation, privacy, document-quality, or delivery gates. If the user says to skip upstream checks for a triggered deliverable, surface the omitted dependency first and record an override risk only after explicit user acceptance.

Keep bounded work bounded. Source planning, reading-priority sorting, source lookup, and minor citation/typo edits should use the light runtime receipt set unless the user asks for formal prose, Word/DOCX, stakeholder-facing or submission-facing output, or protected source-of-record edits. Do not route into the full formal-writing chain merely because the task mentions methodology, literature review, proposal background, or sources.

Before answering rubric, grade-band, marking-criteria, journal/funder/client requirement, LMS requirement, word-count, deadline, or submission-rule questions, use the strongest available project requirement source. Use `university-guidance/RUBRIC_EVIDENCE_GATE.md` for assessed academic work. Distinguish official original text, local summary, inference, and evidence-insufficient status.

Before delivering formal documents or important project notes, use `dissertation-document-quality-gate` at the appropriate level.

For major proposal, manuscript, report, grant, methodology, literature review, or stakeholder-facing writing, use source-first, `material-passport`, and `academic-integrity-preflight` before `cognitive-frameworks`. The cognitive output should name section type, claim, gap/problem type, evidence, warrant, boundary, and rhetorical plan.

For formal academic or professional prose, use `academic-self-review-loop` after `cognitive-frameworks` and before style/document-quality gates. The loop should identify concrete weaknesses, revise argument quality, and make a fresh second-pass judgement.

When language quality, British English, or the user's preferred output pattern matters, use `uk-academic-writing-style` and `style-memory-and-revision-gate` before delivery.

When the user asks for AI-looking prose cleanup, de-AI, humanising, lower-AI-rate, AIGC, AI detector, or disclosure-hiding help, use `authorial-voice-integrity` to reframe the task as authorial voice, academic/professional integrity, and evidence-led style. For formal artifacts, source-first, Material Passport, and integrity checks still come before substantive style revision. Do not promise detector outcomes or use evasion tactics.

## Production Auto Skill Routing

Use this quick sequence at the start of every Production Window turn:

1. Classify the user's current task by mode and task type.
2. Select the smallest useful skill set from the classification table.
3. Compute or consume the Token-Aware Recall tier and state the minimum recall scope for substantial work.
4. Check whether Stage Continuity A+B is triggered. If yes, read `research-wiki/STAGE_GRAPH.md`, write a Stage Continuity Capsule, and run `scripts/stage_continuity_capsule_check.py` when available.
5. Open the relevant `SKILL.md` files before acting on any non-trivial task.
6. Add source-first, cognitive-framework, self-review, argument-spine, style-memory, document-quality, compliance, project-delivery, and context-continuity gates when the task involves formal or stakeholder-facing output.
7. Re-route and recompute recall if the user changes the task during the turn.
8. Before formal delivery, confirm the final artifact still matches the latest recall tier, source map, and gates.
9. Record the routing in `research-wiki/PRODUCTION_RUN_REGISTER.md` for substantial Production tasks.

Use this receipt wording:

```text
Skill routing:
- Mode:
- Skills selected:
- Why these skills:
- Skills considered but skipped:
- Subagent decision:
- Gates required:
- Gates completed:
- Recall Decision Note:
- Stage Continuity Gate triggered:
```

If a substantial Production output has no skill-routing receipt, treat the task as incomplete for maintenance-audit purposes.

## Work Modes

Choose one primary mode before choosing skills:

| Mode | Use When | Main Rule |
|---|---|---|
| Research Mode | literature search, websites, LMS/portals, supervisor/PI/client or public resources, policy, source discovery | use `dissertation-research-search-protocol`; use `dissertation-learning-loop` after useful new reading; separate confirmed source information from interpretation |
| Review Mode | checking proposal, ethics, interview guide, source notes, citations, risks | findings and risks first; use source paths and evidence boundaries |
| Drafting Mode | writing proposals, manuscripts, reports, protocols, stakeholder notes, ethics/compliance wording, Word files | use source-first gate before drafting; use relevant style, style memory, project-delivery, and document-quality gates before delivery |
| Integration Mode | updating project rules, skills, Obsidian, task state, knowledge base | preserve existing project conventions and record what changed |
| Maintenance Mode | false-run checks, system reliability, skill stocktake, workspace surface, automations, knowledge ops | audit first, fix confirmed defects only, and update task state |

## Task Classification

Classify the user's request into one or more categories:

| Task Type | Primary Skills |
|---|---|
| project setup / project type adaptation | `research-project-adapter`, `agent-orchestration`, `dissertation-knowledge-ops` |
| project memory / notes / supervisor discussion | `dissertation-knowledge-ops`, `dissertation-learning-loop`, `supervisor-feedback-loop`, `context-continuity` |
| proposal / manuscript / report / grant writing | `research-project-adapter`, `dissertation-source-first-gate`, `material-passport`, `academic-integrity-preflight`, `cognitive-frameworks`, `dissertation-argument-spine`, `dissertation-chapter-plan`, `dissertation-research-review`, `academic-self-review-loop`, `authorial-voice-integrity`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate` |
| ethics / compliance / participant materials | `dissertation-source-first-gate`, `responsible-ai-agent-audit`, `dissertation-research-review`, `dissertation-shared`, `dissertation-document-quality-gate` |
| LMS/module requirements | `dissertation-research-search-protocol`, `dissertation-knowledge-ops`, `dissertation-chapter-plan`, `dissertation-citation-audit` |
| literature search / literature review | `dissertation-research-search-protocol`, `dissertation-learning-loop`, `dissertation-literature-review`, `cognitive-frameworks`, `dissertation-argument-spine`, `dissertation-citation-audit`, `academic-self-review-loop` when drafting formal synthesis |
| bounded source planning / reading priority sorting | `dissertation-source-first-gate`, `dissertation-research-search-protocol`, `dissertation-citation-audit`, `dissertation-learning-loop`, `context-continuity`; do not add the full formal-writing chain unless the user asks for formal prose, Word/DOCX, stakeholder-facing output, submission-facing output, or protected source-of-record edits |
| bounded research lookup | `dissertation-research-search-protocol`, `dissertation-citation-audit`, `context-continuity`; label metadata-only, source-section-reviewed, or evidence-insufficient status and do not update source registers without confirmation |
| minor edit / typo / citation-key formatting | `dissertation-source-first-gate`, `dissertation-citation-audit`, `context-continuity`; preserve the no-substantive-change boundary and do not upgrade citation readiness |
| research questions / methodology | `cognitive-frameworks`, `dissertation-argument-spine`, `dissertation-research-review`, `dissertation-chapter-plan`, `academic-self-review-loop` when drafting formal prose |
| Stage Continuity triggered deliverable | `context-continuity`, `cognitive-frameworks`, `dissertation-source-first-gate`, `dissertation-argument-spine`, `dissertation-research-review` |
| interview guide / data collection | `qualitative-theme-audit`, `responsible-ai-agent-audit`, `dissertation-research-review` |
| confirmed design-elicitation / co-design outputs | `qualitative-theme-audit`, `responsible-ai-agent-audit`, `dissertation-research-review`; restore archived co-design/design-spec skills only after Maintenance confirms a recurring dedicated deliverable |
| AI agent concept / prototype | `cognitive-frameworks`, `responsible-ai-agent-audit`, `dissertation-research-review`; restore archived design/prototype skills only for a dedicated specification or prototype audit |
| adoption conditions | `responsible-ai-agent-audit`, `cognitive-frameworks`, `dissertation-research-review` |
| active learning or intervention design | `cognitive-frameworks`, `responsible-ai-agent-audit`, `dissertation-research-review`; restore archived topic packs only when this is a concrete project phase |
| teaching knowledge base / RAG plan | `dissertation-knowledge-ops`, `dissertation-research-search-protocol`, `context-continuity` |
| unclear research route / high-impact idea / early design discussion | `brainstorming`, `dissertation-argument-spine`, `dissertation-research-review` |
| file-to-Markdown conversion / source ingestion from documents | `markitdown`, `dissertation-source-first-gate`, `dissertation-knowledge-ops`, `dissertation-learning-loop` |
| learning loop / source ingestion | `dissertation-learning-loop`, `dissertation-knowledge-ops`, `context-continuity` |
| academic writing / authorial voice / AI-style cleanup | `authorial-voice-integrity`, `academic-integrity-preflight` when disclosure or prompt-residue risk appears, `academic-self-review-loop`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate` |
| rubric / marking criteria / journal / funder / client requirement audit | `research-project-adapter`, `dissertation-source-first-gate`, `dissertation-research-search-protocol`, `dissertation-argument-spine`, `dissertation-research-review`, `dissertation-citation-audit`, `dissertation-chapter-plan` |
| LMS / portal / requirement / deadline / word count / submission rule | `research-project-adapter`, `dissertation-source-first-gate`, `dissertation-research-search-protocol`, `dissertation-knowledge-ops`, `dissertation-document-quality-gate` |
| major chapter rewrite / argument audit | `dissertation-argument-spine`, `dissertation-research-review`, `dissertation-citation-audit` |
| final review / defense / viva | `dissertation-research-review`, `context-continuity`; restore archived `viva-prep` only when a thesis/dissertation defense phase is active |
| long task / context handoff / compaction risk | `context-continuity`, `dissertation-knowledge-ops` |
| formal document delivery / QA | `cognitive-frameworks` when argument planning is needed, `academic-self-review-loop`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate`, `context-continuity` |
| agent self-debug / false-run recovery | `dissertation-agent-self-debug`, `dissertation-workspace-surface-audit`, `context-continuity` |
| GitHub release / public template visible-surface verification | `release-surface-verification`, `dissertation-agent-self-debug`, `dissertation-workspace-surface-audit` when live browser or rendered-surface checks are needed |
| agent architecture audit / rule conflict | `dissertation-agent-architecture-audit`, `dissertation-skill-stocktake`, `context-continuity` |
| workspace surface audit | `dissertation-workspace-surface-audit`, `dissertation-automation-audit`, `dissertation-knowledge-ops` |
| browser automation / LMS browser inspection / local page verification | `playwright-dissertation-browser`, global `playwright`, `dissertation-research-search-protocol` when source capture is involved |
| automation / hook / connector audit | `dissertation-automation-audit`, `dissertation-workspace-surface-audit`, `context-continuity` |
| skill stocktake / skill quality review | `dissertation-skill-stocktake`, `dissertation-agent-architecture-audit`, `context-continuity` |
| knowledge system maintenance | `dissertation-knowledge-ops`, `dissertation-workspace-surface-audit`, `context-continuity` |
| agent system maintenance / bug check | `dissertation-agent-self-debug`, `dissertation-agent-architecture-audit`, `dissertation-skill-stocktake`, `dissertation-workspace-surface-audit`, `context-continuity` |
| project skill/rule migration | `using-superpowers`, `project-skill-creator-governance`, global `skill-creator`, `dissertation-skill-stocktake`, `dissertation-agent-architecture-audit`, `dissertation-document-quality-gate`, `context-continuity` |
| Superpowers-style workflow request | `using-superpowers`, `brainstorming` when idea/design is unclear, then the relevant dissertation or maintenance skills |

## Skill Selection Rules

When creating or updating Codex skill files, use the system `skill-creator` skill if it is available. For external workflow migration, audit first, then adapt into existing dissertation skills unless the user explicitly asks for a new active skill.

For project skill creation or updates, use `project-skill-creator-governance` before global `skill-creator`. Do not copy global `skill-creator` or global `playwright` into `.agents/skills/` unless the user explicitly asks for frozen local copies.

Archived adapter or topic-pack skills under `.agents/archived-skills/` are outside the active discovery root and are not routing targets. If a task appears to need one, first use the active core route and only move the required pack back into `.agents/skills/` after Maintenance confirms a recurring project-phase need that justifies the added context load.

For Superpowers-style workflows, use `using-superpowers` as an adapter. It must not override source-first, rubric evidence, document-quality, privacy, or window-separation rules.

For file-to-Markdown conversion, use `markitdown` only after checking tool availability and privacy boundaries. If MarkItDown is unavailable, do not install it without explicit confirmation.

Use one skill when:

- the task is narrow and has one clear output
- the user asks for a quick answer
- the task touches sensitive participant material
- the task involves final wording for ethics or assessed submission

Use multiple skills when:

- the task spans proposal + ethics + interview materials
- the task needs both design and responsible AI review
- the task needs literature + methodology + citation checking
- the task asks for a full project update after new evidence
- LMS/module rules need to be translated into local project plans
- the task needs both source-field extraction and drafting/revision

## Source-First Gate

For formal documents, apply this gate before writing:

1. Identify source documents and existing filled fields.
2. Extract confirmed facts into a short source map.
3. Distinguish confirmed facts from assumptions and `TO CONFIRM` fields.
4. Check whether the document is a fixed template. If so, preserve fixed wording and only replace clearly editable placeholders.
5. Draft or revise only after this source map exists.

Use the dedicated `dissertation-source-first-gate` skill for full instructions when the task involves formal documents, personal/admin facts, official requirements, participant-facing materials, citations, or stakeholder-facing drafts.

For rubric, grade-band, marking criteria, LMS/portal requirements, journal/funder/client requirements, deadlines, word counts, or submission rules:

- read the strongest available project requirement source
- read `university-guidance/RUBRIC_EVIDENCE_GATE.md` when assessed academic grading is relevant
- check local source files before answering
- state whether the answer is based on official original text, a local LMS summary, inference, or insufficient evidence
- do not treat local summaries as complete official wording

For school templates with colored guidance:

- inspect text color, placeholders, and optional bracketed instructions before editing
- preserve black fixed template text unless the template or user explicitly says it can be changed
- replace blue `xxx` or blue guidance only with source-grounded or clearly marked draft wording
- remove unused optional guidance before final submission

## Subagent Decision Rules

Consider subagents under the user's standing permission, but apply the safety and usefulness tests below.

Use subagents when:

- at least two subtasks can run independently
- the task benefits from separate reviewer/explorer perspectives
- one agent can search/read external or LMS content while another audits local files
- one agent can draft while another reviews requirements or risks
- outputs can be merged without conflict

Avoid subagents when:

- the next action depends on one specific answer
- the task requires direct editing of the same files by multiple agents
- the task contains sensitive raw participant data
- the user asks for a short answer
- the work is mostly a single ethics/proposal wording decision

## Recommended Subagent Patterns

For broad research:

- Agent 1: literature/resources search
- Agent 2: local project gap audit
- Main agent: synthesis and final decision

For LMS/module requirement work:

- Agent 1: LMS requirement extraction, read-only
- Agent 2: local file alignment audit
- Main agent: update local files after user confirms

For proposal/ethics preparation:

- Agent 1: proposal structure and rubric alignment
- Agent 2: ethics/privacy/risk review
- Main agent: consolidate into submission-ready draft

For AI agent design:

- Agent 1: pedagogical/active learning fit
- Agent 2: responsible AI and adoption risks
- Main agent: design specification and traceability

## Safety Controls

- Do not send sensitive raw participant data to subagents unless the user explicitly permits it and data is anonymized.
- Do not let subagents make overlapping edits to the same file.
- Main agent must review and integrate subagent outputs.
- Mark uncertain claims as `TO CONFIRM`.
- Preserve source paths for all evidence.
- For LMS or university rules, keep a local summary and include the date captured.
- Use `dissertation-document-quality-gate` before delivering important Word files or formal project outputs.
- Use `research-wiki/DOCUMENT_PIPELINE.md` for important Word, PDF, or stakeholder-facing outputs so thinking, writing, and delivery checkpoints are recorded or explicitly marked not applicable.

## Output Format

For complex tasks, briefly state:

1. task classification
2. skills selected
3. whether subagents are used and why
4. files to be read or updated
5. any safety limits

For simple tasks, do not over-explain; just use the relevant skill and proceed.

For substantial Production tasks, the final delivery or run receipt must also include:

- selected skills and reason
- skills skipped because they were not needed
- subagent decision
- gates completed or not completed
- files created or updated
