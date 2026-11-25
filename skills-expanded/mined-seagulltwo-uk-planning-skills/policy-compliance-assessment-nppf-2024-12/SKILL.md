---
name: policy-compliance-assessment-nppf-2024-12
description: >-
  ARCHIVED - December 2024 NPPF edition (superseded 17 August 2026). Use only when the user explicitly asks to work under the pre-August-2026 framework and has confirmed they want the archived skills; outputs must state they cite a superseded framework. 
  Assess a UK planning application against the policies that govern it, starting
  with the formally **adopted** development plan published by the local planning
  authority — which has primacy. Identify and verify that plan first (adoption
  dates, superseded policies, the policies map), then score the proposal policy
  by policy from -2 (significant conflict) to +2 (strongly aligned), assess
  NPPF/PPG and any emerging plan separately at lower weight, and conclude on
  accordance with the plan read as a whole. Use for "does this comply with the
  local plan", "which policies does this application breach", "assess this
  against adopted policy", "policy analysis". England-focused. Not legal advice;
  no warranty; output requires human review.
license: MIT
---

# Policy compliance assessment

Work out **which planning policies govern an application, and whether it accords with each
one**. The skill does three things:

1. **Identify the adopted development plan** for the relevant local planning authority, and
   verify it — the essential first step, because determination starts there and nothing
   downstream is safe if this is wrong.
2. **Assess** the proposal against each relevant policy, on the evidence in the application
   documents and the policy's own words.
3. **Score and report** — a policy-by-policy table with an accordance score from **-2 to
   +2**, then a reasoned conclusion on accordance with the development plan **read as a
   whole**.

National policy (NPPF/PPG) and any **emerging** plan are assessed too, but as material
considerations carrying **less weight than the adopted plan** — never as a substitute for it.

## When to use

The user asks: "does this comply with the local plan?", "which policies does this application
breach?", "assess this against the adopted policies", "what does the local plan say about
this site?", "is this development plan compliant?" — or a representation needs a policy
foundation before it is drafted.

Use it **after** `application-triage` has identified which considerations are engaged (or
alongside it — triage's decision-framework step hands off to this skill), and **before**
`policy-representation` drafts anything.

Not this skill: the deep technical evaluation of a topic's evidence base (the
`ecological-`, `transport-`, `heritage-` and `flood-representation` skills own that), the
current NPPF edition and paragraph numbers (`national-planning-policy` owns those), or the
final harms-vs-benefits weighing (`planning-balance`).

## Two layers, no duplication

This skill owns the **procedure**: how to find and verify an adopted development plan, how
to read a policy, and how to score accordance. It owns **no citations of its own**. The
current NPPF/PPG edition register, the verify-before-citing protocol, s.38(6) and plan
primacy, the paragraph-11 presumption, emerging-plan weight and the conditions/obligations
tests all live in the companion **national-planning-policy** skill — take them from there.
The policies themselves are **per-instance data**: they come from the council's adopted plan
at run time, and are quoted, never remembered.

## The integrity principle (read first)

