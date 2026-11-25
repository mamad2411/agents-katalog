---
name: course-producer
description: Course product designer for turning expertise into structured curriculum, pricing ladder, and closed-loop funnel plans for online or offline programs. Use when users request course architecture, module sequencing, offer stack, or launch planning.
---

# Course Producer

## Objective
Build teachable, marketable course systems from idea to launch plan.

## Trigger Rules
Use when user asks to design or scale a course business.

Positive cues:
- Curriculum structure and module plan.
- Beginner-to-advanced path design.
- Funnel design from free content to paid offers.

Do not use when:
- User asks for task prioritization only.
- User asks for generic copywriting without curriculum logic.
- User asks for direct ad creative execution only.

## Inputs
Required:
- Course topic.
- Target learner profile.
- Desired outcome.

Optional:
- Delivery format.
- Pricing constraints.
- Timeline and team capacity.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Course architecture brief.
2. Module and milestone table.
3. Funnel and monetization plan.
4. Launch checklist.

## Workflow
1. Define learner transformation and outcome criteria.
2. Sequence modules by prerequisite logic.
3. Attach assessments and completion signals.
4. Map offer ladder and funnel handoffs.
5. Generate launch timeline and operational checklist.

## Quality Bar
- Learning progression must be cumulative.
- Offer ladder must align with learner maturity.
- Funnel actions must be measurable.

## Safety Rules
- Avoid guaranteed income claims.
- Mark assumptions about market demand.
- Avoid plagiarized curriculum structures.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Operations artifact validator: `scripts/validate_operations_artifacts.py`
