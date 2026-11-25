---
name: fortax-legal-brief
description: Prepare a legal briefing for a CA firm or its client from the client folder (and mail/calendar if connected) — a daily list of legal items needing attention, a topic brief, an incident brief (legal notice, data breach, raid, dispute), a meeting brief for a negotiation, board or regulator meeting with action-item tracking, or a vendor agreement status with gaps and expiry dates. Use for "aaj legal me kya pending hai", "is vendor ke saath kya agreements hain", "board meeting ki taiyari", "legal notice aaya hai, brief bana do", "meeting ke action items track karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/brief (Apache-2.0); https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/meeting-briefing (Apache-2.0); https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/vendor-check (Apache-2.0)"
---

# Legal brief

Typical asks: "daily legal brief", "GST notice aur vendor disputes ka status do", "Kapoor Logistics ke saath
kaunse agreements hain", "kal CFO ke saath negotiation hai, brief bana do", "data leak hua hai, turant brief".

Five modes. If the CA does not say which, ask.

| Mode | For | Section |
|---|---|---|
| `daily` | Start-of-day list of legal items needing attention | 1 |
| `topic` | What the firm or client already knows and holds on one legal question | 2 |
| `incident` | A developing situation: legal notice, breach, search, dispute | 3 |
| `meeting` | Prep for a meeting with legal stakes, and its action items | 4 |
| `vendor` | Every agreement the client has with one vendor, dates and gaps | 5 |

This is not legal advice. A brief collects and orders what is in the sources; it is reviewed before anyone
relies on it.

## Sources — what to read and how to say what was not read

Work from what you can actually open:

- **Client folder** — agreements, notices, orders, board minutes, correspondence, the compliance
  calendar, earlier briefs and reviews. Always available; read the files.
- **Mail, calendar, chat, document storage** — only if the CA has connected such a tool to you. Search;
  never send.
- **A portal or site open in the browser** — through your browser tool (Claude in Chrome, a
  Playwright/browser MCP, or the Codex browser); if you have none, give the CA the click path.
- **The CA** — ask for what is not in any source.

Every brief ends with **Sources checked / not available**. A gap stated plainly is better than a brief that
looks complete and is not. Link or name the file rather than reproducing it.

## 1. Daily brief

Scan for:

- **Folder and mail:** new contract or review requests, compliance questions, replies from counterparties
  on live negotiations, legal notices, summons, show-cause notices and orders (tax notices: route to
  `fortax-notice-reply`), advocate correspondence, regulatory update newsletters.
- **Calendar:** today's meetings needing legal prep (board meetings, deal reviews, vendor calls, hearings),
  deadlines this week (contract expiries, renewal notice windows, reply dates, hearing dates, statutory
  filings).
- **Chat:** requests for legal input, escalations, mentions of contract, notice, NDA, privacy, compliance.
- **Agreements register:** contracts awaiting review or signature, expiries in the next 30 days, newly
  executed agreements not yet filed or stamped.

```
Daily legal brief — <date>

Urgent / action required
<sorted by deadline; each with its next step>

Contract pipeline
- Awaiting review: <count, list>
- Awaiting counterparty: <count, list>
- Deadlines this week: <items>

New requests
<reviews, NDAs, compliance questions since the last brief>

Today's meetings
<meeting — prep needed>

Notices and hearings
<authority, reference, reply/hearing date, status>

This week's deadlines
<date — item — owner>

Sources checked / not available
```

Keep it short; every item has a next step or a reason to be there. Learn over time what the CA wants
filtered out.

## 2. Topic brief

1. Take the question in specific words.
2. Search the sources: internal memos, earlier opinions and reviews, playbooks, precedent agreements and
   clauses, mail and chat on the topic.
3. Write it up:

```
Topic brief — <topic>

Summary        <2-3 sentences>
Background     <history from the sources>
Current state  <the client's or firm's present position or practice, per the documents>
Key considerations  <factors, risks, open questions>
Internal precedent  <earlier decisions, memos, positions — with file names>
Gaps           <what is missing, what was not searched>
Next steps     <what the CA should do with it>
Sources checked / not available
```

