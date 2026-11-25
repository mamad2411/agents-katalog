---
name: non-compete-agreement
description: "Creates non-compete agreements with reasonable scope, duration, geographic limits, and enforceability notes. Use when protecting business interests from competition."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Non-Compete Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft a non-compete agreement for employees, contractors, or partners
- Define reasonable scope, duration, and geographic restrictions
- Understand enforceability considerations by state
- Create non-solicitation and non-disclosure provisions alongside a non-compete

**DO NOT** use this skill without subsequent attorney review. Non-compete enforceability varies significantly by state and jurisdiction. This is a drafting tool, not legal advice.

---

## Core Principle

A NON-COMPETE IS ONLY AS STRONG AS ITS REASONABLENESS — OVERLY BROAD RESTRICTIONS ARE UNENFORCEABLE AND DAMAGE YOUR RELATIONSHIP WITH THE SIGNER.

---

## Phase 1: Agreement Context

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Your business** | "What is your business name and industry?" | No default — must be provided |
| **Signer's role** | "Who is signing this? (employee, contractor, partner, seller of a business)" | Employee |
| **Competitive activity** | "What activities do you want to restrict?" | No default — must be provided |
| **Geographic scope** | "Where should the restriction apply? (state, region, nationwide)" | State-level |
| **Duration** | "How long should the restriction last after departure?" | 12 months |
| **State** | "Which state's law governs this agreement?" | No default — critical for enforceability |

**GATE: Do not proceed without the signer's role, competitive activity, and governing state.**

---

## Phase 2: Agreement Structure

```
## Non-Compete Agreement

**This Non-Compete Agreement** is entered into as of [Date] between:

**Company:** [Business Legal Name] ("Company")
**[Employee/Contractor/Partner]:** [Name] ("Restricted Party")

### 1. Recitals

WHEREAS, the Restricted Party [is employed by / provides services to /
is a partner in] the Company and has access to confidential information,
trade secrets, and client relationships;

WHEREAS, the Company has a legitimate business interest in protecting
its [confidential information / customer relationships / goodwill /
specialized training provided];

NOW THEREFORE, in consideration of [continued employment / compensation
of $X / the opportunity to participate in the business / the purchase
price of the business], the parties agree as follows:

### 2. Non-Compete Covenant

During the Restricted Period and within the Restricted Territory, the
Restricted Party shall not, directly or indirectly:

a) Engage in, own, manage, operate, or control any business that
   competes with the Company's [specific business activities]
b) Serve as an employee, contractor, officer, director, or advisor
   to any competing business
c) Invest in any competing business (except passive investments of
   less than 5% in publicly traded companies)

**Competing business** means any business that [specific definition
of competitive activity — be narrow and specific].

### 3. Restricted Period

The restrictions in Section 2 apply during the Restricted Party's
engagement with the Company and for [12/18/24] months following the
termination of the relationship, regardless of the reason for
termination.

### 4. Restricted Territory

The restrictions apply within [specific geographic scope]:
- [Option A: specific states or metro areas]
- [Option B: within X miles of any Company office or client location]
- [Option C: nationwide — use only if justifiable]

### 5. Non-Solicitation

For [12/24] months following termination, the Restricted Party shall not:

a) Solicit, contact, or attempt to do business with any client or
   customer of the Company with whom the Restricted Party had contact
   during the last [12/24] months of engagement
b) Recruit, solicit, or encourage any employee or contractor of the
   Company to leave the Company

### 6. Non-Disclosure

The Restricted Party shall not disclose or use any Confidential
Information of the Company during or after the engagement. Confidential
Information includes [customer lists, pricing, strategies, trade
secrets, proprietary processes, financial information].

### 7. Consideration

In exchange for the Restricted Party's obligations under this
Agreement, the Company provides the following consideration:
[Employment / continued employment / $X lump sum / $X monthly during
restriction period / access to trade secrets and specialized training /
proceeds from business sale]

### 8. Remedies

The Restricted Party acknowledges that a breach would cause irreparable
harm. The Company shall be entitled to injunctive relief in addition to
any other legal remedies, including recovery of attorney fees.

### 9. Severability

If any provision is found unenforceable, the court may modify it to
the minimum extent necessary to make it enforceable rather than
voiding the entire agreement.

### 10. Governing Law

This Agreement is governed by the laws of [State].
```

---

## Phase 3: Enforceability Review

```
## Enforceability Considerations

### State-Specific Notes
[Provide general guidance for the governing state — examples:]

**Generally Enforceable States:** Most states enforce reasonable
non-competes (FL, TX, GA, NC, OH, PA, and most others).

**Restrictive States:**
- **California:** Non-competes are generally unenforceable for employees
  (Cal. Bus. & Prof. Code 16600). Use NDAs and non-solicitation instead.
- **Colorado:** Enforceable only for executives/management earning above
  threshold, or for sale of business.
- **Minnesota, Oklahoma, North Dakota:** Significant restrictions or
  bans on employee non-competes.
- **Washington:** Enforceable only above income thresholds.

### Reasonableness Factors Courts Examine
| Factor | Reasonable | Likely Unreasonable |
|--------|-----------|-------------------|
| Duration | 6-12 months | 3+ years |
| Geography | Metro area or state | Nationwide (without justification) |
| Scope | Specific competing activities | "any business" |
| Consideration | New employment, promotion, or payment | Nothing (signing existing employee with no new benefit) |

### Red Flags That Weaken Enforceability
- No consideration (signing an existing employee without new benefit)
- Overly broad scope (restricting all work, not just competing work)
- Excessive duration (varies by state, but over 2 years is suspect)
- No legitimate business interest (protecting goodwill, trade secrets, or client relationships)
```

---

## Phase 4: Finalize

```
## Agreement Checklist

- [ ] Competitive activity is narrowly and specifically defined
- [ ] Duration is reasonable for the industry and state
- [ ] Geographic scope is limited to where you actually do business
- [ ] Adequate consideration is provided (not just continued at-will employment)
- [ ] Non-solicitation clause included (often more enforceable than non-compete)
- [ ] Non-disclosure clause included
- [ ] Severability clause allows judicial modification
- [ ] Governing state's enforceability rules reviewed
- [ ] Agreement reviewed by an attorney in the governing state
- [ ] Both parties have signed with dates
```

---

## Example: Marketing Agency Employee

**Scope:** Cannot work for or start a competing marketing agency serving the healthcare industry. **Duration:** 12 months. **Geography:** Within the state of Texas. **Non-solicitation:** Cannot solicit agency clients for 18 months. **Consideration:** Employment + access to proprietary client strategies and processes.

---

## Anti-Patterns

- **Overly broad scope** — "cannot work in any capacity for any competitor" is unenforceable in most states. Narrow to specific activities and industries.
- **No consideration for existing employees** — signing an existing employee without a raise, promotion, or bonus often voids the agreement
- **Ignoring state law** — California non-competes are void for employees. Know your state's rules.
- **Using a template from another state** — enforceability is jurisdiction-specific. A Texas-valid non-compete may be void in Colorado.
- **Relying solely on the non-compete** — non-solicitation and NDA clauses are often more enforceable and more practical. Layer all three.

---

## Recovery

- **Operating in California or another ban state:** Replace the non-compete with a strong NDA and non-solicitation agreement. These are generally enforceable everywhere.
- **Non-compete already signed without consideration:** May be unenforceable. Consult an attorney before relying on it.
- **Former employee violating the agreement:** Document the violation, send a cease and desist, and consult an attorney about injunctive relief.
- **Candidate refuses to sign:** Consider whether the role truly requires a non-compete. Non-solicitation and NDA may be sufficient and less objectionable.
