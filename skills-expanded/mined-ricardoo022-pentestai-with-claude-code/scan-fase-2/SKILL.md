---
name: scan-fase-2
description: Execute FASE 2 - Adaptive Schema Discovery. Extracts database schema, table structures, field types, and relationships using REST, GraphQL, and reverse engineering techniques. Identifies hidden tables, shadow APIs, and data models. Adapts to any backend type. Invoke with /scan-fase-2 {url}.
---

# FASE 2: Adaptive Schema Discovery

Deep schema extraction phase that maps the complete data model of the application. Goes beyond documented APIs to discover hidden tables, fields, and relationships.

## Core Principle

**DISCOVER THE COMPLETE DATA MODEL**

The checklist items (2.1-2.3) are MINIMUM requirements. The agent MUST:
- Extract schema from ALL available sources (REST, GraphQL, error messages, JS bundles)
- Identify hidden/internal tables not exposed via public API
- Map relationships between tables (foreign keys, joins)
- Discover field types, constraints, and validation rules
- Find shadow APIs and undocumented endpoints

**CRITICAL: The patterns in `references/` are STARTING POINTS, not limits.**

When you find something unexpected:
1. **Extract it** - any schema information is valuable
2. **Map relationships** - connect discoveries to known tables
3. **Infer from errors** - error messages reveal structure
4. **Cross-reference** - JS bundles often reveal hidden schema

## Invocation

```
/scan-fase-2 {url}
```

**Requires:** FASE 0 completed (backend type known), FASE 1 completed (configs extracted)

## Output

Structured results for the scan-write skill:

```yaml
FASE_2_RESULTS:
  target_url: {url}
  scan_timestamp: "{ISO 8601}"
  backend_type: {from FASE 0}
  status: "{completed|partial|blocked}"
  status_reason: "{if partial/blocked, explain why}"

  tables_discovered:
    - name: {table_name}
      source: {rest|graphql|error|js_bundle|inference}
      fields:
        - name: {field_name}
          type: {data_type}
          nullable: {yes|no|unknown}
          constraints: [unique, foreign_key, etc.]
      rls_status: {enabled|disabled|unknown}
      row_count_estimate: {number or unknown}

  relationships:
    - from_table: {table}
      from_field: {field}
      to_table: {table}
      to_field: {field}
      type: {one-to-one|one-to-many|many-to-many}
      source: {how discovered}

  graphql_schema:
    types_count: {number}
    queries: [list]
    mutations: [list]
    subscriptions: [list]
    custom_scalars: [list]

  hidden_discoveries:
    - type: {hidden_table|shadow_api|undocumented_field|internal_endpoint}
      name: {identifier}
      evidence: {how found}
      risk: {critical|high|medium|low}

  api_endpoints:
    - path: {endpoint}
      method: {GET|POST|PUT|DELETE|PATCH}
      parameters: [list]
      returns: {data_type}
      auth_required: {yes|no|unknown}

  schema_artifacts:
    - type: {openapi|swagger|graphql_sdl|prisma|drizzle|other}
      location: {where found}
      content_summary: {brief description}

  vulnerabilities_found:
    - id: "VULN-2-{seq}"
      type: "{schema_exposed|introspection_enabled|sensitive_fields_exposed|...}"
      title: "{short title}"
      severity: "{CRITICAL|HIGH|MEDIUM|LOW|INFO}"
      description: "{what was found}"
      impact: "{what attacker can do}"
      poc:
        command: "{curl command or method used}"
        response: "{relevant response excerpt}"
        notes: "{additional context}"
      affected:
        - resource: "{table|endpoint|field|...}"
          detail: "{specific detail}"

  secure_findings:
    - test: "{what was tested}"
      result: "SECURE"
      evidence: "{proof of security}"

  tests_skipped:
    - test: "{test name}"
      reason: "{why skipped}"
      recommendation: "{how to enable or alternative approach}"

  additional_findings: [anything else discovered]
```

---

## Execution Methodology

### Phase 2.1: REST API Schema Discovery

