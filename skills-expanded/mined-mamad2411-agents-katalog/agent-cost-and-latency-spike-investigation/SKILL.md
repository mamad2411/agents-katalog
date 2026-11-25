---
name: agent-cost-and-latency-spike-investigation
description: >
  Guides rapidly triaging a sudden cost or latency spike affecting one
  specific agent workflow — scoping it, correlating it against recent
  changes, and applying a fast, safe stopgap — before launching a full
  optimization pass. Use when a user asks "why did our LLM bill jump
  overnight," "this one workflow got slow/expensive all of a sudden,"
  "investigate a cost/latency spike," or reports an alert/invoice surprise
  for a single agent or task type, as distinct from a deliberate,
  scheduled effort to reduce baseline cost or latency.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Agent Cost and Latency Spike Investigation

## Purpose

A sudden cost or latency spike in one agent workflow is an incident, not an
optimization project — the goal in the first hours is to scope it,
identify what changed, and stop the bleeding, not to redesign the pipeline.
[llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md)
covers the deliberate, scheduled work of reducing baseline cost/latency
across an agent (right-sizing models, caching, batching); this skill covers
the narrower, time-pressured question that comes first: *why did this one
workflow suddenly get more expensive or slower than it was yesterday*, and
what's the fastest safe action to take. Confusing the two wastes the
window where a quick rollback would have worked and instead launches a
multi-day optimization effort under incident pressure.

## When to use

- A cost dashboard or billing alert shows a step-change increase for one
  agent/workflow/task type, not a gradual trend.
- p50/p95 latency for one specific workflow doubles (or worse) compared to
  its recent baseline, while other workflows are unaffected.
- An unexpected line item appears on an LLM provider invoice tied to a
  specific agent.
- Before scheduling a full cost/latency optimization pass — this
  investigation determines whether there's an active regression to fix
  first, so the optimization pass starts from a correct baseline.
- Deciding whether a spike is a regression (something broke) or legitimate
  growth (more users, more traffic) — these require entirely different
  responses.

## Prerequisites & environment

- Per-call token usage and latency logging, segmented by workflow/task
  type (not just a single aggregate metric) — if the spike can't be
  isolated to one workflow because everything rolls into one dashboard
  number, segmenting the metrics is itself the first prerequisite to fix.
- A deploy/change log with timestamps: prompt edits, tool schema changes,
  model version or provider changes, retrieval index re-indexing runs,
  and infrastructure/routing changes — the single most useful artifact
  for this investigation is a timeline that can be laid next to the
  metrics timeline.
- Request volume metrics alongside cost/latency, so a spike in absolute
  cost can be distinguished from a spike in cost-per-request.
- Access to a recent-history transcript sample for the affected workflow
  (see
  [agent-bad-response-triage-and-root-cause-classification](../agent-bad-response-triage-and-root-cause-classification/SKILL.md)
  for full-transcript capture practices) so the investigation isn't
  limited to aggregate numbers alone.

## Step-by-step guidance

1. **Scope the blast radius first: one workflow, or everything?** If cost
   or latency moved across *all* workflows and all providers
   simultaneously, this is more likely a provider-wide event (outage,
   pricing change, regional latency issue) than a workflow-specific
   regression — that's the domain of
   [llm-gateway-and-multi-provider-routing](../llm-gateway-and-multi-provider-routing/SKILL.md)
   (check provider status, confirm fallback routing triggered correctly)
   rather than this skill. Confirm the spike is actually isolated to one
   workflow before proceeding with a workflow-specific investigation.

2. **Pull time series for four signals side by side, not cost alone**:
   request volume, tokens per request (input and output separately),
   tool-call count per request, and latency p50/p95. Overlay all four
   against the deploy/change timeline from day one.

   ```
   metric               yesterday   today      delta
   requests/hour        1,180       1,205      flat (+2%)
   avg input tokens/req    2,400      2,410      flat
   avg output tokens/req     310      1,850      +497%  <-- signal
   avg tool calls/req        2.1        2.1      flat
   p95 latency (ms)        1,850      6,200      +235%
   ```

   A table like this immediately narrows the search: flat volume and flat
   input tokens with a jump in output tokens and latency points at a
   generation-side change (prompt, output-format drift, or a model
   change), not a traffic or context-bloat problem.

