---
name: incident-playbook
description: Generate runbooks for common AI automation failures. Covers model timeouts, hallucination detection, cost spikes, accuracy drops, data pipeline failures, and prompt injection attempts.
---

# Incident Playbook — AI Failure Runbook Generator

## Purpose

Generate structured runbooks for common AI automation failures. Every AI system in production will eventually encounter failures specific to the AI domain: models time out, hallucinations slip through, costs spike unexpectedly, accuracy degrades silently, data pipelines break, and adversarial inputs probe for weaknesses.

This skill produces a comprehensive playbook tailored to a specific automation, covering nine failure categories with detection methods, severity classification, step-by-step response procedures, root cause investigation guides, and client communication templates. The playbook is the document your team reaches for at 2 AM when the system is misbehaving.

Run this **after** the automation architecture is understood (ideally after `/ai-invert` and `/guardrail-spec`) and **before** or **during** deployment. The output complements the `/deploy-checklist` by ensuring operational readiness.

## Pre-flight: Auto-sync Check

Before starting, read the root `CLAUDE.md` (if it exists). If `## How to Approach Tasks` appears AFTER `## Tech Stack` or `## Architecture`, the file has an outdated section order. Silently run `/genai-sync` to fix it before continuing with this skill.

## Input

The user provides the name of the automation or system to generate a playbook for. This can be:
- A specific automation name (e.g., "support-classifier", "document-extractor")
- A system or pipeline name (e.g., "rag-pipeline", "lead-scoring-system")
- A reference to existing `.plans/` artifacts that describe the automation

## Workflow

### Step 1: Understand the Automation Architecture

**Actions:**
1. Read the automation codebase: prompts, model configurations, pipeline configs, application code, infrastructure definitions
2. Check root context files (`CLAUDE.md`, `AGENTS.md`) for architecture overview and conventions
3. Read `.plans/` for related artifacts:
   - `INVERT-*.md` — risk analyses identifying failure modes (especially dimensions B-H). Use the risk list to prioritize which runbooks need the most detail.
   - `GUARDRAILS-*.md` and `GUARDRAILS-REPORT-*.md` — guardrail specs and validation results. Reference actual detection methods and fallback behaviors in runbooks.
   - `COST-*.md` — cost projections and budget thresholds. Use for cost spike incident thresholds.
   - `BASELINE-*.md` — baseline metrics. Use for accuracy/latency regression thresholds in detection.
   - `EVAL-*/` — eval suites and results. Use eval thresholds as accuracy incident triggers.
   - `OPS-<name>.md` — ai-ops monitoring config (if exists). **Use the actual dashboard names, alert names, and metric queries defined here** instead of generic monitoring instructions. If ai-ops has defined "alert: cost-spike-daily triggers at >150% of budget via PagerDuty to #oncall-ai," reference that exact alert in the cost spike runbook.
   - `DECISIONS.md` — prior decisions constraining the system
   - `LEARNINGS.md` — lessons from prior incidents. If a prior incident was learned from, reference the specific learning.
4. Map the system architecture:
   - **External dependencies**: model providers (which APIs, which models), embedding services, databases, third-party APIs
   - **Data pipeline**: ingestion sources, processing steps, storage, retrieval
   - **Monitoring**: what is currently monitored, what alerts exist, who is on-call
   - **Deployment**: how the system is deployed, how rollback works
5. Identify the **blast radius** of each component failure — what breaks downstream?

### Step 2: Generate Incident Runbooks

For each of the nine failure categories below, generate a complete runbook section. Tailor every section to the specific automation — generic advice is not useful at 2 AM.

**Every incident must include a "Time to Detect" estimate** — how long this failure would go unnoticed WITHOUT proactive monitoring. This drives monitoring investment decisions:
- **Seconds-minutes:** Immediate user impact, requests fail visibly (e.g., timeouts)
- **Hours:** Degraded quality accumulates, users notice after several interactions (e.g., accuracy drift)
- **Days-weeks:** Silent degradation, no user-visible symptom until threshold breach (e.g., stale embeddings, cost creep)

