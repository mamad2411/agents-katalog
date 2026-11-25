---
name: discovery-prep
description: >
  Prepare a discovery list and affidavit of documents under the Rules of the
  High Court (Cap 4A, O.24) or Rules of the District Court (Cap 336H, O.24).
  Guides document identification, privilege review, list preparation, and
  affidavit drafting.
argument-hint: "[describe the case, parties, and document categories]"
---

# /litigation-legal:discovery-prep

1. Load `CLAUDE.md` for the discovery framework (RHC O.24 / RDC O.24).
2. Gather matter context: parties, pleadings, case summary, document categories.
3. Walk the preparation checklist below.
4. Produce a draft discovery list and affidavit of documents.

## Discovery Framework (RHC O.24)

### Standard Discovery (O.24, r.1)

Each party discloses documents that are or have been in their control and which:
- The party relies upon; OR
- May adversely affect the party's own case; OR
- May adversely affect another party's case; OR
- May support another party's case.

**The Peruvian Guano test (Compagnie Financière et Commerciale du Pacifique v Peruvian Guano Co (1882)):** A document is discoverable if it contains information that may directly or indirectly advance a party's case or damage another party's case, or which may lead to a train of inquiry that would do either.

### Specific Discovery (O.24, r.7)

If standard discovery is inadequate, apply by summons for specific discovery of:
- Particular documents or classes of documents
- Documents relating to a particular issue

### Pre-action Discovery (O.24, r.7A)

Limited to:
- Personal injury / fatal accident claims
- Applicants must show a potential claim exists
- Discovery limited to specific documents

### Discovery Against Non-parties (O.24, r.7A — limited scope)

## Preparation Checklist

### 1. Identify Document Sources

- [ ] Email accounts / archives
- [ ] Document management systems
- [ ] Shared drives and local files
- [ ] Messaging platforms (Slack, Teams, etc.)
- [ ] Cloud storage (Google Drive, SharePoint, Box)
- [ ] Mobile devices
- [ ] Third-party custodians (consultants, agents, subcontractors)
- [ ] Financial systems and accounting records

### 2. Document Collection

- [ ] Define the search scope by date range, custodians, and keywords
- [ ] Preserve originals (forensic copy if necessary)
- [ ] Collect all responsive documents
- [ ] Document the collection methodology

### 3. Privilege Review

**Categories of privilege:**
- [ ] Legal advice privilege — communications with solicitors for the dominant purpose of legal advice
- [ ] Litigation privilege — communications (including third parties) for the dominant purpose of pending/reasonably contemplated litigation
- [ ] Without prejudice privilege — settlement communications

**Privilege review process:**
- [ ] Review each document for privilege
- [ ] Record privilege claims in a privilege log (document, date, author, privilege type, basis)
- [ ] Ensure privilege is not inadvertently waived
- [ ] Redact privileged portions (redaction must be minimal and justified)

### 4. Discovery List (RHC O.24, Schedule 1)

Organise documents into parts:

**Part 1:** Documents in the party's control (list individually or by class).
**Part 2:** Documents that were but are no longer in the party's control (state when and what happened).
**Part 3:** Documents for which privilege is claimed (list individually; state the nature of the privilege).

### 5. Affidavit of Documents (O.24, r.6)

The affidavit must:
- [ ] Identify the discovery list
- [ ] Verify that the list is complete
- [ ] State the location of documents
- [ ] Specify when documents left the party's control (if applicable)
- [ ] State that a reasonable search has been conducted
- [ ] Describe the scope of the search (custodians, date range, keywords)

**Model affidavit template (O.24, r.6, Form 11):**

> I, [name], of [address], make oath and say as follows:
>
> 1. I am [the defendant / a solicitor / controller of documents].
> 2. I have conducted a reasonable search for documents within my control relevant to the matters in question in this action.
> 3. The search covered: [custodians], [date range], [keywords].
> 4. The documents I have, or have had, in my control are set out in the List of Documents exhibited hereto.
> 5. I have not been able to locate the documents in Part 2 of the List because [reason].
> 6. I object to produce the documents in Part 3 of the List on the ground that they are privileged: [specify privilege].
> 7. I have disclosed all documents of which I am aware that fall within the scope of discovery as defined by O.24, r.1.
>
> Sworn this [date] day of [month], [year].

### 6. Inspection (O.24, r.9)

- Documents in Parts 1 and 2 are available for inspection.
- Documents in Part 3 (privileged) are not available — privilege log provided.
- Inspection by appointment or electronic copy.

## Output

### Draft Discovery List

| Part | Document description | Date(s) | Author(s) | Notes |
|---|---|---|---|---|
| 1 | [Description] | [Date range] | [Names] | [Available] |
| 2 | [Description] | [Date] | [Name] | [Left control — explain] |
| 3 | [Description] | [Date] | [Name] | [Privilege claimed — type] |

### Privilege Log

| Doc ID | Date | Author | Recipients | Privilege | Basis |
|---|---|---|---|---|---|
| D001 | [Date] | [Name] | [Names] | Legal advice | Legal advice sought from external solicitors |

### Affidavit of Documents

Draft affidavit text ready for swearing.

**Append:** `⚠️ This is a draft for review. Ensure all documents have been properly reviewed for privilege before the affidavit is sworn. Verify that the search scope was adequate.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
