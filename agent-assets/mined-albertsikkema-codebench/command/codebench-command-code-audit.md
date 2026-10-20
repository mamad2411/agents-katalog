---
description: "CB - Full-codebase audit"
---

You are the orchestrator for a comprehensive codebase audit. You run structural analysis via code-index MCP tools, then launch 6 specialized agents in parallel for deep investigation, and consolidate everything into a severity-ranked report.

## Why This Audit?

This audit systematically checks for the most common issues: missing security controls, no error handling, hardcoded secrets, missing observability, unvalidated dependencies, and missing documentation.

## Step 1: Reconnaissance (Phase 0)

Detect the technology stack before doing anything else. This context gets passed to all agents.

1. **Project overview**: Run `get_project_summary()` via code-index MCP tools
2. **Package manifests**: Glob for package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml, Gemfile, pom.xml, composer.json
3. **Framework config**: Glob for next.config.*, vite.config.*, nuxt.config.*, angular.json, django settings, flask app factory patterns
4. **Infrastructure**: Glob for Dockerfile, docker-compose.yml, kubernetes manifests
5. **Environment config**: Glob for environment variable example/sample/template files
6. **Entry points**: Use `search_symbols("main", kind="function")` and `search_symbols("app", kind="variable")` to find application entry points

Record:
- Primary language(s)
- Framework(s)
- Package manager
- Entry points and route definitions
- Whether it is a frontend, backend, fullstack, CLI, or library

If code-index MCP server is unavailable, fall back to Glob + Grep for recon. Note the limitation in the report.

## Step 2: Structural and Architecture Scan (Phases 2-3)

Run these code-index MCP tool calls directly -- no agent needed for deterministic analysis. Launch as many as possible in parallel:

- `find_bloated_functions(min_signals=2)`
- `find_unhandled_errors()`
- `find_duplicates(threshold=0.8)`
- `find_dead_code(confidence="high")`
- `find_deep_nesting(threshold=3)`
- `find_cognitive_complexity(threshold=10)` -- lower threshold to catch more issues
- `find_testability_issues()`
- `find_nested_loop_patterns()`
- `find_circular_deps()`
- `analyze_coupling()`
- `find_hotspots()`
- `find_temporal_coupling()`
- `find_feature_envy()`

Collect all results. These go into the Structural Analysis section of the report AND get summarized for agents.

If code-index MCP server is unavailable, skip this step and note the gap in the report.

## Step 3: Launch Agents (Phases 1, 4-7, 9)

Launch ALL 6 agents in a SINGLE message for parallel execution. Each agent receives the recon context from Step 1 and a summary of structural findings from Step 2.

Build a shared context block to include in every agent prompt:

```
## Recon Context
- Language(s): [from Step 1]
- Framework(s): [from Step 1]
- Package manager: [from Step 1]
- Entry points: [from Step 1]
- App type: [frontend/backend/fullstack/CLI/library]

## Structural Findings Summary
- Bloated functions: [count] found
- Unhandled errors: [count] found
- Dead code: [count] symbols
- Deep nesting: [count] found
- Complexity hotspots: [count] functions above threshold
- Circular deps: [count] cycles
[... other tool results summarized]
```

### Agent 1: Dependencies (audit-dependencies)

```
subagent_type: Audit Dependencies
prompt: |
  Run a full dependency audit on this codebase.

  [shared context block]

  Package manifests found: [list from recon]

  Follow your instructions: check for CVEs, hallucinated packages, abandoned deps, and license issues.
```

### Agent 2: Security (audit-security)

```
subagent_type: Audit Security
prompt: |
  Run a full security audit on this codebase.

  [shared context block]

  Follow your instructions: run secret scan, then systematic 39-check security review.
```

### Agent 3: Data Governance (audit-data-governance)

```
subagent_type: Audit Data Governance
prompt: |
  Run a full data governance audit on this codebase.

  [shared context block]

  Follow your instructions: inventory PII, trace data flows, check GDPR basics.
```

### Agent 4: Observability (audit-observability)

```
subagent_type: Audit Observability
prompt: |
  Run a full observability audit on this codebase.

  [shared context block]

  Follow your instructions: check logging, structured logging, correlation IDs, audit trails.
```

### Agent 5: Resilience (audit-resilience)

```
subagent_type: Audit Resilience
prompt: |
  Run a full resilience audit on this codebase.

  [shared context block]

  Follow your instructions: check timeouts, retries, circuit breakers, health checks, config safety.
```

### Agent 6: Documentation (audit-documentation)

```
subagent_type: Audit Documentation
prompt: |
  Run a full documentation audit on this codebase.

  [shared context block]

  Follow your instructions: evaluate README, setup instructions, env var docs, architecture docs.
```

## Step 4: Consolidate Report

Once all agents return, build the final report using the template at `.claude/templates/code-audit-report.md`:

1. **Fill in metadata**: project name, date, languages, frameworks from recon
2. **Assign overall risk rating**:
   - CRITICAL: any critical findings exist
   - HIGH: no critical but 3+ high findings
   - MEDIUM: no critical, fewer than 3 high, but medium findings exist
   - LOW: only low/informational findings
3. **Merge findings by severity**: combine all agent findings into Critical / High / Medium / Low buckets
4. **Deduplicate**: if multiple agents flag the same file:line, keep the most detailed finding
5. **Fill severity count table** in executive summary
6. **Include structural analysis** from Step 2
7. **Include full agent reports** in the collapsible details sections
8. **Include manual verification checklist** (runtime + manual review items)

Save the report to `.claude/memories/YYYY-MM-DD-code-audit.md` (use today's date).

## Step 5: Present Results

After saving, present a summary to the user:

```
## Code Audit Complete

**Overall Risk Rating**: [rating]
**Report saved to**: .claude/memories/YYYY-MM-DD-code-audit.md

### Finding Counts
| Severity | Count |
|----------|-------|
| Critical | X |
| High | Y |
| Medium | Z |
| Low | W |

### Top Issues
1. [Most critical finding - one line]
2. [Second most critical - one line]
3. [Third most critical - one line]

The full report includes detailed findings from all 6 audit agents plus structural analysis.
```

## Error Handling

- **Code-index MCP unavailable**: Fall back to Glob/Grep for recon, skip structural scan, note gaps in report
- **Agent fails/times out**: Note the gap in the report section for that agent, continue with others
- **Audit tools unavailable** (npm audit, pip audit, etc.): Dependencies agent notes which tools were unavailable
- **Empty/minimal repo**: Agents should note "insufficient code to analyze" rather than producing false negatives

## Remember

- Launch ALL 6 agents in ONE message -- parallel execution is the main performance lever
- Pass recon context to every agent so they do not waste time rediscovering the stack
- Run code-index tools directly in Step 2 -- no agent overhead for deterministic analysis
- Full agent reports go in collapsible details blocks -- do not lose detail
- The manual verification checklist (runtime + manual review) is always included even though it is not automated
