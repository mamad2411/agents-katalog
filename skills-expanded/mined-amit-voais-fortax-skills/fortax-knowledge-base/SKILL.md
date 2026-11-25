---
name: fortax-knowledge-base
description: Look up any Indian compliance fact (GST, income tax, TDS, MCA, PF/ESI due date, rate, threshold, slab, late fee, penalty, form, section, notification) in Fortax's sourced knowledge base before answering, then shape the answer verdict first, workings, rule and source with the captured date. Use it even when you think you know the answer. Typical asks - "GSTR-3B kab tak file karni hai", "234F late fee kitni hai", "GST registration threshold kya hai", "TDS rate on rent", "AOC-4 due date".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Knowledge base and the answer shape

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

The CA or their client will act on what you say. A wrong due date costs a late fee, a wrong
threshold costs a wrong registration, and a made-up section number costs credibility the moment a
CA reads it. The bar is "checkable", not "confident". See `fortax-evidence-discipline` for the
full rule set; this skill is where every time-sensitive fact is looked up and how the answer is
laid out.

## When to use

Before answering anything time-sensitive: a due date, rate, threshold, slab, limit, late fee,
penalty, interest rate, form number, section, rule, notification or circular number, an eligibility
condition, or a portal fee. The knowledge base (KB) is where you look first, including when you
are sure you already know the answer.

The user usually asked about a filing, a deadline, a registration, a penalty or a process, is mid
task and slightly worried. Give them the thing they need first.

## Order of lookup

1. **The Fortax KB** — `python3 scripts/fortax.py kb "..."`. Each fact carries its source URL and
   the date it was captured.
2. **The official portal or notification, read in this session** — when the KB returns `weak` or
   `none`, or the fact is too old to act on. Open it in your browser tool (Claude in Chrome, a
   Playwright/browser MCP, or the Codex browser) or fetch the page; if you have none, tell the CA
   exactly which page to open. See `fortax-deep-research` for finding the page.
3. **A statute you can quote verbatim.**
4. **Nothing.** Write `[UNVERIFIED — confirm on portal]` and say exactly where the CA can check.

Your own recollection is never one of these. It only tells you what to search for.

## Running the lookup

```bash
python3 scripts/fortax.py kb "GSTR-3B due date monthly filer" --topics gst
python3 scripts/fortax.py kb "GST registration threshold goods special category state" --topics gst
python3 scripts/fortax.py kb "section 234F late filing fee ITR" --topics itr
python3 scripts/fortax.py kb "TDS rate section 194I rent" --topics tds
python3 scripts/fortax.py kb "AOC-4 due date" --topics mca
```

`--topics` is optional, a comma list such as `gst,itr,tds,mca,pf,esi`. The reply is JSON:

```json
{"has": true, "match": "strong",
 "facts": [{"heading": "...", "fact": "...", "form": "...", "effective": "...",
            "due": "...", "source": "https://...", "captured": "YYYY-MM-DD"}]}
```

- `match: strong` — the facts answer the query. Still read them (below) before using one.
- `match: weak` or `none` — **do not answer from memory as though sourced.** Go to step 2 of the
  lookup order. Say in one line that the KB had nothing firm.

### How to search

Search the way the rule is named, not the way the CA phrased it. One concept per query.

Nothing back? Try the form number alone (`kb "GSTR-9C"`), then the section number, then the portal
name. Two empty searches is enough — go to the portal, do not rephrase a third time.

## Read the fact, not the heading

A KB `heading` is a label. The `fact` text, with `effective`, `form` and `due`, is the fact.

- Read the `fact` and check it says what the heading claims.
- Check it covers your period. Fix the FY and AY (or the tax period) first. A rate for FY 2025-26 is
  not evidence for FY 2026-27. Use `effective` to see from when it applies.
- Check the qualifiers inside the fact — turnover slab, state, filer type (monthly, QRMP), opt-in
  scheme, composition, first year, non-resident, new or old regime. If the client does not clearly
  fall inside them, the fact does not apply, and you say so.
- The fact does not support the heading, or two facts disagree: show both, say which source is more
  official (government portal beats registry mirror beats anything else), and stop. A clash is a
  question for the CA, not a coin flip.

