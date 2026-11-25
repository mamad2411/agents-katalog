---
name: api-endpoint-probe
group: domain
triggers:
  - "как работает эндпоинт"
  - "проверь API"
  - "интеграция с новым API"
output: "API parameter map: filters, pagination, auth requirements"
calls: []
---

# Skill: API Endpoint Probe

**Purpose:** Quick reconnaissance of API endpoint parameters before implementation — find what actually works (filters, pagination, limits, auth) via minimal test requests.
**When:** Integrating with a new endpoint where unknown: which params it accepts, pagination type, whether it works without mandatory filters, actual response limit.
**Output:** Table of "works / doesn't work" + recommended call pattern for implementation.

---

## PROCESS

### Step 1 — Collect initial data

Ask user (if not in request):
1. URL or endpoint template (e.g. `GET /v1/trades?market={id}`)
2. Is there auth — API key, Bearer token, cookie?
3. Goal: paginate all records / filter / one-time fetch?
4. Known params from docs? (even partial)

### Step 2 — Build probe plan

Form minimal set of 3–5 test requests:

| # | Goal | Params | Expected result |
|---|------|--------|-----------------|
| 1 | Base call, no filters | — | Does it work at all, response format |
| 2 | Page limit | `limit=1` / `size=1` | Whether param exists, what it's called |
| 3 | Cursor pagination | `cursor=` / `next=` / `after=` | Pagination type |
| 4 | Time-based filter | `startTs=` / `after=` / `since=` | Whether timestamp filter works |
| 5 | Entity filter | `market=X` / `user=Y` | Is filter required or optional |

Show plan to user — wait for "да" before executing.

### Step 3 — Execute probe requests

For each request in plan:
1. Show exact request before executing
2. Execute via `requests` (Python) or `curl` — depending on environment
3. Record: status, response size, key fields

```python
# Python probe template
import requests, json

BASE = "https://api.example.com"
HEADERS = {"Authorization": "Bearer TOKEN"}  # if auth needed

def probe(path, params=None):
    r = requests.get(BASE + path, headers=HEADERS, params=params)
    print(f"{r.status_code} | {len(r.content)}b | {path}?{r.request.path_url.split('?',1)[-1]}")
    try:
        data = r.json()
        if isinstance(data, list) and data:
            print(json.dumps(data[0], indent=2)[:300])
        elif isinstance(data, dict):
            print(json.dumps({k: type(v).__name__ for k, v in data.items()}))
    except:
        print(r.text[:200])
    return r
```

### Step 4 — Record results

After all requests, output summary table:

```
── Probe results: [endpoint] ────────────────────────

| Parameter       | Works? | How to use                  |
|-----------------|--------|-----------------------------|
| no filters      | ✅/❌  | [observation]               |
| limit/size      | ✅/❌  | limit=N or size=N           |
| cursor paging   | ✅/❌  | next_cursor field in response|
| startTs filter  | ✅/❌  | startTs=unix_ms             |
| user filter     | ✅/❌  | required / optional         |

Recommended call for implementation:
  GET [path]?[param1=val]&[param2=val]
  Pagination: [cursor / offset / timestamp / none]
  Limit: [actual page limit]
  Notes: [what doesn't work or is unexpected]
```

### Step 5 — Update documentation

If project has `CLAUDE.md`:
- Add findings to "Known Issues" or a separate "API Notes" section
- Note confirmed pagination type — to avoid re-checking

---

## RULES

- No more than 10 requests without explicit user consent
- Don't use mutating methods (POST/DELETE) without explicit instruction
- If endpoint returns 401/403 — report immediately, don't guess auth
- If param is undocumented but works — mark as "undocumented, verify in next API version"
