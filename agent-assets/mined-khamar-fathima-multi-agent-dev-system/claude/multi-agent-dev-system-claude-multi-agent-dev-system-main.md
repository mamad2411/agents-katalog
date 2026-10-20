# Project Standards — All Agents Must Follow

These standards apply to every agent in the pipeline. They are not suggestions.

If this project involves trading, financial markets, or order execution, agents must additionally apply `tasks/trading_rules.md` as binding rules.

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for any non-trivial task (three or more steps, or involving architectural decisions).
- If something goes wrong, stop and re-plan immediately rather than continuing blindly.
- Use plan mode for verification steps, not just implementation.
- Write detailed specifications upfront to reduce ambiguity.

### 2. Subagent Strategy
- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, allocate more compute via subagents.
- Assign one task per subagent to ensure focused execution.

### 3. Temporary Agent Weakness Response
- Agents may create temporary agents only. Do not create or modify persistent agent definitions unless the user explicitly requests it.
- When an agent detects a weakness it cannot confidently resolve inside its own stage, it must write a structured gap report instead of silently continuing.
- Gap reports go under the active artifact directory:
  - Greenfield runs: `tasks/gap_reports/`
  - Refactor or audit runs: `.pipeline/gap_reports/`
- Gap reports must include:
  - Observed weakness
  - Evidence
  - Risk if ignored
  - Affected area
  - Confidence
  - Recommended response
  - Needed context
  - Exit condition
- The system routes each gap to the smallest reliable intervention:
  - Better prompt instructions for underspecified behavior.
  - A checklist for procedural risk.
  - A deterministic test for mechanically verifiable behavior.
  - A tool or search step for missing capability or missing current facts.
  - A reviewer step for high-risk or subjective changes.
  - A one-off temporary specialist when domain judgment is needed.
- Temporary specialists must be narrowly scoped, receive only relevant context, write their output under `tasks/temporary_agents/` or `.pipeline/temporary_agents/`, and stop after their exit condition.
- The parent pipeline remains responsible for the temporary agent's output. Temporary agents do not spawn persistent agents.
- If the same weakness appears repeatedly, log it as a future improvement candidate in the run summary or lessons, but do not promote it automatically.

### 4. Self-Improvement Loop
- After any correction from the user, update `tasks/lessons.md` with the relevant pattern.
- Create rules for yourself that prevent repeating the same mistake.
- Iterate on these lessons rigorously until the mistake rate declines.
- Review lessons at the start of each session when relevant to the project.

### 5. Verification Before Done
- Never mark a task complete without proving it works.
- Diff behavior between main and your changes when relevant.
- Ask: "Would a staff engineer approve this?"
- Run tests, check logs, and demonstrate correctness.

### 6. Demand Thoughtful Simplicity
- For non-trivial changes, pause and ask whether there is a more elegant solution.
- If a fix feels hacky, implement the solution you would choose knowing everything you now know.
- Do not over-engineer simple or obvious fixes.
- Critically evaluate your own work before presenting it.

### 7. Autonomous Bug Fixing
- When given a bug report, fix it without asking for unnecessary guidance.
- Review logs, errors, and failing tests, then resolve them.
- Avoid requiring context switching from the user.
- Fix failing CI tests proactively.

## Task Management

1. **Plan First**: Write the plan to `tasks/todo.md` with checkable items.
2. **Verify Plan**: Review before starting implementation.
3. **Track Progress**: Mark items complete as you go.
4. **Explain Changes**: Provide a high-level summary at each step.
5. **Document Results**: Add a review section to `tasks/todo.md`.
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections.
7. **Multi-Agent Handoffs**: When passing work between agents, always include a short context summary so the next agent doesn't lose critical state.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Minimize code impact.
- **No Laziness**: Identify root causes. Avoid temporary fixes. Apply senior developer standards.
- **Minimal Impact**: Touch only what is necessary. Avoid introducing new bugs.

## Production Readiness Checklist (Final QA Gate)

Before any task or feature is marked **Done**, the following must be verified:

- [ ] Security & credential audit passed (no secrets in code, proper auth, input sanitization)
- [ ] Performance / latency acceptable under expected load
- [ ] Logging + monitoring hooks in place (structured logs, key metrics, alerting hooks)
- [ ] Documentation updated (README, relevant doc, or inline comments for complex sections)
- [ ] "Staff Engineer" bar passed — would you be comfortable shipping this code?

(For trading/finance projects, see additional checks in `tasks/trading_rules.md`.)
