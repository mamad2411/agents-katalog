---
name: delivery-timeline
description: Generates a delivery timeline from a completed milestones.yaml. Asks for a production deploy date, QA rounds, and days per QA session. Updates each milestone with estimated_days, produces timeline.yaml with a complete relative-day schedule, and appends a workback block mapping every item to a real calendar date working backwards from the production deploy date.
---

# Delivery Timeline

Generates a delivery timeline from a completed `milestones.yaml`. Asks for delivery parameters (production deploy date, QA rounds, days per QA session), updates milestones with day estimates, and produces `timeline.yaml` with two sections: a relative-day `timeline` and a real-date `workback` schedule anchored to the production deploy date.

## Prerequisites

- Completed `milestones.yaml` (output from `/implementation-planner`)

## Usage

```
/delivery-timeline path/to/milestones.yaml
```

## Process

### Step 1: Load & Parse Milestones

Read `milestones.yaml` and extract each milestone's `id`, `name`, `dependencies`, and `estimated_duration`.

Also read `meta.ordering_strategy` if present. Store as `ordering_strategy`. If absent, default to `foundation-first`.

The `ordering_strategy` value drives structural differences in Steps 6 and 7:
- `multi-pr`: PR/review/merge cycles are inserted after each milestone in the development timeline; the fixed pre-QA PR block in Step 7 is omitted.
- All other strategies (`single-feature-branch`, `value-first`, `risk-first`, `vertical-slice`, `foundation-first`): standard single-PR post-development flow (no change to current behavior).

### Step 2: Gather Delivery Parameters

Ask the user the following three questions. You may present them together in a single message:

1. **Production deploy date** — "What is your desired production deploy date? (YYYY-MM-DD)"
2. **QA rounds** — "How many rounds of QA are required?"
3. **QA days per round** — "How many days should be allotted for each QA session?"

If the provided production deploy date falls on a Saturday or Sunday, warn the user:

> "Note: [date] falls on a weekend. Would you like to use [previous Friday] or [next Monday] instead?"

Wait for the user to confirm or correct before proceeding. Store the confirmed values as:
- `production_deploy_date` (ISO 8601 date string)
- `qa_rounds` (integer ≥ 1)
- `qa_days_per_round` (integer ≥ 1)

### Step 3: Convert Durations to Days

Convert each milestone's `estimated_duration` string to a whole number of business days using this table:

| estimated_duration | estimated_days |
|--------------------|----------------|
| 0.5 weeks          | 3              |
| 1 week             | 5              |
| 1.5 weeks          | 8              |
| 2 weeks            | 10             |
| 2.5 weeks          | 13             |
| 3 weeks            | 15             |
| 3.5 weeks          | 18             |
| 4 weeks            | 20             |
| N weeks            | N × 5 (rounded up to nearest whole day) |

For durations expressed in days already (e.g., `5 days`), use the number as-is.

### Step 4: Update milestones.yaml

Add `estimated_days` to every milestone entry in `milestones.yaml`. Do not modify any other fields.

Example — before:
```yaml
- id: m0
  name: Foundation & Project Setup
  estimated_duration: 1 week
```

After:
```yaml
- id: m0
  name: Foundation & Project Setup
  estimated_duration: 1 week
  estimated_days: 5
```

### Step 5: Determine Project Size

Calculate `total_development_days` by summing `estimated_days` across all milestones.

**Large project** if either condition is true:
- `total_development_days > 30`
- Number of milestones > 5

Large projects receive two rounds of QA feedback by default, but this is **overridden by the user-provided `qa_rounds` value** from Step 2. `is_large_project` is still recorded in the summary for informational purposes.

### Step 6: Build the Development Timeline

Starting at Day 0, assign a `completion_day` to each milestone in dependency order. Each milestone's `start_day` is the `completion_day` of its last dependency (or 0 if no dependencies). Its `completion_day` is `start_day + estimated_days`.

For sequential milestone chains (each depends on the previous), completion days are simply cumulative:

```
m0: completion_day = 0 + estimated_days(m0)
m1: completion_day = completion_day(m0) + estimated_days(m1)
m2: completion_day = completion_day(m1) + estimated_days(m2)
...
```

For parallel milestones (same dependency), they share the same `start_day` but their `completion_day` is calculated independently.

#### Standard strategies (all except `multi-pr`)

`last_milestone_day` = the highest `completion_day` among all milestones.

#### `multi-pr` strategy

After each milestone, insert four PR cycle phases before the next milestone may start. Use the milestone id as a prefix (e.g. for `m0`: `m0-pr-creation`, `m0-pr-review`, `m0-review-feedback`, `m0-merge`).

| id pattern              | name pattern                   | estimated_days | notes                                    |
|-------------------------|-------------------------------|----------------|------------------------------------------|
| [milestone-id]-pr-creation     | [Milestone Name] PR Creation  | 0              | Opened on milestone completion_day       |
| [milestone-id]-pr-review       | [Milestone Name] PR Review    | 2              |                                          |
| [milestone-id]-review-feedback | [Milestone Name] Review Feedback Implementation | 2 |                               |
| [milestone-id]-merge           | [Milestone Name] Merge        | 0              | Same day as review-feedback completion   |

