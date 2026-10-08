---
name: managing-posthog
description: |
  Use when working with Posthog — postHog analytics management — monitor events,
  feature flags, experiments, session recordings, and ingestion health. Use when
  reviewing event volumes, managing feature flags, debugging tracking, or
  inspecting experiment results.
connection_type: posthog
preload: false
---

# Managing PostHog

Manage and monitor PostHog product analytics — events, feature flags, experiments, and session recordings.

## Discovery Phase

```bash
#!/bin/bash

POSTHOG_API="${POSTHOG_HOST:-https://app.posthog.com}/api"
AUTH="Authorization: Bearer $POSTHOG_API_KEY"

echo "=== Project Info ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current" \
  | jq '{id: .id, name: .name, timezone: .timezone, completed_snippet_onboarding: .completed_snippet_onboarding}'

echo ""
echo "=== Event Definitions ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/event_definitions?limit=20" \
  | jq -r '.results[] | [.name, .volume_30_day // 0, .query_usage_30_day // 0] | @tsv' | column -t

echo ""
echo "=== Feature Flags ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/feature_flags?limit=15" \
  | jq -r '.results[] | [.id, .key, .active, .rollout_percentage // "filters"] | @tsv' | column -t

echo ""
echo "=== Experiments ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/experiments?limit=10" \
  | jq -r '.results[] | [.id, .name, .start_date, .end_date // "running"] | @tsv' | column -t
```

## Analysis Phase

```bash
#!/bin/bash

POSTHOG_API="${POSTHOG_HOST:-https://app.posthog.com}/api"
AUTH="Authorization: Bearer $POSTHOG_API_KEY"

echo "=== Event Volume (Last 7 Days) ==="
curl -s -H "$AUTH" -X POST "$POSTHOG_API/projects/@current/insights/trend/" \
  -H "Content-Type: application/json" \
  -d '{"events":[{"id":"$pageview","type":"events"}],"date_from":"-7d","interval":"day"}' \
  | jq -r '.result[0].data | to_entries[] | [.key, .value] | @tsv' | column -t

echo ""
echo "=== Top Events by Volume ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/event_definitions?limit=10&ordering=-volume_30_day" \
  | jq -r '.results[] | [.name, .volume_30_day] | @tsv' | column -t

echo ""
echo "=== Feature Flag Usage ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/feature_flags?active=true&limit=10" \
  | jq -r '.results[] | [.key, .active, .rollout_percentage // "complex", .ensure_experience_continuity] | @tsv' | column -t

echo ""
echo "=== Session Recordings Stats ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/session_recordings?limit=5&date_from=-1d" \
  | jq '{total_count: .count, recordings: [.results[:5][] | {id: .id, duration: .recording_duration, activity: .activity_score}]}'

echo ""
echo "=== Ingestion Warnings ==="
curl -s -H "$AUTH" "$POSTHOG_API/projects/@current/ingestion_warnings?limit=10" \
  | jq -r '.results[:10][] | [.type, .count, .last_seen] | @tsv' | column -t
```

## Output Format

```
PROJECT
Name:       <project-name>
Timezone:   <timezone>

TOP EVENTS (30d)
Event Name           Volume
<event-name>         <count>

FEATURE FLAGS
Key              Active  Rollout
<flag-key>       true    <percentage>

EXPERIMENTS
Name             Start        End
<exp-name>       <date>       <date|running>

INGESTION WARNINGS
Type             Count    Last Seen
<warning-type>   <n>      <timestamp>
```

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

