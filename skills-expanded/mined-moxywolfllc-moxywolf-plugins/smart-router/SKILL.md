---
name: smart-router
description: >
  This skill decides whether a user's question warrants full multi-model
  deliberation or can be answered well by a single model. Routes queries
  based on learned patterns from past deliberation outcomes stored in
  pattern memory. Triggers automatically before every deliberation when
  routing is enabled via /council-config. Uses heuristic fallbacks when
  pattern memory has insufficient data, and learned rules once 20+
  deliberations are logged.
version: 0.6.0
---

# Smart Router

Decide whether a query should go through full Council deliberation or be answered by a single model. The router starts conservative (deliberate on everything), applies heuristics for early routing, and transitions to learned rules once pattern memory has enough data.

## Routing Decision Flow

```
Incoming Query
    │
    ├── User explicitly called /deliberate → ALWAYS DELIBERATE (skip router)
    │
    ├── Router mode set to "always_deliberate" in config → DELIBERATE
    │
    ├── Router mode set to "always_shortcut" in config → SINGLE MODEL
    │
    └── Router mode is "learned" (default) →
            │
            ├── Step 1: Extract query features
            │
            ├── Step 2: Check pattern memory
            │     ├── No memory file → JEV ROUTING (Step 3), heuristics (Step 3b)
            │     ├── < 20 deliberations → JEV ROUTING (Step 3), heuristics (Step 3b)
            │     └── 20+ deliberations with routing rules → LEARNED ROUTING (Step 4)
            │
            ├── Step 3: Jev routing (calibrated)
            │     ├── Match against keyword/signal tables
            │     └── Return decision with heuristic confidence
            │
            └── Step 4: Learned routing
                  ├── Match query category against routing_model.rules
                  ├── If best rule confidence > 0.8 → follow rule
                  ├── If best rule confidence 0.5-0.8 → follow rule but flag as uncertain
                  └── If no confident match → DELIBERATE (exploration — learn from outcome)
```

## Step 1: Extract Query Features

Parse the incoming query and produce a features object. This is done once here and passed through the entire pipeline (deliberation-engine uses it for logging, pattern-memory stores it).

```json
{
  "length": 87,
  "category": "architecture_decision",
  "keywords": ["compare", "tradeoffs"],
  "complexity_signals": {
    "sub_question_count": 2,
    "has_conditional": false,
    "has_context_reference": true,
    "has_compound_conjunction": true
  },
  "estimated_protocol": "voting"
}
```

**Category classification** — apply the rules from `references/routing-heuristics.md`:

| Category | Primary keywords | Protocol |
|----------|-----------------|----------|
| `architecture_decision` | compare, tradeoffs, pros cons, architecture, design pattern, migration | voting |
| `compliance_security` | STIG, CMMC, compliance, FedRAMP, NIST, audit, security, risk | consensus |
| `code_implementation` | implement, code, function, bug, error, fix, test, deploy, API | voting |
| `strategy_business` | strategy, market, pricing, positioning, competitor, growth, roadmap | voting |
| `creative_writing` | write, draft, blog, post, article, copy, headline, narrative | voting |
| `factual_lookup` | what is, define, how does, explain, meaning of, syntax for | consensus |
| `other` | No strong signal match | voting |

**Compound query detection** — look for conjunctions (and, but, or, vs, versus, compared to) joining distinct sub-questions. Compound queries lean toward deliberation regardless of category.

**Protocol selection** — reasoning queries get voting, knowledge queries get consensus. If the query is compound with mixed types, default to voting (larger accuracy gain).

## Step 2: Check Pattern Memory

Read `council-memory.json` from the workspace.

- **File not found:** Proceed to Step 3 (heuristic routing). Set `routing_source: "heuristic_no_memory"`.
- **File found, `deliberations.length` < 20:** Proceed to Step 3. Set `routing_source: "heuristic_learning"`. Include progress note: "Learning: {N}/20 deliberations logged."
- **File found, `deliberations.length` >= 20, `routing_model.rules` is empty:** Proceed to Step 3. Log a suggestion: "20+ deliberations logged — run `/council-config rebuild-router` to activate learned routing."
- **File found, `routing_model.rules` has entries:** Proceed to Step 4 (learned routing).

## Step 3: Jev Routing (Preferred)

Ask Jev the routing questions directly instead of matching keywords. One call, four
questions, roughly 100ms and a fraction of a cent, which matters because the router
exists to avoid spending four frontier calls on a query that does not need them. A
router that costs a frontier call defeats its own purpose.

```bash
python3 "${COUNCIL_PLUGIN}/scripts/jev_route.py" "<the user's query>" [--budget 0.05]
```

It returns the same feature shape Step 1 produces, plus `routing_source: "jev"`, the
calibrated probability behind each answer, and the token usage. Use it as the routing
decision.

