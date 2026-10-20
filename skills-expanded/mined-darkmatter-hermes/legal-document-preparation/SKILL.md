---
name: legal-document-preparation
description: "Draft and fill legal contract packets from templates."
version: 1.1.0
---

# Legal document preparation

## When to use

- User asks to "finish", "put together", "complete", "draft", or "assemble" a
  legal contract, agreement, note, or document set.
- User pastes or references a `.pages`, `.docx`, or `.pdf` contract packet
  with bracketed placeholders that need filling.
- User needs a multi-exhibit legal package (term sheet + agreement + note +
  consent + checklist) produced consistently from one set of deal terms.
- Cross-border or related-party deal where tax/corporate/legal analysis
  affects whether the document can be finalized without specialist counsel.
- User asks how family/affiliate cash can enter the business (loan vs equity
  vs gift vs invoice), whether a related-party loan can be interest-free, what
  docs a loan needs, CPA-vs-lawyer, or wants a Dropbox/docx loan packet.

## When NOT to use

- Reviewing an existing completed deal's equity/stock ownership questions →
  use `private-investment-deal-review`.
- Pure `.docx` mechanics (create/read/edit/track-changes) with no legal-domain
  judgment → use `docx`.
- Filling a PDF form → use `pdf-form-filling`.

## Core principle

Legal drafts produced from reference packets are **counsel-ready, not
sign-ready**. The agent's job is to populate factual fields (names, amounts,
dates, rates, addresses) and flag legal/tax judgment points for specialist
review — never to silently choose a legal or tax outcome.

### Classify capital character before drafting

If the user describes money "into the business," lock **loan / equity / gift /
revenue** first. Do not draft an invoice path for what is economically a loan
or capital contribution. Domestic related-party loan rules (AFR, packet
contents, CPA vs lawyer, Dropbox delivery): see
`references/us-related-party-business-loans.md`.

## Workflow

### 1. Locate and inventory all source variants

Before editing anything, find every copy and variant of the source document:

- Original authoring file (`.pages`, `.docx`, etc.) — check `~/Documents`,
  `~/Downloads`.
- Exported PDF.
- Prior render or conversion work directories (e.g. Codex work folders).
- Use `mdfind -onlyin ~ '<search terms>'` to find siblings by
  Spotlight content.
- Use `search_files` with filename globs (`*loan*`, `*contract*`, etc.).

### 2. Prefer clean editable siblings over proprietary-format parsing

Apple `.pages` files are Zip archives of `.iwa` (protobuf-like) blobs. Parsing
IWA internals via `strings` works as a **fallback only** — it loses ordering,
truncates text, and mixes noise with content. Instead:

- Search for a `.docx` or `.pdf` twin of the same document first.
- If a `.docx` twin exists, extract text with:
  ```bash
  textutil -convert txt -output /tmp/document.txt "/path/document.docx"
  ```
- If only a `.pdf` exists, use `web_extract` or `pdftotext` (if installed).
- If only `.pages` exists, extract with `strings` on IWA files as a last
  resort — verify completeness against `preview.jpg` inside the Pages
  archive.

See `references/pages-docx-contract-intake-workflow.md` for the full
extraction recipe.

### 3. Determine document status

Classify the source before drafting:

- **Completed agreement needing edits** — proceed with targeted edits.
- **Template with placeholders** — fill placeholders, preserve disclaimers.
- **Educational/reference packet explicitly not for signature** — keep
  "reference only" labels; do not present as executable without counsel
  review. The packet's own disclaimers govern its status.

### 4. Inventory placeholders

Before filling anything, list every bracketed field so nothing is missed:

```bash
grep -oE '\[[^]]{1,100}\]' /tmp/extracted_text.txt | sort | uniq -c | sort -rn
```

Group placeholders by type: party names, amounts, rates, dates, legal-form
identifiers, and legal-judgment fields (e.g. "secured/unsecured",
"governing law", "prepayment terms"). Separate factual fills from legal/tax
judgments.

### 5. Collect deal terms through a structured intake (once)

Write an intake form (`01-intake.md`) covering:
- Parties (borrower, lender, corporate forms, jurisdictions)
- Relationship map (ownership %, control, affiliate links) — **critical for
  related-party or cross-border deals; party names alone are insufficient**
