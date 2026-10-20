---
name: volcano-logs
description: Use for Volcano project logs, retained log search, log pagination, activity buckets, structured log filters, and server-side log readers using project access tokens.
---
# Volcano Logs Skill

## Role and pairing

Use this skill when application or operator code reads retained project logs or
activity counts through an SDK. Pair it with `volcano-sdk` and
`volcano-platform`.

CLI log commands for one deployed function belong to `volcano-functions` or
`volcano-durable`. This skill covers the SDK project-log facade.

Use the project's language:

| Project signal | SDK behavior |
|---|---|
| `package.json`, `.ts`, `.js` | JavaScript/TypeScript result envelopes |
| `pyproject.toml`, `requirements.txt`, `.py` | Python values and typed exceptions |
| `Gemfile`, `.gemspec`, `.rb` | Ruby values and typed exceptions |

## Credentials

Logs require a platform token or project access token. A `read_only` project
access token is sufficient. Keep it in server code. End-user sessions, anon
keys, and service keys do not grant project log access.

```ts
import { VolcanoClient } from '@volcano.dev/sdk';

const client = new VolcanoClient({
  anonKey: process.env.VOLCANO_ANON_KEY,
  apiUrl: process.env.VOLCANO_API_URL,
  accessToken: process.env.VOLCANO_PROJECT_ACCESS_TOKEN,
});
```

Python uses `VolcanoClient(anon_key=..., access_token=...)`. Ruby uses
`Volcano::Client.new(anon_key: ..., access_token: ...)`. Supply the same project
access token and API URL in each language.

## Search retained logs

### JavaScript and TypeScript

```ts
const request = {
  resource: { type: 'function' as const },
  q: 'level:(warn OR error) body:checkout_failed',
  limit: 100,
};

const { data: page, error } = await client.logs.search(projectId, request);
if (error) throw error;
if (!page) throw new Error('Log search returned no page');
for (const event of page.data) console.log(event.timestamp, event.body);
```

### Python

```python
request = {
    "resource": {"type": "function"},
    "q": "level:(warn OR error) body:checkout_failed",
    "limit": 100,
}
page = client.logs.search(project_id, request)
for event in page.data:
    print(event["timestamp"], event["body"])
```

### Ruby

```ruby
request = {
  resource: { type: "function" },
  q: "level:(warn OR error) body:checkout_failed",
  limit: 100
}
page = client.logs.search(project_id, request)
page.data.each { |event| puts [event["timestamp"], event["body"]] }
```

Python and Ruby raise typed SDK exceptions on request or response failures. Use
`resource.ids` to select resources. Use RFC3339 `start_time` and `end_time` for
a bounded range. Log bodies can be JSON values, not only strings.

## Pagination

```ts
if (page.has_more && page.next_cursor) {
  const { data: next, error } = await client.logs.search(projectId, {
    ...request,
    cursor: page.next_cursor,
  });
  if (error) throw error;
  if (!next) throw new Error('Log search returned no page');
}
```

Keep the resource selector, query, and time bounds unchanged when continuing a
search. Treat the cursor as opaque.

## Activity buckets

```ts
const { data: activity, error } = await client.logs.activity(projectId, {
  resource: request.resource,
  q: request.q,
  bucket_count: 24,
});
if (error) throw error;
if (!activity) throw new Error('Log activity returned no data');
console.log(activity.total, activity.data);
```

Activity groups counts by level, region, and resource ID. Logs arrive
asynchronously, so use bounded polling when a check waits for a new event.

## Safety

- Never put a project token in browser code.
- Do not call auth sign-out to revoke a project token.
- Do not change filters while reusing a cursor.
- Bound polling and log reads.
- Do not assume `body` is a string.

## Verification

- Search with a `read_only` project token.
- Confirm the resource and query filters exclude unrelated events.
- Continue one page with `next_cursor` when present.
- Confirm activity bucket totals sum to the response total.
