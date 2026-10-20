---
name: managing-gcp-policy-intelligence
description: |
  Use when working with Gcp Policy Intelligence — gCP Policy Intelligence and
  IAM recommender management. Covers IAM recommender insights, policy analyzer,
  policy troubleshooter, access approval settings, and security health
  analytics. Use when analyzing IAM permissions, reviewing policy
  recommendations, troubleshooting access denials, or optimizing least-privilege
  access across GCP resources.
connection_type: gcp-policy-intelligence
preload: false
---

# GCP Policy Intelligence Management Skill

Manage GCP Policy Intelligence tools including IAM recommender, policy analyzer, and troubleshooter.

## MANDATORY: Discovery-First Pattern

**Always inspect current IAM state and recommendations before changes.**

### Phase 1: Discovery

```bash
#!/bin/bash
PROJECT="${1:-$(gcloud config get-value project 2>/dev/null)}"

echo "=== IAM Recommender Insights ==="
gcloud recommender insights list --project="$PROJECT" --insight-type=google.iam.policy.Insight --location=global --format='table(name.basename(),description,stateInfo.state)' 2>/dev/null | head -15

echo ""
echo "=== IAM Recommendations ==="
gcloud recommender recommendations list --project="$PROJECT" --recommender=google.iam.policy.Recommender --location=global --format='table(name.basename(),description,stateInfo.state,priority)' 2>/dev/null | head -15

echo ""
echo "=== Service Account Insights ==="
gcloud recommender insights list --project="$PROJECT" --insight-type=google.iam.serviceAccount.Insight --location=global --format='table(name.basename(),description)' 2>/dev/null | head -10

echo ""
echo "=== Unused Service Accounts ==="
gcloud recommender recommendations list --project="$PROJECT" --recommender=google.iam.serviceAccount.Recommender --location=global --format='table(name.basename(),description,priority)' 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
PROJECT="${1:-$(gcloud config get-value project 2>/dev/null)}"
MEMBER="${2:-}"

echo "=== Policy Analyzer ==="
if [ -n "$MEMBER" ]; then
  gcloud asset analyze-iam-policy --organization="$(gcloud organizations list --format='value(name)' --limit=1 2>/dev/null)" --identity="$MEMBER" --format='table(identityList.identities,accessControlLists.accesses.role)' 2>/dev/null | head -20
fi

echo ""
echo "=== Policy Troubleshooter ==="
RESOURCE="${3:-}"
PERMISSION="${4:-}"
if [ -n "$MEMBER" ] && [ -n "$RESOURCE" ] && [ -n "$PERMISSION" ]; then
  gcloud policy-troubleshoot iam "$RESOURCE" --permission="$PERMISSION" --principal-email="$MEMBER" 2>/dev/null | head -20
fi

echo ""
echo "=== Excess Permissions ==="
gcloud recommender insights list --project="$PROJECT" --insight-type=google.iam.policy.Insight --location=global --filter="category=PERMISSION_USAGE" --format='table(description,stateInfo.state)' 2>/dev/null | head -10

echo ""
echo "=== Lateral Movement Risks ==="
gcloud recommender insights list --project="$PROJECT" --insight-type=google.iam.policy.Insight --location=global --filter="category=SECURITY" --format='table(description,severity)' 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show recommendation summaries with priority
- Highlight unused permissions and service accounts
- Summarize policy analysis results concisely

## Safety Rules
- **NEVER apply IAM recommendations without reviewing the role changes**
- **Test permission removals** on non-production projects first
- **Review service account usage** before disabling
- **Check dependent workloads** before revoking permissions
- **Use policy troubleshooter** to verify access before/after changes

## Output Format

Present results as a structured report:
```
Managing Gcp Policy Intelligence Report
═══════════════════════════════════════
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

