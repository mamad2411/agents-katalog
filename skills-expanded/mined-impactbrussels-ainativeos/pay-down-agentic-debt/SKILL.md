---
name: pay-down-agentic-debt
description: Use when an agent-built codebase has grown faster than anyone understands it and every change feels risky - when they say "the codebase is a mess", "I'm scared to touch this", "one fix broke three other things", "it worked when we built it", "we have a God Agent", "there's a ghost in the system", "tech debt is killing us", or a small prompt edit caused a regression three hops away. Produces a ranked debt ledger (interest x principal), the CACE-safe paydown order, and the eval gate each change must pass. Invoke after architect-before-code, with eval-and-safety-harness.
stage: build
function: engineering
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Pay Down Agentic Debt

In a machine-learning system, changing anything changes everything. The debt an agent leaves behind does not sit in one place and wait like the old kind; the intelligence at the centre is a learned thing, and a learned thing entangles whatever it touches. So a surgical, obviously correct fix in one corner degrades a model three hops away you would swear is unrelated, and you are debugging at midnight certain the system has a ghost in it. It does not have a ghost. It has agentic technical debt, and the founders who survive growth are the ones who rank it by interest rate and pay it down without breaking ten things to fix one.

## The method

Find it, rank it by interest, pay it down CACE-safe through the eval gate. Full framework: [`references/debt-method.md`](references/debt-method.md). Source: Handbook [Chapter 07](../../handbook/07-agentic-technical-debt.md).

### Step 1: Audit the repo for the six debts
Point your agentic-coding tool at the codebase and force it to find the categories below, not a vague "what's messy". An unranked list paralyses; a named taxonomy you can score.

| Debt category | What to grep for | Why it bites |
|---|---|---|
| Prompt sprawl | One mega-prompt; rules added per case | Maximum entanglement; nothing testable in isolation |
| Entangled context | A signal feeding more than one learned component | A fix here moves outputs you cannot predict |
| Untested paths | Code with no eval asserting on its content | You ship blind; silent failure has no alarm |
| God Agent | One agent doing many jobs in one context | Unauditable, unchangeable, brittle by construction |
| Missing evals | No held-out set, no eval suite at all | You cannot prove any change is safe, only hope |
| Dead retrieval / broken loop | A signal generated but never stored | The leak in the moat: thrown-away learning |

### Step 2: Score each item by interest x principal
Interest is how fast the debt compounds; principal is the cost to fix. Rank by interest first, always. See the scoring grid in references.

| Interest (rank highest first) | Score |
|---|---|
| Blocks data collection (a silently open loop, a dropped signal) | Highest |
| Blocks scaling (an architectural flaw growth will hit) | High |
| Risks a CACE regression (entangled, touches many learned parts) | Medium |
| Merely cosmetic (ugly code that works and never changes) | Lowest, leave it |

The debt that screams is rarely the debt that kills you. The quiet leak nobody is complaining about, the broken feedback loop, that is usually item one.

### Step 3: Pay it down CACE-safe, one thing at a time
Change one thing. Run the full eval. Measure. Keep or revert. Never bundle. The diff is not the blast radius; the eval is the only thing that knows what moved.

### Step 4: Gate every change on the eval suite
No paydown ships without passing the eval that protects the parts you did not touch. If you have no eval suite, that is your highest-interest debt; build it before you refactor anything.

## Output

- A **ranked debt ledger**: each item scored interest x principal, highest-interest at the top.
- The **safe paydown order**: which item first, and the one isolated change that pays it.
- The **eval gate** for each change: the assertion that proves you broke nothing downstream.
- Next: log the trade-offs you deferred via `capture-learning`; re-run this audit monthly.

## Constraints

- No big-bang refactor. Rewriting the God Agent in one swing is the faster mess, not the faster company. Extract one specialist, gate it, repeat.
- No fix without an eval. CACE means you cannot reason a change safe, you can only measure it. Trusting the green diff is how the regression ships.
- Pay the highest-interest debt first even when the ugly code is screaming. Especially then.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[CACE](../../dictionary/05-failure-modes.md#cace-changing-anything-changes-everything) ·
[agentic technical debt](../../dictionary/05-failure-modes.md#agentic-technical-debt) ·
[entanglement](../../dictionary/05-failure-modes.md#entanglement) ·
[eval](../../dictionary/06-evaluation-and-safety.md#eval) ·
[the God Agent](../../dictionary/04-agentic-patterns.md#the-god-agent-anti-pattern) ·
[infinite loop](../../dictionary/05-failure-modes.md#infinite-loop-runaway-agent)

## Copy-paste version

> For non-coders: paste into a coding tool with repo access (Claude Code, Cursor, Codex). For the ranking and plan alone, paste into any chatbot (Claude.ai, ChatGPT).

```
Act as my staff engineer doing an agentic-debt audit. My product: [ONE_LINER]. Domain: [DOMAIN].
The codebase was largely AI-generated and now every change feels risky.
1. Audit for six debts: prompt sprawl (one mega-prompt), entangled context (a signal feeding more
   than one learned component), untested paths (code no eval checks), a God Agent (one agent doing
   many jobs), missing evals (no held-out test set), and dead retrieval / broken feedback loops (a
   signal generated but never stored).
2. Score each by INTEREST x PRINCIPAL. Rank highest interest first: blocks data collection > blocks
   scaling > risks a CACE regression > merely cosmetic. Tell me ugly code that works and never
   changes is almost free; leave it.
3. Give me the safe paydown order: ONE isolated change per item, the eval that must pass before it
   ships, and what breaks if I bundle changes. Remember CACE: changing anything changes everything.
Do not propose a big-bang rewrite. If I have no eval suite, tell me that is debt item one.
End with the single first change to make this week and the eval that gates it.
```
