---
name: data-classification
description: "Use when a review is about to raise a PII, sensitive-data or leaked-credential finding, or when deciding whether a value may go in a repo, doc site, ticket or log. Classifies the value into four tiers, gates it on who can read where it lands, then sets severity."
license: MIT
---

# Data classification for code review

Most bad calls on sensitive-data findings come from skipping straight to a severity.
The reviewer sees something that *looks* alarming, labels it PII, and files a blocker.
The method below has two steps before severity, and both are cheap:

1. **Classify** the shape.
2. **Gate** it on the audience of wherever it is going.
3. *Then* assign severity.

The most common miss this prevents: internal business data — a customer's legal-entity
name plus an account ID plus a usage metric — flagged as personal PII at blocker severity,
when it is business-confidential data whose real severity depends entirely on who can read
the file it landed in.

## The four classes

Adapt the names to your organization's policy if it already has one, but keep the shape:
four tiers, each with a defined permitted audience.

| Class | What it is | Who may read it |
| --- | --- | --- |
| `public` | Already disclosed, or intended for disclosure | Anyone |
| `internal` | Non-public operational business data with no special designation — the default | Any authenticated member of the organization |
| `confidential` | Data whose disclosure harms a person, a customer or the business: personal contact details, customer usage and account data, internal financials, legal records | A named role or team, not everyone internal |
| `restricted` | Data under a specific legal or contractual regime: government identifiers, compensation, health records, cardholder data, material non-public information, raw customer-submitted content | A narrowly named group — sometimes nobody, by design |

Two boundaries do most of the work:

- **`confidential` is about a *person or a customer*, not about "it felt sensitive".**
  A company's legal name and its CRM account ID are customer business data. An employee's
  home address is personal data. Both are `confidential`; conflating them produces the
  wrong remediation.
- **`restricted` never has a safe destination.** Cardholder data and material non-public
  information do not become acceptable because the repository is private. If the class is
  `restricted`, the audience gate does not soften it.

If you cannot place a shape, say so — "ambiguous between `internal` and `confidential`" is
a usable finding. Silently picking the scarier one is not.

## The audience gate

Before assigning any severity, answer:

> Who reads the artifact this data lands in — the file, the repository, the docs site, the
> chat channel, the log stream — and is that audience already permitted to read this class?

The gate sets **impact**, and impact is the only thing severity encodes. It does not set
whether this change introduced the exposure (that is `in_diff`) and it does not set how
sure you are of the audience (that is `confidence`). An audience you could not verify is
medium confidence at the severity the class earns, not a lower tier. See Case C.

Severity names below are the contract values; `code-review-standards` owns what they mean and their
prose names for Markdown reports.

### Case A — the destination is internal-only

A private repository, an internal wiki page, an internal chat channel, a mirror verified to
return 404 to anonymous requests.

- `public`, `internal` → **no finding.** The audience is authorized and the class is the
  internal baseline, so nothing reached anyone without the permit. This is the one place
  where raising nothing is correct — because there is no exposure, not because the exposure
  is small.
- `confidential` → **MINOR** when the data is no more sensitive than what already lives in
  the systems the same audience can already read. The diff is not a re-disclosure, so the
  impact is reduced; the exposure is still real, so the finding is still real. Not a NIT —
  NIT means no true impact, and a confidential value sitting in a tracked file has some.
  → **MAJOR** when the audience is broader than the class's permitted group. Internal
  financials in a repository every engineer can read is a MAJOR: "any employee" is not the
  finance team.
- `restricted` → **BLOCKER**, regardless of audience. These classes' permitted groups are
  narrower than "anyone internal", so an internal destination does not authorize them.

### Case B — the destination is public

A public repository, a published docs site, a blog post, an artifact handed to a customer.

- `public` → fine.
- `internal` → **NIT** if the shape is already publicly known — republishing a service name
  that already appears on a public mirror exposes nothing new. **MAJOR** if it introduces a
  new internal name whose existence was not previously public. If you could not confirm the
  name is already public, keep the MAJOR and set confidence to MEDIUM; that drives the
  verdict to incomplete instead of quietly lowering the tier.
- `confidential` or `restricted` → **BLOCKER**. The class definition is "not for public
  disclosure".

### Case C — the destination's visibility is uncertain

A mirror whose visibility has not been checked this session, a docs site with ambiguous
access controls, a new artifact type with no documented audience.

**Default to Case B, the stricter gate, and ask.** State the uncertainty in the finding:
"audience visibility unverified; treated as public until confirmed."

The ask has a field. Record the restrictive severity Case B earns and set confidence to
MEDIUM, which drives the aggregate verdict to incomplete and asks a human to look. Do not
express the uncertainty as a lower severity. That is exactly the axis fold the contract
exists to prevent.

## Procedure

1. **Classify.** Which of the four classes is this shape? If undecidable, name both
   candidates rather than skipping the step.
2. **Determine the destination audience.** Where does this artifact live and who reads it —
   internal-only, public, or uncertain?
3. **Apply the gate.** Look up the severity for the class-plus-audience pair.
4. **Record the reasoning in the finding.** Cite the class and the audience determination,
   so a later reviewer can validate the call or re-classify when the audience changes.
5. **State the snap-back condition.** When the severity is MINOR because the audience is
   internal, or NIT because the shape is already public, name the change that would raise
   it. Snap-back describes impact under a *different* audience; it is never a reason to
   record a lower tier than today's audience already earns.

Step 4 is the one people skip, and it is the one that makes the finding durable.

<example>
Not actionable: "Customer name in a doc — Medium."

Actionable: "`confidential` customer data (`Example Corp` plus CRM account id `ACCT-0001`) in a
private-repository document; audience verified internal-only (anonymous fetch returned 404).
MINOR, `in_diff: true`, `confidence: HIGH`. Snaps to BLOCKER if this repository or its mirror
becomes public."
</example>

That MINOR is load-bearing: at the default blocking floor it can fail the job today, and the
snap-back has a tier to snap from. Filed as a NIT, a real exposure would never block at any floor
and would read as a cosmetic remark.

<example>
A public docs page adds `billing-ledger-v2`, an internal service name. A search of the public
mirror found no earlier mention. Finding: "`internal` service name newly published on a public
docs site. MAJOR, `in_diff: true`, `confidence: MEDIUM` (absence from public sources is not
proven). Drops to NIT if the name is shown to be already public."
</example>

## Recurring wrong calls

- **A customer name plus an account ID read as personal PII.** It is customer business
  data. It matters, but it is not a person's contact information and the remediation differs.
- **Downgrading because the audience is small.** A small authorized audience means the
  severity the class earns is already lower; it is not a second discount applied on top.
- **"An architecture decision record documents this, so it's fine."** Documenting a
  disclosure does not authorize it. The gate is about who can read the file.
- **"That customer is public anyway."** A customer being publicly known does not make the
  *combination* of that customer with an internal metric public.
- **"It's only an example."** An example value in a tracked file is a value in a tracked
  file. Use obviously synthetic placeholders.
- **"The audience is authorized, so it's a NIT."** If the audience is genuinely authorized
  and the class is the internal baseline, there is no finding at all. If the class is
  higher, there is a real one. NIT is neither.

## Verify

Before filing, confirm the finding states all four: the class, the destination and how its audience
was determined, the severity, and (for a `MINOR` or `NIT`) the snap-back condition. A finding missing
one goes back through the procedure.

Without a checkout, classify pasted values the same way, and treat the destination's audience as
uncertain (Case C) unless the user states it.
