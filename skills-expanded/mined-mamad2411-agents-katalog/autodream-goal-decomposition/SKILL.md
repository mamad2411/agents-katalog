---
name: "autodream-goal-decomposition"
description: "Claude Code AutoDream: autonomous goal decomposition from high-level objectives, automatic plan generation, self-directed task execution, iterative refinement, and objective-to-action translation"
---

# AutoDream — Autonomous Goal Decomposition

## When to activate
- User provides a high-level objective ("Make the API 10x faster", "Get the project to 1000 stars") without specific steps
- Breaking down ambiguous goals into concrete, executable tasks
- When the user says "figure it out" or "do whatever it takes to achieve X"
- Multi-day or multi-week projects that need automatic decomposition into daily work units
- Autonomous agents that need to self-direct without constant human task assignment
- Strategic planning where the end-state is clear but the path is not

## When NOT to use
- Tasks with explicit, step-by-step instructions already provided
- Simple, well-defined requests ("Add a login button to the header")
- When the user wants to make all architectural decisions themselves
- Tasks requiring human judgment at every decision point (hiring, legal, financial)
- One-off bug fixes or small feature requests

## Instructions

### 1. Goal Decomposition Framework

AutoDream translates objectives into actionable plans:

```
Objective: "Reduce API response time by 90%"
    │
    ├── Goal 1: Profile current performance
    │   ├── Task 1.1: Add request timing middleware
    │   ├── Task 1.2: Identify top 10 slowest endpoints
    │   └── Task 1.3: Baseline: record current p50/p95/p99
    │
    ├── Goal 2: Optimize database layer
    │   ├── Task 2.1: Add query profiling to ORM
    │   ├── Task 2.2: Identify N+1 queries and add eager loading
    │   ├── Task 2.3: Add indexes for top 5 slow queries
    │   └── Task 2.4: Implement query result caching (Redis)
    │
    ├── Goal 3: Optimize application layer
    │   ├── Task 3.1: Add response compression (gzip/brotli)
    │   ├── Task 3.2: Implement response caching headers
    │   └── Task 3.3: Move heavy computations to background jobs
    │
    └── Goal 4: Validate and measure
        ├── Task 4.1: Run load test (k6/Artillery)
        ├── Task 4.2: Compare p50/p95/p99 against baseline
        └── Task 4.3: If < 90% improvement, identify remaining bottlenecks
```

### 2. Decomposition Algorithm

```yaml
autodream_process:
  step_1_understand:
    - Parse objective into measurable criteria
    - Identify constraints (time, budget, technical debt)
    - Determine success metrics (what does "done" look like?)
    
  step_2_explore:
    - Assess current state (what exists today?)
    - Identify gaps (where are we vs. where we need to be?)
    - Research approaches (what solutions exist for this class of problem?)
    
  step_3_decompose:
    - Break objective into 3-5 sub-goals (independent workstreams)
    - For each sub-goal, identify 3-7 concrete tasks
    - Order tasks by dependency (what must come first?)
    - Estimate effort per task (trivial / small / medium / large)
    
  step_4_prioritize:
    - Rank by impact: which tasks move the needle most?
    - Rank by effort: which are quickest wins?
    - Identify critical path: minimum set of tasks to achieve objective
    - Flag risks: what could block each task?
    
  step_5_execute:
    - Start with highest-impact, lowest-risk tasks
    - After each task: measure progress toward objective
    - If measurement shows no improvement: re-evaluate approach
    - If new information emerges: update the plan
```

### 3. Self-Directed Execution

Once decomposed, AutoDream executes tasks autonomously:

```yaml
execution_loop:
  while objective_not_met:
    1. pick_next_task(priority_queue)
    2. check_dependencies(task)
       if blocked: skip, try next task
    3. execute(task)
       - Write code / make changes
       - Run relevant tests
       - Verify the change works
    4. measure_progress(objective_metric)
       if improved: log progress, continue
       if regressed: revert, try alternative approach
       if no_change: flag for review, continue
    5. update_plan(learnings)
       - Add new tasks discovered during execution
       - Remove tasks that became unnecessary
       - Adjust estimates based on actual velocity
```

