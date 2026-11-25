---
name: policy-representation-nppf-2024-12
description: >-
  ARCHIVED - December 2024 NPPF edition (superseded 17 August 2026). Use only when the user explicitly asks to work under the pre-August-2026 framework and has confirmed they want the archived skills; outputs must state they cite a superseded framework. 
  Draft a policy-led representation on a UK planning application — in **support**
  or in **objection**, as the user chooses — from a policy compliance assessment.
  Each point is anchored to a quoted adopted development-plan policy and to the
  application's own documents, the other side is acknowledged, and the ask is
  clear (grant, grant subject to conditions, refuse, or do not determine yet). Will
  not manufacture policy compliance or conflict to fit a stance, and flags any
  mismatch between the stance and the evidence. Use for "write a letter of
  support", "draft an objection based on the policies", "write my representation".
  England-focused. Not legal advice; no warranty; output requires human review,
  and a representation is normally published in the submitter's name.
license: MIT
---

# Policy representation — support or objection

Turn a policy analysis into the letter that actually gets sent. This skill takes the scored
policy table from **policy-compliance-assessment** and drafts a representation that a case
officer can lift into the officer report — **in support or in objection, according to the
user's choice**.

It is the only skill in this repo that drafts **support** as well as objection, and the
discipline is the same either way: every point anchored to a quoted policy and to the
application's own documents, the other side acknowledged, and an ask the analysis can carry.

## When to use

The user has a policy analysis (or the material for one) and asks: "write my representation",
"draft a letter of support for this application", "draft an objection based on the local plan
policies", "put this into a letter I can send to the council".

Run **after** `policy-compliance-assessment`. If no policy analysis exists yet, run that skill
first — this one does not assess policy, and a representation asserting policy conclusions that
have not been worked through is precisely the thing councils discount.

Not this skill: the four topic representation skills (`ecological-`, `transport-`, `heritage-`,
`flood-representation`) draft **objections on their own technical grounds** and own the
deficiency analysis for those topics. Where they have run, integrate their points here rather
than restating them — or let them stand as their own representation and use this skill for the
policy case.

## What you need first

- The **policy analysis** — the plan register, the scored policy table (with quoted
  requirements, the evidence, the weight tiers and the A/B/C classification), and the
  accordance statement. This is the skill's raw material.
- The **user's chosen stance** — support or objection (see the next section before accepting
  it).
- The **application details** — reference, site address, proposal description, council, and the
  case officer's name if known.
- The **application documents** for the facts each point relies on, quoted.
- The **consultation deadline** and the **submission route** — normally the comment form on the
  council's planning portal, or an email quoting the application reference. Note that material
  considerations can be raised at any time before the application is determined, so a missed
  consultation deadline is not necessarily the end.
- **Anything from `planning-balance`**, if it has run — its four outcomes map directly onto the
  ask this skill states.
- What the user is willing to make **public** (see the publication warning below).

## Stance and integrity (read before drafting)

**The stance is the user's to choose. The evidence is not.**

A representation is the user's own; they are entitled to support or oppose an application for
their own reasons, and this skill drafts what they ask for. What it will not do is invent the
policy case for it.

- **Only make points the analysis supports.** Every point must trace to a policy in the table,
  with its quoted requirement and its evidence. No point may overstate a score — a `-1` tension
  is not written as a breach, and a `+1` compliance is not written as a positive benefit.
- **Never manufacture compliance or conflict**, misquote a policy, quote a requirement out of
  its exception limbs, or present an unassessable point (`?`) as a demonstrated one.
- **Where the requested stance runs against the analysis, say so plainly, then offer the
  honest routes.** Set out which points do and do not support the stance, and offer:
  1. draft on the supportable points only, with the mismatch stated to the user (and, where
     integrity requires, acknowledged in the letter itself);
  2. a stance that fits the evidence better — *support subject to conditions*, *no objection but
     requesting conditions*, or *objection limited to named policies*;
  3. the opposite stance.
  Then follow the user's decision, and draft it properly.
- **Do not hide the other side.** An objection that ignores the policies the scheme complies
  with, or a letter of support that ignores a `-2` conflict, invites the reply that the writer
  has not read the plan. Acknowledging and answering the contrary point is what makes a
  representation credible.
- **Declare an interest.** If the user is the applicant, their agent, a relative, an employee, a
  competitor, a prospective purchaser, or is writing as part of an organised campaign, the
  representation should say so. Undisclosed interests and identical template letters are
  discounted when spotted — and rightly.
- **Write in the user's own words.** The templates are skeletons, not text to submit verbatim.
  A representation in the writer's own voice, on this application's facts, carries weight that a
  circulated form letter does not.
- **A representation is public.** In the UK it is normally **published on the council's portal
  in the submitter's name** and kept on the record. Names are usually published; addresses,
  emails and signatures are usually redacted, but practice varies — so include only personal
  detail the user is content to see published, and say this before they send.

## Workflow

