---
name: ai-pmm-reviewer
description: Review AI-generated B2B marketing and PMM drafts for strategic sharpness, customer truth, positioning quality, plain English, and AI tells; diagnose gaps and rewrite only where judgment is clear.
---

# AI PMM Reviewer

## When to use

Use this skill when you have an AI-generated or AI-assisted B2B marketing draft and need PMM judgment before it ships.

Use it for:

- Reviewing blog posts, landing pages, launch copy, emails, ads, sales enablement, positioning statements, messaging frameworks, and executive narratives
- Checking whether a draft matches a messaging framework or positioning strategy
- Finding where the draft sounds generic, inflated, or interchangeable with competitors
- Turning customer calls, notes, transcripts, or summaries into review evidence
- Producing a sharper rewrite after the strategic issues are clear

The core belief: AI makes the average PMM faster, not better. LLM output trends toward average. It often sounds fluent but familiar, and buyers can smell it. AI earns its keep in review: checking a 2,000-word blog against the messaging framework, catching gaps, summarizing customer calls, and helping the PMM say, "I talked to 10 customers, and here is what they said."

AI gets the work to 60% fast. The last 40% requires customer conversations, market instinct, hard positioning choices, voice, and rewriting.

## Inputs

Ask for or infer these inputs:

- Draft content to review
- Company, product, and category
- Target audience, segment, persona, and buying role
- Messaging framework, positioning statement, launch brief, campaign brief, or sales narrative if available
- Customer voice, call notes, quotes, objections, win/loss notes, or research
- Competitive alternatives, including the status quo
- Intended channel and job of the asset
- Desired review depth: quick pass, detailed PMM review, or rewrite-ready teardown

If key inputs are missing, still review the draft, but label assumptions and lower confidence. Do not invent customer truth. Mark missing evidence as a gap.

## Review workflow

### 1. Identify the job of the draft

Before editing words, define what the asset is supposed to do.

Ask:

- Who is the buyer or reader?
- What decision, belief, objection, or action should this asset influence?
- Where will it appear?
- What does the reader already believe?
- What must be different after reading it?

A draft can be well written and still fail the job.

### 2. Check strategic fit

Compare the draft against the positioning and messaging inputs.

Look for:

- Clear target segment rather than a vague market
- Real alternative or status quo
- Specific pain and business consequence
- Differentiated value, not generic capability language
- Reasons to believe
- Customer language
- Explicit tradeoffs about who this is and is not for

If the company logo can be swapped with a competitor and the copy still works, it is not sharp enough.

### 3. Separate PMM problems from copy problems

Do not treat weak strategy as a wording issue.

Classify issues as:

- Positioning gap: unclear audience, alternative, differentiated value, or market frame
- Messaging gap: unclear pain, outcome, proof, or narrative flow
- Evidence gap: claim lacks customer quote, data, mechanism, demo, story, or example
- Voice gap: sounds like AI, category mush, or corporate filler
- Copy gap: too long, abstract, passive, repetitive, or hard to read

Fix the right layer first.

### 4. Find the AI tells

AI drafts often sound competent and empty. Identify the patterns, then explain the business risk.

Common AI tells:

- Grand opening claims with no concrete situation
- Phrases like "in today's fast-paced digital landscape"
- Symmetrical three-part lists that say little
- Overuse of "not only... but also"
- Repeating the same idea with new adjectives
- Claims without a mechanism
- Bland benefit stacks: faster, smarter, seamless, scalable, efficient
- Generic verbs: unlock, empower, transform, optimize, streamline, leverage
- Inflated adjectives: cutting-edge, revolutionary, robust, innovative, comprehensive
- Category mush: solution, platform, ecosystem, synergy, digital transformation
- Polished paragraphs that no customer would ever say out loud

Strip AI-isms, but keep the PMM judgment review focus. The goal is not to make text sound casual. The goal is to make it true, specific, and useful.

### 5. Run PMM-specific checks

Check the draft against these questions:

- Audience: Is the reader specific enough?
- Problem: Is the pain concrete, or is it a generic productivity problem?
- Consequence: Does the copy show what the pain costs the business?
- Status quo: Does it name how customers solve this today?
- Differentiation: Does it say why this product is meaningfully better than the alternative?
- Proof: Does each important claim have evidence, mechanism, data, demo, customer quote, or story?
- Voice of customer: Are there words buyers would actually use?
- Stakes: Does it connect to revenue, cost, risk, uptime, safety, reliability, trust, speed, or ability to say yes?
- Specificity: Could the logo be swapped with a competitor?
- Readability: Is it everyday English?
- Story: Does it show a concrete before/after moment, not just a claim?

