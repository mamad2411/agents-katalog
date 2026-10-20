---
name: analytics-cloudflare
description: Cloudflare GraphQL Analytics for zone traffic, firewall events, Workers metrics, and schema exploration. Use when querying Cloudflare analytics data or exploring the GraphQL API.
connection_type: cloudflare
preload: false
---

# Analytics Cloudflare

## Discovery

<critical>
**If no `[cached_from_skill:analytics-cloudflare:discover]` context exists, run discovery first:**
```bash
bun run ./_skills/connections/cloudflare/analytics-cloudflare/scripts/discover.ts
bun run ./_skills/connections/cloudflare/analytics-cloudflare/scripts/discover.ts --max-zones 5
bun run ./_skills/connections/cloudflare/analytics-cloudflare/scripts/discover.ts --zone example.com
```
Output is auto-cached.
</critical>

**What discovery provides:**
- `accounts`: List of Cloudflare accounts with `id`, `name`
- `zones`: Zone details with `id`, `name`, `status`, `accountId`, `accountName`, `plan`
- `dataRetention`: Retention windows by data type (DNS, HTTP, firewall, workers) based on plan tier
- `availableDatasets`: GraphQL datasets with `name`, `scope` (account/zone), `variableType` (Date!/Time!), `retention`
- `queryHints`:
  - `criticalRequirement`: Must call `graphql_zones_list()` before DNS queries
  - `correctWorkflow`: Step-by-step workflow for queries
  - `variableTypes`: Which datasets use `Date!` vs `Time!`
  - `scopeRequirements`: Which datasets are account-level vs zone-level
  - `safeDateRanges`: Pre-calculated safe date ranges based on retention

**Why run discovery:**
- Get `accountId` required for DNS/Workers queries
- Get `zoneId` required for HTTP/Firewall queries
- Know data retention limits (7-62 days depending on plan)
- Understand correct variable types (Date! vs Time!)
- Avoid 0-record results from incorrect scope or context

**Output Formatting:**

Use `format()` for token-efficient output (40-60% token savings):

```typescript
import { format } from "@connections/_utils/format";

console.log(format(result));  // CORRECT - Uses TOON encoding
// console.log(JSON.stringify(result, null, 2));  // WRONG - Wastes tokens
```

---

## Critical Rules

🚨 **MUST call `graphql_zones_list({ name: 'domain.com' })` BEFORE querying DNS analytics**
- Required to establish zone context
- Hardcoded account IDs → returns 0 records
- Without zone context → returns 0 records

🚨 **CRITICAL: `graphql_graphql_query` Response Handling**

The `graphql_graphql_query` tool returns a **STRING** containing:
1. JSON response data
2. A markdown link to GraphQL Explorer (appended after `\n\n`)

Example response format:
```
{"data":{...},"errors":null}

**[Open in GraphQL Explorer](https://graphql.cloudflare.com/explorer?query=...)**
```

**MANDATORY parsing pattern:**

```typescript
// ✅ CORRECT - Extract JSON before parsing
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];  // Remove markdown link
const parsed = JSON.parse(jsonPart);

// ❌ WRONG - Parsing full string fails with "Unrecognized token '*'"
const parsed = JSON.parse(result as string);  // Error!
```

**Always check for GraphQL errors before accessing data:**

```typescript
if (parsed.errors && parsed.errors.length > 0) {
  console.error('GraphQL Errors:', format(parsed.errors));
  process.exit(1);
}

const data = parsed.data?.viewer?.accounts?.[0]?.dnsAnalyticsAdaptiveGroups || [];
```

**Format requirements:**
- DNS: `Date!` format (`"2026-01-27"`)
- HTTP/Firewall/Workers: `Time!` format (`"2026-01-27T00:00:00Z"`)

**Scope requirements:**
- DNS & Workers: Account-level (`viewer.accounts`)
- HTTP & Firewall: Zone-level (`viewer.zones`)

