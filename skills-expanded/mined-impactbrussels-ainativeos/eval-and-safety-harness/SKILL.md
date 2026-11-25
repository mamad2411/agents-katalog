---
name: eval-and-safety-harness
description: Use when a founder says "is this safe to ship", "it hallucinated to a customer", "it made up a citation", "we need clinical/food-safety/financial guardrails", "how do I evaluate this", "the demo worked but I'm scared to launch", "what if it's wrong about a dose", or is in health, food, or finance and an answer could walk out into a person. Triggers on eval set, golden cases, adversarial cases, regression, critic/judge, LLM-as-judge, deterministic fallback, human-on-the-loop, red-team, release gate. Produces a binary safety rubric, a critic/judge pairing, named fallbacks, and the human boundary. Skill turns a stacked-deck demo into a gated harness; without it, the wrong answer reaches a user unchecked.
stage: trust
function: safety
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Eval and Safety Harness

A demo is not evidence. You picked the input, the moment, the clean case, and the model performed because you stacked the deck. In hard mode that demo is a liability with a clean interface: the wrong answer does not stay on the screen, it walks out into a person. Trust here is engineered before you earn the right to act on a human, never assumed after. This skill builds the harness that turns generation into something a tired clinician can sign their name under.

## The method

Take one real feature, the one where being wrong costs the most, and build these five layers around
it. Full method, how to design the eval set, the release gate, a worked harness, anti-patterns and a
copyable template: [`references/eval-harness-method.md`](references/eval-harness-method.md).

1. **Write the safety rubric.** Turn "is it safe" into pass/fail checks a machine can enforce: every claim cites a real, resolvable source; every number traces to an input; uncertain claims are flagged uncertain; confidence below a threshold refuses rather than guesses. Map each check to a pillar of [the six-pillar trust substrate](../../dictionary/06-evaluation-and-safety.md#the-six-pillar-trust-substrate). If you cannot write five sharp binary checks, your safety bar is still a vibe.

2. **Pair a generator with a separate judge.** One agent drafts. A second, running fresh with its own clean context and the written rubric, scores that draft before anything reaches a human. An author cannot proofread their own typo, and a model defending the context that produced its answer is the same blind spot amplified. Everything turns on the rubric: "is this good?" passes everything; the sharp check catches the hallucinated citation every run.

3. **Set the human-on-the-loop boundary.** Draw the line: what agents execute unattended, and what a human must review or approve. Put human-in-the-loop on the irreversible (a dose, a large trade, a product released to market). Put human-on-the-loop on everything else, where the human reviews the exceptions queue, not every output. Too low and you have built an expensive autocomplete; too high and a bad outcome reaches a person before anyone notices.

4. **Build the deterministic fallbacks.** Name the non-AI path the system takes when confidence is low or the question touches a dose, an allergen, or a threshold. Not a retry, not a better model: a fixed rule, a conservative default, an honest "I cannot assess this, escalating now." A model with no fallback does not stop on a case it does not understand. It answers anyway, confidently, because that is what it was trained to do.

5. **Red-team it.** Manufacture the unhappy path in a lab, where the only thing harmed is a test case. Generate the ambiguous prompts, the adversarial phrasings, the plausible study that does not exist, and confirm the fallback actually fires before a user is affected. The deliverable is the list of cases where the model produced something unsafe and nothing caught it. Each one is a person you would have harmed in production. Fix them, then re-run, because every new model version fails in new ways.

## Output

- The safety rubric (five binary checks mapped to the trust pillars).
- The critic and judge pairing, with the judge enforcing the rubric pre-output.
- The deterministic fallbacks, each named in one sentence.
- The human-on-the-loop boundary: what executes versus what a human approves.
- Next: run `design-the-mva` to ship the smallest agent that proves the loop, with this harness wrapped around it.

## Constraints

- Keep a human on the loop in sensitive domains; agents execute, humans set goals and review outcomes.
- Before any regulated workload, confirm in writing that each AI tool is in audit-log and compliance scope. No confirmation, no access.
- Never ship autonomy before the fallback is real. Autonomy without a fallback is a single point of failure in a costume.
- This is not legal or medical advice. Confirm clinical, food-safety, or financial thresholds with a qualified professional.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[critic/judge pairing](../../dictionary/04-agentic-patterns.md#critic-judge-pairing) ·
[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl) ·
[deterministic fallback](../../dictionary/06-evaluation-and-safety.md#deterministic-fallback) ·
[the six-pillar trust substrate](../../dictionary/06-evaluation-and-safety.md#the-six-pillar-trust-substrate) ·
[hallucination](../../dictionary/05-failure-modes.md#hallucination)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my AI safety engineer. My product: [ONE_LINER]. Domain: [DOMAIN]. The one feature where being
wrong costs the most: [FEATURE]. Help me make it safe before it touches a user.
1. Draft a safety rubric: five pass/fail checks a separate "judge" can hard-fail my output on (e.g.
   every claim cites a real source, every number traces to an input, low confidence refuses).
2. Name the deterministic fallback for [DOMAIN]: the non-AI, predictable path the system takes when
   confidence is low or the question touches a dose, allergen, or threshold. Not "retry the model".
3. Draw the human-on-the-loop line: what an agent can do unattended versus what a human must approve.
Don't reassure me. If a check is vague or the fallback is missing, say so. End with ONE next action I
should take today.
```
