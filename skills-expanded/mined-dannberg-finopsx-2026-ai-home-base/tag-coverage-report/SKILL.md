---
name: tag-coverage-report
description: Compute tag coverage for a project, org, or business unit, and draft the cleanup communications. Triggers on phrases like "tag coverage", "tagging compliance", "find untagged resources", "who isn't tagging properly". Outputs per-tag-key compliance percentages, lists of non-compliant teams/services, and ready-to-send Slack DMs to the likely owners.
---

# Tag Coverage Report

When invoked, compute tag coverage and turn it into action. The report alone is useless — the value comes from the cleanup messages going to the right people. This skill does both.

## Inputs to confirm before starting

- Scope: project, folder, org, business unit, or specific account list
- Required tag keys (from the org's tagging policy — e.g., `cost_center`, `team`, `environment`)
- Time window (default: last 30 days)
- Compliance bar (default: 95% per tag key)

If the org's tagging policy is committed to a doc the AI can read, reference it instead of asking each time.

## Steps

1. **Compute coverage per tag key.** For each required key, calculate:
   - Percentage of resources that have the tag set
   - Percentage of resources where the tag value is one of the allowed values (if the policy specifies allowed values)
   - Total count of non-compliant resources

2. **Group non-compliance by likely owner.** For each non-compliant resource, identify the most likely owning team using:
   - Existing partial tags
   - Project naming conventions
   - Resource creator (from audit logs if available)
   - Account-to-team mapping (from `reference/team-mapping.md` or similar)

3. **Build the per-team breakdown.** For each team with non-compliant resources, produce:
   - Total count
   - Top 3 specific examples (resource ID, what's missing)
   - Estimated cleanup effort (under 30 min / a few hours / requires migration)

4. **Draft the cleanup DMs.** See template below.

5. **Roll up to a leadership view.** One paragraph for the FinOps weekly: overall coverage, which tags are most problematic, which teams are most behind, what's the trajectory.

## Per-team Slack DM template

Slack DM (not channel post) to the team's likely owner. Friendly, specific, includes a link to the policy.

```
Hey [name] — quick FinOps cleanup ask.

We're at [X]% tag coverage org-wide and your team currently has [N] resources missing [tag_key]. The biggest offenders:

- [resource 1] — missing [tag]
- [resource 2] — missing [tag]
- [resource 3] — missing [tag]

[Link to tagging policy]

Most of these look like 5-minute fixes. Could you tackle them by [date 1 week out]? Happy to jump on a quick call if anything's unclear.
```

Avoid in DMs:
- Threats of escalation (not yet — start friendly)
- Org-wide compliance numbers that aren't relevant to that team
- Generic "improve tagging" framing — be specific to their resources

## Output format

```
## Coverage summary
[Table: tag key | coverage % | trend vs last report | notes]

## Top non-compliant teams
[Ranked list with counts and example resources]

## Slack DMs to send
[One DM per team, ready to paste]

## Leadership rollup
[One paragraph for the weekly digest]
```

## Customization notes

- The 95% compliance bar is a default. Tune to your org's maturity.
- If your org runs cost center allocation off the `cost_center` tag specifically, weight that tag higher in the report — non-compliance there has direct financial impact.
- The "estimated cleanup effort" field is a judgment call; the AI should flag where it's unsure rather than guessing.
- If your tagging policy includes an exceptions process, link to it in the DM template so the recipient has an out for legitimate exceptions.