- Economics (principal, currency, rate, term, payments, maturity,
  prepayment, default grace)
- Commercial terms (use of proceeds, security/collateral, covenants)
- Legal mechanics (governing law, venue, notices, board approvals)

Mark unknowns "TBD." Do NOT collect sensitive identifiers (EINs, bank-account
numbers, personal IDs) in chat — those remain closing placeholders filled at
signing.

**Batch intake questions by theme and ask once.** Do not run serial
single-question rounds — once the gating facts are in (parties,
relationship shape, principal, currency, key commercial terms), fold
remaining unknowns into visible `[[TBD]]` placeholders and **draft
immediately.** Unknowns that require counsel judgment become
`[[TBD—COUNSEL/CPA]]`; unknowns that require the user to confirm a fact
become `[[TBD—CONFIRM]]`. Do not block drafting on counsel-judgment fields.

### 6. Cascade consistent terms across all exhibits

Normalize deal terms into one structured record (e.g. `deal_terms.json`),
then populate every exhibit from the same values. Cross-check all exhibits
for identical:
- Principal, currency, rate, day-count basis
- Payment dates, maturity, prepayment terms
- Default grace periods, governing law, notices

Inconsistency between term sheet, promissory note, and loan agreement is a
common source of recharacterization risk in tax-sensitive deals.

**Validate the terms record before generating.** Check for duplicate JSON
keys, undefined generator variables, and currency-formatting bugs (e.g.
`US$$10,000,000` from nesting `$` in an f-string with a `$`-prefixed
variable). Money variables should hold digits only; the `US$` prefix goes
in the template string, never in the variable value.

### 7. Keep legal/tax judgments as visible TBDs

Every unresolved legal or tax judgment should remain conspicuously marked
(e.g. `[[TBD—COUNSEL]]` or `[[TBD—CPA]]`). Do not silently guess:
- Whether a tax safe harbor applies
- Whether a withholding exemption holds
- Whether a feature terminates a tax election
- A specific withholding rate or treaty benefit
- State-law suitability or enforceability

These depend on attribution, treaty eligibility, entity classification, and
facts the agent cannot verify. Phrase them as questions for specialist
confirmation, not as settled conclusions.

### 8. Produce a counsel open-issues memo

Write `00-open-issues.md` alongside the drafts. Organize by category:
- Tax-election eligibility (e.g. S-corp, partnership, LLC classification)
- Arm's-length pricing / transfer-pricing considerations
- Withholding and treaty analysis
- Foreign-ownership / entity-classification reporting
- Debt-vs-equity characterization support (for debt-shaped transactions)
- Foreign-country-side requirements (left to foreign counsel)
- State-law and enforceability
- Currency / FX considerations
- Document consistency checklist

Each issue should state **what to ask counsel**, not what the answer is.

### 9. Label drafts by actual status

Every draft document should carry a header/footer matching its status:
- "DRAFT FOR COUNSEL REVIEW — NOT SIGN-READY"
- "REFERENCE DRAFT — ATTORNEY MARKUP ONLY"

Do not convert a "reference only / not sign-ready" packet into something
presented as executable without counsel review.

### 10. Verify generated output

After generating `.docx` files, verify them before delivering:

- Use `textutil -convert txt -stdout` or python-docx (via `terminal`, not
  `execute_code` — the sandbox Python may not have python-docx installed)
  to extract body text, headers, and footers.
- Search generated text for: malformed money strings (`$$`), stale template
  labels (`[State]`, `[BORROWER LEGAL NAME]`), inconsistent party names,
  missing draft legends, and accidental factual assertions.
- Cross-check that principal, currency, governing law, and parties appear
  identically in every exhibit.
- Headers and footers are not extracted by `textutil` body conversion —
  verify them through python-docx's `doc.sections[0].header` / `.footer`.

Run `scripts/verify_docx_packet.py` for automated consistency checks across
a generated packet.

## Related-party and cross-border deals — additional intake

When the parties are related (family, affiliate, common ownership) or the deal
is cross-border (U.S. ↔ foreign entity), collect before finalizing economics:

