---
name: managing-adyen
description: |
  Use when working with Adyen — adyen payment platform management including
  merchant accounts, payment methods, terminal configuration, risk management,
  settlement reports, and webhook notifications. Covers authorization rates,
  payment method performance, fraud scoring, and payout reconciliation.
connection_type: adyen
preload: false
---

# Adyen Management Skill

Monitor and manage Adyen payment processing infrastructure.

## MANDATORY: Discovery-First Pattern

**Always discover merchant accounts and payment methods before querying transaction data.**

### Phase 1: Discovery

```bash
#!/bin/bash
ADYEN_API="https://${ADYEN_ENVIRONMENT:-checkout-test}.adyen.com"
MGMT_API="https://management-${ADYEN_ENVIRONMENT:-test}.adyen.com/v3"
AUTH="X-API-Key: ${ADYEN_API_KEY}"

echo "=== Company Account ==="
curl -s -H "$AUTH" "$MGMT_API/companies/${ADYEN_COMPANY_ID}" | \
  jq -r '"Company: \(.name)\nStatus: \(.status)\nData Centers: \(.dataCenters | join(", "))"'

echo ""
echo "=== Merchant Accounts ==="
curl -s -H "$AUTH" "$MGMT_API/companies/${ADYEN_COMPANY_ID}/merchants" | \
  jq -r '.data[] | "\(.name) | ID: \(.id) | Status: \(.status) | Channels: \(.salesChannels)"'

echo ""
echo "=== Payment Methods ==="
curl -s -H "$AUTH" -H "Content-Type: application/json" \
  "$ADYEN_API/v71/paymentMethods" \
  -d "{\"merchantAccount\": \"${ADYEN_MERCHANT_ACCOUNT}\"}" | \
  jq -r '.paymentMethods[] | "\(.name) | Type: \(.type) | Brands: \(.brands // [] | join(","))"'

echo ""
echo "=== Webhooks ==="
curl -s -H "$AUTH" "$MGMT_API/merchants/${ADYEN_MERCHANT_ACCOUNT}/webhooks" | \
  jq -r '.data[] | "\(.type) | URL: \(.url) | Active: \(.active) | SSL: \(.sslVersion)"'
```

**Phase 1 outputs:** Company info, merchant accounts, payment methods, webhooks

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Authorization Rate (via reporting) ==="
curl -s -H "$AUTH" -H "Content-Type: application/json" \
  "https://reporting-${ADYEN_ENVIRONMENT:-test}.adyen.com/v1/analytics/transactions" \
  -d "{
    \"merchantAccountCode\": \"${ADYEN_MERCHANT_ACCOUNT}\",
    \"timeRange\": {\"startDate\": \"$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d)\", \"endDate\": \"$(date +%Y-%m-%d)\"}
  }" | jq -r '"Authorized: \(.authorized)\nRefused: \(.refused)\nAuth Rate: \(.authorizationRate)%"' 2>/dev/null || echo "Reporting API requires separate access"

echo ""
echo "=== Terminal Status ==="
curl -s -H "$AUTH" "$MGMT_API/merchants/${ADYEN_MERCHANT_ACCOUNT}/terminals?pageSize=20" | \
  jq -r '.data[] | "\(.id) | Model: \(.model) | Status: \(.connectivity.status) | Firmware: \(.firmwareVersion)"' 2>/dev/null || echo "No terminals configured"

echo ""
echo "=== Risk Rules ==="
curl -s -H "$AUTH" "$MGMT_API/merchants/${ADYEN_MERCHANT_ACCOUNT}/riskSettings" | \
  jq -r '.rules[] | "\(.description) | Enabled: \(.enabled) | Action: \(.action)"' 2>/dev/null || echo "Risk settings require additional permissions"

echo ""
echo "=== Recent Payouts ==="
curl -s -H "$AUTH" "$MGMT_API/merchants/${ADYEN_MERCHANT_ACCOUNT}/payouts?limit=5" | \
  jq -r '.data[] | "\(.pspReference) | Amount: \(.amount.value/100) \(.amount.currency) | Status: \(.status) | Date: \(.createdAt)"' 2>/dev/null || echo "Use settlement reports for payout data"
```

## Output Format

```
ADYEN STATUS
============
Company: {name} | Merchant: {account}
Payment Methods: {count} active
Authorization Rate (7d): {percent}%
Terminals: {online}/{total} online
Webhooks: {active}/{total} active
Risk Rules: {enabled}/{total} enabled
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

- **Environment URLs**: Test vs live use different subdomains — never mix credentials
- **API versioning**: Adyen uses version numbers in paths (v71) — check for latest
- **Merchant vs Company**: Company is top-level; merchant accounts are per-business-unit
- **PCI compliance**: Never log full card numbers — Adyen handles PCI scope
