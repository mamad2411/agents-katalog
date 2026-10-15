---
name: consciousness-transfer
description: >
  Four-phase cognitive internalization methodology (感悟用破 Feel-Discover-Apply-Stress-test).
  Transforms structured knowledge entries into actionable cognitive skills through guided dialogue.
  四阶段认知内化方法论：通过引导式对话将结构化知识转化为可执行的认知技能。
  Use when the user wants to deeply learn a mental model, decision framework, or thinking pattern —
  not just read about it. 当用户想要深入内化一个思维模型、决策框架或认知模式时触发。
trigger: >
  User wants to internalize a cognitive pattern, describes a real-world dilemma
  seeking wisdom, or asks to deeply understand a thinking model.
  用户想内化一个认知模式、描述真实困境寻求智慧、或想深入理解一个思维模型。
  Keywords: 感悟用破, 认知内化, 思维模型学习, 意识体, 决策框架, thinking model,
  mental model, cognitive pattern, wisdom transfer.
---

# Consciousness Transfer: Four-Phase Internalization

> 将知识转化为能力的四阶段内化方法论 / A four-phase methodology for turning knowledge into skill

## When to Use / 何时触发

Activate this skill when the user:
- Provides a structured knowledge entry (YAML or file reference)
- Describes a real-world dilemma and seeks a thinking framework
- Wants to deeply internalize a mental model or decision framework
- Uses phrases like: "帮我内化这个模型", "我想学这个思维方式", "用感悟用破方法论", "I want to internalize this", "teach me this model deeply"

Do NOT activate for:
- Simple factual questions ("什么是兼听则明？")
- Quick lookups or summaries
- Code-related tasks

## Input

Provide a structured knowledge entry in one of three ways:

1. **Inline YAML** — paste the knowledge entry directly in the conversation
2. **File reference** — point to a YAML file (e.g., `references/tang_taizong_decision.yaml`)
3. **Situation description** — describe your real-world dilemma; the skill will match it to a relevant entry

Bundled examples are available in [`references/`](./references/):
- `tang_taizong_decision.yaml` — Tang Taizong's decision framework (唐太宗兼听则明)
- `munger_multimodel.yaml` — Charlie Munger's latticework of mental models

Provide a structured knowledge entry (inline or from a file):

```yaml
title: "Short label (≤10 chars)"
description: "2-4 sentence explanation of this cognitive pattern"
mental_model:
  - "Step 1: actionable instruction"
  - "Step 2: actionable instruction"
  - "Step 3: actionable instruction"
context_trigger: "What scenario activates this model"
decision_tree:
  "Condition A": "Action 1"
  "Condition B": "Action 2"
modern_parallel: "A concrete modern-life scenario where this applies"
counter_example: "A specific case where this model failed"
effectiveness: "effective | mixed | destructive"
confidence: 0.85
source_text: "Original source material (if applicable)"
source_citation: "Source reference (if applicable)"
```

### Field Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Short label for the pattern |
| `description` | Yes | Plain-language explanation |
| `mental_model` | Yes | Actionable steps (array, ≥3 steps) |
| `counter_example` | Yes | When/where this model fails (≥20 chars) |
| `context_trigger` | No | Scenario that activates this model |
| `decision_tree` | No | If/then structured logic |
| `modern_parallel` | No | Modern life parallel scenario |
| `effectiveness` | No | effective / mixed / destructive |
| `confidence` | No | 0.0-1.0 credibility score |
| `source_text` | No | Original source material |
| `source_citation` | No | Source reference |

---

## Flow

### Phase 0: Context Collection & Pattern Matching

If the user describes a real-world situation instead of providing a knowledge entry, collect context first.

**Step 1: Understand the user's situation**

Ask 2-3 of these (not all):
- What specific situation are you facing? (The more concrete, the better)
- What are you most uncertain about in this situation?
- What options have you already considered?
- How much time pressure are you under? (days / weeks / months?)

**Step 2: Match to a knowledge entry**

If you have access to a knowledge base, search for entries relevant to the user's situation. Present 2-3 most relevant entries (title + one-line description) and let the user choose.

If the user provides a knowledge entry directly, skip to Phase 1.

---

### Phase 1: Feel — Story Immersion 感

**Goal**: Let the user emotionally enter the context before introducing any theory.

**How to execute**:

1. Read the knowledge entry's `source_text`, `source_citation`, and any related context.

2. Tell the story as a narrative:
   - First the **dilemma**: What situation was the person in? What pressure were they under?
   - Then the **choice**: What decision did they make? What alternatives existed?
   - Finally the **outcome**: What happened? What was the cost?
   - Do NOT name the "thinking model" in the story — let the user feel it.

3. After the story, ask:
   > "Why do you think they did it that way? If you were in their shoes, what would you have done?"

**Constraints**:
- The story must be grounded in `source_text` — do not fabricate details.
- If `confidence < 0.7`, state upfront: "The historical record on this is disputed."
- Use modern language for narration; preserve original text for key quotes.

---

### Phase 2: Discover — Socratic Guided Discovery 悟

**Goal**: Guide the user to articulate the model's core logic themselves, through progressive questioning.

**How to execute**:

1. Read the entry's `mental_model`, `decision_tree`, and `context_trigger`.

2. Design 3-4 progressive questions, from concrete to abstract:
   - **Q1 (Concrete)**: Return to a specific moment in the story — "At that point, what information did they have? Which information did they focus on?"
   - **Q2 (Pattern)**: Guide discovery of the pattern — "Did you notice? Every time they made a decision, they did the same thing first. What was it?"
   - **Q3 (Abstract)**: Distill the model — "If you wrote this method as a step-by-step checklist, what would it look like?"
   - **Q4 (Boundary)**: Explore failure conditions — "Under what circumstances would this method not work?"

