---
name: accessibility-statement
description: Produce a conformance claim and an accessibility statement from real audit evidence, refusing to claim more than the evidence supports. Determines the scope of the claim, grades each success criterion by the class of evidence behind it, maps WCAG success criteria to the instruments that reference them (EN 301 549, Section 508, national accessibility law), drafts the statement with its mandatory sections, and audits an already-published statement against current reality. Use before publishing or refreshing a statement, before a tender accessibility section, or after an accessibility complaint. Not legal advice.
disallowed-tools: Write Edit NotebookEdit
user-invocable: true
argument-hint: "[--instrument en301549|section508|wcag] [--scope path-or-url-pattern] [--audit-existing]"
context: fork
agent: foundry-legal:accessibility-compliance-analyst
model: opus
effort: high
metadata:
  foundry.vertical: compliance
  foundry.io: "audit evidence -> conformance claim + accessibility statement draft"
license: Apache-2.0
---

# Accessibility statement

> **Automated technical assessment. Not legal advice.** A published accessibility statement is a
> public representation that can be enforced against you, and overstating conformance converts an
> accessibility defect into a false statement — to a public buyer, that is a different order of
> problem. Have a qualified professional confirm the statement before you publish it.

Two jobs get confused, and the confusion is where the liability comes from:

- **Testing** finds barriers. That is `foundry-quality`'s job, not this one.
- **Conformance** is a *claim* about a defined scope, at a defined level, on a defined date, backed
  by evidence of a defined class. That is this skill.

**Governing rule:** never upgrade a claim to close a gap. If the evidence supports "partially
supports", the statement says "partially supports" — including when the tender scoring punishes it.

## When to use this

- Publishing or refreshing an accessibility statement.
- Answering a tender or procurement accessibility section, or producing a conformance report.
- After a complaint, an enforcement contact, or a customer challenge to an existing statement.
- After a release that materially changed the surfaces in scope.

## When NOT to use this

- You have no audit evidence. Then the only honest output is a statement of non-conformance plus a
  plan to obtain evidence — which this skill will produce, and which is the correct deliverable.
- You want the barriers fixed. Different job, different vertical.
- You need to know whether an accessibility law applies to your organisation. Legal determination.
- You want to substitute this for testing with disabled users. It cannot, and it says so.

## Procedure

### Step 1 — Scope

A claim without a precise scope is meaningless; a scope drawn too wide is how a statement becomes
false. Define, in publishable words:

- **Included**: URLs, applications, flows, document types, platform versions — as an inclusion rule
  someone else could apply.
- **Excluded, with reasons**: third-party embeds, legacy sections, archives, user-generated content,
  pre-recorded media published before a date.
- **Full pages, complete processes**: a claim over a multi-step process requires every step. If
  checkout step 3 fails, the claim over checkout fails.
- **Non-web surfaces**: desktop clients, installers, generated PDFs and emails, kiosks, hardware.
- **The support channel** itself — several instruments require it to be accessible and nobody tests it.
- **Authenticated areas** — automated crawls stop at the login wall, leaving the product untested.

`--scope` narrows the run. A narrowed run may never be presented as a claim over the whole product.

### Step 2 — Map instruments to criteria

WCAG is a technical standard; it becomes an obligation because an instrument references it — at a
specific version and level, with added requirements of its own. Build the mapping from the packs and
`references/criteria-mapping.md`.

Two checks that must be explicit:

- **Version drift, both directions.** Testing against WCAG 2.2 AA is not automatically a valid claim
  under an instrument naming 2.0 AA; and 2.2 removed SC 4.1.1 Parsing, which older reports still list.
- **Beyond WCAG.** EN 301 549 and the Revised 508 Standards contain clauses with no WCAG equivalent
  (non-web software, real-time communication, biometrics, hardware, documentation, support services).
  A WCAG-only audit cannot support a claim under either.

### Step 3 — Grade the evidence before grading the product

Classify how each criterion was tested — automated pass, manual inspection with a recorded method,
assistive technology testing with the AT and version named, code review, or not evaluated. What each
class can support: `references/evidence-classes.md`.

