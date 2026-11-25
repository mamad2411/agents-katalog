---
name: jobs-to-be-done
description: "Applies the Jobs-to-Be-Done (JTBD) framework to frame customer needs as job statements and identify underserved needs. Based on the work of Clayton Christensen and Tony Ulwick's Outcome-Driven Innovation methodology."
category: discovery
default_depth: standard
---

# Jobs-to-Be-Done Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Applies the Jobs-to-Be-Done (JTBD) framework to frame customer needs as job statements and identify underserved needs. Based on the work of Clayton Christensen and Tony Ulwick's Outcome-Driven Innovation methodology.

## When to Use

- Reframing product strategy around customer outcomes instead of features
- Identifying new market opportunities by finding underserved jobs
- Writing better user stories grounded in real customer motivation
- Evaluating whether a proposed feature actually addresses a meaningful job

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick reframe of a feature request into a job statement | Step 1 (Identify the Core Job) only |
| **Standard** | Discovery cycle scoping or roadmap prioritization | All steps |
| **Deep** | New market entry or Outcome-Driven Innovation initiative | All steps + emotional/social job elaboration per step, switching cost analysis, non-consumption deep dive |

**Omit rules:** At Light depth, skip Steps 2-5 (Job Map, Outcomes, Opportunity Scoring, Competing Solutions). Produce only the core job statement with functional/emotional/social layers.

## Key Concepts

**Job:** The progress a customer is trying to make in a particular circumstance. Jobs are stable over time, technology changes, jobs don't.

**Three layers of jobs:**
1. **Functional job**, The practical task (e.g., "get from A to B quickly")
2. **Emotional job**, How they want to feel (e.g., "feel confident I'll arrive on time")
3. **Social job**, How they want to be perceived (e.g., "appear responsible to my team")

**Hiring and firing:** Customers "hire" products to do a job and "fire" them when something does it better.

## Framework

### Step 1: Identify the Core Job

Work with the PM to articulate the main job using the canonical format:

```
When I [situation/context],
I want to [motivation/goal],
So I can [desired outcome].
```

**Rules for good job statements:**
- Describe the customer's goal, not your product's function
- Include the triggering context, jobs exist in situations
- Focus on outcomes, not solutions
- Should be solution-agnostic (no product names or feature names)

**Example:**
```
When I'm preparing for a board meeting,
I want to quickly assemble key metrics into a narrative,
So I can demonstrate progress and maintain investor confidence.
```

### Step 2: Map the Job Steps

Break the core job into its constituent steps using the Universal Job Map:

| Step | Description | Questions to Ask |
|---|---|---|
| 1. Define | What needs to be accomplished? | "How do you figure out what needs doing?" |
| 2. Locate | Find inputs needed | "Where do you get what you need to start?" |
| 3. Prepare | Set up for execution | "What preparation is required?" |
| 4. Confirm | Verify readiness | "How do you know you're ready to proceed?" |
| 5. Execute | Perform the core task | "Walk me through doing the actual thing" |
| 6. Monitor | Track progress | "How do you know it's going well?" |
| 7. Modify | Make adjustments | "What do you do when things go wrong?" |
| 8. Conclude | Finish and clean up | "How do you wrap up?" |

### Step 3: Identify Desired Outcomes

For each job step, define what success looks like using Outcome Statements:

```
[Direction] + [metric] + [object of control] + [contextual qualifier]

Examples:
- Minimize the time it takes to gather data from multiple sources
- Minimize the likelihood of presenting outdated metrics
- Increase the confidence that the narrative matches the data
```

**Rules:**
- Start with a direction: Minimize, Increase, Reduce, Maximize
- Reference something measurable, even if not precisely quantified
- Keep solution-agnostic, no product or feature names

### Step 4: Assess Satisfaction (Opportunity Scoring)

For each outcome, assess:
- **Importance** (1-10): How much does this matter to the customer?
- **Satisfaction** (1-10): How well is this currently served?

