---
name: heritage-representation
description: >-
  Evaluate the heritage/historic-environment evidence submitted with a UK
  planning application (Heritage Statement / Statement of Significance, setting
  and archaeological assessments), identify the statutory duties and national
  policy it engages, and draft a concise, well-founded objection — or advise
  that no sustainable objection exists. Covers listed buildings, conservation
  areas, scheduled monuments, non-designated assets and archaeology.
  England-focused. Not legal advice; no warranty; output requires human review.
license: MIT
---

# Heritage representation on a planning application

Help a member of the public produce a rigorous, credible representation on the **heritage /
historic-environment** merits of a planning application. The skill does three things:

1. **Evaluate** the applicant's heritage evidence against the statutory duties and current
   policy and guidance, and identify the material deficiencies.
2. **Map** each deficiency to the specific legislation, national policy and guidance it
   engages.
3. **Draft** the representation in clear, precise, concise language — or advise that the
   evidence is sound and no sustainable objection exists.

## When to use

The user has a planning application (or a listed-building-consent application) and wants to
object, or find out whether they can, on heritage grounds — harm to a **listed building** or
its **setting**, a **conservation area**, a **scheduled monument**, a **registered park/garden
or battlefield**, a **non-designated heritage asset**, or **archaeology**. Trigger phrases:
"object on heritage grounds", "is this Heritage Statement adequate", "this harms the
conservation area / the setting of the listed building", "they haven't assessed the
archaeology."

Not this skill: ecology, transport, flood risk, general amenity — separate matters.

## What you need first

- The **application reference and council**, or the **documents themselves** — uploaded,
  pasted, or already-downloaded files work directly; the companion **planning-document-search**
  skill is only needed when you don't have them (it retrieves them from the reference + council).
- The **heritage documents** — the Heritage Statement / Statement of Significance, any setting
  assessment, archaeological desk-based assessment or evaluation, and the heritage section of
  the Design and Access Statement. Also the **conservation officer's and Historic England's
  consultation responses** (often the strongest anchor).
- The **designations and their significance** — what is listed (and its grade), the
  conservation area and its **appraisal**, scheduled monuments, registered parks/gardens
  (check `planning.data.gov.uk` and the Historic England list).
- The **local plan's** historic-environment policies.
- **If this is an amendment application — the parent permission and every earlier amendment.**
  A s.96A non-material amendment or a s.73 variation supplies only the change, and the heritage
  case turns on what that change does to the asset or its setting **compared with what was
  permitted**: the approved elevations, materials, joinery, roof form and boundary treatment,
  and the conditions the conservation officer relied on. Get the parent's decision notice and
  full condition set, its approved plans, its officer report, **and every earlier amendment** —
  an accumulation of individually small substitutions is how an approved design is eroded.
  Method: the **application-triage** skill's `references/amendment-applications.md`.

## The integrity principle and two framing points (read before drafting)

**Only object where the evidence is genuinely inadequate or the harm genuinely unacceptable.**
Heritage harm is a matter of planning judgement; if significance is properly assessed and the
proposal genuinely preserves or enhances, there is **no sustainable objection** — say so.
Treat "don't object" as a valid output.

Two points specific to heritage:
- **The level of harm drives the test.** *Substantial harm / total loss* — substantial harm is
  now defined as harm that would "seriously affect a key element of the asset's significance"
  (NPPF HE5(2)(c)) — engages the very demanding HE6(5) test; any lesser harm is weighed
  against public benefits under HE6(4). Applicants routinely under-state harm — getting the
  level right is decisive. (But don't over-claim "substantial harm" either; credibility
  depends on the honest level.) ⚠ The Aug 2026 NPPF **abolished the "less than substantial
  harm" label** — don't use it when arguing under the current edition; it belongs only to
  decisions made under the pre-17-Aug-2026 editions (see the national-planning-policy skill's
  edition register and crosswalk).
- **Harm below the substantial threshold is not "neutral".** The Act requires **considerable
  importance and weight** to preserving the asset, its setting and conservation-area
  character; the NPPF requires **substantial weight** to the conservation of a designated
  asset (HE6(1)) and makes *any* harm "a matter of considerable importance and weight"
  (HE6(3)).

**Classify every point's ask — (A) refuse, (B) don't determine yet, or (C) condition it.**
An evidential deficiency is not itself a reason for refusal. For each confirmed point, be
explicit about which outcome it supports: **(A)** the evidence *demonstrates* unacceptable
harm under the applicable test → a refusal reason; **(B)** the evidence is *insufficient* for
the Council to reach the necessary conclusion (significance not assessed; archaeology not
established before determination) → the application should **not be determined** until the
information is provided; **(C)** the issue can be adequately controlled → ask for the
*specific* condition or obligation (materials, detailed design, a written scheme of
archaeological investigation). Most deficiency findings are (B), not (A) — claiming (A) on
(B) evidence is the classic credibility mistake. And test every point against (C): if a
condition would lawfully and satisfactorily resolve it, ask for that rather than refusal —
over-asking weakens the whole representation.