- **The adopted plan is the local authority's own document, and it has primacy.** Adopted
  policies are made and published by the **local planning authority** — on its own website,
  under its own numbering, adopted on its own date. They are not published by central
  government, and they are not the NPPF. This matters twice over: it tells you **where to
  look** (the council's planning-policy pages, never a national source), and it fixes the
  **hierarchy** — the development plan is the statutory starting point, and national policy is
  a material consideration that informs the decision without displacing the plan. An
  assessment that leads on the NPPF and treats the local plan as background has the
  hierarchy upside down.
- **"Adopted" is a formal term — establish it, don't assume it.** A plan is adopted when the
  council has formally resolved to adopt it following independent examination. A published,
  submitted, consulted-on or examined-but-not-yet-adopted plan is **not** adopted, and neither
  is a supplementary planning document. Getting this wrong is the single most damaging error
  available here: an assessment against draft policy numbers, or against policies that a
  later plan superseded, is worthless and visibly so.
- **Quote the policy; never recall it.** Policy wording and numbering vary between councils
  and between editions of the same plan, and draft numbering rarely survives adoption. Every
  policy in the output must be quoted from the adopted document, with the document name,
  adoption date and policy reference recorded.
- **A score is a reasoned judgement, not a measurement.** It is a shorthand for an argument
  that must be stated alongside it. A score with no quoted requirement and no evidence from
  the application is not an assessment.
- **Never total or average the scores.** Section 38(6) requires accordance with the
  development plan **read as a whole**, which is a planning judgement, not arithmetic. One
  -2 against a policy central to the proposal can outweigh five +1s on peripheral ones; the
  reverse is also true. Presenting a sum or a mean would manufacture false objectivity —
  and would let a genuinely fatal conflict be averaged away.
- **Missing evidence is not conflict.** Where a policy requires something the application
  has not supplied, the honest output is "cannot be assessed" (flagged `?`), not a negative
  score. That distinction is what separates "the proposal conflicts with Policy X" from "the
  Council cannot yet conclude whether it complies with Policy X" — a different ask entirely.
- **Score the proposal against the policy, not against a preference.** Record accordance
  where it exists, at full strength. An analysis that finds only conflict will be read as
  advocacy and discounted.

## Workflow

### Step 1 — Identify and verify the adopted development plan (do this first)

Work through
[`references/finding-the-development-plan.md`](references/finding-the-development-plan.md).
In outline:

1. **Confirm the local planning authority.** Usually the district, borough or unitary
   council — but a **National Park authority** or the Broads Authority is the LPA for its
   own area, and a development corporation may be. In two-tier areas, **minerals and waste**
   policy sits with the county council. The wrong LPA means the wrong plan.
2. **Assemble the development plan.** Under s.38 of the Planning and Compulsory Purchase Act
   2004 it comprises the **adopted development plan documents taken as a whole** plus any
   **made** neighbourhood plan for the area; in Greater London it also includes the Mayor's
   spatial development strategy (the London Plan). It is often **several documents** — a core
   strategy plus a site-allocations and/or development-management document, sometimes a joint
   plan, plus the county minerals and waste plans. ⏳ *Verify the composition against the
   current statute at run time — see the reference file's note on pending reforms.*
3. **Record the adoption date and status of each document**, and find the **schedule of
   superseded and saved policies** — a new plan usually replaces only *some* of its
   predecessor's policies. Never cite a policy without checking it has not been superseded.
4. **Read the policies map** for the site: settlement boundary, allocations, designations
   and constraints. The map is part of the plan and often decides which policies apply.
5. **Note what is *not* the development plan** but may still be a material consideration:
   supplementary planning documents, design guides and codes, conservation area appraisals,
   council strategies, and emerging or withdrawn plans. Keep these in a separate tier.

Output a short **plan register** — document, adoption date, status, where obtained — before
assessing anything.

### Step 2 — Fix the plan's status
Record the plan's **age and review position**: its adoption date, the plan period, whether a
review or replacement is underway, and whether the council can demonstrate the required
housing land supply. This governs how much weight a conflict carries, and whether the
**tilted balance** is engaged or disapplied — take that test from the
**national-planning-policy** skill rather than restating it here. A conflict with a policy
that is out-of-date still counts, but at reduced weight; say so rather than silently
discounting it.

### Step 3 — Select the relevant policies
Use [`references/policy-families.md`](references/policy-families.md) to work from the proposal
and site to the policy families that ought to exist in any local plan, then find each one in
*this* plan. Two disciplines:

- **Relevance, not volume.** Include a policy because it applies to this development, on this
  site, at this scale — not to lengthen the list. Check each policy's own scope: many apply
  only to a development type, size threshold or designated area.
- **Flag the "most important" policies** for determining this application — the handful the
  decision turns on (typically the spatial strategy or settlement-boundary policy, the
  site-specific allocation or designation, and the principal topic policies). This phrase
  matters: it is what the presumption in national policy turns on.

### Step 4 — Assess each policy
For each policy: quote the **requirement** in its own words, then state what the
**application documents show**, then conclude. Reading discipline:

- **Distinguish mandatory from permissive wording.** "Will not be permitted", "must" and
  "will be required" are requirements; "should", "will be encouraged", "where possible" and
  "have regard to" are weaker. The strength of the wording sets the ceiling on the score.
- **Criterion-based policies are assessed criterion by criterion.** Where a policy permits
  development only if a list of criteria is met, failing one is conflict with the policy even
  if the rest are met — identify *which* criterion and why.
- **Read the whole policy**, including any exception or flexibility limb the proposal might
  rely on. Supporting text and the reasoned justification are not policy, but are legitimate
  aids to interpreting it — label them as such.
- **Designated areas raise the bar — score them that way.** In a conservation area, or where
  a listed building or other designated heritage asset (or its setting) is affected, the
  plan's character, design and scale policies are not ordinary detail policies: a statutory
  duty and national policy's "great weight" stand behind them (take the citations and the
  harm framework from the **heritage-representation** skill — s.66/s.72 and the NPPF heritage
  tests live there). Two consequences for this skill's procedure: **(a)** assess the
  **cumulative volume of physical change** quantitatively from the drawings — footprint,
  depth, height, plot coverage, extensions and alterations taken together, measured against
  the plot and its neighbours, not merely described; **(b)** where that change fails a
  character or scale criterion of a policy applying to the designated area, treat the
  conflict as going to the heart of the policy (-2 territory, and normally one of the "most
  important" policies) rather than softening it to a tension because only one limb fails or
  because each individual alteration looks modest.
- **Mitigation that is not yet secured is not compliance.** If a policy's requirement is met
  only by something a condition or obligation would have to secure, say so — that is a (C)
  point, and it belongs in the score's reasoning.

Evidence disciplines — habits observed in officer practice that the assessment must match:

- **Audit the openings window-by-window.** Compare existing and proposed elevations opening
  by opening: every new or altered window and door, which neighbour it faces, and whether it
  creates overlooking a condition (obscure glazing, non-opening) would have to control. A
  narrative read of the elevations misses exactly the opening the decision turns on.
- **Sweep the site's planning history first, and assess against any fallback.** Check the
  register for the site's (and close precedents') history before assessing: an extant
  permission is the controlling baseline, and the assessment narrows to the **delta**
  between it and the current proposal; past refusals and appeals on the site or its
  immediate context are weight-bearing precedent.
