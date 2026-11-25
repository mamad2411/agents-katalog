---
name: futureproof-onboarding-interview
description: |
  Runs a structured ~2-hour onboarding interview that pulls a new client's
  real business context — one question at a time, pushing past marketing-speak —
  and synthesises it into a 10-section HyperTuned memory that becomes the
  persistent context every other FutureProof skill reads. Use when a new
  FutureProof client is being set up, or when the user says "run my onboarding
  interview", "build my business memory", "set up HyperTuned", or "capture my
  business context". For capturing and saving durable business context, not for
  recommending skills (hand off to futureproof-skill-picker) or scoping a build
  (route to futureproof-brd).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="futureproof-onboarding-interview")
```

Use the returned `context`, `instructions`, and `recent_sessions` to see what business context already exists for this client.

> **Returning user check:** If the connect result's "User Knowledge" section already holds a HyperTuned business
> memory, do NOT restart from zero. Summarise what is already captured, then ask
> whether to refresh a specific section, fill a "still thin" gap, or leave it as
> is. For first-time clients, run the full interview below.

## Step 2: Frame the Session

The subject is **the business, not the founder's life story** — the founder only matters where their thinking is load-bearing for how the business runs.

Set expectations out loud before the first question:

- It takes about two hours. One question at a time.
- You will push back when an answer goes shallow or generic.
- Say why it is deliberate: "The website version of your business is useless here — I want the real version."

Get a clear "ready" before you start. It is a conversation, not a form.

## Step 3: Run the Interview

### 3A: The interview loop (repeat for every question)

1. Ask exactly **one** question. Never stack two questions into one turn.
2. Listen, then choose the next question from what they actually said — not from a script.
3. Score the answer before moving on: is it specific and true only of **them**, or could it describe fifty other businesses?
4. If it is shallow, jargon, a segment instead of a person, or contradicts something earlier — push back **once**, warmly but directly, then re-ask. Be specific: not "tell me more", but "that works for any competitor — what's the version only true for you?"
5. Log any signal that surfaces (a real customer phrase, a contradiction, an "it lives in my head" admission) and bring it back when its area comes up.

### 3B: Coverage map (reach all ten — each has a bar to clear)

Follow the thread; you do not have to march down this list in order. But every area must eventually clear its bar. The line below is your **opening** move — keep digging until the answer clears the bar.

1. **What it does** — on a Tuesday, plain English, no category labels. BAR: a stranger could picture the actual work.
2. **Why it exists** — the problem solved + why existing options weren't good enough. BAR: a specific inadequacy, not "they were bad."
3. **Who it serves** — one real human, not a segment: state on arrival, their words, fears, wins, what they tried before. BAR: you could spot them in a room.
4. **What ships** — the real deliverable + process; what a client gets for their money. BAR: a concrete artifact + steps.
5. **Where it's going** — success at 12 months and 3 years; what would let the founder walk away happy. BAR: a number or a named outcome.
6. **What it stands for** — the non-negotiables; what it won't do even for money. BAR: a real line they've actually held.
7. **What makes it different** — the version they'd tell a competitor over a beer. BAR: not repeatable by a rival.
8. **How it sounds** — voice, tone, banned words, signature phrases. BAR: you could ghostwrite a sentence they'd approve.
9. **How it operates** — team, roles, processes that work vs. processes that live in someone's head. BAR: named owners + where it breaks.
10. **Where the gaps are** — what slows it down, what's undocumented, the founder-shaped ceiling. BAR: an honest weak point, not a humble-brag.

### 3C: Synthesise the memory

When every area has cleared its bar, stop interviewing. Write structured memory content in the **client's own words**, organised into the ten sections below. Each section maps to one area of the coverage map. Close with an honest "still thin" note — framed as a heads-up, not homework.

```
# HyperTuned Memory — <client name>

## 1. What the business does
<On a Tuesday, plain English, no category labels.>

## 2. Why it exists
<The problem solved + the specific inadequacy of existing options.>

## 3. Who it serves
<One real human: state on arrival, their words, fears, wins, what they tried before.>

## 4. What ships
<The real deliverable + the process behind it. The concrete artifact + steps.>

## 5. Where it's going
<Success at 12 months and 3 years. A number or a named outcome.>

