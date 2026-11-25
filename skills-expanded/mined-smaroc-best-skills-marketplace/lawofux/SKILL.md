---
name: lawofux
description: "Apply Laws of UX (lawsofux.com) principles to design and build winning customer experiences. 30 psychology-backed UX laws covering usability, perception, memory, decision-making, and interaction design. Use when the user says 'lawofux', 'laws of ux', or asks to design an app, modify UI/UX, review UX, build a user interface, improve user experience, create a landing page, design a dashboard, or any task involving UI design, app design, or UX optimization."
---

# Laws of UX

Apply 30 evidence-based UX laws from lawsofux.com to every design decision. Reference: [references/laws.md](references/laws.md) for full details on each law.

## Workflow

### 1. Analyze the Task

Identify which UX laws are most relevant to the current design task:

| Task Type | Primary Laws to Apply |
|---|---|
| **Navigation/IA** | Hick's Law, Serial Position Effect, Miller's Law, Chunking |
| **Forms/Input** | Postel's Law, Doherty Threshold, Goal-Gradient, Tesler's Law |
| **Landing/Marketing** | Aesthetic-Usability, Von Restorff, Peak-End Rule, Fitts's Law |
| **Dashboards/Data** | Cognitive Load, Law of Proximity, Chunking, Law of Pragnanz |
| **Onboarding** | Paradox of Active User, Hick's Law, Zeigarnik Effect, Goal-Gradient |
| **E-commerce** | Choice Overload, Serial Position, Jakob's Law, Peak-End Rule |
| **Mobile** | Fitts's Law, Miller's Law, Flow, Doherty Threshold |
| **Settings/Config** | Tesler's Law, Pareto Principle, Hick's Law, Occam's Razor |

### 2. Apply Laws During Design

For every UI component or screen, run through this checklist:

**Reduce Friction**
- Choices minimized at each step? (Hick's Law)
- Info chunked into digestible groups? (Miller's Law, Chunking)
- System responds <400ms? (Doherty Threshold)
- Complexity absorbed by system, not user? (Tesler's Law)

**Guide Attention**
- Primary CTA visually distinct? (Von Restorff Effect)
- Important items at start/end of sequences? (Serial Position Effect)
- Related elements grouped spatially? (Law of Proximity)
- Similar elements styled consistently? (Law of Similarity)

**Match Expectations**
- Standard patterns used? (Jakob's Law)
- Input handled flexibly? (Postel's Law)
- Interface self-explanatory without docs? (Paradox of Active User)
- Design matches users' mental models? (Mental Model)

**Drive Completion**
- Progress clearly shown? (Goal-Gradient Effect, Zeigarnik Effect)
- Positive peak moments designed in? (Peak-End Rule)
- Touch targets large enough? (Fitts's Law — min 44px)
- Users can maintain flow state? (Flow)

### 3. Document Decisions

When presenting designs, briefly note which laws informed key decisions:

```
// CTA button: 48px height, high-contrast color (Fitts's Law + Von Restorff)
// Nav: 5 items max, key actions at edges (Hick's Law + Serial Position)
// Form: 3-step wizard with progress bar (Goal-Gradient + Chunking)
```

## Quick Reference — Top 10 Laws for Every Project

1. **Jakob's Law** — Follow existing conventions. Don't reinvent patterns.
2. **Hick's Law** — Fewer choices = faster decisions. Progressive disclosure.
3. **Fitts's Law** — Big targets, close to thumb. Min 44px touch targets.
4. **Miller's Law** — Chunk content into groups of 5-7 related items.
5. **Doherty Threshold** — Keep response times under 400ms. Use skeleton screens.
6. **Von Restorff Effect** — One distinctive CTA per view. Don't over-highlight.
7. **Law of Proximity** — Spacing defines grouping. Labels near their fields.
8. **Peak-End Rule** — Celebrate completions. Smooth error recovery.
9. **Tesler's Law** — Absorb complexity in code, not in the user's face.
10. **Postel's Law** — Accept messy input gracefully. Auto-format.

## Full Law Details

Read [references/laws.md](references/laws.md) for complete descriptions, origins, takeaways, and application guidance for all 30 laws.
