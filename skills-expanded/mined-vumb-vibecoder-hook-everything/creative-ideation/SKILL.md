---
name: creative-ideation
description: Generate non-cliche hook ideas, campaign concepts, and product angles using live web signals, Graveyard pruning, and Koestler Bisociation. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Creative Hook Ideation Engine (Live-Signal & Bisociation Protocol)

When an AI is asked for "creative hook ideas" without a strict protocol, it samples from the center of its static training distribution - producing outdated 2019-era viral templates (`"Unpopular opinion:"`, `"X is dead, long live Y"`, `"Imagine a world where..."`). Savvy audiences recognize these templates instantly and scroll past.

Follow this 5-step protocol to generate fresh, high-converting hook concepts anchored in current reality.

## Step 1: Mandatory Live Web Signal Mining (Do Not Rely on Static Memory Alone)

Before brainstorming a single hook idea, load `skills/market-intelligence` and run 2-3 targeted web searches (when search tools are available) to harvest **live, current-year friction** in the user's domain:

1. **Recent Changelogs, Pricing Shifts & Breakages** Check what changed in the last 30-90 days (new API limits, framework updates, algorithm shifts, regulatory changes, or tool price hikes).
2. **2-to-4 Star Practitioner Complaints** Collect exact phrases, error codes, or frustrations that real users are posting on forums, Reddit, Hacker News, GitHub Issues, or product reviews right now.
3. **Fatigued Consensus** Identify what "best practice" everyone is repeating right now that secretly fails in production or wastes money.

*Organic Guardrail* - Pass every discovered signal through the **Organic Fit Gate** (`skills/market-intelligence`). Never force a trending topic if it is not causally tied to the user's core problem.

## Step 2 - The "First-3 Graveyard" Rule (Pruning High-Probability Clichés)

Your first 3 ideas are statistically guaranteed to be the most predictable ideas that every other LLM and average copywriter will generate.

1. Mentally generate the 3 most obvious hooks for the request (e.g., a generic time-saving promise, a standard curiosity question, a dramatic fear hook).
2. **Discard all 3 immediately.** Never present them as recommendations. (Show a brief `[Discarded Graveyard]` line so the user sees which cliches you eliminated.)

## Step 3: Koestler Bisociation (Colliding Two Orthogonal Matrices)

Arthur Koestler (*The Act of Creation*, 1964) proposed that genuine originality (**Bisociation**, `M23`) happens when you connect two self-consistent but habitually separate matrices of thought:
- **Matrix A** represents the live domain friction or user pain discovered in Step 1.
- **Matrix B** represents one of the **6 Non-Obvious Structural Lenses** below.

Generate 5 distinct hook concepts by colliding Matrix A with 5 different lenses from Matrix B:

| Lens ID | Structural Lens | How It Transforms a Raw Topic Into a Fresh Hook |
|---|---|---|
| **L1** | **The Forensic Autopsy** | Instead of giving advice, reconstruct the exact timeline and dollar/hour cost of a specific failure down to a single overlooked line, setting, or habit. |
| **L2** | **The Inverted Metric** | Take the #1 metric everyone in the niche is currently bragging about optimizing, and prove with concrete mechanics how over-optimizing it causes a worse downstream failure. |
| **L3** | **The Un-Gated Micro-Artifact (Trojan Gift)** | Instead of writing an ad or pitch, turn the hook into a 10-second runnable check, cheat-sheet table, diagnostic script, or interactive calculator that solves the first 20% of the problem for free right in the feed. |
| **L4** | **The Benevolent Gatekeeper (Anti-Target Filter)** | Open by disqualifying 70% of the mainstream audience with a free 1-line alternative, then speak exclusively to the 30% facing the high-stakes edge case. |
| **L5** | **The Unspoken Industry Taboo (Costly Truth)** | State the uncomfortable operational truth that vendors or creators in this space know privately but never admit publicly because it hurts short-term upsells. |
| **L6** | **Cross-Discipline Mechanism Borrow** | Import a precise working protocol from an unrelated high-reliability field (ER trauma triage, aviation pre-flight checklists, submarine acoustic monitoring, restaurant kitchen mise-en-place) to solve the user's workflow problem. |

## Step 4: Bind Each Idea to a 4-Note Psychological Chord

For every generated idea, structure the output so the user can deploy it immediately:

1. **Concept Name & Bisociation Pair** combines `[Live Signal / Friction]` x `[Lens L1-L6]`.
2. **Psychological Chord (`skills/hook-compounding`)** names the exact 4 notes (`Trust Damper + Cognitive Anchor + Active Generator + Forward Vector`).
3. **Verbatim Draft Hook** provides the actual opener, ad, or UX flow copy (100% compliant with all 85 rules in `skills/anti-slop`).
4. **Why It Converts Invisibly** explains in 1-2 sentences how the hook bypasses skepticism and leads naturally into the product or article payoff.

## Step 5: Novelty & Anti-Slop Self-Audit

Before showing the ideas to the user, verify three checks:
- Every idea references a concrete, current mechanism, number, or lived behavior rather than abstract buzzwords.
- All 5 ideas are structurally different from one another (no two ideas using the same Lens or Chord).
- Every draft hook scores `<= 15/100` on `tools/slop_scan.py`.