**Start with standard REST introspection:**

```bash
# Supabase REST introspection
curl -s "https://{project}.supabase.co/rest/v1/" \
  -H "apikey: {anon_key}" | jq '.definitions | keys'

# Check OpenAPI/Swagger endpoints
curl -s "https://{domain}/openapi.json"
curl -s "https://{domain}/swagger.json"
curl -s "https://{domain}/api-docs"
curl -s "https://{domain}/docs"
curl -s "https://{domain}/.well-known/openapi.json"
```

**Extract table information:**

```javascript
// For Supabase - get detailed schema
mcp__playwright__browser_evaluate({
  function: `async () => {
    const response = await fetch('{supabase_url}/rest/v1/', {
      headers: { 'apikey': '{anon_key}' }
    });
    return response.json();
  }`
})
```

### Phase 2.2: GraphQL Schema Discovery

**Full introspection query:**

```graphql
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args { ...InputValue }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args { ...InputValue }
    type { ...TypeRef }
    isDeprecated
    deprecationReason
  }
  inputFields { ...InputValue }
  interfaces { ...TypeRef }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes { ...TypeRef }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType { kind name }
      }
    }
  }
}
```

```bash
# Execute introspection
curl -s -X POST "https://{project}.supabase.co/graphql/v1" \
  -H "apikey: {anon_key}" \
  -H "Content-Type: application/json" \
  -d '{"query": "{introspection_query}"}'
```

**Per-type field discovery:**

```graphql
{
  __type(name: "{table_name}") {
    name
    fields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
```

### Phase 2.3: Error-Based Schema Discovery

**Provoke errors to reveal schema:**

```bash
# Invalid field error reveals valid fields
curl -s "https://{project}.supabase.co/rest/v1/{table}?select=nonexistent_field" \
  -H "apikey: {anon_key}"

# Response often includes: "Could not find field 'nonexistent_field' in table '{table}'. Valid fields are: id, name, email, ..."

# Invalid table error reveals valid tables
curl -s "https://{project}.supabase.co/rest/v1/nonexistent_table" \
  -H "apikey: {anon_key}"

# Type mismatch reveals field types
curl -s "https://{project}.supabase.co/rest/v1/{table}?id=eq.not_a_number" \
  -H "apikey: {anon_key}"
# Error: "invalid input syntax for type uuid" → field is UUID
```

**GraphQL error mining:**

```graphql
# Query with typos to trigger helpful errors
{
  profles { id }  # Typo: "profles" instead of "profiles"
}
# Error: "Did you mean 'profiles'?"

# Request non-existent field
{
  profiles { nonexistent_field }
}
# Error: "Field 'nonexistent_field' not found on type 'profiles'. Available fields: id, name, email, created_at"
```

### Phase 2.4: Source Map Exploitation

**Source maps expose complete original source with type definitions:**

```bash
# Check for source maps
SOURCE_MAP_PATHS=(
  "/_next/static/chunks/main.js.map"
  "/_next/static/chunks/pages/_app.js.map"
  "/static/js/main.*.js.map"
  "/assets/index-*.js.map"
)

for path in "${SOURCE_MAP_PATHS[@]}"; do
  map_url="${domain}${path}"
  response=$(curl -s -w "%{http_code}" -o /tmp/sourcemap.json "$map_url")
  if [ "$(echo "$response" | tail -1)" = "200" ]; then
    echo "SOURCE MAP FOUND: ${path}"

    # Extract original file names
    jq -r '.sources[]' /tmp/sourcemap.json | grep -E '(schema|model|type|interface|prisma|drizzle)'

    # Extract TypeScript interfaces from sourcesContent
    jq -r '.sourcesContent[]' /tmp/sourcemap.json 2>/dev/null | \
      grep -E '(interface|type|model)\s+\w+\s*\{' | head -50
  fi
done
```

