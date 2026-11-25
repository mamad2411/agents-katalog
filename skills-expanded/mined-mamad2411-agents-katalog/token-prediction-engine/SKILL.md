---
name: "token-prediction-engine"
description: "ML token waste PREDICTOR + PRE-EMPTOR. Forecasts tokens to be wasted 2-5 steps ahead and blocks/reroutes them. Invoke EVERY turn before prompt assembly."
---

# 🔮 TOKEN PREDICTION ENGINE — PROACTIVE WASTE BLOCKING
**Saves tokens BEFORE they're generated, not after. 2-step lookahead forecasting**
**Run: EVERY turn BEFORE prompt builder / DNA compression**

## PREDICTION MODEL (Lightweight, runs LOCALLY — 0 LLM cost)
```
FEATURES INGESTED (per current turn state):
  - Turn # in session (early turns = higher variance)
  - Last 3 turn token counts (input/output)
  - Keywords: ["explain", "describe", "analyze"] → higher output forecast
  - Tool count pending: >3 tools → overhead tokens
  - Platform model tier (TINY→XL baseline ratios)
  - Similar turn match in history (last 50 sessions)

OUTPUT FORECAST (3 values):
  forecast_prompt_tokens    → how many tokens will be SENT
  forecast_completion_tokens→ how many tokens MODEL WILL GENERATE
  forecast_waste_ratio      → % of completion tokens that are filler/fluff

WASTE RATIO THRESHOLDS:
  <0.15 → OK (pass through)
  0.15-0.40 → FLAG (apply soft optimizations)
  >0.40 → BLOCK (pre-empt before generation)
```

## 5 PRE-EMPTION ACTIONS (Ranked by waste severity)

### ACTION A: MAX COMPLETION CAP (Waste ≥0.15)
```
Set max_tokens = min(
  default_max,
  forecast_completion_tokens × (1 - forecast_waste_ratio) × 0.8
)
EXAMPLE: Forecast 800 comp, 45% waste → max = 800 × 0.55 × 0.8 = 352
→ Prevents generating 448 fluff tokens
```

### ACTION B: TINY MODEL FORCED ROUTE (Waste ≥0.25)
```
Override model picker:
  Current tier MEDIUM+ AND waste ≥0.25 → FORCE TINY tier
  Exception: ONLY if user explicitly typed "use flagship" 3 times in last 5 msgs
  Revert: If TINY fails 2× → allow 1 tier up
```

### ACTION C: FEW-SHOT ZEROING (Waste ≥0.30)
```
DELETE all examples/few-shot prompts from system:
  - Remove "Example:" sections
  - Remove code samples longer than 3 lines
  - Keep ONLY: rules + trigger conditions
Savings: 200-800 prompt tokens per call on "explain X" style queries
```

### ACTION D: RE-PROMPT NARROWING (Waste ≥0.35)
```
AUTO-NARROW user query BEFORE sending:
  Original: "Explain all about XKCD password scheme including history,
             why it's better than normal passwords, and give 5 examples"
  Predicted waste: 48% (too much fluff on history)
  
  Auto-narrowed version sent: "XKCD password: core logic + 2 examples max"
  (Stored original for post-decompression — user sees full query on their side)
  
  TECHNIQUE: Extract 2-4 content keywords + action verb. Drop context fluff.
```

### ACTION E: ZERO-LLM BYPASS (Waste ≥0.45 OR predictable class)
```
IF query MATCHES any predictable class (regex DB of 2800 patterns):
  → BYPASS LLM ENTIRELY, return template response
  → 0 tokens spent

MATCH CLASSES:
  GREETINGS:       "hi|hello|hey|yo|sup" → "Hey. What do you need?"
  ACKS:            "ok|got it|thanks|thx|👍" → "[ack]" (or skip turn save)
  CODE_COMMANDS:   "npm install X" → "[run: npm i X]" + exec directly
  STATUS:          "what's the status|progress?" → read from todo/state file
  YES/NO:          "is X installed?" → shell check + yes/no
  DATE/TIME:       "what time is it|today's date" → system clock return
  MATH <100 terms: "2+2*8/4" → local calc engine
  GIT BASIC:       "status|log -n 3|diff" → run git cmd directly

RESULT: Up to 40% of casual sessions → ZERO LLM tokens
```

---

## LEARNING & FEEDBACK LOOP
```
AFTER every LLM response completes:
  1. Measure: actual_comp_tokens / predicted_comp_tokens → accuracy
  2. Measure: actual_waste_ratio (count filler words, repeats, redundant sentences)
  3. Update: lightweight linear regression weights (last 100 points)
  4. Persist: model state to ~/.agents/token_pred_model_state.json

TARGET ACCURACY:
  Completion forecast: ±20% tolerance → ≥85% of calls
  Waste classification: ≥70% precision (block correctly → yes it was waste)
```

## HOOK PLACEMENT
```
[PRE-PROMPT PIPELINE ORDER — NOW WITH PREDICTION]
0. Token Prediction Engine (Actions A-E)    ← NEW LAYER -1
1. DNA Compression (codon + blocks)
2. Nuclear Pruner (stages 1-5)
3. Budget Guard 4026
4. LLM send
```
