---
name: guardrails-and-safety
version: 1.0.0
min_mindforge_version: 10.0.7
status: stable
triggers: guardrails, ai safety layer, hallucination detection, output validation layer, content filtering, ai boundary enforcement, graceful degradation pattern, confidence calibration, refusal pattern, safety guardrail, output quality gate, ai output control
---

# Guardrails and Safety

## When this skill activates

This skill activates when designing safety layers for AI systems, validating AI outputs, detecting hallucinations, filtering harmful content, enforcing behavioral boundaries, or implementing graceful degradation. Use this skill whenever AI-generated output is consumed by users or downstream systems and correctness, safety, or trustworthiness is a requirement.

## Mandatory actions when this skill is active

### Before

1. **Risk assessment** — Classify the risk level of the AI output. High risk: medical/legal/financial advice, code that handles money/auth, user-facing claims. Low risk: internal summaries, creative brainstorming, non-critical formatting.
2. **Define failure modes** — Enumerate what can go wrong: hallucinated facts, malformed output, harmful content, scope creep, leaked system prompts, confidently wrong answers.
3. **Identify stakeholders** — Who consumes this output? End users, other AI agents, automated systems? Each requires different guardrail approaches.
4. **Establish ground truth** — Determine what sources can be used to verify AI claims. No verification source = higher hallucination risk.

### During

#### Output Validation (Schema Check, Reference Grounding, Claim Verification)

**Schema validation:**
- Parse all structured outputs through a schema validator (Zod, Pydantic, JSON Schema).
- Reject outputs that don't conform. Never silently accept malformed data.
- Validate semantic constraints beyond syntax: dates in the past, IDs that exist, values within valid ranges.

**Reference grounding:**
- For factual claims, require the AI to cite specific sources from the provided context.
- Verify citations actually exist in the context window. Reject fabricated references.
- Cross-reference extracted facts against the source document. Flag discrepancies.

**Claim verification pipeline:**
```
AI Output → Extract claims → Match claims to source → Score confidence → Flag ungrounded claims
```

- Claims with no source match receive a "unverified" flag.
- Claims contradicting source receive a "contradicted" flag.
- Only claims with verified source matches pass without flags.

#### Hallucination Detection

- **Citation requirement** — For factual tasks, require inline citations: "[from file.ts:42]". Absence of citations on factual claims is a hallucination signal.
- **Self-consistency check** — Ask the same question multiple times (temperature > 0). If answers diverge significantly, confidence should be low.
- **Source comparison** — Compare AI output against retrieved context. Claims not present in context are hallucination candidates.
- **Knowledge boundary awareness** — Train the system to say "I don't have information about X" rather than fabricate. Reward refusal over confabulation.
- **Confidence scoring** — Implement a scoring function:
  - 1.0: Directly quoted from source
  - 0.8: Clearly supported by source
  - 0.5: Plausible inference from source
  - 0.2: Not supported, model's general knowledge
  - 0.0: Contradicts available evidence

#### Content Filtering

**PII detection:**
- Scan outputs for patterns: email addresses, phone numbers, SSNs, credit card numbers, physical addresses.
- Use regex for structured PII + NER models for unstructured PII (names, locations in context).
- Action: redact, mask, or block output containing PII not explicitly requested.

**Toxicity filtering:**
- Apply toxicity classifiers to AI outputs before delivery.
- Threshold: block outputs scoring above toxicity threshold (adjust per use case).
- Log blocked outputs for review and model improvement.

**Off-topic detection:**
- Compare output topic to the requested task.
- If the AI produces content unrelated to the request, it may be following injected instructions.
- Action: flag for review, re-generate with stronger constraints.

#### Boundary Enforcement (Scope Limits, Capability Declaration)

- **Capability declaration** — The system prompt must explicitly state what the AI can and cannot do. This is not optional.
- **Scope fencing** — Define topics/actions that are in-scope vs out-of-scope. Out-of-scope requests receive a structured refusal, not an attempt.
- **Action restrictions** — List dangerous actions the AI must never take (delete production data, send emails without confirmation, execute unreviewed code).
- **Escalation triggers** — Define conditions that require human review before proceeding: confidence below threshold, ambiguous instructions, high-impact actions.

**Boundary enforcement template:**
```
You CAN: [list of permitted capabilities]
You CANNOT: [list of restricted capabilities]
When uncertain: [escalation procedure]
When asked to do something restricted: [refusal response]
```

#### Graceful Degradation

- **Partial answer over no answer** — If the AI can answer part of the question confidently, provide that part and explicitly flag what it cannot answer.
- **Confidence flagging** — Prefix uncertain claims with qualifiers: "Based on the provided context...", "I'm not certain, but...", "This may be incomplete because..."
- **Fallback hierarchy:**
  1. Full confident answer (ideal)
  2. Partial answer with uncertainty flags (acceptable)
  3. Structured "I cannot answer because..." (acceptable)
  4. Silent failure or confident wrong answer (unacceptable)
- **Degradation transparency** — Always tell the user what information is missing and why the answer may be incomplete.

#### Confidence Calibration

- **Calibration principle** — Expressed confidence must match actual accuracy. "Definitely" = right >95% of the time.
- **Banned phrases when uncertain** — "certainly", "definitely", "obviously", "without doubt" unless grounded in verified source.
- **Required phrases when uncertain** — "likely", "based on available information", "this appears to be", "I'm not certain but".
- **Metacognitive awareness** — The AI must identify gaps in its knowledge: "I don't have enough context to answer this part."

#### Refusal Patterns (When to Refuse)

**Refuse when:** harmful content requested, clearly out of scope, insufficient context with high stakes, capabilities not available, or safety boundaries would be violated.

**Refusal format:** "I cannot [action] because [reason]. What I can do instead: [alternative]."

- **Never refuse without explanation.** Always state why and offer alternatives.
- **Never refuse legitimate requests.** Overly cautious refusals degrade trust and usability.

### After

1. **Audit guardrail triggers** — Review what was blocked/flagged. High false-positive rate means guardrails are too aggressive.
2. **Measure hallucination rate** — Sample outputs and verify claims against sources. Track rate over time.
3. **Test adversarially** — Attempt to bypass guardrails with injection, social engineering, and edge cases. Patch gaps.
4. **User feedback loop** — Collect reports of incorrect outputs that passed guardrails. These are the most valuable signals.

## Self-check before task completion

- [ ] Output validation schema is defined and enforced programmatically
- [ ] Hallucination detection is active for factual claims (citation requirement or source comparison)
- [ ] PII filtering scans all user-facing outputs
- [ ] Capability boundaries are explicitly declared in system prompt
- [ ] Graceful degradation is implemented (partial answers > silent failures)
- [ ] Confidence calibration prevents false certainty on ungrounded claims
- [ ] Refusal patterns provide clear explanation and alternatives
- [ ] Guardrails have been tested adversarially with bypass attempts
- [ ] False positive rate is monitored and acceptable
- [ ] Escalation path exists for edge cases guardrails cannot resolve
