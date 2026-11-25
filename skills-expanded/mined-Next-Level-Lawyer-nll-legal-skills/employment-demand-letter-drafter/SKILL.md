---
name: employment-demand-letter-drafter
description: Draft an employment law demand letter (wrongful termination, discrimination, wage claim) from case facts and supporting documentation. Use whenever the user wants a demand letter drafted or outlined for an employment claim, provides employment records/facts and wants them turned into a demand package, or wants an existing employment demand letter revised.
---

# Employment Demand Letter Drafter

Turns employment claim facts and documentation into a structured demand letter draft, tailored to the specific claim type (wrongful termination, discrimination/harassment, wage and hour).

## Workflow

1. **Gather inputs**: claim type, employment history (dates, position, performance history), the adverse action and its timing relative to any protected activity, comparator evidence if discrimination-based, and damages information (lost wages, benefits, emotional distress narrative, mitigation efforts).
2. **Structure the letter** by claim type:
   - Wrongful termination/retaliation: employment history → protected activity → adverse action and temporal proximity → pretext evidence (if employer's stated reason is disputed)
   - Discrimination/harassment: employment history → protected class basis → specific incidents/pattern → comparator evidence → employer's response (or lack thereof) if reported
   - Wage and hour: employment classification and pay structure → specific violation (unpaid overtime, misclassification, break violations) → calculation basis for amount owed
3. **Draft in a firm, professional tone** — factual and confident, not inflammatory. Don't invent specific dollar figures the user hasn't provided; use placeholders.
4. **Note administrative prerequisites** if applicable (e.g., "this letter does not substitute for a required EEOC/state agency charge, which should be filed within the applicable deadline") so the letter isn't mistaken for satisfying a required filing.
5. **Flag weak points** as attorney notes, not folded into the draft itself.

## Output format

```
[Firm letterhead placeholder]

Re: [Claimant] v. [Employer]

Dear [Counsel/HR contact],

[Employment history / background paragraph]

[Claim-specific narrative paragraph(s) — protected activity/class, adverse action, evidence]

[Damages summary — itemized where figures are provided, placeholders otherwise]

[Demand statement and response deadline]

Sincerely,
[Attorney name placeholder]
```

**Attorney notes (not part of letter):** [weak points, missing administrative charge status, documentation gaps]

## Document Output Format

Use the `docx` skill to produce a proper business letter, not a markdown block:

- **Letterhead block:** firm name/address/phone placeholder at the top, standard business letter convention.
- **Date, recipient block, Re: line:** claimant v. employer, formatted as standard legal correspondence.
- **Body:** professional serif font (Times New Roman or Garamond, 12pt), 1" margins, single-spaced with blank lines between paragraphs.
- **Damages summary:** real Word table where figures are provided, clean placeholders where not.
- **Administrative-prerequisite note** (e.g., EEOC charge language), if included, formatted as a clearly set-apart paragraph, not buried mid-letter.
- **Signature block:** attorney name and firm placeholder.
- Keep "Attorney notes" out of the letter file itself — deliver separately.

## Notes

- Never state or imply this letter satisfies an EEOC/state agency charge requirement — flag that separately if the claim type requires one.
- Never fabricate a specific damages calculation — use placeholders unless the user provides the actual wage/hours data to calculate from.
