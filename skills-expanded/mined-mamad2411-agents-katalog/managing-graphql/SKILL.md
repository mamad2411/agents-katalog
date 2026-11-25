---
name: managing-graphql
description: |
  Use when working with Graphql — graphQL API management - schema introspection,
  query complexity analysis, resolver performance monitoring, and subscription
  management. Use when analyzing GraphQL schemas, optimizing query performance,
  monitoring resolver bottlenecks, or managing real-time subscriptions.
connection_type: graphql
preload: false
---

# GraphQL Management Skill

Analyze and manage GraphQL APIs including schema introspection, query analysis, and performance monitoring.

## Core Helper Functions

```bash
#!/bin/bash

# GraphQL endpoint configuration
GRAPHQL_ENDPOINT="${GRAPHQL_ENDPOINT:-http://localhost:4000/graphql}"
GRAPHQL_HEADERS="${GRAPHQL_AUTH_HEADER:-}"

# GraphQL query executor
gql_query() {
    local query="$1"
    local variables="${2:-{}}"
    curl -s -X POST "$GRAPHQL_ENDPOINT" \
        -H "Content-Type: application/json" \
        ${GRAPHQL_HEADERS:+-H "$GRAPHQL_HEADERS"} \
        -d "{\"query\": $(echo "$query" | jq -Rs '.'), \"variables\": ${variables}}" | jq '.'
}

# Introspection query shorthand
gql_introspect() {
    gql_query '{ __schema { types { name kind description fields { name type { name kind ofType { name kind } } } } } }'
}
```

## MANDATORY: Discovery-First Pattern

**Always introspect the schema before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Schema Overview ==="
gql_query '{ __schema { queryType { name } mutationType { name } subscriptionType { name } directives { name description locations } } }' \
    | jq '{
        query_type: .data.__schema.queryType.name,
        mutation_type: .data.__schema.mutationType.name,
        subscription_type: (.data.__schema.subscriptionType.name // "none"),
        directives: [.data.__schema.directives[] | .name]
    }'

echo ""
echo "=== Type Summary ==="
gql_query '{ __schema { types { name kind } } }' \
    | jq '{
        total_types: (.data.__schema.types | length),
        by_kind: (.data.__schema.types | group_by(.kind) | map({kind: .[0].kind, count: length})),
        user_types: [.data.__schema.types[] | select(.name | startswith("__") | not) | .name] | sort
    }'

echo ""
echo "=== Root Query Fields ==="
gql_query '{ __type(name: "Query") { fields { name description type { name kind ofType { name kind } } args { name type { name kind } } } } }' \
    | jq '[.data.__type.fields[] | {name, args: [.args[] | .name], return_type: (.type.name // .type.ofType.name)}]'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Always filter introspection results; never dump the full schema
- Group fields by type or domain for readability

## Common Operations

### Schema Introspection and Analysis

```bash
#!/bin/bash

echo "=== Object Types with Fields ==="
gql_query '{ __schema { types { name kind description fields { name type { name kind ofType { name kind ofType { name } } } } } } }' \
    | jq '[.data.__schema.types[] | select(.kind == "OBJECT" and (.name | startswith("__") | not)) | {
        name,
        field_count: (.fields | length),
        fields: [.fields[] | {name, type: (.type.name // .type.ofType.name // (.type.ofType.ofType.name + "!"))}]
    }]'

echo ""
echo "=== Input Types ==="
gql_query '{ __schema { types { name kind inputFields { name type { name kind ofType { name } } } } } }' \
    | jq '[.data.__schema.types[] | select(.kind == "INPUT_OBJECT") | {name, fields: [.inputFields[] | .name]}]'

echo ""
echo "=== Enum Types ==="
gql_query '{ __schema { types { name kind enumValues { name description isDeprecated deprecationReason } } } }' \
    | jq '[.data.__schema.types[] | select(.kind == "ENUM" and (.name | startswith("__") | not)) | {name, values: [.enumValues[] | .name]}]'

echo ""
echo "=== Deprecated Fields ==="
gql_query '{ __schema { types { name fields { name isDeprecated deprecationReason } } } }' \
    | jq '[.data.__schema.types[] | select(.fields) | .fields[] | select(.isDeprecated) | {type: .name, field: .name, reason: .deprecationReason}]'
```

### Query Complexity Analysis