**Retention (Free plan):**
- DNS: 7 days only
- HTTP: 31 days
- Firewall/Workers: 30 days

---

## Verified Working Example

```typescript
import { graphql_zones_list, graphql_graphql_query } from '@connections/cloudflare';
import { format } from '@connections/_utils/format';

async function queryDNS() {
  // Step 1: CRITICAL - Establish zone context
  const zonesResult = await graphql_zones_list({ name: 'cloudthinker.io' });
  const zones = typeof zonesResult === 'string' ? JSON.parse(zonesResult) : zonesResult;
  const accountId = zones.zones[0].account.id;

  // Step 2: Query with Date! format
  const query = `query($accountTag: string!, $start: Date!, $end: Date!) {
    viewer {
      accounts(filter: { accountTag: $accountTag }) {
        dnsAnalyticsAdaptiveGroups(
          filter: { date_geq: $start, date_leq: $end }
          limit: 1000
        ) {
          count
          dimensions { queryName queryType responseCode }
        }
      }
    }
  }`;

  const result = await graphql_graphql_query({
    query,
    variables: { accountTag: accountId, start: '2026-01-27', end: '2026-01-28' }
  });

  // Step 3: CRITICAL - Extract JSON before parsing (remove markdown link)
  const resultStr = result as string;
  const jsonPart = resultStr.split('\n\n')[0];
  const parsed = JSON.parse(jsonPart);

  // Step 4: Check for GraphQL errors
  if (parsed.errors && parsed.errors.length > 0) {
    console.error('GraphQL Errors:', format(parsed.errors));
    process.exit(1);
  }

  // Step 5: Access the data
  const dnsData = parsed.data?.viewer?.accounts?.[0]?.dnsAnalyticsAdaptiveGroups || [];

  if (dnsData.length === 0) {
    console.log('No DNS data available for the specified period');
    process.exit(0);
  }

  // Step 6: Display results with format() for token efficiency
  console.log(format(dnsData));
}

queryDNS();
```

---

## Query Templates

### DNS Analytics (Account-Level)

```typescript
// MUST establish zone context first
const zonesResult = await graphql_zones_list({ name: 'example.com' });
const zones = typeof zonesResult === 'string' ? JSON.parse(zonesResult) : zonesResult;
const accountTag = zones.zones[0].account.id;

const result = await graphql_graphql_query({
  query: `query($accountTag: string!, $start: Date!, $end: Date!) {
    viewer { accounts(filter: { accountTag: $accountTag }) {
      dnsAnalyticsAdaptiveGroups(
        filter: { date_geq: $start, date_leq: $end }
        limit: 1000
      ) {
        count
        dimensions { queryName queryType responseCode zoneName }
      }
    }}
  }`,
  variables: {
    accountTag,
    start: '2026-01-27',  // Date! format, within 7 days
    end: '2026-01-28'
  }
});

// CRITICAL: Extract JSON before parsing
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];
const parsed = JSON.parse(jsonPart);

if (parsed.errors) {
  console.error('Errors:', format(parsed.errors));
  process.exit(1);
}

const dnsData = parsed.data?.viewer?.accounts?.[0]?.dnsAnalyticsAdaptiveGroups || [];
```

### HTTP Traffic (Zone-Level)

```typescript
const zonesResult = await graphql_zones_list({});
const zones = typeof zonesResult === 'string' ? JSON.parse(zonesResult) : zonesResult;
const zoneTag = zones.zones.find(z => z.name === 'example.com')?.id;

const result = await graphql_graphql_query({
  query: `query($zoneTag: string!, $start: Time!, $end: Time!) {
    viewer { zones(filter: { zoneTag: $zoneTag }) {
      httpRequests1hGroups(
        filter: { datetime_geq: $start, datetime_lt: $end }
        limit: 24
      ) {
        dimensions { datetime }
        sum { requests bytes cachedRequests }
      }
    }}
  }`,
  variables: {
    zoneTag,
    start: '2026-01-10T00:00:00Z',  // Time! format
    end: '2026-01-11T00:00:00Z'
  }
});

// CRITICAL: Extract JSON before parsing
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];
const parsed = JSON.parse(jsonPart);

if (parsed.errors) {
  console.error('Errors:', format(parsed.errors));
  process.exit(1);
}

const httpData = parsed.data?.viewer?.zones?.[0]?.httpRequests1hGroups || [];
```

