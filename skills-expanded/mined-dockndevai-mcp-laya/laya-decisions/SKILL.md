---
name: laya-decisions
description: >-
  When and how to offload a decision to laya through mcp-laya — a fast, local, non-autoregressive
  System-1 engine for typed decisions (classify / score / yes-no) over text, email, tickets or JSON,
  in 100+ languages, with calibrated confidence and no hallucination. Use whenever you need a quick
  judgment call (routing, triage, a yes/no gate, a severity score, a moderation/guard check) instead
  of a slow, costly, hallucination-prone LLM round-trip.
---

# Deciding with laya (mcp-laya)

laya answers **typed questions** about a state in a single local forward pass (~33 ms), across 100+
languages, returning a **calibrated confidence** with every answer and **generating no text** — so
there is nothing to parse and nothing to hallucinate. It runs locally and offline; the data never
leaves the machine.

## When to reach for laya instead of thinking it through yourself

Use laya for the repetitive **System-1** judgment calls — the ones that are fast, bounded, and
benefit from a confidence score:

- **Routing / classification** — which team/department/category does this belong to?
- **Yes/no gates** — is this a refund request? a security incident? spam? on-topic?
- **Severity / ordinal scoring** — how urgent (0..n)? how negative the sentiment?
- **Triage / moderation / prompt-injection guarding** — via the built-in presets.
- **Language/script detection** — before deciding how to handle multilingual input.

Do **not** use it for open-ended generation, extraction of long spans, or anything needing a written
explanation — that's the main model's job. laya decides; it doesn't write.

## The tools

- `decide(state, questions)` — several typed questions at once (the full engine). Each question:
  - `choice`: `{"type":"choice","instructions":"…","criteria":{"labelA":"desc","labelB":"desc"}}`
  - `score`:  `{"type":"score","instructions":"…","criteria":["level0","level1","level2"]}`
  - `noul`:   `{"type":"noul","instructions":"…"}`  (yes / no / unknown)
- `classify(state, labels|criteria, instructions?)` — one best category.
- `score(state, instructions, levels)` — one ordinal rating.
- `check(state, instructions)` — one yes/no gate.
- `triage(state, preset)` — a ready-made set: `triage`, `email`, `moderation`, `guard`.
- `detect_language(text)`, `explain_routing(state, questions)`, `list_models()`.

`state` can be plain text **or** a JSON object (e.g. `{"from":…, "subject":…, "body":…}`) — pass the
structure you have; laya reads it directly.

## Writing good typed questions

- **Give `choice` labels short descriptions** (`criteria` as a map), not bare names — accuracy jumps.
- **Order `score` levels low → high**; the result is an expected value across them plus a legend.
- **Phrase `noul` as a single, answerable yes/no**, e.g. "Does the user explicitly request a refund?"
- **Batch related questions in one `decide` call** — same forward pass, one round-trip.
- Let the model auto-route (default). Only pin `model=` (`english` / `multilingual` /
  `typed-decisions`) when you have a reason.

## Trust the confidence, not the label alone

Every answer carries `confidence` (calibrated). Use it for control flow:

- High confidence → act on it directly.
- Low confidence (or `low_confidence: true` when a threshold is set, or a value near 0.5 on a
  yes/no) → don't treat it as ground truth; fall back to the main model or ask the user.

laya makes judgments, not facts. It's the fast first pass; you decide what a low-confidence answer
warrants.

## Example

```jsonc
// One call, three decisions on a support ticket:
decide(
  {"subject":"Duplicate charge on #4411","body":"Billed twice for March. Refund today or we cancel."},
  {
    "department": {"type":"choice","instructions":"Which team?","criteria":{"billing":"payments, refunds","technical":"bugs, outages","sales":"pricing"}},
    "urgency":    {"type":"score","instructions":"How urgent?","criteria":["low","soon","critical"]},
    "churn_risk": {"type":"noul","instructions":"Does the user threaten to cancel?"}
  }
)
// -> department=billing (0.95), urgency≈2 (critical), churn_risk=yes (0.91)
```

Then branch on the results: route to billing, mark critical, flag the churn risk — all from one
local, sub-100 ms call.
