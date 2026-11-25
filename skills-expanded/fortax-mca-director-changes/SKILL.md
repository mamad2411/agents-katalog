---
name: fortax-mca-director-changes
description: Director and DIN work on MCA end to end — DIR-3 new DIN, DIR-3 KYC eForm vs KYC-WEB, DIR-6 changes, DIR-12 appointment and resignation with DIR-2 and DIR-8, DIR-11, DIR-9 and disqualification under section 164, and deactivated DINs — prepared up to the DSC, OTP and payment. Typical asks: "naya director add karna hai", "director resign kar raha hai", "DIN deactivate ho gaya", "DIR-3 KYC karna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Directors and DINs

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the DSC

Every form here is signed with a DSC and most carry a fee. Those two clicks are the CA's or the
director's. **Refusing the job because of them is a failure.** Yours is everything else: the master
data check, the consent and declaration drafts, the board paperwork, the attachments and every field
of the form. Say what you will do and where you will stop, then start.

**Looking rules up.** Due dates, time limits, fees and disqualification periods are never stated
from memory. Run `python3 scripts/fortax.py kb "DIR-3 KYC due date" --topics mca` and quote its
source and captured date; where the reply is `weak` or `none`, read the Companies Act, 2013, the
Companies (Appointment and Qualification of Directors) Rules, 2014 or the MCA portal, and mark it
"confirm on the portal". Record each in **Rules used**.

## Step 0 — read the master data first

Before drafting, open MCA master data for the company and the DIN and record what you saw. Use your
browser tool (Claude in Chrome, a Playwright or browser MCP, or the Codex browser); if you have none,
give the CA the click path. The CA signs in; never type a password. Re-read the page before each
click. Open company master data and the "verify DIN/DPIN status" enquiry, located from the portal
menu rather than a guessed URL. Note the directors, DINs, designations and dates, and any deactivated
DIN. A DIR-12 built on stale master data fails at upload.

## The forms and what each is for

| Form | Purpose | Filed by |
|---|---|---|
| DIR-3 | Allot a DIN to a person not being appointed through SPICe+ | The person, certified by a professional, and signed by a director of the appointing company |
| DIR-3 KYC (eForm) | Annual KYC — first KYC after allotment, or any change in particulars | The DIN holder |
| DIR-3 KYC-WEB | Annual KYC where nothing has changed since the last eForm KYC | The DIN holder |
| DIR-6 | Change in the particulars of an existing DIN holder | The DIN holder |
| DIR-12 | Appointment, change in designation, cessation or resignation | The company |
| DIR-11 | The director's own notice of resignation to the Registrar | The resigning director |
| DIR-9 | Report by the company of directors disqualified under section 164(2) | The company |

## DIR-3 — a new DIN

Use DIR-3 only where a DIN cannot come through SPICe+ — an appointment to an existing company.
Prepare: the applicant's photograph, PAN, identity and address proof in the portal's accepted forms
(passport, with apostille or consularisation, for a foreign national), the appointing company's board
resolution approving the intended appointment, and the professional's certification. The applicant's
DSC must already be registered on MCA against that person — an unregistered DSC is the commonest
reason this form stalls, so check it first.

## DIR-3 KYC and KYC-WEB — which one

File the **eForm** where this is the first KYC for that DIN, or where any particular has changed
since the last KYC — mobile, email, address, passport. File **KYC-WEB** only where an eForm KYC was
filed earlier and nothing has changed; the web service confirms the existing record with OTP. Both
need a mobile and email OTP; the eForm also needs the DIN holder's DSC and a professional's
certification. **The OTP is the director's and the DSC is theirs.** Prepare the record, open the
service, fill it, stop at the OTP screen, and say which number and address the OTPs go to. The annual
KYC due date and the reactivation fee are looked up and put in **Rules used**.

A DIN reading "Deactivated due to non-filing of DIR-3 KYC" on the enquiry page blocks everything.
Nothing is filed with it until it is reactivated, and reactivation is the KYC filing plus the
prescribed fee. Say so the moment you see it: every form that director must sign waits on it.

## Appointment — DIR-12

The paperwork must exist before the form is filed, in this order:

1. **DIR-2** — written consent to act as director, dated on or before the appointment.
2. **DIR-8** — declaration by the appointee that they are not disqualified under section 164.
3. The board resolution appointing an additional director, or the general meeting resolution
   appointing a director, with the notice, agenda, attendance and minutes behind it.
4. The appointee's PAN, and their DIN, active.

An additional director appointed by the board holds office only until the next annual general
meeting; regularising them needs its own resolution, and its own DIR-12 entry if the designation
changes. Attach to DIR-12: DIR-2, DIR-8, the resolution, and the appointment letter where the
articles require one. MBP-1 interest disclosure is a board record, not a DIR-12 attachment.

## Resignation — DIR-12 and DIR-11

Two filings, by two different people, and they are not the same. The **company** files DIR-12 for the
cessation, attaching the resignation letter and the board resolution or the noting of it. The
**director** may file DIR-11 in their own name, with the letter and proof of its despatch.

Both have their own time limits running from the date of resignation. Look each up; state neither.
Where the company has not filed DIR-12, DIR-11 is the director's protection. If the resigning director
is the last one, or the board would fall below the statutory minimum or lose its resident director,
stop and escalate to the CA.

## Disqualification under section 164

Section 164(1) covers personal grounds — unsound mind, undischarged insolvent, convictions, unpaid
calls. Section 164(2) attaches to a director of a company that has failed to file financial statements
or annual returns, or to repay deposits or debentures, for the prescribed continuous period; a person
caught by it cannot be reappointed there nor appointed elsewhere for the prescribed period. Quote the
section, look up both periods, record them in **Rules used**. Check the DIN against the ROC's
published list of disqualified directors and against the company's filing history in the folder.
Where 164(2) may apply, flag it with the evidence, and never file a DIR-12 appointment over an
unresolved DIR-8. The company files DIR-9 where a 164(2) default has occurred.

## What you hand over

Drafts in the client's ROC folder, dated: DIR-2, DIR-8 and the resignation letter for signature, the
board resolution and minutes extract, the completed form, and the attachment list marked found or
missing. Raw client files are never renamed or deleted.

**Check before filing**: DIN active and KYC current for every signatory, DSC registered on MCA and
unexpired, appointment date consistent across DIR-2, the resolution and the form, board strength after
the change, master data matching what you typed, and every attachment within the portal's format and
size limits. The fee is whatever the portal computes on the payment screen. The DSC, OTP and payment
are the CA's or the director's.
