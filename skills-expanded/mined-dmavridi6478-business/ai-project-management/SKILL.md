---
name: ai-project-management
description: Run project management with Claude as the working layer — planning (WBS, milestones, dependencies), schedule management (critical path, buffers), cost management (budget variance, earned value), resource management (allocation, RACI), quality management (acceptance criteria, defect tracking), procurement (vendor selection, contract tracking), and status reporting. Use when asked to plan a project, build a project tracker/dashboard, report project status, or manage schedule/budget/resource/quality/procurement for an active project.
---

# AI-Assisted Project Management

Source: prompted by reviewing a social-media "AI-Powered Project Management with Claude" infographic that turned out to be unreliable on inspection — duplicate/conflicting section numbers (two sections labeled "7," two labeled "AI Tools for Project Managers" with completely mismatched content), fabricated-looking metrics (identical percentages repeated across unrelated rows), and garbled labels throughout every panel. None of that is repeated here. This is real project-management methodology, written fresh, with Claude's actual role in each part called out rather than assumed.

## 1. Project planning

- **Work Breakdown Structure (WBS)**: decompose the project into deliverables, then tasks under each deliverable, small enough that each task has a single clear owner and a checkable "done" state. A WBS that's really just a restated task list (no hierarchy) hasn't done its job — it should reveal dependencies and gaps that a flat list hides.
- **Milestones**: dated checkpoints tied to a deliverable being complete, not calendar markers ("halfway point"). A milestone with no deliverable behind it doesn't tell you anything when it's missed.
- **Dependencies**: mark what blocks what before scheduling — this is what determines the critical path in step 2, not the other way around.

Claude's role here: turn a rough scope description into a structured WBS and dependency map, and flag missing dependencies a first draft usually omits (cross-team handoffs, external/vendor-owned tasks).

## 2. Schedule management

- **Critical path**: the longest chain of dependent tasks — this determines the earliest possible finish date, and any slip on it slips the whole project. Tasks off the critical path have slack; tasks on it don't.
- **Buffers**: protect the plan's most uncertain estimates (novel work, external dependencies) with schedule buffer, not by padding every task equally — padding everything hides where the real risk is.
- **Tracking**: compare actual progress against the plan on a cadence that matches project pace (weekly for most projects), and treat a schedule variance as a signal to investigate the *cause*, not just a number to report.

Claude's role here: compute/re-derive the critical path when tasks or dependencies change, and flag when a schedule slip on a non-critical task has quietly become critical because of accumulated delay.

## 3. Cost management

- **Budget baseline**: set once, changed only through a deliberate change-control process — a budget that silently drifts with every re-forecast isn't a baseline.
- **Earned Value Management (EVM)**, the standard way to know if a project is actually on track rather than just "spending on schedule":
  - **CPI (Cost Performance Index)** = earned value / actual cost. Below 1.0 means over budget for the work actually completed.
  - **SPI (Schedule Performance Index)** = earned value / planned value. Below 1.0 means behind schedule.
  - **EAC (Estimate at Completion)** = a forecast of total cost based on current CPI, not the original budget — the number that matters for "will we finish on budget."
- A project can be under budget in raw spend and still be in trouble if CPI/SPI show little was actually delivered for that spend — track the ratio, not just the dollar total.

Claude's role here: compute CPI/SPI/EAC from raw actuals-vs-planned data, and translate what the ratios mean in plain language for a status report.

## 4. Resource management

- **Allocation**: assign people to tasks against actual capacity (accounting for existing commitments), not against an idealized 100%-available week.
- **RACI** (Responsible / Accountable / Consulted / Informed): one person Accountable per deliverable, even when several are Responsible for pieces of it — ambiguity here is where deliverables fall through gaps.
- **Overallocation**: flag it explicitly when it happens rather than letting a resource silently carry more committed work than capacity allows — it's the leading cause of schedule slip that a schedule-only view misses.

Claude's role here: cross-reference the WBS/schedule against a team's existing commitments and surface overallocation before it causes a slip, not after.

## 5. Quality management

- **Acceptance criteria**: defined per deliverable *before* work starts, specific enough that "done" isn't a judgment call at delivery time.
- **Defect tracking**: log against the deliverable and its acceptance criteria, not as a generic bug list — a defect that doesn't map to a stated criterion usually means the criteria were incomplete, which is itself worth flagging.
- **Audits**: sample-check completed work against criteria on a cadence, rather than only at final delivery when a systemic quality issue is expensive to fix.

Claude's role here: draft acceptance criteria from a deliverable description, and check delivered work against stated criteria directly rather than a generic quality pass.

## 6. Procurement management

- **Vendor selection**: score against criteria defined before proposals arrive (not adjusted after seeing them), covering price, capability match, and delivery track record — not price alone.
- **Contract tracking**: key dates (delivery milestones, renewal/termination windows, payment terms) tracked against the schedule from step 2, since a vendor delay becomes a project delay the moment its output is on the critical path.
- **Purchase/requisition tracking**: separate from contract tracking — a contract being signed doesn't mean the goods/services have actually been delivered against it.

Claude's role here: cross-check vendor contract dates against the project schedule and flag when a vendor deliverable sits on the critical path — that's the scenario where a vendor slip is most costly and least visible until it's already late.

## 7. Reporting

- **Status reports**: lead with the RAG (Red/Amber/Green) status per workstream and *why* — a status report that's all narrative and no clear status, or all status with no reasoning, is equally unhelpful to a reader deciding whether to intervene.
- **Executive summary**: budget/schedule/quality health in one line each, with the EAC and critical-path status from steps 2-3, not a restated task list.
- Report the trend, not just the current number — "CPI has been declining for 3 weeks" is more actionable than "CPI is 0.94" alone.

Claude's role here: assemble the report from the actual underlying data (schedule, budget, RACI, defect log) rather than from a status narrative alone — and flag when the narrative and the underlying numbers disagree.

## AI tools worth knowing about (verified, not guessed)

The reviewed infographic's tool table was too garbled to trust (names like "Gumial AI" and "Nutian AI" don't resolve to anything real) — rather than guess, here's what's actually verifiable: general-purpose assistants (Claude, ChatGPT, Gemini) apply directly to every section above via prompting; several PM-specific platforms ship their own AI features (Notion AI for docs/summarization, ClickUp's AI features for task/summary generation, Atlassian Intelligence in Jira for backlog/ticket assistance, Microsoft Copilot in Project/Planner, Power BI Copilot for report narration). Verify current capabilities directly with each vendor before relying on a specific claim — this space changes fast enough that a static list goes stale within months.

## Related skills in this repo

- **business-decision-frameworks**: use for *prioritizing* which projects/initiatives to run — this skill is for managing one once it's underway.
- **quarterly-okr-architect**: sets the goals a project should ladder up to; this skill tracks the execution against them.
- **business-intelligence-report** / **ceo-reporting-skill**: for a project status report going to leadership, use this skill's RAG/EAC/trend approach as the input, those skills' format as the output.
- **mcp-integration-scout** (agent): check before assuming a specific PM tool (Jira, Linear, Asana) is connected — several are referenced in this repo's own MCP setup already (see the main README's MCP Servers section).
