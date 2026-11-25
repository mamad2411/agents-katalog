---
name: audience-calibration
description: Calibrate hook speed, cognitive load, proof type, and register across audiences using the Elaboration Likelihood Model and Construal Level Theory. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Audience Calibration & Cognitive Routing

A hook that converts a Staff Engineer on GitHub will bore a consumer scrolling on a phone at 11 PM. Conversely, a hook that stops a consumer on social media will trigger immediate disgust and skepticism in a CFO or systems architect.

Use the **Elaboration Likelihood Model (ELM - Petty & Cacioppo 1986)** and **Construal Level Theory (CLT - Trope & Liberman 2010)** to calibrate your hook's processing route, psychological distance, and proof density.

---

## Step 1: Diagnose Processing Route (ELM) & Construal Level (CLT)

1. **Central Route Processing (High Motivation + High Ability to Scrutinize)** Your reader is actively trying to solve a painful problem, evaluate a tool, or learn a craft.
   - *Rule* - Peripheral tricks (flashy formatting, clever puns, emotional hype, authority name-dropping) **backfire** here. Lead with **Low-Construal (concrete, close, mechanistic) evidence** such as exact numbers, reproducible steps, failure boundaries, and architecture trade-offs.
2. **Peripheral-to-Central Bridge (Low Initial Motivation or Low Bandwidth / Skimming)** Your reader is scrolling a feed, checking email between meetings, or browsing casually.
   - *Rule* - Readers will not invest cognitive effort in a 40-word technical paragraph on Line 1. Use a **High-Fluency Peripheral Hook** (a visceral 8-word scene, a sharp visual isolation, or an unexpected number contrast) in Seconds 1-3 that immediately bridges into Central substance by Sentence 3.

---

## Step 2 - The 4 Audience Calibration Profiles

Select the profile matching your target reader or user:

| Profile | Processing State | What Triggers Instant Distrust (Ban List) | Optimal Hook Chord & Proof Type |
|---|---|---|---|
| **1. Skeptical Practitioner / Builder** *(Engineers, Designers, Analysts, Researchers)* | **Strict Central Route, Ultra-Low Construal** (Wants "How it works" & "Where it breaks") | Marketing adjectives, hiding trade-offs, gated demos, high-level abstractions, "AI magic" claims. | **Chord 3 (Forensic Confession)** or **Chord 5 (Open Workbench)**. Lead with a runnable command, a raw diff/query, exact p99 numbers, and explicit failure boundaries (`M20` + `M22`). |
| **2. Time-Poor Executive / Buyer** *(Founders, VPs, CFOs, Operations Leads)* | **High Stakes, Mixed Route, Risk & Mental-Accounting Focus** | Long throat-clearing stories, unquantified features, high switching risk, unclear pricing or lock-in. | **Chord 1 (Trojan Diagnostic)** + **Mental Accounting Reframe (`M25`)** + **Regret Regulation (`M26`)**. Lead with the exact weekly dollar/hour leak in their current process and a risk-free pilot boundary. |
| **3. Fast-Scrolling Consumer / General Reader** *(Mobile feeds, B2C apps, Newsletters)* | **Peripheral Entry -> Emotional/Experiential Bridge** | Jargon, walls of text, multi-field forms, delayed gratification, complex setup instructions. | **Chord 2 (Velvet Rope Sandbox)** or **In-Medias-Res Scene (`M2`)**. Open with a 1-sentence lived micro-frustration they recognize in their body ("38 purchases under $12"), followed by a 1-tap visual result in `< 10 seconds`. |
| **4. Peer Community / Forum Member** *(Hacker News, Reddit, Substack, Discord, X)* | **Hyper-Sensitive Persuasion Radar (`M17` PKM at Maximum)** | Corporate `"We are thrilled to announce"`, polished PR voice, self-promotion without giving away the farm, defensive replies. | **Pure Practitioner Notebook Voice**. Use first-person singular (`"I broke..."`) or candid team notes, give away 100% of the method/code inside the post itself (**Costly Signaling `M22`**), and put any product link quietly at the very bottom as an optional footnote. |

---

## Step 3: Channel-Specific Pacing Adjustments

- **Cold Email / DM** stays under 4 sentences and `< 75 words` total. Sentence 1 must prove you looked at their specific artifact (`M4`). Zero attachments or calendar links in Touch 1.
- **Landing Page Hero** stays under `< 35 words` above the primary interactive element. Visitors must grasp *who it is for*, *who it is NOT for*, and *what happens when they click* within 4 seconds.
- **Long-Form Essay / Technical Post** drops into the scene or anomaly in Sentence 1 (`< 18 words`). Deliver the first concrete takeaway within the first 150 words so the reader trusts you before you ask them to read 2,000 words.
