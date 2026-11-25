---
name: execution-plan-generator
description: Generates a sprint execution plan from a GitHub epic/milestone
version: 1.0.0
triggers:
  - "generate execution plan"
  - "create sprint plan"
  - "plan epic"
  - "execution plan for"
inputs:
  repo:
    description: "GitHub repo in org/name format"
    required: true
    example: "owner/repo"
  epic:
    description: "Epic issue number (the parent issue that references sub-issues)"
    required: true
    example: 42
  base_branch:
    description: "Base branch for development"
    required: false
    default: "main"
  clone:
    description: "Whether to clone the repo for codebase analysis"
    required: false
    default: false
  wip_limit:
    description: "Override WIP limit (auto-calculated if omitted)"
    required: false
output: markdown
output_path: "execution-plan-{repo_name}-{epic}.md"
tools:
  - gh
---

# Execution Plan Generator

Generates a structured sprint execution plan from a GitHub epic. Analyzes issues, infers dependencies, assigns parallel lanes, and outputs a sprint-runner-compatible markdown plan.

## Quick Start

```
Given repo owner/repo and epic #42, generate an execution plan.
```

## How It Works

### Phase 1: Issue Collection

**Detect the tracker type first.** The plan's `tracker` config field determines how to fetch issues:

#### GitHub Issues (default)
```bash
# Get the epic issue body (contains task list with issue references)
gh issue view {epic} --repo {repo} --json title,body,labels

# Extract referenced issue numbers from the epic body
# Patterns: - [ ] #N, - [x] #N, #N, {repo}#N

# Fetch each referenced issue
gh issue view {N} --repo {repo} --json number,title,body,labels,state,assignees
```

If the epic uses a milestone instead:
```bash
gh issue list --repo {repo} --milestone "{milestone}" --state all --json number,title,body,labels,assignees --limit 100
```

#### Linear
```bash
# Use linear CLI or GraphQL API
linear issue list --project "{project_name}" --state "Backlog,Todo,In Progress"
# Or fetch by parent issue identifier
```

**Important:** Don’t assume tracker type from the repo. Check the plan config or ask.

### Phase 2: Issue Analysis

For each issue, extract structured data from the body:

1. **Title keywords** — classify by type (contract, schema, security, adapter, test, docs, config)
2. **Acceptance criteria** — look for `## Acceptance Criteria`, `## AC`, `- [ ]` checklists
3. **File hints** — paths mentioned in body (`src/`, `pkg/`, `*.go`, `*.ts`, etc.)
4. **Explicit dependencies** — phrases like "depends on #N", "after #N", "requires #N", "blocked by #N"
5. **Labels** — priority labels (P0, P1, P2), type labels (bug, feature, security)

### Phase 3: Codebase Analysis (Optional)

If `clone: true` or a local clone exists:

```bash
# Clone to temp directory
git clone --depth 1 https://github.com/{repo}.git /tmp/plan-{repo_name}

# Analyze structure
find . -name '*.go' -o -name '*.ts' -o -name '*.py' -o -name '*.rs' | head -200
cat go.mod 2>/dev/null || cat package.json 2>/dev/null  # dependency structure

# Hot file analysis (most changed files recently)
git log --oneline --name-only -100 | grep -E '\.(go|ts|py|rs|java)$' | sort | uniq -c | sort -rn | head -20
```

This provides:
- Package/module layout for better file-overlap detection
- Hot files that are likely merge-conflict zones
- Import graph hints for dependency inference

### Phase 4: Dependency Inference

Dependencies are inferred using a layered heuristic system. **Conservative by default** — when unsure, serialize.

#### 4.1 Explicit Dependencies (Highest Confidence)

Scan each issue body for:
```
depends on #N, depends on #{N}
after #N, after #{N}
requires #N, requires #{N}
blocked by #N, blocked by #{N}
must complete #N first
prerequisite: #N
```

These create hard edges in the dependency graph.

#### 4.2 Semantic Type Ordering (High Confidence)