```javascript
// Check for inline source maps in bundles
mcp__playwright__browser_evaluate({
  function: `() => {
    const scripts = Array.from(document.querySelectorAll('script[src]'));
    const inlineMapPatterns = [];

    for (const script of scripts) {
      // Will need to fetch and check each bundle
      inlineMapPatterns.push({
        src: script.src,
        mapUrl: script.src + '.map'
      });
    }

    return inlineMapPatterns;
  }`
})
```

**Source map findings to extract:**
- Complete TypeScript interfaces
- Prisma/Drizzle schema definitions
- Original variable names before minification
- Comments with TODO/FIXME containing secrets

### Phase 2.5: Browser State Inspection

**Modern apps cache schema in client state:**

```javascript
mcp__playwright__browser_evaluate({
  function: `async () => {
    const state = {};

    // Next.js __NEXT_DATA__
    const nextData = document.getElementById('__NEXT_DATA__');
    if (nextData) {
      try {
        state.__NEXT_DATA__ = JSON.parse(nextData.textContent);
      } catch {}
    }

    // Apollo Client cache
    if (window.__APOLLO_STATE__) {
      state.apolloCache = window.__APOLLO_STATE__;
    }
    if (window.__APOLLO_CLIENT__) {
      try {
        state.apolloExtract = window.__APOLLO_CLIENT__.cache.extract();
      } catch {}
    }

    // React Query state
    if (window.__REACT_QUERY_STATE__) {
      state.reactQuery = window.__REACT_QUERY_STATE__;
    }

    // Relay store
    if (window.__RELAY_STORE__) {
      state.relayStore = window.__RELAY_STORE__;
    }

    // URQL data
    if (window.__URQL_DATA__) {
      state.urqlData = window.__URQL_DATA__;
    }

    // Redux/Zustand stores
    if (window.__REDUX_DEVTOOLS_EXTENSION__) {
      state.hasRedux = true;
    }

    // LocalStorage keys (schema hints)
    state.localStorageKeys = Object.keys(localStorage);
    for (const key of state.localStorageKeys) {
      if (key.includes('supabase') || key.includes('schema') || key.includes('types')) {
        try {
          state['localStorage_' + key] = JSON.parse(localStorage.getItem(key));
        } catch {
          state['localStorage_' + key] = localStorage.getItem(key);
        }
      }
    }

    // IndexedDB databases
    if (indexedDB.databases) {
      try {
        const dbs = await indexedDB.databases();
        state.indexedDB = dbs.map(db => ({ name: db.name, version: db.version }));
      } catch {}
    }

    return state;
  }`
})
```

**What to extract from browser state:**
- `__NEXT_DATA__.props` - Server-rendered data structures
- Apollo cache - Complete type definitions
- localStorage - Supabase type cache
- IndexedDB - Offline-first app schemas

### Phase 2.6: JS Bundle Schema Extraction

**ORM/Schema definitions in code:**

