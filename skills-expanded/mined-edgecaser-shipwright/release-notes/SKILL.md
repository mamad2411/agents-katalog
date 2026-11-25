---
name: release-notes
description: "Transforms Jira/Linear tickets, changelogs, and commit histories into polished, customer-facing release notes. Supports segmentation by audience (end users, admins, developers) and tone calibration for different channels."
category: execution
default_depth: standard
---

# Release Notes Generator

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Transforms Jira/Linear tickets, changelogs, and commit histories into polished, customer-facing release notes. Supports segmentation by audience (end users, admins, developers) and tone calibration for different channels.

## When to Use

- After each release or deployment
- Preparing changelog entries for product updates
- Drafting customer communications for major releases
- Creating internal release summaries for support, sales, and CS teams

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Patch or hotfix with fewer than 5 changes | Gather Raw Inputs, Categorize Changes, Write Customer-Facing Notes (Fixes & Improvements only) |
| **Standard** | Regular minor or major release | All sections |
| **Deep** | Major version launch, breaking changes, or public-facing announcement | All sections + migration guide appendix, customer segmentation matrix, coordinated launch timeline across channels |

**Omit rules:** At Light depth, skip Internal Release Notes and Channel Adaptation. Produce only a categorized changelog with one-line benefit statements.

## Framework

### Step 1: Gather Raw Inputs

Collect the raw materials for the release:

```markdown
## Release: [version / name]
## Date: [release date]
## Type: [Major / Minor / Patch / Hotfix]

### Raw Inputs
- [ ] Merged PRs / commits since last release
- [ ] Completed Jira/Linear tickets
- [ ] Design specs for new features
- [ ] Bug reports that were resolved
- [ ] Performance improvements with benchmarks
- [ ] Breaking changes or deprecations
```

### Step 2: Categorize Changes

Group changes into standard categories:

```markdown
### New Features
- [Feature name]: [One-sentence description of what users can now do]

### Improvements
- [Area]: [What got better and how it helps]

### Bug Fixes
- [Fixed]: [What was broken and what the fix means for users]

### Performance
- [Area]: [What improved, include numbers if available]

### Breaking Changes
- [Change]: [What stopped working and what to do instead]

### Deprecations
- [Feature]: [What's being phased out, timeline, and migration path]
```

### Step 3: Write Customer-Facing Notes

**Rules for good release notes:**
- Lead with value, not implementation
- Use customer language, not engineering jargon
- Explain "what you can do now" not "what we changed"
- Include visuals (screenshots, GIFs) for significant UI changes
- Call out breaking changes prominently

```markdown
# What's New in [Product] [Version]
[Release date]

## Highlights

### [Feature Name], [Benefit headline]
[2-3 sentences explaining what this enables for the user. Focus on the outcome, not the mechanism. Include a concrete example of when you'd use this.]

### [Improvement Name], [Benefit headline]
[1-2 sentences on what got better.]

## Fixes & Improvements
- **[Area]:** [Plain-language description of what was fixed]
- **[Area]:** [Description]

## Breaking Changes
> **Action required:** [Clear description of what changed, who's affected, and what to do]

## Coming Soon
[Optional: tease what's next to maintain momentum]
```

### Step 4: Write Internal Release Notes

Different audience, different depth:

```markdown
# Internal Release Notes: [Version]

## For Support/CS Teams
### What customers will notice:
- [Visible change 1, with talking points for customer questions]
- [Visible change 2]

### Known issues still open:
- [Issue], Workaround: [steps]

### FAQ for customer questions:
Q: [Anticipated question]
A: [Suggested response]

## For Sales Teams
### New selling points:
- [Feature] enables [use case], relevant for [segment]

### Competitive implications:
- [How this changes our competitive position]

## For Engineering/On-Call
### Deployment notes:
- [Migration steps, feature flags, rollback procedure]

### Monitoring:
- [What to watch, metrics, alerts, dashboards]
```

### Step 5: Channel Adaptation

Adapt the same content for different channels:

| Channel | Length | Tone | Focus |
|---|---|---|---|
| In-app changelog | 1-2 sentences per item | Concise, scannable | What's new |
| Email announcement | 3-5 paragraphs | Warm, excited | Top highlights + CTA |
| Blog post | 500-1000 words | Narrative, detailed | Story behind the release |
| Social media | 1-2 sentences | Punchy, visual | Single biggest highlight |
| Slack/internal | Bullet points | Casual, practical | What the team needs to know |

## Minimum Evidence Bar

**Required inputs:** A list of merged PRs, completed tickets, or a changelog diff since the last release, plus the release version and date.

**Acceptable evidence:** Git commit history, Jira/Linear ticket exports, design specs for new features, QA test reports, and performance benchmarks.

**Insufficient evidence:** If no ticket list or commit history is available, stop and recommend pulling the changelog diff from version control or the project management tool before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** What changed, which bugs were fixed, and what breaking changes exist must be grounded in the commit/ticket record.
- **Hypotheses:** Customer impact estimates and "coming soon" teasers are forward-looking -- label them as such.

## Output Format

Produce:
1. **Customer-Facing Release Notes**, polished, benefit-oriented
2. **Internal Release Notes**, segmented by audience (Support, Sales, Eng)
3. **Channel Variants**, adapted versions for email, blog, social, in-app

**Shipwright Signature (required closing):**
4. **Decision Frame**, recommended communication priority and channel sequencing, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, unconfirmed customer impact of changes, missing performance benchmarks, unclear migration paths for breaking changes
6. **Pass/Fail Readiness**, PASS if every customer-facing change has a benefit statement and breaking changes have migration instructions (at Light depth: PASS if every change has a one-line benefit statement; breaking-change migration instructions are still required if any breaking changes exist); FAIL if breaking changes are undocumented or customer-facing notes use engineering jargon
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Engineering jargon**, "Refactored the query layer" means nothing to customers; "Search is now 3x faster" does
- **Listing every ticket**, Customers don't need to see "Fixed typo in tooltip." Curate.
- **Burying breaking changes**, These need prominent placement and clear migration instructions
- **No internal notes**, Support and sales teams get blindsided without a heads-up
- **Inconsistent cadence**, Ship release notes with every release; silence erodes trust

## Weak vs. Strong Output

**Weak:**
> Improved performance of the data processing pipeline and refactored the caching layer for better efficiency.

Engineering jargon that tells the customer nothing about what changed for them.

**Strong:**
> **Faster exports:** CSV and PDF exports now complete up to 3x faster for datasets over 10,000 rows. Large reports that previously timed out will now download reliably.

Leads with the customer benefit, quantifies the improvement, and explains when they will notice the change.