Issues are classified into types, and types have a natural ordering:

```
Layer 0 (Foundation):   schema, contract, interface, types, proto
Layer 1 (Security):     security, auth, rbac, policy, validation
Layer 2 (Core):         core logic, engine, service, handler
Layer 3 (Integration):  adapter, connector, plugin, loader, client
Layer 4 (Quality):      test, e2e, integration-test, benchmark
Layer 5 (Adoption):     docs, migration, rollout, config, ci/cd
```

**Rule:** An issue at Layer N is assumed to depend on any Layer <N issue that touches the same package/area, unless evidence suggests otherwise.

Classification heuristics (applied to title + labels):
- **Schema/Contract:** title contains "schema", "contract", "interface", "types", "proto", "API", "model"
- **Security:** title contains "security", "auth", "rbac", "policy", "validation", "permission"
- **Core:** title contains "implement", "engine", "service", "handler", "core", "logic"
- **Integration:** title contains "adapter", "connector", "plugin", "loader", "client", "integration"
- **Test:** title contains "test", "e2e", "benchmark", "coverage"
- **Adoption:** title contains "doc", "migration", "rollout", "config", "CI", "deploy", "README"

#### 4.3 File Overlap Analysis (Medium Confidence)

For each issue, estimate which files/packages it will touch:
1. **Explicit paths** mentioned in the issue body
2. **Package inference** from keywords (e.g., "loader" → `pkg/loader/`, `src/loader/`)
3. **Codebase matching** (if clone available) — grep for types/functions mentioned in the issue

When two issues have **>50% file overlap**, they should be serialized (same lane). When overlap is **<20%**, they can safely parallelize.

Between 20-50%: serialize (conservative default).

#### 4.5 Hot File / Conflict-Prone File Warning

If codebase analysis is available, identify **high-churn files** (from `git log`) that appear in multiple issues. These are merge-conflict magnets.

```bash
# Top 20 most-changed files in recent history
git log --oneline --name-only -100 | grep -E '\.(go|ts|py|rs|java)$' | sort | uniq -c | sort -rn | head -20
```

**For any file that appears in 3+ issues:** Force serialization or add an explicit warning in the plan:
```
⚠️ CONFLICT RISK: pkg/engine/evaluate.go appears in issues #101, #103, #107
   → Serialize these or expect merge conflicts after each merge
```

Common conflict-prone patterns:
- Go import blocks (parallel lanes both adding imports)
- Registration/init files (blank imports, Register() calls)
- `go.sum` / `package-lock.json` (always auto-resolvable, but flag them)
- Shared constants/enum files

#### 4.4 Keyword Cross-References (Low Confidence)

If issue #M's body mentions a type, function, or concept that is the primary deliverable of issue #N, infer #M depends on #N. Examples:
- #N title: "Define PolicyDocument schema"
- #M body: "Load PolicyDocument from YAML" → #M likely depends on #N

### Phase 5: Lane Assignment Algorithm

#### 5.1 Build the DAG

From Phase 4, construct a directed acyclic graph (DAG). If cycles are detected, break them by removing the lowest-confidence edge.

#### 5.2 Topological Sort with Grouping

1. Compute topological order of the DAG
2. Assign each issue a **depth** (longest path from any root)
3. Issues at the same depth with no mutual dependencies are candidates for parallelization

#### 5.3 Lane Construction

```
Algorithm: Greedy Lane Assignment

1. Sort issues by depth (ascending), then by type layer (ascending)
2. Initialize empty lanes = []
3. For each issue I in sorted order:
   a. Find all lanes where I has no dependency conflict
      (I's dependencies are all in earlier positions of that lane or other lanes)
   b. Among valid lanes, pick the one with LEAST file overlap with I
   c. If no valid lane exists, or all have >30% file overlap, create new lane
   d. Append I to the chosen lane
4. Name each lane by its dominant theme (most common type classification)
```

#### 5.4 Phase Assignment

Group lanes into execution phases:

