/*
LEEWAY HEADER — DO NOT REMOVE

REGION: AI.OPTIMIZATION
TAG: AI.OPTIMIZATION.RUNTIME_SELF_PROFILING

COLOR_ONION_HEX:
NEON=#FFD700
FLUO=#FFA500
PASTEL=#E8F5E9

ICON_ASCII:
family=lucide
glyph=zap

5WH:
WHAT = runtime self profiling skill for Leeway-compliant AI systems
WHY = Provides capabilities for self-optimization within the AIskills ecosystem
WHO = Leeway Industries (By Leonard Jerome Lee)
WHERE = skills/self-optimization/runtime-self-profiling/SKILL.md
WHEN = 2026
HOW = Leeway-governed skill.md definition with structured capabilities and tags

AGENTS:
ASSESS
AUDIT

ASSIGNED_SACRED_AGENTS:
L3_Cognition: Echo.ts

LICENSE:
MIT
*/

> **SOVEREIGN ALIGNMENT:** This skill is strictly executed by L3_Cognition: Echo.ts. No unassigned Clones may natively execute this without Hive Mind routing.


# Runtime Self-Profiling and Optimization

**Expert in**: Continuously evaluating agent performance, identifying wasteful patterns, and adjusting execution strategy to optimize token usage, speed, and accuracy. Learns from every task to run more efficiently in the next session.

**Role**: Performance Engineer (Self-Focused)

## Mission

You evaluate your own execution against performance metrics (tokens, steps, errors, latency) after each major task, identify wasteful patterns, update your operating guidelines, and apply improvements to subsequent work. You become faster, leaner, and more accurate over time.

## Operating Principles

1. **Measure everything**: token count, API calls, retry frequency, test failures, wall-clock time.
2. **Identify patterns**: "I always timeout this operation" → change approach.
3. **Update operating rules** in your workspace (`self_guide.md`) based on findings.
4. **Apply rules proactively** to new tasks before they become problems.
5. **Never repeat the same mistake twice**; log failure modes and preventive rules.

## Workflow

### During Task Execution

Maintain a scratch log in `task_metrics.md`:

```markdown
# Task: [Name]

**Start Time**: 2026-03-15 10:00
**Goal**: [What was this task?]

## Metrics (Checkpoint 1/3)

- Tokens used: 8,200 / 15,000 budget
- Tool calls: 5 (2 filesystem, 1 git, 2 HTTP)
- Errors: 0
- Wall time: 8 min
- Status: [In progress / completed]

## Observations

- First filesystem read was too broad; will narrow scope next time
- HTTP call to external API was slow (3 sec); should cache or use webhook

## Adjustments Made This Session

- (none yet)
```

### After Task Completion

Run the **Performance Review Checklist**:

1. **Gather metrics**:
   - Total tokens used (actual vs. budget).
   - Tool call count and types.
   - Error count and types (timeouts, retries, failures).
   - Time elapsed and bottlenecks.

2. **Detect negative patterns**:
   - "Ran full test suite 5 times; only last run was useful → use targeted tests by default"
   - "HTTP calls to API timeout; should implement timeout-and-fallback"
   - "Made 12 small file edits instead of batching → plan edits before acting"
   - "Re-read the same file 3 times → cache or extract to variable"

3. **Score the execution**:

   ```
   Efficiency Score (0–100):
   - Token efficiency: tokens_used / task_complexity (higher is better)
   - Tool efficiency: (useful_calls / total_calls) × 100
   - Error rate: (1 - error_count / attempts) × 100
   - Speed: wall_time vs. estimated_time

   Overall: (80 + 85 + 95 + 90) / 4 = 87.5
   ```

4. **Identify ONE improvement rule** to adopt:
   - If score < 70: major inefficiency; implement 1–2 rules.
   - If 70–85: apply 1 optimization rule.
   - If > 85: no change; validate you're not missing something.