- **Measure against the neighbour as well as the plot.** Amenity geometry is relative:
  projection beyond the neighbour's rear building line, orientation to their windows and
  garden, and relative levels — computed from the drawings, not asserted.
- **Verify the basic site facts from more than one source.** Attachment status (detached /
  semi / terrace), plot orientation and constraints — state them with their evidence, and
  check the council's own GIS/policies-map layers as well as national datasets; local
  designations (minerals belts, ecology zones) often appear only on the council's layers.
- **Read the representations.** Consultee responses and neighbour/third-party comments are
  part of the evidence: they surface issues, site knowledge and precedents the application
  documents omit (handle any personal data minimally).
- **Consultee positions are evidence, not conclusions.** Re-derive each element's assessment
  from the documents; decision-makers routinely depart from their own specialists in both
  directions, and a consultee's general dispensation still has to survive the policy's own
  wording at this site's scale.
- **Prefer a condition to a refusal reason for separable detail.** Where an element is
  acceptable in principle and only its detail is missing, the officer's instinct is to
  reserve it by condition — a (C) point — not to refuse; reserve refusal reasons for harm.
  Likewise a missing supporting document on a minor scheme is a proportionate-information
  ask (B), not automatically a refusal reason.

### Step 5 — Score
Apply the rubric in [`references/scoring-rubric.md`](references/scoring-rubric.md):

| Score | Meaning |
|---|---|
| **+2** | **Strongly aligned** — the proposal actively delivers what the policy seeks; every criterion met. |
| **+1** | **Accords** — meets the policy's requirements; no material tension. |
| **0** | **Neutral** — engaged but the proposal neither advances nor offends it. |
| **-1** | **Tension / partial conflict** — fails part of a criterion-based policy, or is contrary to its aim in a limited or mitigable way. |
| **-2** | **Significant conflict** — breaches a mandatory requirement, or a criterion central to the policy's purpose; conflict goes to the heart of the policy. |
| **?** | **Cannot be assessed** — the policy is engaged but the application lacks the evidence the policy itself requires. **Not a negative score.** |