## Workflow

### Step 1 — Intake and read
Identify the asset(s) affected and their designation/grade; whether the effect is on the asset,
its setting, or a conservation area's character; and the application type (permission vs
listed-building consent). Read the conservation officer's / Historic England's response first.
Get the Statement of Significance and any setting/archaeology assessments.

**On an amendment, read the chain before evaluating anything:** characterise the harm caused by
the **change** against the permission **as already varied**, and assess the accumulated
substitutions together — the drawings condition is where an approved design quietly changes.

### Step 2 — Evaluate against the deficiency catalogue (function 1)
Work through [`references/deficiency-catalogue.md`](references/deficiency-catalogue.md). For
each candidate deficiency, confirm it is **present** and **material**, and capture the specific
evidence — the document, author, date, paragraph. Quote the Heritage Statement's own words.
Grade findings and lead with the decision-critical. Apply the integrity principle.

Key tests: Is **significance** assessed, and proportionately (fabric *and* setting, group
value, historic interest)? Is the **effect classified and the level of harm correctly
characterised** (positive / no effect / harm / total loss — NPPF HE5(2))? Are the **statutory
duties and the required weight** (substantial weight, HE6(1)) given effect? Is the
**public-benefit balance** genuinely carried out? For conservation areas, does the scheme
**preserve or enhance**? For archaeology, is significance established **before**
determination?

### Step 3 — Map to law, policy and guidance (function 2)
Attach the precise instrument from
[`references/national-guidance.md`](references/national-guidance.md) — the LB & CA Act 1990
duties (ss.66/72), the NPPF historic-environment policies (HE4–HE10) and the harm tests, the
PPG, Historic England guidance, the relevant case law on the statutory duties — plus the
**local plan** heritage policies and the **conservation area appraisal**. Cite specifically,
and verify every NPPF citation against the current edition first (the companion
**national-planning-policy** skill owns the edition register; for representations about
decisions made before 17 August 2026, cite the edition in force at determination).

### Step 4 — Draft (function 3)
Draft to [`references/house-style.md`](references/house-style.md) and
[`references/objection-template.md`](references/objection-template.md): header → RE line
(name the asset) → opening → bulleted framework list → numbered conclusion-headed points
(quoted evidence; establish significance / characterise harm / invoke the duty; the ask) →
numbered **Summary of requests** → objection sentence → sign-off. Keep it concise; use bullets
for lists and `(a)/(b)` for multi-limb points.

### Step 5 — Check before sending
- Every point is evidenced from the documents or cited guidance; nothing asserted.
- The harm level is characterised honestly (not over- or under-claimed).
- The statutory duties and the required weight (substantial weight, HE6(1)) are correctly
  invoked — and no abolished vocabulary ("great weight", "less than substantial harm") is
  quoted as current policy.
- Consultant-/campaign-specific framing excluded unless the user asked and it is defensible.
- Requests are concrete and correctly timed.
- Every point is classified **(A) demonstrated harm / (B) insufficient evidence / (C)
  conditionable** — and no point asks for refusal where a condition would lawfully and
  satisfactorily do.
- **Hand back to a human, with the two warnings:** the draft must be read and checked, and
  submitting it puts a **public document in the user's name** on the council's portal.

## Reference files

- [`references/deficiency-catalogue.md`](references/deficiency-catalogue.md) — the evaluation
  checklist.
- [`references/national-guidance.md`](references/national-guidance.md) — the law/policy/guidance
  catalogue with citations.
- [`references/house-style.md`](references/house-style.md) — how a strong representation reads.
- [`references/objection-template.md`](references/objection-template.md) — skeleton + annotated
  worked example.

## Scope and limitations

- **Not legal advice, and no warranty.** Not a substitute for a solicitor or a heritage
  professional; guarantees no outcome; provided "as is".
- **Human review is necessary before submitting.** A person must check every quote and
  citation against the actual documents.
- **A UK planning representation is a public document in the submitter's name** — normally
  published on the council's portal; include only personal details the user is content to make
  public.
- **England-focused.** The 1990 Act applies in England and Wales, but national policy (NPPF/
  PPG) is England; devolved policy differs — flag when outside England.
- **Evidence-bound; heritage harm is a matter of judgement.** Identify significance and harm on
  the evidence; don't assert a level of harm you cannot support.
- **The honest answer is sometimes "don't object."**
