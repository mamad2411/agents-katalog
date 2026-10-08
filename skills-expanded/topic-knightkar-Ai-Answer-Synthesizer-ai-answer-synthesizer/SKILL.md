---
name: ai-answer-synthesizer
description: Synthesize multiple AI responses into one clear, actionable answer with confidence-aware analysis. Use whenever a user pastes, references, or describes answers from multiple AI tools (ChatGPT, Claude, Gemini, Copilot, Perplexity, Grok, DeepSeek, etc.) and wants help making sense of them. Trigger on phrases like "I asked multiple AIs," "which answer should I follow," "combine these responses," "simplify these for me," "these AI answers are confusing," or any mention of comparing AI outputs. Also trigger when users paste multiple long text blocks that appear to be AI-generated responses, even without explicitly saying so. Use this skill even if only 2 responses are provided.
---

# AI Answer Synthesizer

Turn multiple AI responses into one clear answer with confidence-aware synthesis.

## What This Skill Adds

Without this skill, Claude summarizes. With it, Claude adjudicates.

The method:
1. Extract discrete claims from each response
2. Detect real consensus vs. vocabulary differences
3. Flag meaningful contradictions
4. Assess lone-claim risk (insight or hallucination?)
5. Score recommendations against the user's apparent skill level
6. Produce one recommended path with honest confidence

## Modes

### Quick Mode
Triggered by: short messages, urgency, overwhelm, or explicit request for brevity.

Output format:

**The answer:** [2-4 sentences]
**Confidence:** [High / Medium / Low] — [one-line reason]
**Do this next:** [one concrete step]

### Deep Mode (Default)
Triggered by: full pasted responses, "help me understand," or analytical questions.

Output format:

**The Short Answer**
[2-3 sentences. The verdict.]

**Confidence:** [High / Medium / Low] — [one-line reason]

**What They Agree On**
[Bullets. Only genuine consensus. No padding.]

**Where They Actually Disagree**
[Only real disagreements. For each: the split, which side is better supported, whether it changes the recommendation. If they mostly agree, say so and keep this to one line.]

**The Recommended Path**
[3-5 numbered steps. Concrete. Matched to user's skill level.]

**What to Ignore For Now**
[Advanced or premature suggestions the user doesn't need yet.]

**One Thing to Watch Out For**
[The single most important caveat or risk.]

## Method

Execute in order.

### Step 1: Identify the Real Question
The surface question often masks the actual need:
- "How do I build this?" → What's the easiest viable path?
- "Compare these" → Give me a recommendation, not a balanced report
- "Explain this" → I'm overwhelmed, translate this for me
- "Which is right?" → Give me a verdict with reasoning

Base the response on the real goal, not the literal phrasing.

### Step 2: Extract Claims
For each AI response, identify:
- Core recommendation (what it says to DO)
- Key claims (specific facts, tools, steps)
- Assumptions (skill level, budget, timeline it assumes)
- Caveats (warnings, risks, limitations)
- Complexity level (beginner / intermediate / advanced)
- Immediate next step

### Step 3: Build the Consensus Map
Classify each claim:
- **Strong consensus** — most responses support it → high confidence, lead with this
- **Partial consensus** — some support it → moderate confidence, include with note
- **Lone claim** — only one response makes it → flag for review (see Lone Claim Rules below)
- **Direct contradiction** — responses recommend incompatible actions → analyze which is better supported

### Step 4: Collapse Vocabulary Aliases
AIs frequently say the same thing with different words. Collapse these BEFORE reporting disagreements:
- prototype / MVP / proof of concept / first version
- deploy / host / ship / put it live
- API / integration / connecting services
- frontend / UI / the part users see

Only report a disagreement if the actual recommendations diverge, not just the terminology.

### Step 5: Assess Complexity Fit
Score each recommendation against the user's apparent situation:
- Do they sound technical or non-technical?
- Did they mention constraints (time, skill, budget)?
- Is the recommendation realistic for someone at their level?

The best answer for THIS user is not always the most technically impressive one — it's the one they can actually execute.

### Step 6: Synthesize
Combine into one recommended path. Be opinionated when evidence supports it. Present multiple options only when the choice genuinely depends on user context you don't have.

## Critical Thinking Rules

### The Popularity Trap (Anti-Consensus Bias)
If three AIs give a safe, generic answer and one gives a well-reasoned, specific insight, do NOT default to the majority. Consensus is a signal, not a verdict. A minority answer that is clearly better reasoned, better scoped to the user, or includes a critical caveat the others miss should be weighted accordingly.

Ask: Is the majority answer actually better, or just more common?

### The Hallucination Cascade
When synthesizing AI outputs, you risk amplifying errors from the source responses. Guard against this:
- If a specific factual claim appears in only one response AND is stated without hedging → treat with extra skepticism
- If multiple responses make the same dubious claim → that is shared training bias, not confirmation
- If a claim is critical to the recommendation, note the confidence level explicitly
- Never present a synthesis claim with more certainty than the source material warrants

### Complexity Is Not Quality
The longest, most detailed, most architecturally sophisticated answer is not automatically the best. For most users, the answer that gets them to a working result fastest is the best answer. Do not reward complexity for its own sake.

## Lone Claim Rules
When a claim appears in only one response:
- Do not automatically reject it
- Do not automatically trust it
- Assess: Is this a genuine insight, an unsupported speculation, a hallucination, or domain-specific nuance?
- If the lone claim materially changes the recommendation, call it out explicitly and state your confidence

## Confidence Rules
- **High:** Strong overlap across responses, no serious contradictions, recommendation fits the user well
- **Medium:** Useful consensus exists but there are real tradeoffs, incomplete inputs, or moderate uncertainty
- **Low:** Major conflicts, missing information, or high uncertainty about the right path

When confidence is limited, say why in one line. Do not bury uncertainty in hedging language — state it directly.

## Edge Cases

**Only 2 responses:** Still useful. Run the full method. Lower confidence appropriately.

**Responses mostly agree:** Say so immediately. Don't manufacture differences. Skip or minimize the disagreement section.

**One response is strong but too advanced:** Preserve the insight as a "future upgrade." Recommend the simpler version now.

**User is overwhelmed:** Shorten everything. One recommendation. Three steps max. Skip the analysis sections.

**Subjective topic:** Shift from "which is correct" to "which approach fits your goals." Frame as preference-matching, not fact-finding.

**User asks which AI is best:** Don't rank models globally. Evaluate each answer's quality for THIS specific question.

**Partial or messy inputs:** Work with what's available. Note gaps only when they meaningfully limit confidence.

## What Not to Do

- Summarize each response in sequence (book report, not synthesis)
- Present all options equally when evidence favors one
- Repeat the user's question back to them
- Add motivational filler or empty encouragement
- Produce 10+ step action plans when 4 steps would do
- Hide behind "it depends" when you have enough to recommend
- Assume the longest or most detailed response is the best
- Inflate weak agreement into "strong consensus"
- Strip away important caveats in the name of simplification
- Use fake precision (numbered confidence scores, percentage agreement)

## Tone

Write like a sharp, kind colleague who respects the user's time. Direct but warm. Confident but honest about uncertainty. The user should leave with more clarity than they arrived with — not more cognitive load.
