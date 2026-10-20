---
name: managing-cloud-custodian
description: |
  Use when working with Cloud Custodian — cloud Custodian policy engine
  management. Covers policy authoring, dry-run execution, resource filtering,
  action enforcement, multi-cloud support (AWS/Azure/GCP), Lambda deployment,
  compliance reporting, and policy organization. Use when managing Cloud
  Custodian policies, auditing cloud resources, enforcing compliance rules, or
  reviewing policy execution results.
connection_type: cloud-custodian
preload: false
---

# Cloud Custodian Management Skill

Manage and inspect Cloud Custodian policies, resource filters, actions, and compliance reports.

## MANDATORY: Discovery-First Pattern

**Always run policies in dry-run mode before enforcing actions.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Custodian Version ==="
custodian version 2>/dev/null

echo ""
echo "=== Policy Files ==="
find . -name "*.yml" -o -name "*.yaml" 2>/dev/null | while read f; do
    POLICIES=$(grep -c "^  - name:" "$f" 2>/dev/null || grep -c "^- name:" "$f" 2>/dev/null)
    [ "$POLICIES" -gt 0 ] && echo "$f: $POLICIES policies"
done | head -15

echo ""
echo "=== Policy Summary ==="
for f in $(find . -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -5); do
    grep -E "^\s+- name:|^\s+resource:" "$f" 2>/dev/null | paste - - | head -10
done | head -20

echo ""
echo "=== Output Directory ==="
ls -la output/ 2>/dev/null | head -10 || echo "No output directory found"
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

POLICY_FILE="${1:?Policy file required}"

echo "=== Validate Policies ==="
custodian validate "$POLICY_FILE" 2>&1 | tail -10

echo ""
echo "=== Dry Run ==="
custodian run --dryrun -s output/ "$POLICY_FILE" 2>&1 | tail -20

echo ""
echo "=== Resources Found ==="
for dir in output/*/; do
    POLICY_NAME=$(basename "$dir")
    COUNT=$(cat "$dir/resources.json" 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
    echo "$POLICY_NAME: $COUNT resources matched"
done | head -15

echo ""
echo "=== Sample Matches ==="
for dir in output/*/; do
    POLICY_NAME=$(basename "$dir")
    echo "--- $POLICY_NAME ---"
    cat "$dir/resources.json" 2>/dev/null | jq '.[0:3][] | {id: (.ResourceId // .InstanceId // .BucketName // .Name // .id), type: (.ResourceType // .InstanceType // "N/A")}' 2>/dev/null | head -10
done | head -25
```

## Output Format

```
CLOUD CUSTODIAN STATUS: <policy-file>
Policies: <count> | Resource Types: <unique types>
Validation: <passed|failed>
Dry Run Results:
  <policy-name>: <count> resources matched
  <policy-name>: <count> resources matched
Actions: <list of actions configured>
Issues: <any validation errors, empty matches, or action warnings>
```

## Safety Rules

- **NEVER run policies without `--dryrun` first** -- always preview matched resources
- **NEVER use destructive actions** (terminate, delete) without explicit user confirmation
- **Always validate policy files** before running -- `custodian validate`
- **Review matched resources** from dry-run output before enabling enforcement
- **Test policies on non-production accounts** before deploying to production

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

## Common Pitfalls

- **Filter specificity**: Overly broad filters can match unintended resources -- always dry-run first
- **Action ordering**: Actions execute in order -- ensure dependent actions are sequenced correctly
- **Lambda deployment**: Deployed Lambda policies run on schedule -- ensure they have correct IAM permissions
- **Cross-account access**: Multi-account policies require assumed roles in target accounts
- **Output storage**: Output directories grow over time -- configure S3 output for long-term storage
- **Rate limiting**: Policies querying many resources can hit API rate limits -- use `max-resources` safety
- **Mode configuration**: Pull mode runs once; Lambda/periodic modes run continuously -- understand the difference
