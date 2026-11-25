---
name: design-the-mva
description: Use when a founder is about to build the first version and is piling features instead of proving one loop - "what's my MVP", "what should I build first", "scope this down", "let's add X too", "the demo works, ship it", "which feature first", "this is our biggest use case so start there", or they are scoping the highest-value highest-risk job because it impresses. Produces a Minimum Viable Agent: the one Goldilocks task (high-volume, guideline-based, low-risk), the closed loop it proves, the single high-risk hypothesis, and a bounded self-healing fallback. Skill before: a feature pile that demos. After: one experiment that can come back no.
stage: ship
function: product
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Design the MVA

The cheapest thing in your company is now a feature. You describe one in a sentence and it works by lunch, which is exactly the trap dressed as a gift. So founders pile up panels and integrations and call it a product, while the one question that decides whether the company lives goes untested: will a real person let a machine own the job the whole thing depends on. Ship the smallest agent that proves that loop, not the feature pile that flatters you.

## The method

Full method, the Goldilocks scoring filters, a worked MVA scope, anti-patterns, and a copyable
template: [`references/mva-method.md`](references/mva-method.md).

### Step 1 - Find the Goldilocks task
Pick one task that is high-volume, guideline-based, and low-risk, all three at once. High-volume, so the loop runs often enough to save real time and throw off real signal. Guideline-based, so there is a knowable right answer a human can check at a glance. Low-risk, so a wrong answer is an annoyance and not a harm. Your highest-value task is usually your highest-risk one. Write that on the roadmap for later. Earn trust on the boring task next to it first.

### Step 2 - Define the Minimum Viable Agent
The Minimum Viable Agent is the smallest agent that proves the intelligence loop closes: task in, agent acts, outcome out, human accepts or corrects, the system records the choice. The deliverable is not a screen. It is a working loop around one task, and it can be thin on the surface: a text box, an email reply, a row someone approves. The intelligence is the product.

### Step 3 - Name the one high-risk hypothesis it tests
State the trust bet so it can come back no: users in role R, facing task T, will accept the agent's output without redoing it at least M percent of the time. One hypothesis, not a multi-feature dashboard. If a proposed build does not map to a bet that can fail, it is scope creep, however reasonable it sounds.

### Step 4 - Add the self-healing fallback
Decide in one bounded sentence what the agent does when it is unsure or the model fails: retry a set number of times, switch to a backup, then drop to a fixed non-AI path and escalate to a named human. A pilot user who hits a dead end twice goes back to doing it by hand. You lose them on reliability, not capability.

## Output

- The MVA spec: the one Goldilocks task, the loop it proves, the single high-risk hypothesis, and the bounded fallback.
- Run [`measure-ai-native-pmf`](../measure-ai-native-pmf/SKILL.md) next, once the loop is live and the hypothesis has a clean yes or no.

## Constraints

- One task, not ten. The unit of work is an experiment, not a feature.
- Pick the Goldilocks zone, not the hardest problem. The first wrong answer on a high-risk job detonates the trust your whole roadmap needs.
- The MVA must prove the loop or it is just a feature. Run the Remove-the-AI test: take the model out, and if the loop still works, you scoped a feature.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[Minimum Viable Agent](../../dictionary/07-ai-native-business.md#minimum-viable-agent-mva) ·
[the Goldilocks zone](../../dictionary/07-ai-native-business.md#the-goldilocks-zone) ·
[self-healing fallback](../../dictionary/04-agentic-patterns.md#self-healing-fallback) ·
[the Remove-the-AI test](../../dictionary/07-ai-native-business.md#the-remove-the-ai-test)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my AI-native product coach. My idea: [ONE_LINER]. Who it's for: [ICP]. Domain: [DOMAIN].
Help me write my Minimum Viable Agent in one sentence, in this exact shape:
"My first agent does [the single task] for [ICP], proving that [the loop], and when it fails it [the fallback]."
Rules:
1. The task must pass all three Goldilocks tests: high-volume (runs often), guideline-based (a
   knowable right answer a human checks at a glance), and low-risk (a wrong answer is an annoyance,
   not a harm). If my chosen task is my highest-value but highest-risk one, push back and tell me to
   pick the safe job next to it instead.
2. The loop must prove a real human hands a real job to the machine and keeps the result. If removing
   the AI leaves it still working, tell me I scoped a feature, not an agent.
3. The fallback must be bounded: retry a set number of times, then drop to a fixed answer and a named
   human. No infinite loops.
Don't flatter me. End with the ONE next action to build it.
```
