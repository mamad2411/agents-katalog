---
name: wp-runtime-profiling
description: Profiles WordPress PHP runtime, hooks, load stages, memory, external calls, and component attribution using approved tools and production-safe evidence.
---

# WordPress runtime profiling

Use this skill when baseline evidence points to server-side execution or when component attribution is required.

## Tool choices

Use [profiling-tool-decision-matrix.md](resources/profiling-tool-decision-matrix.md) before selecting a tool.

Possible tools include:

- Query Monitor for request-level WordPress evidence;
- `wp profile` for WordPress load stages and hooks;
- XHProf-compatible profiling for call graphs;
- Server-Timing for controlled server-side benchmarks;
- host/APM traces when authorized.

## Rules

- Profiling adds overhead; do not use profiler timings as neutral end-user benchmarks.
- Keep request, data, cache, and authentication state explicit.
- Attribute time to hooks, callbacks, queries, HTTP calls, templates, or components with evidence.
- Redact query parameters, headers, payloads, paths, and stack data where needed.
- Run [profile-wordpress-runtime-workflow.md](workflows/profile-wordpress-runtime-workflow.md).
