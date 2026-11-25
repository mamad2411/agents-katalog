---
name: post-mortem
description: Use this skill when the user asks to write a post-mortem, run a retrospective on a shipped or failed project, analyze an incident, or capture lessons from a near-miss. Trigger phrases include "write the post-mortem", "run the retro", "debrief this incident", "what went wrong", "post-mortem de este incidente", "retro del proyecto", "lessons learned", "blameless retro". Produces a timeline of facts, contributing factors, action items with owners, and structural signals, without blaming individuals.
---

# post-mortem

> **Anchor:** A post-mortem is a tool for the next incident, not a trial for the last one.

## When to use

Use this skill when the user needs a structured retrospective on something that has already happened. Works for:

- An outage, security incident, or production bug with customer impact.
- A launch that failed to move the intended metric.
- A project that shipped late, over budget, or with features cut.
- A near-miss where the wrong outcome was avoided but barely.
- A recurring pattern of small failures that suggests a structural issue.

Do not use when:

- The user is red-teaming a plan before it executes. Use `red-team-review`.
- The user is evaluating a candidate after a failed hire. Use `candidate-evaluation`.
- The user is writing a scorecard for an ongoing vendor. Use `vendor-evaluation`.

## Philosophy

A post-mortem is a ritual, and rituals serve results. Three handbook concepts apply. **No heroes, no blame:** blaming individuals makes the next post-mortem harder to write honestly, and hides the structural conditions that produced the failure. The goal is to change the conditions, not to name a villain. **Rituals serve results:** a retro that follows the template but produces no change in how the team operates next time has failed. Every post-mortem closes with things that will be different, owned, and scheduled. **Cultural signals are delivery:** how the retro is run is itself the signal. A team that cannot hold a blameless conversation about a failure will deliver differently than one that can.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: post-mortem, incident, blameless, timeline, contributing factor, action item, owner, retro, near-miss, runbook, SEV-1, SEV-2, detection, recovery, rollback, comms, customer impact.
- **EN.** Direct US business register. Do not soften failure language.
- Names of services, systems, and environments stay as they are in the org.

## Method

### Step 1. Scope the retrospective

A vague scope produces a vague retro. Write:

- **What happened.** One paragraph in plain language, no jargon.
- **When.** Start and end timestamps with timezone, or date range for a project.
- **Who was affected.** Customers, internal users, partners, regulators. Numbers if available.
- **Severity.** If this is an incident, the formal severity. If a project retro, the business impact.
- **Type.** Incident, launch retro, project retro, near-miss, pattern review.

### Step 2. Build the timeline from facts

The timeline is the spine. It precedes analysis. Rules:

- Only facts. Time-ordered. Attributed to a system log, message, or named person's report.
- No interpretation yet. No "should have" or "could have".
- Include detection, mitigation, escalation, and recovery markers.
- Include external facts: customer tickets, press, regulator contact, if relevant.

If the timeline is disputed, flag the specific entry. Do not erase it.

### Step 3. Identify contributing factors, not a single cause

Failures are almost never a single cause. Write three to seven contributing factors. Each factor is:

- **The condition.** A property of the system, the process, or the context.
- **Why it contributed.** The specific way it made this failure more likely or worse.
- **Not a name.** A factor is never "X forgot to do Y". It is "the process did not catch that Y was missing".

Reframe any individual-level blame into the conditions that allowed the behavior.

### Step 4. What worked

Equal weight to what worked. This section is not a performative positive; it is essential for learning.

- **Detection.** Signals that fired fast and accurately.
- **Response.** Behaviors during the incident that limited damage.
- **Recovery.** Patterns that got the system back to green.
- **Communication.** Where the team, customers, and leadership were aligned.

What worked is what you want to scale. Name it with the same rigor as what did not.

### Step 5. What did not work

- **Detection gaps.** What was not signaling, or signaled too late.
- **Response gaps.** Where the runbook or escalation broke down.
- **Recovery gaps.** Where the rollback was absent, slow, or hazardous.
- **Communication gaps.** Where internal or external comms lagged or confused.
- **Decision gaps.** Where a decision was hard to make because the authority or information was missing.

### Step 6. Write action items that change conditions

Every contributing factor gets at least one action item, unless the team explicitly decides to accept the risk.

Each action item has:

- **The change.** A specific thing that will be different next time.
- **Owner.** Named person, not a team.
- **Due date.** Specific, not "soon".
- **How we will know it landed.** The signal that confirms the action took effect.
- **Kill criterion.** What would cause this action to be deprioritized or canceled.

Action items without owners, dates, and verification are wishes.

### Step 7. Capture structural and cultural signals

Some failures point at patterns beyond the specific incident. Call them out:

- **Structural.** "The on-call rotation is thin enough that one person's sick day caused the escalation to stall."
- **Cultural.** "The team did not surface concerns about this service earlier because the last time they did, the response was defensive."
- **Process.** "Changes of this class have shipped without a staging test three times in the last quarter."

These are for leadership to act on. Do not hide them in the body of the retro.

### Step 8. Name documentation to create or update

Most retros reveal missing or wrong docs. Be specific:

- **Runbook to create.** For the specific failure mode.
- **Runbook to update.** What changed.
- **Policy to revise.** If a policy allowed the failure.
- **Architecture note.** If a design decision needs to be recorded for the next team.

Link to the skills that can produce these (`documentation-extraction`).

### Step 9. Distribute and revisit

A post-mortem in a drawer is worse than no post-mortem. Define:

- **Audience.** Who must read this.
- **Publication channel.** Where it lives.
- **Revisit date.** When the team checks whether action items actually landed.
- **Deprecation signal.** When the post-mortem is closed for maintenance.

## Templates

- `templates/en/incident-post-mortem.md`: production incident retro.
- `templates/en/project-retro.md`: project, launch, or initiative retro.
- `templates/es/incident-post-mortem.md`: retro de incidente de producción.
- `templates/es/project-retro.md`: retro de proyecto, lanzamiento, o iniciativa.

## Related skills

- `red-team-review`: use it instead when the plan has not executed yet and you want a pre-mortem.
- `candidate-evaluation`: use it when the retro is on a failed hire and the rubric needs refining.
- `vendor-evaluation`: use it when scoring an ongoing vendor rather than a past incident.
- `documentation-extraction`: use it to turn the retro's runbook and doc gaps into durable docs.

## Anti-patterns

This skill must never produce:

- A post-mortem that names an individual as the cause.
- A timeline that is interpretive instead of factual.
- A "single root cause" in a system that obviously had several.
- Action items without owners, dates, or verification.
- A retro that buries cultural or structural signals inside the body.
- A retro that uses "learning opportunity" as a substitute for action.
- A retro that is never revisited.
- A post-mortem that quietly absolves the decision-makers who set the conditions.

## Checklist before delivery

- [ ] Scope, timing, affected parties, severity, and type are named.
- [ ] Timeline is facts-only, attributed, and time-ordered.
- [ ] Three to seven contributing factors are written, each framed as conditions.
- [ ] What worked is covered with the same rigor as what did not.
- [ ] Every contributing factor has at least one action item or an explicit risk acceptance.
- [ ] Every action item has owner, date, verification, and kill criterion.
- [ ] Structural and cultural signals are surfaced for leadership.
- [ ] Documentation to create or update is named.
- [ ] Audience, channel, and revisit date are named.
- [ ] No buzzwords from the voice rules appear.
