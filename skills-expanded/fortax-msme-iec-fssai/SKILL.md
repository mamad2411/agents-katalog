---
name: fortax-msme-iec-fssai
description: Business registrations in India — Udyam (MSME) registration and update, Importer Exporter Code on DGFT with its annual update, FSSAI basic registration, state or central licence and renewal on FoSCoS, and Startup India DPIIT recognition — eligibility check, documents and every portal field, prepared up to the client's Aadhaar OTP, e-sign, payment or submit. Typical asks: "Udyam certificate chahiye", "IEC banwana hai", "FSSAI license kaunsa lagega", "startup recognition apply karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Udyam, IEC, FSSAI, Startup India

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Each of these ends in an Aadhaar OTP, a DSC or a payment belonging to the client or the CA. **That is the
last step, not the job.** The eligibility check, the documents, the data and every field on the portal are
yours. Say in one line which registration, what you will fill and where you stop, then start.

Common to all four: fix the constitution and the exact legal name at intake, work only from documents in the
client folder, and write outputs to the client's registrations folder (for example
`<Client>/<FY 2026-27>/Registrations/`) with a dated name, never renaming or deleting a raw client file.
**Never state a fee, a turnover or investment limit, a validity period or a due date from memory** — look
each up on the portal or with `python3 scripts/fortax.py kb "Udyam classification limits"` (quote its source
and captured date; on `weak` or `none`, read the portal) and record it in **Rules used** with the date checked.

**Portals.** Open each portal in your browser tool (Claude in Chrome, a Playwright or browser MCP, or the
Codex browser); if you have none, give the CA the click path and work from what they paste or screenshot.
The client or CA signs in; never type or store a password. Re-read the page before every step.

## 1. Udyam registration (MSME)

**Who.** Micro, small and medium enterprises, classified on investment in plant, machinery or equipment
together with turnover. Those limits define the category and are revised: read the current ones on
udyamregistration.gov.in and record them. Traders are covered only for the purposes notified, so confirm the
activity is in scope first.

**Documents.** Aadhaar of the proprietor, managing partner or karta — for a company or LLP, of the
authorised signatory — and the mobile linked to it, since the OTP goes there; PAN of the enterprise, which
the portal validates against the income tax database; the GSTIN where registered, from which the portal
pulls turnover; and the bank account and IFSC, NIC codes, employee count and address.

**Portal.** udyamregistration.gov.in. **Check for an existing registration first** with Print / Verify
Udyam Certificate; a duplicate is a defect. Open the new-registration page, enter the Aadhaar number and
name, then **stop — the Aadhaar OTP is the client's**. After it, continue with PAN validation and the
enterprise details, pick NIC codes from what the business actually does, and stop again at the declaration.

Enterprises on the old Udyog Aadhaar had to migrate to Udyam, and a Udyam registration must be updated
periodically with current ITR and GST data or it is liable to suspension. The update cycle and the
consequence of missing it are on the portal — read them, do not assert them.

## 2. Importer Exporter Code (DGFT)

**Who.** Anyone importing into or exporting out of India, subject to the notified exemptions for personal
use and certain government bodies. One IEC per PAN — check whether a code already exists against the PAN.

**Documents.** PAN of the entity; proof of establishment or incorporation; address proof of the premises
(sale deed, lease, rent agreement or a recent utility bill in the entity's name); a cancelled cheque or
bank certificate for the account to be linked; DSC or the signatory's Aadhaar for e-sign.

**Portal.** dgft.gov.in. Register the user against the PAN, then Services → IEC → Apply for IEC. The CA
signs in. Fill entity details, branch and address, directors or partners, and bank details; upload the
proofs in the formats the upload screen states. **Stop at** the declaration, the fee payment and the DSC or
Aadhaar e-sign. Any later change of address, bank, constitution, name or directors is filed as a
modification on the same portal with the same e-sign; some need prior approval, so check that change type.

**Annual update.** An IEC must be updated on DGFT every year even when nothing has changed, or it is liable
to be deactivated. Look up the update window and the reactivation route on the portal and record them, never
state the dates, and put the update on the client's compliance calendar the day the IEC is issued.

## 3. FSSAI registration and licence

**Who.** Every food business operator — manufacture, processing, packing, storage, transport, distribution,
retail, catering, import, e-commerce food. Which of three levels applies turns on turnover, production
capacity, the activity and whether the business runs in more than one state. **Look the criteria up on
foscos.fssai.gov.in; never state a turnover figure or a capacity.**

| Level | Broad scope | Confirm on FoSCoS |
|---|---|---|
| Basic registration | The smallest operators, single state | Turnover ceiling |
| State licence | Mid-sized, single state | Turnover and capacity bands |
| Central licence | Large operators, importers, multi-state head office, e-commerce, notified categories | Turnover floor, category list |

**Documents.** Photo and ID of the proprietor, partners or directors; premises and constitution proof; the
product list in FoSCoS's own category tree; for manufacturing, the layout plan, equipment list and water
test report where required; a food safety management plan or declaration; NOC from the local body or the
owner where rented; and for importers, the IEC.

**Portal.** foscos.fssai.gov.in. Choose level, state, district and kind of business, then fill the
application — re-read the page before every step, since the category tree drives what the form asks next.
**Stop at** the fee payment and the submit; afterwards download the certificate and record the number.

**Renewal.** A licence runs for a chosen tenure and must be renewed before expiry, and a lapse means applying
afresh and, for some categories, stopping operations. Tenure options, the renewal window and the late fee are
on FoSCoS — read them into **Rules used**, never quote them. Annual returns apply to some licence categories;
confirm which on the portal.

## 4. Startup India / DPIIT recognition

**Who.** A private limited company, registered partnership firm or LLP, within a defined age from
incorporation and under a turnover ceiling, working on innovation or improvement of a product, process or
service, or with a scalable business model. An entity formed by splitting up or reconstructing an existing
business does not qualify. **The age limit and the turnover ceiling are notified and revised — read them on
startupindia.gov.in and record them.**

**Documents.** Certificate of incorporation or registration; PAN; a write-up on what makes the business
innovative or scalable; directors' or partners' details; and the website, pitch deck, patent or award if any.

**Portal.** startupindia.gov.in. Create the profile, then apply for DPIIT recognition: entity details,
activity, funding and the innovation write-up. That write-up is the application — draft it from what the
client actually does, in plain language, and let the CA settle it. **Stop at** the declaration and submit.

Recognition is the certificate a client needs for the concessional trademark and patent fee slabs, so file
it in `<Client>/Permanent/` and point `fortax-trademark` at it. The separate income-tax exemptions for
startups are a further application with their own conditions; DPIIT recognition is not that exemption.

## Hand over

For each registration, in the client's registrations folder with a dated name: the intake sheet, the
document checklist with what is still missing, and a note of what was filled where.

- What is filled, what is blank and why, and the exact next click and whose it is.
- **Check before filing**: legal name against PAN and the constitution proof; address against the proof
  uploaded; activity codes or food categories against what the business actually does; no duplicate
  registration against that PAN; every certificate in the entity's exact legal name; every limit, fee,
  tenure and update window verified on the portal today, in **Rules used** with its source.
- The recurring obligation each registration creates — the Udyam update, the IEC annual update, the FSSAI
  renewal, any annual return — listed for the client's compliance calendar with its source. Record the
  registration numbers in the client's permanent file.
