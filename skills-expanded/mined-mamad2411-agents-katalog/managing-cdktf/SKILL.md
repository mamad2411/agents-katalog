---
name: managing-cdktf
description: |
  Use when working with Cdktf — cDK for Terraform (CDKTF) project and stack
  management. Covers project synthesis, provider generation, stack deployment,
  output inspection, and diff analysis using TypeScript, Python, Go, Java, or
  C#. Use when working with CDKTF projects, synthesizing Terraform
  configurations, deploying stacks, or debugging provider bindings.
connection_type: cdktf
preload: false
---

# CDKTF Management Skill

Manage CDK for Terraform projects, synthesize HCL, deploy stacks, and inspect outputs.

## MANDATORY: Discovery-First Pattern

**Always inspect the CDKTF project structure and synthesized output before deploying.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== CDKTF Version ==="
cdktf --version 2>/dev/null

echo ""
echo "=== Project Structure ==="
cat cdktf.json 2>/dev/null | jq '{language, app, terraformProviders: (.terraformProviders // [] | length), terraformModules: (.terraformModules // [] | length)}'

echo ""
echo "=== Stacks ==="
cdktf list 2>/dev/null | head -15

echo ""
echo "=== Generated Providers ==="
ls .gen/providers/ 2>/dev/null | head -10 || echo "No generated providers found"

echo ""
echo "=== Dependencies ==="
if [ -f package.json ]; then
  jq '.dependencies // {} | keys' package.json 2>/dev/null | head -15
elif [ -f requirements.txt ]; then
  head -15 requirements.txt
fi
```

### Phase 2: Analysis

```bash
#!/bin/bash
STACK="${1:-}"

echo "=== Synth Output ==="
cdktf synth 2>&1 | tail -10

echo ""
echo "=== Synthesized Stacks ==="
ls cdktf.out/stacks/ 2>/dev/null

echo ""
if [ -n "$STACK" ]; then
  echo "=== Stack Plan ($STACK) ==="
  cdktf diff "$STACK" 2>&1 | tail -30
else
  echo "=== Default Stack Plan ==="
  cdktf diff 2>&1 | tail -30
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Always synth before diff or deploy
- Show resource counts from synthesized output, not full HCL
- Summarize provider versions rather than listing all bindings

## Safety Rules
- **NEVER run `cdktf deploy` without `cdktf diff` first**
- **Always run `cdktf synth`** to validate before deployment
- **Review generated Terraform** in `cdktf.out/` before applying
- **Pin provider versions** in `cdktf.json` for reproducibility
- **Use `--auto-approve` only** when explicitly confirmed

## Output Format

Present results as a structured report:
```
Managing Cdktf Report
═════════════════════
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

