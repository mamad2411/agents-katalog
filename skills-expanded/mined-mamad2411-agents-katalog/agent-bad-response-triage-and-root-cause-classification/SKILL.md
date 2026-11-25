---
name: agent-bad-response-triage-and-root-cause-classification
description: >
  Guides triaging a single reported bad, wrong, or harmful agent response:
  reproducing it deterministically and classifying the root cause into one
  of five buckets — prompt issue, tool failure, retrieval issue, model
  behavior change, or genuine edge case — so the fix targets the actual
  cause instead of the symptom. Use when a user asks to "investigate this
  bad agent response," "why did the agent say/do that," "triage this
  reported hallucination/harmful output," "figure out if this is a prompt
  bug or a model regression," or files an incident about a single
  problematic agent interaction that needs root-causing before a fix ships.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Agent Bad Response Triage and Root Cause Classification

## Purpose

A single reported bad response — a wrong answer, a fabricated fact, an
unsafe or off-policy reply, an action that shouldn't have happened — looks
identical on the surface regardless of why it happened, but the fix is
completely different depending on the cause. Patching a prompt in response
to what was actually a tool timeout fixes nothing and adds prompt cruft;
rolling back a model version in response to what was actually a stale
retrieval index wastes an incident cycle and hides the real problem. This
skill is a triage runbook: reproduce the exact conditions that produced the
bad response, then work through a deliberate decision tree to classify the
root cause into one of five buckets — **prompt issue**, **tool failure**,
**retrieval issue**, **model behavior change**, or **genuine edge case** —
before deciding on a fix. It assumes an eval harness and guardrail layer
already exist (or should); this skill is what happens *between* "someone
reported a bad response" and "here's the regression case and the fix,"
which [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
covers on the prevention side.

## When to use

- A user, support ticket, or monitoring alert reports one specific bad,
  wrong, or harmful agent response and it needs root-causing before a fix
  is proposed.
- Deciding whether an observed failure is a one-off (genuine edge case) or
  a systemic issue (prompt, tool, retrieval, or model) that will recur.
- A stakeholder is pressuring for an immediate prompt patch and you need to
  first confirm the prompt is actually the cause.
- After a model provider version bump, a tool schema change, or a
  retrieval-index update, and a report comes in that might be linked to
  that change.
- Building or refining an incident-response runbook specifically for
  agent/LLM output issues, distinct from traditional application incidents.

## Prerequisites & environment

- Access to the full transcript of the reported interaction: every model
  call (system prompt, user input, prior turns), every tool call and its
  raw result, and the final output — not just the final answer shown to
  the user. If your agent doesn't log this today, treat "add full
  transcript logging" as a blocking prerequisite, not optional polish.
- The ability to reproduce a call with pinned inputs: the exact prompt
  version, tool-schema version, model version/identifier, and (for
  RAG-backed agents) the retrieval index snapshot or timestamp in effect
  at the time of the original response.
- A changelog of recent changes to the system: prompt edits, tool schema
  changes, model version bumps or provider-side model updates, and
  ingestion/re-indexing runs — with timestamps, so they can be correlated
  against when the bad response occurred.
- Access to the eval suite (see
  [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md))
  so a confirmed root cause can be turned into a permanent regression case.

## Step-by-step guidance

1. **Capture the report faithfully before touching anything.** Record the
   exact user input, timestamp, session/request ID, the full output shown,
   and precisely what was wrong about it (factually incorrect, unsafe,
   off-policy, unhelpful, took an unwanted action). Do this before
   attempting any fix or even a reproduction attempt — a report that gets
   paraphrased or summarized early loses the detail that root-causing
   depends on.

2. **Pull the full transcript for that request ID**, not just the final
   answer: every LLM call's input and output, every tool call's arguments
   and raw (untruncated) result, and, if retrieval was involved, exactly
   which chunks were retrieved and in what order. Most triage dead-ends
   happen because someone tries to root-cause from the final answer alone.

3. **Attempt a pinned reproduction.** Re-run the same input against the
   *exact* prompt version, tool-schema version, model version, and
   retrieval index snapshot that were live at the time of the original
   response (not today's versions). Three outcomes are possible, and each
   points the investigation differently:
   - **Reproduces identically** — the cause is deterministic given that
     exact configuration; proceed to the classification tree below.
   - **Reproduces only sometimes** — the model's inherent sampling
     variance is a factor; treat this as a signal to check prompt
     ambiguity and edge-case framing, not to conclude "the model is just
     random and unfixable."
   - **Does not reproduce at all** — check whether something changed
     *between* the original request and now (model version, tool backend,
     index) even though you tried to pin it; an unpinnable dependency
     (e.g. a managed model endpoint with no version pinning available) is
     itself a finding to report upstream.

4. **Work through the root-cause decision tree in this order** — later
   checks are more expensive, so rule out cheaper explanations first:

   | Check | Signal that confirms this bucket |
   |---|---|
   | **Tool failure** | A tool call in the transcript errored, timed out, returned malformed/truncated data, or returned a stale/wrong result that the model then reasoned over as if correct. |
   | **Retrieval issue** | (RAG-backed agents only) The retrieved chunks were missing the correct source, contained outdated content, or a relevant chunk existed but wasn't in the top-k returned. |
   | **Prompt issue** | Tool calls and retrieval were all correct, but the system prompt is ambiguous, missing an explicit instruction for this case, or contradicts itself — the model did a reasonable thing given what it was told. |
   | **Model behavior change** | The prompt, tools, and retrieval are all unchanged and were confirmed working before a specific date/model version, and the failure correlates with a provider-side model update or your own version bump. |
   | **Genuine edge case** | Reproduces deterministically, every upstream component (tools, retrieval, prompt) is confirmed correct and unambiguous, and the input is a legitimately novel scenario the system was never designed to handle. |

   ```python
   def classify_root_cause(transcript, changelog):
       if any(t.tool_result.error or t.tool_result.is_stale for t in transcript.tool_calls):
           return "tool_failure"
       if transcript.used_retrieval and not correct_source_in_topk(transcript):
           return "retrieval_issue"
       if prompt_has_ambiguity_or_gap(transcript.system_prompt, transcript.input):
           return "prompt_issue"
       if changelog.model_version_changed_since(transcript.last_known_good_date):
           return "model_behavior_change"
       return "genuine_edge_case"  # only after the above are actively ruled out, not by default
   ```

   Treat this function as a starting checklist, not a black box — each
   branch needs a human to actually inspect the evidence, not just a
   boolean flag.

5. **For a tool failure**, check whether the dispatcher surfaced the
   failure as a structured error the model could react to, or let it look
   like success (see
   [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)). If the
   agent got stuck retrying the same failing call, this may overlap with a
   tool-call loop — see
   [agent-tool-call-loop-diagnosis-and-circuit-breaking](../agent-tool-call-loop-diagnosis-and-circuit-breaking/SKILL.md).

6. **For a retrieval issue**, check separately whether the failure is a
   *recall* problem (right chunk exists but wasn't retrieved in top-k) or
   a *freshness* problem (index is stale relative to the source) — the
   fixes differ (re-ranking/chunking tuning vs. re-indexing cadence). See
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md) for the
   retrieval-quality pattern and
   [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md)
   for freshness/re-indexing mechanics.

7. **For a prompt issue**, resist the urge to patch the live production
   prompt immediately.

   > **Warning:** Editing a production system prompt directly in response
   > to one incident, with no staged rollout and no rollback path, risks
   > trading one failure mode for another that a quick spot-check won't
   > catch. Change the prompt in a branch/staging config, re-run the full
   > eval suite (not just the failing case) against it, and only then
   > promote it — with the previous version kept as an immediate rollback
   > target — per
   > [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md).

8. **For a model behavior change**, confirm the correlation with actual
   evidence (a version/date match in provider release notes or your own
   deployment log), not just suspicion after ruling out other causes.
   Where the model version is pinnable, that pin itself is the immediate
   mitigation; where it isn't (a "latest" alias endpoint), treat the lack
   of pinning as a finding to fix independent of this specific incident.

9. **For a genuine edge case**, do not treat "nothing is broken" as
   closing the ticket. A genuine edge case still needs a decision: is this
   rare enough to accept, or common enough to warrant new prompt guidance,
   a new tool, or a guardrail? Either way, it becomes a new eval case.

10. **Regardless of root cause, add the case to the eval suite** as a
    permanent regression test (see
    [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md))
    and, if the response was unsafe or policy-violating rather than merely
    low-quality, add or tighten a runtime guardrail as defense-in-depth
    independent of whatever upstream fix is applied.

11. **Track root-cause category over time**, not just per-incident fixes.
    If "tool failure" or "retrieval issue" keeps recurring as the
    classification, that's a signal the underlying tool reliability or
    index freshness needs a structural fix, not another one-off patch.

## Best practices

- Classify before fixing — resist pressure to ship an immediate patch
  before the root-cause tree has actually been worked through; a fast
  wrong fix costs more triage time later than a slightly slower right one.
- Keep the pinned-reproduction environment (versioned prompts, tool
  schemas, model identifiers, index snapshots) as a standing capability,
  not something assembled ad hoc during each incident.
- Prefer the cheapest, most falsifiable checks first (tool errors in the
  transcript, retrieval top-k contents) before reaching for the more
  expensive and less certain "maybe the model changed" explanation.
- Write the root-cause classification and evidence into the incident
  record even when the fix is obvious — the pattern across many incidents
  is often more valuable than any single fix.
- Treat "genuine edge case" as a real category with its own decision (ship
  a guardrail/prompt update or explicitly accept the risk), not a
  euphemism for "we don't know and are closing this."
- When a model behavior change is confirmed, report it upstream (provider
  changelog cross-check, internal deployment log entry) so the next
  similar report can be resolved faster.

## Common pitfalls

- **Symptom:** The team patches the system prompt the same day a bad
  response is reported, the report stops recurring, and it's marked
  resolved — then a different but related bad response appears weeks
  later.
  **Fix:** The original patch likely treated a symptom (this exact
  phrasing) rather than the root cause (an ambiguous instruction that
  produces this whole class of bad response). Re-run the full
  classification tree, and validate the fix against the eval suite's
  adversarial/edge-case subset, not just the one reported case.

- **Symptom:** Investigation stalls because the transcript only contains
  the final answer, not the intermediate tool calls or retrieved chunks,
  so there's no way to tell whether the failure was upstream.
  **Fix:** Treat full transcript logging (every model call, every tool
  call and raw result, every retrieved chunk) as a blocking prerequisite
  for this skill, not an optional nicety — retrofit it before attempting
  root-cause work on future incidents.

- **Symptom:** A reported bad response is blamed on "the model got worse"
  without evidence, a model version is rolled back, and the same class of
  bad response happens again on the old version.
  **Fix:** Confirm model-behavior-change as the cause with an actual
  version/date correlation before rolling back — check tool failures and
  retrieval quality first, since both are far more common causes than an
  actual model regression and a rollback that doesn't fix anything wastes
  an incident cycle while hiding the real cause.

- **Symptom:** A tool silently returned stale or partially-truncated data
  (no error raised), the model reasoned over it as if correct, and the
  investigation initially looks like a "hallucination" because the
  transcript shows the model confidently stating something false.
  **Fix:** Always inspect raw tool results in the transcript before
  concluding the model fabricated something — a model that accurately
  reports bad tool data isn't hallucinating, and the fix belongs in the
  tool/dispatcher layer (see
  [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)), not the
  prompt.

- **Symptom:** The same reported issue is re-triaged from scratch multiple
  times because no eval case was added after the first investigation.
  **Fix:** Make "add a regression case to the eval suite" a mandatory,
  non-optional last step of every triage, regardless of how the root
  cause was classified.

## Worked example

**Report:** A user asks the internal support agent "What's the refund
window for orders placed during the holiday sale?" and the agent confidently
answers "90 days," which is wrong — the correct policy (30 days for
holiday-sale orders, per an updated policy page) exists in the knowledge
base.

Triage:

1. Full transcript pulled for the request ID: system prompt (unchanged in
   3 months), one retrieval call, no other tool calls, final answer "90
   days, per our standard policy."
2. Pinned reproduction: re-running the same query against the retrieval
   index snapshot from the time of the report reproduces the same wrong
   answer identically.
3. Decision tree: no tool errors present (no tool calls other than
   retrieval) → not a tool failure. Retrieval top-6 chunks inspected:
   contain the *old* refund policy chunk (90 days, general orders) but not
   the newer holiday-sale-specific policy chunk, even though the newer
   chunk exists in the source CMS.
4. Root cause classified as **retrieval issue**, specifically a freshness
   problem, not a recall problem — the corpus's ingestion job runs weekly
   and the holiday-sale policy page was published 4 days before the
   report, so the new page hadn't been re-indexed yet.
5. Immediate action: manually trigger a re-index of the changed page
   rather than patching the prompt (which would have wrongly targeted a
   prompt issue that wasn't the cause).
6. Structural fix: per
   [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md),
   move ingestion from a weekly batch schedule to the CMS's
   on-publish webhook so policy changes are searchable within minutes, not
   up to a week later.
7. A new eval case is added: query "refund window for holiday sale orders"
   with expected source `doc-holiday-refund-policy`, run against the
   ingestion pipeline's freshness check going forward.

## Cross-references

- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md) — where the confirmed root cause becomes a permanent regression case and, for unsafe outputs, a runtime guardrail.
- [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md) — tool-failure classification depends on how tool errors are surfaced (or swallowed) by the dispatcher.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) and [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md) — retrieval-issue root causes split between retrieval-pattern tuning and ingestion freshness.
- [agent-tool-call-loop-diagnosis-and-circuit-breaking](../agent-tool-call-loop-diagnosis-and-circuit-breaking/SKILL.md) — when a tool failure manifests as a stuck retry loop rather than a single bad answer.
- [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md) — fixing a confirmed prompt-issue root cause.
