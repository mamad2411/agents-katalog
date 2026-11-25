---
name: customer-journey-mapping
description: "Creates end-to-end customer journey maps with stages, touchpoints, actions, emotions, pain points, and moments of truth. Produces maps that connect the experience layer to product opportunities and measurement points."
category: customer-intelligence
default_depth: standard
---

# Customer Journey Mapping

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Creates end-to-end customer journey maps with stages, touchpoints, actions, emotions, pain points, and moments of truth. Produces maps that connect the experience layer to product opportunities and measurement points.

## When to Use

- Redesigning a core product experience (onboarding, upgrade, renewal)
- Aligning cross-functional teams on the end-to-end customer experience
- Identifying the highest-leverage improvement opportunities in the user lifecycle
- Preparing for a design sprint or UX research initiative
- Onboarding new team members to understand the customer experience holistically

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick alignment artifact for a single journey segment (e.g., onboarding only) | Define Scope & Persona, Map the Stages, one stage Detail |
| **Standard** | Full end-to-end journey map for a redesign or cross-functional alignment | All sections |
| **Deep** | Multi-persona or multi-journey mapping with service blueprint and measurement plan | All sections + backstage service blueprint, persona variant overlays, instrumentation plan |

**Omit rules:** At Light depth, skip Identify Cross-Stage Patterns and Measurement Framework. Produce only a stage map with pain points and top opportunities for the scoped segment.

## Framework

### Step 1: Define Scope & Persona

```markdown
## Journey Map Scope

**Persona:** [Name, from your persona library]
**Journey:** [Which journey, e.g., "First-time user from signup to first value moment"]
**Trigger:** [What initiates this journey, e.g., "Colleague shares a link to a project"]
**End state:** [What "done" looks like, e.g., "User has created their first project and invited a teammate"]
**Time span:** [Minutes / Hours / Days / Weeks]
```

### Step 2: Map the Stages

Break the journey into high-level stages:

```markdown
## Journey Stages

| Stage | Description | Duration | Entry Trigger | Exit Trigger |
|---|---|---|---|---|
| 1. Awareness | Discovers the product exists | Variable | [trigger] | Visits website/app |
| 2. Evaluation | Assesses whether it fits their need | [time] | Visits site | Signs up / leaves |
| 3. Onboarding | First-run experience | [time] | Signs up | Reaches activation |
| 4. First Value | Achieves the core outcome | [time] | Completes setup | "Aha moment" |
| 5. Habit | Incorporates into routine | [time] | First value | Regular usage |
| 6. Expansion | Deepens usage or upgrades | [time] | Habit formed | More features / seats |
```

### Step 3: Detail Each Stage

For each stage, map the full experience:

```markdown
### Stage [N]: [Name]

**User goal:** [What they're trying to accomplish at this stage]

#### Touchpoints & Actions
| Touchpoint | Channel | User Action | System Response |
|---|---|---|---|
| [Landing page] | Web | Reads headline, scans features | Page load, social proof |
| [Signup form] | Web | Enters email, creates password | Validation, welcome email |
| [Onboarding wizard] | In-app | Follows guided setup | Progress indicators |

#### Emotional Journey
| Moment | Emotion | Intensity (1-5) | Trigger |
|---|---|---|---|
| [Seeing the landing page] | Curious | 3 | [Clear headline] |
| [Hitting a confusing step] | Frustrated | 4 | [Unclear UI label] |
| [Completing first task] | Satisfied | 5 | [Visible result] |

#### Pain Points
| Pain Point | Severity | Evidence | Frequency |
|---|---|---|---|
| [Can't find the next step] | High | [Support tickets, session recordings] | [X% of users] |
| [Loading time too long] | Medium | [Analytics, NPS comments] | [X% of sessions] |

#### Moments of Truth
Critical decision points where the user decides to continue or leave:

- **MOT 1:** [Description, e.g., "User sees the empty state after signup"]
  - Current experience: [What happens now]
  - Ideal experience: [What should happen]
  - Drop-off rate: [X]% of users leave at this point

#### Opportunities
| Opportunity | Impact | Effort | Quick Win? |
|---|---|---|---|
| [Improve empty state with templates] | High | Small | Yes |
| [Add progress indicator to onboarding] | Medium | Small | Yes |
| [Redesign signup flow] | High | Large | No |
```

### Step 4: Identify Cross-Stage Patterns