Voice of customer is PMM currency. A strong review should help the team say, "We heard this from customers," not "The model suggested this phrasing."

### 6. Score the draft

Use the scoring rubric below. Be direct. Do not inflate scores because the prose is fluent.

Score each area from 1 to 5:

1. Audience clarity
2. Problem specificity
3. Status quo and alternative
4. Differentiated value
5. Proof and credibility
6. Customer language
7. Plain-English readability
8. Narrative flow
9. Distinctiveness versus competitors
10. Usefulness for sales or buyer conversation

Overall score:

- 45-50: Strong. Needs line edits, not strategy repair.
- 38-44: Good foundation. Some gaps or generic sections need sharpening.
- 30-37: Serviceable 60% draft. Needs PMM judgment, proof, and rewriting.
- 20-29: Generic or under-supported. Likely AI-ish. Needs strategic repair.
- Below 20: Not ready. Rebuild from customer truth and positioning.

### 7. Recommend what to gather

If the draft lacks customer truth, name the missing inputs.

Useful evidence includes:

- 5 to 10 customer calls or call summaries
- Exact customer phrases
- Sales call objections
- Win/loss patterns
- Before/after workflow examples
- Competitive displacement stories
- Demo moments that prove the mechanism
- Quantified impact or credible proxy metrics

Do not pretend a rewrite can solve missing market insight.

### 8. Rewrite with judgment

Only rewrite after diagnosis. The rewrite should make hard choices visible.

Rewrite rules:

- Use concrete nouns and verbs
- Replace claims with situations, mechanisms, proof, or stories
- Prefer everyday English over category language
- Cut filler before adding polish
- Name the real alternative when useful
- Show business consequence, not just activity
- Preserve any good customer language
- Avoid jargon: solution, synergy, leverage, cutting-edge, revolutionary, ecosystem, empower, streamline
- Avoid vague AI/productivity claims unless the mechanism is clear
- Make the copy sound like a sharp PMM, not like a humanized chatbot

Stories beat claims. If you can show a customer moment, use it.

## Output format

Return the review in this structure:

1. Short diagnosis
   - 3-5 bullets on what is working and what is weak

2. Scorecard
   - Table or bullets with 1-5 scores for each rubric area
   - Overall score out of 50
   - Readiness level: strong, needs sharpening, 60% draft, strategic repair, or rebuild

3. PMM gaps
   - Audience/segment gaps
   - Problem/consequence gaps
   - Status quo/alternative gaps
   - Differentiation gaps
   - Proof gaps
   - Voice-of-customer gaps

4. AI tells and language issues
   - Specific phrases to cut or replace
   - Why each phrase weakens the draft

5. Questions or evidence to gather
   - Customer questions
   - Sales questions
   - Proof needed

6. Rewrite direction
   - Message to lead with
   - What to cut
   - What to add
   - Tone and language guidance

7. Revised draft or sample rewrite
   - Rewrite only the requested section, or provide a concise full rewrite if appropriate
   - Keep the rewrite grounded in the available evidence
   - Mark assumptions if the rewrite relies on inferred context

## Quality bar

A strong AI PMM review:

- Improves the strategy, not just the wording
- Calls out generic AI language directly
- Distinguishes missing evidence from weak copy
- Applies positioning and messaging fundamentals
- Uses voice of customer as the standard for credibility
- Names the real alternative or status quo
- Pushes toward concrete situations and business consequences
- Explains why the draft would or would not help a buyer decide
- Produces a rewrite that is sharper, shorter, and more specific
- Refuses to overclaim when proof is missing

## Anti-patterns

Avoid:

- Merely "humanizing" AI text while keeping weak thinking
- Replacing one set of generic adjectives with another
- Praising fluent copy that says nothing specific
- Treating all audiences as "modern teams" or "businesses today"
- Using customer-free claims as if they were insight
- Hiding weak differentiation behind "AI-powered," "seamless," or "intelligent"
- Writing taglines before the positioning is clear
- Rewriting away useful customer language because it sounds less polished
- Making the product the hero when the customer situation should be the hero
- Claiming transformation without naming what changes, for whom, and why it matters