A topic brief is not legal research. If the question needs current law or case law, say so and use
`fortax-deep-research` (statute, notification, and judgments from SCC Online, Manupatra, Indian Kanoon or
the court's own site, each cited) or recommend an advocate. Never state a holding from memory.

## 3. Incident brief

For a legal notice, litigation threat, departmental search or summons, data breach, IP dispute, employee
complaint or regulator inquiry.

1. Take the description.
2. Scan quickly: mail and chat about it, relevant policies and response plans, insurance policies,
   response meetings on the calendar, contracts affected (indemnities, notice clauses, insurance
   requirements).
3. Produce the brief **fast with what is known**; do not wait for complete information.

```
Incident brief — <topic>
Prepared: <date, time>     Severity: <if determinable, per fortax-legal-compliance-check>

Situation summary
Timeline                <dated, from the sources>
Immediate legal considerations
  - Statutory notices and deadlines (look each up; see below)
  - Preservation: stop routine deletion of relevant mail, chats, files and devices now
  - Confidentiality: route legal analysis through the advocate; keep the circle small
Relevant agreements     <contracts, insurance policies, and their notice clauses and time limits>
Response so far         <what has already been done>
Key contacts            <internal and external, from the sources>
Immediate actions
  1. <most urgent>
  2. …
Information gaps
Sources checked / not available
```

Deadlines that commonly run from the incident — look each up and quote the source, or mark "confirm":
DPDP Act, 2023 and DPDP Rules intimation to the Data Protection Board and affected data principals (see
`fortax-india-dpdp-act`); CERT-In reporting of cyber incidents under its directions under the IT Act; SEBI
LODR disclosure for a listed company; insurer notice under the policy; contractual breach-notice clauses;
reply dates in a legal notice or show-cause notice; GDPR's 72 hours only if EU personal data is involved.

Recommend an advocate for anything significant. Preservation notices and holding replies are drafted with
`fortax-legal-response`.

## 4. Meeting brief

### Identify the meeting
Title and type; participants and what each wants; agenda; the CA's role (adviser, presenter, negotiator,
observer); how much time there is to prepare.

### What to prepare, by type

| Meeting type | Key prep |
|---|---|
| Deal review | Contract status, open issues, counterparty history, negotiation strategy, approvals needed |
| Board / committee | Legal and compliance update, top risks, pending matters, regulatory changes, draft resolutions, notice/agenda/quorum per the Companies Act and Secretarial Standard SS-1 (confirm periods) |
| Vendor call | Agreement status (Section 5), open issues, performance, relationship history, objectives |
| Internal sync | Workload, priority matters, deadlines |
| Client / customer | Agreement terms, open issues, relationship context |
| Regulator / department | Matter background, compliance status, earlier submissions and correspondence, the advocate's briefing, what not to say |
| Litigation / dispute | Case status, recent orders, strategy, settlement range |
| Cross-functional | Legal effect of a business decision, risk rating, compliance needs |

### Gather context
Calendar (details, earlier meetings with the same people in the last 3 months, follow-ups); mail and chat
(recent threads, open action items, shared documents); client folder (agendas, earlier minutes, agreements,
memos, drafts); the agreements register (contracts with the counterparty, amendments, renewals).

### Write the brief
Use the template and the type-specific additions in `references/meeting-brief-template.md`. Flag
**preparation gaps**: sources not available, information that looks out of date, unanswered questions,
documents not found.

### Action items
During or after the meeting:

```
Action items — <meeting> — <date>
| # | Action | Owner (one person) | Deadline (a date) | Priority H/M/L | Type | Status |
```

- Specific: "Send redline of clause 4.2 to the counterparty's advocate", not "follow up on contract".
- One owner, never a team. A date, never "soon". Note dependencies.
- Type: firm action / client management action / counterparty or advocate action / meeting to schedule.

