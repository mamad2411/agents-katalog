---
name: trust-architecture
description: Build credibility in writing, marketing, and product flows using Mayer's ABI model, inoculation, operational transparency, and costly signaling. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Trust Architecture

Attention without trust produces bounce rates. According to the **Persuasion Knowledge Model** (Friestad & Wright 1994), modern readers and users constantly scan for signs that someone is trying to sell or manipulate them. Once they detect hype, their cognitive defenses lock shut.

Use this skill to disarm skepticism *before* or *while* deploying any hook.

## The ABI Trust Equation (Mayer, Davis & Schoorman 1995)

A person will only invest time or money when three independent perceptions are present:

1. **Ability (Can you actually solve this?)** is demonstrated through forensic specificity, working artifacts, and domain precision, never through self-praise ("industry-leading", "world-class").
2. **Benevolence (Are you on my side or just extracting value?)** is proven when you protect the user's time, wallet, or autonomy even at a short-term cost to yourself.
3. **Integrity (Do your rules stay consistent when nobody is looking?)** shows up through upfront constraints, symmetric cancellation, and zero hidden conditions.

## The 6 Invisible Trust Levers

Embed at least one of these levers in the opening 20% of any article, landing page, or product flow:

### 1. The Benevolent Anti-Pitch (Benevolence + Anti-Reactance)
Tell a specific segment of your audience why they should **not** buy your product or read your guide, and hand them a free alternative.
- *Why it works* - A manipulator never turns away a prospect. By narrowing who the solution is for, everyone inside the target boundary immediately trusts that you are telling the truth.
- *Example* - "If your database has fewer than 5 million rows, do not buy our indexing engine. Add a composite B-tree index in 30 seconds (here is the exact snippet) and close this page. We built this only for teams where standard vacuuming locks production."

### 2. Pre-Emptive Inoculation (McGuire 1961)
Name the exact skeptical objection running through the reader's head before they can voice it, validate why smart people think that way, and show the specific boundary where that assumption breaks.
- *Why it works* - Meta-analyses (Banas & Rains 2010) confirm two-sided refutational messages outperform one-sided praise because they co-opt the reader's internal counter-arguing process.
- *Example* - "Your first instinct is probably that another linter will slow down CI by two minutes. Ours did too in v0.1, until we moved AST parsing to a background daemon that only checks touched lines."

### 3. Competence-First Pratfall (Aronson 1966; Helmreich et al. 1970)
Establish clear technical or domain competence first, then admit a specific, honest limitation or past mistake.
- *Guardrail* - Never open with incompetence if the audience does not know you are capable. Pair the flaw with proof of mastery ("We process 1.4 billion webhook events a week, and we still do not support XML payloads because...").

### 4. Operational Transparency (Buell & Norton 2011)
People distrust black boxes and instant "magic" claims. Show the actual mechanism and steps being executed.
- *In Writing* - Show the failed SQL query, the benchmark script, and the raw latency distribution instead of just claiming "we made it 5x faster."
- *In Products* - Instead of a generic spinner saying `"Optimizing your portfolio..."`, show the real operations: `"Scanning 142 tax lots -> Checking 30-day wash-sale window -> Found 3 harvestable pairs ($410 estimated savings)."`

### 5. Costly Signaling (Spence 1973; Zahavi 1975)
A claim is only credible to the degree that a low-quality imitator could not afford to make it.
- *Cheap Signal (Zero Trust)* - "We care deeply about developer experience and data portability."
- *Costly Signal (High Trust)* - Putting a live, un-gated interactive sandbox and a 1-click `"Export entire workspace to plain Markdown"` button directly on the homepage.

### 6. Forensic Calibration (Low Construal Specificity)
Replace rounded, marketing-style numbers (`10x faster`, `99.9% accurate`) with calibrated measurements and explicit failure conditions (`cuts p95 latency from 310ms to 42ms on JSON payloads under 1MB; degrades on nested blobs over 10MB`).
