---
name: hiring-review
description: >
  Review an offer letter and any restrictive covenants — jurisdiction check
  included. Substantive rules (covenant enforceability, pay-transparency,
  salary-history limits, exemption criteria) are researched per hire, not
  stored. Use when the user says "review this offer", "can we use a
  non-compete here", "check this offer letter", "hiring in [state]", or
  attaches an offer.
argument-hint: "[offer letter file, or describe the hire]"
---

# /hiring-review

1. Load `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint, hiring review triggers, restrictive covenant policy.
2. Use the workflow below.
3. Check: jurisdiction, classification, restrictive covenants, background check compliance.
4. Flag anything that hits the jurisdiction-specific escalation table.

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-hk-law/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

Offer letters are mostly boilerplate until they're not. The jurisdiction check
and the restrictive-covenant check are where this skill earns its keep. The
skill does not state the law — every jurisdiction-specific rule is researched
and cited at the time of review.

## Load context

`~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint, hiring review triggers, restrictive
covenant policy, offer letter template location.

## Output header

Prepend the work-product header from `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → `## Outputs` (it differs by user role — see `## Who's using this`).

## Workflow

### Step 1: Jurisdiction

Where will this person work? Not where HQ is — where *they* are.

If remote: their home state/country governs. If hybrid: usually their home
state, but check the offer letter's choice-of-law clause (may or may not hold
up).

Check the jurisdiction table in `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` for this state/country. If it's
not in the table — new jurisdiction — flag that: "First hire in [state]. The
jurisdiction table doesn't cover this. Research needed before offer goes out."

### Step 2: Classification

Exempt or non-exempt? The offer should say, and the role should support it.

| Test | Check |
|---|---|
| Salary basis | Paid a fixed salary regardless of hours? |
| Salary level | Above the applicable federal and state thresholds? |
| Duties test | Does the role actually involve the exempt duties? |

> **Research before calling exemption.** Identify the currently operative
> salary thresholds (federal and state — several states index annually and
> several have tiered thresholds by employer size) and the applicable duties
> test(s) for the role. Cite primary sources. Verify currency.

If the offer says exempt but the role description does not support the
exempt duties — flag it. Misclassification is expensive.

### Step 3: Restrictive covenants

If the offer includes a non-compete, customer non-solicit, employee
non-solicit, or confidentiality/IP assignment:

> **Research enforceability before advising.** For the employee's jurisdiction,
> identify the currently operative rules on each restrictive covenant in the
> offer. Non-compete enforceability in particular has shifted in multiple
> states in recent years through legislation, agency action, and litigation —
> do not rely on prior memory of which states permit non-competes. Note:
> - The specific type of covenant (non-compete, customer non-solicit, employee
>   non-solicit, confidentiality/trade-secret, IP assignment) — each has its
>   own rules.
> - Any salary or income threshold that conditions enforceability.
> - Any notice, consideration, or garden-leave requirements.
> - Any industry-specific carve-outs (e.g., healthcare, broadcasting).
> - Duration and geographic-scope reasonableness tests.
> - Choice-of-law and choice-of-forum enforceability for out-of-state covenants.
> Cite primary sources. Verify currency.

Per `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` restrictive covenant policy: does this hire even get one?
Some companies use them selectively. Apply the house policy first, then
research overlays from the jurisdiction.

> **No silent supplement.** If a research query to the configured legal research tool returns few or no results for the jurisdiction's exemption thresholds, restrictive-covenant rules, pay-transparency law, or any other item you're researching, report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking. Say: "The search returned [N] results from [tool]. Coverage appears thin for [jurisdiction / topic]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) flag as unverified and stop. Which would you like?" A lawyer decides whether to accept lower-confidence sources.
>
> **Source attribution.** Tag every citation in the review with where it came from: `[Westlaw]`, `[CourtListener]`, or the MCP tool name for citations retrieved from a legal research connector; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations the user supplied. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags.

### Step 4: Jurisdiction-specific requirements

Check the `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` table for this jurisdiction. Common categories to
research for each hire:

- **Pay transparency** — does the jurisdiction require a salary range in the
  posting? If so, is this offer within the posted range? Research the current
  rule (including any recent amendments or new enforcement guidance).
- **Ban-the-box** — does the jurisdiction or locality restrict the timing or
  scope of criminal-history inquiries?
- **Salary-history limits** — is the jurisdiction one that restricts asking
  about or relying on prior salary? Research current rules and recent
  amendments.
- **Required offer-letter or onboarding notices** — some jurisdictions require
  specific notices at offer or hire (wage-notice statutes, sick-leave notices,
  etc.). Research what is currently required and whether a template exists.

Cite primary sources. Verify currency.

### Step 5: Offer letter content

Read the letter. Check:

