---
name: grainbound-causal-worldbuilding
description: Use when building, diagnosing, reverse-engineering, or revising fantasy and science-fiction worldbuilding with The Grainbound-style causal loops, environmental determinism, bottom-up culture design, OAC/WAC/WOAC reasoning, species or race biology, magic-as-environment, politics, factions, maps, religions, economies, and anti-vibe lore audits.
---

# Grainbound Causal Worldbuilding

Use this skill to turn lore from vibes into pressure-tested systems. Culture, politics, religion, economy, aesthetics, species traits, and maps must emerge from people or bodies solving problems under constraint.

## Quick Start

Use this skill for:

- Creating cultures from terrain, climate, resources, threats, bodies, or magic
- Reverse-engineering an existing trait, custom, aesthetic, law, ritual, faction, or species trope
- Diagnosing hollow or disconnected lore
- Designing believable political systems and faction conflict
- Turning maps, biology, and magic systems into story pressure
- Building AI IDE or `CLAUDE.md` worldbuilding workflows

Before substantial work:

- Load `references/method-map.md` for the condensed operating model.
- Load `references/output-contracts.md` when the user needs reusable templates or strict output shapes.
- Load `references/source-index.md` when the user asks where the principles came from or wants source refresh commands.

## Prime Directive

Do not invent top-down lore until the base layer exists.

Before government, religion, economy, art, status symbols, holidays, or social customs, define:

- Body or magic constraints, if non-human biology or magic matters
- Landscape: movement cost, visibility, defensibility, connectivity
- Climate: predictability, survival stress, resource cycling
- Resource profile: scarcity, abundance, storage, portability, control points
- Natural threats: predictability, frequency, defensibility

Every cultural detail must be traceable to a causal loop:

```xml
<reasoning>
Want:
Obstacle:
Action:
Consequence:
New pressure:
</reasoning>
```

Use `WOAC` for Want, Obstacle, Action, Consequence. `OAC` is acceptable shorthand only when the Want is obvious and stated nearby.

## Operating Loop

1. Identify the task type: forward build, reverse engineer, diagnosis, species design, politics, map audit, magic audit, or integration.
2. Extract user constraints: existing lore, must-keep aesthetics, genre, technology level, magic rules, geography, species biology, timeline, tone, and forbidden changes.
3. Build or recover the base layer before adding high-level institutions.
4. Run one or more WOAC cycles. Each consequence becomes the context for the next cycle.
5. Map consequences into the six-layer cultural stack.
6. Audit the five forces: environment, power, belief, exchange, and legacy.
7. Extract values from repeated actions, repeated obstacles, and permanent consequences.
8. Preserve contradictions that produce story pressure. Do not smooth them away.
9. Present only the lore needed for the user's current task, with causal links visible.

## Base-Layer Protocol

If the user asks for a culture, start here:

```text
Landscape:
- Movement cost:
- Visibility:
- Defensibility:
- Connectivity:

Climate:
- Predictability:
- Survival stress:
- Resource cycling:

Resource profile:
- Scarcity:
- Abundance:
- Storage:
- Portability:
- Control points:

Threat profile:
- Predictability:
- Frequency:
- Defensibility:
```

Rules:

- High movement cost tends to isolate and specialize communities.
- Low movement cost tends to increase trade, contact, and cultural blending.
- High visibility tends to reward speed, vigilance, reputation, scouting, and preemptive action.
- Low visibility tends to reward ambush, secrecy, traps, local knowledge, and fortified interiors.
- High defensibility tends to reward holding, gatekeeping, ritual continuity, and entrenched authority.
- Low defensibility tends to reward usefulness, alliances, mobility, deterrence, or tribute.
- Predictable climate can support calendars, bureaucracy, storage, and institutional authority.
- Unpredictable climate tends to reward neighbor-trust, hospitality, practical competence, and flexible leadership.
- High survival stress makes social rules strict because mistakes are expensive.
- Low survival stress allows more individual variation, slower institutions, and tolerated inefficiency.
- Resource cycling determines whether people trust stores, movement, favors, herds, routes, or institutions.

Treat these as pressure tendencies, not single-answer laws. The same pressure can produce rival cultures if groups solve the problem differently.

## Six-Layer Cultural Stack

Generate culture in this order:

1. Survival Strategy: How do they get calories, water, shelter, safety, and reproduction from this specific terrain, body, or magic constraint?
2. Social Organization: What coordination system does that survival strategy require?
3. Value Systems: Which behaviors must become honorable, sacred, shameful, or taboo to protect the coordination system?
4. Worldview and Religion: How do they explain threats, randomness, death, time, power, and uncontrollable forces?
5. Symbolic Culture: What architecture, clothing, art, music, tools, titles, and spatial layouts embody the values?
6. Cultural Expressions: What idioms, greetings, reflexes, food habits, rituals, etiquette, and daily defaults fall out of the deeper stack?

Do not fill these as separate wiki boxes. Each layer must answer a pressure from the layer beneath it.

## Reverse-Engineering Vibes

Use this when the user already has a cool trait and wants it to feel inevitable.

1. Pick one existing element: custom, visual, taboo, ritual, law, faction, caste, weapon, architecture, species trait, or holiday.
2. Run a reverse chain:

```text
Consequence: What exists now?
Action: What action would have created it?
Obstacle: What problem made that action necessary?
Want: What survival, power, belief, exchange, or legacy need drove the response?
Bedrock: geography, body, magic, historical event, or human universal
```

3. Ripple forward with: "If this is true, what else must be true?"
4. Audit all five forces so the culture does not become lopsided.
5. Extract values and contradictions from repeated actions, repeated obstacles, and permanent consequences.

Stop deep reverse when you reach bedrock: geography, biology/body, external magic, a historical event, or a human universal.

## Species, Race, and Magic

Treat the body as the first environment.

For each non-human species or biologically distinct group:

- What does the body give them that humans do not have?
- What does the body cost them that humans do not pay?
- What does the body make them experience that humans cannot?

Run one WOAC cycle per functional trait, then stack the consequences. Look for contradictions between traits. Those contradictions become internal factions, values in tension, and story engines.

Magic rule:

- If magic comes from the body, treat it as biology.
- If magic comes from the world, treat it as environment or resource geography.
- If only some bodies can use it, expect class structure, institutional control, fear, legitimacy struggles, or protection rackets.

## Politics

Politics asks two questions:

- Who controls what?
- Why does everyone else accept it?

Before designing titles or institutions, identify:

- Power centers: groups, offices, families, guilds, priesthoods, armies, councils, companies, charismatic individuals
- Currency of power: land, food, water, votes, trade routes, divine legitimacy, reputation, military force, debt, information, magic access
- Hidden enforcement: what threat, dependency, or credible force makes the visible system stick

Run WOAC between power centers. The throne, council, temple, or charter is furniture; the engine is wanting, blocking, maneuvering, and consequence.

For hierarchies, include middle layers. Loyalty is conditional, historical, and costly to maintain. Give vassals, clients, guild branches, officer corps, provinces, or sub-factions their own wants and cross-connections.

## Output Rule

When drafting final lore, keep the causal chain visible but concise. The user should be able to point at any detail and answer: "What pressure made this necessary, and what new pressure does it create?"

## Guardrails

- Use The Grainbound material as worldbuilding methodology only.
- Do not imitate Tony or The Grainbound's voice, persona, examples, or rhetorical style.
- Do not provide long transcript excerpts.
- Do not claim environmental pressure creates only one possible culture. It narrows plausible responses; people can still solve the same pressure differently.
- Do not let realism erase story usefulness. Preserve contradictions and pressure points characters can act on.