### 4. Iterative Refinement

AutoDream improves its plan as it learns:

**Before starting:**
```
Plan: 12 tasks, estimated 3 days
Critical path: Profile → Optimize DB → Optimize App → Validate
Risk: "Unknown if caching will help without profiling data"
```

**After completing Goal 1 (profiling):**
```
Learning: "80% of latency is in 3 database queries, not the app layer"
Plan update: 
  - Expand Goal 2 (4 → 6 tasks, deeper DB optimization)
  - Reduce Goal 3 (3 → 1 task, app-layer optimization less impactful)
  - Revised estimate: 2 days (faster than expected)
```

### 5. Progress Reporting

```markdown
## AutoDream Progress Report

**Objective:** Reduce API response time by 90%
**Baseline:** p99 = 2,400ms | **Current:** p99 = 380ms (84% improvement)
**Status:** Goal 3 of 4 | Task 10 of 14

### Completed
| Task | Impact | Time |
|------|--------|------|
| Profile endpoints | Found 3 bottlenecks | 30m |
| Fix N+1 in /users | p99: 2400ms → 1200ms | 1h |
| Add Redis cache | p99: 1200ms → 600ms | 2h |
| Add indexes | p99: 600ms → 380ms | 45m |

### In Progress
- Compress responses (brotli) — expected 10-15% further improvement

### Remaining
- Background job for report generation
- Final load test validation

### Revised Estimate
Original: 3 days → **Revised: 1.5 days** (DB optimization was highest-impact)
```

### 6. Objective Templates

Common objective patterns AutoDream handles:

```yaml
performance_objective:
  template: "Make {system} {N}x {faster/cheaper/smaller}"
  decompose_into: [profile, optimize_hotspots, validate, benchmark]
  
quality_objective:
  template: "Get {project} to {quality_standard}"
  decompose_into: [audit_current, fix_critical, improve_coverage, certify]
  
growth_objective:
  template: "Grow {metric} from {current} to {target}"
  decompose_into: [analyze_funnel, identify_levers, implement_top3, measure]
  
migration_objective:
  template: "Migrate {system} from {old} to {new}"
  decompose_into: [assess_scope, plan_phases, migrate_incrementally, validate_parity]
```

## Example

**AutoDream decomposing "Get UitKit to trending on GitHub":**

```yaml
objective: "Get UitKit repository to GitHub Trending"
success_criteria: "Appear in daily or weekly trending for claude-code or developer-tools topic"

decomposition:
  goal_1_content_quality:
    - Fix all 107 frontmatter validation errors
    - Fix 6 manifest stub entries
    - Complete 3 incomplete workspace stacks
    - Add 20 high-value new skills (Q1 2026 features)
    
  goal_2_discoverability:
    - Add topic tags: claude-code, ai-coding, developer-tools, skills
    - Optimize README first 100 chars for GitHub preview
    - Add comparison table (UitKit vs competitors)
    - Create "Quick Start" section with install in 30 seconds
    
  goal_3_distribution:
    - Post on Reddit r/ClaudeAI, r/programming
    - Submit to awesome-claude-code list
    - Write "Introducing UitKit" blog post
    - Share in relevant Discord/Slack communities
    
  goal_4_validation:
    - Run all CI checks green
    - Verify install works on fresh machine
    - Test all 5 language localizations
    - Ensure all 42 stacks validate

execution_order: goal_1 → goal_4 → goal_2 → goal_3
reasoning: "Quality before visibility — trending with broken validation damages credibility"
```

## Anti-Patterns

- **Over-decomposition:** Breaking "add a button" into 15 sub-tasks — match granularity to task complexity
- **No measurement loop:** Executing all tasks without checking if the objective is actually being met — always measure after each goal
- **Rigid plans:** Not updating the plan when new information emerges — AutoDream must re-plan as it learns
- **Objective ambiguity:** "Make it better" has no measurable success criteria — always define what "done" means numerically
- **Infinite scope:** Not time-boxing the exploration phase — set a max exploration budget before committing to a plan
- **Parallel everything:** Trying to execute all sub-goals simultaneously without respecting dependencies — respect the critical path
