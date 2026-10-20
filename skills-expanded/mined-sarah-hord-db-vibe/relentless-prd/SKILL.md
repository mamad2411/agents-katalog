---
name: relentless-prd
description: Generate a structured PRD through interactive discovery. Outputs a markdown file with testable acceptance criteria and an agent handoff block, ready for `relentless` auto-continuing implementation.
user-invocable: true
---

# PRD Generator

Generate a structured Product Requirements Document through interactive discovery. The output is a markdown file with testable acceptance criteria and a machine-readable handoff block, designed to feed directly into `relentless` for auto-continuing implementation.

**Announce at start:** "I'll help you write a PRD. Let me ask a few questions to understand what you need."

## Process

### Phase 1: Discovery (interactive)

Ask the user what they want to build. Then ask **up to 5** targeted clarifying questions — adapt based on what's already clear. Don't ask questions the codebase can answer. Common areas to probe:

- **Scope**: What's in and out? Is this a new feature, enhancement, or fix?
- **Users**: Who is this for? What's their workflow today?
- **Constraints**: Tech stack, compatibility, performance, security requirements?
- **Success criteria**: How do we know it's done? What does "working" look like?
- **Dependencies**: Does this need external APIs, data sources, or other features?

Ask questions one batch at a time (2-3 per message), not all at once. Stop as soon as you have enough to write a clear PRD — don't over-interview.

### Phase 2: Write discovery brief

Capture everything from Phase 1 into a structured brief file at `./_prd_brief_<slug>.md`:

```markdown
# PRD Brief: <Feature Name>

## Discovery Summary
<What the user wants to build, in 2-3 sentences>

## Scope
- In: <what's included>
- Out: <what's excluded>

## Users & Workflow
<Who uses this, what their current workflow is>

## Success Criteria (from user)
<How do we know it's done — user's words, not yet formalized>

## Constraints
<Tech stack, compatibility, performance, security — anything the user mentioned>

## Dependencies
<External APIs, data sources, other features>

## Slug
<slug>
```

Tell the user: "Discovery captured. Now I'll research the codebase and write the PRD — this runs through the relentless engine so it won't eat your context."

### Phase 3: Codebase research + PRD writing (relentless-protected)

Dispatch codebase research and PRD writing through the relentless engine. This phase is token-heavy (Glob/Grep exploration, reading multiple files, generating the full PRD with Agent Handoff JSON).

**Skill-aware routing during Phase A:** when external domain context is needed, explicitly invoke relevant installed skills before finalizing requirements. Keep this selective (only when it removes real ambiguity), for example:

- Databricks product capability/support ambiguity: `product-question-research`, `databricks-docs`
- Databricks workspace file layout/deployed code context: `databricks-workspace-files`
- Salesforce/Jira/Slack integration requirements: `salesforce-actions`, `jira-actions`, `slack-messaging`
- New plugin/skill overlap risk: `dupe-check`

If a skill was used to shape requirements, capture the decision in the PRD `Background`/`Design` sections and include the resulting constraints in Agent Handoff.

