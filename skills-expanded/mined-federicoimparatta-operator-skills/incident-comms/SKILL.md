---
name: incident-comms
description: Use this skill when the user needs to communicate during a live incident. Trigger phrases include "incident update", "status page update", "comms during an incident", "write an incident notice", "draft a resolution note", "all-clear message", "comunicado de incidente", "actualización de estado". Produces calm, factual updates while the incident is still moving. No heroes, no blame. Works in English and Rioplatense Spanish.
---

# incident-comms

> **Anchor:** No heroes, no blame, during the incident too. Say what is known, and when you will say more.

## When to use

Use this skill when the user needs to communicate while an incident is unfolding or just after it clears. Works for:

- A live incident that needs a public or internal status update before root cause is known.
- A status page entry that must say what is affected and when the next update lands.
- A resolution note that declares the all-clear and points to a forthcoming post-mortem.

Do not use when:

- The incident is over and the user needs root cause analysis. Use `post-mortem` instead.
- The user needs a routine status update with no active incident. Use `stakeholder-update`.

## Philosophy

Incident comms is a cultural artifact under stress. What you write while the system is on fire tells everyone who reads it how the team operates.

Two concepts apply directly. **No heroes, no blame:** during the incident too, not just in the retro. You do not name the person who pushed the change, you do not narrate a lone engineer saving the day, and you do not speculate about cause while people are still working. You say what is known, what is being done, and when the next update arrives. **Cultural signals are delivery:** the update is not overhead on top of the real work. A calm, specific, on-time update is how trust gets delivered to users and stakeholders during the worst moment. A vague or late update is a second incident.

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

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: incident, status page, rollback, deploy, root cause, post-mortem, SLA, downtime, mitigation. Do not translate those to Spanish equivalents that no one uses during an incident.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the update, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. State the impact in user terms, scope, and start time

Open with what the user cannot do, not with the internal component that failed. Name who is affected, what surface is degraded, and when it started. Avoid jargon that only the on-call team understands.

### Step 2. State current status and what is being done, without speculation

Say where the team is now: investigating, identified, mitigating, monitoring. Describe the action in progress. Do not guess at root cause and do not promise a fix time you cannot back. If cause is unknown, say it is unknown.

### Step 3. Commit to a next update time, always

Every in-progress update ends with when the next one comes. This is non-negotiable. Pick a concrete time or interval, even if the only news at that time is "still working on it". A missing next-update time is the most common failure of incident comms.

### Step 4. Give the workaround if one exists

If users can route around the problem, say how in one or two steps. If there is no workaround, say there is none rather than leaving it unsaid.

### Step 5. For the resolution note, switch to the all-clear variant

When the incident clears, the resolution note states: what was affected, the total duration, what is confirmed fixed, and a pointer to the forthcoming post-mortem. Do not bury the all-clear under preamble. Do not deliver root cause here; that is the post-mortem's job.

### Step 6. Never assign blame in real time

Do not name an individual, a team, or a vendor as the cause while the incident is live or in the resolution note. Attribution belongs in the post-mortem, written after the facts are in. In-flight blame is always wrong and always corrosive.

## Templates

- `templates/en/incident-update.md`: in-progress incident notice.
- `templates/en/resolution-note.md`: the all-clear after the incident.
- `templates/es/incident-update.md`: aviso de incidente en curso.
- `templates/es/resolution-note.md`: el all-clear después del incidente.

## Related skills

- `post-mortem`: use it after the incident clears to find and document root cause. Incident comms points to it, it does not replace it.
- `stakeholder-update`: use it for routine status when there is no active incident.
- `documentation-extraction`: use it to pull the incident timeline and updates into a durable record once the dust settles.

## Anti-patterns

This skill must never produce:

- An update that opens with the internal component name instead of user impact.
- An in-progress update with no committed next-update time.
- A message that speculates about root cause while the incident is live.
- A message that names a person, team, or vendor as the cause in real time.
- A resolution note that delivers root cause instead of pointing to the post-mortem.
- An update that narrates a single engineer heroically fixing the problem.
- A status update written in marketing voice instead of plain facts.
- A resolution note that buries the all-clear under preamble.
- An update that mixes English and Spanish inconsistently within a single section.
- A promise of a fix time the team cannot back.

## Checklist before delivery

- [ ] First line states user-facing impact, not the internal component.
- [ ] Scope and start time are named.
- [ ] Current status uses a known phase: investigating, identified, mitigating, monitoring.
- [ ] No speculation about root cause appears anywhere.
- [ ] In-progress updates commit to a concrete next-update time.
- [ ] Workaround is stated, or its absence is stated.
- [ ] Resolution note names duration, confirmed fixes, and points to the post-mortem.
- [ ] No person, team, or vendor is blamed in real time.
- [ ] No buzzwords from the voice rules appear anywhere.