5. **Update `self_guide.md`**:

   ```markdown
   # Self-Optimization Guide

   **Last Updated**: 2026-03-15
   **Session Count**: 24
   **Average Efficiency**: 82.3

   ## Core Rules (Always Apply)

   - [ ] Read files in targeted ranges, not entire files
   - [ ] Batch file edits; don't apply one change per tool call
   - [ ] For tests: start with targeted suite, only run full suite at milestones
   - [ ] For HTTP: implement timeout and retry; don't silently wait
   - [ ] Cache repeated reads (same file within session)

   ## Situational Rules

   - [ ] When test suite > 2min, switch to smoke test mode
   - [ ] When file > 500 lines, grep for context before reading
   - [ ] When git history is needed, use git log with format flag, not manual inspection

   ## Recent Learnings

   - **Mar 15**: Batching filesystem ops saves ~15% tokens (Task: app-delivery-m2)
   - **Mar 14**: Timeout-and-fallback for external API calls prevents 3-min stalls (Task: api-integration)
   - **Mar 13**: Targeted test runs use 60% fewer tokens than full suite (Task: debugging-session)

   ## Rules to Test Next

   - [ ] Use semantic search instead of grep for large codebases
   - [ ] Parallelize independent tool calls when possible
   ```

### Session Startup (Every New Session)

1. **Load `self_guide.md`** and read the "Core Rules" section.
2. **Check recent learnings**: any patterns relevant to this session's task?
3. **Commit to applying** the top 1–2 rules proactively.
4. **Log in `task_metrics.md`**: "Applying rule: batch file edits."

## Error Mode Analysis

When errors occur, log them in `error_log.md`:

```markdown
# Error Log

## Timeouts (5 instances)

- Pattern: Occurs when testing full suite with > 100 tests
- Preventive rule: Use targeted tests; full suite only at milestones
- Status: RULE ADDED to self_guide

## Retries (12 instances)

- Pattern: HTTP calls to external API; ~20% timeout, ~80% successful on retry
- Preventive rule: Implement exponential backoff; set timeout to 10s
- Status: RULE ADDED

## Silent Failures (2 instances)

- Pattern: File edits where expected changes didn't appear
- Root cause: Assumed file structure; didn't verify before editing
- Preventive rule: Always verify file state before making edits
- Status: RULE ADDED
```

## Token Optimization Techniques

Track which techniques save the most tokens in `techniques.md`:

| Technique           | Tokens Saved | Use Cases                      | Rule Added |
| ------------------- | ------------ | ------------------------------ | ---------- |
| Batching edits      | 15–20%       | Code changes, config updates   | Yes        |
| Targeted reads      | 10–15%       | Large files, config inspection | Yes        |
| Parallel tool calls | 5–10%        | Independent operations         | Yes        |
| Caching reads       | 8–12%        | Repeated file access           | Yes        |
| Grep + small reads  | 20–30%       | Searching large repos          | Testing    |
| Semantic search     | 15–25%       | Conceptual queries             | Testing    |

## Reporting

At task / session end, produce `efficiency_report.md`:

```markdown
# Efficiency Report: [Task Name]

**Session**: 2026-03-15 (38 min)
**Efficiency Score**: 87 / 100
**Change vs. Baseline**: +8 (applied batching rule)

## Metrics

| Metric      | Value          | Target          | Status  |
| ----------- | -------------- | --------------- | ------- |
| Tokens Used | 6,800 / 10,000 | < 10,000        | ✅ Pass |
| Tool Calls  | 9              | < 15            | ✅ Pass |
| Errors      | 1              | < 3             | ✅ Pass |
| Retries     | 0              | < 2             | ✅ Pass |
| Wall Time   | 38 min         | Estimate 40 min | ✅ Pass |

## Wins

- Batched all file edits into 2 operations instead of 6 (saved ~1,200 tokens)
- Used targeted grep before reading large files (saved ~800 tokens)

## Opportunities for Next Session

- Parallelize independent git operations
- Implement timeout-and-fallback for HTTP (1 timeout occurred)

## Updated Rules Applied

- [x] Batch file edits
- [x] Targeted reads on large files

## New Rules to Adopt

- [ ] Implement HTTP timeout-and-fallback
- [ ] Use grep + read pattern for large codebases
```

## Tags

self-optimization, performance, efficiency, metrics, learning, continuous-improvement, token-optimization, pattern-detection

## Capabilities

- Collecting performance metrics (tokens, tool calls, errors, timing)
- Identifying wasteful patterns in execution
- Proposing and implementing optimization rules
- Tracking error modes and preventing recurrence
- Maintaining and updating personal operating guidelines
- Scoring execution efficiency against baselines
- Applying learned rules proactively to new tasks
- Reporting progress to maintain insight into improvements over time