```bash
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -n 3 -t 20 -p bypassPermissions -v \
  "You are writing a PRD. Read the discovery brief at _prd_brief_<slug>.md for context.

PHASE A — Codebase Research:
0. If domain capability/support is ambiguous, invoke the most relevant installed skill(s) first and capture what they confirmed
1. Find relevant files using Glob and Grep for the feature area described in the brief
2. Read key files to understand current patterns, conventions, and architecture
3. Identify integration points — where will new code connect to existing code?
4. Note conventions — file naming, test patterns, import style, error handling
5. Record any skill-derived constraints/assumptions so implementation can follow them

PHASE B — Write the PRD:
Write prd_<slug>.md using the template below. Adapt sections to scope — remove empty sections.

TEMPLATE:
# PRD: <Feature Name>

**Version**: 1.0 | **Status**: Draft | **Date**: <today>

## Summary
One paragraph: what this does, why it matters, and the primary success metric.

## Background
What exists today. What problem this solves. Any prior art or failed attempts.

## Research Inputs (only if used)
- Skills invoked and why (1 line each)
- External constraints confirmed (support matrix, auth limits, API behavior)

## Goals
- [Goal 1 — measurable]
- [Goal 2 — measurable]

## Non-Goals (explicit scope boundaries)
- [What this does NOT cover — be specific]
- [These prevent scope creep during autonomous implementation]

## Requirements

### Functional
- FR-1: <requirement>
- FR-2: <requirement>

### Non-functional (if applicable)
- NFR-1: <performance/security/scale requirement with numbers, not adjectives>

## Design

### Architecture
How this fits into the existing codebase. Key files, modules, patterns to follow.
Reference actual file paths discovered during codebase research.

### Interface changes
Public APIs, function signatures, config changes, CLI flags — whatever applies.

### Data model (if applicable)
Schema changes, new types, state management.

## Acceptance Criteria

Use Given/When/Then format. Every criterion must be specific and verifiable.
Include machine-verifiable fields for each AC: id, description, verifiable (true/false), test_type (pytest/vitest/manual), gate_file, gate_test.

- AC-1: Given [context], when [action], then [expected outcome]
- AC-2: Given [context], when [action], then [expected outcome]

Bad: 'Works well.' 'Is fast.' 'Handles errors.'
Good: 'Returns 401 with body {error: \"token_expired\"} when JWT exp < now.'
Good: 'Completes indexing of 10k documents in under 30 seconds.'

## Risks
- [Risk 1]: [mitigation]
- [Risk 2]: [mitigation]

## Open Questions
- [ ] [Unresolved decision that might affect implementation]

---

## Agent Handoff

> Machine-readable block for relentless and other autonomous agents.

\`\`\`json
{
  \"prd_version\": \"1.0\",
  \"goal\": \"<single sentence — the agent's termination condition>\",
  \"success_criteria\": [\"<AC-1 short form>\", \"<AC-2 short form>\"],
  \"must_have\": [\"<FR-1>\", \"<FR-2>\"],
  \"out_of_scope\": [\"<non-goal 1>\", \"<non-goal 2>\"],
  \"constraints\": {
    \"tech_stack\": \"<languages/frameworks from codebase>\",
    \"key_files\": [\"<file paths discovered during research>\"],
    \"patterns\": \"<conventions to follow>\"
  },
  \"preferred_skills\": [
    \"<skill-name used during PRD research, only if required for implementation>\"
  ],
  \"escalate_on\": [
    \"ambiguous requirement that could be interpreted multiple ways\",
    \"missing dependency or API credentials\",
    \"conflicting acceptance criteria\",
    \"architectural decision not covered in this PRD\"
  ],
  \"loop_guards\": {
    \"max_iterations\": 7,
    \"state_hash_check\": true,
    \"heartbeat_interval_seconds\": 30,
    \"on_stuck\": \"pause_and_surface\",
    \"state_persistence\": \"local_disk\"
  }
}
\`\`\`

IMPORTANT: The PRD must reference actual file paths and patterns found during codebase research, not placeholders." \
  > /absolute/path/to/project/relentless_prd_<slug>.log 2>&1
```

Run in background. When complete, read `prd_<slug>.md` to verify it was written.

### Phase 4: Quality check

Before presenting, verify:
- [ ] Every acceptance criterion is testable (Given/When/Then or concrete assertion)
- [ ] Non-goals are explicit — the agent knows what NOT to build
- [ ] No ambiguous language ("fast", "easy", "simple" — replace with numbers)
- [ ] Technical design references actual codebase files and patterns
- [ ] Agent Handoff JSON is valid and `escalate_on` covers likely failure modes
- [ ] Scope matches effort — don't over-document small changes

### Phase 5: Review and refine

Present the PRD to the user for review. Incorporate feedback. Iterate until they approve.

### Phase 6: Implementation handoff

Once approved, present the options:

```
PRD saved to ./prd_<slug>.md

Ready to implement. Options:
  1. "implement it"        → I'll run relentless in the background right now
  2. "implement it quietly" → Same but no verbose output
  3. Run manually from terminal:
     relentless -f ./prd_<slug>.md -n 8 -m opus -b 3.0 -v
```

**When the user says "implement it" (or similar):**

Run relentless in the background via the Bash tool with `run_in_background: true`.

**Important:** The `env -u` prefix strips environment variables that prevent nested Claude sessions from launching.

```bash
env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -f ./prd_<slug>.md -p bypassPermissions -v > ./relentless_<slug>.log 2>&1
```

Tell the user: "Implementation running in background. I'll notify you when it completes. Progress is tracked in `_relentless_state.md` and full output in `relentless_<slug>.log`."

If the user says "implement it quietly" or wants less output, drop the `-v` flag.

**When relentless completes**, read the state file and summarize:
- Which acceptance criteria passed
- Any escalations or blockers hit
- Files created/modified
- Whether it succeeded or needs manual follow-up

## Guidelines

- **Be opinionated** — If the user is vague, propose a concrete design and let them push back. Don't ask "what do you prefer?" when you can recommend.
- **Acceptance criteria are king** — These drive implementation. Every AC should map to a verifiable check. The agent will use these as its completion signal.
- **Non-goals prevent scope creep** — An autonomous agent will try to "improve" things. Explicit non-goals keep it focused.
- **escalate_on is a safety valve** — List situations where the agent should stop and ask rather than guess. This prevents hallucinated solutions to ambiguous requirements.
- **Match the codebase** — Reference actual file paths, patterns, and conventions. The implementing agent needs to know WHERE to put code, not just WHAT to build.
- **No implementation code** — The PRD describes *what*, not *how*. Save code for the implementation phase.