### Firewall Events (Zone-Level)

```typescript
const result = await graphql_graphql_query({
  query: `query($zoneTag: string!, $start: Time!, $end: Time!) {
    viewer { zones(filter: { zoneTag: $zoneTag }) {
      firewallEventsAdaptive(
        filter: { datetime_geq: $start, datetime_leq: $end }
        limit: 100
      ) {
        action clientCountryName clientIP clientRequestPath datetime
      }
    }}
  }`,
  variables: { zoneTag, start, end }
});

// CRITICAL: Extract JSON before parsing
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];
const parsed = JSON.parse(jsonPart);

if (parsed.errors) {
  console.error('Errors:', format(parsed.errors));
  process.exit(1);
}

const firewallEvents = parsed.data?.viewer?.zones?.[0]?.firewallEventsAdaptive || [];
```

### Workers Analytics (Account-Level)

```typescript
const zonesResult = await graphql_zones_list({});
const zones = typeof zonesResult === 'string' ? JSON.parse(zonesResult) : zonesResult;
const accountTag = zones.zones[0].account.id;

const result = await graphql_graphql_query({
  query: `query($accountTag: string!, $scriptName: string!, $start: Time!, $end: Time!) {
    viewer { accounts(filter: { accountTag: $accountTag }) {
      workersInvocationsAdaptive(
        filter: { scriptName: $scriptName, datetime_geq: $start }
        limit: 100
      ) {
        dimensions { datetime scriptName status }
        sum { requests errors }
      }
    }}
  }`,
  variables: { accountTag, scriptName, start, end }
});

// CRITICAL: Extract JSON before parsing
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];
const parsed = JSON.parse(jsonPart);

if (parsed.errors) {
  console.error('Errors:', format(parsed.errors));
  process.exit(1);
}

const workersData = parsed.data?.viewer?.accounts?.[0]?.workersInvocationsAdaptive || [];
```

---

## Common Workflows

### Check DNS queries
1. Filter zone: `graphql_zones_list({ name: 'example.com' })`
2. Parse result: `JSON.parse(zonesResult)`
3. Extract account ID: `zones.zones[0].account.id`
4. Query DNS with Date! format
5. **Parse response**: `JSON.parse(result.split('\n\n')[0])`
6. Check errors, then access data

### Check zone traffic
1. Get zone ID: `graphql_zones_list({})`
2. Parse result: `JSON.parse(zonesResult)`
3. Query HTTP with Time! format
4. **Parse response**: `JSON.parse(result.split('\n\n')[0])`
5. Access: `parsed.data.viewer.zones[0].httpRequests1hGroups`

### Find blocked requests
1. Get zone ID: `graphql_zones_list({})`
2. Parse result: `JSON.parse(zonesResult)`
3. Query firewall events
4. **Parse response**: `JSON.parse(result.split('\n\n')[0])`
5. Filter by `action: "block"`

---

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `JSON Parse error: Unrecognized token '*'` | Markdown link in response | Use `result.split('\n\n')[0]` before parsing |
| DNS returns 0 records | No zone context | MUST call `graphql_zones_list({ name: 'domain.com' })` first |
| Type mismatch | Wrong variable type | DNS=`Date!`, others=`Time!` |
| HTTP returns 0 records | Wrong type or old dates | Use `Time!` + dates within 31 days |
| `Cannot read property 'data' of undefined` | Didn't parse response | Always `JSON.parse(result.split('\n\n')[0])` |

### Quick Diagnostic

