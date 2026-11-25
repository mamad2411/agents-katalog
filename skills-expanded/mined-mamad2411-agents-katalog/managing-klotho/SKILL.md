---
name: managing-klotho
description: |
  Use when working with Klotho — klotho cloud compiler and infrastructure
  generation. Covers application compilation, cloud target configuration,
  generated infrastructure inspection, deployment orchestration, and topology
  visualization. Use when using Klotho to compile applications to cloud
  infrastructure, reviewing generated IaC, or deploying to AWS.
connection_type: klotho
preload: false
---

# Klotho Management Skill

Manage Klotho-compiled applications, inspect generated infrastructure, and deploy to cloud targets.

## MANDATORY: Discovery-First Pattern

**Always inspect Klotho annotations and compilation output before deploying.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Klotho Version ==="
klotho --version 2>/dev/null

echo ""
echo "=== Project Config ==="
cat klotho.yaml 2>/dev/null || cat .klotho/config.yaml 2>/dev/null | head -20

echo ""
echo "=== Klotho Annotations ==="
grep -rn "@klotho" --include="*.ts" --include="*.py" --include="*.go" . 2>/dev/null | head -15

echo ""
echo "=== Application Structure ==="
ls -la 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Compile ==="
klotho . --app "${1:-myapp}" --provider aws 2>&1 | tail -15

echo ""
echo "=== Generated Infrastructure ==="
ls compiled/ 2>/dev/null | head -10 || ls .klotho/output/ 2>/dev/null | head -10

echo ""
echo "=== Resource Topology ==="
cat compiled/topology.json 2>/dev/null | jq '.resources[] | {type, name}' 2>/dev/null | head -20 || \
cat .klotho/output/topology.json 2>/dev/null | jq '.resources[] | {type, name}' 2>/dev/null | head -20

echo ""
echo "=== Generated Pulumi/Terraform ==="
find compiled/ -name "*.ts" -o -name "*.tf" 2>/dev/null | head -10 || \
find .klotho/output/ -name "*.ts" -o -name "*.tf" 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show topology summaries, not full generated code
- Summarize resource types and connections
- Display annotation usage patterns concisely

## Safety Rules
- **NEVER deploy without reviewing generated infrastructure**
- **Validate annotations** before compilation
- **Review generated IaC** in compiled output directory
- **Test with dry-run** before actual deployment
- **Check cloud permissions** match generated resource requirements

## Output Format

Present results as a structured report:
```
Managing Klotho Report
══════════════════════
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

