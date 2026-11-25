---
name: exec-problem-solving
description: Apply 7 executive problem-solving frameworks used under pressure. Use when the user faces a business decision, recurring problem, strategic crisis, or runs /ooda, /dmaic, /5whys, /premortem, /first-principles, /six-hats, or /decision-tree. Picks the right framework for the situation or runs the one requested. Source: stephanieshills.com.
---

# Executive Problem-Solving: 7 Frameworks

Seven decision and problem-solving frameworks used by executives. Each has a specific trigger — pick the one that matches the situation, or let the skill recommend.

---

## Framework Selection Guide

| Situation | Best Framework |
|---|---|
| Competitive crisis, market shift, urgent action needed | OODA Loop |
| Operational process that keeps failing or needs improvement | DMAIC |
| Recurring problem with unknown root cause | Root Cause / 5 Whys |
| New initiative or product launch — what could go wrong? | Pre-Mortem |
| Conventional solutions aren't working | First Principles |
| Team misaligned, groupthink risk, complex decision | Six Thinking Hats |
| High-stakes decision with multiple options and uncertainty | Decision Tree |

---

## /ooda — OODA Loop (John Boyd)

Speeds up decisions and action in fast-changing situations.

**Steps:**
1. **Observe** — Gather real-time data and facts. What is actually happening right now?
2. **Orient** — Analyze context and past lessons. What does this mean given our history?
3. **Decide** — Choose best response now from available options.
4. **Act** — Execute and test results. Move faster than the situation develops.

**Prompt template:**
```
Apply the OODA Loop to [situation/crisis]. 
Observe: What are the hard facts right now — data, signals, customer behavior?
Orient: What past experience or context is relevant? What biases might distort our read?
Decide: What are the 2–3 response options? Which has the best risk/speed trade-off?
Act: What specific action do we take in the next 24–72 hours?
Give me a decision memo I can share with my team.
```

---

## /dmaic — DMAIC Framework (Six Sigma / Motorola)

Data-driven method to pinpoint issues, measure performance, and test fixes.

**Steps:** Define → Measure → Analyze → Improve → Control

**Prompt template:**
```
Apply the DMAIC framework to [process/problem].
Define: What exactly is the problem? What is in scope? What does success look like?
Measure: What data do we need? What does current performance look like vs target?
Analyze: What are the root causes? Use data, not guesses.
Improve: What solutions address the root cause? Test them.
Control: How do we lock in the improvement and prevent regression?
Structure this as a project brief I can take to my team.
```

---

## /5whys — Root Cause Analysis (Sakichi Toyoda)

Drill down 5× with "Why?" to reach the true cause, not the surface symptom.

**Prompt template:**
```
Apply the 5 Whys to [problem statement].
Start with the observable problem, then ask WHY 5 times in sequence.
At each level, challenge whether the answer is a symptom or a cause.
Stop when you reach a cause that is within our control to fix.
Output: the causal chain + the real root cause + recommended fix.
Do not stop at symptoms. The answer "because people don't follow the process" is itself a symptom — keep asking why.
```

---

## /premortem — Pre-Mortem Analysis (Gary Klein)

Assume the initiative fails. Work backward to prevent it.

**Prompt template:**
```
Run a pre-mortem on [initiative/launch/decision].
Assume it is now [date 6–12 months from now] and [initiative] has failed badly.
Step 1: Brainstorm every realistic reason it failed — operational, market, human, financial, competitive.
Step 2: Map each failure reason on a 2×2: Impact (Low→High) × Likelihood (Low→High).
Step 3: For each HIGH-impact + HIGH-likelihood risk: what is the mitigation we build in now?
Step 4: What are the 3 most dangerous risks no one is talking about?
Output as a risk register table + top 3 mitigation actions.
```

---

## /first-principles — First Principles Thinking (Aristotle / Elon Musk)

Break the problem to its foundational truths. Rebuild from there.

**Steps:**
1. Identify the problem you want to solve
2. Break it into its fundamental pieces — strip away assumptions
3. Question and challenge every assumption ("Is this actually true?")
4. Create a new solution from the ground up — ignore how it's always been done

**Prompt template:**
```
Apply first principles thinking to [problem/assumption].
Step 1: State the problem clearly.
Step 2: List every assumption embedded in how we currently approach this. Be exhaustive.
Step 3: Challenge each assumption: Is it physically/logically necessary, or is it just convention?
Step 4: What remains as bedrock truth that we cannot eliminate?
Step 5: Build the best solution starting only from those truths — ignore industry norms.
What solution emerges that existing players cannot copy because they're too invested in their current model?
```

---

## /six-hats — Six Thinking Hats (Edward de Bono)

Parallel thinking via 6 perspectives to prevent groupthink and unlock balanced team decisions.

**The 6 Hats:**
- 🤍 **White Hat** — Facts only. Data, information, what we know and don't know.
- ❤️ **Red Hat** — Feelings. Gut reactions, intuitions, emotions — no justification needed.
- 🖤 **Black Hat** — Risk. Critical judgment, what can go wrong, downside.
- 💛 **Yellow Hat** — Benefits. Optimism, value, why this could work.
- 💚 **Green Hat** — Creativity. New ideas, alternatives, possibilities.
- 💙 **Blue Hat** — Process. Managing the thinking itself, next steps, summary.

**Prompt template:**
```
Apply the Six Thinking Hats to [decision/topic].
White Hat: What facts do we have? What information is missing?
Red Hat: What are the gut reactions and emotional responses from stakeholders?
Black Hat: What are all the ways this could fail or cause harm?
Yellow Hat: What is the best case? What genuine value does this create?
Green Hat: What creative alternatives exist? What hasn't been tried?
Blue Hat: What is the recommended next step given all the above?
Present each hat as a section, then synthesize a recommendation.
```

---

## /decision-tree — Decision Tree Analysis (J. Ross Quinlan)

Map choices, probabilities, and outcomes visually for high-stakes decisions.

**Prompt template:**
```
Build a decision tree for [high-stakes decision with uncertainty].
Start at the Decision Point.
For each option (2–4 max), list:
- The action/choice
- The key uncertain outcomes (2–3 per branch)
- Estimated probability of each outcome (must sum to 100% per branch)
- Expected value or impact (financial or strategic) for each outcome

Calculate the Expected Value for each major option.
Identify which branch has the best risk-adjusted outcome.
Flag which assumptions, if wrong, would flip the recommendation.
Output as a structured table + written recommendation.
```

---

## Auto-select mode

If the user describes a problem without specifying a framework, diagnose and apply:
1. State which framework fits best and why in one sentence
2. Run that framework's prompt against the problem
3. Offer the next-most-relevant framework as an alternative
