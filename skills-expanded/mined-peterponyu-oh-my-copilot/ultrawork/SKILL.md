---
name: ultrawork
description: "[OMCP] Parallel execution engine for high-throughput task completion"
orchestrates-agents: "executor, debugger, designer, writer, test-engineer"
argument-hint: "<task description with parallel work items>"
level: 4
---

# [OMCP] Ultrawork

## Agent orchestration

This skill decomposes independent work and routes subtasks to specialist custom
agents such as `executor`, `debugger`, `designer`, `writer`, and
`test-engineer`.

<Purpose>
Ultrawork is a parallel execution engine and execution protocol for independent work. It emphasizes intent grounding, parallel context gathering, dependency-aware task graphs for non-trivial work, and concise evidence-backed execution summaries. It is a component, not a standalone persistence mode -- it provides parallelism and routing guidance, but not persistence, verification loops, or long-lived state management.
</Purpose>

<Use_When>
- Multiple independent tasks can run simultaneously
- User says "ulw", "ultrawork", or wants parallel execution
- You need to delegate work to multiple agents at once
- Task benefits from concurrent execution but the user will manage completion themselves
</Use_When>

<Do_Not_Use_When>
- Task requires guaranteed completion with verification -- use `ralph` instead (ralph includes ultrawork)
- Task requires a full autonomous pipeline -- use `autopilot` instead (autopilot includes ralph which includes ultrawork)
- There is only one sequential task with no parallelism opportunity -- delegate directly to an executor agent
- User needs session persistence for resume -- use `ralph` which adds persistence on top of ultrawork
</Do_Not_Use_When>

<Why_This_Exists>
Sequential task execution wastes time when tasks are independent. Ultrawork enables firing multiple agents simultaneously and routing each to the right model tier, reducing total execution time while controlling token costs. It is designed as a composable component that ralph and autopilot layer on top of.
</Why_This_Exists>

<Execution_Policy>
- Fire all independent agent calls simultaneously -- never serialize independent work
- Always pass the `model` parameter explicitly when delegating
- Read `docs/shared/agent-tiers.md` before first delegation for agent selection guidance
- Use `run_in_background: true` for operations over ~30 seconds (installs, builds, tests)
- Run quick commands (git status, file reads, simple checks) in the foreground
- Resolve intent and uncertainty before implementation; explore first, ask only when still blocked
- For non-trivial tasks, produce a dependency-aware plan with parallel waves before execution
- Keep delegated-task reports concise: short summary, files touched, verification status, blockers
- Manual QA is required for implemented behavior, not just diagnostics
</Execution_Policy>

<Steps>
1. **Read agent reference**: Load `docs/shared/agent-tiers.md` for tier selection
2. **Ground intent first**: Confirm whether the request is implementation, investigation, evaluation, or research; do not code before that is clear
3. **Gather context in parallel**:
   - direct tools for quick reads/searches
   - exploration/docs agents for broad context
4. **Classify tasks by independence**: Identify which tasks can run in parallel vs which have dependencies
5. **Create a task graph for non-trivial work**:
   - Parallel Execution Waves
   - Dependency Matrix
   - acceptance criteria and verification steps per task
6. **Route to correct tiers**:
   - Simple lookups/definitions: LOW tier (Haiku)
   - Standard implementation: MEDIUM tier (Sonnet)
   - Complex analysis/refactoring: HIGH tier (Opus)
7. **Fire independent tasks simultaneously**: Launch all parallel-safe tasks at once
8. **Run dependent tasks sequentially**: Wait for prerequisites before launching dependent work
9. **Background long operations**: Builds, installs, and test suites use `run_in_background: true`
10. **Verify when all tasks complete** (lightweight):
   - Build/typecheck passes
   - Affected tests pass
   - Manual QA completed for implemented behavior
   - No new errors introduced
11. **Anti-slop cleanup** (post-artifact quality step, after executors produce code and before reporting completion):
   - **Invoke the `ai-slop-cleaner` skill via the Skill tool: `Skill("ai-slop-cleaner")`.** Run in standard mode (not `--review`) bounded to the files the executors changed this run.
   - **ai-slop-cleaner is a SKILL, not an agent.** Do NOT call it via `Task(subagent_type="oh-my-copilot:ai-slop-cleaner")` — that subagent type does not exist. If you see "Agent type not found", retry with the Skill tool — do NOT substitute a similarly-named agent as a "closest match".
   - Keep the cleanup scope to the changed-file set; do not broaden it to unrelated files.
   - Re-run the lightweight verification (build/typecheck, affected tests) after the cleanup pass; loop back if a regression appears.
</Steps>

<Tool_Usage>
- Use `[Delegate to the executor agent]
` for simple changes
- Use `[Delegate to the executor agent]
` for standard work
- Use `[Delegate to the executor agent]
` for complex work
- Use `run_in_background: true` for package installs, builds, and test suites
- Use foreground execution for quick status checks and file operations
- Use `Skill("ai-slop-cleaner")` for the post-artifact anti-slop cleanup pass. `ai-slop-cleaner` is a skill, not an agent — invoke it via the Skill tool, never via `Task(subagent_type=...)`.
</Tool_Usage>

<Examples>
<Good>
Three independent tasks fired simultaneously:
```
[Delegate to the executor agent]

[Delegate to the executor agent]

[Delegate to the executor agent]

```
Why good: Independent tasks at appropriate tiers, all fired at once.
</Good>

<Good>
Correct use of background execution:
```
[Delegate to the executor agent]

[Delegate to the executor agent]

```
Why good: Long build runs in background while short task runs in foreground.
</Good>

<Bad>
Sequential execution of independent work:
```
result1 = Task(executor, "Add type export")  # wait...
result2 = Task(executor, "Implement endpoint")     # wait...
result3 = Task(executor, "Add tests")              # wait...
```
Why bad: These tasks are independent. Running them sequentially wastes time.
</Bad>

<Bad>
Wrong tier selection:
```
[Delegate to the executor agent]

```
Why bad: Opus is expensive overkill for a trivial fix. Use executor with Haiku instead.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- When ultrawork is invoked directly (not via ralph), apply lightweight verification only -- build passes, tests pass, no new errors
- For full persistence and comprehensive architect verification, recommend switching to `ralph` mode
- If a task fails repeatedly across retries, report the issue rather than retrying indefinitely
- Escalate to the user when tasks have unclear dependencies or conflicting requirements
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All parallel tasks completed
- [ ] Build/typecheck passes
- [ ] Affected tests pass
- [ ] No new errors introduced
- [ ] ai-slop-cleaner pass completed on the changed-file set (post-artifact quality step)
</Final_Checklist>

<Advanced>
## Relationship to Other Modes

```
ralph (persistence wrapper)
 \-- includes: ultrawork (this skill)
     \-- provides: parallel execution only

autopilot (autonomous execution)
 \-- includes: ralph
     \-- includes: ultrawork (this skill)
```

Ultrawork is the parallelism layer. Ralph adds persistence and verification. Autopilot adds the full lifecycle pipeline.
</Advanced>