| Phase | Contents | Entry Criteria |
|-------|----------|----------------|
| P0 | Foundation schemas, contracts, security | None — start immediately |
| P1 | Core implementation that consumes P0 outputs | P0 complete |
| P2 | Integration, adapters, connectors | Relevant P1 items complete |
| P3 | Testing, e2e, benchmarks | P2 complete (or relevant P1) |
| P4 | Docs, migration, rollout, CI/CD | P3 complete (or can start with P2) |

Issues within a phase can run in parallel across lanes.

### Phase 6: WIP Limit Calculation

```
Recommended WIP = min(
  floor(sqrt(total_issues)),
  number_of_lanes,
  3  # hard cap for solo dev, 5 for team
)
```

For reference: 13 issues → WIP 2-3, 25 issues → WIP 3-4, 50 issues → WIP 4-5.

Factors that reduce WIP:
- High file overlap across issues (merge conflict risk)
- Many security-critical issues (need careful review)
- Unfamiliar codebase

Factors that increase WIP:
- Well-separated packages (microservice-like)
- Strong test coverage (safe to parallelize)
- Multiple developers available

### Phase 7: Output Generation

Generate the execution plan markdown using the template in `references/plan-template.md`.

For each issue's **Dev prompt**, synthesize:
1. Which files to create/modify (from file analysis)
2. Key acceptance criteria (from issue body)
3. Dependencies to be aware of (what contracts/interfaces to consume)
4. Testing expectations
5. Any gotchas from codebase analysis

## Edge Cases

### Epic with no task list
Fall back to milestone-based issue collection, or search for issues with a specific label.

### Circular dependencies detected
Log a warning. Break the cycle at the weakest edge (lowest confidence heuristic). Add a note in the plan.

### Issues with no body
Classify by title only. Add a warning in the dev prompt: "Issue body is empty — clarify requirements before starting."

### More than 50 issues
Recommend splitting into sub-epics. Generate plan for the first ~25 highest-priority issues and note the remainder.

### Cross-repo dependencies
Note them in the dependency graph with full `org/repo#N` syntax. These become external blockers, not lane-internal dependencies.

## Example

Input:
```
repo: owner/repo
epic: #42
clone: true
```

Output structure (13 issues):
```
6 lanes (A-F), 5 phases, WIP limit: 2

Lane A (Contracts):     #1 → #5 → #9
Lane B (Security):      #2 → #6
Lane C (Core):          #3 → #7 → #11
Lane D (Loaders):       #4 → #8 → #12
Lane E (Testing):       #10 → #13
Lane F (Adoption):      #14

Phase 0: #1, #2          (contracts + security — no deps)
Phase 1: #3, #4, #5      (core + loaders consume contracts)
Phase 2: #6, #7, #8      (security integration + core features)
Phase 3: #9, #10, #11    (advanced contracts + testing)
Phase 4: #12, #13, #14   (final adapters + adoption)
```

## Dev Prompt Authoring Guidelines

When generating dev prompts for each issue, follow these rules to avoid subagent failures:

1. **Keep prompts plain English** — no shell metacharacters, no backticks, no heredocs, no nested quotes
2. **Reference code examples via files** — if you need to show patterns, write them to a temp file and reference the path
3. **Be specific about file paths** — `Create pkg/adapters/terraform/adapter.go` not `Create the adapter file`
4. **Include the test command** — `Run: go test ./pkg/adapters/terraform/...` so the agent knows how to verify
5. **Avoid `$()`, backtick substitution, or complex quoting** in prompt text — these cause shell parse errors when the prompt is passed through an agent runner / CLI wrapper

**Anti-pattern (breaks):**
```
Implement the adapter using `func NewAdapter() *Adapter { return &Adapter{} }`
```

**Correct (works):**
```
Create a NewAdapter constructor that returns a pointer to Adapter. Follow the pattern in pkg/adapters/opa/adapter.go.
```

## References

- `references/plan-template.md` — Full output template with field descriptions
