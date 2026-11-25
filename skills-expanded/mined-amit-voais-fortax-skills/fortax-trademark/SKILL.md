---
name: fortax-trademark
description: Indian trademark work from search to renewal — IP India public search, Nice class selection, word vs device mark, applicant category and fee slab, user affidavit and a prepared TM-A; then status check, examination report reply, hearing brief, Trade Marks Journal and opposition / counter-statement, certificate, and renewal on TM-R — prepared up to the CA's payment, e-sign and submit. Typical asks: "brand ka trademark karna hai", "TM search karo", "objection aaya hai reply banao", "trademark renewal due hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Trademark: filing, objection, opposition, renewal

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Every stage ends in a payment, a DSC or e-sign, and a submit belonging to the applicant, the agent or the
CA. That is the last step, not the job. **Refusing the work because its final click is theirs is a
failure.** The search, the classes, the mark, the category, the affidavit, every field of TM-A, reading an
examination report, drafting the reply, assembling evidence, watching the journal and preparing TM-R are
yours. Say in one line what you will do and where you stop, then start.

**Fees, periods and windows are never stated from memory.** Class counts, fee per class, slabs, the
opposition window, the counter-statement period, validity and the renewal, surcharge and restoration
windows all change. Read them on the IP India site or run
`python3 scripts/fortax.py kb "trademark renewal window TM-R"` (quote its source and captured date; on
`weak` or `none`, read the Trade Marks Act, 1999 / Trade Marks Rules, 2017 or the portal) and record each in
**Rules used** with the date checked.

**Portals.** Open IP India public search, status, e-register and e-filing in your browser tool (Claude in
Chrome, a Playwright or browser MCP, or the Codex browser); if you have none, give the CA the click path and
work from what they paste or screenshot. The CA signs in; never type or store a password. Re-read the page
before every action; elements change per page.

**No opinions over your own name.** You report what the register shows. You do **not** opine on
registrability, likelihood of success, whether an opposition will succeed, or infringement risk without the
CA's explicit sign-off, and such an opinion goes out over the CA's name. Asked, set out the grounds, the
evidence on each side, and the gaps in both.

Folders: working files in `<Client>/<FY 2026-27>/Trademark/`; originals of use evidence, journal pages and
certificates in `<Client>/Permanent/Trademark/`. Raw client files are never renamed or deleted.

# Part A — filing a new application (TM-A)

## A1 — intake

Write `<date>_TM_intake.md`. Never take the mark from a phone call; get it in writing. A space, a hyphen or
a capital changes the application.

| Field | Needed for |
|---|---|
| The mark, exactly as it will be used | TM-A and the search |
| Word mark, device mark, or both | Artwork and number of applications |
| Applicant legal name and address, as on PAN or incorporation | TM-A |
| Applicant category | Fee slab and the proof to attach |
| Goods and services actually sold or offered | Class selection |
| In use already, and from when | Prior-use claim and the affidavit |
| Agent details, if any | TM-A and the power of attorney |

## A2 — the public search, before anything is promised

- Open the IP India public search. Select the search type (wordmark, phonetic, Vienna code) and enter
  the mark. Run it three ways — exact, phonetic, starts-with — across **every class you are considering**.
- Record each hit: application number, mark, class, proprietor, status, date. Screenshot as evidence.
  Write `<date>_TM_search_<mark>.md` with a conflict table and one line each on why a mark is close —
  identical, phonetic, same class, same trade channel.

**A search result is never a guarantee of registration.** Put that sentence in the file. A prior user off
the register, an application not yet reflected, an examiner's own view on distinctiveness, or a later
opposition can all defeat a mark that looked clear.

## A3 — classes, from what the business actually sells

Classification follows the Nice Classification, adopted in the Fourth Schedule to the Trade Marks Rules.
**Goods and services are separate classes.** A firm that makes a product and also runs a service around it
needs both; one does not cover the other. List, in the client's words, what is sold and what is done for
customers. Map each line using the IP India class finder or the class headings on screen, not from memory.
Split goods from services, name the class for each line, and get the CA's confirmation before entering
anything. Each extra class is a separate cost and a separate risk of objection; any multi-class concession
is read on the portal, not assumed.

## A4 — mark type and applicant category

| Choose | When | Watch for |
|---|---|---|
| Word mark | The words are the asset, in any font or colour | Widest cover for the words, none for the logo |
| Device mark | Logo, stylisation or a colour combination matters | Protects the mark as depicted; a redrawn logo may fall outside |
| Both, separately | Name and logo both carry value | Two applications, two fees |

Claiming colour narrows protection to that scheme; say so before it is claimed. Artwork must meet the
portal's format and size limits — read them on the upload screen.

**Applicant category** drives the fee slab and the proof required: individual or sole proprietor (a
proprietorship declaration); a DPIIT-recognised startup (the recognition certificate — see
`fortax-msme-iec-fssai`); a Udyam registered small enterprise (the Udyam certificate); partnership, LLP,
company, trust or society (constitution proof and authorisation). A concessional slab claimed without the
certificate in the folder becomes a defect at examination. Check the certificate exists, is current, and
carries the applicant's exact legal name. Confirm the slabs on the portal; never state a fee.

## A5 — use, and the user affidavit

Two routes only. **Proposed to be used** — no affidavit, no use evidence. **Used since a date** — a
prior-use claim needing a user affidavit and evidence from that date (see the evidence table in Part C). A
first-use date the client cannot evidence is worse than "proposed to be used"; it invites attack. Draft the
affidavit only from documents in the folder, and never fabricate or round a date. If the earliest evidence
is later than the date stated, flag it — do not quietly file the safer date. Index the originals in
`<date>_TM_use_index.md`.

