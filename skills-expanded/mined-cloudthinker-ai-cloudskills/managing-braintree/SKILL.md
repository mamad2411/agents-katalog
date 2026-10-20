---
name: managing-braintree
description: |
  Use when working with Braintree — braintree payment gateway management
  including transactions, subscriptions, customers, payment methods, disputes,
  settlements, and merchant account configuration. Covers transaction success
  rates, decline analysis, settlement reporting, and fraud tool monitoring.
connection_type: braintree
preload: false
---

# Braintree Management Skill

Monitor and manage Braintree payment processing and merchant accounts.

## MANDATORY: Discovery-First Pattern

**Always discover merchant configuration and payment methods before querying transactions.**

### Phase 1: Discovery

```bash
#!/bin/bash
BT_ENV="${BRAINTREE_ENVIRONMENT:-sandbox}"
BT_API="https://payments${BT_ENV:+.$BT_ENV}.braintreegateway.com/merchants/${BRAINTREE_MERCHANT_ID}"
AUTH="-u ${BRAINTREE_PUBLIC_KEY}:${BRAINTREE_PRIVATE_KEY}"

echo "=== Merchant Account Info ==="
curl -s $AUTH -H "Content-Type: application/xml" \
  "$BT_API/merchant_accounts" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
for ma in root.findall('.//merchant-account'):
    print(f\"{ma.find('id').text} | Status: {ma.find('status').text} | Currency: {ma.find('currency-iso-code').text} | Default: {ma.find('default').text}\")
"

echo ""
echo "=== Plans (Subscriptions) ==="
curl -s $AUTH -H "Content-Type: application/xml" "$BT_API/plans" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
for p in root.findall('.//plan'):
    print(f\"{p.find('name').text} | ID: {p.find('id').text} | Price: {p.find('price').text} | Billing: {p.find('billing-frequency').text}\")
"

echo ""
echo "=== Add-ons & Discounts ==="
curl -s $AUTH -H "Content-Type: application/xml" "$BT_API/add_ons" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
for a in root.findall('.//add-on'):
    print(f\"Add-on: {a.find('name').text} | Amount: {a.find('amount').text}\")
" 2>/dev/null || echo "No add-ons configured"
```

**Phase 1 outputs:** Merchant accounts, subscription plans, add-ons

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Transaction Search (last 7 days) ==="
curl -s $AUTH -H "Content-Type: application/xml" \
  "$BT_API/transactions/advanced_search" \
  -d "<search><created-at><min>$(date -v-7d +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d '7 days ago' +%Y-%m-%dT%H:%M:%S)</min></created-at></search>" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
txns = root.findall('.//transaction')
statuses = {}
for t in txns:
    s = t.find('status').text
    statuses[s] = statuses.get(s, 0) + 1
for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f'{s}: {c}')
print(f'Total: {len(txns)}')
"

echo ""
echo "=== Disputes ==="
curl -s $AUTH "$BT_API/disputes" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
disputes = root.findall('.//dispute')
print(f'Open disputes: {len([d for d in disputes if d.find(\"status\").text in [\"open\", \"accepted\"]])}')
print(f'Total disputes: {len(disputes)}')
"

echo ""
echo "=== Active Subscriptions ==="
curl -s $AUTH -H "Content-Type: application/xml" \
  "$BT_API/subscriptions/advanced_search" \
  -d "<search><status><item>Active</item></status></search>" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
print(f'Active subscriptions: {len(root.findall(\".//subscription\"))}')
"
```

## Output Format

```
BRAINTREE STATUS
================
Merchant: {id} ({currency})
7-Day Transactions: {count} (Success: {pct}%)
Decline Rate: {percent}%
Active Subscriptions: {count}
Open Disputes: {count}
Settlement Pending: {amount}
Issues: {list_of_warnings}
```

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

- **Sandbox vs Production**: Different API endpoints — environment must match credentials
- **XML API**: Braintree uses XML for search — JSON available for GraphQL API
- **Transaction states**: settled vs settling vs authorized — understand the lifecycle
- **Duplicate checking**: Braintree has built-in duplicate detection — check gateway rejections