**DNS returns 0 records?**
1. 🚨 Did you call `graphql_zones_list({ name: 'domain.com' })` FIRST?
   - ❌ Hardcoded account ID → 0 records
   - ❌ `graphql_zones_list({})` without name → may return 0 records
   - ✅ MUST filter zone by name to establish context
2. Using `Date!` format (not `Time!`)?
3. Dates within 7-day retention window?
4. Using `viewer.accounts` (not `viewer.zones`)?

**Still returns 0 records with correct workflow?**
- Free/Pro plan API limitation (expected behavior)
- Dashboard shows data (uses internal APIs)
- Public GraphQL API has limited exposure on lower tiers
- Upgrade to Business/Enterprise for full API access

---

## Reference

### Available Datasets

| Dataset | Scope | Var Type | Retention (Free) |
|---------|-------|----------|------------------|
| `dnsAnalyticsAdaptiveGroups` | Account | `Date!` | 7 days |
| `httpRequests1hGroups` | Zone | `Time!` | 31 days |
| `firewallEventsAdaptive` | Zone | `Time!` | 30 days |
| `workersInvocationsAdaptive` | Account | `Time!` | 30 days |

### Filter Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `_eq` | `action_eq: "block"` | Equals |
| `_geq`, `_gte` | `datetime_geq: $start` | Greater than or equal |
| `_leq`, `_lte` | `datetime_leq: $end` | Less than or equal |
| `_in` | `action_in: ["block", "challenge"]` | In list |

---

## Response Handling Best Practices

### The Complete Pattern

Every `graphql_graphql_query` call MUST follow this pattern:

```typescript
import { graphql_graphql_query } from '@connections/cloudflare';
import { format } from '@connections/_utils/format';

try {
  const result = await graphql_graphql_query({ query, variables });

  // Step 1: Extract JSON portion (remove markdown link)
  const resultStr = result as string;
  const jsonPart = resultStr.split('\n\n')[0];

  // Step 2: Parse JSON
  const parsed = JSON.parse(jsonPart);

  // Step 3: Check for GraphQL errors
  if (parsed.errors && parsed.errors.length > 0) {
    console.error('GraphQL Errors:');
    console.error(format(parsed.errors));
    process.exit(1);
  }

  // Step 4: Access data with fallback
  const data = parsed.data?.viewer?.accounts?.[0]?.dnsAnalyticsAdaptiveGroups || [];

  // Step 5: Handle empty results
  if (data.length === 0) {
    console.log('No data available for the specified period');
    console.log('Note: Check date range, retention limits, and plan tier');
    process.exit(0);
  }

  // Step 6: Display results with format() for token efficiency
  console.log(format(data));

} catch (error) {
  console.error('Query execution failed:', error);
  process.exit(1);
}
```

### Why This Pattern Is Mandatory

1. **String Response**: Tool returns string, not object
2. **Markdown Appended**: `\n\n**[Open in GraphQL Explorer](...)**` breaks JSON.parse
3. **GraphQL Errors**: Can have `errors` array even with 200 status
4. **Empty Results**: Valid response but no data (common with wrong context/dates)
5. **Token Efficiency**: Use `format()` instead of `JSON.stringify()`

### Quick Reference

```typescript
// ✅ CORRECT
const resultStr = result as string;
const jsonPart = resultStr.split('\n\n')[0];
const parsed = JSON.parse(jsonPart);

// ❌ WRONG - Will fail with "Unrecognized token '*'"
const parsed = JSON.parse(result as string);

// ❌ WRONG - Assumes object response
const data = result.data?.viewer?.accounts;

// ✅ CORRECT - Check errors before accessing data
if (parsed.errors) {
  console.error('Errors:', format(parsed.errors));
  process.exit(1);
}

// ✅ CORRECT - Use format() for output
console.log(format(data));

// ❌ WRONG - Wastes tokens
console.log(JSON.stringify(data, null, 2));
```

## Output Format

Present results as a structured report:
```
Analytics Cloudflare Report
═══════════════════════════
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

