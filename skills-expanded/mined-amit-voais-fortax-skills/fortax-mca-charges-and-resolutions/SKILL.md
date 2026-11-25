---
name: fortax-mca-charges-and-resolutions
description: Register, modify or satisfy a company charge on MCA (CHG-1, CHG-9, CHG-4, condonation in CHG-8) and file resolutions in MGT-14 — deciding which resolutions actually need filing, reading the security documents, and drafting the notice, agenda, resolution and minutes behind them — prepared up to the DSC and payment. Typical asks: "bank loan ka charge create karna hai", "loan close ho gaya, charge satisfy karo", "MGT-14 file karna padega kya", "special resolution draft karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Charges and resolutions

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the DSC

Both families of form end in a DSC and a payment that belong to the CA or a director. **Refusing the
job because of that last click is a failure.** Yours is the rest: establishing what the company
actually resolved, drafting the notice, agenda, resolution and minutes, reading the charge documents,
filling every field, assembling the attachments. Say where you will stop, then start.

**Looking rules up.** Notice periods, minute-book deadlines, filing periods, extended periods and
fees are never stated from memory. Run
`python3 scripts/fortax.py kb "CHG-1 time limit creation of charge" --topics mca` and quote its source
and captured date; where the reply is `weak` or `none`, read the Companies Act, 2013, the Companies
(Registration of Charges) Rules, 2014, Secretarial Standards or the MCA portal and mark it "confirm on
the portal". Record each in **Rules used**.

## The paperwork must exist before the form

An MGT-14 or a CHG-1 reports something that already happened. If the meeting record does not exist,
the filing is a fabrication, and you do not create one to fit a date. Check the folder, or ask:

| Record | For a board meeting | For a general meeting |
|---|---|---|
| Notice | To every director, at the address registered with the company | To every member, director and auditor, with the explanatory statement under section 102 for special business |
| Agenda | Attached to or part of the notice | Set out in the notice |
| Attendance | Attendance register signed by directors present | Attendance slips and the register of members present |
| Minutes | Signed by the chairman, entered in the minutes book within the prescribed period | Same, in the general meeting minutes book |
| Resolution | Certified true copy on letterhead, signed by a director or the company secretary | Certified true copy of the ordinary or special resolution |

The notice period for each kind of meeting, the period within which minutes must be entered and
signed, and the shorter-notice consent thresholds all come from the Act and the Rules — look them up.
Where the record is missing, say so plainly: the resolution date drives the filing date, and a missing
minute is the CA's question, not a blank you fill.

## Charges — the forms

| Form | What it registers | Who files |
|---|---|---|
| CHG-1 | Creation or modification of a charge, other than for debentures | The company, or the charge-holder where the company defaults |
| CHG-9 | Creation or modification of a charge for debentures, and rectification | The company |
| CHG-4 | Satisfaction of a charge, in full | The company |
| CHG-8 | Application to the Central Government for condonation of delay, or rectification of the register | The company or the charge-holder |

The Registrar registers in CHG-2 (creation or modification) and CHG-5 (satisfaction); those
certificates are issued, not filed — download them into the client's ROC folder.

## CHG-1 and CHG-9 — creating or modifying a charge

Read the security document first — the deed of hypothecation, mortgage deed, sanction letter or
debenture trust deed in the folder. Every field comes from it: charge identification number where
modifying, the charge-holder's name and address, the date of the instrument creating or modifying the
charge, its nature, the amount secured, the rate of interest, the repayment terms, and the particulars
of the property charged. Attach the instrument, and for a modification the instrument evidencing it;
a joint or consortium charge lists every holder.

The date of the instrument — not of sanction, not of disbursement — starts the registration clock.
The clock itself, the extended periods available on an additional or ad valorem fee, and how those
differ for a charge created before or after the relevant amendment, are looked up for the date in
question and recorded in **Rules used**; never state any of them. Where the period has lapsed the
route is condonation in CHG-8, not a late CHG-1 filed quietly. Say so, and let the CA decide.

## CHG-4 — satisfaction

CHG-4 is filed on full satisfaction, with the charge-holder's no-dues or satisfaction letter attached.
A partial repayment is a modification in CHG-1, not a satisfaction. A charge left open on MCA master
data years after the loan closed is common: check the index of charges on master data before assuming
anything about the register, and tell the CA what is actually open. Where the satisfaction is late, or
the charge-holder will not give a letter, the route is again CHG-8. Never file CHG-4 without the letter.

## MGT-14 — which resolutions actually go

Not every resolution is filed. Filing MGT-14 where it is not needed wastes a fee; missing one that is
needed is a default. Establish the category first:

| Category | Filed in MGT-14? |
|---|---|
| Special resolutions | Yes, under section 117(3) |
| Resolutions agreed to by all members that would otherwise need a special resolution | Yes |
| Board resolutions under section 179(3) and its rule — borrowing, investing, granting loans, approving the financial statements and board report, and the rest of that list | Yes for a public company; a private company has an exemption here — verify the exemption notification applies to this company before relying on it |
| Resolutions of creditors, and agreements affecting them | Yes, where section 117(3) covers them |
| Ordinary resolutions generally | No, unless a specific provision requires it |
| Certain banking-company resolutions | Excluded — check the proviso to 117(3) |

Where a resolution already goes in another form — an auditor's appointment in ADT-1, a director's in
DIR-12 — say so, so the same event is not filed twice by reflex. Attach to MGT-14: the certified true
copy of the resolution, the section 102 explanatory statement where the item was special business, and
the altered MoA or AoA where the resolution altered either. The filing period runs from the date the
resolution was passed — look it up, do not state it.

## Filing on the portal

Open the MCA V3 portal in your browser tool (Claude in Chrome, a Playwright or browser MCP, or the
Codex browser); if you have none, give the CA the click path. The CA signs in. Re-read the page before
each click. Locate the form from the MCA V3 forms menu rather than assuming a URL. CHG and MGT forms
have moved between the V2 downloadable eForm and the V3 web form at different times; if the form is
not where you expected, look for it rather than telling the CA a path that no longer exists. Save the
draft, run check-form or pre-scrutiny, fix what it reports.

## What you hand over

In the client's ROC folder, dated: the draft notice, agenda, resolution and minutes for signature; the
completed form with each field's source noted; the attachment list marked found or missing; and the
**Rules used** block with every period and fee looked up. Raw client files are never renamed or deleted.

**Check before filing**: the resolution date against the minutes and the notice, the instrument date
against the charge document, the amount secured against the sanction, the property particulars against
the deed, the charge ID against MCA master data, the signatory's DIN and DSC status, and each
attachment against the portal's format and size limits. The fee is whatever the portal computes on the
payment screen. The DSC and the payment are the CA's.