```javascript
// Search for Prisma schema patterns
const prismaPatterns = [
  /model\s+(\w+)\s*\{([^}]+)\}/g,  // model User { ... }
  /@@map\("(\w+)"\)/g,              // table name mapping
];

// Search for Drizzle schema patterns
const drizzlePatterns = [
  /pgTable\s*\(\s*['"](\w+)['"]/g,  // pgTable('users', ...)
  /serial\s*\(\s*['"](\w+)['"]/g,   // serial('id')
  /varchar\s*\(\s*['"](\w+)['"]/g,  // varchar('name')
];

// Search for TypeORM/Sequelize patterns
const ormPatterns = [
  /@Entity\s*\(\s*['"]?(\w+)['"]?\)/g,
  /@Column\s*\([^)]*\)/g,
  /tableName:\s*['"](\w+)['"]/g,
];

// Search for Supabase type definitions
const supabasePatterns = [
  /Database\s*=\s*\{/,
  /Tables:\s*\{/,
  /Row:\s*\{/,
];

// Search for Validation Library patterns (CRITICAL for schema)
const zodPatterns = [
  /z\.object\s*\(\s*\{([^}]+)\}/g,           // z.object({ ... })
  /z\.(string|number|boolean|date|array|enum)\s*\(/g,
  /\.parse\s*\(|\.safeParse\s*\(/g,
];

const yupPatterns = [
  /yup\.object\s*\(\s*\)\.shape\s*\(\s*\{([^}]+)\}/g,
  /yup\.(string|number|boolean|date|array)\s*\(/g,
];

const joiPatterns = [
  /Joi\.object\s*\(\s*\{([^}]+)\}/g,
  /Joi\.(string|number|boolean|date|array)\s*\(/g,
];

// Search for tRPC patterns (reveals full API schema)
const trpcPatterns = [
  /createTRPCRouter\s*\(\s*\{/g,
  /t\.router\s*\(\s*\{/g,
  /\.input\s*\(\s*z\./g,                      // Input validation
  /\.output\s*\(\s*z\./g,                     // Output type
  /publicProcedure|protectedProcedure/g,
];

// Form library patterns (reveal expected data)
const formPatterns = [
  /useForm\s*\(\s*\{/g,                       // React Hook Form
  /register\s*\(\s*['"](\w+)['"]/g,           // Field names
  /<Formik\s+initialValues\s*=\s*\{/g,        // Formik
  /<Field\s+name\s*=\s*['"](\w+)['"]/g,
];

// Table component patterns (reveal data schema)
const tablePatterns = [
  /columnHelper\.accessor\s*\(\s*['"](\w+)['"]/g,
  /accessorKey:\s*['"](\w+)['"]/g,
  /createColumnHelper<(\w+)>/g,
];
```

```bash
# Download and search bundles for all patterns
curl -s "{bundle_url}" | grep -oE '(model|pgTable|@Entity|tableName)\s*[:(]\s*["\x27]?\w+["\x27]?'

# Zod validation schemas
curl -s "{bundle_url}" | grep -oE 'z\.(object|string|number|boolean|array|enum)\s*\('

# tRPC routers
curl -s "{bundle_url}" | grep -oE '(createTRPCRouter|publicProcedure|protectedProcedure)'

# React Hook Form fields
curl -s "{bundle_url}" | grep -oE 'register\s*\(\s*["\x27]\w+["\x27]'
```

### Phase 2.5: Response Analysis & Inference

**Analyze API responses to infer schema:**

```javascript
function inferSchema(response) {
  const schema = {};

  function analyzeValue(key, value) {
    if (value === null) return { type: 'unknown', nullable: true };

    switch (typeof value) {
      case 'string':
        // Detect specific types by format
        if (/^\d{4}-\d{2}-\d{2}/.test(value)) return { type: 'timestamp' };
        if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value)) return { type: 'uuid' };
        if (/^[\w.-]+@[\w.-]+\.\w+$/.test(value)) return { type: 'email' };
        if (/^https?:\/\//.test(value)) return { type: 'url' };
        return { type: 'text' };
      case 'number':
        return Number.isInteger(value) ? { type: 'integer' } : { type: 'decimal' };
      case 'boolean':
        return { type: 'boolean' };
      case 'object':
        if (Array.isArray(value)) return { type: 'array', items: analyzeValue(key, value[0]) };
        return { type: 'jsonb', properties: inferSchema(value) };
      default:
        return { type: 'unknown' };
    }
  }

  for (const [key, value] of Object.entries(response)) {
    schema[key] = analyzeValue(key, value);
  }

  return schema;
}
```

### Phase 2.6: Relationship Discovery

**Identify foreign key relationships:**

```javascript
// Naming convention analysis
const fkPatterns = [
  /(\w+)_id$/,      // user_id → users table
  /(\w+)Id$/,       // userId → users table (camelCase)
  /^fk_(\w+)/,      // fk_user → users table
  /(\w+)_uuid$/,    // user_uuid → users table
];

// Cross-reference with discovered tables
function findRelationships(tables, fields) {
  const relationships = [];

  for (const field of fields) {
    for (const pattern of fkPatterns) {
      const match = field.name.match(pattern);
      if (match) {
        const targetTable = match[1] + 's'; // Simple pluralization
        if (tables.includes(targetTable)) {
          relationships.push({
            from_field: field.name,
            to_table: targetTable,
            type: 'many-to-one'
          });
        }
      }
    }
  }

  return relationships;
}
```

