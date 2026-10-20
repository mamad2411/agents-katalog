---
name: vercel-performance
description: "Investigate slow routes using available measurements and logs. Use for measured deployment latency/cache problems; react-rerenders handles client render cost."
---

# vercel-performance

Investigate slow routes using available measurements and logs.

## Choose this workflow

Use for measured deployment latency/cache problems; react-rerenders handles client render cost.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; slow routes, deployment, workload, and existing measurements.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Server response, cold starts, caching, payloads, and relevant client delivery behavior.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Correlate timing with runtime and cache state, and compare like-for-like requests with matching regions, payloads and cache states.
2. Separate cold start, warm handler, dependency, network and browser timing, and rank optimizations by evidence.

## Technical method

- **Inspect:** Obtain equivalent revision/region/payload samples, cache status and cold/warm conditions.
- **Method:** Attribute latency to network, application, data access and cache; optimize the measured dominant stage.
- **Avoid misdiagnosis:** Comparing a cold miss before with a warm hit after does not demonstrate an improvement.
- **Check the result:** Repeat matched conditions, retain error rates and tail latency, and verify cache changes do not mix users or stale personalized content.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).


## Decision branches

- **When a fast sample is cached and a slow sample is uncached:** Report separate distributions and investigate cache eligibility before claiming compute regression.

## Deliver and verify

- Measurement conditions and distributions, the limiting boundary, and a bounded optimization plan or experiment.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Cache hits and misses are compared separately; a single slow sample does not become a universal latency claim.

## Stop and recover

- Load generation belongs to test-load, and new remote profiling needs a resolved target and budget. No automatic paid plan upgrade or unrelated application rewrite.

## Example requests

- **Normal (inspect):** Analyze these route timings; distinguish cached responses from cold execution.
- **Edge (inspect):** Compare slow preview requests with cached production responses fairly.
- **Blocked (inspect):** Assess supplied timing samples without load testing or changing the paid plan.
