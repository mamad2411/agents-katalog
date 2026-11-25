---
name: interview-synthesis
description: Use this skill when the user asks to turn user research into patterns. Trigger phrases include "synthesize user interviews", "interview notes to patterns", "research synthesis", "what did we learn from these interviews", "cluster these findings", "sintetizar entrevistas". Produces patterns grounded in observed behavior, not a feature list. Separates what users do from what they say. Works in English and Rioplatense Spanish.
---

# interview-synthesis

> **Anchor:** PM as anthropologist. Discovery is a practice. Kill the assumption you loved.

## When to use

Use this skill when the user has raw research input (interview notes, transcripts, support tickets, session recordings, survey free-text) and needs to turn it into named patterns the team can act on. Works for:

- A batch of user interviews that needs structure before a decision.
- Mixed qualitative input from several sources that needs clustering.
- A discovery round where the question is "what is actually going on", not "what should we build".

Do not use when:

- The user has patterns already and wants to pitch a direction. Use `feature-proposal`, which is the pitch that comes after synthesis.
- The user has a confirmed problem and wants to spec the build. Use `prd-authoring`, which is the spec that comes after synthesis.

## Philosophy

Synthesis is where most research dies. The team runs the interviews, then writes a feature list from memory and calls it insight. Two concepts from the handbook do the work here.

**PM as anthropologist.** The job is to observe, not to invent. A user telling you what they want is data about their stated preference, not about their behavior. The pattern lives in what they did, the workaround they built, the moment they gave up. Treat every interview as field notes, not as a vote.

**Discovery is a practice.** Synthesis is not a one-time report. It is a repeated discipline that compounds. Each round confirms some assumptions and kills others, and the killed ones are the valuable output. A synthesis that confirms everything you already believed found nothing. The point of the practice is to be wrong on paper before you are wrong in production.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: insight, pattern, job-to-be-done, discovery, backlog, stakeholder, AB test, KPI. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the synthesis, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Separate observed behavior from stated preference

Read every input twice. The first pass tags what the user did: the workaround, the abandoned flow, the tool they opened instead, the moment they stopped. The second pass tags what the user said they wanted. Keep these in two columns. A stated preference is a lead to investigate, never a finding on its own.

### Step 2. Cluster into patterns with frequency

Group the observed behaviors into patterns. A pattern is a behavior that shows up across more than one person, named in plain language. For each, record how many of your sources show it. Frequency is not proof, but a behavior seen once is an anecdote and a behavior seen across half your sources is a signal. Write the count.

### Step 3. Name the job-to-be-done per pattern

For each pattern, name what the user was trying to get done when the behavior appeared. Phrase it as the user's goal in their context, not as a feature. "Get back to where I was after a mistake" is a job. "Add an undo button" is a solution. Keep the job free of solution language.

### Step 4. List assumptions confirmed and assumptions killed

Go back to what the team believed before this round. For each prior assumption, mark it confirmed, killed, or untouched, and cite the input that decided it. The killed assumptions are the most valuable part of the output. Name them plainly, including the one you were attached to.

### Step 5. Quote sparingly and only as evidence

Use direct quotes only to support a named pattern, never to decorate the report. One sharp quote per pattern is enough. A quote that is not attached to a pattern is filler. Attribute each quote to a source, anonymized if needed.

### Step 6. End with the next cheapest validation, not a feature list

Close by naming the single cheapest test that would confirm or kill the strongest pattern. A fake door, five more targeted interviews, a support-ticket query, a prototype shown to three users. Do not close with a roadmap. Synthesis ends at "here is what to investigate next", not at "here is what to build".

## Templates

- `templates/en/synthesis-report.md`: full research synthesis across a round of inputs.
- `templates/en/pattern-card.md`: a single pattern and its job-to-be-done.
- `templates/es/synthesis-report.md`: síntesis completa de una ronda de research.
- `templates/es/pattern-card.md`: un solo patrón y su job-to-be-done.

## Related skills

- `feature-proposal`: use it after synthesis, when a pattern is strong enough to pitch a direction.
- `prd-authoring`: use it after synthesis, when the problem is confirmed and the build needs a spec.
- `ux-audit`: use it when the question is whether an existing flow has usability problems, not what users are trying to get done.
- `competitive-teardown`: use it when the input is competitor products rather than your own users.

## Anti-patterns

This skill must never produce:

- A synthesis that reports stated preferences as findings.
- A synthesis that lists features instead of patterns and jobs.
- A synthesis where every prior assumption survived untouched.
- A pattern with no frequency count.
- A job-to-be-done written as a solution.
- A report padded with quotes that support no pattern.
- A synthesis that ends with a roadmap instead of the next cheapest test.
- A pattern built from a single source presented as a signal.
- A report that hides which assumption the team was attached to.
- A synthesis that mixes English and Spanish inconsistently within a single section.

## Checklist before delivery

- [ ] Observed behavior and stated preference are kept separate.
- [ ] Every pattern carries a frequency count.
- [ ] Every pattern names a job-to-be-done free of solution language.
- [ ] Assumptions are marked confirmed, killed, or untouched, each with a citation.
- [ ] At least one assumption was killed, or the report states plainly why none were.
- [ ] Quotes appear only as evidence for a named pattern.
- [ ] The report ends with the next cheapest validation, not a feature list.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] The synthesis reads cleanly to a stranger who was not in the interviews.
