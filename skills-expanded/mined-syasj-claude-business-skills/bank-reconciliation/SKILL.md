---
name: bank-reconciliation
description: "Reconcile book to bank and leave a list of items a human must clear, with no plugs. Use when the user mentions bank reconciliation, book to bank, unreconciled cash, bank rec, or asks for a bank reconciliation. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'bank-reconciliation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Bank Reconciliation

Reconcile book to bank and leave a list of items a human must clear, with no plugs.

## When to use this skill

Use this skill when the user:

- bank reconciliation
- book to bank
- unreconciled cash
- bank rec

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Statement ending balance and date
- Book balance for the same account
- Outstanding checks and deposits
- Items the user cannot explain

## Workflow


### 1. Match the account and the date

A reconciliation of the wrong account or the wrong day is not a near miss. Stop and correct the frame.
### 2. Compute the difference

Statement balance to book balance, then list outstanding items the user supplied. Show the remaining unexplained amount in the open.
### 3. Classify leftovers

Timing, error, or unknown. Unknown is acceptable. A forced explanation is not.
### 4. Look for duplicates and old items

Outstanding items older than the user's threshold need a decision, not another month of carry-forward.
### 5. Propose entries only as drafts

The accountant posts. You do not declare the books updated.
### 6. No credentials

Do not ask for online banking passwords or one-time codes. Work from exports the user chooses to share.

## Output

Deliver a **bank reconciliation**.

- Purpose of this bank reconciliation, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Priya Shah, controller at Northline Studio in Calgary, is closing August 2026. The operating account will not tie, and three deposits in transit are older than a month.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Period: August 2026 · Account: operating (CAD)

Bank statement ending balance, 31 Aug 2026 ....... 97,820.00
GL cash balance, 31 Aug 2026 .................... 94,350.00

Outstanding checks (per GL, not yet cleared):
  #2241  Office Depot     28 Aug 2026     3,250.00
  #2242  Redline Parts    29 Aug 2026     1,820.00

Deposits in transit (per GL, not on statement):
  DIT-01  deposited 21 Jul 2026  (41 days)   6,200.00
  DIT-02  deposited  4 Aug 2026  (27 days)   3,100.00
  DIT-03  deposited  9 Aug 2026  (22 days)   2,400.00

On statement, not in GL:  NSF fee 85.00 · service charge 65.00
Stale-item threshold (their policy): 30 days
Reviewer sign-off: not signed
```

### Example outcome

**Bank reconciliation — operating account, August 2026**
To: Priya Shah, controller, Northline Studio · Date: 14 September 2026

**Adjusted bank balance**

| Line | Amount (CAD) |
| --- | ---: |
| Statement balance, 31 Aug 2026 | 97,820.00 |
| Less: outstanding checks (#2241, #2242) | (5,070.00) |
| Add: deposits in transit (DIT-01/02/03) | 11,700.00 |
| **Adjusted bank balance** | **104,450.00** |

**Adjusted book balance**

| Line | Amount (CAD) |
| --- | ---: |
| GL balance, 31 Aug 2026 | 94,350.00 |
| Less: bank charges not yet booked (85.00 + 65.00) | (150.00) |
| **Adjusted book balance** | **94,200.00** |

**Unexplained difference: 10,250.00. This reconciliation does not close.**

The difference is shown, not plugged. No "other" line was created to force a zero.

**Items that need a decision**

| Item | Amount | Age | Why it is here |
| --- | ---: | ---: | --- |
| DIT-01 | 6,200.00 | 41 days | Past their 30-day threshold. Trace to the bank's deposit record. If the deposit never landed, reverse the GL entry and find the source funds. |
| DIT-02 | 3,100.00 | 27 days | Approaching the threshold. Confirm receipt with the bank this period. |
| DIT-03 | 2,400.00 | 22 days | Within tolerance. Carry, and watch next period. |

**Draft journal entry — for the controller to post, not posted here**

```
Dr  Bank service charges expense      150.00
      Cr  Cash — operating                      150.00
(NSF 85.00 + monthly service charge 65.00; confirm the NSF payee before posting)
```

**Deliberately not done**
- No plug labelled "other" to force the reconciliation to zero.
- No bank password or one-time code requested. Everything above came from the export Priya shared.
- No DIT written off silently; the 41-day item is raised as a decision, not carried forward again.

**Open items before sign-off**
- Investigate the 10,250.00 difference. The account does not close until it is explained or classified as a known error.
- Reviewer signature is missing. Close is not complete without it.
- Recs are stored in one person's inbox rather than the shared folder. Move them this period.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A plug labeled 'other' to force a zero.
- Asking for a bank password.
- Carrying year-old outstanding items with no comment.

## Related skills

- `month-end-close`
- `treasury-policy-brief`
- `internal-controls-walkthrough`
