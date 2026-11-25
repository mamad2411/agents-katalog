---
name: fortax-deep-research
description: Research an Indian tax, GST, company-law or labour-law question from the statute, notifications, circulars and rulings, with a short answer, confidence, authority table and sources. Also finds and weighs case law (ITAT, High Court, Supreme Court, AAR/AAAR) and sweeps new CBIC, CBDT, MCA, EPFO and ESIC circulars and notifications for a client list. Typical asks - "is par research karo", "koi judgment hai 194J vs 194C par", "43B(h) ka latest circular", "is mahine kya naye notifications aaye", "advance ruling milegi kya".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Deep research, case law and circular tracking

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Three jobs share one discipline: read the primary text in this session, cite it by number and date,
and never present commentary as law. For a long, multi-source report with a citation registry and
counter-review, use `fortax-research-citations` on top of this.

## 1. Frame the question (write it down first)

- The exact question, the client fact pattern (entity type, turnover, state, dates, amounts), and
  the decision it drives.
- What would change the answer: thresholds, dates of applicability, old or new regime, notifications
  issued after a date, which Act applies to the period (Income-tax Act, 1961 or the Income-tax Act,
  2025, as applicable to the tax year).
- Start a note in the client folder (`<Client>/<FY 2026-27>/<area>/`) or the firm's research folder,
  named `YYYY-MM-DD_<slug>.md`, with sections:
  Question · Facts · Short answer · Authority · Analysis · Open points · Sources.

## 2. Source hierarchy (search in this order, stop when settled)

1. **Statute and rules** — Income-tax Act and Rules, CGST Act and Rules (and the state SGST Act where
   relevant), IGST Act, Companies Act 2013 and rules, LLP Act, EPF and ESI Acts. Text at
   `indiacode.nic.in`, `cbic-gst.gov.in`, `incometaxindia.gov.in` / `incometax.gov.in` (Acts and
   Rules), `mca.gov.in`.
2. **Delegated law** — notifications, circulars, orders, instructions: CBIC (`cbic-gst.gov.in`,
   `cbic.gov.in`), CBDT (income-tax portal, Notifications/Circulars), MCA (Notifications), EPFO and
   ESIC circulars.
3. **Fortax knowledge base** — `python3 scripts/fortax.py kb "..."` returns sourced facts with a
   source URL and a captured date. Prefer it for due dates, fees and thresholds. Only a `strong`
   match counts; `weak` or `none` sends you back to the primary text. See `fortax-knowledge-base`.
4. **Portal FAQs, user manuals, advisories** — GST portal news and updates, e-invoice portal,
   TRACES, MCA e-form help.