After the meeting: draft the action-item mail for the CA to send; list calendar reminders to set; update
the agreements register and risk register; file the notes in the client folder; flag anything urgent.
Tracking: High daily until done; Medium at the weekly review; Low at the next meeting; overdue items raised
with the owner and at the next meeting.

## 5. Vendor agreement status

### Identify the vendor
Legal name vs trade name ("Kapoor Logistics Pvt Ltd" vs "KapoorLog"), abbreviations, group companies.
Match by PAN or GSTIN where the folder has it. If ambiguous, or a group, ask whether to check one entity or
the group.

### Search
Client folder and agreements register first: active agreements, expired ones (last 3 years), drafts in
negotiation or awaiting signature, amendments and addenda. Then mail (last 6 months: agreement
attachments, negotiation threads), chat (last 3 months), document storage, and the purchase ledger or
vendor master if the CA provides it (to confirm the relationship is live).

### For each agreement

| Field | Details |
|---|---|
| Type | NDA, MSA, SOW/PO terms, DPA / processor contract, SLA, licence, lease, other |
| Status | Active / Expired / In negotiation / Awaiting signature |
| Effective date | |
| Expiry | And auto-renewal: yes/no, renewal term, notice period and the last date to give notice |
| Key terms | Liability cap, governing law and forum, termination, payment terms |
| Stamped / registered | As seen on the copy |
| Amendments | On file |
| Location | File path of the executed copy |

### Gap analysis

```
Agreement coverage — <vendor>
[FOUND/MISSING] NDA
[FOUND/MISSING] Master / service agreement
[FOUND/MISSING] SOW or PO terms
[FOUND/MISSING] SLA
[FOUND/MISSING] Data processing contract (needed if the vendor handles personal data — DPDP Act)
[FOUND/MISSING] Insurance certificate (if the contract requires one)
[FOUND/MISSING] Vendor KYC: PAN, GSTIN certificate, Udyam certificate (MSME payment terms), bank details
[FOUND/MISSING] Foreign vendor: TRC, Form 10F, no-PE declaration (withholding and DTAA)
```

Flag gaps the relationship needs (an MSA but no data processing contract when the vendor handles personal
data). Flag expired agreements with surviving obligations (confidentiality, indemnity). Put anything
expiring or with a notice window inside 90 days at the top.

```
Vendor agreement status — <vendor legal name>
Search date: <date>
Sources checked: <list>     Not available: <list, with what the CA should search, e.g. "<vendor> agreement" in mail>

Relationship: <vendor / partner / customer>, <PAN / GSTIN if known>

Agreements
### <Type> — <Status>
- Effective <date>; expires <date> (<auto-renews / does not>; notice by <date>)
- Key terms: <summary>
- Copy: <path>

Gap analysis
Upcoming actions    <expiries, notice dates, missing agreements, amendments needed>
Notes               <context from mail/chat>
```

If nothing is found anywhere, say so plainly and ask where else agreements are kept.

## Rules

- **Read-only.** Nothing is sent, filed, signed or replied to. Drafts go to the CA.
- **No dates or periods from memory.** Statutory periods are looked up or marked "confirm" with the law
  named; contract dates come from the document with its clause number.
- **No case law from memory.**
- **Made-up names in examples only**; the brief itself uses the client's real records from the folder and
  stays in the client folder: `YYYY-MM-DD_<mode>_<subject>_brief.md`.

---

Credits: the daily, topic and incident modes are adapted from `brief`, the meeting brief and action-item
tracking from `meeting-briefing`, and the vendor agreement status from `vendor-check`, all in
[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), © Anthropic,
Apache License 2.0 (`LICENSE-THIRD-PARTY-knowledge-work-plugins.txt`).

Changes by Fortax: adapted for Indian law and CA practice, merged with meeting-briefing and vendor-check
(knowledge-work-plugins); sources rewritten around the client folder with connectors optional; added Indian
incident deadlines (DPDP, CERT-In, SEBI LODR), board-meeting and vendor KYC/withholding checks; US research
platforms replaced with cited Indian sources; nothing is sent.
