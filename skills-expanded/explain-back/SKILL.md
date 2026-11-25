---
name: explain-back
description: "Use before trusting, merging, or building on code that was just written or is about to change. The agent explains it back in plain language — what it does, why it exists, what breaks if it's wrong — and doesn't proceed until the mental model is confirmed. Use on AI-generated diffs that look fine but nobody can explain, and before changing an unfamiliar file."
---

# Explain Back

## The failure mode this fixes

The most expensive bug in AI-assisted development isn't wrong code — it's code that *looks* right that nobody understands. The agent writes 80 lines, the human skims, says "looks good," and merges. Six weeks later it breaks and no one — human or agent — can say why it existed.

`explain-back` inverts review. Before code is trusted, the agent must explain it back in plain language until the human confirms the model is correct. If the agent can't explain a line, that line is suspect. If the human can't follow the explanation, the code is too clever. Either way, you find out *now*, not at 3am.

## When to Use This Skill

- Right after you (the agent) generate a non-trivial change, before declaring it done
- When reviewing code an agent wrote and the diff "looks fine" but no one built a model of it
- When onboarding to an unfamiliar file before changing it
- When the human catches themselves about to approve something they can't explain
- Before building new logic on top of existing code whose behavior is assumed, not known

**Don't use when:** the change is a trivial rename, a config value, or a one-line typo fix. Reserve it for logic that someone will later have to reason about.

## Instructions

Work through these phases in order. Do not skip to a fix or a "looks good" — the whole point is to surface the gap between what the code says and what everyone *thinks* it says.

### 1. Restate the intent (before reading the code closely)

State, in one sentence, what this code is *supposed* to do — from the requirement, the PR title, or the conversation. Do not look at the implementation yet. This is the contract you'll check the code against.

> "This function is supposed to deduplicate incoming webhook events so we never process the same payment twice."

### 2. Explain it back, line group by line group

Walk the code in small chunks. For each chunk, say in plain language:
- **What** it does (the mechanic)
- **Why** it's there (the intent it serves)
- **What breaks** if it's wrong or removed

Use no jargon the human hasn't used first. If you cannot explain *why* a chunk exists — only *what* it does — flag it explicitly as `UNJUSTIFIED`. Unjustified code is the #1 source of silent bugs and is the highest-value thing this skill finds. If an `UNJUSTIFIED` chunk turns out to have no callers or no observable effect, hand it to `delete-this`; if the explanation keeps stumbling over what something is *called*, route the fix to `name-things`.

**Scale depth to risk, not line count.** On a large diff, chunk at the function level and drop to line-level only where the assumptions concentrate — state changes, boundaries, error paths, anything touching money or auth. An explanation nobody reads defeats the skill exactly the way "looks good" does.

### 3. Name the assumptions

List every assumption the code depends on that is not enforced in the code itself:
- "Assumes `event.id` is always present" — is it?
- "Assumes this runs single-threaded" — does it?
- "Assumes the upstream already validated the amount" — verified where?

Each unenforced assumption is a kill-risk. Rank them.

### 4. Find the divergence

Compare the explanation (steps 2–3) against the intent (step 1). Call out exactly where they diverge:
- Code does *more* than intended (scope creep / hidden side effects)
- Code does *less* than intended (missing cases)
- Code does something *different* (the bug)

### 5. Confirm or correct the model

Present the explanation to the human and ask them to **restate the intent in their own words** — not a yes/no. "Is this right?" invites a lazy "yep"; "In one line, what did you expect this to do?" surfaces the mismatch.
- If their restatement matches your explanation → the code is now trusted; proceed.
- If it diverges → you have found a real defect or a real misunderstanding. Stop and resolve it before writing any fix.

**Running unattended (no human in the loop)?** Do not silently proceed. Emit the full explanation, the ranked `ASSUMPTIONS`, and any `UNJUSTIFIED` or `DIVERGENCE` findings as an explicit, logged block, and treat each unconfirmed high-risk assumption as a blocker to flag — not something to wave through. The point of the skill survives without a human: the gap still gets written down where the next reader will see it.

Do not propose a fix until the model is confirmed. A fix built on a wrong model is just a faster bug.

If a `CONTEXT.md` exists at the repo root, explain in *its* vocabulary — translate the code into the project's real domain nouns, not generic ones.

## Output format

```
INTENT
  <one sentence: what this is supposed to do>

EXPLANATION
  [chunk 1] what / why / breaks-if-wrong
  [chunk 2] ...
  UNJUSTIFIED: <any code whose "why" you cannot state>

ASSUMPTIONS (ranked by risk)
  1. <assumption> — enforced? <yes/no/where>
  2. ...

DIVERGENCE FROM INTENT
  <does more / does less / does different — be specific with line refs>

CONFIRM
  "In one line, what did you expect this to do?"  (restate, don't yes/no)
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Explaining *what* without *why* | "It calls `.filter()`" is narration, not understanding. The value is in the why. |
| Using the code's own vocabulary to explain the code | Circular. Translate into the domain, not back into the syntax. |
| Skipping straight to a fix | A fix on an unconfirmed model is a faster bug. Confirm first. |
| Accepting "looks good" as confirmation | The human must restate the intent in their own words, or it isn't confirmed. |
| Marking everything justified | If nothing is `UNJUSTIFIED`, you probably didn't look hard. Most real diffs have at least one. |

## Mental Model

> Code you can't explain back is code you don't own yet. Explain it back until you do — *before* you trust it, not after it breaks.