5. **Professional guidance** — ICAI guidance notes, technical guides, FAQs (`icai.org`).
6. **Case law** — only when statute and circulars leave real ambiguity. See section 6.
7. **Secondary commentary** (tax news sites, blogs, software vendors' guides) only to locate primary
   sources. Never cite them as authority.

## 3. Finding the page

Knowing the hierarchy is useless if you cannot find the document. Three ways, in order:

1. **The KB first.** If a `strong` match settles the question, cite it and stop — no browsing
   needed.
2. **Search, then read.** Use your web search tool, or open a search engine in your browser tool.
   Search the way the document is titled, not the way the question was asked:
   `site:incometaxindia.gov.in circular 43B(h)`, `"notification no" CGST rule 42 2024`,
   `ITAT order section 194J professional technical`.
3. **Fetch the page you found.** A web-fetch tool reads a public page directly and is the fastest way
   to get the text of a circular, a judgment or an Act section once you have its URL.

Do not guess URLs. A government portal's own search box is usually worse than a search engine, and
clicking blindly through a home page wastes the CA's time — three failed clicks means go back to
search.

**When a host will not load or is blocked**, try the fetch tool instead, or tell the CA the host and
ask them to open it. A blocked domain is never a reason to answer from memory.

Keep each page's URL and the date you read it. Every one goes in the Sources block.

## 4. Reading discipline

- Quote the operative words of a section or notification, with section, sub-section, clause and
  proviso, and the notification or circular number and date.
- Check the **applicability date** and whether it was later amended, substituted or omitted (search
  "as amended", "substituted by", "omitted by").
- For GST, check both the CGST and the state's SGST position where relevant; for rates, check the
  schedule entry and the HSN/SAC.
- Note the **date of your research**. Anything can change with the next Finance Act or notification;
  say which year a rule is for.

## 5. Output (in the note and in chat)

- **Short answer** in three lines, with confidence:
  High (statute clear) / Medium (circular-based or interpretation) / Low (conflicting rulings, no
  clear text).
- **Authority table**: source · what it says · effective from · link.
- **Analysis**: apply to the client facts; show the computation if money is involved (in a
  spreadsheet or script, not mental arithmetic — see `fortax-evidence-discipline`).
- **Open points**: what to confirm with the partner or the department; whether to seek an advance
  ruling.
- **Sources**: full list with the date each was read.

## 6. Case-law research

1. **Issue statement** — one sentence, with the section and the disputed words.
2. **Where to look** — `itat.gov.in` (orders), High Court and Supreme Court judgment portals, GST
   AAR/AAAR orders on `gst.gov.in` and state AAR pages, CBIC/CBDT circulars that accept or contest a
   ruling; the Fortax KB for rulings already captured. Commentary sites only to find citations —
   then open the order itself.
3. **For each ruling record** — court/bench, case name, citation or order number, date, facts in two
   lines, the ratio (the actual reasoning, not the headnote), outcome, and whether it was later
   followed, distinguished, reversed or is pending in SLP.
4. **Weigh it** — the jurisdictional High Court binds the assessing officer in that state; the
   Supreme Court binds all; ITAT and AAR orders are persuasive, and an AAR ruling binds only the
   applicant (and its jurisdictional officer). Note conflicting High Court views and whether a
   CBDT/CBIC circular directs officers.
5. **Output** `YYYY-MM-DD_caselaw_<slug>.md`: issue → table of rulings → weight analysis → how to
   plead it (a paragraph the CA can lift into a reply, see `fortax-notice-reply`) → risks.

Never invent a citation. If you cannot open the order text, list it as "to verify" and do not quote
it.

## 7. Circular and notification tracker

1. **Window** — the last 30 days by default, or the period the CA names.
2. **Sources to sweep** — fetch the index pages, then each item:
   - CBIC GST: notifications (central tax, central tax rate, integrated tax), circulars, press
     releases; GST portal "News and updates" and advisories.
   - CBDT: notifications, circulars, press releases; income-tax portal latest updates.
   - MCA: notifications, circulars, "What's new"; e-form version changes.
   - EPFO and ESIC circulars; state professional tax and labour department notices for the client's
     state.
   - The Fortax KB (`kb "notification <topic>"`, `kb "extension <form>"`, `kb "circular <topic>"`)
     for items already captured.
3. **For each item capture** — number, date, subject, effective date, what changed (one line), who
   is affected (turnover, entity type, state, filer type), action needed, deadline.
4. **Client impact** — go through the CA's client list (their spreadsheet, or each client's
   `CLIENT.md` in the client folders, see `fortax-client-folder`). Tag each client an item touches
   and propose the concrete action, for example: "Sharma Traders: QRMP filer, IFF window extended —
   confirm the new date on the notification before telling the client."
5. **Output** `YYYY-MM-DD_updates_<period>.md` with the table, plus, if asked, a short client-facing
   summary drafted with `fortax-client-comms` for the CA to send.

Mark anything you could not open or verify as "unverified" instead of paraphrasing from a headline.

## Never

- Never cite a section number, notification number or ruling you did not read in this session or
  get from a `strong` KB match.
- Never present commentary as law. Never say "as per the latest circular" without its number and
  date.
- Never fill a gap with a remembered figure. `[UNVERIFIED — confirm on portal]` and where to look.
