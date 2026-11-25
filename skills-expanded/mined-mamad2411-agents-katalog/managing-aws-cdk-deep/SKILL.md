---
name: managing-aws-cdk-deep
description: |
  Use when working with Aws Cdk Deep — aWS CDK application and stack management.
  Covers stack synthesis, CloudFormation template inspection, diff analysis,
  deployment orchestration, context values, asset management, and construct
  library usage. Use when managing CDK apps, debugging synthesis errors,
  reviewing stack diffs, or analyzing deployed CloudFormation resources.
connection_type: aws-cdk
preload: false
---

# AWS CDK Deep Management Skill

Manage AWS CDK applications, synthesize templates, analyze diffs, and deploy stacks.

## MANDATORY: Discovery-First Pattern

**Always inspect CDK app structure and synth output before deploying.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== CDK Version ==="
cdk --version 2>/dev/null

echo ""
echo "=== CDK App Stacks ==="
cdk ls 2>/dev/null | head -20

echo ""
echo "=== Project Config ==="
cat cdk.json 2>/dev/null | jq '{app, context}' | head -15

echo ""
echo "=== CDK Context ==="
cdk context 2>/dev/null | head -15

echo ""
echo "=== Dependencies ==="
if [ -f package.json ]; then
  jq '{aws_cdk: .dependencies["aws-cdk-lib"], constructs: .dependencies["constructs"]}' package.json 2>/dev/null
elif [ -f requirements.txt ]; then
  grep -i "aws-cdk" requirements.txt 2>/dev/null
fi
```

### Phase 2: Analysis

```bash
#!/bin/bash
STACK="${1:-}"

echo "=== Synth ==="
cdk synth ${STACK:+"$STACK"} --quiet 2>&1 | tail -5

echo ""
echo "=== Stack Diff ==="
cdk diff ${STACK:+"$STACK"} 2>&1 | tail -30

echo ""
echo "=== CloudFormation Resources ==="
if [ -n "$STACK" ]; then
  TEMPLATE="cdk.out/${STACK}.template.json"
else
  TEMPLATE=$(ls cdk.out/*.template.json 2>/dev/null | head -1)
fi
if [ -f "$TEMPLATE" ]; then
  jq '.Resources | to_entries | group_by(.value.Type) | map({type: .[0].value.Type, count: length}) | sort_by(-.count)' "$TEMPLATE" | head -20
fi

echo ""
echo "=== Stack Outputs ==="
if [ -f "$TEMPLATE" ]; then
  jq '.Outputs // {} | keys' "$TEMPLATE" 2>/dev/null
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show resource type summaries, not full template dumps
- Use `--quiet` synth to reduce noise
- Summarize diffs by resource type

## Safety Rules
- **NEVER run `cdk deploy` without `cdk diff` first**
- **Always bootstrap** target accounts/regions before first deploy
- **Review IAM changes carefully** in diff output
- **Use `--require-approval broadening`** for security-sensitive stacks
- **Check for resource replacements** that could cause data loss

## Output Format

Present results as a structured report:
```
Managing Aws Cdk Deep Report
════════════════════════════
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

