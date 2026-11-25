---
name: invoice-chaser
description: |
  Chase overdue invoices on a fixed escalation ladder that gets paid without damaging the relationship. Use when invoices are overdue, when someone dreads chasing payment, or when they want a repeatable collections routine.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, small_business_operations, small_business_ops]
metadata:
  title: "Invoice Chaser"
  category: "small-business-ops"
  tags: "agency_delivery, small_business_operations, small_business_ops"
  keywords: "small business, chase overdue invoices, this client has not paid, collections routine, payment reminder, how do i ask for payment"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Invoice Chaser

## What this does

Late payment is usually a process failure at the payer, not a refusal, and it is fixed by reaching the right person with the right document rather than by escalating tone. This skill sets a dated ladder, writes each message so it is easy to act on, and only shifts tone at the point where the ladder has run out.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- chase overdue invoices
- this client has not paid
- collections routine
- payment reminder
- how do I ask for payment

## Inputs

- **invoices**: amount, issue date, due date, and days overdue
- **contacts**: who signed, who approves, and who actually pays
- **terms**: the agreed payment terms and any late fee clause

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Check your own side first. A missing purchase order number, a wrong entity name, or an invoice sent to the wrong address is the cause more often than unwillingness, and chasing before checking is embarrassing.
2. Identify the payer, who is usually not your contact. Most chasing fails because it goes to the person who agreed to the work rather than the person who processes payment.
3. Set the ladder by date, not by feeling: a light reminder before due, a factual note just after, a direct request with the invoice reattached, then a call, then a formal notice.
4. Attach the invoice to every message. Asking someone to find it is asking them to do work, and that is where the reply stops.
5. Keep every message short and answerable. The reply you want is a date, so ask for a date.
6. Escalate the person before escalating the tone. Going up the chain politely works better than going harder at the same person.
7. Record what worked. The step that produces payment for a given client is stable, and knowing it removes the earlier steps next time.
8. Approval stop. Before sending any reminder to a customer, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before sending any reminder to a customer. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The ladder with dates, the message per step, the payer identification, the pre check result, and the record of which step landed.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Your own invoicing details are checked before the first chase
- The payer is identified separately from the contact
- The invoice is attached at every step
- Escalation moves up the chain before it changes tone
- Every message asks for a date

## Optional: run it on live data

This skill works with no tool. To add live data, run Company Contact Details Extractor (https://apify.com/mambalabs/company-contact-details-extractor?fpr=mamba) on your own Apify
account to find the accounts payable contact on the customer's website.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `cash-runway-snapshot`
- `month-end-narrative`
- `client-onboarding-brief`

Ships in the **small-business-operations**, **agency-delivery** packs.
