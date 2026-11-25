---
name: fortax-mca-incorporation
description: Incorporate a private, public, OPC, section 8 or producer company in India on the MCA V3 portal — name check (MCA and trademark register), RUN or SPICe+ Part A, Part B, AGILE-PRO-S (INC-35), INC-9, e-MoA (INC-33) and e-AoA (INC-34), office proof and the pre-scrutiny fix-up — prepared up to the DSC and payment. Typical asks: "company incorporate karni hai", "pvt ltd registration", "SPICe+ bharna hai", "naam available hai kya".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Company incorporation (SPICe+)

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Every MCA filing ends in a DSC affixation and a payment. Both belong to the CA or the director.
**Refusing an incorporation because its last step is theirs is a failure.** Everything before it is
yours: the name search, the intake, the documents, every field of SPICe+ Part A and Part B, the
linked forms, the e-MoA and e-AoA, and the pre-scrutiny fix-up. Say in one line what you will do and
where you will stop, then start.

**Looking rules up.** Every period, cap, fee and limit below is looked up, never stated from memory:
run `python3 scripts/fortax.py kb "SPICe+ name reservation validity" --topics mca` and quote the
source URL and captured date. Where the reply is `weak` or `none`, read it on the MCA portal or the
Companies (Incorporation) Rules, 2014, and mark it "confirm on the portal". List each in a
**Rules used** block with source and date checked.

## Step 1 — intake

Write `<date>_incorporation_intake.md` in the client's ROC folder (for example
`<Client>/<FY 2026-27>/ROC/`). Ask only for what is missing.

| Field | Needed for |
|---|---|
| Company type (private, public, OPC, section 8, producer) | decides forms, subscribers, declarations |
| Proposed names in preference order, and the objects in plain words | Part A, activity code, MoA objects |
| Authorised and paid-up capital | Part B, subscription table, stamp duty |
| Registered office address, and whether it exists yet | Part B, or INC-22 later |
| Each subscriber: name, PAN, address, shares subscribed | e-MoA, INC-9 |
| Each proposed director: DIN if held, else PAN and ID documents | Part B, DIN allotment |
| Nominee (OPC only), and state of registration | INC-3, ROC jurisdiction, stamp duty |

Fix the constitution first. It decides the subscriber count, the declarations and which linked forms
open. Validate every PAN format (five letters, four digits, one letter) and check the 4th character
against the person's status (P individual, C company, F firm, and so on).

## Step 2 — name availability, and the discipline around it

Never promise a name — the Registrar decides. Before proposing anything, run all of these:

- MCA company and LLP name search, for identical and closely resembling names.
- The trademark register (IP India public search), for the proposed word in the classes matching the
  objects. A collision with a registered mark gets the name refused or challenged later. Search it, do
  not assume. See `fortax-trademark` for how to run the search.
- The name-availability restrictions in the Companies (Incorporation) Rules — undesirable names,
  names needing central government approval, names implying state patronage or a regulator link — and
  whether the objects need a sectoral regulator's in-principle approval (RBI, IRDAI, SEBI) first.

Give the CA two or more names with the evidence for each, say which are riskier and why, and write
"this name may be refused" where that is true. Reservation runs either through **RUN** (name only) or
through **SPICe+ Part A**, which reserves inside the incorporation flow — usually the better route,
since reservation and filing stay in one application. A reserved name has a validity window and a
capped number of resubmissions; look both up, put them in **Rules used**, and never state either from
memory.

## Step 3 — SPICe+ Part A

SPICe+ is a web form on the MCA V3 portal, filed from a logged-in MCA account — not a downloadable
PDF like the old V2 eForms. Open the portal in your browser tool (Claude in Chrome, a Playwright or
browser MCP, or the Codex browser); if you have none, give the CA the click path and work from what
they paste or screenshot. The CA signs in — password, OTP and captcha are theirs; never type or store
a password. Re-read the page before every click, since elements change on each page. Locate SPICe+
under the company forms menu rather than assuming a URL. Fill company type, class, category,
sub-category, the activity code matching the real objects, and the proposed names with their
significance. Save the draft, record the application number.

## Step 4 — Part B and the linked forms

Part B carries the whole incorporation: capital structure, registered office, subscribers and
directors, DIN applications for those without one, PAN and TAN, and the professional certification.

| Form | What it does |
|---|---|
| INC-33 | e-MoA — objects, liability, capital, subscription table |
| INC-34 | e-AoA — articles, from Table F/G/H/I or with amended regulations |
| AGILE-PRO-S (INC-35) | GSTIN (optional), EPFO, ESIC, bank account, professional tax where the state needs it |
| INC-9 | declaration by each subscriber and first director, auto-generated in most cases |
| INC-3, URC-1 | OPC nominee consent; conversion of an existing firm or LLP, in that route only |

DIN is allotted through SPICe+ for first directors, up to a capped number per application; anyone
holding a DIN uses it, anyone beyond the cap applies in DIR-3 first (`fortax-mca-director-changes`).
Confirm the cap on the portal.

## Step 5 — what each person must give

- Every subscriber and director: PAN, plus identity and address proof in the form the portal accepts;
  for a foreign national or NRI, passport with apostille or consularisation as applicable.
- Photograph where asked; DIR-2 consent from every director; the professional's INC-8 declaration.
- Registered office proof: ownership document or rent/lease deed, an NOC from the owner, and a recent
  utility bill. **A rented office with no NOC stops the filing** — flag it at intake, not at Part B.
  Where the office is not ready, incorporate on a correspondence address and file INC-22 after,
  within a time limit you look up rather than recall.
- Anything not in the client folder goes in a "please send" list at the top of the intake sheet.

## Step 6 — stop at the DSC and the payment

Fill everything, run the portal's own pre-scrutiny or check-form, fix what it reports, stop, and hand
over with:

- Which forms are complete, which fields are blank and why; whose DSC each form needs, and whether
  every DSC is registered on MCA and unexpired.
- That fee and stamp duty vary by state and by authorised capital — give the figure the portal itself
  computes on the payment screen, never one from memory.
- **Check before filing**: names against the search evidence, object clause against the activity code,
  subscription table totalling the paid-up capital (add it in a spreadsheet or script, not in your
  head), every PAN and DIN, office proof against the typed address, and each attachment against the
  portal's format and size limits.

After the CA submits, record the SRN and date. Resubmission has its own window and attempt cap — look
them up. On approval the certificate of incorporation issues with the CIN, and PAN and TAN come with
it; download the certificate, approved MoA and AoA and the PAN and TAN letters into the client's ROC
folder, and file the certificate in `<Client>/Permanent/`.

## Output

In the client's ROC folder, dated: the intake sheet with application number and SRN, the name search
evidence, the document checklist with what is missing, and a note of what was filled where. Every
rule relied on goes in **Rules used**. Never a submitted form, and never rename or delete a raw file.