3. Feedback strategy after user answers:
   - Close to the core logic: affirm + add details
   - Off track: redirect with a counter-question ("What if...?")
   - Stuck: give a hint (one branch from `decision_tree`), then ask again

4. After guided discovery, present the complete model:
   - `title` + `description` (one-line definition)
   - `mental_model` (step checklist)
   - `context_trigger` (when to use)
   - `decision_tree` (if/then logic)

**Constraints**:
- Questions must be grounded in the actual knowledge entry — do not invent questions.
- Do not give too much information at once — advance one step at a time.
- If the user already understands (accurate answers), accelerate and skip ahead.

---

### Phase 3: Apply — Transfer Practice 用

**Goal**: Have the user apply the model to their own real situation, bridging "understanding" and "ability."

**How to execute**:

1. Return to the user's real-world scenario (from Phase 0), or ask:
   > "What specific situation do you have right now where you could try this method?"

2. Guide the user to analyze their situation using `mental_model` steps:
   - What does Step 1 look like in their scenario?
   - Step 2?
   - Which branch of `decision_tree` matches their situation?

3. If the user has no specific scenario, use `modern_parallel` as a practice scenario:
   > "Imagine you're the person in this scenario. What would you do? Walk through the steps one by one."

4. After the user answers, cross-check:
   - Against `decision_tree`: Does their reasoning path match?
   - Against `counter_example`: Are they falling into a historical pitfall?
   - If there's a deviation, point it out without negating — ask: "If the result were X, which step do you think went wrong?"

5. Deliver an **action checklist**:
   - 1-3 specific things the user should do in their own situation
   - Each item maps to a model step
   - Expected resistance (from `counter_example`)

**Constraints**:
- Must land in the user's real scenario — no staying theoretical.
- If the user's scenario doesn't fit this model, be honest and suggest a different one.
- If `effectiveness` is "destructive", warn strongly.

---

### Phase 4: Stress-test — Failure Boundary Exploration 破

**Goal**: Help the user understand the model's boundaries and failure conditions. Avoid "when you have a hammer, everything looks like a nail."

**How to execute**:

1. Read `counter_example` and `effectiveness`.

2. Tell the counter-example story: How did this model fail historically?

3. Ask 1-2 stress-test questions:
   - "If your opponent also knew this model, how would they counter it?"
   - "Under what conditions would this model's assumptions completely break down?"
   - "What premise does this model depend on most? What if that premise changed?"

4. Guide the user to summarize:
   - What are the **applicable boundaries** of this model?
   - When should they **switch to a different model**?
   - What **meta-lesson** can be learned from this model's failure?

5. Present the final **Usage Manual**:
   - Model name + one-line definition
   - Applicable scenarios
   - Operation steps (`mental_model`)
   - Decision logic (`decision_tree`)
   - Failure signals (when to stop using it)
   - Alternative patterns (recommend 1-2 related entries)

**Constraints**:
- Counter-example must come from `counter_example` — do not fabricate.
- If `effectiveness` is "destructive", focus on "why it's harmful" rather than "where the boundaries are."
- The Usage Manual is the core deliverable of the entire session.

---

### Closure: Internalization Confirmation

After all four phases, do an internalization check:

1. Ask: "In your own words, describe the core of this model in one sentence." (Tests true understanding)
2. Ask: "When do you plan to use it for the first time?" (Tests transferability)
3. If the answer is accurate and specific, mark the entry as "internalized."
4. If the answer is vague or inaccurate, return to Phase 2 for re-guidance.

Finally, recommend 1-2 related knowledge entries as "next to learn."

---

## Output

A complete consciousness-transfer session produces:

1. **Situation matching report**: Which entries matched the user's scenario + why
2. **Narrative**: Story grounded in `source_text` (with original quotes)
3. **Usage Manual**:
   - Model name + one-line definition
   - Applicable scenarios
   - Operation steps (`mental_model`)
   - Decision logic (`decision_tree`)
   - Failure signals (from `counter_example`)
   - Alternative patterns (related entries)
4. **Action checklist**: 1-3 specific things to do
5. **Internalization confirmation**: User's own description + planned first application

---

## Notes

### Teaching Principles 教学原则

- **Lead with story, not theory** (先感后理): Always tell the story first. Never open with "This model is..."
- **Guide, don't lecture** (引导而非灌输): Use questions to lead the user to discover the answer themselves.
- **Land in reality** (落到真实): Phase 3 must connect the model to the user's actual situation.
- **Honestly mark boundaries** (诚实标注边界): Every model has failure conditions. Don't idolize any wisdom.
- **Respect the user's pace** (尊重节奏): If they understand, accelerate. If confused, slow down.

### Four-Phase Dependencies 四阶段依赖关系

- Phase 1 (Feel) provides the emotional anchor for Phase 2 (Discover)
- Phase 2 (Discover) provides the cognitive framework for Phase 3 (Apply)
- Phase 3 (Apply) provides the practical foundation for Phase 4 (Stress-test)
- Exception: If the user explicitly says they already understand a phase, you may briefly summarize it.

### Quality Gate 质量门控

Before presenting a knowledge entry to the user, verify:
- `mental_model` has ≥3 non-empty steps
- `counter_example` is ≥20 characters
- If `confidence > 0.7`, there should be a credible `source_citation`
- If any of these fail, note the weakness to the user.

### Brand 品牌

This skill is part of the **Emperor Cognition** (帝王认知体) project — a system that extracts transferable cognitive patterns from Chinese imperial history. The four-phase methodology (感悟用破) is inspired by Chinese classical education traditions: 记 (memorize), 悟 (comprehend), 用 (apply), 化 (internalize).