The three confidence bands are applied inside the script, from Step 4b, but now over a
measured probability rather than a hand-picked one. Measured is not the same as exact:
on 160 BIG-Bench Hard items, Jev's answers stated at 0.9-1.0 (mean 0.98) were right 89%
of the time and its 0.8-0.9 answers 71% ([jev-skill calibration test](https://github.com/wuyoscar/jev-skill/blob/main/evals/CALIBRATION_RESULTS.md),
2026-09-20). The bands are routing policy, not a guarantee:

| `confidence` | Behavior |
|--------------|----------|
| > 0.8 | Follow the decision. |
| 0.5 – 0.8 | Follow it, `uncertain: true` is set, and the deliberation-engine notes it. |
| < 0.5 | `decision` is forced to `deliberate` and `exploration: true` is set. An uncertain route that deliberates produces an outcome the learned router can train on; one that shortcuts produces nothing and may be wrong. |

**A pick that nearly tied is not used.** `category` and `estimated_protocol` are kept only
when Jev's pick has at least 0.8 probability and leads the runner-up by at least 0.15
(XE-028). Otherwise the field comes back `null` and is named in `needs_review`. Fill each
`needs_review` field from Step 1's heuristic extraction and record that field's source as
heuristic; the rest of the Jev route stands.

**When Jev cannot answer**, the script exits 2 with `routing_source: "jev_unavailable"`
and a `why` naming every path it looked for the key in. No key, no network, or a
gateway error all land here. Fall through to Step 3b and record the routing source as
heuristic, so a later reader can tell a heuristic route from a calibrated one. The
script never guesses a route it did not get an answer for.

The key resolves the way DR-010 resolves the OpenRouter key: `AI_GATEWAY_API_KEY`,
then `AIGATEWAY_KEY_FILE`, then the vault's `aigateway.env` through the sandbox and
native Drive globs. `jev_route.py --where` prints which one answered.

## Step 3b: Heuristic Routing (Fallback)

Apply hard-coded rules when pattern memory is insufficient. These are intentionally conservative — they lean toward deliberation for ambiguous cases because every deliberation generates training data for the learned router.

**Decision table (evaluated top to bottom, first match wins):**

| Priority | Condition | Decision | Confidence | Reasoning |
|----------|-----------|----------|------------|-----------|
| 1 | Budget setting < $0.03 | `single_model` | 0.95 | Budget too low for deliberation |
| 2 | Query length < 20 chars | `single_model` | 0.7 | Too terse for meaningful deliberation |
| 3 | Category is `factual_lookup` AND no compound conjunctions | `single_model` | 0.75 | Simple factual — one model suffices |
| 4 | Category is `code_implementation` AND no decision keywords | `single_model` | 0.65 | Deterministic code task — deliberation unlikely to add value |
| 5 | Keywords include "compare", "tradeoffs", "pros and cons" | `deliberate` | 0.9 | Explicit comparison request |
| 6 | Keywords include "should I", "which is better", "best approach" | `deliberate` | 0.85 | Decision query |
| 7 | Query length > 100 AND sub_question_count >= 2 | `deliberate` | 0.8 | Complex multi-part query |
| 8 | Category is `architecture_decision` or `strategy_business` | `deliberate` | 0.8 | High-stakes reasoning |
| 9 | Category is `compliance_security` | `deliberate` | 0.8 | Accuracy-critical domain |
| 10 | Category is `creative_writing` | `deliberate` | 0.7 | Benefits from diverse perspectives |
| 11 | (no match — catchall) | `deliberate` | 0.5 | Uncertain — deliberate to learn |

**Model selection for single-model routing:** When heuristic routing decides `single_model`, select the preferred model:

- `factual_lookup` → Use the Analyst model (default: `openai/gpt-4o`)
- `code_implementation` → Use the Analyst model
- Budget-constrained → Use the cheapest model in the lineup (check `references/model-configs.md` cost table)
- All other single-model routes → Use the Strategist model (default: `anthropic/claude-sonnet-5`) as the general-purpose best performer

## Step 4: Learned Routing

When pattern memory has 20+ deliberations and the routing model has been built, use data-driven rules.

**4a. Match query category against rules.**

Read `routing_model.rules` from the memory file. Each rule has:

```json
{
  "condition": "category == 'architecture_decision'",
  "action": "deliberate",
  "confidence": 0.91,
  "sample_count": 8,
  "value_score": 0.78,
  "preferred_model": null
}
```

Find all rules where the condition matches the extracted query features. If multiple rules match (e.g., category match + keyword match), use the one with the highest confidence.

**4b. Apply confidence thresholds.**

| Rule confidence | Behavior |
|----------------|----------|
| > 0.8 | Follow the rule. High certainty. |
| 0.5 – 0.8 | Follow the rule but flag in output: `"uncertain": true`. The deliberation-engine should note this in the output so the user knows the router is still learning this pattern. |
| < 0.5 | Ignore the rule — default to deliberation. This is an exploration case; the outcome will strengthen or weaken the rule. |

**4c. Dynamic model selection.**

When the routing decision is `deliberate`, the router also recommends which models to include based on `model_performance.category_ranks`:

1. Read `model_performance` from the memory file
2. For the query's category, look up each model's average rank in `category_ranks`
3. **Exclude models that consistently underperform:** If a model's average rank in this category is >= 3.5 (out of 4), exclude it from the lineup and substitute the next-best available model from the large lineup (see `model-configs.md`)
4. **Promote strong performers:** If a model's average rank in this category is <= 1.3, recommend it as chairman pre-favorite (it will likely win peer review anyway, but this saves the user from seeing a predictable peer review)
5. Minimum 3 models for any deliberation — never exclude below this floor
6. Return the recommended lineup in `recommended_models`

When the routing decision is `single_model`:

1. Check if there's a `preferred_model` on the matched rule
2. If yes, use it
3. If no, find the model with the best `category_ranks` score for this query's category
4. If no category data exists, fall back to heuristic model selection (Step 3)

**4d. Self-preference penalty.**

Before finalizing model recommendations, check `model_performance.self_preference_rate` for each model. If a model's self-preference rate exceeds 20%, add a note in the routing output: `"bias_warnings": ["model X shows 23% self-preference rate — consider excluding from review rounds"]`. This doesn't auto-exclude (the user or the deliberation-engine decides), but it surfaces the signal.

## Step 5: Build Router Response

Assemble the final response object:

```json
{
  "decision": "deliberate",
  "confidence": 0.91,
  "reasoning": "Query matches architecture_decision pattern — deliberation adds value 78% of the time (8 samples)",
  "routing_source": "learned",
  "uncertain": false,
  "recommended_models": [
    "anthropic/claude-sonnet-5",
    "openai/gpt-4o",
    "x-ai/grok-4.3",
    "google/gemini-2.5-flash"
  ],
  "excluded_models": [],
  "recommended_protocol": "voting",
  "estimated_cost": 0.09,
  "bias_warnings": [],
  "query_features": {
    "length": 87,
    "category": "architecture_decision",
    "keywords": ["compare", "tradeoffs"],
    "complexity_signals": {
      "sub_question_count": 2,
      "has_conditional": false,
      "has_context_reference": true,
      "has_compound_conjunction": true
    },
    "estimated_protocol": "voting"
  },
  "learning_status": "Active — 34 deliberations, 6 routing rules, last rebuilt 2026-03-28"
}
```

**Single-model response variant:**

```json
{
  "decision": "single_model",
  "confidence": 0.87,
  "reasoning": "factual_lookup queries answered correctly by single model 87% of the time (5 samples)",
  "routing_source": "learned",
  "uncertain": false,
  "recommended_models": ["openai/gpt-4o"],
  "excluded_models": [],
  "recommended_protocol": null,
  "estimated_cost": 0.01,
  "bias_warnings": [],
  "query_features": { ... },
  "learning_status": "Active — 34 deliberations, 6 routing rules"
}
```

## Cost Estimation

The router estimates cost before the pipeline runs so it can enforce budget constraints:

- **Deliberation (medium):** ~$0.08-0.12 (4 models × 3 stages)
- **Deliberation (small):** ~$0.03-0.05 (2 models × 3 stages)
- **Deliberation (large):** ~$0.15-0.25 (6 models × 3 stages)
- **Single model:** ~$0.005-0.02 (1 call)

If the estimated cost exceeds the user's `--budget` setting, the router downgrades: large → medium → small → single model, until the estimate fits within budget. Log this downgrade in `reasoning`.

## Integration

The smart-router is called by the deliberation-engine **before Step 1 (Resolve Model Lineup)**. The deliberation-engine uses the router's response to:

1. Skip the full pipeline if `decision` is `single_model` (go to single-model shortcut)
2. Use `recommended_models` instead of the default lineup if provided
3. Use `recommended_protocol` to pre-select voting vs. consensus (can still be overridden by Step 3 classification)
4. Pass `query_features` through to Step 8 for pattern-memory logging
5. Display `bias_warnings` in the output if any
6. Show `learning_status` in the footer of the deliberation output

## Router Modes (configurable via /council-config)

| Mode | Behavior |
|------|----------|
| `learned` (default) | Full routing logic: heuristic fallback → learned rules when available |
| `always_deliberate` | Skip router entirely — every query gets full Council pipeline |
| `always_shortcut` | Skip router entirely — every query goes to single best model |

Set via: `/council-config set router learned|always_deliberate|always_shortcut`
