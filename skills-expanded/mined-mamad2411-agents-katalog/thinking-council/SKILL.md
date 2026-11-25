---
name: thinking-council
description: |
  Structured deliberation with 4 advisors illuminating a question from
  different perspectives. Inspired by Daniel Miessler's Council pattern.
  Visible transcript of the debate.

  [WHAT] Convene a council of 4 distinct perspectives (expert roles fitted
  to the question) that debate, challenge, and build on each other's
  arguments. Produces a visible transcript with conclusion and action recommendation.

  [WHEN] Use when: council, deliberate, multiple perspectives, weigh arguments,
  structured debate, "I need to think this through"

  [EXPERTISE] Structured deliberation, multi-perspective analysis, dialectical reasoning
argument-hint: "[question to deliberate]"
allowed-tools: Read, Grep, Glob, Write, WebSearch, WebFetch
---

# The Council

**Role:** structured deliberation with 4 perspectives.
**Tone:** respectful but honest. Each advisor is genuine in their perspective.

## How the Council works

1. **Question is presented** (from $ARGUMENTS or the user's prompt)
2. **4 advisors are selected** based on the question's domain
3. **3 deliberation rounds** with a visible transcript
4. **Conclusion** with consensus, dissent, and a recommendation

## Selecting advisors

Pick 4 roles that MAXIMISE perspective spread. At least one must be contrarian.

**Example role pools:**

| Question domain | Possible advisors |
|---|---|
| Policy/society | Political scientist, practitioner, activist, economist |
| Tech/architecture | Architect, security expert, end user, ops engineer |
| Research | Supervisor, critical opponent, industry person, peer doctoral student |
| Strategy | Optimist, pessimist, historian, pragmatist |
| Security/threats | Defender, attacker, analyst, decision-maker |

Advisors must NOT be generic. Name them, give them background, make them specific.

## Deliberation protocol

### Round 1: opening statements
Each advisor presents their position in 3-5 sentences. Clear stance.

### Round 2: challenge and depth
Each advisor reacts to the others' positions. Identifies blind spots, builds on, challenges assumptions. The contrarian role MUST challenge consensus.

### Round 3: synthesis and closing words
Each advisor offers their closing word in light of what they've heard. Have they changed their mind? What remains?

## Output format

```markdown
## Council on: [The question]

### Advisors
- **[Name]** — [Role/background, 1 sentence]
- **[Name]** — [Role/background, 1 sentence]
- **[Name]** — [Role/background, 1 sentence]
- **[Name]** — [Role/background, 1 sentence]

### Round 1: opening statements

**[Name]:** [Position]

**[Name]:** [Position]

**[Name]:** [Position]

**[Name]:** [Position]

### Round 2: challenge

[Free format, advisors interact]

### Round 3: closing words

[Each advisor summarises]

### The Council's conclusion

**Consensus:** [What the council agrees on]
**Dissent:** [Where disagreement remains]
**Recommendation:** [Action recommendation to the user]
```

## Round-by-round transcript

**A visible transcript is mandatory.** The Council's value lies in the debate, not the conclusion. The user must be able to follow each advisor's position round by round and see WHERE views shift or harden.

- Mark **ROUND 1**, **ROUND 2**, **ROUND 3** clearly as headings
- Per round: all 4 advisors in the same order, so position shifts are visible
- In round 3: explicitly note if an advisor has **changed position** (and why) or **hardened** (why they remain unconvinced)
- The conclusion comes AFTER the transcript, not instead of it

## Rules

- Advisors are NEVER unanimous from the start. If everyone agrees, swap one out.
- The contrarian role is mandatory and must be genuinely challenging, not a straw man.
- The transcript should be readable and interesting, not mechanical.
- The user can interrupt between rounds with questions or adjustments.
- Advisors should reference real thinkers, data, and examples where relevant.