**Opportunity Score** = Importance + max(Importance - Satisfaction, 0)

| Score Range | Interpretation |
|---|---|
| 15-20 | Underserved, high opportunity |
| 10-14 | Appropriately served, moderate opportunity |
| 0-9 | Overserved, low opportunity (or table stakes) |

### Step 5: Identify Competing Solutions

Map what customers currently "hire" to do this job:
- Direct competitors (same category)
- Indirect competitors (different category, same job)
- Non-consumption (doing nothing or manual workarounds)

## Minimum Evidence Bar

**Required inputs:** Target persona or segment and a description of the problem space or feature area to analyze.

**Acceptable evidence:** Customer interview transcripts, support tickets, survey verbatims, behavioral analytics, sales call recordings, or documented workaround observations.

**Insufficient evidence:** If no customer evidence exists (only stakeholder opinions or feature requests), state "Insufficient evidence for opportunity scoring" and produce a partial artifact with job statements drafted as hypotheses and scoring sections marked `[TBD, requires: customer interview data or behavioral analytics]`; flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Opportunity scores (Step 4) and competing solutions (Step 5) must be grounded in evidence or sourced data.
- **Hypotheses:** Job statements (Step 1) and job maps (Step 2) may be drafted speculatively when evidence is thin, label as "hypothesis" and flag for validation.

## Output Format

```markdown
# Jobs-to-Be-Done Analysis: [Domain]

## Core Job Statement
When I [context], I want to [goal], So I can [outcome].

## Job Map
| Step | Customer Activity | Pain Points | Current Workarounds |
|---|---|---|---|
| Define | ... | ... | ... |
| [etc.] | | | |

## Desired Outcomes (ranked by opportunity score)
| # | Outcome Statement | Importance | Satisfaction | Opp. Score |
|---|---|---|---|---|
| 1 | Minimize the time to... | 9 | 3 | 15 |
| [etc.] | | | | |

## Competitive Landscape (by job, not by product)
| Solution Hired | Job Steps Served | Strengths | Weaknesses |
|---|---|---|---|

## Underserved Opportunities
[Top 3-5 outcomes with highest opportunity scores, with strategic implications]

## Framed Options
[Top underserved opportunities with possible next steps, prototype tests, deeper research, etc.]
```

**Shipwright Signature (required closing):**
8. **Decision Frame**, Top underserved opportunities worth pursuing, trade-off between breadth of jobs vs. depth of scoring, confidence in opportunity scores with evidence quality, owner, decision date, revisit trigger
9. **Unknowns & Evidence Gaps**, Job steps with no customer evidence, outcomes scored on assumption rather than data
10. **Pass/Fail Readiness**, PASS if the core job statement is solution-agnostic and every scored outcome is backed by evidence. At Light depth, PASS requires the functional, emotional, and social layers; outcome scoring is not required. Do not invent outcomes to make a list longer: if evidence does not identify a material outcome, record that gap and avoid a prioritized-outcome recommendation. FAIL if job statements contain product or feature names, or all scores are assumed.
11. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Defining jobs as features**, "I want to use a Gantt chart" is a solution, not a job
- **Ignoring context**, Jobs only make sense in specific situations
- **Skipping emotional and social jobs**, Functional alone misses half the picture
- **Surveying importance without satisfaction**, You need both to find opportunity
- **Competitor analysis by product instead of by job**, Your real competition might not be in your category

## Weak vs. Strong Output

**Weak:**
> "When I need to manage projects, I want a better tool, so I can be more productive."

Contains a solution ("better tool"), vague outcome ("more productive"), and no triggering context.

**Strong:**
> "When I'm coordinating a cross-functional launch with 4+ teams, I want to see who's blocked and why without chasing status updates, so I can unblock dependencies before they delay the ship date."

Solution-agnostic, specific context with a threshold, measurable outcome tied to a real consequence.
