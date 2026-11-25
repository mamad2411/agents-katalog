---
name: implementation-recap
description: Generate a structured recap of an implementation — the original problem, the solution, and a defense of why it's the right approach across correctness, optimality, and elegance. Use this skill when the user asks to "recap", "summarize the implementation", "write up the changes", "explain what we did and why", "document the approach", or wants to articulate the rationale behind a set of changes for a PR description, design doc, team update, or their own understanding. Also trigger when the user wants to explain or justify an implementation to others.
---

# Implementation Recap

You've been asked to produce a recap of an implementation — not just what changed, but why it's the right approach. This serves as both documentation and a persuasive argument for the choices made.

A good recap helps the author articulate their thinking, gives reviewers confidence, and serves as a reference for anyone who touches this code later. It should read like a thoughtful engineer explaining their work to a peer.

## Step 1: Understand the full picture

Before writing anything, gather context. You need to understand both the problem and the solution deeply.

**The problem:**
- What was broken, missing, or inadequate? Look at the conversation history, commit messages, linked issues, or ask the user.
- What were the constraints? (backwards compatibility, performance requirements, deadlines, dependencies)
- What would happen if this wasn't addressed?

**The solution:**
- Read all changed files and understand the implementation end-to-end
- Trace the key code paths — how does data flow through the changes?
- Identify the non-obvious decisions — the parts where a reasonable engineer might have gone a different direction

**The alternatives:**
- What other approaches could have been taken? Think about at least 2-3 alternatives that a thoughtful reviewer might suggest. You need these to argue convincingly for the chosen approach.

Use subagents if the change set is large. Spawn one per area of the codebase to read and summarize the changes, then synthesize their findings.

## Step 2: Write the recap

Structure it as follows:

### Problem

State the problem clearly and concisely. Include enough context that someone unfamiliar with the history can understand what needed to happen and why. If there's a root cause, name it. If there are symptoms, describe them. Avoid jargon where possible — if you must use domain terms, make sure the surrounding context makes their meaning clear.

### Solution

Walk through the implementation at the right level of abstraction. Not line-by-line (the diff is there for that), but component-by-component or decision-by-decision. For each significant piece:
- What it does
- Why it's structured the way it is
- Any subtlety that isn't obvious from reading the code alone

### Why this approach

This is the heart of the recap. For each of the three axes, make the case:

**Correctness**: Explain why this implementation is correct — not just "it works" but why it handles the tricky cases. Call out specific edge cases, error conditions, or invariants that the implementation preserves. If there are known limitations, name them honestly and explain why they're acceptable.

**Optimality**: Explain the performance characteristics. What's the complexity? Why is it appropriate for the expected data scale? If you made a deliberate tradeoff (e.g., using more memory to save CPU, or accepting O(n log n) when O(n) was theoretically possible but far more complex), explain the reasoning.

**Elegance**: Explain how the solution fits into the existing codebase. Does it follow established patterns? Does it introduce new abstractions, and if so, why are they justified? How does it set up future work? Is it easy to modify, extend, or delete?

### Alternatives considered

For each alternative you identified in Step 1, briefly describe it and explain why the chosen approach is better. Be fair — acknowledge the strengths of alternatives before explaining why they lose on balance. This isn't about dismissing other ideas, it's about showing that the decision was thoughtful.

## Guidelines

- **Be honest, not defensive.** If there are genuine weaknesses or tradeoffs in the implementation, name them. A recap that acknowledges limitations is more credible than one that pretends they don't exist.
- **Write for a smart but uninformed reader.** Assume the reader is a competent engineer who hasn't been following along. They can read code, but they need you to explain the *why*.
- **Keep it proportional.** A small bug fix gets a short recap. A major architectural change gets a thorough one. Match the depth to the significance.
- **Use the code as evidence.** When you claim the implementation handles an edge case, point to the specific code that does it. When you claim it's performant, reference the actual complexity or the relevant code path.
