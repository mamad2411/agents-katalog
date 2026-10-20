---
name: analyzing-sonarqube
description: SonarQube code quality and security analysis. Use when working with code quality metrics, security hotspots, quality gates, or issue tracking in SonarQube Cloud or Server.
connection_type: sonarqube
preload: false
---

# Analyzing SonarQube

## Discovery

<critical>
**If no `[cached_from_skill:analyzing-sonarqube:discover]` context exists, run discovery first:**
```bash
bun run ./_skills/connections/sonarqube/analyzing-sonarqube/scripts/discover.ts
bun run ./_skills/connections/sonarqube/analyzing-sonarqube/scripts/discover.ts --max-projects 10
```
Output is auto-cached.
</critical>

**What discovery provides:**
- `projects`: All projects with `key`, `name`, `qualifier`, `visibility`
- `qualityGates`: Quality gate statuses per project (`OK`, `ERROR`, `WARN`)
- `issueSummary`: Per-project breakdown by severity (`BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`)
- `capabilities`: Available toolsets (analysis, issues, projects, quality-gates, rules, duplications, measures, security-hotspots, dependency-risks, coverage, sources, system)

## Tools

The SonarQube MCP server exposes tools organized by toolset. Organization and URL are handled automatically by the server — do NOT pass `organization` manually.

**Projects:** `search_my_sonarqube_projects(page?)`, `list_pull_requests(projectKey)`

**Issues:** `search_sonar_issues_in_projects(projects[]?, pullRequestId?, severities[]?, impactSoftwareQualities[]?, issueStatuses[]?, issueKey[]?, p?, ps?)`, `change_sonar_issue_status(key, status)` — severities: `INFO`, `LOW`, `MEDIUM`, `HIGH`, `BLOCKER`; issueStatuses: `OPEN`, `CONFIRMED`, `FALSE_POSITIVE`, `ACCEPTED`, `FIXED`

**Quality Gates:** `get_project_quality_gate_status(projectKey?, projectId?, analysisId?, pullRequest?)`, `list_quality_gates()`

**Rules:** `show_rule(key)`

**Measures:** `get_component_measures(projectKey, metricKeys[], pullRequest?)` — valid keys: `ncloc`, `coverage`, `bugs`, `vulnerabilities`, `code_smells`, `duplicated_lines_density`, `sqale_index`, `alert_status`. Do NOT guess metric keys — invalid keys cause 404 errors.

**Security Hotspots:** `search_security_hotspots(projectKey, hotspotKeys[]?, branch?, pullRequest?, files[]?, status?, resolution?, sinceLeakPeriod?, onlyMine?, p?, ps?)`, `show_security_hotspot(hotspotKey)`, `change_security_hotspot_status(hotspotKey, status, resolution?, comment?)`

**Duplications:** `search_duplicated_files(projectKey, pullRequest?, pageSize?, pageIndex?)`, `get_duplications(key, pullRequest?)`

**Coverage:** `search_files_by_coverage(projectKey, pullRequest?, maxCoverage?, pageIndex?, pageSize?)`, `get_file_coverage_details(key, pullRequest?, from?, to?)`

**Analysis:** `analyze_code_snippet(projectKey, fileContent, codeSnippet?, language?, scope?)`, `analyze_file_list(file_absolute_paths)`, `run_advanced_code_analysis(projectKey, branchName?, filePath?, fileContent?, fileScope?)`

**Sources:** `get_raw_source(key, pullRequest?)`, `get_scm_info(key, commits_by_line?, from?, to?)`

**Dependency Risks:** `search_dependency_risks(projectKey?, branchKey?, pullRequestKey?)`

**System (Server only):** `get_system_health()`, `get_system_info()`, `get_system_status()`, `ping_system()`, `get_system_logs(name?)`

<critical>
**EDITION LIMITS:** `dependency-risks` requires SonarQube Cloud or Server with Advanced Security license. `system` tools are Server-only. Check `capabilities` from discovery before using.
</critical>

## Quick Patterns

**Project overview:**
```typescript
const projects = await search_my_sonarqube_projects({});
const gate = await get_project_quality_gate_status({ projectKey: "my-project" });
```