```bash
#!/bin/bash

echo "=== Mutation Fields ==="
gql_query '{ __type(name: "Mutation") { fields { name args { name type { name kind ofType { name } } } type { name kind ofType { name } } } } }' \
    | jq '[.data.__type.fields[] | {name, args: [.args[] | {name, type: (.type.name // .type.ofType.name)}], return_type: (.type.name // .type.ofType.name)}]'

echo ""
echo "=== Nested Type Depth Analysis ==="
gql_query '{ __schema { types { name kind fields { name type { name kind ofType { name kind ofType { name kind ofType { name } } } } } } } }' \
    | jq '[.data.__schema.types[] | select(.kind == "OBJECT" and (.name | startswith("__") | not)) | {
        name,
        nullable_fields: [.fields[] | select(.type.kind != "NON_NULL") | .name],
        list_fields: [.fields[] | select(.type.kind == "LIST" or (.type.ofType.kind? == "LIST")) | .name],
        object_refs: [.fields[] | select((.type.kind == "OBJECT") or (.type.ofType.kind? == "OBJECT")) | .name]
    }] | map(select(.object_refs | length > 0))'

echo ""
echo "=== Potential N+1 Query Patterns ==="
echo "Types with list fields returning objects (potential N+1 sources):"
gql_query '{ __schema { types { name kind fields { name type { name kind ofType { name kind ofType { name kind } } } } } } }' \
    | jq '[.data.__schema.types[] | select(.kind == "OBJECT" and (.name | startswith("__") | not)) | .fields[] | select(.type.kind == "LIST" or (.type.ofType.kind? == "LIST"))] | map(.name) | unique'
```

### Resolver Performance Monitoring

```bash
#!/bin/bash

echo "=== Apollo Studio / GraphQL Metrics (if available) ==="
echo "Check your GraphQL server's tracing extension for resolver-level metrics."

echo ""
echo "=== Test Query Latency ==="
for query_name in "simple_query" "nested_query" "list_query"; do
    start_time=$(date +%s%N)
    case $query_name in
        "simple_query") gql_query '{ __typename }' > /dev/null ;;
        "nested_query") gql_query '{ __schema { types { name } } }' > /dev/null ;;
        "list_query") gql_query '{ __schema { types { name fields { name } } } }' > /dev/null ;;
    esac
    end_time=$(date +%s%N)
    latency=$(( (end_time - start_time) / 1000000 ))
    echo "${query_name}: ${latency}ms"
done

echo ""
echo "=== Schema Size Metrics ==="
gql_query '{ __schema { types { name kind fields { name } } } }' \
    | jq '{
        total_types: (.data.__schema.types | length),
        total_fields: [.data.__schema.types[] | (.fields // []) | length] | add,
        avg_fields_per_type: ([.data.__schema.types[] | select(.fields) | (.fields | length)] | (add / length) | floor),
        largest_types: [.data.__schema.types[] | select(.fields) | {name, fields: (.fields | length)}] | sort_by(-.fields) | .[0:5]
    }'
```

### Subscription Management

```bash
#!/bin/bash

echo "=== Subscription Fields ==="
gql_query '{ __type(name: "Subscription") { fields { name description args { name type { name } } type { name kind ofType { name } } } } }' \
    | jq 'if .data.__type then [.data.__type.fields[] | {name, description, args: [.args[] | .name], return_type: (.type.name // .type.ofType.name)}] else "No Subscription type defined" end'

echo ""
echo "=== WebSocket Endpoint Check ==="
WS_ENDPOINT="${GRAPHQL_WS_ENDPOINT:-ws://localhost:4000/graphql}"
echo "WebSocket endpoint: ${WS_ENDPOINT}"
curl -s -o /dev/null -w "%{http_code}" \
    -H "Upgrade: websocket" \
    -H "Connection: Upgrade" \
    -H "Sec-WebSocket-Version: 13" \
    -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
    "${GRAPHQL_ENDPOINT}" && echo " (WebSocket upgrade supported)" || echo " (WebSocket not available)"
```

## Safety Rules
- **Read-only by default**: Only use introspection queries and read operations
- **Never execute** mutations without explicit user confirmation
- **Query depth limits**: Respect server-side depth limits; do not craft deeply nested queries
- **Rate limiting**: GraphQL servers may have query complexity limits; avoid expensive introspection in tight loops
- **No credential exposure**: Never include auth tokens or API keys in query output

## Output Format

Present results as a structured report:
```
Managing Graphql Report
═══════════════════════
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

## Common Pitfalls
- **Introspection disabled**: Production servers often disable introspection; use schema files instead
- **N+1 queries**: List fields returning objects can cause resolver-level N+1 problems; check DataLoader usage
- **Over-fetching**: Requesting all fields on large types wastes bandwidth; select only needed fields
- **Circular types**: Types referencing each other can cause infinite loops in code generators
- **Breaking changes**: Removing fields or types breaks existing clients; use deprecation workflow instead