State coverage as two fractions: criteria evaluated / criteria in scope, and pages sampled / pages in
scope, with the sampling method. **A claim over an unsampled population is an extrapolation and must
be labelled as one.**

### Step 4 — Decide what may be claimed

| Verdict | Condition |
|---|---|
| Supports | met throughout the scope, on evidence of the right class |
| Partially supports | met with identified exceptions — listed **specifically**; "some images" is not a listing |
| Does not support | not met |
| Not applicable | the scope contains nothing the criterion applies to, justified against content |
| Not evaluated | no evidence of the right class — always available, always better than a guess |

Three refusals to make under pressure:

1. No "fully conformant" while any criterion is not evaluated. Unevaluated is not met.
2. No claim over an unsampled population without stating the sampling method and labelling the
   extrapolation.
3. No remediation plan substituting for a claim. "Will conform by Q4" is a plan; today's statement
   describes today.

### Step 5 — Draft the statement

All nine elements from `references/statement-structure.md`. Anything you cannot fill from evidence is
marked as an open item — never invented. The section that gets omitted, and that enforcement bodies
read first, is **non-accessible content, itemised, each with its reason**.

Test the feedback mechanism: send to it and confirm delivery. Record the test as evidence. A feedback
address that bounces is the most embarrassing possible defect in an accessibility statement.

Where a regime prescribes a template, form or portal, use it — several reject free-form statements.

### Step 6 — Audit an existing statement

`--audit-existing` runs this alone. Check whether the stated level is still supported by current
evidence, whether the non-accessible content list matches current known barriers, whether the feedback
channel was tested this quarter and responses meet the stated time, and whether the scope still
matches the product after new features.

A statement that overstates current conformance is a `risk.v1`, not merely an accessibility finding —
the exposure is different in kind.

## Output

```
.foundry/blackboard/<wave>/accessibility-compliance-analyst.json   compliance-check.v1[] + finding.v1[]
.foundry/scratch/<session>/accessibility-statement.draft.md        statement for human review
.foundry/scratch/<session>/conformance-report.draft.md             per-criterion report for procurement
```

To the caller: the defensible claim in one sentence (scope, standard, level, date), the four counts
(supports / partially / does not support / not evaluated), and the disclaimer. This skill never
publishes anything — it holds no write tools.

## Exit criteria

- [ ] Scope written as an inclusion rule plus an explicit exclusion list, both publishable.
- [ ] Every applicable instrument mapped to standard, version and level; version drift checked both
      ways.
- [ ] Non-web surfaces, authenticated areas and the support channel each in scope with evidence, or
      explicitly excluded in the statement text.
- [ ] Evidence class recorded per criterion; the four counts sum to the criteria in scope.
- [ ] Coverage stated as two fractions plus the sampling method.
- [ ] Every "partially supports" lists its specific exceptions.
- [ ] Every "not applicable" justified against content, not convenience.
- [ ] All nine statement elements present, open items marked rather than invented.
- [ ] Feedback mechanism tested; the test recorded as evidence.
- [ ] A final separate pass confirms no claim exceeds its evidence class.
- [ ] Artifacts pass `mcp__plugin_foundry-core_foundry__contract_validate`.

## Degradation

| Missing | Behaviour |
|---|---|
| Any audit evidence | produce a non-conformance statement plus an evidence-gathering plan; refuse to draft a conformance claim |
| Manual test records | claim only what automated evidence supports, state the fraction, and mark the remainder not evaluated |
| AT test records | criteria depending on AT behaviour stay not evaluated; name them |
| Prescribed template unavailable | draft against the generic nine-element structure and flag that the prescribed form must be used to publish |

## Deliberately not covered

Running the audit · fixing barriers · deciding legal scope · disproportionate burden assessments
(recorded as a claim to be substantiated, never assessed) · substituting for testing with disabled
users · interpreting an enforcement notice · certifying conformance — nothing here is a certification
and no output may be presented to a buyer or regulator as one.

## References

- `references/evidence-classes.md` — what each class of evidence can support, per criterion type
- `references/statement-structure.md` — the nine mandatory elements and drafting rules
- `references/criteria-mapping.md` — mapping WCAG criteria to the instruments that reference them