**Hong Kong does not have an "at-will" employment doctrine.** Employment contracts in HK are governed by the Employment Ordinance (Cap 57) and the express terms of the contract. Key requirements for HK offer letters:

- **Statutory particulars (Cap 57 s.42C):** Employers must provide a written statement of employment terms within 7 days of commencement, including: wages, wage period, end-of-year payment, statutory holiday entitlement, annual leave, sickness allowance, notice period, maternity/paternity leave entitlement, and MPF details.
- **Notice period:** Must be stated in the contract; statutory minimum is 7 days if no contractual period specified (Cap 57 s. 6).
- **Probation period:** Common in HK, typically 1-3 months. During probation, shorter notice periods may apply (often 7 days or contractual).
- **No at-will language needed.** HK law requires cause or notice for termination. Adding "at-will" is legally meaningless and potentially misleading.
- **Right-to-work verification:** Every employer in HK must verify that the employee has the legal right to work (HKID holder, or valid employment visa). Employing someone without a valid work permit is an offence under the Immigration Ordinance (Cap 115).
- **Salary and benefits:** State the wage, wage period, bonus structure (13th month / end-of-year payment per Cap 57 s. 41B), MPF contributions (employer standard 5% under Cap 485 s. 7A), and any contractual benefits.
- **Equity terms (if any):** Consistent with the equity plan.
- **Integration clause:** So the offer letter is the whole deal.

**Checklist for HK offer letters:**
- Statutory particulars (or reference that they will be provided within 7 days per Cap 57 s.42C)
- Notice period compliant with Cap 57 s.6 minimum
- Probation period terms clear
- Right-to-work status verified (HKID / visa)
- MPF obligations acknowledged
- Restrictive covenants (if any) — test for reasonableness
- Contingencies clear (background check, reference check)
- Start date, title, salary, reporting structure stated
- End-of-year payment / bonus terms (if discretionary, clearly state)

## Output

> **Jurisdiction assumption.** This review applies the Employment Ordinance (Cap 57) and related Hong Kong legislation. Employment protections, contractual requirements, and MPF obligations in HK are governed by specific statutory provisions. If the employee works outside HK or choice-of-law is contested, this analysis may not apply as written.

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]

## Hiring Review: [Candidate] — [Role] — Hong Kong SAR

**Overall:** [Clear to send | Changes needed | Escalate]

### Jurisdiction
Hong Kong SAR. Governed by Employment Ordinance (Cap 57) and related legislation.

### Employee vs Contractor
[Employee / Contractor classification under HK common law tests — control test, organisation test.]

### Restrictive covenants
[If any. Enforceability per HK common law — requires legitimate business interest, reasonableness in scope/duration/geography. Time-limited and geographically limited covenants are more likely enforceable than blanket restrictions. Flag any restraint of trade issues.]

### HK requirements
- Statutory particulars under Cap 57 s.42C (written statement of employment terms within 7 days)
- MPF enrolment obligations (Cap 485) — must enrol employee in registered scheme within 60 days
- Probation period terms and notice period compliance
- Right-to-work verification in HK (valid HKID / visa / work permit)
- Compliance with PDPO (Cap 486) for collection and processing of candidate personal data

### Offer letter
[Any issues with the letter itself — does it include or reference the statutory particulars per Cap 57 s.42C?]

### Action items
- [ ] [specific change needed before sending]
```

## Consequential-action gate (make an offer)

**Before producing a "Clear to send" recommendation or a final offer letter for signature:** Read `## Who's using this` in `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Making an offer has legal consequences — the letter is a contract, and restrictive covenants, classification, and jurisdiction-specific terms are difficult to reset once sent. Have you reviewed this offer with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> - Candidate, role, jurisdiction (HK SAR)
> - Employee/contractor classification analysis under HK common law
> - Restrictive covenants in the offer and enforceability analysis (legitimate business interest / reasonableness)
> - HK statutory requirements (Cap 57 s.42C particulars, MPF enrolment, right-to-work verification)
> - Open questions and what's unresolved
> - What could go wrong (unenforceable restrictive covenant, missing statutory particulars, MPF non-compliance, improper right-to-work procedures)
> - What to ask the attorney (is this employment or contractor; can we use this non-compete; are the statutory particulars complete)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

Do not produce a "Clear to send" output past this gate without an explicit yes. A marked-DRAFT flagged for attorney review is fine.

---

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- Draft the offer letter — reviews it.
- Make the hire decision — checks the paperwork.
- State restrictive-covenant or exemption rules from memory — every
  jurisdiction-specific call is based on researched, cited sources verified
  for currency.
- Research a new jurisdiction in depth on its own — flags that research is
  needed, and uses `wage-hour-qa` or outside counsel to fill in.
