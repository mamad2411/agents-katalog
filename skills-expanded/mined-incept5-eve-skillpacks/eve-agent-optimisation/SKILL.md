---
name: eve-agent-optimisation
description: Analyse agent execution to find wasted tool calls, wrong turns, and blind alleys. Optimise agents to reach their goal in the fewest turns, tokens, and least time. Recommend harness/model changes — never apply without user approval.
---

# Eve Agent Optimisation

The goal: get the agent to its objective in the **fewest tool calls, fewest tokens, shortest time**. Find where it wastes effort and eliminate it.

## Hard Rule: Recommend, Don't Change

**Never change the harness, model, reasoning effort, or permission policy without asking the user first.** These are cost and capability decisions that belong to the project owner. Diagnose, explain the tradeoff, and recommend — then wait for approval.

## What You're Looking For

Analyse agent execution logs to identify:

1. **Wrong turns** — agent tried an approach that couldn't work and had to backtrack.
2. **Blind alleys** — agent spent tokens exploring something irrelevant to the goal.
3. **Unnecessary tool calls** — agent read files it didn't need, ran commands that gave no useful information, or repeated calls with slight variations.
4. **Missing context** — agent had to discover something through trial and error that should have been stated in the SKILL.md or job description.
5. **Wrong tool for the job** — agent used a slow or fragile tool when a faster/native alternative exists (e.g., shelling out to `pdftotext` when the LLM reads PDFs natively).
6. **Excessive reading** — agent read entire large files when it only needed a section, or read many files looking for something that could have been found with a targeted search.
7. **Verbose output** — agent explained its reasoning at length when the task only needed a concise result.
8. **Retry loops** — agent repeated the same failing operation, hoping for a different result.

## Diagnostic Workflow

### Step 1: Get the Execution Record

```bash
eve job diagnose <job-id>          # Full timeline, routing, errors
eve job show <job-id> --verbose    # Phase, attempts, harness, agent
eve job receipt <job-id>           # Token usage + cost
```

Key numbers:
- **Input tokens** — how much the agent read. High = reading too much.
- **Output tokens** — how much it wrote. High = verbose or excessive reasoning.
- **Attempt count** — more than 1 means the agent crashed or timed out.
- **Duration** — compare against what a focused agent should take.

### Step 2: Stream or Replay the Logs

```bash
eve job follow <job-id>            # Real-time (if still active)
eve job logs <job-id>              # Historical
```

Read the log sequentially. For each tool call, ask:
- **Did this advance the goal?** If not, it's waste.
- **Could this have been avoided?** If the SKILL.md had told the agent where to look, would it have skipped this?
- **Was this the right tool?** Could a different approach have gotten the same information faster?
- **Was the scope right?** Did the agent read an entire file when it needed 10 lines?

### Step 3: Map the Critical Path

Identify the **minimum set of tool calls** needed to achieve the goal:

1. What files actually mattered?
2. What commands actually produced useful output?
3. What decisions were correct on first attempt?

Everything else is waste. Quantify: how many tool calls were on the critical path vs total? What percentage of tokens were spent on productive work?

### Step 4: Identify Root Causes

For each category of waste, trace back to the root cause:

| Waste | Root Cause | Fix |
|-------|-----------|-----|
| Agent explored wrong files | SKILL.md doesn't say where to look | Add specific file paths or search patterns to SKILL.md |
| Agent tried wrong approach first | SKILL.md doesn't state the preferred approach | Add explicit instructions: "Do X, not Y" |
| Agent read files it didn't need | Job description too vague | Narrow the description; specify exact scope |
| Agent retried failing command | No error handling guidance | Add failure mode instructions to SKILL.md |
| Agent used wrong tool for file type | SKILL.md doesn't mention native capabilities | Add file-type routing: "PDFs: read natively. Images: view directly." |
| Agent read entire large file | No guidance on targeted reading | Add instructions: "Read only lines 1-50" or "Search for X" |
| Agent verbose in output | No output format specified | Specify exact format: JSON schema, attachment name, concise summary |
| Agent lacks context for decisions | Missing resource refs or env vars | Attach the right resources; ensure `with_apis` is configured |
| Agent re-discovers known facts | No persistent memory strategy | Use org docs, KV store, or attachments to carry forward knowledge |
| Agent slow due to provisioning | Too many resources, large clone, unnecessary toolchains | Trim resource refs, configure shallow clone, remove unused toolchains |

## The Fix Is Almost Always the SKILL.md

The SKILL.md is the highest-leverage optimisation target. A precise SKILL.md eliminates entire categories of wasted tool calls.

### Write for Efficiency

1. **State the goal in one sentence.** The agent should know exactly what it's trying to achieve before doing anything.

2. **Name specific files and paths.** "Check the auth config" wastes tool calls searching. "Read `src/config/auth.ts` lines 1-30" is one tool call.

3. **State the approach explicitly.** "Use native PDF reading via the Read tool — do NOT shell out to conversion tools" prevents the agent from trying the wrong path.

4. **Specify what NOT to do.** If there's a common wrong turn, block it. "Do not read the entire test suite; only read the failing test file."

