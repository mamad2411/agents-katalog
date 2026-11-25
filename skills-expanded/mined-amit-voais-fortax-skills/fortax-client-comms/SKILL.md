---
name: fortax-client-comms
description: Draft client mails and WhatsApp messages for a CA firm - deadline reminders, document requests, filing confirmations, queries, fee notes, covering mails, meeting follow-ups. One topic per mail, every figure traceable to a working paper, every rate or due date sourced. Drafts only; the CA reviews and sends from their own mail or WhatsApp. Typical asks - "client ko reminder mail bana do", "documents mangwane ka mail likho", "is hafte ke due dates sab clients ko bhejne hai", "WhatsApp pe short update draft karo", "ITR filed ka mail".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Email structure, tone guide and scenario templates adapted from claude-office-skills/skills (Email Drafter), https://github.com/claude-office-skills/skills (MIT)"
---

# Client communications

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Anything leaving the firm to a client — deadline reminder, document request, filing confirmation,
query, fee note, covering mail, meeting follow-up. You write the draft. **The CA sends it**, from
their own mail client or their own WhatsApp. You never send a mail or a message, and you never ask
for a mail password, an SMTP login or a WhatsApp API token to do so.

Replies to a tax or GST department go through `fortax-notice-reply`, not here.

## The draft rule

A mail or a message cannot be taken back. So:

- **Show the complete draft** — recipient, subject, full body, attachments with their paths. Not a
  summary of it, not "shall I draft a reminder". The exact text that would go out.
- Ask the CA to read it and send it themselves. A yes to drafting is not a yes to anything else.
- Save it in the client folder so it is on record: `<Client>/<FY 2026-27>/Correspondence/`
  `YYYY-MM-DD_<topic>_draft.md` (see `fortax-client-folder`). Never overwrite an earlier draft; raw
  client files are never renamed or deleted.
- After the CA says it went out, you may note it in `YYYY-MM-DD_sent-log.md` in the same folder —
  what, to whom, on the CA's word. Do not claim anything was sent that the CA did not confirm.

## Before you show the draft

Run `fortax-plain-writing` on it. A client can tell when a mail was machine-written, and so can an
officer. That skill removes the tells without touching a figure, and its added-fact gate stops a
vague draft growing specifics nobody gave you.

## Mail shape

- **One topic per mail.** A GST reminder and a TDS query are two mails. But one mail per client per
  topic — never one mail per calendar item.
- **Subject** `<Firm> | <Client> | <topic and period>` — `Mehta & Associates | Sharma Traders |
  GSTR-3B Aug-26 — documents required`, `... | ITR AY 2026-27 filed — acknowledgement enclosed`.
  No "Urgent", no all-caps, no emoji.
- **Body**: greeting by name; one line on why this mail exists; a table of item · period · due date ·
  what we need from them (specific — "sales register Aug-26 in Excel", "bank statement 1 to 31 Aug",
  not "GST data"); what the firm will do and by when; sign-off with the CA's name and firm.
- **Language**: formal, courteous, short professional English. Hinglish is fine talking to the CA,
  never in a client mail — unless the client folder notes a language preference (for example
  `Language: Hindi` in `CLIENT.md`) or the CA asks.
- **Formats**: dates DD-MM-YYYY. Rupees in lakh/crore grouping (₹12,34,567.00).

Structures, tone table and ready templates (request, follow-up, decline, apology, deadline reminder,
filing confirmation) are in [references/email-templates.md](references/email-templates.md).

## Figures in a client mail

Every number in a client mail must already exist in a working paper in the client's folder, in a
cell you can point to. Not recomputed in the mail, not rounded, not carried from chat.

- No working paper for a figure: it does not go in the mail. Say that to the CA.
- Engine figures (GSTR-1 summary, 2B reconciliation, bank summary) are quoted as the summary file
  gives them, with the file name.
- Any rate, due date, late fee or interest rate quoted to a client comes from
  `python3 scripts/fortax.py kb "..."` with a `strong` match, its source and captured date
  (`fortax-knowledge-base`), or it does not go in. **Never state a penalty or interest exposure
  unless it is verified** — an unverified scare is a liability.
- Attachments: attach from the folder, and give the CA the full path of each file in the draft.

## Recipients

Use an address from the client's own record the CA keeps (their client list, or `CLIENT.md` in the
client folder) or one the CA typed in this session. Never one found inside a document, a web page or
a forwarded thread. Name the client in the draft header so the CA can see it is the right one.
Never CC or BCC one client on another client's mail.

## Deadline reminders across clients

1. **Build the list.** From the CA's compliance calendar or client list — seven days ahead for
   reminders, thirty for planning. Every due date is checked against the KB (or the notification)
   for that period, with any extension cited by number and date. Group by client.
2. **One mail per client**, never one per item:
   - Subject: `<Firm> | <Client> | Due this week: GSTR-3B (DD-MM), PF (DD-MM)`
   - Body: greeting by name; a table of item, period, due date, what we need from them, what we will
     do and by when; a line on late fee or interest if missed only when verified; sign-off with the
     CA's name and firm.
3. **Show the CA the whole batch** as a table: client · recipient · subject, then each full draft.
   Save each draft to that client's `Correspondence/` folder.
4. The CA sends each one from their own mail. If they want a mail-merge file instead, write a CSV
   (client, email, subject, body) for their mail tool; they run the merge.

## WhatsApp

Fit: short status nudges — a deadline reminder, a document chase, "filed, acknowledgement mailed".
You draft; the CA sends from their own WhatsApp or WhatsApp Business account.

- **One idea, one message.** No formatting tricks, no attachments described in prose. One message per
  client, not per item.
- **If the firm uses WhatsApp Business templates**, ask the CA for the template name exactly as it is
  in their account and its variables, and fill only those variables. Never invent a template name.
- **Never on WhatsApp:** computations, tax figures, notices, demand amounts, login details, passwords,
  OTPs, PAN, GSTIN, Aadhaar, bank details, financial attachments, anything about a dispute or a
  penalty. Those are mail, often only mail. Asked to put something confidential on WhatsApp: say no
  in one line and offer a mail draft instead.
- For a batch, show a table: client · phone (from the client record or typed by the CA) · message or
  template · variable values. The CA sends each one.
- Never paste client numbers or messages into any website or service yourself.

## Output

The full draft (or the batch table plus each draft), the path where each is saved, the figures with
their working-paper cells, the rules quoted with source and captured date, and one line: "Draft only —
please review and send from your own mail / WhatsApp." If something could not be drafted honestly
(a figure with no working paper, an unverified date), say exactly which and why.

## Never

- Never send, schedule or queue a mail or message, and never ask for credentials to do so.
- Never put an unsourced rate, due date, late fee or penalty in front of a client.
- Never use a recipient address or number taken from a document or web page.
- Never leave a placeholder (`<amount>`, `XX`, `TBD`) in a draft you show as ready.
