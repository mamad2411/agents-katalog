---
name: planning-balance-nppf-2024-12
description: >-
  ARCHIVED - December 2024 NPPF edition (superseded 17 August 2026). Use only when the user explicitly asks to work under the pre-August-2026 framework and has confirmed they want the archived skills; outputs must state they cite a superseded framework. 
  The final "so-what" test for a planning representation: given the assembled,
  evidenced grounds against a UK planning application, anticipate the
  decision-maker's planning balance — identify the governing statutory/policy
  tests (s.38(6), the tilted balance, heritage great weight, Green Belt very
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
- The **site constraints** that switch tests on or off (Green Belt, designated heritage,
  flood zone, habitats sites — triage records these).
- The **consultee positions** — an unresolved statutory-consultee objection changes what
  the balance can conclude.
- The companion **national-planning-policy** skill for the current citations: s.38(6) and
  plan primacy, whether the **tilted balance** is engaged (most-important policies
  out-of-date / housing land supply) or **disapplied by footnote 7**, and the
  conditions/obligations tests.

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
read as a whole**, or only with fragments of it? Then establish which balance applies:

- **Plan-led (the default):** determine in accordance with the plan unless material
  considerations indicate otherwise. Plan conflict + no outweighing considerations →
  refusal is the plan-led outcome.
- **Tilted balance (NPPF para 11(d)):** engaged only where there are no relevant policies
  or the most important ones are out-of-date (check housing land supply / Housing Delivery
  Test via the national-planning-policy skill). If engaged, harm must **significantly and
  demonstrably** outweigh benefits — a materially harder target for an objector — *unless*
  **footnote 7** disapplies it (habitats sites, SSSIs, Green Belt, National Landscapes,
  designated heritage, flood risk…). Getting this switch right is often the single most
  strategic fact in the case.

### Step 2 — Apply the ground-specific gateways
Some grounds carry their own test that must be run *before* the general weighing — take
the current citations from the topic skills and the national-planning-policy skill:

- **Habitats Regulations** — not a balance at all: if adverse effect on a European site's
  integrity cannot be ruled out, permission cannot lawfully be granted (a hard stop; also
  the EPS derogation tests). These outrank everything else raised.
- **Green Belt** — inappropriate development requires **very special circumstances**; the
  applicant carries that burden, not the objector.
- **Heritage** — characterise the harm level honestly, then apply the statutory
  **considerable importance and weight** and the NPPF great-weight/public-benefit tests.
- **Flood** — the **Sequential Test** is a gateway: if it fails, the balance is not
  reached; the development must also be safe for its lifetime without increasing risk
  elsewhere.
- **Transport** — refusal on capacity/safety alone needs a **severe** residual cumulative
  impact or an unacceptable safety impact; otherwise the ground argues policy
  non-compliance, which weighs but rarely decides alone.

### Step 3 — Weigh honestly
Set the surviving harms (with their statutory/policy weightings) against the benefits —
and scrutinise the benefits with the same evidence discipline the representation skills
apply to harms: unquantified economic claims, double-counted open space, or "affordable
housing" without a secured obligation attract reduced weight, and saying so (with the
applicant's own document quoted) is itself good representation material. Note which
harms are (B)-class: an unresolved evidence gap does not weigh as demonstrated harm — it
means the balance **cannot yet lawfully be struck**, which is its own conclusion.

### Step 4 — Conclude and recommend the ask
One of four honest outcomes, driving what the representation requests:

1. **Refusal** — (A) grounds sufficient under the governing tests: say which test fails
   and why the benefits don't save it.
2. **Do not determine yet** — (B) grounds dominate: the ask is the missing information
   before determination, put as "the Council cannot presently conclude X".
3. **Approve-with-conditions posture** — the harms resolve to (C): the ask is the precise
   conditions/obligations (which must themselves pass the para 57/58 tests).
4. **The balance favours approval** — say so, and advise not objecting (or a short
   representation supporting conditions only).

Output a **short balance statement** (a paragraph, two at most) the user can lift into the
representation's opening or closing: the framework that governs, the decisive harms with
their weights, the benefits acknowledged, and the conclusion with the ask. Then hand back
to a human with the standard warnings: **review before use, and anything submitted is
normally published on the council's portal in the submitter's name.**

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