5. **Define the output format.** "Write a JSON attachment named `findings.json` with schema `{issues: [{file, line, severity, message}]}`." This eliminates formatting deliberation.

6. **Tell the agent what context it has.** "The resource index at `.eve/resources/index.json` lists all attached documents with mime_type. Read it first to determine processing strategy."

7. **Provide decision trees for branches.** Instead of "handle different file types appropriately":
   ```
   Check mime_type in resource index:
   - application/pdf → read natively, use page ranges for >10 pages
   - text/* → read directly
   - image/* → view directly (multimodal)
   - other → describe and note for human review
   ```

8. **Keep it short.** Every word the agent reads consumes input tokens. Cut filler. Use tables and lists over prose.

### Test the SKILL.md

After rewriting, run the same job again and compare:
- Fewer tool calls?
- Fewer tokens?
- Faster completion?
- Correct result on first attempt?

```bash
eve job compare <old-job-id> <new-job-id>   # Compare receipts
```

## Beyond the SKILL.md

When SKILL.md changes aren't sufficient, look at these levers (all require user approval to change):

### Harness and Model

If the agent is consistently:
- **Too slow** for the task → recommend a faster model (e.g., sonnet → haiku).
- **Not capable enough** → recommend a more capable model (e.g., sonnet → opus).
- **Using too many thinking tokens** → recommend lower reasoning effort.
- **Not thinking enough** → recommend higher reasoning effort.

Present the tradeoff (speed vs cost vs quality) and let the user decide.

### Permission Policy

If the agent is blocked waiting for approvals on every file edit:
- Recommend `yolo` for automated batch work.
- Recommend `auto_edit` for supervised coding.
- Explain the security implications.

### Resource Refs

If provisioning is slow:
- Remove resource refs the agent doesn't actually use.
- Mark optional context as `required: false`.
- Thread `mime_type` so the agent doesn't need to probe file types.

### Git Controls

If the agent wastes time on git operations:
- `commit: auto` + `push: on_success` eliminates manual git ceremony.
- `create_branch: if_missing` avoids branch creation failures.
- `ref_policy: auto` minimises clone scope.

### Job Scope

If the agent is doing too much in one job:
- Split into focused children via orchestration.
- Each child gets a narrow scope and specialised SKILL.md.
- Cheaper models for simpler children; capable models only where needed.

### Team Coordination

If child agents duplicate work:
- Ensure skills read `.eve/coordination-inbox.md` at startup.
- Wire `depends_on` for sequential steps.
- Use attachments (not prose) for passing data between jobs.

## Optimisation Report Template

After analysing an agent's execution, present findings in this format:

```
## Agent Optimisation Report: <job-id>

**Goal:** <what the agent was trying to do>
**Result:** <succeeded/failed> in <duration> using <tokens> tokens (<cost>)

### Efficiency Score
- Total tool calls: N
- Productive tool calls: M (X%)
- Wasted tool calls: N-M (Y%)

### Waste Categories
1. <category>: N calls, ~X tokens wasted
   - Example: <specific wasteful action from logs>
   - Fix: <specific SKILL.md or config change>

### Recommended Changes
- [ ] SKILL.md: <specific edit> — eliminates <category> waste
- [ ] SKILL.md: <specific edit> — eliminates <category> waste
- [ ] (Requires approval) Model: <current> → <recommended> — <reason>
- [ ] (Requires approval) Reasoning: <current> → <recommended> — <reason>

### Expected Improvement
- Estimated tool calls: N → M
- Estimated tokens: X → Y
- Estimated time: A → B
```

## Quick Reference: Common Waste Patterns

| Pattern | Signal in Logs | Fix |
|---------|---------------|-----|
| File hunting | Multiple `Read` calls to different files | Name the target file in SKILL.md |
| Grep cascade | Multiple searches with different patterns | Provide the right search term |
| Trial and error | Tool call fails, agent retries with variation | Document the correct approach |
| Over-reading | Read tool on 5000+ line file | Specify line ranges or tell agent to search first |
| Unnecessary exploration | Agent reads README, CHANGELOG, etc. | Explicitly say what NOT to read |
| Format deliberation | Long assistant turns deciding output structure | Specify output format in SKILL.md |
| Redundant validation | Agent re-checks things it already confirmed | Structure the SKILL.md as a linear flow |
| Native capability miss | Shell out to CLI tool when LLM can process directly | State native capabilities explicitly |
| Context re-discovery | Agent re-learns project structure every run | Use org docs or KV store for persistent context |
| Approval blocking | Agent pauses waiting for permission | Recommend `yolo` or `auto_edit` to user |

## Related Skills

- `eve-job-debugging` — CLI commands for monitoring and diagnosing jobs.
- `eve-orchestration` — decomposing work into parallel children.
- `eve-agent-memory` — storage primitives for persistence across jobs.
- `eve-skill-distillation` — encoding learned patterns into reusable skills.
- `eve-read-eve-docs` — platform reference docs (CLI, manifest, jobs, harnesses).