- Who owns each entity (% each, citizenship)
- Who controls each entity (direct, indirect, constructive)
- Whether any U.S. person controls the foreign entity
- Exact family/affiliate/common-ownership link
- Whether the foreign entity could be classified as a Foreign Flow-Through
  Entity (FFTE) or Foreign-Owned/Controlled Entity (FOCE) for U.S. tax purposes
- Existing intercompany balances, loans, agreements, or side letters
- Foreign entity's U.S. presence (office, branch, permanent establishment,
  U.S. trade/business)

These facts drive attribution, treaty eligibility, withholding, and
debt-vs-equity analysis. They are specialist determinations — the agent
raises them, it does not resolve them.

**Distinguish relationship layers carefully.** A founder/adviser
relationship with acknowledged influence but zero ownership is not
automatically "common ownership" or a statutory related-party relationship.
Use neutral labels ("family-connected, no reported common ownership") until
counsel classifies the relationship. Separate: direct ownership, attributed
ownership, formal management authority, contractual/economic rights,
practical influence, prior commercial dealings, and family relationship —
each has different tax implications.

See `references/cross-border-corporate-loans.md` for a condensed knowledge
bank covering S-corp eligibility, withholding/portfolio-interest, debt-vs-
equity characterization, Japanese-side requirements, and FX considerations.

For **domestic U.S. related-party** loans (both parties US, family/affiliate
capital into the operating company), see
`references/us-related-party-business-loans.md` — capital character table,
AFR/below-market interest, minimum doc packet, CPA-vs-lawyer lanes, and
Dropbox `.docx` delivery.

## Pitfalls

- **Do not parse IWA internals when a DOCX/PDF sibling exists.** `strings`
  on `.iwa` files loses ordering, truncates text, and mixes UUIDs/format
  noise with content. Always search for clean siblings first.
- **Do not encode unverified tax/legal conclusions as settled rules.** A
  prior session's statement that "safe harbor X is unavailable" or
  "exemption Y fails" may depend on attribution, treaty eligibility, or
  entity classification facts that were never verified. Route these to the
  open-issues memo as questions for counsel, not as reusable assertions.
- **Do not promise a withholding rate in a contract.** Withholding depends
  on treaty eligibility, attribution, and documentation. The borrower should
  not promise a rate or waive required withholding without CPA advice.
- **Do not convert a reference packet into a sign-ready agreement.** If the
  source says "not legal/tax/accounting/investment advice" or "not a
  sign-ready agreement," keep that status until qualified counsel approves.
- **Do not guess state-law suitability.** Confirm the selected state law
  permits the interest rate, recognizes foreign-lender enforceability, and
  does not require state-specific foreign-lender licensing.
- **Do not assume the foreign entity owns 0% of the domestic entity.** If
  the lender owns or controls stock, the deal characterization may change
  entirely. Ask for the ownership map first.
- **Currency choice has tax consequences.** Foreign-currency-denominated
  principal can create FX gain/loss exposure for the borrower on repayment.
  Default to USD unless counsel advises otherwise.
- **Avoid oral or side arrangements with related parties.** A "no oral or
  side agreements" representation strengthens bona fide debt treatment.
- **Money-formatting in python-docx f-strings.** If `PR = "$10,000,000"`
  and the template is `f"US${PR}"`, the output is `US$$10,000,000`. Keep
  money variables as digit-only strings (`PR = "10,000,000"`) and prepend
  the currency prefix in the template string only.
- **python-docx is not in the execute_code sandbox.** The sandbox Python
  interpreter may not have python-docx installed. Run python-docx
  generation and verification scripts via `terminal`, not `execute_code`.
- **Duplicate JSON keys silently overwrite.** If `deal_terms.json` has two
  `"maturity"` keys, the parser takes the last one. Validate the JSON
  before generating exhibits — duplicate keys produce inconsistent output
  across documents that reference the same field.
- **Headers/footers are invisible to textutil body extraction.**
  `textutil -convert txt -stdout` extracts body text only. To verify
  counsel-review headers and footer legends in generated `.docx` files,
  read them through python-docx: `doc.sections[0].header.paragraphs[0].text`.
