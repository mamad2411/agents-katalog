---
name: cognitive-architecture-review
description: Use when an AI system already exists or is half-designed and you need to judge whether it is AI-native or a dressed-up wrapper. Reach for it when a founder says "is this actually AI-native", "audit my architecture", "why does it feel fragile", "an investor will run the Remove-the-AI test on us", "the agent does everything", "we bolted memory on later", "where is our moat", or a prototype demos well but you cannot say what compounds. Produces a four-pillar scorecard (Brain, Memory, Planning, Tools), the single weakest link, a severity-by-effort fix list, and a verdict on whether the system survives having its AI removed. Run after architect-before-code, before agentic-build-loop.
stage: architect
function: system
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Cognitive Architecture Review

A system that demos well tells you almost nothing. The demo runs on the happy path, with the founder
steering, before any of the load lands. The question that decides whether you have a company is
quieter: strip the AI out, and does anything of value remain? Most "AI products" survive the removal,
which is the precise reason they get cloned and never command an AI-native price. This skill audits
what you already built, names the pillar holding it up by luck, and finds the loop that should make
it yours.

## The method

Score the four pillars, find the missing loop, then run the Remove-the-AI test on the whole design.
Full rubric, worked audit, and anti-patterns: [`references/review-rubric.md`](references/review-rubric.md).

### Step 1: Score each pillar against the rubric

Walk the system and grade each pillar 0 to 3 (absent, bolted-on, present, load-bearing). Use the
red-flag column in the rubric to catch the pillar that is present on the slide and absent in the code.

| Pillar | The question that scores it | Common red flag |
|--------|-----------------------------|-----------------|
| Brain | Which model reasons, and what is the cheaper fallback for bulk or failure? | One frontier model on every call, no fallback, no eval |
| Memory | What does the system know that the model does not? | Memory is the context window; nothing persists between sessions |
| Planning | How does it decide its moves, in order, before acting? | One mega-prompt does retrieval, reasoning, and acting at once |
| Tools | Which actions reach the world, and what is each blast radius? | Tool calls with no guardrail on the irreversible ones |

### Step 2: Find the closed loop, or prove there is not one

Point to the single line where a customer's use this week makes the product measurably better next
month. Trace it: use to capture to data to a sharper product. If you cannot draw that return arrow,
record it as the headline finding. No loop means no flywheel means no moat, however good the pillars.

### Step 3: Run the Remove-the-AI test on the whole design

Mentally delete every model call. If the product still does its core job, you graded a feature, not a
company. Write the one-sentence verdict: AI-native (collapses without intelligence) or wrapper
(survives removal). This verdict outranks any individual pillar score.

### Step 4: Prioritise the fixes by severity against effort

Place each finding on the grid in the rubric. Fix the load-bearing pillar with the worst score first.
A missing closed loop is always severity-high, whatever it costs to build.

## Output

- A filled **four-pillar scorecard** with a 0 to 3 grade and evidence for each pillar.
- The **single weakest link** named, plus the **closed-loop diagnostic** (present, weak, or absent).
- A **severity-by-effort fix list**, top item first, and a one-line **AI-native or wrapper** verdict.
- Next: feed the fix list into `agentic-build-loop`, or back to `architect-before-code` if a pillar is absent.

## Constraints

- Do not grade the pitch deck. Grade what the code and the data actually do; a pillar on a slide is a zero.
- The God Agent is a failure, not a feature. One agent doing Brain, Memory, Planning, and Tools at once scores low on every pillar; say so.
- Apply the Remove-the-AI test last and let it overrule a flattering pillar average. A high-scoring wrapper is still a wrapper.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test) ·
[data flywheel](../../dictionary/07-ai-native-business.md#data-flywheel) ·
[AI-native vs wrapper](../../dictionary/07-ai-native-business.md#ai-native-vs-wrapper) ·
[the God Agent](../../dictionary/04-agentic-patterns.md#the-god-agent-anti-pattern)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my lead systems engineer running an architecture audit. Do not flatter the design.
My product: [ONE_LINER]. Domain: [DOMAIN]. Here is how it works today: [DESCRIBE_THE_SYSTEM].

Audit it against the four pillars. Grade each 0 to 3 (absent, bolted-on, present, load-bearing)
and quote my own description as evidence:
1. Brain: which model reasons, and what cheaper fallback covers bulk or failure?
2. Memory: what does the system know that the model does not, and does it persist between sessions?
3. Planning: how does it decide its moves, in order, before acting, and where does a human approve?
4. Tools: which actions reach the world, and what is the worst case if each misfires?

Then: trace the ONE closed loop where a customer's use this week makes the product better next month.
If you cannot find it, tell me I have a wrapper and say so as the headline finding.

CONSTRAINTS: grade the system as described, not as I wish it were; a pillar I only assert is a zero.
Flag the God Agent if one component does everything. Run the Remove-the-AI test last and let it
overrule a good average.

OUTPUT: the four-pillar scorecard with evidence; the single weakest link; the closed-loop verdict
(present/weak/absent); a fix list sorted by severity against effort; and one next action.
```
