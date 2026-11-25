---
name: intellectual-property-audit
description: "Audits IP assets with trademark, copyright, trade secret, and patent inventory and protection recommendations. Use when assessing and organizing your business IP portfolio."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Intellectual Property Audit

## When to Use This Skill

Use this skill when you need to:
- Inventory all intellectual property assets in your business
- Identify unprotected IP that needs registration or documentation
- Assess IP risks such as infringement exposure or gaps in protection
- Create an IP management plan with action items and timelines

**DO NOT** use this skill for filing applications (use trademark-application), drafting agreements, or legal disputes. This is for auditing and organizing your IP portfolio. Consult an IP attorney for legal strategy.

---

## Core Principle

YOUR IP IS OFTEN YOUR MOST VALUABLE BUSINESS ASSET — IF YOU DO NOT KNOW WHAT YOU OWN, YOU CANNOT PROTECT IT, LICENSE IT, OR LEVERAGE IT.

---

## Phase 1: Business Inventory

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business name** | "What is your legal business name?" | No default — must be provided |
| **Products/services** | "What do you sell or offer?" | No default — must be provided |
| **Brand assets** | "What brand names, logos, and slogans do you use?" | No default — list all |
| **Content created** | "What original content have you created? (courses, books, software, designs)" | No default — list all |
| **Processes/methods** | "Any proprietary processes, methods, or formulas?" | None |
| **Employee/contractor work** | "Have employees or contractors created IP for your business?" | Yes |

**GATE: Do not proceed without brand assets and content inventory.**

---

## Phase 2: IP Inventory

### Trademark Assets

```
## Trademark Inventory

| Asset | Type | Status | Registration # | Class | Renewal Date |
|-------|------|--------|----------------|-------|-------------|
| [Business name] | Word mark | [Registered/Pending/Unregistered] | [#] | [Class] | [Date] |
| [Logo] | Design mark | [Status] | [#] | [Class] | [Date] |
| [Product name] | Word mark | [Status] | [#] | [Class] | [Date] |
| [Slogan/tagline] | Word mark | [Status] | | | |
| [Domain names] | Domain | Active | N/A | N/A | [Renewal] |

### Trademark Gaps
- [ ] [Asset] — used in commerce but not registered
- [ ] [Asset] — potential conflict identified
```

### Copyright Assets

```
## Copyright Inventory

| Asset | Type | Created | Registered | Creator | Ownership |
|-------|------|---------|-----------|---------|-----------|
| [Course name] | Educational content | [Date] | [Yes/No] | [Creator] | [Company/Assigned] |
| [Website copy] | Literary work | [Date] | [No] | [Creator] | [Status] |
| [Software code] | Software | [Date] | [No] | [Creator] | [Status] |
| [Book/ebook] | Literary work | [Date] | [Yes/No] | [Creator] | [Status] |
| [Designs/graphics] | Visual art | [Date] | [No] | [Creator] | [Status] |

### Copyright Gaps
- [ ] [Asset] — created by contractor without IP assignment clause
- [ ] [Asset] — high-value work not registered with Copyright Office
```

### Trade Secrets

```
## Trade Secret Inventory

| Asset | Description | Protection in Place |
|-------|-------------|-------------------|
| [Client list] | [Customer database with contact and purchase history] | [NDA: Yes/No, Access restricted: Yes/No] |
| [Pricing formulas] | [Proprietary pricing methodology] | [NDA: Yes/No] |
| [Processes/methods] | [Unique business processes or methods] | [Documented: Yes/No] |
| [Supplier info] | [Vendor relationships and terms] | [NDA: Yes/No] |

### Trade Secret Gaps
- [ ] [Secret] — no NDA covering access
- [ ] [Secret] — accessible to departing employees without restriction
```

### Patent Assets (if applicable)

```
## Patent Inventory

| Asset | Type | Status | Application # | Expiration |
|-------|------|--------|---------------|-----------|
| [Invention] | [Utility/Design/Provisional] | [Granted/Pending/None] | [#] | [Date] |
```

---

## Phase 3: Risk Assessment

```
## IP Risk Assessment

### Protection Gaps (Action Required)
| Risk | Severity | Action Needed | Priority |
|------|----------|--------------|----------|
| [Brand name unregistered] | High | File trademark application | Immediate |
| [Contractor work without IP assignment] | High | Execute assignment agreements | Immediate |
| [No NDAs with team members] | Medium | Create and distribute NDAs | Within 30 days |
| [Key content unregistered] | Medium | Register copyright | Within 90 days |
| [Domain variations unsecured] | Low | Register key variations | Within 90 days |

### Infringement Risks
| Risk | Description | Action |
|------|-------------|--------|
| [Third-party using similar name] | [Details] | [Monitor / Cease and desist / Legal review] |
| [Content being copied] | [Details] | [DMCA takedown / Legal review] |

### Contractual IP Issues
| Issue | Description | Action |
|-------|-------------|--------|
| [Contractor with no IP clause] | [Past work may not be owned] | Execute retroactive assignment |
| [Employee with no invention assignment] | [Inventions may be disputed] | Add clause to employment agreement |
```

---

## Phase 4: IP Management Plan

```
## IP Action Plan

### Immediate (Next 30 Days)
1. [ ] [Action — e.g., file trademark for primary brand name]
2. [ ] [Action — e.g., execute IP assignment with key contractor]
3. [ ] [Action — e.g., implement NDA for all team members]

### Short-Term (30-90 Days)
1. [ ] [Action]
2. [ ] [Action]

### Ongoing
- [ ] Annual IP audit (schedule for [month])
- [ ] Trademark renewal tracking
- [ ] New content/product IP assessment before launch
- [ ] Contractor agreements include IP assignment clause
- [ ] Monitor for infringement [monthly / quarterly]
```

---

## Example: Online Course Business

**IP assets:** Business name (unregistered), 3 course titles, course content (12 modules), proprietary framework name, website copy, logo, 2 ebooks, email sequences, templates.

**Key findings:** Business name and framework name are not trademarked — competitors could use them. Course content created by a contractor without IP assignment clause — ownership is unclear. Ebooks are not copyright registered. No NDAs in place.

**Priority actions:** 1) File trademark for business name and framework name. 2) Execute IP assignment with contractor retroactively. 3) Register copyright on highest-value course. 4) Implement NDAs for all team access to client lists and methods.

---

## Anti-Patterns

- **Assuming you own what you paid for** — without a written IP assignment, the creator may own the work. This is especially true for contractors.
- **Only protecting trademarks** — IP includes copyrights, trade secrets, and potentially patents. Audit all categories.
- **Ignoring domain names** — your domain is a brand asset. Secure key variations (.com, .co, common misspellings).
- **No regular audit schedule** — IP grows as your business grows. Audit annually, not once.
- **Treating trade secrets casually** — a trade secret that is not actually kept secret loses its legal protection.

---

## Recovery

- **Contractor created key assets without IP clause:** Negotiate a retroactive assignment agreement. This may require additional compensation.
- **Discovered someone infringing your brand:** Document the infringement. Send a cease and desist. Consult an IP attorney if they do not comply.
- **Trademark name is already taken:** Assess the overlap (different class, different geography). Consult a trademark attorney for options.
- **No IP protections in place at all:** Start with the highest-value asset. For most solopreneurs, that is the brand name (trademark) and primary product content (copyright).
