---
name: pwrl-plan-research
description: "Perform local and external research to inform technical design decisions during planning."

argument-hint: "[scoped context from pwrl-plan-scope]"
---

# pwrl-plan-research — Research & Findings

**Purpose:** Second step in the planning workflow. Accepts scoped context from `pwrl-plan-scope`, performs local codebase research, detects high-risk areas, and determines if external research is needed. Returns research findings that inform the design phase (`pwrl-plan-design`).

## Interaction Method

- Use the platform's `ask_user_question` extension for decisions (e.g., approve external research).
- Ask one question at a time. Present findings before asking for confirmation.
- Use multiple-choice questions when possible (e.g., "Should I run external research on [topic]?").
- If input is empty or missing scoped context, ask: "Please provide a task description or run pwrl-plan-scope first to gather context."

## Input

This skill expects the scoped context object from `pwrl-plan-scope` (S2). It contains:

```yaml
scope-id: YYYY-MM-DD-NNN-scope
domain: software
problem: "..."
intended_behavior: "..."
success_criteria: ["..."]
related_learnings: ["docs/learnings/XXX.md"]
learning_gaps: ["gap_name"]
```

If the context is not provided, try to bootstrap by searching for recent scope files in `docs/plans/.scope/` or prompt the user to run `pwrl-plan-scope` first.

## Output: Research Findings

After completing the workflow, produce a research findings block (in memory or as markdown):

```yaml
research-id: YYYY-MM-DD-NNN-research
status: complete

# Research Findings

## Patterns Found
- `path/to/pattern/file` — [pattern description]

## High-Risk Detection
- Detected areas: [list]
- Risk Level: HIGH | MEDIUM | LOW
- External Research Recommended: YES | NO

## Tech Stack
- [Framework]: [version]
- [Language]: [version]
- [Database]: [version]
- [Key libraries]: [versions]

## External Research
- Needed: YES | NO
- Guidance: [librarian query or web search suggestion]
- Status: completed | skipped | declined

## Technical Constraints
- [Constraint 1]
- [Constraint 2]

## Findings Summary
[2-3 sentence overview of all findings]
```

This findings object is passed to `pwrl-plan-design` (S4) for the design phase.

## Workflow

### Step 1: Local Pattern Discovery

1. Read the scoped context to understand the task.
2. Search the codebase for patterns relevant to the task using `grep` and `find`:
   - Search for similar implementations (e.g., if task is "add auth", search for auth patterns)
   - Search in common directories: `src/`, `app/`, `lib/`, `services/`, `api/`
   - Search config files for tech stack versions: `package.json`, `composer.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, etc.
3. For each pattern found:
   - Record the file path
   - Count how many similar examples exist
   - Describe the pattern briefly
   - Rate confidence: HIGH (3+ examples), MEDIUM (1-2 examples), LOW (0 examples)
4. If no relevant config files found, inspect codebase structure for clues: languages, frameworks, directory structure.

### Step 2: High-Risk Area Detection

Scan the task description and scoped context for high-risk keywords across six areas: Security, Payments, APIs, Migrations, Complex Logic, and Infrastructure. For details on the risk keyword table, area definitions, and heuristics for assigning risk levels, see **[high-risk-detection.md](references/high-risk-detection.md)**.

### Step 3: External Research Decision

1. Apply the decision rule:
   ```
   should_run_external_research = high_risk_detected AND patterns_found_count < 3
   ```
2. If `should_run_external_research` is true:
   - Recommend external research.
   - Generate a specific query for the librarian skill or web search.
   - Ask the user: "This task involves high-risk area(s) ([areas]) with only [count] local example(s). Should I run external research?"
   - Options: yes, no, skip
3. If user accepts: Provide specific librarian guidance with query.
4. If user declines or if research is not needed: Proceed with local findings only.

### Step 4: External Research Guidance (if needed)

Generate targeted librarian or web search queries when external research is recommended. For query templates, formatting guidance, and examples for each high-risk area, see **[external-research-guidance.md](references/external-research-guidance.md)**.

### Step 5: Technical Constraints Gathering

1. Document all technical constraints found:
   - Framework and language versions from config files
   - Performance requirements or implications
   - Compatibility notes (e.g., "must support IE11", "must work with existing auth")
   - Deployment constraints (e.g., "must run on AWS Lambda")
   - Integration constraints (e.g., "must use existing logging framework")
2. If constraints are not obvious from codebase, ask the user:
   - "Are there any technical constraints or requirements I should be aware of?"
   - Collect any additional constraints the user mentions.

### Step 6: Present and Confirm

1. Present the full research findings to the user via `ask_user_question`.
2. Ask: "Are these findings sufficient to proceed to design?"
3. If confirmed: Return the research findings object.
4. If corrections needed: Iterate on steps 1-5 as needed based on feedback.
5. **Do not proceed to design/generation** — this skill only performs research.

## Edge Cases

Seven edge cases encountered during research: no local patterns found, conflicting local patterns, missing tech stack info, user declining external research on high-risk tasks, multiple high-risk areas, unavailable librarian/search, and overwhelming pattern count. For decision trees, handling strategies, and examples, see **[edge-cases.md](references/edge-cases.md)**.

## State Passing (to S4: pwrl-plan-design)

Research findings are passed to `pwrl-plan-design` in markdown format with YAML frontmatter. Downstream skills read it from memory or from `docs/plans/.research/YYYY-MM-DD-NNN-research.md`. For detailed schema documentation, field reference, storage conventions, and versioning rules, see **[state-schema.md](references/state-schema.md)**.

## References

- **Source:** Phase 2 of `pwrl-plan/SKILL.md`
- **Input:** Scoped context from `pwrl-plan-scope` (S2)
- **Downstream:** `pwrl-plan-design` (S4) — receives research findings
- **Skills:** May invoke librarian skill for external research
- **Config:** `package.json`, `composer.json`, etc. for tech stack detection