**GraphQL relationship discovery:**

```graphql
# Look for nested types that indicate relationships
{
  __type(name: "profiles") {
    fields {
      name
      type {
        name
        kind
        ofType {
          name
          kind
        }
      }
    }
  }
}

# Fields returning another type = relationship
# Example: "orders" field returning "[Order]" = one-to-many
```

### Phase 2.7: Hidden Table Discovery

**Discover tables not in public schema:**

```bash
# Try common table name patterns
COMMON_TABLES=(
  "users" "profiles" "accounts" "members" "customers" "admins"
  "posts" "comments" "articles" "messages" "notifications"
  "orders" "payments" "subscriptions" "invoices" "transactions"
  "products" "items" "categories" "tags"
  "files" "uploads" "documents" "attachments" "media"
  "settings" "configs" "preferences" "options"
  "logs" "audit_logs" "activity_logs" "events"
  "sessions" "tokens" "api_keys" "refresh_tokens"
  "roles" "permissions" "user_roles" "role_permissions"
  "teams" "organizations" "workspaces" "projects"
  "forms" "form_responses" "submissions" "surveys"
  "_prisma_migrations" "_drizzle_migrations" "schema_migrations"
)

for table in "${COMMON_TABLES[@]}"; do
  response=$(curl -s -w "\n%{http_code}" "https://{project}.supabase.co/rest/v1/${table}?limit=1" \
    -H "apikey: {anon_key}")

  http_code=$(echo "$response" | tail -1)

  # 200 = table exists and accessible
  # 401/403 = table exists but protected
  # 404 = table doesn't exist

  if [ "$http_code" != "404" ]; then
    echo "FOUND: $table (HTTP $http_code)"
  fi
done
```

**GraphQL type enumeration:**

```graphql
# Get ALL types including internal ones
{
  __schema {
    types {
      name
      kind
      description
    }
  }
}

# Filter for table-like types (not built-in)
# Types starting with __ are internal GraphQL types
# Types like "String", "Int", "Boolean" are scalars
# Remaining OBJECT types are likely tables
```

---

## Adaptive Discovery Rules

**The agent MUST go beyond the checklist when it discovers:**

1. **Unexpected tables** → Enumerate all fields and relationships
2. **Schema artifacts in bundles** → Extract complete definitions
3. **Verbose error messages** → Mine for field names and types
4. **Internal/admin endpoints** → Document for later testing
5. **Soft-deleted data patterns** → Note `deleted_at`, `is_deleted` fields
6. **Audit fields** → Note `created_at`, `updated_at`, `created_by` patterns
7. **Multi-tenant patterns** → Note `tenant_id`, `organization_id` fields
8. **Polymorphic patterns** → Note `type`, `kind`, `discriminator` fields
9. **Version fields** → Note `version`, `revision` for optimistic locking
10. **Metadata fields** → Note `metadata`, `extra`, `attributes` JSONB fields

### Schema Inference from Response Patterns

When API documentation is unavailable, infer schema from responses:

```javascript
// Analyze multiple responses to build confident schema
function buildSchemaFromSamples(samples) {
  const fieldStats = {};

  for (const sample of samples) {
    for (const [field, value] of Object.entries(sample)) {
      if (!fieldStats[field]) {
        fieldStats[field] = { types: {}, nullCount: 0, totalCount: 0 };
      }

      fieldStats[field].totalCount++;

      if (value === null) {
        fieldStats[field].nullCount++;
      } else {
        const type = inferType(value);
        fieldStats[field].types[type] = (fieldStats[field].types[type] || 0) + 1;
      }
    }
  }

  // Build final schema with confidence
  const schema = {};
  for (const [field, stats] of Object.entries(fieldStats)) {
    const primaryType = Object.entries(stats.types)
      .sort((a, b) => b[1] - a[1])[0];

    schema[field] = {
      type: primaryType ? primaryType[0] : 'unknown',
      nullable: stats.nullCount > 0,
      confidence: primaryType ? primaryType[1] / stats.totalCount : 0
    };
  }

  return schema;
}
```