### Step 1 — Intake and confirm the stance
Take the policy analysis and the stance. Before drafting, run the **mismatch check**: does the
weight of the analysis point the same way as the requested stance? If not, apply the integrity
routes above and settle the stance with the user before writing.

### Step 2 — Select the points to lead on
A representation is not the policy table restated. Choose **three to six points**, ordered by
force:

- lead with the highest-magnitude scores (`-2` / `+2`) on policies flagged **most important**;
- include a `?` point where the gap is material — it carries the "do not determine yet" ask;
- drop `0`s, and drop `-1`s on peripheral policies. Filler dilutes; a short letter making three
  policy points well beats a long one making eleven.
- prefer **development plan** policies to national or emerging ones. Where the plan carries the
  point, national policy is support, not the lead — and an emerging policy leads only where
  nothing adopted covers the matter, with its limited weight stated.

### Step 3 — Build each point
One point per numbered section, each with the same anatomy (see
[`references/house-style.md`](references/house-style.md)):

1. **The conclusion as the heading** — "The proposal conflicts with Policy `[ref]`…" or "The
   proposal accords with Policy `[ref]`…".
2. **The policy requirement, quoted**, with the plan name and adoption date.
3. **The fact, from the application's own documents** — quoted, with the document, author, date
   and paragraph or drawing reference.
4. **The conclusion, reasoned** — why the fact does or does not satisfy the requirement.
5. **The ask**, if the point carries one.

### Step 4 — Answer the other side
- **In objection:** acknowledge the policies the scheme complies with and the benefits it
  claims, then explain why the conflicts nevertheless outweigh them. Where a benefit is
  unsecured or unquantified, say so — with the applicant's own document quoted.
- **In support:** acknowledge the principal objections and the conflicts the analysis found,
  then explain why they are outweighed, are matters of detail, or can be secured by condition.
  Support that engages with the objections is far more useful to a case officer than support
  that does not.

Frame both against the statutory starting point — determination in accordance with the
development plan unless material considerations indicate otherwise — and take the current
citations, including whether the presumption in national policy is engaged, from the
**national-planning-policy** skill. Do not cite an NPPF paragraph number that has not been
verified at run time.

### Step 5 — State the ask
The ask must be one the analysis can carry, and consistent with **planning-balance** where it
has run:

| Stance | Available asks |
|---|---|
| **Support** | Grant permission · grant subject to specified conditions or obligations securing the benefits relied on |
| **Objection** | **Refuse**, where the analysis shows demonstrated conflict (A) · **do not determine yet**, where material policy requirements cannot be assessed on the submitted evidence (B) · **grant only subject to specified conditions**, where the point is resolvable (C) |

Conditions and obligations asked for must themselves be capable of meeting the statutory tests
— take those from the **national-planning-policy** skill. Over-asking (refusal where a
condition would plainly do) weakens the whole representation.

### Step 6 — Draft
Draft to [`references/house-style.md`](references/house-style.md) and the matching skeleton in
[`references/representation-templates.md`](references/representation-templates.md): header →
RE line → opening (consultation status, stance, request to be placed on the file) → the policy
framework as a short bulleted list → numbered points → the other side answered → numbered
**summary of requests** → the stance sentence → sign-off.

### Step 7 — Check before sending
- Every policy quoted is from the **adopted** document, with its name, adoption date and
  reference — and matches the analysis.
- Every fact is quoted from an application document, correctly referenced.
- No point overstates its score; no `?` is written as demonstrated; no `-1` is written as a
  breach.
- The other side is acknowledged and answered.
- The stance, the points and the ask are consistent with each other.
- Any **interest is declared**; the text is in the user's own words, not a form letter.
- The ask is concrete, correctly timed ("before determination"), and passes the conditions and
  obligations tests where it asks for them.
- Any NPPF/PPG citation has been verified at run time against the current edition.
- The **submission route and deadline** are given to the user.
- **Hand back to a human, with the two warnings:** the draft must be read and checked, and
  submitting it puts a **public document in the user's name** on the council's portal.

## Reference files

- [`references/house-style.md`](references/house-style.md) — how a strong policy-led
  representation reads, in either stance: voice, structure, the anatomy of a policy point, and
  the moves specific to support and to objection.
- [`references/representation-templates.md`](references/representation-templates.md) — two
  skeletons (objection and support) with condensed, annotated worked examples.

## Scope and limitations

- **Not legal advice, and no warranty.** A drafting aid for a lay representation; not a
  substitute for a solicitor or a planning consultant; guarantees no outcome; provided "as is".
- **Human review is necessary before submitting.** A person must check every quotation, policy
  reference and figure against the actual documents.
- **A UK planning representation is a public document in the submitter's name** — normally
  published on the council's portal and kept on the record. Include only personal details the
  user is content to make public.
- **England-focused.** The policy framework cited is England's; flag and adjust elsewhere.
- **Evidence-bound and stance-honest.** The user chooses the stance; the skill does not bend
  the evidence to it, and says so when the two do not match.
- **"The policies don't support the letter you want" is a valid, valuable output** — as is
  advising a narrower stance than the one requested.