3. **Apply the decision tree once the shape of the change is visible:**
   - **Volume up, per-request metrics flat** → legitimate traffic growth,
     not a regression; this is a capacity/budget conversation, not an
     incident.
   - **Volume flat, tokens-per-request up** → likely context bloat
     (uncontrolled history growth, duplicated retrieved chunks) or a
     prompt/tool-description change — see
     [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md).
   - **Volume flat, tool-call count per request up** → likely a stalled or
     looping agent — see
     [agent-tool-call-loop-diagnosis-and-circuit-breaking](../agent-tool-call-loop-diagnosis-and-circuit-breaking/SKILL.md).
   - **Latency up, tokens flat** → likely a provider-side latency change,
     a model/region switch, or a downstream tool/dependency slowdown — see
     [llm-gateway-and-multi-provider-routing](../llm-gateway-and-multi-provider-routing/SKILL.md).
   - **Cost up, tokens flat** → likely a pricing change, a model routing
     change (silently routed to a pricier model/tier), or a provider
     billing anomaly — verify against the routing config and provider
     invoice line items directly.
   - **RAG-backed workflow, retrieval-stage metrics implicated** → check
     whether a recent re-indexing job changed chunk count/size or
     duplicated content — see
     [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md)
     and
     [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
     for query-side cost/latency levers (over-retrieval, `ef_search`
     misconfiguration).

4. **Correlate against the change log directly**, not just by shape of the
   metrics. Pull every prompt edit, tool schema change, model version bump,
   and re-indexing run within the window the spike started, ordered by
   timestamp — the metrics tell you *what kind* of change to look for, the
   change log tells you *which specific change* it was.

5. **Sample actual transcripts from the spike window**, not just
   aggregates — three or four real requests showing exactly where the
   extra tokens or latency landed (a much longer generated answer, an
   extra retrieved chunk, a retried tool call) turn a statistical
   correlation into a confirmed cause.

6. **Quantify blast radius before deciding urgency**: is this an ongoing,
   accumulating cost (every request now costs more) or a one-time event
   (a single bad batch job)? An ongoing per-request regression justifies
   an immediate stopgap even before full root-cause is confirmed; a
   one-time event mostly needs a retrospective, not urgent action.

7. **Apply the fastest safe stopgap, correlated to the identified change —
   usually a rollback, not a redesign.** If a specific prompt edit, model
   version bump, or config change correlates cleanly with the spike's
   start time, reverting that specific change is almost always faster and
   safer than attempting a fix forward under time pressure.

   > **Warning:** A stopgap fix applied directly to production without a
   > tested rollback path (e.g. hand-editing a live prompt or routing
   > config with no previous version saved) risks replacing one incident
   > with another. Roll back to the last known-good, versioned
   > configuration rather than improvising a new one under pressure — see
   > [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
   > for why an unvalidated forward-fix is riskier than a clean rollback.

8. **Hand off to the deliberate optimization pass once contained.** Once
   the spike is stopped and root-caused, if the investigation also
   surfaces general inefficiency (not just the regression that caused the
   spike — e.g. "we've never right-sized the model for this step"), that
   becomes a scheduled task for
   [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md),
   not something to solve inside this incident.

9. **Add a per-workflow cost/latency regression alert** (not just an
   aggregate account-level billing alert) so the next spike in this
   specific workflow pages before a month-end invoice surprises anyone —
   thresholds should be relative to that workflow's own recent baseline,
   not a single global number.

## Best practices

- Segment cost and latency dashboards by workflow/task type from the
  start; an aggregate-only dashboard dilutes a severe single-workflow
  spike into an unremarkable overall trend.
- Prefer a clean rollback to the last known-good configuration over a
  forward fix improvised during the incident — validate any forward fix
  against the eval suite before it replaces the rollback as the permanent
  solution.
- Always check the four signals (volume, tokens, tool-call count, latency)
  together — cost and latency spikes frequently share a root cause but not
  always the same one, and treating them as one signal hides the
  distinction.
- Sample real transcripts, not just aggregate metrics, before closing out
  the investigation — a statistical correlation with the change log is
  strong evidence but a confirmed transcript is proof.
- Keep a running timeline of prompt/tool/model/index changes with
  timestamps as a standing artifact, not something reconstructed from
  memory during each incident.
- Distinguish "legitimate traffic growth" from "regression" early and
  explicitly — treating growth as an incident wastes urgency budget, and
  treating a regression as growth delays the fix.

## Common pitfalls

- **Symptom:** The team immediately schedules a full model/architecture
  optimization review in response to a sudden spike, before checking
  whether a single recent change (a prompt edit, a model version bump)
  is the actual, fixable cause.
  **Fix:** Run this fast triage first — correlate against the change log
  and roll back the specific change if one correlates cleanly — before
  committing to a multi-day optimization effort that the eval suite and
  metrics may show was unnecessary.

- **Symptom:** The investigation concludes "the model provider must have
  changed something" with no supporting evidence, because it's easier to
  blame an external, unverifiable cause than to check the team's own
  recent deploys.
  **Fix:** Check the internal change log (prompt, tool, model version,
  index) first — most spikes correlate with an internal change; only
  escalate to a suspected provider-side cause after internal causes are
  actively ruled out, and verify against the provider's own status page
  or release notes rather than assuming.

- **Symptom:** An aggregate, account-wide cost dashboard shows only a
  minor overall uptick, masking a severe spike in one specific low-volume
  but now much more expensive workflow.
  **Fix:** Segment cost and latency metrics by workflow/task type as a
  standing practice, not only when an incident is already suspected —
  aggregate-only monitoring structurally cannot catch this class of spike
  early.

- **Symptom:** A quick prompt or routing-config edit is pushed directly to
  production to stop the spike, with the previous version not saved
  anywhere, and a subsequent issue traced to that same hotfix has no clean
  rollback target.
  **Fix:** Always roll back to a previously versioned, known-good
  configuration rather than hand-editing production under pressure; treat
  configuration (prompts, routing rules, model pins) as version-controlled
  artifacts specifically so this rollback path always exists.

- **Symptom:** The spike is correctly root-caused and fixed, but no
  workflow-specific alert is added, so an unrelated regression in the same
  workflow six weeks later isn't caught until the next invoice cycle.
  **Fix:** Add a per-workflow cost/latency regression alert with a
  threshold relative to that workflow's own recent baseline as a mandatory
  last step of every spike investigation, not an optional follow-up.

## Worked example

**Scenario:** The `contract-summarizer` agent's average cost per request
jumps from roughly $0.04 to $0.31 overnight, with total request volume
essentially unchanged; the on-call engineer is asked to investigate before
anyone commits to a redesign.

1. **Scope:** Cost dashboards for two other agents sharing the same model
   provider show no change — confirmed isolated to `contract-summarizer`,
   ruling out a provider-wide event.
2. **Signal table:**
   ```
   metric                yesterday   today     delta
   requests/hour              340        335    flat
   avg input tokens/req      6,100      6,050    flat
   avg output tokens/req       420      3,900    +828%
   avg tool calls/req            0          0    flat
   p95 latency (ms)          2,100      9,700    +362%
   ```
   Flat volume and input tokens, output tokens and latency both up sharply
   → generation-side change, not traffic or retrieval.
3. **Change log correlation:** a prompt edit merged the previous evening
   changed the summarization instruction from "produce a 3-5 sentence
   summary" to "produce a comprehensive summary covering all material
   terms," removing the previous length constraint entirely.
4. **Transcript sample:** three sampled requests confirm outputs went from
   ~5-sentence summaries to multi-page summaries restating most of the
   input contract.
5. **Blast radius:** ongoing and accumulating — every request since the
   prompt merge costs roughly 7x more, not a one-time event, so an
   immediate stopgap is justified.
6. **Stopgap:** the prompt is rolled back to the previous versioned
   revision (length constraint restored) rather than hand-editing a new
   instruction under pressure; cost per request returns to baseline within
   the hour.
7. **Follow-up:** the intent behind the original edit (some users wanted
   more comprehensive summaries for complex contracts) is handed to
   [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md)
   and [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md)
   as a deliberate follow-up: an explicit, length-bounded "detailed mode"
   evaluated against the eval suite for both quality and cost before
   shipping, rather than an unbounded prompt change pushed directly to
   everyone.
8. A per-workflow alert is added: page if `contract-summarizer` avg output
   tokens/request exceeds 2x its 7-day rolling baseline.

## Cross-references

- [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md) — the deliberate optimization pass this investigation feeds into once the active spike is contained.
- [agent-tool-call-loop-diagnosis-and-circuit-breaking](../agent-tool-call-loop-diagnosis-and-circuit-breaking/SKILL.md) — a common root cause when tool-call count per request is the signal that moved.
- [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md) — diagnosing and fixing a context-bloat or prompt-change root cause.
- [llm-gateway-and-multi-provider-routing](../llm-gateway-and-multi-provider-routing/SKILL.md) — when the spike is provider- or routing-correlated rather than workflow-specific.
- [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md) — when a re-indexing run correlates with a RAG-backed workflow's spike.
- [agent-bad-response-triage-and-root-cause-classification](../agent-bad-response-triage-and-root-cause-classification/SKILL.md) — the parallel triage process when the symptom is a bad response rather than cost/latency.
