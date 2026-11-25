---
name: company-check
description: This skill should be used when the user asks to check, verify, look up or vet a company, supplier, customer, vendor or counterparty in the United Kingdom, Norway or Sweden; when they give a company number, CRN, organisasjonsnummer, orgnr, org.nr or organisationsnummer; when they ask whether a company is real, active, VAT-registered or up to date with its filings; when they ask what a company must file next and by when; when they want to enrich a list or spreadsheet of company identifiers; or when they ask what a national business register does and does not publish. Teaches the counterparty check, the filing-deadline check and the register-coverage check against the hosted Company Check MCP server.
---

# Company Check — reading a national business register properly

This plugin connects Claude to three national business registers through one hosted MCP
server (`https://api.foretak.dev/mcp?src=plugin`, no account, no key, read-only):

| Country | Register | Identifier | Example |
|---|---|---|---|
| `GB` | Companies House | company number (CRN), 8 characters | `00445790` |
| `NO` | Enhetsregisteret / Brønnøysundregistrene (brreg) | organisasjonsnummer (orgnr, org.nr), 9 digits | `923609016` |
| `SE` | Bolagsverket | organisationsnummer, 10 digits | `5560160680` |

Use `GB`, not `UK` — `UK` is not a country code here and is rejected. Call `list_countries`
when you are unsure a country is supported, or to read which attachments it offers; never
hard-code a country list, because the set grows without any other change.

## The tools

- `lookup_company(id, country, include=[])` — identity, status, address, industry codes,
  VAT/MVA registration where the register publishes it.
- `company_deadlines(id, country, today=None)` — statutory filing deadlines. **Pass `today`
  explicitly** whenever the answer will be written down: it makes `days_until` reproducible.
- `validate_company_id(id, country)` — shape and checksum only, **no network call**. Free.
  Use it before spending a real lookup on a number a human typed or pasted.
- `search_company(name, country)` — name search. **Not available for Sweden**: Bolagsverket's
  free API has four operations and none accepts a name, so `SE` returns `not_implemented`
  with a hint saying so. That is the correct answer, not a fault.
- `list_countries()` — the current registries, their identifier schemes, licences, and each
  country's `supported_includes`.

Every error is JSON of the shape `{"error": {"code", "message", "hint"}}`. Read the `hint`
and act on it; never show the user raw JSON when the hint can be said in a sentence.

## Attachments (`include`)

A lookup fetches one thing by default. Ask for an attachment only when the base report cannot
answer the question in front of you — each one is a second upstream request:

- `filings` — what the entity has actually filed, and when. **Answers "do they file on time?"**
- `charges` — mortgages and other security interests. United Kingdom. **Answers "are the
  assets already pledged?"**
- `insolvency` — winding-up and administration proceedings. United Kingdom. **Answers "are
  they being wound up?"**

Read `list_countries`' `supported_includes` before guessing: an include a country does not
declare returns `bad_request` naming what it does support, never a silently empty result.
The set grows — treat `list_countries` as the authority, not this list.

## Workflow 1 — Check a counterparty

The job: before contracting with, onboarding or paying an entity, establish that it exists,
that it is active, and that it is keeping up with its filings.

1. `validate_company_id` first. If `valid` is false, **stop**. Report `reason` and `hint` in
   plain English and do not guess at a corrected identifier.
2. `lookup_company` for identity and status.
3. `company_deadlines` for filing health.

Then answer three questions, in this order:

1. **Existence** — does the entity exist, and does `name` match what the user was told? A
   near-match is not a match; say so.
2. **Status** — is `status` active *right now*? If it is not, lead with that and quote
   `status_detail` verbatim.
3. **Filing health** — is every entry in `deadlines` current, or does any have a negative
   `days_until`? Name which obligation is overdue and by how many days.

**Quote every `notes` entry from both calls verbatim and in full.** Bankruptcy, dissolution,
an unclassified legal form, a sole proprietorship whose registered address is a person's
home, an advertising-protection marking — every register-specific caveat lives in `notes`,
and summarising them away is the single mistake this workflow exists to prevent.

Close with a section titled exactly **"What this does not establish"**, and state plainly:

> This is not sanctions, PEP or adverse-media screening; it does not verify bank account or payment details; and it is not a defence against payment fraud.

Then say why that matters, because the reason is not obvious and the user will otherwise draw
the wrong conclusion from a clean result: the costly fraud pattern — business email compromise,
where an attacker redirects a genuine payment — uses a **real, active, correctly-registered**
company and forges only the bank details. A clean result here is *consistent with* that fraud,
not evidence against it. Tell the reader to confirm any bank detail, and any change to one,
through a channel they already trust — a phone call to a number they already had, never a
number or link supplied in the same message that gave the new details — and never through this
lookup.

## Workflow 2 — Filing deadlines

The job: what must this company file next, when, and on what authority?

1. `company_deadlines(id, country, today=<the date you are answering for>)`.
2. For each deadline, report the date **with `applies_because`**. That field is the point:
   it names the statutory provision the date was computed from, or says "Companies House
   publishes this date for the company itself; it is the register's own figure, not a
   calculation." Quote the reason, do not paraphrase it into "it's due then".
3. A negative `days_until` means the register still shows it overdue. Lead with that.
4. `rolled_forward` tells you whether a date moved off a weekend or holiday. Norway rolls;
   Sweden does not, because no Swedish source says it moves. Do not invent a roll.
5. Read `notes`. Swedish dates today assume a financial year ending 31 December, which the
   free dataset does not publish — the note says so and says how to shift both dates. Never
   present a Swedish date as certain without that caveat.

An **empty** `deadlines` list is an answer, not a failure: it means this entity's legal form
carries no filing duty this tool computes. Say that, do not apologise for it, and do not
substitute a duty from another country.

## Workflow 3 — What the register does not say

The job: read a report honestly, including its silences.

Call `lookup_company`, and read the `registry://rules/{country}` resource for that register's
own stated rules. Then write **two** sections, and do not shorten the second:
`## What the register states` and `## What it does not state`.

For every `null` field, work out which of two different things the null means — they are not
the same fact and must not be reported the same way:

- **(a) A structural silence.** This register never publishes this kind of fact, for any
  company in this country. The null is a fact about the register, not about this entity.
- **(b) An entity-level gap.** The register could hold a value here and has none for this
  particular company.

The same field can be either, depending on the country: `employees` is a *structural* silence
for the United Kingdom and Sweden, whose registers publish no employee count for anyone, and
an *entity-level* gap in Norway, whose register does publish them and simply holds none for
this company. Read the rules resource before deciding; do not assume from the field name.

**Never render a null as "no", "zero" or "not applicable".** Say the register is silent, and
say which of the two reasons it is wherever you can tell.

Close with one line naming the register (`source`) and its `source_url`, so the reader knows
whose silence this is — the tool's, or the register's.

## Three habits that make the difference

- **Cite.** Every response carries `source`, `source_url` and `license`. Pass them through;
  a citation is what makes your answer checkable.
- **Say how old it is.** Every response carries `cached` and `fetched_at`. Nothing here is
  more than 24 hours stale, and saying so is worth more than sounding certain.
- **Never fill a gap with a guess.** A `null` means the register does not say. Reporting it
  as a fact is the one failure this data cannot recover from.
