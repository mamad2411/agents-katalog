---
name: design-decision-audit
description: Audit design documents for missing decisions, compatibility risks, rollout gaps, and observability omissions. Use whenever the user asks to review a design doc, architecture proposal, implementation-facing design, plan, or design-adjacent markdown file for completeness, migration strategy, rollback, data handling, or suggested additions without directly editing the document. Also trigger on short requests such as `review <file>.md` or `audit <file>.md` when the target looks like a design, plan, architecture, proposal, or decision document.
---

# Design Decision Audit

## Overview

Use this skill to audit a design document before implementation.
The job of this skill is to find missing or weak design decisions, explain the risk, and propose targeted additions.

This skill does not directly edit the design document unless the user explicitly asks for that in a later step.

## Inputs

Required input:
- A design document path, design document content, or both

Optional input:
- Extra context paths such as related design docs, implementation plans, or requirement notes

## Language Strategy

Match the audit language to the user's instruction language.

Use this priority order:
1. An explicit output-language request from the user
2. The dominant natural language of the user's current instruction
3. The dominant natural language of the most recent user instructions in the same task
4. English if the signal is weak or ambiguous

Rules:
- Keep the chat response and any saved report in the same language
- Translate section headings into the chosen output language
- Keep file paths, code identifiers, and literal config keys unchanged
- Do not mix languages unless the user explicitly asks for bilingual output

Default heading examples:

If the output language is English:
- `Executive Summary`
- `Triggered Modules`
- `Findings`
- `Suggested Additions`
- `Open Questions`
- `Report Path`

If the output language is Chinese:
- `Executive Summary` → translate heading
- `Triggered Modules` → translate heading
- `Findings` → translate heading
- `Suggested Additions` → translate heading
- `Open Questions` → translate heading
- `Report Path` → translate heading

## Minimal Prompt Handling

Do not require the user to spell out the full audit scope.

If the user gives a short instruction such as:
- `review <file>.md`
- `audit <file>.md`
- `check <file>.md`

infer a full design-decision audit when the target appears to be one of these:
- design doc
- architecture proposal
- implementation plan
- checklist-backed review doc
- proposal or decision record

Strong clues include:
- filename terms such as `design`, `review`, `plan`, `proposal`, `architecture`, `decision`
- repo locations such as `docs/`, `design-docs/`, `exec-plans/`, `proposals/`
- document content that describes rollout, schema, compatibility, migration, states, jobs, or observability

When a short prompt names a markdown file but the document type is still unclear:
- open the file first
- if the file reads like a design, plan, or architecture doc, proceed with the audit
- ask a clarifying question only if the file is clearly not design-adjacent and running this skill would likely be wrong

## Context Strategy

Always read the target design document before forming conclusions.

If the user provides additional document paths, read them when they affect compatibility, migration, or design intent.

Honor explicit user scoping before inheriting ambient repo conventions.
Examples:
- "Treat this as a standalone doc"
- "Do not use the current repo rules"
- "Use only the checklist I provided"

When the user explicitly narrows the rule source:
- use only the files and instructions explicitly named by the user
- do not inherit unrelated repo standards just because they exist nearby
- do not infer a repo report directory from the current workspace unless the user asked for saving

When the document is explicitly marked as draft, WIP, or incomplete (e.g., contains "WIP", "draft", "TBD", "work in progress" in the title, frontmatter, or first section):
- Note the draft status in the Executive Summary
- Downgrade all `[GAP]` findings by one priority level (`P1` → `P2`, `P2` → `P3`)
- Prefix downgraded gap findings with `[DRAFT]` to signal the author likely knows these are missing
- Keep all `[RISK]` and `[ASSUME]` findings at their original priority — a wrong decision is still wrong in a draft