### Unknown API Discovery

When you encounter undocumented endpoints:

```yaml
unknown_apis:
  - endpoint: "/api/internal/metrics"
    method: GET
    discovered_via: "JS bundle fetch() call"
    response_sample: {...}
    inferred_purpose: "Internal monitoring endpoint"
    auth_status: "Returns 401 without token"
    risk: "medium"
    recommendation: "Test with authenticated token in FASE 14"
```

---

## Backend-Specific Techniques

### Supabase

```bash
# PostgREST returns OpenAPI spec
curl -s "https://{project}.supabase.co/rest/v1/" -H "apikey: {key}" | jq '.paths | keys'

# pg_catalog queries via RPC (if exposed)
# This would be CRITICAL if accessible
curl -X POST "https://{project}.supabase.co/rest/v1/rpc/get_tables" -H "apikey: {key}"
```

### Firebase/Firestore

```bash
# Firestore collections are not enumerable by default
# Must infer from app behavior and JS bundles

# Look for collection references in code
grep -oE "collection\(['\"](\w+)['\"]\)" bundle.js
grep -oE "doc\(['\"](\w+)/['\"]" bundle.js
```

### Custom REST APIs

```bash
# Try common documentation endpoints
curl -s "https://{api}/swagger.json"
curl -s "https://{api}/openapi.json"
curl -s "https://{api}/api-docs"
curl -s "https://{api}/docs"
curl -s "https://{api}/schema"
curl -s "https://{api}/_schema"
```

### Hasura

```bash
# Hasura metadata endpoint (if exposed)
curl -X POST "https://{hasura}/v1/metadata" \
  -H "Content-Type: application/json" \
  -d '{"type": "export_metadata", "args": {}}'

# Full introspection always available unless disabled
curl -X POST "https://{hasura}/v1/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{__schema{types{name fields{name}}}}"}'
```

---

## Unknown Schema Discovery Heuristics

**When you find schema elements NOT in the patterns, use these heuristics:**

### Heuristic 1: Table Name Analysis

Infer table purpose from naming conventions:

```javascript
const tableNamePatterns = {
  // User data
  userData: /^(users?|profiles?|accounts?|members?|customers?|people)$/i,

  // Transactions
  transactions: /^(orders?|payments?|invoices?|transactions?|purchases?)$/i,

  // Content
  content: /^(posts?|articles?|comments?|messages?|notifications?)$/i,

  // Files
  files: /^(files?|uploads?|documents?|attachments?|media)$/i,

  // Auth/Permissions
  auth: /^(roles?|permissions?|sessions?|tokens?|api_keys?)$/i,

  // Junction tables (many-to-many)
  junction: /^(\w+)_(\w+)$|^(\w+)_to_(\w+)$/i,

  // Audit/Logs
  audit: /^(logs?|audit_logs?|activity|events?|history)$/i,

  // Config
  config: /^(settings?|configs?|preferences?|options?)$/i,

  // Internal
  internal: /^(_|__|\$|sys_|pg_|information_schema)/i,
};

function inferTablePurpose(tableName) {
  for (const [purpose, pattern] of Object.entries(tableNamePatterns)) {
    if (pattern.test(tableName)) return purpose;
  }
  return 'unknown';
}
```

### Heuristic 2: Field Type Inference from Values

When type is unknown, infer from sample values:

```javascript
function inferFieldType(sampleValue) {
  if (sampleValue === null) return { type: 'unknown', nullable: true };

  // UUID
  if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(sampleValue)) {
    return { type: 'uuid', likely_pk_or_fk: true };
  }

  // Timestamp
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(sampleValue)) {
    return { type: 'timestamp' };
  }

  // Email
  if (/^[\w.-]+@[\w.-]+\.\w+$/.test(sampleValue)) {
    return { type: 'text', format: 'email' };
  }

  // URL
  if (/^https?:\/\//.test(sampleValue)) {
    return { type: 'text', format: 'url' };
  }

  // JSON object
  if (typeof sampleValue === 'object' && !Array.isArray(sampleValue)) {
    return { type: 'jsonb', nested_schema: Object.keys(sampleValue) };
  }

  // Array
  if (Array.isArray(sampleValue)) {
    return { type: 'array', element_type: inferFieldType(sampleValue[0])?.type };
  }

  // Boolean
  if (typeof sampleValue === 'boolean') return { type: 'boolean' };

  // Number
  if (typeof sampleValue === 'number') {
    return Number.isInteger(sampleValue) ? { type: 'integer' } : { type: 'numeric' };
  }

  // Default text
  return { type: 'text' };
}
```

### Heuristic 3: Relationship Inference

Detect relationships from field naming:

```javascript
function inferRelationship(fieldName, knownTables) {
  // Pattern: {table}_id or {table}Id
  const fkMatch = fieldName.match(/^(\w+?)_?[Ii]d$/);
  if (fkMatch) {
    const possibleTable = fkMatch[1];
    // Try plural forms
    const candidates = [
      possibleTable,
      possibleTable + 's',
      possibleTable + 'es',
      possibleTable.replace(/y$/, 'ies')
    ];

    for (const candidate of candidates) {
      if (knownTables.includes(candidate)) {
        return {
          type: 'foreign_key',
          references_table: candidate,
          relationship: 'many-to-one'
        };
      }
    }

    // Table not found but likely FK
    return {
      type: 'likely_foreign_key',
      probable_table: possibleTable,
      note: 'Referenced table not discovered yet'
    };
  }

  return null;
}
```

### Heuristic 4: Hidden Table Detection

When a table returns 401/403 instead of 404:

```javascript
async function probeHiddenTables(baseUrl, apiKey, tableNames) {
  const results = { exists: [], hidden: [], notFound: [] };

  for (const table of tableNames) {
    const response = await fetch(`${baseUrl}/rest/v1/${table}?limit=1`, {
      headers: { 'apikey': apiKey }
    });

    switch (response.status) {
      case 200:
        results.exists.push({ table, accessible: true });
        break;
      case 401:
      case 403:
        // Table EXISTS but access denied
        results.hidden.push({
          table,
          accessible: false,
          status: response.status,
          note: 'Table exists but requires different auth level'
        });
        break;
      case 404:
        results.notFound.push(table);
        break;
      default:
        results.exists.push({ table, accessible: 'unknown', status: response.status });
    }
  }

  return results;
}
```

### Heuristic 5: Schema from Error Messages

Extract schema info from verbose errors:

```javascript
function parseSchemaFromError(errorMessage) {
  const discoveries = [];

  // PostgreSQL: column "X" does not exist
  const colMatch = errorMessage.match(/column "(\w+)" does not exist/i);
  if (colMatch) {
    discoveries.push({ type: 'invalid_column', name: colMatch[1] });
  }

  // PostgreSQL: relation "X" does not exist
  const relMatch = errorMessage.match(/relation "(\w+)" does not exist/i);
  if (relMatch) {
    discoveries.push({ type: 'invalid_table', name: relMatch[1] });
  }

  // PostgREST: valid columns are X, Y, Z
  const validColsMatch = errorMessage.match(/valid columns are[:\s]+([^.]+)/i);
  if (validColsMatch) {
    const columns = validColsMatch[1].split(/[,\s]+/).filter(Boolean);
    discoveries.push({ type: 'valid_columns', columns });
  }

  // Type mismatch: invalid input syntax for type X
  const typeMatch = errorMessage.match(/invalid input syntax for type (\w+)/i);
  if (typeMatch) {
    discoveries.push({ type: 'field_type', dataType: typeMatch[1] });
  }

  // GraphQL: Did you mean X?
  const suggestMatch = errorMessage.match(/Did you mean ['"]?(\w+)['"]?/i);
  if (suggestMatch) {
    discoveries.push({ type: 'suggestion', name: suggestMatch[1] });
  }

  return discoveries;
}
```