The PR cycle adds **4 calendar days** of overhead after each milestone. The next milestone's `start_day` = `completion_day` of its predecessor's `merge` phase (not the raw milestone `completion_day`).

For sequential milestones under `multi-pr`:

```
m0: start_day=0, completion_day=estimated_days(m0)
m0-pr-creation: start_day=completion_day(m0), completion_day=completion_day(m0)          # 0 days
m0-pr-review: start_day=completion_day(m0), completion_day=completion_day(m0)+2
m0-review-feedback: start_day=completion_day(m0)+2, completion_day=completion_day(m0)+4
m0-merge: start_day=completion_day(m0)+4, completion_day=completion_day(m0)+4            # 0 days

m1: start_day=completion_day(m0-merge), completion_day=completion_day(m0-merge)+estimated_days(m1)
# ... repeat for each milestone
```

For parallel milestones under `multi-pr`, each branch gets its own PR cycle. A milestone depending on multiple parallel predecessors starts after the latest `merge` completion_day among them.

`last_milestone_day` = the highest `completion_day` of the final `[milestone-id]-merge` phase across all milestones.

### Step 7: Append Post-Development Timeline

Add delivery phase items starting from `last_milestone_day`. Each item has a `start_day` (day the work begins) and `completion_day` (day the work is done). Items with `estimated_days: 0` complete on the same day they start.

Use `qa_rounds` and `qa_days_per_round` from Step 2 to drive the QA section.

#### Fixed Pre-QA Phases

**Standard strategies (all except `multi-pr`):** Include the full PR/merge/deployment block below. This represents the single end-of-project PR.

| id                   | name                            | estimated_days | notes                              |
|----------------------|---------------------------------|----------------|------------------------------------|
| post-pr-creation     | PR Creation                     | 0              | Opened on last milestone day       |
| post-pr-review       | PR Review                       | 2              |                                    |
| post-review-feedback | Review Feedback Implementation  | 2              |                                    |
| post-merge           | Merge                           | 0              | Same day as feedback impl          |
| post-deployment      | Deployment                      | 1              |                                    |

**`multi-pr` strategy:** Omit `post-pr-creation`, `post-pr-review`, `post-review-feedback`, and `post-merge` — those cycles already occurred per-milestone in Step 6. Start directly with `post-deployment`.

| id              | name        | estimated_days | notes                                    |
|-----------------|-------------|----------------|------------------------------------------|
| post-deployment | Deployment  | 1              | Final deployment after all milestones merged |

#### QA Phases (repeated for each round 1..qa_rounds)

For each round R from 1 to `qa_rounds`, generate the following phases using `qa_days_per_round` as the QA Deadline duration. Use round-specific ids (e.g. `post-qa-r1-deadline`, `post-qa-r2-deadline`). When `qa_rounds == 1`, ids may omit the round suffix (e.g. `post-qa-deadline`).

| id pattern                     | name pattern                            | estimated_days                        | notes                                            |
|--------------------------------|-----------------------------------------|---------------------------------------|--------------------------------------------------|
| post-qa-rR-deadline            | QA Deadline (Round R)                   | `qa_days_per_round`                   | Time allotted for QA team testing                |
| post-qa-rR-feedback-impl       | QA Feedback Implementation (Round R)   | 3 if (R == 1 and qa_rounds > 1) else 2 |                                                  |
| post-qa-rR-pr                  | QA PR (Round R)                         | 0                                     |                                                  |
| post-qa-rR-feedback            | QA Feedback (Round R)                   | 2 if (R == 1 and qa_rounds > 1) else 1 |                                                  |
| post-qa-rR-merge               | QA Merge (Round R)                      | 0                                     |                                                  |

#### Fixed Post-QA Phase (all projects)

| id            | name    | estimated_days |
|---------------|---------|----------------|
| post-signoff  | Signoff | 1              |

### Step 8: Build Workback Schedule

Map every timeline item (milestones + delivery phases) to a real calendar date by working **backwards** from `production_deploy_date`.

**Anchor point:** `production_deploy_date` = the real date for `completion_day` of `post-signoff` (the final day of the timeline, `total_delivery_days`).

**Business day arithmetic:** When counting backwards, skip Saturdays and Sundays. One business day back from a Monday is the previous Friday.

**For each timeline item:**
- `completion_date` = `production_deploy_date` minus (`total_delivery_days` − `item.completion_day`) business days
- `start_date` = `production_deploy_date` minus (`total_delivery_days` − `item.start_day`) business days

**`project_start_date`** = `production_deploy_date` minus `total_delivery_days` business days (Day 0).

Include all items from `timeline` in the same order. Also append a final entry for `production-deploy` with `date: production_deploy_date`.

### Step 9: Generate timeline.yaml

Write `timeline.yaml` in the same directory as `milestones.yaml`.

## Output Format

### Updated milestones.yaml

The `estimated_days` field is added to each milestone entry. All other content is preserved exactly.

### timeline.yaml Schema