**Issue investigation:**
```typescript
import type { Issue, QualityGateStatus } from "./_skills/connections/sonarqube/analyzing-sonarqube/schemas";
const issues = await search_sonar_issues_in_projects({
  projects: ["my-project"], severities: ["BLOCKER", "HIGH"], ps: 50
}) as { issues: Issue[] };
```

**Metrics analysis:**
```typescript
import type { Measure } from "./_skills/connections/sonarqube/analyzing-sonarqube/schemas";
const metrics = await get_component_measures({
  projectKey: "my-project",
  metricKeys: ["coverage", "bugs", "vulnerabilities", "code_smells", "duplicated_lines_density"]
}) as { component: { measures: Measure[] } };
```

**Security review:**
```typescript
import type { SecurityHotspot } from "./_skills/connections/sonarqube/analyzing-sonarqube/schemas";
const hotspots = await search_security_hotspots({
  projectKey: "my-project", status: "TO_REVIEW"
}) as { hotspots: SecurityHotspot[] };
```

**Coverage analysis:**
```typescript
const lowCoverage = await search_files_by_coverage({
  projectKey: "my-project", maxCoverage: 50, pageSize: 20
});
const details = await get_file_coverage_details({ key: "my-project:src/main.ts" });
```

<critical>
**ARRAY PARAMS:** Parameters marked with `[]` (projects, severities, issueStatuses, issueKey, impactSoftwareQualities, metricKeys, hotspotKeys, files) MUST be passed as arrays, NOT comma-separated strings. Example: `severities: ["BLOCKER", "HIGH"]` not `severities: "BLOCKER,HIGH"`. Passing strings causes `java.lang.String cannot be cast to class java.util.List`.

**PAGINATION:** Parameters use `p` (page number) and `ps` (page size), NOT `page`/`pageSize`. Default page size is 100. Start with `ps: 50` for exploration.
</critical>

## Workflows

**Quality Assessment**: `search_my_sonarqube_projects()` → `get_project_quality_gate_status(projectKey)` → `get_component_measures(metricKeys)` for overall health
**Security Audit**: `search_security_hotspots(status: "TO_REVIEW")` → `show_security_hotspot(key)` for details → `search_sonar_issues_in_projects(issueStatuses: ["OPEN"])`
**Issue Triage**: `search_sonar_issues_in_projects(severities: ["BLOCKER", "HIGH"])` → group by type → `show_rule(key)` for fix guidance
**Coverage Review**: `search_files_by_coverage(maxCoverage: 50)` → `get_file_coverage_details(key)` → identify gaps

## Common Errors

| Error | Solution |
| ----- | -------- |
| "Component not found" | Verify project key via `search_my_sonarqube_projects()` |
| "Insufficient privileges" | Check token permissions (Browse, Administer) |
| "Parameter required" | Ensure `projectKey` or `component` is provided |
| "Unknown metric" | Use `get_component_measures` with valid metric keys |
| "Invalid severities: MAJOR" or "CRITICAL" or "MINOR" | Old severity names removed. Use: `INFO`, `LOW`, `MEDIUM`, `HIGH`, `BLOCKER` |
| "not available" on dependency-risks | Requires Cloud or Advanced Security license |

## Anti-Patterns

- **Skip discovery**: Always run discovery first for project keys and available capabilities
- **Use old severity names** (`CRITICAL`, `MAJOR`, `MINOR`): These no longer exist. Only valid values: `INFO`, `LOW`, `MEDIUM`, `HIGH`, `BLOCKER`
- **Fetch all issues at once**: Use severity filters and pagination, start with `ps: 50`
- **Ignore quality gate**: Always check `get_project_quality_gate_status()` before deep-diving into issues
- **Raw metric keys**: Use descriptive groupings — reliability (bugs), security (vulnerabilities), maintainability (code_smells)
- **Assume all toolsets available**: Check `capabilities` from discovery; some may be disabled by server config or edition
- **Pass organization manually**: The MCP server injects organization automatically from its config — never pass it as a tool parameter
- **Use `page`/`pageSize`**: The correct params are `p` and `ps`
- **Guess metric keys**: Only use documented keys (`ncloc`, `coverage`, `bugs`, `vulnerabilities`, `code_smells`, `duplicated_lines_density`, `sqale_index`, `alert_status`). Keys like `complexity`, `security_rating`, `reliability_rating` cause 404 errors

## Output Format

Present results as a structured report:
```
Analyzing Sonarqube Report
══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

