---
name: agent-immune-system
description: Agent Immune System governance skill for maintaining long-term agent instruction health. Also trigger this when the user says "agent immune system" or "instruction health manager." Use before editing AGENTS.md, CLAUDE.md, global/project instructions, or SKILL.md files; after Hermes/review/postmortem findings; after long or failed sessions with instruction confusion; and when rules feel duplicated, bloated, stale, conflicting, autoimmune, or overfit. Produces promotion, demotion, pruning, regeneration, and memory-routing proposals with human approval before active instruction changes.
---

<what-to-do>

Maintain long-term instruction health. Treat AGENTS.md, CLAUDE.md, project instructions, skills, memory reports, issue reports, Hermes findings, and postmortems as inputs to the Agent Immune System.

Do not convert every mistake into a permanent rule. A mistake is an antigen, not automatic memory.

When invoked, produce a concrete instruction-health decision:

1. Identify the evidence being reviewed.
2. Classify whether it is isolated, recurring, damaging, generalizable, already covered, or context-caused.
3. Query available memory/history when relevant: gbrain, `knowledge/incidents/`, reports, issue history, review history, or prior instruction changes.
4. Score promotion cost against future-error reduction.
5. Detect autoimmune risk: duplication, conflicts, exception chains, overcorrection, token burn, or suppression of useful core behavior.
6. Look for regeneration opportunities: can several scar rules become one cleaner principle?
7. Route the finding to the smallest sufficient memory destination.
8. Produce a human-reviewable report. Do not silently edit active instruction files.

Ask one question at a time only when the answer materially changes the decision and cannot be discovered from local files.

</what-to-do>

<supporting-info>

## Mental Model

This skill is the immune system above task execution:

```text
Primary Agent
  -> Project Agent
    -> Skills
      -> Execution

Instruction Health Manager
  -> monitors all layers
  -> governs instruction memory
  -> proposes optimized instruction artifacts
```

Active instructions are the execution contract. This skill governs proposed changes to that contract so AGENTS.md, CLAUDE.md, and SKILL.md files remain the optimized expression of lessons that survived selection pressure.

## Evidence Sources

Inspect only the sources needed for the current review:

- `AGENTS.md`, `CLAUDE.md`, `.codex/AGENTS.md`, `.claude/CLAUDE.md`
- project instructions and README-like agent files
- `skills/*/SKILL.md`
- `_reports/`, `docs/reports/`, `docs/postmortems/`, issue reports
- Hermes/review artifacts
- local `knowledge/` folders inside this skill
- gbrain or other long-term memory systems when available

Never harvest credentials, transcripts, shell history, keychain, or private tokens to reconstruct evidence.

## Workflow

### 1. Frame The Review

State:

- trigger: pre-edit, post-session, review finding, postmortem, periodic audit, or manual request
- scope: global instructions, project instructions, one skill, or one incident cluster
- proposed output: report only, promotion proposal, pruning proposal, regeneration proposal, or hook/adaptor update

### 2. Innate Immune Classifier

Reject active promotion quickly when any are true:

- one-off or low-cost issue
- caused by bad task context rather than reusable agent behavior
- already covered by existing instructions
- duplicate or narrower than an existing principle
- would add more token/cognitive cost than it prevents
- belongs in a project/skill reference rather than global instructions

### 3. Adaptive Immune Classifier

Promote slowly. Require evidence of recurrence, severity, and generality.

Default threshold:

| Signal | Action |
|---|---|
| 1 low/medium issue | Log only |
| 2 similar issues | Watchlist |
| 3 similar issues | Reference antibody candidate |
| 4+ similar issues | Direct inclusion candidate |
| 1 critical general issue | Immediate reference candidate; direct inclusion only with explicit unacceptable-delay risk |
| Old rule with no recent hits | Prune or demote candidate |

### 4. Autoimmune Detector

Find instructions that create more problems than they solve:

- exception chains: "never X, except Y, except Z..."
- duplicate rules in multiple files
- rules that conflict with project-specific guidance
- rules that make agents stop, ask, or refuse when execution is safe
- overly broad bans created from narrow incidents
- old wound rules with no recent hits
- token-heavy policy dumps that do not change behavior

### 5. Regeneration Engine

Prefer cleaner principles over accumulated scars. Ask:

> Can five instructions be replaced by one higher-level principle?

Regeneration proposals should list the old rule cluster, the new principle, behavior preserved, behavior intentionally removed, and risks.

### 6. Memory Router

Choose the smallest sufficient destination:

- tolerate: no write
- inflammation: temporary check with an expiry date or review count
- watchlist: `knowledge/watchlists/` with promotion/demotion criteria
- dormant memory: `knowledge/incidents/` with "do not revisit unless pattern recurs"
- reference antibody: `knowledge/reference-antibodies/`
- active instruction: AGENTS.md, CLAUDE.md, project instruction, or SKILL.md proposal
- deletion/demotion: pruning proposal

Use gbrain as memory backend when available. gbrain remembers; this skill judges.

### 7. Output

For narrow reviews, use quick-review mode:

- evidence
- finding
- harm
- recommended action
- confidence

Use `templates/instruction-health-report.md` as drafting scaffolding for broad audits and `templates/promotion-proposal.md` for active instruction changes.

For deep instruction audits, session reviews, postmortems, or architecture-style comparisons, write the final artifact as a single self-contained HTML file in the current project's `_reports/` directory:

```text
_reports/report-instruction-health-YYYY-MM-DD.html
```

No external CDNs. Use the markdown template only to structure content before rendering the HTML report.

Every broad audit report must include:

- Health score, 0-100
- Promotion candidates
- Demotion/deletion candidates
- Regeneration candidates
- Autoimmune findings
- Memory routing decisions
- Human approval checklist

Do not apply active instruction edits unless David explicitly asks in the current conversation.

## Hooks

Hook scripts live in `hooks/`:

- `claude-instruction-pretool-hook.sh`: detects edits to active instruction files and emits a promotion-gate reminder.
- `claude-instruction-posttool-hook.sh`: logs instruction edits as audit candidates.
- `codex-instruction-hook.sh`: adapter script for Codex/manual invocation because Codex does not expose Claude-style native hook settings in this environment.

See `references/hook-integration.md` before installing or changing hooks.

## Reference Files

- `references/promotion-rubric.md`: when deciding whether a lesson becomes active instruction memory.
- `references/autoimmune-rubric.md`: when evaluating harmful, conflicting, bloated, or overfit rules.
- `references/regeneration-rubric.md`: when compressing many rules into fewer principles.
- `references/hook-integration.md`: Claude/Codex hook wiring and trigger guidance.
- `references/subagent-prompts.md`: prompts for independent reviewers once the main skill framework exists.

</supporting-info>