```yaml
version: "1.0.0"
project: [project name from milestones.yaml]
generated: "[ISO 8601 timestamp]"
milestones_file: milestones.yaml

summary:
  total_development_days: [n]
  total_delivery_days: [n]            # development + post-dev
  is_large_project: [true/false]
  milestone_count: [n]
  qa_rounds: [n]                      # from user input
  qa_days_per_round: [n]              # from user input
  production_deploy_date: "[YYYY-MM-DD]"
  delivery_model: [ordering_strategy value from milestones.yaml meta, e.g. multi-pr]

timeline:
  # Development milestones
  - id: [milestone id, e.g. m0]
    name: [milestone name]
    type: milestone
    start_day: [n]
    completion_day: [n]
    estimated_days: [n]
    dependencies: [list of milestone ids, or []]

  # ... additional milestones

  # Post-development delivery phases
  - id: post-pr-creation
    name: PR Creation
    type: delivery
    start_day: [n]
    completion_day: [n]
    estimated_days: 0
    notes: "Opened upon completion of final milestone"

  - id: post-pr-review
    name: PR Review
    type: delivery
    start_day: [n]
    completion_day: [n]
    estimated_days: 2

  # ... remaining delivery phases

workback:
  production_deploy_date: "[YYYY-MM-DD]"
  project_start_date: "[YYYY-MM-DD]"   # Day 0 in real calendar terms
  schedule:
    - id: [same id as timeline entry]
      name: [same name as timeline entry]
      type: [milestone | delivery]
      start_date: "[YYYY-MM-DD]"
      completion_date: "[YYYY-MM-DD]"

    # ... all timeline items in order

    - id: production-deploy
      name: Production Deploy
      type: deploy
      date: "[YYYY-MM-DD]"             # = production_deploy_date
```

## Example Output

See [examples/timeline.yaml](./examples/timeline.yaml) for a complete sample.

## Gap Analysis

After generating `timeline.yaml`, perform a gap analysis and report findings inline.

### Checks

**Coverage**
- [ ] Every milestone in `milestones.yaml` appears in `timeline.yaml`
- [ ] All milestone dependencies are respected (no milestone completes before its dependencies)
- [ ] `estimated_days` was added to every milestone in `milestones.yaml`

**Duration Reasonableness**
- [ ] No single milestone has `estimated_days: 0` (flag for review)
- [ ] No milestone exceeds 30 days without a note explaining the scope
- [ ] Duration conversions match the table in Step 2

**Project Size Classification**
- [ ] `is_large_project` correctly reflects `total_development_days > 30` OR `milestone_count > 5`
- [ ] QA rounds in `timeline.yaml` match user-provided `qa_rounds`
- [ ] QA Deadline phases each use `qa_days_per_round` days

**Delivery Model**
- [ ] `ordering_strategy` was read from `milestones.yaml` (or defaulted to `foundation-first`)
- [ ] `delivery_model` in `timeline.yaml` summary matches the resolved strategy
- [ ] For `multi-pr`: each milestone has a corresponding `[milestone-id]-pr-creation / pr-review / review-feedback / merge` block in the timeline; `post-pr-creation` through `post-merge` are absent from post-development phases
- [ ] For all other strategies: `post-pr-creation` through `post-merge` are present in post-development phases; no per-milestone PR blocks exist

**Timeline Integrity**
- [ ] `completion_day` values are strictly increasing for sequential milestones
- [ ] Parallel milestones have correct independent `completion_day` values
- [ ] Post-development phases follow immediately after `last_milestone_day`
- [ ] `total_delivery_days` = `completion_day` of `post-signoff`

**Workback Integrity**
- [ ] `project_start_date` = `production_deploy_date` minus `total_delivery_days` business days
- [ ] `production-deploy` entry date matches `production_deploy_date`
- [ ] All `completion_date` values are on weekdays (Mon–Fri)
- [ ] `workback.schedule` contains all entries from `timeline` in the same order
- [ ] `post-signoff` completion_date = `production_deploy_date`

### Gap Analysis Report

After generating files, output a brief inline report:

```
## Timeline Gap Analysis

**Project:** [name]
**Delivery Model:** [ordering_strategy]
**Total Development Days:** [n] ([n] weeks)
**Total Delivery Days:** [n] (including post-dev phases)
**Project Size:** [Small / Large] ([reason if large])
**QA Rounds:** [n] × [qa_days_per_round] days each
**Production Deploy:** [YYYY-MM-DD]
**Project Start:** [YYYY-MM-DD]

**Checks:**
✓ All [n] milestones included
✓ Dependency order respected
✓ Duration conversions applied
[✓ / ✗] estimated_days added to milestones.yaml
[✓ / ✗] QA rounds match user-specified value ([n] rounds)
[✓ / ✗] All workback dates land on weekdays
[✓ / ✗] post-signoff completion_date = production_deploy_date

**Issues:** [none / list issues]

**Recommendations:** [none / list recommendations]
```

If issues are found, ask:

> "I found the following timeline issues:
>
> - [Issue 1]
> - [Issue 2]
>
> Would you like to:
>
> 1. Fix these issues now
> 2. Proceed with the timeline as-is
> 3. Manually adjust the estimates before generating"
