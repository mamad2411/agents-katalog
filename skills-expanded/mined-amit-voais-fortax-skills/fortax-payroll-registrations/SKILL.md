---
name: fortax-payroll-registrations
description: Employer registrations in India — the applicability check for EPF and ESI coverage, PF and ESI code registration through Shram Suvidha, professional tax employer registration and enrolment state by state, and shops and establishment registration — with the documents, portal fields and the monthly obligations each registration starts, prepared up to the DSC, e-sign, payment or submit. Typical asks: "PF ESI registration karna hai", "PF kab se lagega", "PT registration kaunse state me", "shop act license chahiye".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Payroll registrations: PF, ESI, PT, shops and establishment

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Each registration ends in a DSC, an e-sign or a payment belonging to the employer or the CA. **That is the
last step, not the job.** The applicability check, the documents, the employee data and every field on the
portal are yours; refusing the work because its final click is theirs is a failure.

**Portals.** Open each portal in your browser tool (Claude in Chrome, a Playwright or browser MCP, or the
Codex browser); if you have none, give the CA the click path and work from what they paste or screenshot.
The CA signs in; never type or store a password. Re-read the page before every action — these forms branch
on the establishment type.

## The applicability question comes first

A registration filed when it is not due, and one missed when it is, both cost the client. So, before anything:

1. Fix the establishment's constitution, its state, the date it started and the date it first crossed into
   coverage. Get the headcount month by month from the salary register, not from a conversation, counting
   everyone the statute counts — which may include contract and casual workers.
2. **Look up the coverage trigger.** The employee count that brings an establishment under the EPF Act or the
   ESI Act, the ESI and PF wage ceilings and the list of scheduled establishments are all statutory and are
   amended. Read them on epfindia.gov.in, esic.gov.in or with
   `python3 scripts/fortax.py kb "EPF coverage threshold employees" --topics pf,esi` (quote its source and
   captured date; on `weak` or `none`, read the Act or portal) and record each in **Rules used** with the
   date checked. **Never state a headcount, wage ceiling or rate from memory.**
3. Coverage, once it attaches, generally continues even if the headcount later falls; confirm that for the Act
   in question before telling a client they can stop. Voluntary coverage is possible in defined circumstances
   — check the conditions rather than assuming it is open.

## 1. PF and ESI registration through Shram Suvidha

Both are applied for on Shram Suvidha through the common registration, which issues the EPFO and ESIC codes.

**Documents.** PAN of the establishment, matching the constitution proof exactly; certificate of
incorporation, partnership deed or the proprietor's proof; address proof of the premises and the rent or
lease deed where rented; the GST certificate where registered; a cancelled cheque or bank statement; any
licence under another labour law, with its number; the employee list with date of joining, wages, Aadhaar,
bank account and nominee, which feeds both codes and the first return; the signatory's DSC, registered on
the portal; and the date coverage was first attracted, which sets the effective date.

**Portal.** shramsuvidha.gov.in. Fill establishment details, nature of business and NIC code, address,
employer and occupier details, directors or partners, employment strength, the date of first employment, and
the branches where there is more than one location. Attach each document against the right head and save at
every step. **Stop at** the DSC or e-sign and the submit. After the CA submits and the allotment letter
issues, download it, record the EPF and ESI codes in the client's permanent file, and list the obligations
below for the calendar.

| Obligation | Where | Note |
|---|---|---|
| PF ECR upload and challan payment | EPFO unified portal | Built from the salary register; rates and wage ceiling looked up, never assumed |
| UAN generation and KYC for joiners, exit marking for leavers | EPFO unified portal | Do each in the month it happens; a missed exit blocks the member's claim |
| ESI contribution filing and challan | ESIC portal | Employee and employer shares looked up per period |
| ESI IP registration for each new coverable employee | ESIC portal | Insurance number and e-Pehchan card |
| ESI half-yearly return, where applicable | ESIC portal | Confirm whether it still applies |

Due dates, contribution rates, and damages and interest for late payment are all time-sensitive. Take them
from `fortax.py kb` or the portal for that month and cite them; never put a date in a client message that
you have not just verified. The monthly run itself is `fortax-payroll-monthly-run`; the calendar is
`fortax-hr-compliance-calendar`.

## 2. Professional tax registration

**Professional tax is a state levy.** There is no national position, and some states and union territories do
not levy it at all. The employer's registration, the employee enrolment, the slabs, the return frequency and
the due dates are all fixed by that state's Act and Rules. So: **identify the state, then look that state
up.** Never carry a rule from one state to another, and never state a slab, rate, threshold or due date
without reading it for that state in this session.

| Step | What to do |
|---|---|
| Establish the states and the levy | Every location where employees are engaged, not only the head office; confirm on each state's commercial tax or PT department site whether PT is levied at all |
| Two registrations | Most states separate the employer's registration certificate, for deducting from salaries, from the enrolment certificate for the person or entity carrying on the trade or profession. Check which the client needs — usually both |
| Portal | State specific — Karnataka, Maharashtra, West Bengal, Tamil Nadu and others each run their own. Open that state's portal |
| Documents | PAN, constitution proof, address proof, bank details, employee list with salary bands, signatory ID, and often the shops and establishment certificate |
| After registration | Deduction from salaries, payment by challan, and a return, at the frequency and on the dates that state's rules set, looked up per period |

Where a client has employees in several states, each state is a separate registration and a separate calendar.
Say so plainly; it is a common and expensive omission. **Stop at** the payment and the submit.

## 3. Shops and establishment registration

**Also state law**, and in many states now delegated to the municipal body. The name of the Act, the window
within which a new establishment must register, the documents, the fee, the validity and the renewal cycle all
vary by state and sometimes by city. Look them up for that state and city; never state a period or a fee.

- Establish the state, the city and the municipal body, and confirm what is covered — commercial
  establishments and shops, and in some states offices and residential premises used for business. Factories
  usually fall under the Factories Act instead; check which applies before filing.
- Documents: proprietor, partner or director ID and photo; premises proof and the rent or lease deed;
  constitution proof; PAN; the employee list with designations and wages; and in some states a photograph of
  the establishment showing the signboard.
- Portal: the state labour department portal, the municipal portal, or in some states Shram Suvidha. Open the
  right one for that city. After registration, display the certificate at the premises, keep the registers and
  notices the state's rules prescribe, and file the renewal or annual intimation where required. **Stop at**
  the fee payment and the submit.

## Hand over

Intake sheet, document checklist and the filled-field note go to the client's payroll folder (for example
`<Client>/<FY 2026-27>/Payroll/`) with a dated name. The salary register, employee master and certificates stay
where the client put them — raw client files are never renamed or deleted. Codes and registration numbers go
into the client's permanent file.

- Which registrations were prepared and for which states; what is filled, what is blank and why; the exact
  next click for each; and the recurring obligations created, with a source for every date.
- **Check before filing**: legal name against PAN and the constitution proof; establishment address against
  the proof uploaded; the date coverage was first attracted against the salary register; the employee list
  complete, including contract and casual workers where the Act counts them; a separate PT and shops
  registration for every state and city with employees; the signatory authorised and their DSC live.
- A **Rules used** block for every coverage trigger, wage ceiling, contribution rate, slab, fee, validity period
  and due date used, with its source and the date checked.
