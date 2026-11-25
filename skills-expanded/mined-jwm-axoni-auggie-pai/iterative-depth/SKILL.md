---
name: iterative-depth
description: Multi-angle deep exploration through cognitive lenses, each pass surfaces requirements and insights invisible from other angles. USE WHEN iterative depth, multi-angle, deep exploration, multiple passes, lenses, thorough analysis, edge cases, hidden requirements.
---

# Iterative Depth: Multi-Angle Deep Exploration

Structured multi-angle exploration of the same problem through cognitive lenses. Each pass surfaces requirements, edge cases, and insights invisible from other angles. Grounded in 20 established techniques across cognitive science, AI/ML, requirements engineering, and design thinking.

## Customization

Check for user customizations at:
`~/.augment/USER/SKILLCUSTOMIZATIONS/IterativeDepth/PREFERENCES.md`

If this file exists, load and apply preferences found there. They override defaults below.

## Core Concept

Instead of analyzing a problem once, run 2-8 structured passes through the same problem, each from a systematically different lens. The combination yields understanding that no single-pass analysis can produce.

**Why it works:**
1. **Perspective Blindness Compensation** -- Any single viewpoint has blind spots. Rotating through viewpoints covers gaps.
2. **Progressive Pre-Understanding** -- Each pass updates understanding, making subsequent passes more perceptive.
3. **Convergence Signal** -- When multiple lenses surface the same insight, it is high-priority.

## The 8 Lenses

Ordered from most concrete to most abstract, and from most commonly useful to most specialized.

### Lens 1: LITERAL (Surface Requirements)
**Question:** "What did they explicitly say? What are the concrete, stated requirements?"
Extract every stated requirement, constraint, preference. No interpretation -- only what was said.

### Lens 2: STAKEHOLDER (Who Else Cares?)
**Question:** "Who are all the people, systems, and entities affected? What does each need?"
Identify every stakeholder beyond the requester: end users, maintainers, admins, downstream systems, future developers.

### Lens 3: FAILURE (What Goes Wrong?)
**Question:** "What could fail? What would an adversary exploit? What are the edge cases?"
Assume the solution exists. Break it. Error states, race conditions, security holes, performance under load.

### Lens 4: TEMPORAL (Past, Present, Future)
**Question:** "How does this change over time? What happens in 6 months?"
Why does this problem exist now? What changes in the future that would break this solution? Migration paths, backwards compatibility.

### Lens 5: EXPERIENTIAL (How Should It Feel?)
**Question:** "When this works perfectly, how does the user FEEL?"
Beyond functional correctness: speed, elegance, confidence, trust. The difference between "works" and "works beautifully."

### Lens 6: CONSTRAINT INVERSION (What If?)
**Question:** "What if we removed all constraints? What if we added extreme ones?"
Remove assumed constraints -- what would we build? Add extreme constraints -- what is truly essential? Both reveal hidden assumptions.

### Lens 7: ANALOGICAL (What Patterns Apply?)
**Question:** "What similar problems have been solved before? What patterns from other domains apply?"
This problem is not unique. What emerged in other codebases, industries, fields?

### Lens 8: META (Is This the Right Question?)
**Question:** "Are we solving the right problem? Is the framing itself correct?"
Step outside the problem. Is the request a symptom of a deeper issue? Would a different question yield a better outcome?

## Depth Selection

| Depth | Lenses Used | Which Ones | Best For |
|-------|-------------|------------|----------|
| **Quick** | 2 | Literal + Failure | Fast validation, simple tasks |
| **Standard** | 4 | Literal + Stakeholder + Failure + Experiential | Most tasks |
| **Deep** | 8 | All 8 lenses | Complex problems, high stakes |

When invoked with a specific count (e.g., "do 3 passes"), select lenses in order from Lens 1 through Lens N.

### Domain-Specific Lens Priority

| Domain | Prioritized Lenses |
|--------|--------------------|
| **Security-focused** | Failure, Stakeholder, Temporal |
| **UX-focused** | Experiential, Stakeholder, Literal |
| **Architecture** | Temporal, Constraint Inversion, Analogical |
| **Ambiguous request** | Meta, Stakeholder, Literal |

## Execution Process

### Step 1: Determine Depth
Based on complexity, user request, or stakes. Default to Standard (4 lenses) if unclear.

### Step 2: Run Passes Sequentially

For each lens, produce:

```
ITERATIVE DEPTH -- Pass [i]/[N]: [LENS NAME]

Lens Question: "[The lens's core question]"

Findings:
- [Finding 1 -- potential criterion or insight]
- [Finding 2 -- potential criterion or insight]
- [Finding 3 -- refinement of something found in earlier pass]

New Insights:
+ [New insight this lens uniquely reveals]
~ [Refined insight -- was X, now Y based on this angle]
```

### Step 3: Synthesize

After all passes:

1. **Deduplicate** -- Remove semantically identical findings across lenses
2. **Merge refinements** -- If multiple lenses refined the same finding, take the most specific version
3. **Prioritize** -- Order by how many lenses surfaced the insight (consensus = high priority)
4. **Identify the key insight** -- The most surprising finding that single-pass analysis would have missed

## Output Format

```markdown
## Iterative Depth Analysis: [Topic]

### Coverage
- Lenses used: [list]
- New insights discovered: [count]
- Existing insights refined: [count]

### Findings by Lens
[Summary of each lens pass with key findings]

### Consolidated Insights (Priority Order)
1. [Highest priority -- surfaced by multiple lenses]
2. [Second priority]
3. [Third priority]
...

### Key Insight
[The most surprising finding across all lenses -- the thing single-pass analysis would have missed]
```

## Scientific Foundation

This technique draws from validated methods across disciplines:

| Technique | Source | How It Maps |
|-----------|--------|-------------|
| Hermeneutic Circle | Gadamer, 1960 | Each pass refines pre-understanding |
| Triangulation | Denzin, 1970 | Each lens is a different method on same problem |
| Six Thinking Hats | de Bono, 1985 | Structured perspectives applied sequentially |
| Self-Consistency | Wang et al., 2022 | Multiple reasoning paths yield better answers |
| Viewpoint-Oriented RE | Finkelstein & Nuseibeh, 1992 | Multiple stakeholder viewpoints reveal hidden requirements |
| Cognitive Flexibility | Spiro et al., 1988 | "Criss-crossing" a concept from different directions |
| Causal Layered Analysis | Inayatullah, 1998 | Progressive depth through layers |

## Anti-Patterns

- **Repetitive Passes**: Each lens must be structurally different, not just a re-run with slight variation
- **Skipping Synthesis**: Running all lenses but not consolidating defeats the purpose
- **Surface-Only**: Using lenses as checklists rather than genuinely exploring from each angle
- **Over-Depth**: Using 8 lenses on a simple task that needs 2 -- match depth to stakes
- **Ignoring Convergence**: When multiple lenses find the same thing, it is a strong signal -- do not dismiss it
