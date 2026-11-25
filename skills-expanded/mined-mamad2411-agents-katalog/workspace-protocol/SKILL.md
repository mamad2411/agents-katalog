# Workspace Protocol — Shared File-Based Agent Communication

## When This Activates

Any multi-agent workflow (feature-pipeline, fullstack-orchestrator, or any orchestrator spawning 2+ sub-agents).

## Core Rule

> Agents communicate through files, not through prompts. The filesystem IS the shared state.

## Directory Structure

```
.kiro/workspace/{feature-name}/
├── STATUS.md              # Pipeline state — the coordination bus
├── 01-brs.md              # product-manager output
├── 02-review.md           # devils-advocate output
├── 03-arch-plan.md        # architecture-reviewer output (selected plan)
├── 04-tests/              # test-forge output
│   ├── ServiceTests.cs
│   └── ControllerTests.cs
├── 05-implementation/     # forge output (generated code paths)
├── 06-code-review.md      # reviewer findings
└── 07-summary.md          # final handoff report
```

## STATUS.md Format

```markdown
# Feature: {name}
Created: {date}
Current Stage: {N}

| # | Stage | Agent | Status | Output |
|---|-------|-------|--------|--------|
| 1 | BRS | product-manager | ✅ | 01-brs.md |
| 2 | Review | devils-advocate | ✅ | 02-review.md |
| 3 | Architecture | architecture-reviewer | ✅ Plan B | 03-arch-plan.md |
| 4 | Tests | test-forge | 🔄 | 04-tests/ |
| 5 | Implementation | forge | ⏳ | — |
| 6 | Code Review | reviewers | ⏳ | — |
| 7 | Summary | orchestrator | ⏳ | — |

## Human Decisions
- {date}: Selected Plan B (architecture)
- {date}: Approved BRS (no changes)

## Blocked
- None
```

## How Orchestrators Use This

### Creating a workspace (start of pipeline)

```bash
FEATURE="sip-cancellation"
WS=".kiro/workspace/$FEATURE"
mkdir -p "$WS/04-tests" "$WS/05-implementation"
```

Then write initial STATUS.md.

### Delegating to a sub-agent (tiny prompt)

```
subagent prompt (ENTIRE prompt — nothing more):

"You are {agent_role}. Feature: {feature_name}.
Workspace: .kiro/workspace/{feature_name}/
Read: {input_files}
Write your output to: {output_file_or_dir}
Update STATUS.md: set stage {N} to ✅
Respond with ONLY: Done: {stage_name}"
```

### Collecting results (read files, not transcripts)

```bash
# Check if stage is done
grep "| 4 |" .kiro/workspace/sip-cancellation/STATUS.md
# Read the output
cat .kiro/workspace/sip-cancellation/04-tests/*.cs
```

**NEVER use the subagent's response text as data.** It should only be "Done: {stage}".

## Rules for Sub-Agents

When you receive a workspace path:

1. **Read STATUS.md** — understand where the pipeline is
2. **Read only YOUR input files** — don't read everything
3. **Write your output to the specified location**
4. **Update STATUS.md** — mark your stage ✅ with output path
5. **Respond with ONLY "Done: {stage}"** — nothing else

### What NOT to do

- ❌ Don't summarize your work in the response (write to file instead)
- ❌ Don't read other agents' outputs unless they're your explicit input
- ❌ Don't modify other agents' output files
- ❌ Don't pass large content back in your response

## Crash Recovery

If pipeline is interrupted:

```
User: "Continue sip-cancellation"
Agent: reads .kiro/workspace/sip-cancellation/STATUS.md
       → sees Stage 4 was 🔄 (in progress)
       → checks if 04-tests/ has files
       → if yes: mark ✅, proceed to Stage 5
       → if no: re-run Stage 4
```

No state lost. No re-running completed stages.

## Parallel Agents

For fan-out (e.g., multiple reviewers in parallel):

```
.kiro/workspace/{feature}/06-reviews/
├── dotnet-review.md       # Written by dotnet-reviewer
├── react-review.md        # Written by react-reviewer
├── security-review.md     # Written by security-reviewer
└── performance-review.md  # Written by performance-reviewer
```

Orchestrator polls: `ls .kiro/workspace/{feature}/06-reviews/*.md | wc -l`
When count matches expected → all reviews done → proceed.

## Token Budget Impact

| Approach | Tokens per sub-agent call |
|----------|--------------------------|
| Full content in prompt | 5,000–10,000 |
| File protocol (just path + instructions) | 100–200 |
| **Savings** | **95–98%** |
