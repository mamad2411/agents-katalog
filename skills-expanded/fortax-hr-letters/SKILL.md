---
name: fortax-hr-letters
description: Draft employment letters for a client company from the firm's own templates — offer, appointment, probation extension, confirmation, increment, transfer, warning, show cause, acceptance of resignation, relieving and experience certificate — filling only instructed terms, leaving signature and date blank, matching the salary structure file, and flagging bonds, non-competes, misconduct and termination for legal review. Typical asks: "offer letter banao", "appointment letter draft karo", "relieving letter chahiye", "warning letter likhna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# HR letters

You draft employment paperwork for a client company from the firm's own templates. You fill only what
you were given, you leave the signature and the date for a human, and you flag anything that reads
like it needs a lawyer.

1. **Never invent a term.** If the notice period, probation length, salary figure, designation,
   reporting line, location, joining date, bond, non-compete or leave entitlement is not in the CA's
   instruction and not in the template, it does not go in the letter. Leave `[____]` and list it.
2. **Never sign and never date.** No signature block filled, no "For Sharma Traders Private Limited"
   with a name under it, no date on the letter or in the body. Those are a human's.
3. **Flag for legal review** anything with legal consequence you were not told to write: bonds and
   service agreements, non-compete and non-solicit, IP assignment, garden leave, salary recovery on
   early exit, termination for cause, anything alleging misconduct, and anything that varies a term
   already given to the employee in writing. `fortax-contract-review` can take a flagged clause further.

## Step 1 — the template comes first

Look in the firm's templates folder for its letter templates and use the one that is there. Read it
whole before drafting. Keep its clause order, headings, numbering and letterhead placeholders. The
firm's wording is the firm's position; do not improve it.

Where the firm has no template for the letter asked for, say so in one line, draft a plain structural
version, mark it clearly as not from a firm template, and ask whether it should be saved as one. Never
import wording from another client's signed letter.

## Step 2 — the facts

From the client's own records take the employing company's legal name, address and CIN. Take employee
facts from documents, not from conversation — the salary structure file from `fortax-salary-structuring`,
the appointment file, the HR mail. Where the instruction and a document disagree, name both and stop.

| Field | Needed for |
|---|---|
| Employee full name, as it will appear on record | Every letter |
| Designation, department, grade | Offer, appointment, increment, transfer, confirmation |
| Date of joining | Appointment, confirmation, relieving, experience |
| Location and reporting manager | Offer, appointment, transfer |
| Compensation, by component | Offer, appointment, increment |
| Probation period and confirmation date | Probation, confirmation |
| Notice period | Offer, appointment, resignation acceptance, relieving |
| Effective date of the event | Increment, transfer, relieving |
| Last working day | Resignation acceptance, relieving, experience |

Each of these is a client term, not a statutory number, so it comes from the instruction or the
template. Where a letter must touch a statutory entitlement — leave, gratuity, bonus, notice under a
state's shops and establishment Act — do not state a period, rate or number. Reproduce the template's
wording, or refer to applicable law and company policy, and tell the CA which figure needs verifying
if they want it spelled out (`fortax-gratuity-bonus-leave` has the lookups).

## Step 3 — the letters

| Letter | Turns on | Careful with |
|---|---|---|
| Offer | Acceptance by a date, joining by a date | Not the appointment letter; do not fold in full terms unless the template does |
| Appointment | Joining actually happened | Full terms and the annexed structure, matching the salary file exactly |
| Probation extension | A review decision the client made | Reason, revised end date, and that it is an extension, not a fresh probation |
| Confirmation | Probation completed | Confirmation date, and whether any term changes on confirmation |
| Increment | An approved revision | Effective date, arrears if any, revised annexure from `fortax-salary-structuring` |
| Transfer | A management decision | Location, effective date, whether terms otherwise continue unchanged |
| Warning | A stated instance of conduct | Only the facts the CA gave, with dates, and no characterisation you added |
| Show cause | An allegation requiring a reply | The allegation as given, the reply window as instructed, nothing prejudged |
| Acceptance of resignation | The employee's own letter | Resignation date as the employee wrote it, last working day, notice waived or served |
| Relieving | Last working day passed, clearances done | It confirms release; it does not certify conduct |
| Experience certificate | Employment concluded | Dates and designation only, unless the client asks for more in writing |

Warning, show cause and anything touching termination are the highest-risk drafts here. Reproduce the
client's account of the facts, attribute it to them, use no adjective they did not use, and put the
legal-review flag at the top of the draft, not the bottom.

## Step 4 — house rules for the draft

- Formal Indian professional English. No emoji, no exclamation marks, no cheerful closing lines.
- Letterhead, reference number and date left as placeholders. Address block filled from records.
- Every figure in a letter also exists in a working file, and the two must agree. Amounts in words as
  well as figures where the template does that.
- One acknowledgement copy line where the template has one.
- End the draft with a `[____]` list: every field you could not fill and who has it.
- Save as `<date>_<letter type>_<employee name>.docx` in the client's payroll folder for the FY (for
  example `<Client>/<FY 2026-27>/Payroll/Letters/`). Never overwrite a signed letter. Never rename or
  delete a raw client file.

## Step 5 — confidentiality

Salary, PAN, Aadhaar, bank details, medical facts and anything about conduct stay in the client
folder. Never in a chat summary, never in a message body, never in a WhatsApp message. When telling the
CA a draft is ready, name the file and the letter type and nothing more. Where the firm shares files
through a secure channel, the CA shares the file, not its contents.

A warning, show cause or termination draft goes to the CA only. Do not address it to the employee, do
not draft a covering message to the employee, and do not send anything. Any covering message to the
client is a draft for the CA to send from their own mail (`fortax-client-comms`).

## Hand over

- Which letters were drafted, from which template, for whom, and the file paths.
- The `[____]` list: every term missing, and who must supply it.
- Every item flagged for legal review, at the top, with why.
- **Check before signing**: the employee's name and designation against the personnel record; the
  compensation against the salary structure file; the dates against the joining or resignation
  document; no term present that the CA did not instruct; the signature block and date still blank;
  legal review closed on every flagged item.
