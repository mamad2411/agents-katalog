---
name: cross-functional-collab
description: Use this skill when working with designers, product managers, business stakeholders, or non-technical team members. Trigger on keywords: working with PM, designer collaboration, stakeholder, business requirements, cross-team, non-technical, translate requirements, align with product, pushback from business.
---

# Cross-Functional Collaboration

## The Translation Problem

Developers think in systems. PMs think in outcomes. Designers think in experiences. Executives think in risk and cost. None of these are wrong — they're just different lenses on the same reality.

**Your job:** Translate fluently between all of them.

---

## Working with Product Managers

### What PMs Need From You
- Honest estimates (not optimistic, not padded)
- Technical risk flagged early — surprises are worse than bad news
- Alternatives when you can't build exactly what they ask
- Business impact framing when you need to deprioritize tech debt

### What You Need From PMs
- Clear acceptance criteria before you start
- Priority when scope is too large for the sprint
- Access to users when requirements are ambiguous
- Decision authority on trade-offs they create

### Handling Unrealistic Requests
```
WRONG: "That's not possible"
RIGHT: "I can build [what they asked] in 3 weeks, or 
        I can build [simpler version that achieves the same goal] 
        in 3 days. Which would you prefer given the timeline?"
```

Always offer an alternative, not just a no.

---

## Working with Designers

### Collaboration Principles
- Review designs before implementation starts — not after
- Flag technical constraints early: "This animation would cost 3x more than a simpler one"
- Suggest technically feasible alternatives that preserve design intent
- Implement exactly what's designed, or discuss changes before deviating

### Common Friction Points
| Design asks for | Technical reality | How to bridge |
|---|---|---|
| Pixel-perfect animation | Expensive on low-end devices | Discuss progressive enhancement |
| Complex custom component | Library component exists | Show the library option, let them decide |
| Real-time updates everywhere | WebSocket complexity | Agree on which features justify real-time |

---

## Translating Technical Decisions to Business Language

| Instead of | Say |
|---|---|
| "We need to refactor the auth module" | "Our login system has reliability issues that affect 5% of users. Fixing it takes 1 week now or 1 month when it fails in production." |
| "We have technical debt" | "We've accumulated shortcuts that are slowing us down. We're shipping 30% slower than 6 months ago because of them." |
| "We need to upgrade our database" | "Our current database won't handle the load at 2x our current user base. Upgrading now costs X. Waiting until it fails costs 5x." |

---

## Disagreeing Professionally

When you disagree with a non-technical decision:
```
1. Understand first — "Help me understand the reasoning behind this"
2. State your concern clearly — "My concern is [specific risk/impact]"
3. Propose an alternative — "What if we tried [approach] instead?"
4. Accept the decision — if they proceed anyway, commit fully
5. Document your concern — brief note in the ticket/PR
```

Disagreeing → discussing → deciding → committing is healthy.
Disagreeing → grumbling → passive resistance is not.