## A6 — prepare TM-A

On the IP India e-filing site, fill applicant details and category, agent and power of attorney, mark type
and representation, class or classes with the specification of goods and services, use claim with date,
priority claim if any, and the address for service in India. Upload artwork, category certificate,
affidavit and POA, saving at every step. Then stop. Payment, DSC or e-sign, and submit are the CA's.

# Part B — after TM-A: objection, hearing, opposition, renewal

This starts at an application number.

## B1 — know where the application actually is

Never work from the client's account of the status; check the register. Open the IP India status and
e-register pages, enter the application number and read: status, class, report date, journal number and
date, opposition entries, correspondence. Download the report and every notice into the client's trademark
folder; screenshot the status page. Record the stage and the date checked in `<date>_TM_<appno>_status.md`.

## B2 — read the examination report properly

| Objection | What it says | What the reply supplies |
|---|---|---|
| Absolute grounds | Descriptive, generic, laudatory or non-distinctive | Distinctiveness of the mark as a whole; coined or arbitrary use; acquired distinctiveness with evidence |
| Relative grounds | Conflicts with cited earlier marks | Each cited mark distinguished on wording, structure, class, goods, trade channel, consumer; consent or coexistence if held |
| Formalities | Wrong category, missing affidavit or POA | Fix the defect and attach the document; do not argue |
| Specification | Goods or services too broad or vague | A narrowed specification the client can live with |

Tabulate the objections, answer each under its own number; one not answered is treated as unanswered.

## B3 — draft the reply, then prepare the hearing

Write `<date>_TM_<appno>_examination_reply.md`. Structure: application number, mark, class, applicant and
report date; each objection quoted and answered in the report's own numbering; for every cited mark a
comparison row — mark, class, goods, proprietor, status — and why it does not conflict; evidence of use by
exhibit number where distinctiveness is claimed; the prayer to waive and advertise. A cited mark abandoned,
removed or restricted is a strong point, so verify its status and screenshot it. Quote the report, never
paraphrase it. Cite case law only after verifying it through `fortax-deep-research`, never from memory, and
assert no market share, sales or years of use unless a folder document supports it. You draft; the CA
settles it. Attach on the portal, stop at the submit.

**If a hearing is fixed**, prepare it, do not attend. Diary the date and mode from the notice. Build a brief:
the objections on one page, the reply filed, the cited-mark table re-verified that week, exhibits in order,
and what the CA carries — POA, affidavit, user evidence, any consent or coexistence agreement. For an
adjournment or post-hearing submissions, read the procedure on the portal.

## B4 — publication, opposition and counter-statement

Once objections clear, the mark is advertised in the Trade Marks Journal. Record the journal number and date
and download the journal page into `Permanent/Trademark/` — the client's proof of advertisement. The
opposition window runs from publication: read its length on the IP India site, put it in **Rules used**, and
remind the CA at its end. Advertised is not registered; say so plainly.

| Stage | What you prepare |
|---|---|
| Notice of opposition | Summary of the grounds, the opponent's marks and their register status |
| Counter-statement | A draft answering each ground; deny what is not admitted; assert the applicant's own use |
| Opponent's evidence | An index, marking what is actually proved rather than asserted |
| Applicant's evidence | Numbered exhibits with the supporting affidavit; hearing brief as in B3 |

Each stage carries a time limit, extendable only in the prescribed manner. Look every one up; never assert
one. A missed counter-statement window can be fatal — flag it in writing the day the notice is downloaded.

## B5 — certificate, then renewal on TM-R

On registration, download the certificate into `Permanent/Trademark/` and record in the client's permanent
file the mark, the application and registration numbers, the classes, and the date from which registration
runs. Renewal is computed from that date, so get it right; look the validity period and the renewal window
up, set the calendar entry, and state neither from memory.

Before filing TM-R, confirm the registration is live and the proprietor's name and address are current — a
change needs its own form first. On the e-filing site, prepare TM-R for the registration number and classes.
There is a window before expiry, a surcharged late route after it, and a restoration route beyond that;
those lengths, fees and the surcharge all change, so read them on the portal and record them. Attach the POA
where the agent files, then stop at payment and submit.

# Part C — evidence of use

| Evidence | What it proves |
|---|---|
| Dated invoices showing the mark on the goods or service line | Actual commercial use, and from when |
| Packaging, labels and signage photographs | The mark as used against the mark as applied |
| Dated advertisements, media coverage, domain and social handle records | Reach, continuity, earliest public use |
| GST returns or audited accounts showing the branded revenue line | Scale, tied to a filed document |
| Distributor, franchise or licence agreements | Use by permitted users |

Originals stay untouched in `<Client>/Permanent/Trademark/`. The index and exhibit bundle go to
`<date>_TM_<appno>_evidence_index.md`, one row each: document, date, what it proves, exhibit number.

# Hand over

- What is filled, field by field, and what is blank and why; or the stage the application is at with the
  register screenshot and the date checked, and the drafted reply, counter-statement or TM-R with what is
  attached to it.
- The search file with its conflict table and the no-guarantee line; the class mapping the CA confirmed,
  and the classes deliberately left out.
- **Check before filing a TM-A**: the mark's exact spelling and artwork against the client's written
  instruction; applicant name against PAN or incorporation; category against the certificate attached;
  class list against the goods-and-services mapping; first-use date against the earliest evidence in the
  folder.
- **Check before filing a reply, counter-statement or TM-R**: every objection answered and numbered; every
  cited mark's status re-verified today; every claim about use traceable to a document in the folder; the
  applicant's name and address matching the register; the right classes on TM-R.
- In every case: each fee, slab, period and window verified on the portal today, listed in **Rules used**
  with its source and the date checked.