- **Do not conflate governing-law concepts.** Formation state does not
  automatically determine governing law. Keep separate fields for: state
  of formation, principal place of business, governing law, venue/forum,
  and foreign qualification in operating states. All remain subject to
  counsel confirmation.
- **Corporate-form precision.** Do not guess Japanese entity type (KK/GK/
  other) or officer terminology. Confirm the lender's legal form before
  finalizing titles. Avoid mixing `代表取締役` (typically KK representative
  director) and `代表社員` (typically GK representative member).
- **Large-loan escalation.** For a material loan (e.g. $2M+ related-party, or
  $10M+ generally), add closing gates for repayment capacity, corporate
  authority, tax documentation, independent approval, transfer-pricing/
  market-rate support, regulatory reporting, and actual payment
  administration. Do not treat a polished packet as sign-ready merely because
  formatting is complete.
- **Do not promote recommendations into confirmed facts.** A recommendation
  (e.g. "father should be recused") is not a confirmed fact until the user
  or counsel confirms it. Keep `deal_terms.json` faithful to what the user
  actually said; mark recommended-but-unconfirmed actions as
  `[[TBD—CONFIRM]]`, not as settled booleans.
- **Do not claim a lawyer is always mandatory — or that a CPA replaces one.**
  Split lanes: CPA for AFR/imputed interest/books/1099; attorney for
  enforceability, entity authority, usury, security/guaranty, intercreditor.
  At ~$2M related-party, default advice is CPA necessary + lawyer light
  review best cost/benefit; CPA-only is a conscious residual-risk choice on
  clean unsecured ≥ AFR terms only. See
  `references/us-related-party-business-loans.md` §5.
- **Do not default related-party loans to 0% "for simplicity."** Contractual
  0% is possible; tax imputation + debt-vs-equity optics usually make ≥ AFR
  (or CPA-directed PIK) the default recommendation.
- **When Cooper asks for a template/packet, deliver real `.docx` into Dropbox**
  (`~/Dropbox (Personal)/docs/<Packet Name>/`), not only chat markdown.
  Verify with `textutil -convert txt -stdout` + `unzip -t` on macOS.
- **If funding already happened, stop pre-wire drafting.** Flip the whole packet
  to post-funding ratification (Prior Advance language, funding-month AFR,
  catch-up interest, Brex evidence, QBO reclass). Details:
  `references/us-related-party-business-loans.md` §8b.
- **AFR = month cash moved**, not the month you draft. Look up IRS Rev. Rul.
  for that month; mid-term for 3–9 year notes. Regenerate all exhibits after
  the rate/date change and grep for stale month names.

## Overlap with other skills

- `private-investment-deal-review` — covers reviewing completed investment
  deals (Echo.xyz SPVs, angel/SAFE rounds, equity ownership questions). A
  different class: reviewing what you own vs. drafting what you'll sign.
- `docx` — covers `.docx` mechanics (create/read/edit/template). Use as a
  tool within this workflow, but the legal-domain judgment lives here.
- `pdf-form-filling` — covers filling interactive/flat PDF forms. Different
  document class.

## References

- `references/pages-docx-contract-intake-workflow.md` — Pages/DOCX
  extraction recipe, placeholder inventory, and legal drafting safeguards.
- `references/cross-border-corporate-loans.md` — Condensed knowledge bank
  for U.S. S-corp / foreign-lender cross-border loans: S-corp eligibility,
  withholding/portfolio-interest, debt-vs-equity characterization,
  Japanese-side requirements, FX considerations, and family-connected
  mitigation patterns.
- `references/us-related-party-business-loans.md` — Domestic U.S.
  related-party business loans: capital character (loan/equity/gift/invoice),
  AFR / below-market interest, minimum doc packet, CPA-vs-lawyer lanes,
  Dropbox `.docx` delivery, books after funding, and pitfalls.
- `scripts/verify_docx_packet.py` — Automated consistency verifier for
  generated DOCX packets: checks shared terms, detects `$$` formatting
  bugs and stale template labels, enumerates unresolved placeholders by
  owner, verifies draft legends in headers/footers, and validates the
  deal-terms JSON for duplicate keys.