If the user does not override the scope and the repo contains project-standard files, inherit them instead of ignoring them.
Typical examples:
- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/design-docs/*checklist*.md`
- other review standards or design templates explicitly referenced by the user

When project-standard files exist, resolve them in this order:
1. Explicit user instructions in the current task
2. Explicitly provided checklist or standard files
3. Repo-wide review contracts such as `AGENTS.md` or `CONTRIBUTING.md`
4. Repo checklist or template files that are clearly design-review specific
5. Default rules in this skill

When multiple candidate repo files exist at the same priority:
- prefer the file whose title or filename most clearly matches design review, design decision, or architecture review
- prefer the file closest in scope to the target document
- ignore release, implementation, or deployment checklists unless the user asked for them
- ask the user only if competing files would likely change the audit conclusion

When project-standard files exist and are in scope:
- follow their review contract
- follow their finding-ID format if one is explicitly required
- follow their report location if one is explicitly required
- use their design checklist to refine or override the default checklist in this skill

When project-standard files do not exist:
- use the default review scope and checklist defined in this skill

## Core Goal

Produce a structured audit that answers three questions:

1. Which important design decisions are already explicit?
2. Which important design decisions are missing, weak, or contradictory?
3. What exact content should be added to make the design reviewable and implementation-safe?

## Default Review Scope

When the repo does not define a stricter review scope, audit these dimensions:
- Correctness and project standards
- Performance bottlenecks
- KISS and DRY
- Observability: logs, metrics, alerts
- Idempotency and data consistency

Then audit the design against this default checklist:
- Migration and cutover
- Data handling
- Schema and storage
- Backward compatibility
- Observability

Only add conditional modules when the design actually triggers them.

## Default Conditional Modules

Use the repo checklist when one exists.
Otherwise use these default module triggers.

Trigger a module only when the design clearly matches its signals.
Do not force every module into every audit. If a module does not apply, omit it.

| Module | Trigger signals |
|--------|----------------|
| Semi-structured payloads | JSON fields, dynamic columns, flexible schema, payload validation, extensible attributes, `interface{}` or `any` typed storage |
| Performance and indexing | query patterns, index design, pagination, bulk reads/writes, hot-path latency, large table scans |
| State machine or orchestration | status transitions, state enum, workflow steps, job scheduling, retry logic, FSM diagrams |
| Concurrency and locking | mutex, row-level lock, optimistic lock, concurrent writers, race condition mitigation, distributed lock |
| Async jobs and failure isolation | background jobs, queues, workers, dead-letter queues, retry with backoff, at-least-once delivery |
| Human review | manual approval steps, escalation paths, review SLA, operator action required |
| Audit and compliance | audit log, PII handling, data retention, GDPR/CCPA, regulatory requirements, immutable records |
| Scan and alert design | scheduled scans, anomaly detection, alert thresholds, on-call routing, runbook references |

## Default Finding Contract

If the repo defines a finding format, priority scheme, or review contract, follow the repo contract.
Otherwise use the defaults below.

## Findings Standard

Rules:
- Use thread-unique IDs
- Default ID format: `CR01 [P1] [GAP]` — priority tag followed by type tag
- Order findings from highest priority to lowest priority
- Treat `P0` and `P1` as merge-blocking by default
- Do not give conclusion-only findings
- If there are findings, use a flat bullet list and keep the full prefix on every item
- If there are no findings, use the Verified Checklist format described below

Default priorities:
- `P0`: merging or deploying will **necessarily** cause at least one of: data corruption, service unavailability, security vulnerability, or no rollback path
- `P1`: damage is possible but requires specific conditions to trigger, OR a design gap that prevents engineers from safely proceeding with implementation
- `P2`: meaningful correctness or operability risk that is unlikely to cause immediate harm but degrades reliability or maintainability
- `P3`: minor but real improvement with no production risk

Finding type tags — always include one per finding:
- `[GAP]`: a required decision is absent from the document
- `[RISK]`: a decision exists but is incorrect, contradictory, or dangerously incomplete
- `[ASSUME]`: the design implies a decision that was never made explicit; flag the hidden assumption

Explain each finding in this order:
1. What the issue is
2. How the current design triggers it
3. One concrete example
4. Why it matters to this change

Use expected behavior versus current behavior when that comparison makes the risk clearer.

Do NOT write conclusion-only findings. Examples:

BAD:
- `CR01 [P1] [GAP]: Migration strategy is unclear and may cause data loss.`
- `CR02 [P2] [RISK]: Observability is insufficient.`

GOOD:
- `CR01 [P1] [GAP]: The design does not specify how the job handles partial failures. If the job inserts 500 rows and fails at row 300, there is no rollback or resume mechanism described. Re-running the job would create duplicate rows unless the caller enforces idempotency externally.`
- `CR02 [P2] [RISK]: The rollback plan in step 4 says "revert the migration" but the migration is destructive (column drop). A revert would require restoring from backup, which is not mentioned. Operators following this plan would have no path forward during an incident.`

## No-Findings Protocol

When there are no findings, do not write only `No findings identified.`

Instead, produce an explicit verified checklist that confirms what was checked and what was not triggered:

```
No findings identified.

Verified:
- ✓ <dimension>: <one sentence confirming what was checked and what was found sound>
- ✓ <dimension>: ...

Skipped (not triggered):
- <Module name>: <one-line reason why it was not triggered>
```

Example:
```
No findings identified.

Verified:
- ✓ Migration strategy: gradual rollout with feature flag and dual-write described; rollback path explicit
- ✓ Idempotency: job uses upsert on unique constraint; safe to re-run
- ✓ Observability: structured log on every state transition; alert threshold defined

Skipped (not triggered):
- State machine module: no status transitions in scope
- Concurrency and locking module: single-writer path only
```

## Suggested Additions Standard

After findings, provide suggested additions that the author can copy into the design document.

Suggested additions must be:
- Concrete
- Short
- Decision-oriented
- Grouped by section or topic
- Based on the recommended repair option, not every option

Do not write generic advice such as "consider adding more detail".
Write the missing decision directly.

Good example:
- `Migration Strategy`: Use gradual rollout behind a feature flag. Keep reads on the legacy path for one release while dual-writing the new field. Roll back by disabling the flag and stopping dual-write.

Bad example:
- `Migration Strategy`: Add more migration details.

## Remediation Options Standard

For every material finding, compare repair options instead of giving only one answer.

Apply this rule to:
- all `P0`
- all `P1`
- all `P2`

Do not apply this rule to:
- `P3` findings unless the user explicitly asks for option analysis
- no-finding reviews

For each applicable finding, create exactly three distinct repair options:
- `Option A`
- `Option B`
- `Option C`

The three options must differ in approach or trade-off.
Do not create fake variety by rewording the same solution three times.

Then choose one recommended option and explain why it is best for the current design.
Also explain briefly why the other two options were not selected.

Keep the comparison concise:
- use one compact markdown table for the three options
- one short paragraph for the recommendation
- one short line per rejected option

The options table should prefer these columns:
- `Option`
- `Approach`
- `Pros`
- `Trade-offs`

Do not add more columns unless the user explicitly asks for deeper analysis.

Good comparison dimensions:
- implementation complexity
- rollback safety
- compatibility risk
- runtime cost
- operability
- long-term maintainability

Bad comparison dimensions:
- vague preference
- duplicated wording
- generic statements such as "less ideal"

If the design is clearly blocked by one finding, the recommended option should prefer safety and reversibility over speed.

## Output Calibration

Scale remediation verbosity to document complexity.

For short or simple documents (under 300 words, or fewer than 3 triggered modules, or all findings are P3):
- Collapse the three-option table into a single recommended approach plus one-line trade-off note
- Do not suppress findings — only reduce remediation prose
- Example: `Recommended: use a feature flag for rollout. Trade-off: adds one release cycle of flag management overhead.`

For complex documents (5 or more triggered modules, or any P0 finding, or more than 6 findings total):
- Apply the full three-option table format for every P0–P2 finding
- Do not abbreviate option analysis

Default to the full format when complexity is unclear.

## Output Format

Always use this structure in the chat response:

```markdown
# Design Audit
## Executive Summary
## Triggered Modules
## Findings
## Suggested Additions
## Open Questions
## Report Path
```

Section rules:
- `Executive Summary`: 2 to 5 sentences on overall audit posture
- `Triggered Modules`: list only the modules actually used; if none apply, write `- None`
- `Findings`: include the chosen `XX [P#]` items or state `No findings identified.`
- `Suggested Additions`: grouped by section heading or topic
- `Open Questions`: include only questions that materially block confident review
- `Report Path`: this section must always exist
- if a report file was written, include the saved path
- if the task is chat-only and no file was required, write `- Chat only (not requested)`

Use section names in the chosen output language while preserving the same logical structure.

Within each applicable finding, use this sub-structure:
- finding statement (include type tag: `[GAP]`, `[RISK]`, or `[ASSUME]`)
- `Options`
- `Recommended Option`
- `Why Not Others`

Within `Options`, use a markdown table instead of prose whenever possible.

Do not replace the required sections with a free-form review.
Even short audits must keep the exact section names.

For `Suggested Additions`:
- Write copy-ready sentences, not reminders
- Use only the recommended option when turning analysis into suggested document text
- Prefer section labels such as `Migration Strategy`, `Rollback Plan`, `Observability`, `Consumer Impact`
- If there are no useful additions, say `No suggested additions.`

## Report File

Save a report file only when one of these is true:
- the user explicitly asks to save the report
- the repo has an obvious existing report directory and the task implies report persistence

Preferred path selection:
1. Use a path explicitly requested by the user
2. Use the repo's established report directory if one clearly exists, such as `docs/reports/`, and repo conventions are in scope
3. If the task clearly requires saving but no path can be inferred, ask the user where to save the report
4. Otherwise keep the result in the chat only

If writing a report file:
- use the current local date in the repo timezone
- derive `<topic>` from the design document filename when possible
- use a short stable fallback such as `design-audit` when needed
- keep the file sections aligned with the chat response

Do not claim the report path unless the file has actually been written.

## Workflow

### Phase A: Context Preparation

Goal: Build a complete context package and perform default checklist audit.

1. Read the design document.
2. Determine the audit output language from the user instruction.
3. Read repo-standard files when present and relevant.
4. Read user-provided context files that affect scope or intent.
5. Determine whether the user explicitly limited the audit to standalone mode or named files only.
6. Resolve the review contract, finding format, checklist, and report-path conventions using the priority order in this skill.
7. Determine which conditional modules are triggered.
8. **Default checklist audit**: Audit the design against the 5 default dimensions (correctness and project standards, performance bottlenecks, KISS and DRY, observability, idempotency and data consistency). Record these as preliminary findings.
9. **Assemble context package**: Combine the design document content, repo standards, review contract, draft status, and triggered module list into a structured context package for Phase B.

### Phase B: Parallel Module Audit

Goal: Audit each triggered conditional module in parallel using specialized subagents.

**When no modules are triggered**: Skip Phase B entirely. Use only Phase A preliminary findings.

**When one or more modules are triggered**:

10. For each triggered conditional module, launch a parallel Sonnet subagent:
    - Read the agent template at `skills/design-decision-audit/agents/module-auditor.md`
    - Fill in the template parameters:
      - `{{MODULE_NAME}}`: the module name (e.g., "State Machine and Orchestration")
      - `{{TRIGGER_SIGNALS}}`: the trigger signals that matched this module
      - `{{DESIGN_DOC}}`: the design document content
      - `{{REPO_STANDARDS}}`: repo standards content (or "None" if standalone)
      - `{{REVIEW_CONTRACT_SECTION}}`: review contract if one exists (or empty)
    - Use the filled template as the subagent prompt
    - Each subagent runs independently with no shared state

11. Collect findings from all subagents as they complete.

**Fallback**: If a subagent fails or times out, the main agent audits that module inline using the same dimension scope.

### Phase C: Synthesis

Goal: Merge, deduplicate, prioritize, and format all findings into the final audit output.

12. **Merge findings**: Combine Phase A preliminary findings (default checklist) and Phase B findings (module audits) into a single list.

13. **Deduplicate** using this decision tree:
    - Two findings describe the same issue at the same location → merge into one, keep the finding with richer detail. If from different sources, append `[CROSS-VALIDATED]` to the finding tag.
    - Two findings share a root cause but describe different manifestations → keep both, add cross-references (e.g., "see also CR01").
    - Unsure whether two findings overlap → keep both, do not merge.

14. **Assign final IDs**: Number findings as CR01, CR02, ... in priority order (P0 first, then P1, etc.).

15. **Token guard**: If the merged findings text exceeds roughly 4000 tokens, keep all P0 and P1 findings in full. For P2 and P3, keep only the summary line and defer detail to the report file.

16. **Generate repair options**: For each P0 to P2 finding, generate three distinct repair options and recommend the best one. Apply Output Calibration rules (full table for complex documents, collapsed format for simple ones).

17. **Write suggested additions**: Based on the recommended options, produce copy-ready additions grouped by section or topic.

18. **Draft handling**: If the document was marked draft/WIP, downgrade `[GAP]` findings by one priority level and prefix with `[DRAFT]`.

19. **Format output**: Assemble the final response using the required six-section structure (Executive Summary, Triggered Modules, Findings, Suggested Additions, Open Questions, Report Path).

20. **Save report**: If the task requires saving, write the report file. If no save path can be inferred, ask the user.

21. Return the structured audit response with the report path in the chosen language.

## Boundaries

Do:
- Audit the design document
- Call out missing or weak decisions
- Propose concrete additions
- Compare repair options for material findings and recommend the best one
- Save a report file when required by the task or repo convention
- Make the triggered checklist scope explicit
- Keep the response reviewable by a human without extra interpretation

Do not:
- Edit the design document directly
- Generate an implementation plan unless the user asks for one
- Expand into code review unless the user changes scope
- Ask unnecessary questions if the missing information can be identified as a design gap
- Collapse the audit into informal prose
- Omit the report path or the triggered module declaration

## Escalation Rules

Ask a short blocking question only when:
- The target design document is not identifiable
- The repo contains multiple candidate docs and the correct one is ambiguous
- A missing context file is necessary to avoid a likely wrong conclusion
- Multiple in-scope standards conflict and the choice would likely change the audit result
- The task requires a saved report but no report path can be inferred from the user request or repo conventions

Otherwise, continue the audit and list the uncertainty under `Open Questions`.

## Quality Bar

Before finishing, check these points:
- The response has all six required sections
- `Triggered Modules` is explicit, even when empty; each triggered module names the signals that fired it
- Findings follow the repo-required format, or `CRXX [P#] [TYPE]` when no repo format exists
- Every finding includes a type tag: `[GAP]`, `[RISK]`, or `[ASSUME]`
- No finding is conclusion-only — each one states what, how, a concrete example, and why it matters
- Every `P0` to `P2` finding contains repair options, one recommendation, and brief rejection reasons
  - Full three-option table for complex documents
  - Single recommended approach + one-line trade-off for short/simple documents
- `Suggested Additions` reflect the recommended option rather than repeating all options
- If there are no findings, the response uses the Verified Checklist format (not just `No findings identified.`)
- If the document was marked draft/WIP, `[GAP]` findings are downgraded one level and prefixed `[DRAFT]`
- The chat response and saved report use the same inferred output language
- Suggested additions are copy-ready
- Explicit user overrides beat ambient repo conventions
- If the task requires saving, a report path was either written or explicitly confirmed by the user
