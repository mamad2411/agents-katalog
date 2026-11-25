---
name: planning-balance
description: >-
  The final "so-what" test for a planning representation: given the assembled,
  evidenced grounds against a UK planning application, anticipate the
  decision-maker's planning balance — identify the governing statutory/policy
  tests (s.38(6), the location-based presumption of the August 2026 NPPF
  (S3–S6), heritage substantial weight, Green Belt very
  special circumstances, the transport and flood tests), weigh harms against
  the scheme's benefits honestly, and recommend what the representation should
  actually ask for: refusal, deferral for information, or conditions — or
  advise that the balance favours approval. Run after application-triage and
  the representation skills. England-focused. Not legal advice; no warranty;
  output requires human review.
license: MIT
---

# Planning balance — the "so-what" test

A planning decision is not the sum of technical defects. This skill runs **last**, after
the grounds have been assembled and evidenced, and answers the question every strong
representation must survive:

> Even if these harms and deficiencies exist, are they sufficient — under the tests that
> actually govern this application — to justify refusal?

The objector is not the decision-maker. What this skill does is **anticipate the balance
the case officer must strike**, so the representation asks for the outcome the balance can
actually support — which is what makes it liftable into the officer report rather than
filed as noise.

## When to use

- As the **final step** of the chain: `application-triage` has ranked the grounds, the
  representation skills have evidenced them, and each point carries its A/B/C
  classification. Run this before anything is drafted into a final ask.
- Directly, when the user asks: "would this actually be refused?", "is our case strong
  enough?", "should we push for refusal or for conditions?"

## What you need first

- The **evidenced grounds**, each classified **(A)** demonstrated unacceptable impact /
  **(B)** insufficient evidence / **(C)** conditionable (the representation skills produce
  this), and the **development-plan policies** each ground conflicts with.
- The **policy compliance assessment** from the companion **policy-compliance-assessment**
  skill, where it has run — the plan register, the policy-by-policy accordance scores (-2 to
  +2, with `?` where a policy requirement cannot be assessed), the weight tiers, and its
  accordance statement. Two cautions carry through to the balance: the scores are **never
  totalled or averaged** — accordance with the plan **read as a whole** is the judgement made
  here, and one significant conflict with the plan's strategy can outweigh many compliances on
  matters of detail; and every `?` is a **(B)**, so it bears on whether the balance can lawfully
  be struck at all rather than weighing as harm.
- The **scheme's claimed benefits** — from the Planning Statement and application forms:
  housing numbers (market and affordable), economic claims, regeneration, BNG, public
  realm. The balance has two pans; a representation that never engages with the benefits
  is not doing the exercise.
- **Where the application is an amendment** (s.73 variation, s.96A non-material amendment):
  the **parent permission and every earlier amendment**, and the officer report that granted
  the parent. The balance struck here is between the amended scheme and the permission **as it
  already stands** — the method for rebuilding that baseline is in the **application-triage**
  skill's `references/amendment-applications.md`.
- The **site constraints** that switch tests on or off (Green Belt, designated heritage,
  flood zone, habitats sites — triage records these).
- The **consultee positions** — an unresolved statutory-consultee objection changes what
  the balance can conclude.
- The companion **national-planning-policy** skill for the current citations: s.38(6) and
  plan primacy, how the **presumption in favour of sustainable development** (NPPF S3–S6)
  bears on this site — within or outside a settlement, any S5 gateway claimed (e.g. the
  S5(1)(j) unmet housing need route via housing land supply / Housing Delivery Test), any
  refusal-directive policy that overrides the balance, and any Annex A(2) weight question
  over the plan policies relied on — and the conditions/obligations tests.

## The integrity principle (read first)

**The balance is where over-claiming goes to die.** Inflating a (B) evidence gap into an
(A) refusal case, dismissing real benefits, or demanding refusal where conditions would
plainly do, hands the case officer a reason to discount the whole representation. The
honest outputs of this skill include: "the balance favours approval — don't object",
"object, but ask for conditions, not refusal", and "the only sound ask is that the
application not be determined until X is before the Council." Each of those is a success,
not a failure. Credibility spent here is spent for every future representation too.

## Workflow

### Step 1 — Identify the governing framework
Start from s.38(6): does the assembled case amount to **conflict with the development plan
read as a whole**, or only with fragments of it? Then establish how the national presumption
bears on the site — the mechanism and current citations live in the
**national-planning-policy** skill. In outline (August 2026 NPPF — the old para 11(d)
"tilted balance" and its footnote 7 no longer exist):

- **Plan-led (the statutory default):** determine in accordance with the plan unless
  material considerations indicate otherwise; a proposal according with both an up-to-date
  plan and the Framework's decision-making policies "should be approved without delay"
  (S3(1)(c)). Plan conflict + no outweighing considerations → refusal is the plan-led
  outcome — but check **Annex A(2)** first: a plan policy materially inconsistent with the
  Framework's national decision-making policies carries only "very limited weight" unless
  the plan was examined against this Framework, so a case resting on such a policy is far
  weaker than its adopted status suggests.
- **Within a settlement (S4):** approval unless the benefits "would be substantially
  outweighed by any adverse effects", assessed against the national decision-making
  policies. This pro-approval balance applies **regardless of plan status** — a materially
  harder target for an objector than the old tilted balance was.
- **Outside a settlement (S5):** only the listed categories should be approved, each on the
  same "substantially outweighed" balance — including housing through the **S5(1)(j)**
  unmet-need gateway where the council lacks a five-year supply or scores below 75% in the
  Housing Delivery Test. A proposal outside every category needs exceptional circumstances
  (S5(4)) — a strong objector's point where it holds.