Incidents with days-weeks detection lag are the most dangerous — they need proactive monitoring most urgently.

If a failure category does not apply to this automation (e.g., no RAG pipeline means "Embedding Index Stale" is irrelevant), note it as "N/A for this system" with a one-line explanation, and move on.

---

#### Incident 1: Model Timeout / Rate Limit Exceeded

**Detection:**
- Typical signals: increased latency, 429 status codes, request queue growth
- **Time to detect (without monitoring):** Seconds-minutes — requests fail immediately and visibly
- **Detection commands** (tailor to THIS project's actual tools):
  ```
  # Check error rate (replace with project's actual monitoring tool/query)
  <actual log query, e.g., "grep '429\|timeout' /var/log/app/ai-pipeline.log | wc -l">
  <or dashboard URL: "https://grafana.internal/d/ai-pipeline?panel=error-rate">
  <or CLI: "aws cloudwatch get-metric-statistics --metric-name ModelErrors ...">
  ```
  **Every detection section must include at least one runnable command, log query, or dashboard URL** that the on-call person can execute immediately. "Check the dashboard" is not a detection command. "Open https://grafana.internal/d/ai-pipeline and check the error-rate panel for the last 15 minutes" is.

**Severity Classification:**

| Severity | Symptom | Blast Radius (for THIS automation) |
|----------|---------|-----------------------------------|
| P1 | User-facing requests failing | <name specific downstream systems and user count affected — e.g., "Classification API serves Dashboard + Slack notifier, ~2K users/day"> |
| P2 | Batch processing delayed, user-facing has fallback | <name what degrades — e.g., "Nightly re-classification delayed, stale labels for up to 24h"> |
| P3 | Only non-critical background tasks affected | <name what's affected — e.g., "Analytics pipeline receives delayed data"> |

**Rule:** Severity must name the specific blast radius for THIS system, not generic impact. "User-facing requests failing" becomes "Classification API returns errors → client dashboard shows 'processing' indefinitely → Slack notifications stop → 2K daily users affected."

**Immediate Response:**
1. Confirm the incident — check model provider status page and internal metrics
2. Activate fallback model (if configured) — document the specific fallback path
3. Enable request queuing or retry with exponential backoff
4. If rate limited: check for runaway loops or misconfigured batch jobs consuming quota
5. Communicate to affected users if response times are visibly degraded

**Root Cause Investigation:**
- Check if the model provider has a known outage (status page, social media, support channels)
- Check if traffic volume spiked unexpectedly (new client, batch job, retry storm)
- Check if a code change increased tokens per request or request frequency
- Review rate limit headers from recent responses to understand consumption patterns

**Resolution:**
- If provider outage: wait for resolution, keep fallback active, monitor provider status
- If self-inflicted (traffic spike, runaway job): fix the root cause, then restore primary model
- If persistent rate limiting: request quota increase, implement better request batching, or add caching

**Prevention:**
- Configure fallback model with automatic failover
- Implement circuit breaker pattern for model API calls
- Set up rate limit consumption alerts at 70% and 90% of quota
- Cache frequent requests to reduce API call volume
- Implement request prioritization (user-facing > batch)

**Client Communication Template:**
> We are experiencing intermittent delays in [system name] responses due to elevated demand on our AI infrastructure. Our team is actively working on this. Expected resolution: [time]. Your requests are being queued and will be processed. No data has been lost.

---

#### Incident 2: Token Limit Exceeded (Context Too Large)

**Detection:**
- Error codes indicating context length exceeded (provider-specific error codes)
- Requests failing with specific input patterns (long documents, many retrieved chunks)
- Sudden increase in model API errors correlated with input size

**Severity Classification:**
- P1 if a class of inputs consistently fails with no fallback
- P2 if only edge-case inputs are affected and most requests succeed
- P3 if the system gracefully truncates and produces acceptable output

**Immediate Response:**
1. Identify which inputs are triggering the limit — log the input sizes
2. Check if a recent change increased context size (more RAG chunks, longer system prompt, new few-shot examples)
3. If possible, temporarily reduce context (fewer chunks, shorter system prompt) to restore service
4. Route oversized requests to a model with a larger context window (if available)

**Root Cause Investigation:**
- Measure token distribution across components: system prompt + few-shot examples + retrieved context + user input + output reservation
- Identify which component grew — was it a prompt change, a retrieval config change, or unusual input?
- Check if token counting is accurate (tokenizer mismatch between estimation and actual API)

**Resolution:**
- Implement input truncation with graceful degradation (summarize long inputs, reduce chunk count)
- Optimize system prompt and few-shot examples for token efficiency
- Upgrade to a model with a larger context window if the use case requires it
- Implement dynamic context management — adjust chunk count based on input size

**Prevention:**
- Add pre-flight token count validation before every model API call
- Set hard limits on each context component (system prompt budget, retrieval budget, input budget)
- Monitor token usage distribution over time — detect drift before it causes failures
- Test with maximum-size inputs in the eval suite

**Client Communication Template:**
> Some requests with unusually large inputs are experiencing processing errors in [system name]. Our team has identified the issue and is implementing a fix. Requests with typical input sizes are unaffected. If you are experiencing errors, please try with a shorter input while we resolve this.

---

#### Incident 3: Content Filter Triggered

**Detection:**
- Model provider returns content filter / safety block responses
- Spike in blocked requests that should be legitimate
- User complaints about requests being rejected

**Severity Classification:**
- P1 if the content filter is blocking a high percentage of legitimate requests
- P2 if only specific input patterns are affected
- P3 if the filter is working correctly but users need guidance

**Immediate Response:**
1. Determine if the filter is the model provider's built-in filter or your custom guardrail
2. If provider filter: check for provider-side filter sensitivity changes (often unannounced)
3. If custom guardrail: check for recent configuration changes to thresholds or patterns
4. Review sample blocked requests to classify as true positives vs false positives
5. If false positive rate is high: temporarily relax custom filters (if safe) or route to fallback

**Root Cause Investigation:**
- Review blocked request samples — what pattern triggers the filter?
- Check if the model provider updated their content policy or filter model
- Check if input patterns changed (new use case, new client, different language)
- If custom filter: review filter rules for overly broad patterns

**Resolution:**
- If provider filter: adjust prompts to avoid triggering patterns, contact provider support, consider alternative model
- If custom filter: refine detection rules to reduce false positives while maintaining protection
- Add exemptions for known-safe input patterns (with logging)
- Implement a secondary path for filtered requests (human review queue)

**Prevention:**
- Test prompts against known content filter edge cases in eval suite
- Monitor content filter trigger rate as a key metric — alert on sudden changes
- Maintain a list of known false-positive input patterns and test against them
- Keep custom filter thresholds configurable so they can be tuned without redeployment

**Client Communication Template:**
> Some requests in [system name] are being flagged by our safety filters. We are reviewing the filter configuration to reduce false positives. If your request was incorrectly blocked, please contact [support channel] and we will process it manually.

---

#### Incident 4: Hallucination Detected in Production

**Detection:**
- User reports factual errors, fabricated citations, or invented data in outputs
- Automated fact-checking or consistency checks flag discrepancies
- Output audit reveals claims not supported by retrieved context
- Downstream systems receive incorrect data from the automation

**Severity Classification:**
- P1 if the hallucination caused a client action (financial decision, published content, customer communication)
- P1 if the hallucination involves fabricated legal, medical, or financial information
- P2 if detected internally before impacting client actions
- P3 if the hallucination is minor (formatting, low-impact phrasing) and caught by review

**Immediate Response:**
1. Identify the scope — is this a one-off or a pattern? Check recent outputs for similar hallucinations
2. If client-facing: immediately notify the affected client with a correction
3. If the hallucination caused downstream actions: assess impact and initiate reversal if possible
4. If a pattern is detected: add a temporary guardrail (keyword filter, human review for affected output types)
5. Preserve the input, output, and retrieved context for root cause analysis

**Root Cause Investigation:**
- Was relevant context retrieved? Check retrieval results for the failing request
- Was the context accurate? Check source documents for correctness and freshness
- Did the model ignore the context? Compare output claims against retrieved chunks
- Was the prompt encouraging fabrication? (e.g., "always provide an answer" without "say you don't know if unsure")
- Did a model version change introduce new hallucination patterns?

**Resolution:**
- Fix the prompt to explicitly instruct "only answer based on provided context" and "say you don't know if unsure"
- Improve retrieval quality (better chunking, reranking, relevance filtering)
- Add output verification guardrails (fact-check against source data, consistency checks)
- Update eval suite with the hallucination case as a regression test
- If model version caused the issue: pin to previous version or switch models

**Prevention:**
- Include hallucination-specific test cases in the eval suite (questions where the answer is NOT in the context)
- Implement automated output-vs-context consistency checking
- Require citation for factual claims in the prompt design
- Monitor hallucination rate as a key quality metric
- Regular human review sampling of production outputs

**Client Communication Template:**
> We identified an error in a response provided by [system name] on [date]. The output contained [brief description of error]. We have corrected this and implemented additional verification to prevent recurrence. We apologize for any inconvenience. If you took action based on this output, please [specific remediation guidance].

---

#### Incident 5: Embedding Index Stale or Corrupted

**Detection:**
- Retrieval quality drops — model outputs become less relevant or accurate
- Known documents are not being retrieved for relevant queries
- Embedding index metadata shows last update timestamp is stale
- Index size mismatch with expected document count

**Severity Classification:**
- P1 if the system is returning irrelevant or outdated information to clients
- P2 if retrieval quality is degraded but outputs are still roughly correct
- P3 if only newly added documents are not yet indexed (known delay)

**Immediate Response:**
1. Check the last successful index update timestamp
2. Verify the embedding pipeline is running — check job logs, scheduler status
3. If index is corrupted: switch to the last known-good index snapshot (if available)
4. If stale: trigger a manual index rebuild
5. If the system is producing notably wrong outputs: add a temporary disclaimer or route to fallback

**Root Cause Investigation:**
- Check the embedding pipeline job logs — did a job fail silently?
- Check source data availability — is the upstream data source accessible?
- Check for schema changes in source documents that broke the parser
- Check embedding model availability — did the embedding API have an outage?
- Check storage — did the index exceed storage limits?

**Resolution:**
- Fix the pipeline failure and trigger a full reindex
- If source data changed format: update the parser and reprocess
- If embedding model changed: re-embed all documents with the new model
- Verify index integrity after rebuild (document count, spot-check retrievals)

**Prevention:**
- Monitor index freshness as a key metric — alert when last update exceeds threshold
- Implement index integrity checks (document count, embedding dimension, spot-check queries)
- Maintain index snapshots for quick rollback
- Run a daily retrieval quality test (known query -> expected document pairs)
- Set up pipeline failure alerts with clear error messages

**Client Communication Template:**
> [System name] may be using slightly outdated information for responses generated between [start time] and [end time]. We have refreshed our data and responses are now current. If you received a response during this window that seems outdated, please resubmit your request.

---

#### Incident 6: Cost Spike Detected

**Detection:**
- Cost monitoring alert triggers (daily spend exceeds threshold)
- Token usage dashboard shows unexpected increase
- Model provider billing alert fires
- Unusual request volume or request size patterns

**Severity Classification:**
- P1 if spend rate will exceed monthly budget within days
- P2 if spend is elevated but within manageable range
- P3 if the spike is explained by legitimate usage growth

**Immediate Response:**
1. Identify the source of the spike — which endpoint, which client, which model?
2. Check for runaway loops, retry storms, or misconfigured batch jobs
3. If a specific source is identified: throttle or pause it
4. If unexplained: enable request sampling to reduce volume while investigating
5. Check if a code change increased tokens per request (longer prompts, more context, removed caching)

**Root Cause Investigation:**
- Compare current request patterns with baseline: volume, tokens per request, model used
- Check for recent deployments that changed prompt length, retrieval count, or model selection
- Check for client-side changes that increased request volume
- Check if caching is functioning correctly — cache hit rate vs baseline
- Check for duplicate or unnecessary model calls in the pipeline

**Resolution:**
- Fix the root cause (runaway job, cache failure, prompt bloat, missing dedup)
- Implement or restore caching for frequently repeated requests
- Optimize prompts for token efficiency if they have grown
- If legitimate growth: update budget projections and get approval for increased spend

**Prevention:**
- Set cost alerts at multiple thresholds (50%, 80%, 100% of budget)
- Implement per-client and per-endpoint cost tracking
- Add automatic throttling when spend rate exceeds configured threshold
- Review token usage in every deployment checklist
- Cache system prompt tokens where the provider supports it (prompt caching)

**Client Communication Template:**
> We detected unusual usage patterns in [system name] that resulted in elevated processing costs. We have identified and resolved the cause. There is no impact to your service or data. [If client-caused: We recommend reviewing your integration to ensure request patterns align with expected usage.]

---

#### Incident 7: Accuracy Drop Below Threshold

**Detection:**
- Automated eval suite shows accuracy below threshold on scheduled run
- User feedback indicates declining output quality
- Downstream metrics (conversion rate, error rate, rejection rate) shift negatively
- Human review sampling shows increased error rate

**Severity Classification:**
- P1 if accuracy drop is significant (>10% below baseline) and client-facing
- P2 if accuracy drop is moderate (5-10% below baseline) or detected before client impact
- P3 if accuracy drop is minor (<5%) and caught by monitoring

**Immediate Response:**
1. Confirm the accuracy drop with a focused eval run (not just monitoring noise)
2. Check if the model provider made a change (model version update, behavior change)
3. Check if input distribution shifted (new type of request, different client, seasonal pattern)
4. If drop is severe and confirmed: activate fallback (previous model version, simplified prompt, human review)
5. Notify stakeholders of the quality degradation and response plan

**Root Cause Investigation:**
- Run evals against the previous model version — does accuracy restore? (model change)
- Run evals with recent production inputs vs original eval inputs — does accuracy differ? (distribution shift)
- Check for prompt changes, retrieval changes, or guardrail changes that could affect output quality
- Check if the training data or knowledge base has changed
- Analyze error patterns — is the accuracy drop uniform or concentrated in specific input types?

**Resolution:**
- If model change: pin to previous version, evaluate new version, adjust prompts for new model behavior
- If distribution shift: update prompts and eval suite to handle new input patterns
- If code change: revert the change and investigate
- Update baseline with corrected performance metrics
- Add regression test cases for the patterns that failed

**Prevention:**
- Run automated evals on a regular schedule (daily or weekly)
- Monitor accuracy-correlated proxy metrics in real time (confidence scores, retrieval relevance)
- Pin model versions and test before upgrading
- Maintain a diverse eval set that covers known input variations
- Track input distribution metrics to detect shift early

**Client Communication Template:**
> We detected a temporary reduction in [system name] output quality and have taken corrective action. Outputs generated between [start time] and [end time] may have reduced accuracy. We recommend reviewing any critical decisions made based on outputs from this period. Quality has been restored to normal levels.

---

#### Incident 8: Data Pipeline Failure (Upstream Source Unavailable)

**Detection:**
- Pipeline health check fails — source API returns errors or timeouts
- Data freshness monitoring shows last successful fetch exceeds threshold
- Zero new documents processed in expected time window
- Scheduled ingestion job reports failure

**Severity Classification:**
- P1 if the system is serving answers based on critically outdated data
- P2 if data is stale but still within acceptable freshness window
- P3 if the pipeline failure is detected early and a retry will resolve it

**Immediate Response:**
1. Identify which upstream source is unavailable — check connectivity, authentication, source status
2. Check if the system can operate on cached/stale data with acceptable quality
3. If data freshness is critical: add a disclaimer to outputs noting the data staleness
4. Trigger a manual pipeline run once the source is available
5. Check if other downstream systems are also affected

**Root Cause Investigation:**
- Check upstream source status — is it a known outage, maintenance window, or permanent change?
- Check authentication — did API keys expire, credentials rotate, or permissions change?
- Check network — firewall changes, DNS issues, VPN requirements?
- Check data format — did the source schema change, breaking the parser?
- Check rate limits — is the pipeline being throttled by the source?

**Resolution:**
- If source outage: wait for resolution, implement retry with backoff, trigger backfill when available
- If auth failure: rotate credentials, update secrets, verify permissions
- If schema change: update parser, reprocess recent data, verify data integrity
- If permanent source change: evaluate alternative sources or negotiate with the source provider

**Prevention:**
- Monitor pipeline health with heartbeat checks (not just failure alerts)
- Implement graceful degradation — serve stale data with freshness indicator rather than failing
- Set up credential expiration monitoring and proactive rotation
- Maintain source API documentation and change notification subscriptions
- Test pipeline recovery by simulating source failures in staging

**Client Communication Template:**
> [System name] is currently operating with data last updated on [timestamp] due to a temporary disruption in our data feed. Responses remain available but may not reflect changes after [timestamp]. We expect to restore full data freshness by [estimated time]. Critical decisions should be verified against primary sources during this period.

---

#### Incident 9: Prompt Injection Attempt Detected

**Detection:**
- Guardrail triggers on prompt injection patterns (role switching, instruction override, encoded instructions)
- Canary token detected in output (system prompt leakage)
- Output suddenly deviates from expected format or content scope
- Unusual input patterns from a specific user or session

**Severity Classification:**
- P1 if the injection succeeded — system prompt leaked, business rules bypassed, or unauthorized output produced
- P2 if the injection was detected and blocked but the attempt was sophisticated
- P3 if the injection was a known pattern and was blocked by standard guardrails

**Immediate Response:**
1. If the injection succeeded: assess what was exposed or what action was taken
2. Block or rate-limit the offending user/session/IP
3. Review the last N outputs from the same user/session for prior successful injections
4. If system prompt was leaked: assess the sensitivity of leaked content
5. Preserve the full request/response chain for security review

**Root Cause Investigation:**
- How did the injection bypass existing guardrails? (new pattern, encoding trick, multi-turn attack)
- Was this a targeted attack or automated probing?
- What was the attacker's likely objective? (data extraction, behavior manipulation, system prompt theft)
- Review guardrail coverage — which defense layer failed or was missing?
- Check if similar patterns appear in other sessions

**Resolution:**
- Add the new injection pattern to the detection rules
- If system prompt was leaked: rotate any sensitive information in the prompt
- Strengthen guardrail layers — add classifier-based detection if using only pattern matching
- Implement output monitoring for system prompt fragments
- If a vulnerability was exploited: patch and re-test

**Prevention:**
- Layer injection defenses (pattern matching + classifier + input/output consistency check)
- Embed canary tokens in system prompts to detect leakage
- Minimize sensitive information in system prompts
- Implement session-level anomaly detection
- Regular adversarial testing (red-team the prompts)
- Rate-limit users who trigger injection guardrails

**Client Communication Template:**
> Our security systems detected and blocked an unauthorized attempt to manipulate [system name]. No client data was exposed or compromised. We have strengthened our defenses against this type of attempt. [If client needs to take action: We recommend reviewing any outputs from session [ID] before relying on them.]

---

### Step 3: Write to Disk

**Actions:**
1. Create `.plans/` directory if it does not exist
2. Generate a short kebab-case name from the automation (e.g., `support-classifier`, `rag-pipeline`, `document-extractor`)
3. Write the full playbook to `.plans/PLAYBOOK-<name>.md` with this header:

```markdown
# Incident Playbook: <automation name>

**Created:** <date>
**System:** <brief description of the automation>
**Architecture:** <key components — model provider, data sources, deployment platform>
**On-Call:** <who is responsible for incident response — role or team>
**Escalation Path:** <who to escalate to for P1 incidents>

## Incident Response Overview

| # | Incident Type | Applicable? | Severity Range |
|---|--------------|-------------|----------------|
| 1 | Model Timeout / Rate Limit | <Yes/No> | <P1-P3> |
| 2 | Token Limit Exceeded | <Yes/No> | <P1-P3> |
| 3 | Content Filter Triggered | <Yes/No> | <P1-P3> |
| 4 | Hallucination in Production | <Yes/No> | <P1-P3> |
| 5 | Embedding Index Stale | <Yes/No> | <P1-P3> |
| 6 | Cost Spike | <Yes/No> | <P1-P3> |
| 7 | Accuracy Drop | <Yes/No> | <P1-P3> |
| 8 | Data Pipeline Failure | <Yes/No> | <P1-P3> |
| 9 | Prompt Injection | <Yes/No> | <P1-P3> |

## Runbooks

<Full runbook sections from Step 2, tailored to this specific automation>
```

4. Inform the user: "Incident playbook saved to `.plans/PLAYBOOK-<name>.md`"

### Step 4: Present Summary

After writing to disk, present a concise summary:

```
## Incident Playbook: <name>

**Applicable Incidents:** <count of 9>
**System Dependencies:** <list key external dependencies>

### Escalation Chain

| Time Since Detection | Action | Who |
|---------------------|--------|-----|
| 0 min | On-call acknowledges, starts runbook | <on-call engineer> via <channel> |
| 15 min | If not resolved: escalate to team lead | <team lead> via <channel> |
| 30 min | If P1 and not resolved: escalate to engineering manager | <eng manager> via <channel> |
| 1 hour | If P1 and client-facing: notify client success team | <client success> via <channel> |
| 2 hours | If P1 and not resolved: executive notification | <VP/CTO> via <channel> |

Adjust time thresholds based on the automation's SLA. Client-facing P1 incidents should escalate faster than internal P2s.

### Quick Reference

| Incident | Detection | Severity | First Action |
|----------|-----------|----------|-------------|
| Model Timeout | <metric/alert> | <P1/P2/P3> | <first step> |
| Token Limit | <metric/alert> | <P1/P2/P3> | <first step> |
| ... | ... | ... | ... |

Playbook saved to `.plans/PLAYBOOK-<name>.md`.
```

## Notes

- This skill is language-agnostic — it produces operational runbooks, not code
- Read actual code, configs, and architecture before writing runbooks — generic runbooks are useless at incident time
- Tailor every runbook to the specific automation — name the actual model provider, actual monitoring tools, actual deployment platform
- If an `/ai-invert` analysis exists, use its risk findings to prioritize which runbooks need the most detail
- If a `/guardrail-spec` exists, reference its detection methods and fallback behaviors in the runbooks
- Client communication templates should be professional, honest, and specific — avoid jargon but do not hide what happened
- Severity classifications should be calibrated to the specific automation's impact — a P1 for an internal tool may be a P3 for a critical client-facing system
- Runbooks should be executable by someone who did not build the system — include specific commands, URLs, and contact information where possible
- Review and update the playbook after every real incident — lessons learned should feed back into prevention measures
- The playbook complements the `/deploy-checklist` — the checklist verifies readiness, the playbook handles what goes wrong after deployment