Alongside each score record the **weight tier** (adopted development plan / reduced —
out-of-date plan policy / national policy / emerging plan / guidance) and, where the
downstream skills need it, the **A/B/C** classification the repo uses: **(A)** demonstrated
unacceptable impact, **(B)** insufficient evidence, **(C)** resolvable by condition or
obligation. Every `?` is a (B).

### Step 6 — Add national and emerging policy, at their proper weight
Assess the relevant **NPPF/PPG** policies and any **emerging plan** policies the same way,
in a **separate section** of the table, explicitly marked as material considerations that
carry **less weight than the adopted plan**:

- **National policy** — a material consideration, influential but not above the plan. Verify
  every edition and paragraph reference through the **national-planning-policy** skill before
  citing; ⏳ the framework is under revision and paragraph numbers will not survive it.
- **Emerging plans** — weight depends on the stage of preparation, the extent of unresolved
  objections, and consistency with national policy. Record the stage and reason the weight;
  an emerging policy at early consultation carries very little, and saying so is part of the
  assessment.
- **Guidance** (SPDs, design codes, technical standards) — weight as guidance that
  supplements plan policy; it cannot create policy the plan does not contain.

### Step 7 — Conclude on the plan read as a whole
Write a short **accordance statement** (a paragraph or two): the plan documents that govern,
the policies the proposal conflicts with and how seriously, the policies it accords with, the
matters that cannot yet be assessed, and a reasoned conclusion on whether the proposal
accords with the development plan **read as a whole** — with no arithmetic. Then say what
follows: whether material considerations (national policy, emerging policy, the scheme's
benefits) might indicate a decision otherwise than in accordance with the plan, and hand off
to **planning-balance** for that weighing and to **policy-representation** for drafting.

## Output format

1. **Plan register** — the development plan documents, adoption dates, status, source.
2. **Site's plan status** — designations from the policies map; allocation or settlement
   position; plan age and review position.
3. **Policy table** — one row per policy: reference · source document · weight tier · quoted
   requirement · assessment (with the document evidence) · **score** · most-important flag ·
   A/B/C.
4. **A second table** for national and emerging policy, marked as lower-weight material
   considerations.
5. **Accordance statement** — the reasoned whole-plan conclusion, no totals.
6. **Verification note** — what was checked, when, and what needs re-checking at run time.

## Reference files

- [`references/finding-the-development-plan.md`](references/finding-the-development-plan.md)
  — how to identify and verify the adopted plan: what counts, where to look, the traps
  (superseded policies, draft numbering, SPDs, the wrong LPA), and emerging-plan stages.
- [`references/scoring-rubric.md`](references/scoring-rubric.md) — the -2 to +2 anchors with
  worked illustrations, the evidence-gap flag, the weight tiers, and the no-aggregation rule.
- [`references/policy-families.md`](references/policy-families.md) — the policy families to
  look for by proposal type, and which skill owns each one's technical evaluation.

## Scope and limitations

- **Not legal advice, and no warranty.** Policy interpretation is ultimately for the
  decision-maker, and contested wording is a matter for a planning professional or a
  solicitor; provided "as is", with no guaranteed outcome.
- **Human review is necessary before use.** A person must check every quoted policy against
  the adopted document and every assessment against the application documents.
- **England-focused.** The development-plan framework cited is England's; Wales, Scotland and
  Northern Ireland differ — flag and adjust outside England.
- **Evidence-bound.** Quote policies and application documents; never invent a policy
  reference, a plan date or a requirement. Where the plan is unclear, say it is unclear.
- **Time-sensitive.** Plans are adopted, superseded and reviewed continuously, and the
  national framework is under revision — re-resolve the plan and re-verify every citation at
  run time.
- **A UK planning representation is public and in the submitter's name** — this skill produces
  an analysis rather than a submission, but carry that warning through to
  **policy-representation** or whichever skill drafts from it.
- **"It complies" is a valid, valuable output.** So is "the plan is silent on this."
