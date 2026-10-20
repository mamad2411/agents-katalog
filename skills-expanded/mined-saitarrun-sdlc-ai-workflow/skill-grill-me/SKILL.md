---
name: skill-grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me", "stress test", "poke holes", "challenge my plan".
version: 1.0.0
---

# Skill: Grill Me

Relentless design/plan review via structured interview. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. Reach shared understanding by testing assumptions and exposing gaps.

## Process

1. **Parse the plan/design** — Identify key decisions, dependencies, assumptions
2. **Ask one question at a time** — Deep on one branch; await answer before moving
3. **Explore codebase first** — If a question is answerable by code inspection, do that instead of asking
4. **Provide recommended answer** — For each question, suggest what you think is the right call (so user can react faster)
5. **Resolve branch completely** — Don't jump to another decision until this one is fully understood
6. **Walk dependency tree** — Only move to dependent decisions once blockers are cleared
7. **Reach shared understanding** — Stop when both agree on the plan or user signals done

## Question Structure

For each question:

```
**Q: [Question]**

My take: [Your recommended answer + reasoning]

What do you think?
```

## When to Explore Code Instead

If user hasn't answered a question yet:
- Design decision that's already implemented? Read the code.
- Architecture pattern already in repo? Grep for examples.
- Library choice already wired? Check package.json / imports.

This avoids asking about settled questions.

## Decision Tree Example

```
Plan: Add user authentication

├─ Auth mechanism? (OAuth vs. session vs. JWT)
│  └─ Once decided → ask: which provider?
│     └─ Once decided → ask: token expiry strategy?
│        └─ Once decided → ask: refresh token rotation?
│
├─ DB schema for sessions/tokens?
│  └─ Once decided → ask: cleanup/revocation strategy?
│
├─ Rate limiting & brute force?
│  └─ Once decided → ask: lockout duration vs. progressive delay?
```

Only ask dependent questions after parent is resolved.

## Stopping

**User says**: "stop grill", "that's enough", "I'm confident now"  
**You decide**: "We've resolved the full decision tree and reached agreement."

---

**Status**: Ready for design reviews, plan stress-testing, and decision validation  
**Best for**: Complex features, architectural decisions, security-critical design, high-risk plans