- **The override:** under S4(2)(c) and S5(2) the presumption yields where the proposal
  would fail a national decision-making policy that directs refusal in specific
  circumstances (habitats/SSSIs, Green Belt, flood, substantial heritage harm,
  transport…) — the successor to the old footnote 7 disapplication. Which of S4/S5
  governs, which gateway is claimed, and whether the override bites is often the single
  most strategic fact in the case.

### Step 2 — Apply the ground-specific gateways
Some grounds carry their own test that must be run *before* the general weighing — take
the current citations from the topic skills and the national-planning-policy skill:

- **Habitats Regulations** — not a balance at all: if adverse effect on a European site's
  integrity cannot be ruled out, permission cannot lawfully be granted (a hard stop; also
  the EPS derogation tests). These outrank everything else raised.
- **Green Belt** — inappropriate development requires **very special circumstances**; the
  applicant carries that burden, not the objector.
- **Heritage** — characterise the harm level honestly, then apply the statutory
  **considerable importance and weight** and the NPPF substantial-weight/public-benefit
  tests (since August 2026 the Framework says "substantial weight", not "great weight").
- **Flood** — the **Sequential Test** is a gateway: if it fails, the balance is not
  reached; the development must also be safe for its lifetime without increasing risk
  elsewhere.
- **Transport** — on capacity/safety the NPPF now *directs* refusal where the network
  impact would be **severe** or the highway-safety impact unacceptable (TR6(4), including
  the construction phase) — a refusal-directive policy that can also trigger the S4/S5
  override — but the evidential bar stays high; otherwise the ground argues policy
  non-compliance, which weighs but rarely decides alone.

### Step 3 — Weigh honestly
Set the surviving harms (with their statutory/policy weightings) against the benefits —
and scrutinise the benefits with the same evidence discipline the representation skills
apply to harms: unquantified economic claims, double-counted open space, or "affordable
housing" without a secured obligation attract reduced weight, and saying so (with the
applicant's own document quoted) is itself good representation material. Note which
harms are (B)-class: an unresolved evidence gap does not weigh as demonstrated harm — it
means the balance **cannot yet lawfully be struck**, which is its own conclusion.

**On an amendment application the two pans hold different things.** The comparison is with the
permission **as it already stands**, not with an undeveloped site, and that changes what counts
on each side:

- **Benefits already committed by the parent permission are not benefits of the amendment.**
  The housing, the jobs and the BNG were secured by the earlier grant; only what the change
  *adds* belongs in the benefits pan. An applicant re-presenting the parent scheme's benefits
  as the case for the amendment is double-counting, and saying so with their own document
  quoted is good representation material.
- **Benefits the amendment takes away are harms.** Where the change removes, dilutes or
  defers something the original permission secured — affordable units, screen planting,
  habitat, a mitigation measure the officer report relied on — the loss weighs against it.
- **Weigh the chain, not just this link.** Where several amendments have preceded this one,
  the erosion they add up to is the honest measure of what is being asked; for a s.96A that
  cumulative view is also the statutory test (s.96A(2) TCPA 1990).
- **The fallback only counts if it can still be built.** The parent permission is a genuine
  fallback and carries real weight — but only while it remains capable of lawful
  implementation. Where what has already been built makes completing the earlier scheme
  physically impossible, further development under it is unlawful (*Hillside Parks Ltd v
  Snowdonia National Park Authority* [2022] UKSC 30). Check before conceding the fallback.

### Step 4 — Conclude and recommend the ask
One of four honest outcomes, driving what the representation requests:

1. **Refusal** — (A) grounds sufficient under the governing tests: say which test fails
   and why the benefits don't save it.
2. **Do not determine yet** — (B) grounds dominate: the ask is the missing information
   before determination, put as "the Council cannot presently conclude X".
3. **Approve-with-conditions posture** — the harms resolve to (C): the ask is the precise
   conditions/obligations (which must themselves pass the NPPF DM6 conditions tests and,
   for obligations, CIL Regulation 122(2) — the Framework no longer restates the
   obligations tests; cite the regulation).
4. **The balance favours approval** — say so, and advise not objecting (or a short
   representation supporting conditions only).

Output a **short balance statement** the user can lift into the representation's opening or
closing. Structure it — don't run it into one long paragraph:

- **one sentence** naming the framework that governs (s.38(6) and the operative test);
- the **decisive harms, each with its weight** — as short bullets if there are more than
  two, never chained through a paragraph with semicolons;
- **one sentence** acknowledging the benefits and the weight they carry;
- **one sentence** with the conclusion and the ask.

Then hand back to a human with the standard warnings: **review before use, and anything
submitted is normally published on the council's portal in the submitter's name.**

## Scope and limitations

- **Not legal advice, and no warranty.** The balance is ultimately the decision-maker's
  planning judgement; this skill anticipates it to sharpen a lay representation, is not a
  substitute for a solicitor or planning consultant, guarantees no outcome, and is
  provided "as is".
- **Human review is necessary before use.** A person must check the tests invoked and the
  weights claimed against the actual documents and current policy.
- **England-focused.** The tests cited are the England framework; flag and adjust outside
  England.
- **Evidence-bound.** Weigh only harms that survived the representation skills' evidence
  discipline and benefits actually claimed in the application; invent neither.
- **The honest answer is sometimes "the balance favours approval."** Treat that as a
  valid, valuable output.
