---
name: cost-salience-variety-margin
description: Applies the first natural field experiment on making organizational costs salient (Hong, Riyanto, Yan & Huo, JEBO vol. 248, 2026, DOI 10.1016/j.jebo.2026.107634; university staff stationery ordering; randomizing cost visibility in an online ordering interface) — where showing the organization's cost left order frequency and quantity unchanged but cut item VARIETY by 27%, producing substantial university savings — as the design rule that third-party-cost salience operates on the variety (extensive) margin, not the volume (intensive) margin, with direct application to cloud-spend and subscription-culture interventions. Use when [designing cost-transparency features for team SaaS or cloud spend, deciding where to surface metered AI token costs, or choosing which behavioral lever to pull for expense reduction]. NOT for [personal-finance budgeting apps, individual willingness-to-pay research, or pricing strategy].
---

# Cost Salience Works on Variety, Not Volume

**Source:** Hong, Riyanto, Yan & Huo, "Making organization's cost salient: A natural field experiment," *Journal of Economic Behavior & Organization* vol. 248, 2026 (DOI 10.1016/j.jebo.2026.107634). Setting: a university where staff order stationery online at the university's expense. Randomized: treatment saw **cost information in the ordering interface**; control did not.

## The Result

- **Intensive margin (volume):** order frequency unchanged; quantity of requested items (conditional on ordering) unchanged.
- **Extensive margin (variety):** the **variety of items ordered fell — overall consumption down 27%**, generating substantial university savings.
- Mechanism: individuals **partially internalize the external effects** of their actions when the organization's cost is made salient — people respond to "my choice costs the institution something" on the *breadth* of what they add, not on whether/how much they order.

## Why This Matters

Cost-transparency interventions in organizations usually aim at total spend and usually fail or backfire (people rationalize, or the metric is gamed). This finding gives a precise lever: **surface the organization's cost at the moment of adding a new item type, not at the moment of ordering more of what you already need.** The behavioral target is the *add-another-SKU* decision, which is exactly where cloud/SaaS sprawl happens: new services, new regions, new model tiers, new add-on features — each individually trivial, collectively the bill.

**Design rules:**
1. **Put third-party cost on the add-item step** (the "add this service/model/region" moment), not the checkout or invoice. The invoice arrives too late; the ordering interface is the intervention surface.
2. **Expect no effect on the intensive margin — don't fight it.** People who need the item keep ordering it; salience will not make core usage cheaper. Pair with rightsizing/optimization for volume; use salience for sprawl.
3. **Pair salience with a decision aid** (the study is pure information; pairing with a cheaper-alternative suggestion at the same moment is the natural extension).
4. **For AI spend specifically:** the library's inference-cost skills (metered anxiety, token budgets) address the *individual* facing their own meter. This adds the *institutional* framing — a dev seeing "this subagent fan-out just cost the team $0.40" at request time targets the variety margin (another agent, another model tier) rather than guilt over necessary volume.
5. **Ethical note:** the study's effect runs through internalized external cost — a legitimate boost-style intervention (information that helps the actor align with their own values), distinct from shame-based displays which risk reactance and gaming.

## Honest Caveats

- Single organization, stationery domain, one-shot design; no long-run persistence measured; variety effects may partially reflect one-time catalog rationalization rather than sustained behavior. Generalization to cloud/SaaS spend is an analogy (mechanism-parallel), not tested in-domain.
- The result is a mean effect; heterogeneity (who internalizes) was not the paper's focus.

## A-Tech Alignment

- **Financial freedom:** the organizational version of spend-awareness — "make the team's meter visible at the moment of variety, not volume" is directly actionable for A-Coder-style token governance.
- **Practical:** one lever, one placement rule, one measurable outcome (variety share) — a one-page checklist.
- **Open source:** replicable interface-level experiment any org can run on its own procurement UI.
- **Privacy:** honest N/A — no behavioral-profiling angle; flagged rather than faked.

## Related Skills

- `ai-agent-finfops-cost-optimization` — the cost-architecture side of AI spend.
- `plan-limit-cognitive-thirst-trap` — individual metering psychology this complements at the org level.
- `nudge-complementarity-benefit-cost` — pairing rules for multi-component nudges.
- `digital-addiction-economics-2026` — revealed-cost information interventions.