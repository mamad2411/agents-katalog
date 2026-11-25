---
name: termination-review
description: >
  Termination review — high-risk flag detection, severance + release, and
  final pay timing by jurisdiction. Jurisdiction-specific rules and release
  consideration periods are researched per review, not stored. Use when the
  user says "reviewing a termination", "can we fire this person", "term
  review", or describes a termination scenario.
argument-hint: "[describe the termination, or attach documentation]"
---

# /termination-review

1. Load `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → termination review triggers, high-risk flags, severance practice, jurisdiction rules.
2. Use the workflow below.
3. Walk the checklist. Check every high-risk flag.
4. Final pay timing per employee's jurisdiction. Severance + release if applicable.
5. If any high-risk flag fires: escalate per table, don't proceed without sign-off.

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-hk-law/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

Most terminations are fine. A few are lawsuits waiting to happen. This skill
runs the checklist that catches the second kind before the decision is final.
The skill does not state the law — every jurisdiction-specific rule and
release-period requirement is researched and cited at the time of review.

## Load context

`~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → termination review triggers, high-risk flags, standard severance,
jurisdiction table.

## Output header

Prepend the work-product header from `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → `## Outputs` (it differs by user role — see `## Who's using this`). Match the memo format from seed term memos referenced in that config where one exists. The work-product header is always first.

## Workflow

### Step 1: The basic facts

- Employee name (or role if staying abstract)
- Jurisdiction (where they work)
- Reason for termination (performance, misconduct, RIF, position elimination)
- How long employed
- Length of continuous employment (critical for notice period, severance, and long service payment under Cap 57)
- Monthly wages and average wages (for calculating statutory entitlements)
- Whether any other employees are being terminated as part of a redundancy exercise (triggers Part VA of Cap 57)
- When is the planned term date

### Step 2: High-risk flag scan (HK Employment Ordinance)

This is the most important step. Check every flag from `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md`. HK-default
set:

| Flag | Why it's high-risk | Check |
|---|---|---|
| **Recent complaint** | Retaliation / victimisation claim | Has this employee filed any complaint (HR, EOC, Labour Department, trade union) recently? |
| **Protected leave / sickness absence** | Unlawful dismissal under Cap 57 s.15 | Currently on or recently returned from statutory maternity leave, paternity leave, or paid sickness days? |
| **Pregnancy** | Absolute prohibition on dismissal | Is the employee pregnant? Dismissal during pregnancy is a criminal offence under Cap 57 s.15 — triple damages payable |
| **Discrimination / harassment complaint** | Cap 480 / 487 / 527 / 602 | Has the employee raised discrimination or sexual harassment concerns? |
| **Trade union activity** | Anti-union dismissal | Is the employee a trade union member or organiser? Dismissal for trade union membership/activity is unlawful |
| **Whistleblower** | Protected disclosures | Has this employee raised concerns about illegality, safety, fraud? |
| **Employees' Compensation pending** | Cap 282 | Is there an active work injury claim? Dismissal while compensation pending is high-risk |
| **Thin documentation** | "Why now?" problem | For performance terms: is there a written warning process, documented feedback? Or did this come out of nowhere? |
| **Comparator problem** | Disparate treatment discrimination | Is someone else doing the same thing and not being terminated? |
| **Contract/handbook promise** | Breach of contract | Does the employment contract or handbook promise a process that isn't being followed? |

**Wrongful dismissal flag (Cap 57 ss. 32A–32P).** An employee with not less than 2 years of continuous employment is protected against unreasonable and unfair dismissal. The employee can claim reinstatement or terminal payment. This applies even if proper notice was given. Fire this flag when the termination reason might be contested as unreasonable.

**Summary dismissal flag (Cap 57 s. 9).** Summary dismissal without notice is only permitted for gross misconduct. If the employer relies on summary dismissal and the conduct doesn't meet the high threshold, the dismissal is unlawful and the employee is entitled to damages in lieu of notice.

**Any flag fires → escalate per `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` before the term proceeds.** Not
after. Before.

### Step 3: HK-specific requirements

> **Research the applicable rules under the Employment Ordinance (Cap 57) before
> finalizing the plan.** Specifically:
>
> - Notice period — determine the contractual and statutory minimum notice period under Cap 57 s. 6. Note whether the contract provides for payment in lieu of notice or summary dismissal provisions.
> - Wage timing — wages due on termination must be paid as soon as practicable, and in any case within 7 days (Cap 57 s. 25). Late payment attracts interest.
> - Holiday pay and annual leave pay — whether accrued but untaken statutory holidays and annual leave must be paid out on termination.
> - Long Service Payment (LSP) — under Cap 57 Part VB, an employee with 5+ years continuous employment who is dismissed (other than for summary dismissal or redundancy) may be entitled to LSP.
> - Severance payment — under Cap 57 Part VA, an employee with 2+ years continuous employment who is laid off or dismissed by reason of redundancy is entitled to severance payment.
> - Required notices — Cap 57 s. 42C requires employers to provide a written statement of statutory particulars; ensure the statement reflects the termination terms.
>
> Cite primary sources. Verify currency.
>
> **No silent supplement.** If a research query returns few or no results for the relevant Cap 57 provision, report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking.
>
> **Source attribution.** Tag every citation — notice period rule, holiday pay rule, LSP/severance calculation, Cap 57 section — with where it came from.

### Step 4: Severance, LSP, and release