### Heuristic 6: Unknown API Endpoint Analysis

When you find an endpoint not matching known patterns:

```javascript
function analyzeUnknownEndpoint(path, response) {
  const analysis = {
    path,
    type: 'unknown',
    schema_hints: []
  };

  // Check if it returns array (collection) or object (single resource)
  if (Array.isArray(response)) {
    analysis.type = 'collection';
    if (response.length > 0) {
      analysis.schema_hints = Object.keys(response[0]);
    }
  } else if (typeof response === 'object' && response !== null) {
    analysis.type = 'resource';
    analysis.schema_hints = Object.keys(response);
  }

  // Infer from path structure
  if (/\/v\d+\//.test(path)) {
    analysis.versioned = true;
  }
  if (/\/:?\w+Id|\/:\w+/.test(path)) {
    analysis.parameterized = true;
  }

  return analysis;
}
```

### Decision Tree for Unknown Schema Elements

```
Found unknown table/field/endpoint?
│
├─ Is it a TABLE?
│   ├─ Returns 200 → Extract all fields, infer types
│   ├─ Returns 401/403 → Mark as HIDDEN, exists but protected
│   ├─ Returns 404 → Does not exist via this API
│   └─ Returns error with schema info → Parse error for hints
│
├─ Is it a FIELD?
│   ├─ Has sample value → Infer type from value
│   ├─ Name ends in _id → Likely foreign key
│   ├─ Name matches known patterns → Classify accordingly
│   └─ Unknown → Document with type 'unknown'
│
├─ Is it an ENDPOINT?
│   ├─ Returns collection → Treat as table equivalent
│   ├─ Returns object → Single resource endpoint
│   ├─ Returns error → Parse for schema hints
│   └─ Returns nothing → Mark as discovered, needs auth?
│
└─ Still unsure?
    └─ Document in additional_findings with:
        - What was found
        - Where it was found
        - Sample values if any
        - Your hypothesis
```

### Output for Unknown Discoveries

```yaml
unknown_discoveries:
  - type: {table|field|endpoint|relationship}
    name: {identifier}
    source: {where_found}
    sample_value: {if available}
    inferred_type: {your inference}
    inferred_purpose: {your hypothesis}
    confidence: {high|medium|low}
    needs_further_testing: {yes|no}
```

---

## Discovery Priority

When multiple tables/endpoints are found, prioritize extraction:

| Discovery Type | Priority | Reason |
|----------------|----------|--------|
| Tables with user data (profiles, users, accounts) | HIGH | Core data model |
| Tables with transactions (orders, payments) | HIGH | Business-critical |
| Admin/internal tables | HIGH | Often hidden |
| Junction tables (*_roles, *_permissions) | MEDIUM | Reveal relationships |
| Audit/log tables | MEDIUM | Historical data |
| Migration tables | LOW | Schema evolution |
| Config/settings tables | LOW | Application config |

---

## Error Handling

**If introspection is disabled:**
```yaml
FASE_2_RESULTS:
  status: partial
  note: "GraphQL introspection disabled - using alternative methods"
  methods_used:
    - error_mining
    - js_bundle_analysis
    - response_inference
  recommendation: "Schema partially discovered via alternative techniques"
```

**If all schema discovery fails:**
```yaml
FASE_2_RESULTS:
  status: minimal
  note: "Schema discovery limited - strict API configuration"
  tables_discovered: []
  recommendation: "Proceed to FASE 3 with table names from FASE 1 JS bundle analysis"
```

---

## References

- `references/schema-extraction-techniques.md` - Advanced extraction methods
- `references/api-fingerprinting.md` - API type identification patterns
- FASE 0 results - Backend type and base configs
- FASE 1 results - Extracted configs and endpoints from JS bundles

---

## After Completion

After executing FASE 2, provide the YAML results and call `/scan-write`:

```
/scan-write {client_name} --fase 2
```

This logs the schema discovery results to SCAN-IN-PROGRESS.md.