## 6. What it stands for
<The non-negotiables. A real line they've held, even against money.>

## 7. What makes it different
<The version they'd tell a competitor over a beer. Not repeatable by a rival.>

## 8. How it sounds (voice)
<Tone, signature phrases, banned words. Enough to ghostwrite a sentence they'd approve.>

## 9. How it operates (team & ops)
<Team, roles, what works vs. what lives in someone's head. Named owners + where it breaks.>

## 10. Where the gaps are
<What slows it down, what's undocumented, the founder-shaped ceiling.>

## "Still thin" note
<What is missing or shallow after this session — a heads-up for the next session or the account manager.>
```

## Step 4: Deliver and Save the Memory

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — show the client the drafted memory and ask for the go-ahead.
> 2. **Produce as a document** — a structured, self-contained artifact, not inline chatter.
> 3. **Offer amends** — "Any section you want to sharpen before I save it?"
> 4. **Persist it as the client's business context** so every other FutureProof skill reads it:

```
FutureProof:save_context(skill="futureproof-onboarding-interview", universal_context={
  business_memory: "<the full 10-section memory, in the client's own words>",
  still_thin: "<the honest gaps note>",
  captured: "onboarding-interview"
})
```

`save_context` queues the memory for HyperTuned. HyperTuned usually stores it within a minute. After that, each later `connect()` shows the memory in the "User Knowledge" section of the result. It shows as JSON text with a `business_memory` field. The picker and every downstream skill read it there. The connect result has no `universal_context` field.

## Step 5: Hand Off to the Skill Picker

Only start Step 5 after Step 4 has saved the memory and the client has approved it. If the memory is missing, finish Step 4 first — the picker's matches are only as good as the memory it reads.

1. Hand off to the **futureproof-skill-picker** skill. It ranks the FutureProof catalog against the pains this client named and returns the best 10.
2. Tell the picker to weight **Section 10, "Where the gaps are"** (the client's problems) and **Section 4, "What ships"** (the work they repeat) — these two carry the strongest pain signal.
3. The picker runs one recommended skill live on the client's real input and leaves a short written plan for the rest.
4. Any named need with no matching skill routes to the **futureproof-brd** skill — a Business Requirements Document, the build request sent to the dev team.

## Step 6: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged,
> create a lightweight hypothesis based on the most uncertain choice made this
> session (e.g. which questions surfaced the richest answers).

```
FutureProof:save_experiment(skill="futureproof-onboarding-interview", experiment={
  hypothesis: "[e.g. 'Opening with Section 10 (gaps) before Section 1 surfaces more honest weak points earlier in the interview']",
  variants: ["control: cover areas in listed order", "variant: lead with the gaps and repeated-work areas"],
  measurement: "[e.g. number of sections that clear their bar without a second push, across the next N interviews]",
  expected_impact: "[e.g. richer memory in less time; fewer 'still thin' flags at synthesis]"
})
```

## Step 7: Request Research

> **Research must be user-specific.** Only request research if this session
> revealed a concrete knowledge gap tied to this client's business. Skip generic
> "best practices" queries.

```
FutureProof:request_research(skill="futureproof-onboarding-interview",
  query="[Contextual query tied to the client's industry, ICA, or model — e.g. 'Current buyer language and top objections for <client's niche> in 2025']",
  reason="[Why this fills a gap the memory left thin — e.g. 'Section 3 stayed shallow on the buyer's prior attempts; need market language to sharpen it']"
)
```

## Step 8: Save Session

> **Session summary must be fact-dense:** include the client's company, ICA,
> industry, what was captured, any corrections given, and end with **"Next
> session defaults: [3-5 things to pre-fill on next connect()]"**.
>
> **Outcomes array:** one concrete fact per item, each extractable as a standalone
> business fact.

```
FutureProof:save_session(skill="futureproof-onboarding-interview", session={
  summary: "...[fact-dense: company, ICA, model, what the memory captured, sections still thin, handoff status to the picker. End with: Next session defaults: ...]",
  outcomes: [
    "Company: [name and what it does in one line]",
    "ICA: [the one real buyer captured in Section 3]",
    "Voice: [signature phrases and banned words from Section 8]",
    "Top gaps: [the pains from Section 10 to feed the picker]"
  ],
  metadata: {}
})
```