Per `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → standard severance:

- Is the employee entitled to statutory severance payment (Cap 57 Part VA) or Long Service Payment (Cap 57 Part VB)? Note that severance and LSP are mutually exclusive — the employee receives the higher.
- Is a contractual ex gratia payment being offered beyond the statutory minimum?
- Release required? (Usually yes if paying ex gratia severance — that's the consideration.)

> **HK does not have a direct equivalent of OWBPA.** There is no federal-age-discrimination-specific release framework. However, general contract law governs releases — ensure any release is supported by fresh consideration beyond what the employee is already legally entitled to.

Separately, consider whether:
- The settlement agreement contains non-disclosure/non-disparagement clauses compatible with the Equal Opportunities Commission's guidance on discrimination-related settlement terms.
- The employee is waiving statutory rights (some rights under Cap 57 cannot be contracted out of; Cap 57 s. 70).
- Independent legal advice is advisable (it strengthens the enforceability of the release).

### Step 5: Documentation check

For performance terminations especially:

- Is there a paper trail? Written warnings, PIP, feedback docs?
- Does the paper trail tell a consistent story?
- Is there anything in writing that contradicts the reason (recent positive
  review, bonus, promotion)?

The "why now" question: if this person has been underperforming for a year,
what changed? The answer should be documented.

## Output

> **Research-connector pre-flight.** Before emitting the memo, check whether a legal research connector is reachable for this session — Westlaw, CourtListener, or any firm-configured research MCP. Collect this into the reviewer note per CLAUDE.md `## Outputs`: if no connector returns results in Step 3 (or none is configured at run time), record it in the **Sources:** line of the reviewer note — e.g., `not connected — cites from training knowledge; the highest-fabrication topics in termination-law memos are final-pay timing, OWBPA group/individual distinctions, state-specific NDA / non-disparagement rules (e.g., CA SB 331), and NLRB positions (e.g., McLaren Macomb) — spot-check those first`. Per-citation `[model knowledge — verify]` tags remain inline. Do not emit a standalone banner above the memo.

> **Jurisdiction assumption.** This review applies the Employment Ordinance (Cap 57) and related Hong Kong legislation as stated in Step 1. Employment rules under Cap 57 apply to all employees in Hong Kong SAR. If the employee works under a different employment regime or choice-of-law is contested, this analysis may not apply as written.

Match the memo format from seed term memos referenced in `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md`. If none:

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]

## Termination Review: [Employee] — [Date]

**Jurisdiction:** Hong Kong SAR
**Legislation:** Employment Ordinance (Cap 57), [other applicable ordinances]
**Reason:** [Performance / Misconduct / Redundancy / Mutual agreement / Summary dismissal]
**Planned date:** [Date]
**Length of continuous employment:** [years/months]

---

### Bottom line

[Can you proceed / Need to fix X first / Stop — one-sentence why]

---

### High-risk flags

[Every flag from Step 2. ✅ Clear or 🔴 FLAG with detail.]

**Escalation:** [None needed | Escalate to [name] before proceeding — [which flag]]

---

### HK requirements (Cap 57)

- Notice period: [contractual minimum + statutory minimum under Cap 57 s.6]
- Wage payment on termination: [within 7 days / as soon as practicable per Cap 57 s.25]
- Holiday pay / annual leave pay: [accrued entitlements to be paid out]
- Long Service Payment / Severance Payment: [applicable / not applicable — cite Part VA/VB]
- Employees' Compensation implications: [if any]

---

### Severance and release

- Statutory severance/LSP: [amount per formula / none]
- Ex gratia payment: [if offered]
- Release: [required / not — if required, confirm fresh consideration; recommend independent legal advice]
- [Non-disclosure/non-disparagement clause check]

---

### Documentation

[Assessment of paper trail. Gaps flagged.]

---

### Go / No-go

[Clear to proceed | Proceed with changes below | Hold — escalation pending]

### Checklist for termination day

- [ ] Final wages paid within 7 days (Cap 57 s.25)
- [ ] Accrued holiday pay / annual leave pay calculated and paid
- [ ] Severance payment / LSP calculated (if applicable)
- [ ] MPF accrued benefits — ensure employer contributions are properly dealt with (Cap 485)
- [ ] Letter of employment / reference letter prepared
- [ ] Settlement agreement (if applicable) with independent legal advice recommended
- [ ] Return of company property / access revocation coordinated
- [ ] PDPO data privacy obligations — handling of employee personal data after termination
```

## Consequential-action gate (terminate an employee)

**Before producing a "Go" recommendation or a term-day checklist marked ready:** Read `## Who's using this` in `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Terminating an employee has legal consequences — wrongful-termination, discrimination, retaliation, and wage-law claims all trace back to how this decision is structured. Have you reviewed this termination with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> - Employee, jurisdiction, reason, planned date
> - Every high-risk flag the review surfaced (recent complaint, protected leave, protected class + timing, whistleblower, thin documentation, comparator, contract/handbook promise) — with detail
> - Jurisdiction-specific findings (final pay, PTO, required notices, mass-layoff rules) and where they were cited from
> - Severance/release analysis, including any OWBPA/older-worker-protection angles
> - Open questions and what's unresolved
> - What could go wrong (the claim theory this fact pattern supports)
> - What to ask the attorney (is this a clean term; do we need more documentation first; does the release need specific language; do we need to stagger decisional units)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service. Employment is one of the practice areas where a short consult before the termination meeting consistently outvalues a post-termination claim defense.

Do not produce a "Clear to proceed" output past this gate without an explicit yes. A marked-DRAFT flagged for attorney review is fine.

---

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- Make the termination decision. It checks the decision.
- Have the conversation. The manager does that.
- State release or jurisdiction rules from memory — every rule is researched
  and cited at the time of review.
- Guarantee no lawsuit. It reduces the risk by catching the obvious problems.
