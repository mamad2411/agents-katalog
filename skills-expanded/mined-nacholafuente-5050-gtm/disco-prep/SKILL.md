---
name: disco-prep
description: Generate a tight pre-discovery-call prep brief from an intro email, referral, or company name. Outputs a 3-section scan doc (who they are, ranked questions, proof to drop) you can read in the two minutes before a sales or consulting call. Use when the user says "/disco-prep", pastes an intro email, or asks to "prep for the disco call", "what should I ask", or "disco agenda". Output goes to the chat, not a file. One-shot, no warehouse, no cron.
---

# Discovery Call Prep

Generate a pre-discovery-call prep brief from an intro email, referral, or company name. The deliverable is **markdown in the chat**, not a file. The goal: walk into the call already knowing who they are, what to ask, and which past win to drop as proof.

**This is a scan doc, not a report.** Target output: under 350 words. If you're padding, cut.

## Input

The user provides some combination of: an intro email, a company name + domain, prior notes, a LinkedIn profile, or a vague "call with X tomorrow."

Extract: contact name, company, stakeholders on the call, referrer, stated needs, tools mentioned, numbers (size, volume).

If you don't have a **company domain**, ask before researching. Do not hallucinate.

## Pre-Flight (before writing anything)

1. **Research.** Web-search the domain + recent news (last 6 months). Fetch the homepage. Look up named stakeholders.
2. **Match to past work.** Skim your own notes/CRM for analogous clients to anchor the proof in Section 3. Keep a short list of past wins by vertical wherever you keep it.

## Voice & Quality Bar

- **Specific, not generic.** Every question references THIS prospect's context. No "what's your tech stack?"
- **Diagnostic, not polite.** Each question shapes scope.
- **Cut ruthlessly.** A disco call is 30 to 45 min. Pick the questions that matter most.
- **Short sentences. No fluff.** Don't restate what the email already said.

## Do not invent

- Only state facts that appear in the source material (email, notes, research).
- Do not infer timelines, deal volume, or team size unless explicitly stated.
- "Eventually" / "down the line" / "future" = NOT a commitment. Treat as parking-lot.
- If the source is silent on something, it becomes a must-ask question, not a claim.
- When tempted to extrapolate ("this means they probably want X by Y"), stop and turn it into a question instead.

## Output Format

**Exactly 3 sections.** Use `## N. Section Name` headers. Be terse.

### Header block (above section 1)

```
> Disco Prep: {Company}
> Call with: {stakeholders + roles}
> Referrer: {referrer or "direct inbound"}
> Prepared: {today's date}
```

### 1. Who They Are (30-sec read)

**2 sentences max.** Company type, size, geography, what they do. One bonus line ONLY if there's a non-obvious signal that shapes the call (recent funding, new hire, founder background, returning client). Otherwise stop at 2.

### 2. Questions to Ask, Ranked

**Cap at 8 total.** 5 must / 3 should. Each = one line, with a short *why* in italics. Tag the stakeholder if several are on the call.

**Must-ask (5, scope-defining).** Cover the gaps that block writing a proposal: who consumes the output, what's in scope, which tools/systems are involved, hard timeline, decision maker. Anything you were tempted to assume goes here as a question instead.

**Should-ask (3, shapes design).** Pipeline stages, notification routing, reporting cadence, integration triggers, ops handoff specifics.

Format: `**Q:** "actual question phrasing" (*why it matters*)`

### 3. Proof to Drop

**1 past win only.** Pick the strongest match.

```
- {Past client or anonymized}, {one-line situation match} -> {one specific metric or outcome}
  When to drop: {minute X / on objection Y}
```

Keep a simple match map by vertical (e.g. VC/PE -> your fund client, gym/SaaS -> your churn client) so you reach for the right proof fast.

## Rules

1. **Output to chat only.** Never write to a file.
2. **Pre-flight first.** Research before writing.
3. **No invented facts.** If it's not in the source, it's a question, not a claim.
4. **No generic questions.** Every Q references something specific from the intro.
5. **Tag the stakeholder** when multiple are on the call.
6. **Cap total output ~350 words.** If over, cut.
7. **Three sections only.** Who -> Questions -> Proof. No agenda, no hypothesis, no red-flags section.