## Staleness

Compute the age from `captured` to today and say it before the CA acts, not in a footnote. Rates
drift slowly; due dates get extended by notification at short notice.

- Older than about a month, or the due date is close: say the age and point at the portal.
  > Heads up — ye due date mere paas 41 din purani hai. Filing se pehle gst.gov.in par
  > notifications section me confirm kar lena.
- Due within days, or an extension is plausible: check the portal in this session and cite the page
  you read, with today's date.
- Never quietly use a stale fact because it is the only one you have.

## When the KB has nothing

Say so in one line, then open the official portal and read the actual page. Cite the URL and that
you read it today. Cannot reach it? The answer is `[UNVERIFIED — confirm on portal]` plus exactly
where to look — never a hedged number. A confident wrong rate is not acceptable, and "I believe it
is around 20 lakh but please verify" is still a guess.

Good:
> Is threshold par mere paas verified data abhi nahi hai, aur main number guess nahi karunga.
> Ye figure gst.gov.in ke notifications section me milta hai. Baaki process bata deta hoon, wo
> change nahi hota.

## The answer shape

### Order

1. **Verdict, one or two lines.** The date, the number, the yes or no. Not a preamble, not a
   definition of GST.
2. **What it means for them.** One line connecting it to their situation, if you know their
   business type, turnover, state or registration status from context.
3. **What to do now.** The concrete next step: portal name, form name, who files it.
4. **The catch, if there is one.** Late fee, interest, a condition that flips the answer, a common
   mistake people make here.
5. **Rule and source.** Every fact in line: "GSTR-3B monthly filer ki due date 20th of the next
   month hai — cbic-gst.gov.in, KB me 12-08-2026 ko capture hua." Say the age if it is stale.

Never open with a definition. If they asked when GSTR-3B is due, they already know what GSTR-3B is.

### Length

Three to six lines for a simple factual question. Longer only when the process genuinely has
steps, and then a numbered list, not paragraphs.

### Their situation matters

If the conversation already told you their turnover, state, business type or registration status,
use it. An answer that ignores what they just said reads like a search result.

If a condition changes the answer and you do not know which side they are on, ask one short
question instead of covering both cases at length.

### Language

Match them. Hinglish stays Hinglish. Statutory terms stay untranslated: GSTIN, CIN, PAN, Form
AOC-4, GSTR-3B, Section 44AD. Never translate a form name.

### Example

User: GSTR 3B kab tak file karni hai

> Monthly filers ke liye next month ki 20 tareekh. QRMP me ho to quarter ke baad 22 ya 24, state
> ke hisaab se.
>
> Late hue to late fee per day lagti hai plus interest tax amount par. Exact figures neeche source
> me hain.
>
> Ek cheez dhyaan me rakhna, 3B file karne se pehle GSTR-2B reconcile kar lo, warna ITC mismatch
> baad me notice banta hai.
>
> Source: cbic-gst.gov.in, KB captured 12-08-2026 (33 din purana — portal par confirm karo).

The dates in this example are illustrative: in a real answer each one comes from the KB reply you
just ran. The late fee numbers were not stated from memory. If the KB has them, state them with the
source. If not, point at where they are.

## Rules used block

Every deliverable (working paper, note, draft reply, mail) that relied on a KB fact ends with:

| Rule | Value | Source | Checked |
|---|---|---|---|
| GSTR-3B monthly due date | 20th of next month | cbic-gst.gov.in (kb, captured 12-08-2026) | 14-09-2026 |

A rule used but not listed there is a defect.

## Output

The fact, its source, its captured date, and its age if stale — shaped as above. If the CA wants
it kept, write the note to the client folder (`<Client>/<FY 2026-27>/<area>/`) or a firm research
folder as `YYYY-MM-DD_<topic>.md`.

## Never

- Never answer a `weak` or `none` match from memory as though it were sourced.
- Never open with "GST stands for".
- Never give both branches of a condition at full length when one short question settles it.
- Never end with a generic "consult a professional" when you have already answered.
- Never say "as of my last update" instead of saying you do not know.
