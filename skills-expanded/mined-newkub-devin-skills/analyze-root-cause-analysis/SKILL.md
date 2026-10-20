---
name: analyze-root-cause-analysis
description: Analyze the root cause of problems with a systematic method
argument-hint: "[target]"
related:
  - deep-review-codebase
  - deep-debug
  - use-bun-shell
  - resolve-errors

---

## Goal

Find the root cause of a problem with a systematic method to prevent it from recurring

## Scope

Use `analyze-root-cause-analysis` for the specific tasks and workflows it covers (root cause analysis)

## Execute

### 1. Gather Evidence

> Goal: Collect information and evidence related to the problem

Collect all information and evidence related to the problem

1. Run `/deep-debug` to gather baseline data
2. Collect relevant logs, metrics, and traces
3. Collect screenshots, error messages, and stack traces
4. Collect a timeline of events
5. Collect environment information (version, config, dependencies)

### 2. Construct Causal Graph (Graph Theory)

> Goal: Build a DAG of causal relationships to order events

Build a Directed Acyclic Graph (DAG) of causal relationships:

Formula: G = (V, E) where V = nodes (events/variables), E = directed edges (causal links)

Steps:
1. Identify all relevant nodes V = {v₁, v₂, ..., vₙ} (deploy, config, traffic, error)
2. Create directed edges E = {(vᵢ → vⱼ)} for causal relationships
3. Verify the graph is a DAG (no cycles)
4. Use Topological Sort to order the causal chain
5. Mark root nodes (nodes with no incoming edges) as potential root causes

### 3. Use 5 Whys (Causal Inference)

> Goal: Apply the 5 Whys technique with causal inference to trace the root cause

Apply the 5 Whys technique together with Causal Inference:

Formula: P(Y | do(X)) = causal effect of X on Y

Steps:
1. Start from the observed problem (effect node)
2. Ask "why" 5 times, tracing backward through the causal graph
3. Each answer must be a parent node in the DAG
4. Use do-calculus to verify the intervention actually fixes the problem
5. Stop at a root node that can be intervened on

Example:
- Problem: Server crash
- Why 1: Out of memory
- Why 2: Memory leak
- Why 3: Unclosed database connections
- Why 4: Missing connection pool cleanup
- Why 5: No proper shutdown handler in deployment script
- Root Cause: The deployment script has no shutdown handler

### 4. Analyze Causal Paths (Graph Theory)

> Goal: Analyze causal paths in the DAG to find the most important nodes

Analyze causal paths in the DAG:

Formula: Path(vᵢ → vⱼ) = sequence of edges from vᵢ to vⱼ

Steps:
1. Identify every causal path from root nodes to the effect node
2. Compute path length (number of edges) and path strength
3. Use Betweenness Centrality to find the most important nodes
4. Identify bottleneck nodes (nodes present in many paths)
5. Pick the root node with the shortest and strongest causal paths

### 5. Validate Causal Hypothesis (Causal Inference)

> Goal: Test the causal hypothesis with an intervention

Validate the causal hypothesis with an intervention:

Formula: P(Y | do(X)) ≠ P(Y | X) means X is a causal cause

Steps:
1. Run `/use-bun-shell` to test the intervention do(X)
2. Create a test case that reproduces the problem
3. Compare P(Y | do(X)) with P(Y | X)
4. If P(Y | do(X)) ≠ P(Y | X) → X is a causal cause
5. Check that no confounding variables are hidden

### 6. Document Root Cause

> Goal: Record the root cause and the detailed analysis

Record the root cause and the detailed analysis

1. Write an RCA (Root Cause Analysis) report
2. State the root cause clearly
3. Explain the analysis method
4. Attach all evidence
5. List action items for prevention

### 7. Define Preventive Actions

> Goal: Define actions to prevent the problem from recurring

Define actions to prevent recurrence

1. Run `/resolve-errors` to fix the current problem
2. Add monitoring/alerting to detect problems early
3. Add test cases to prevent regressions
4. Update documentation and runbooks
5. Run training or knowledge sharing with the team

## Rules

### 1. Evidence-Based

Every conclusion must be backed by evidence

- Collect all logs, metrics, and traces
- Decide with data, not gut feeling
- Record the source of every piece of evidence

### 2. 5 Whys Technique

Use the 5 Whys technique correctly

- Each answer must be a cause, not a symptom
- Stop when you reach a fixable point
- Don't stop at human error (usually a symptom of a bad process)

### 3. Causal Graph Theory

Use Graph Theory for causal analysis:

- Build a DAG (Directed Acyclic Graph) for causal relationships
- Use Topological Sort to order the causal chain
- Use Betweenness Centrality to find key nodes
- Analyze causal paths from root to effect
- Verify there are no cycles (confounding loops)

### 4. Causal Inference Standards

Causal hypotheses must be validated with interventions:

- Use do-calculus to verify causal effect
- Compare P(Y | do(X)) with P(Y | X)
- Check for hidden confounding variables
- Verify the intervention actually fixes the problem

### 5. Documentation Requirements

Document the RCA in detail

- State the root cause clearly
- Explain the analysis method
- Attach all evidence
- List action items for prevention

- Use /deep-review-codebase if needed
## Expected Outcome

- Root cause clearly identified
- Every conclusion backed by evidence
- Clear preventive actions
- Complete documentation
- The problem does not recur
