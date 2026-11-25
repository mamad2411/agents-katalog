---
name: night-shift-workflow
description: Design and govern an autonomous, scheduled Claude workflow that runs unattended (overnight, on a cron, or on a recurring trigger) and hands the user a decision-ready brief instead of raw output when they return — e.g. a morning decision brief, a recurring status digest, or any "gather → triage → prepare → deliver" background job. Use this whenever the user wants to automate a recurring check/report/brief, asks to "run this every morning/night," wants Claude to "work while I'm away," is setting up a scheduled task/Routine/cron job, or is deciding what an autonomous agent should be allowed to do unattended vs. what needs human sign-off. Pairs with the `night-shift-canvas` procedure for the six design decisions to nail down before scheduling anything.
---

# Night Shift Workflow

Source: "Your AI Should Start Working Before You Do — Claude's Night Shift" carousel (@parm.ai). A framework for building a scheduled Claude workflow that does real preparation work unattended — gathering, comparing, triaging, and drafting — and hands back a decision-ready brief, not a raw summary, while keeping humans in control of anything consequential.

## Core distinction: a chat session waits for you; a scheduled workflow runs because the time arrived

The source carousel's "manual routine vs. night shift system" comparison is the whole point of this skill:

| Manual routine | Night shift system |
|---|---|
| Open Claude | Scheduled trigger fires |
| Paste updates | Gather authorized updates from connected sources |
| Request a summary | Analyze and prioritize against yesterday |
| Correct the structure | Draft the brief in a fixed, predictable format |
| Share the result | Flag exceptions and deliver |

A workflow that still requires the user to remember to start it and correct its output isn't automated — it's the same manual routine with extra steps. Real automation means the workflow initiates itself and lands in a state the user can act on immediately.

## The five design decisions (the "Night Shift Canvas")

Before building or scheduling anything, run the `night-shift-canvas` procedure — it walks through six questions (Output, Trigger, Sources, Rules, Actions, Approval). "If one decision is undefined, the workflow is not ready to run unattended" — per the source material, an undefined answer to any one of these isn't a detail to fill in later, it's a sign the workflow isn't ready to schedule yet.

## Triage rules: a summary is not a decision system

Don't hand back an undifferentiated list of everything that happened. Classify each item using four buckets, from the source material:

| Bucket | Criteria | Example |
|---|---|---|
| **Escalate** | Deadline today, financial impact, customer risk, executive decision, or blocked critical work | "Supplier delay — shipment moved to next week" |
| **Review** | Material change, emerging risk, or conflicting information | "Budget variance — +12% vs. forecast" |
| **Include** | Useful context, no immediate action needed | "Product update — new help-center article" |
| **Ignore** | Duplicates, routine notifications, low-value noise | "Newsletter — marketing weekly digest" |

Clear rules produce signal; vague rules produce noise — write the classification criteria down explicitly (not "use judgment") before the first scheduled run, and refine them from what actually shows up, not from a hypothetical list drafted in advance.

## The autonomy boundary: what Claude may do unattended vs. what needs a human

This is the governance core of the skill — match oversight to the stakes, keep a human at the boundary of anything consequential.

**Claude may do unattended:**
- Retrieve authorized information from connected sources
- Compare against a prior state (yesterday, last run) to identify what changed
- Classify urgency using the triage rules above
- Draft the brief in the agreed format
- Prepare recommended actions (a proposal, not an execution)

**Requires human approval before Claude acts:**
- Sending sensitive communications
- Committing money
- Changing critical records
- Approving consequential decisions
- Acting when evidence is incomplete or conflicting

This is the same underlying discipline as this repo's `web-task-scoping` skill (Target/Limit/Run/Review) applied to scheduled/background workflows instead of interactive browser tasks — both exist so an autonomous agent stays inspectable rather than accumulating unbounded authority. When a workflow's job touches both categories (e.g. a brief that also drafts an email), split it: the drafting is unattended, the sending is not.

## Mapping this onto what's actually available in this environment

This isn't aspirational — this session has the real primitives the source carousel describes:

| Canvas element | This environment's tool |
|---|---|
| Trigger (scheduled/recurring) | `mcp__Claude_Code_Remote__create_trigger` (a Routine — cron or one-shot, fires into this session or a fresh one) or `CronCreate` for harness-native scheduling |
| Trigger (self-paced/dynamic loop) | `ScheduleWakeup` — used by `/loop` for self-paced recurring checks rather than a fixed cron |
| One-shot future reminder | `mcp__Claude_Code_Remote__send_later` |
| Sources (connected, authorized) | Whatever's live via `ListConnectors`/installed MCP servers (Gmail, Google Calendar, Google Drive, Notion, Slack, etc.) — never assume a source is connected; check before building the workflow around it |
| Managing/updating the trigger later | `update_trigger`, `delete_trigger`, `fire_trigger` (manual on-demand run), `list_triggers` |

Before proposing a Night Shift-style workflow, check what's actually connected (`ListConnectors`) rather than designing around a source that isn't available — this mirrors the `ai-search-visibility` skill's discipline of verifying real connector availability instead of assuming it.

## Output conventions when using this skill

- Always design the deliverable (the brief's exact format/questions) before configuring the trigger — the source material's own ordering: "define the output first, everything else follows."
- State the triage rules explicitly to the user before the first scheduled run, and confirm the human-approval boundary list — don't let a workflow silently drift into taking consequential action because a rule was implied rather than written down.
- When proposing a new scheduled Routine, name the six canvas answers in the proposal so the user can catch a missing one before it goes live, not after a bad unattended run.

## Related skills in this repo

- **web-task-scoping**: The same autonomy-boundary discipline (what an agent may do unattended vs. what needs approval), applied to browser/web tasks instead of scheduled background workflows — apply both together when a scheduled workflow's job involves web automation.
- **ai-search-visibility** / **advisory-board**: Also part of the "personal AI infrastructure" bundle — setting up Claude Code itself as a tool rather than producing a business deliverable directly.
- **business-intelligence-report** / **ceo-reporting-skill**: If the scheduled brief is business/executive-facing rather than personal, those skills' reporting structure and tone apply to the brief's content once this skill has defined its cadence and triage rules.
- **improve-system**: A different kind of recurring self-check (session-signal capture to memory) — same "runs on its own cadence" shape, different purpose (system improvement vs. operational briefing).
- **outbound-campaign-brief**: Applies this skill's Claude-may/human-approval boundary to B2B outbound specifically — building the target list and drafting outreach is autonomous, sending is gated behind explicit approval and a stated send cap.
- **subagent-depth-control**: If a scheduled workflow spawns nested subagents, that skill's depth setting is another lever for controlling how much unattended work (and token cost) happens per run.

## Notes

Source: "Your AI Should Start Working Before You Do — Claude's Night Shift" carousel (@parm.ai / Parm.AI). The "Night Shift Canvas" six-question worksheet is captured as its own procedure (`docs/procedures/night-shift-canvas.md`) so it can be run as a discrete step before scheduling any workflow this skill describes.
