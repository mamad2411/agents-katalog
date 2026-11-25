---
name: fortax-gstr2b-reconciliation
description: Reconcile a month's GSTR-2B with the client's purchase register - download 2B from the GST portal in the CA's own logged-in browser, run the Fortax engine to match, judge the leftover pairs (typos, dropped prefixes), and give ITC to claim now, ITC at risk, GSTR-3B Table 4 figures and supplier follow-up drafts. Typical asks - "Aug ka 2B reconcile karo", "ITC kitna claim karein", "2B vs books", "supplier ne file kiya ki nahi", "2B download kar do".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GSTR-2B reconciliation

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Two kinds of match, never mixed

- **Match (the engine).** Same supplier GSTIN, document type and invoice number (zero padding and
  separators ignored), taxable value and tax within the tolerance (₹1 by default). Buckets: matched,
  mismatch, missing in 2B, missing in books, and "probable" (number written differently, same amounts).
  Every amount, total, count and 3B figure in its reply is the engine's. **Never add up, recompute or
  re-list them.**
- **Judgement (you).** Only what the rules could not pair, and only from the pairs the engine hands you.

## Step 1 — the files

- **Purchase register** for the month, .xlsx or .csv, from any accounting software (Tally, Busy, Zoho,
  an ERP, Excel): supplier GSTIN, supplier's invoice number (the supplier's number, not your voucher
  number), invoice date, document type (invoice / credit note / debit note), taxable value, IGST, CGST,
  SGST, cess. Rows with no supplier invoice number cannot match — list them for the CA to fix at source.
- **GSTR-2B** for the same month and GSTIN. Look in the folder where the CA drops files and in
  `<Client>/<FY>/GST/<YYYY-MM>/` first. A file with "2B" in its name and this GSTIN or period is already
  there -> use it, skip the portal.

## Step 2 — getting 2B from the portal (only if no file)

GSTR-2B for a month is generated on the 14th of the next month. Asked for August before 14 September ->
say it is not out yet; offer GSTR-2A only if the CA wants a provisional look.

**The CA logs in, in their own browser.** Username, password, captcha and OTP are theirs; never type or
store them. Download only — nothing on this path submits, files or pays.

After the CA says they are logged in, either drive the page with your browser tool (Claude in Chrome, a
Playwright/browser MCP, or the Codex browser) — read the page before every click, element references change
on each page — or, if you have none, give the CA this click path:

1. **Check the GSTIN.** The dashboard must show this client's GSTIN. A saved session can belong to another
   client; if it does, ask the CA to log out and log in to the right one.
2. **Returns Dashboard.** Services -> Returns -> Returns Dashboard (or the "Return Dashboard" button on the
   home page).
3. **Period.** Financial Year (April–March holding the month), Quarter, Period = the month -> Search.
4. **GSTR-2B tile.** "Auto-drafted ITC Statement GSTR-2B" -> **Download** (not View).
5. **JSON.** Choose **Download JSON file** / **Generate JSON file to download**. If it says the file is
   being generated, wait a few seconds and click again. A large client's 2B can come in several parts —
   download every part.
6. **File it.** Move the download(s) from the Downloads folder into `<Client>/<FY>/GST/<YYYY-MM>/`, named
   with GSTIN and period. If only Excel is offered, download it — the engine reads the portal's 2B workbook
   too (amendment sheets are listed, not merged).

The portal changes its menus. If a step is not on the page, find the same thing by its words ("GSTR-2B",
"Download", "JSON") and finish; tell the CA what the path was now.

Never click Submit, File, Proceed, Save as draft, Generate summary or anything that changes a return.
Never download for a GSTIN other than the client's.

## Step 3 — run the engine

```bash
python3 scripts/fortax.py gstr2b --g2b "<2B.json|zip|xlsx>" --books "<purchase_register.xlsx>" \
  --gstin 27ABCDE1234F1Z5 --fp 082026 --company "Sharma Traders" [--tolerance 1] [--out <folder>]
```

Writes next to the register: `GSTR2B_recon_<GSTIN>_<MMYYYY>.xlsx`, `_summary.txt`, and
`_pairs_to_judge.json` when there are leftovers for you. A 2B of another GSTIN is refused; a 2B of another
month is flagged — get the right one. Several 2B parts: run per part or ask the CA for the single zip.

## Step 4 — judge the pairs

When the reply ends with a NEXT STEP and pairs, read `_pairs_to_judge.json`. For each: supplier, both
numbers, both dates, both amounts.

- **Same document:** a typo or transposed digits (`771` / `717`), a dropped prefix or FY suffix
  (`45` / `TS/45/26-27`), a separator the rules missed, rounding of a few rupees, dates within a few days.
- **Not the same:** two different invoices of one supplier with similar amounts; dates weeks apart; numbers
  sharing digits by chance. **Never pair on amount alone. When unsure, leave it out.**

Write the ones you accept to a file, e.g. `ai_matches_082026.json`:

```json
[{"gstin": "27AAACX1234A1Z9", "books": "45", "g2b": "TS/45/26-27", "reason": "same invoice, FY suffix dropped in books"}]
```

**Every item needs all four fields** — copy `gstin`, `books` and `g2b` exactly as listed in the pair.
Rerun the same command with `--ai-matches ai_matches_082026.json`. The engine applies them only between
leftovers of that supplier, marks them as AI-matched, and refuses any that do not fit — say which were
refused.

## Step 5 — read the result out

As the summary says it, then in plain words:

- ITC as per books and as per 2B; **claim now**; what can be claimed after the CA confirms the probable,
  AI-matched and mismatch rows; **at risk** (in books, not in 2B).
- Your matches, each with its reason, and that the CA confirms them.
- Missing in 2B by supplier; missing in books; ITC not available as per 2B; reverse charge.
- Register rows with no supplier invoice number.
- The GSTR-3B Table 4 figures, labelled "as per 2B, check before use" — they feed `fortax-gstr1-and-3b`.
- The workbook path.

## Step 6 — supplier follow-up (drafts only)

If documents are missing in 2B, offer one draft per supplier listing its invoices, dates and tax, asking them
to file or amend GSTR-1 / IFF. Write the drafts to a file and show them; the CA sends them from their own
mail. Do not suggest WhatsApp unless the CA asks.

## What you say about ITC

- ITC is claimed only on documents in 2B with ITC available (section 16(2)(aa) CGST Act). Missing in 2B is
  not claimed "to be safe" — it waits for the supplier.
- Mismatch: take the lower of books and 2B until the difference is explained.
- Reverse charge: pay the tax in cash first, then claim the credit in the same month.
- Credit notes in 2B cut ITC even if not booked — say so when "missing in books" has credit notes.
- Section 17(5) blocked credit and Rule 42/43/37 reversals are removed in the 3B working, not here.

## Never

- Recompute a total, a bucket count or a 3B figure.
- Match anything yourself outside `--ai-matches`, or call a match certain.
- Change the client's purchase register or send a supplier mail — draft, and the CA decides.
- Type the CA's portal password, captcha or OTP.
