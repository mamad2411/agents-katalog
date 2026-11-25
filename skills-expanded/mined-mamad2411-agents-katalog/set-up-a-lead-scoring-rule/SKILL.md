---
name: set-up-a-lead-scoring-rule
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create or update a lead scoring rule that helps prioritize leads using clear fit and intent signals.

## Preconditions

- Admin or marketing-ops access to lead scoring settings.
- Agreed scoring criteria and threshold definitions.
- Test leads or historical examples for validation.

## Steps

1. **Open scoring settings.** [BRANCH: Salesforce | HubSpot | generic] open scoring automation or Einstein/lead score configuration in Salesforce; open Score properties or lead scoring in HubSpot; in another CRM, open scoring or workflow rules. → *Expect:* scoring rules can be viewed or edited.
2. **Define positive fit signals.** Add points for approved attributes such as target industry, company size, role, territory, and product fit. → *Expect:* good-fit leads receive fit points.
3. **Define intent signals.** Add points for approved behaviors such as demo request, pricing-page visit, event attendance, reply, or high-value form submission. → *Expect:* active interest raises the score.
4. **Define negative signals.** Subtract points for student, vendor, competitor, bad email, out-of-market geography, or low-fit company. → *Expect:* poor-fit leads are deprioritized.
5. **Set thresholds and actions.** Define MQL, sales-ready, nurture, or disqualify thresholds and any routing workflow. → *Expect:* score changes map to an operational action.
6. **Test with sample records.** Apply the rule to known good, weak, and bad leads. → *Expect:* sample scores match sales judgment.
7. **Publish the rule.** Save or activate the rule after review by sales and marketing owners. → *Expect:* new or updated scores calculate in the CRM.
8. **Monitor early results.** Review routed leads and false positives after initial use. → *Expect:* scoring quality can be adjusted with evidence.

## Decision points

- If sales disagrees with score outputs → adjust criteria before full routing automation.
- If behavior tracking lacks consent → exclude that signal.
- If scores will trigger outreach → include suppression and ownership checks in downstream workflows.

## Failure modes & recovery

- **F1 Score inflation:** detect too many leads crossing threshold → reduce broad signals or raise thresholds.
- **F2 High-fit leads missed:** detect good leads below threshold → add or increase fit and intent signals.
- **F3 Noncompliant signal:** detect use of restricted personal or tracking data → remove the signal and rescore affected leads.

## Verification

The active scoring rule applies documented positive, negative, and threshold logic, and sample records score according to agreed sales and marketing expectations.

## Variations

- Fit-only scoring: use firmographic and role data when behavior tracking is unavailable.
- Product-led scoring: include approved usage milestones and workspace activity.
- Regional scoring: adjust geography and consent-related signals by market.

## Safety & privacy

Use transparent, business-relevant criteria. Do not score on protected classes, sensitive personal data, or tracking signals that lack consent or policy approval.