```markdown
## Cross-Stage Analysis

### Emotional Arc
[Describe the overall emotional trajectory, where are the peaks and valleys?]

### Critical Drop-Off Points
| Transition | Drop-Off Rate | Primary Reason | Opportunity |
|---|---|---|---|
| Evaluation → Signup | [X]% | [reason] | [opportunity] |
| Signup → Activation | [X]% | [reason] | [opportunity] |
| Activation → Habit | [X]% | [reason] | [opportunity] |

### Moments of Delight
- [Moment 1]: [What makes users happy, protect and amplify this]
- [Moment 2]: [Another positive moment to preserve]

### Channel Consistency Gaps
| Touchpoint A | Touchpoint B | Inconsistency | Impact |
|---|---|---|---|
| [Website messaging] | [In-app experience] | [Promise vs. reality gap] | [Disappointment at onboarding] |

### Service Blueprinting (Backstage)
| Frontstage Action | Backstage Process | Support System | Failure Point |
|---|---|---|---|
| [User clicks "Get Started"] | [Account provisioning] | [Auth service] | [Timeout under load] |
```

### Step 5: Measurement Framework

```markdown
## Journey Metrics

| Stage | Key Metric | Current | Target | Data Source |
|---|---|---|---|---|
| Awareness | Website visits from target segment | [N] | [target] | [Analytics] |
| Evaluation | Signup conversion rate | [X]% | [target] | [Analytics] |
| Onboarding | Onboarding completion rate | [X]% | [target] | [Product analytics] |
| First Value | Time to first value (TTFV) | [X days] | [target] | [Product analytics] |
| Habit | Day-30 retention | [X]% | [target] | [Product analytics] |
| Expansion | Expansion revenue rate | [X]% | [target] | [Billing] |
```

## Minimum Evidence Bar

**Required inputs:** A defined persona (or target user description), at least one data source per journey stage (analytics, research, or support data), and a clear journey scope (trigger and end state).

**Acceptable evidence:** Product analytics (funnels, drop-offs, TTFV), user research transcripts, session recordings, support ticket patterns, NPS/CSAT by stage, onboarding completion data.

**Insufficient evidence:** If a journey stage has no analytics and no qualitative research, state "Insufficient evidence for Stage [N] detail" and produce a partial artifact with evidenced stages fully mapped and unsupported stages marked `[TBD, requires: analytics instrumentation or user interviews for this stage]`. Flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Drop-off rates, touchpoint sequences, and documented pain points must be grounded in observed data.
- **Hypotheses:** Emotional journey intensities and moment-of-truth impact estimates may be inferred, label them "Hypothesis, validate with research" when not sourced from direct user input.

## Output Format

Produce a Customer Journey Map with:
1. **Scope & Persona**, who and what journey
2. **Stage Map**, high-level journey stages
3. **Stage Details**, touchpoints, emotions, pain points, moments of truth per stage
4. **Cross-Stage Analysis**, drop-offs, patterns, delight moments
5. **Opportunity Register**, prioritized list of improvements
6. **Measurement Framework**, metrics per stage

**Shipwright Signature (required closing):**
7. **Decision Frame**, experience findings and improvement options with expected impact, trade-offs (quick wins vs. structural redesigns), confidence level with evidence quality, owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, stages with no analytics or research coverage, emotional journey assumptions not validated with users, backstage failure points not yet mapped
9. **Pass/Fail Readiness**, PASS if mapped stages cite evidence and distinguish observed friction, no observed friction, and unknowns; prioritize supported opportunities (listing is sufficient at Light depth). FAIL if assumptions are presented as observed customer behavior. Do not invent a pain point for every stage.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Inside-out mapping**, Map from the customer's perspective, not your product's feature list
- **Happy path only**, Include error states, confusion, and abandonment
- **No evidence**, Every pain point needs a source: analytics, research, or support data
- **Too granular**, A journey map is strategic, not a UI flowchart; stay at the experience level
- **Maps that sit on a shelf**, Connect every pain point to an opportunity with an owner

## Weak vs. Strong Output

**Weak:**
> "Pain point: Onboarding is confusing."

No specificity about what is confusing, for whom, or how severe. Cannot be acted on.

**Strong:**
> "Pain point: 34% of new users abandon the workspace setup wizard at step 3 (team invitation). Session recordings show users looking for a 'skip' option. Severity: High. Evidence: product analytics + 12 session recordings (Jan cohort)."

Pinpoints the exact moment, quantifies drop-off, names the evidence sources, and gives designers a clear target.
