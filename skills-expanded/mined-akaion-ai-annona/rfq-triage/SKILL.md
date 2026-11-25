---
name: rfq-triage
description: Turn customer RFQs and test specifications into one row per request with the parameters a quotation needs, and list what is missing before anyone prices it.
version: 2
tools: [document_reader, explorer]
pins: local
---

# Triage requests for quotation

An RFQ for a probe card, a test socket or a fixture arrives as a mix of email,
PDF specification, drawing and spreadsheet. The quotation is only as good as the
parameters lifted out of them, and the costly mistake is a plausible number that
the customer never wrote.

## Finding the material

List **every** file under the folder you were given, recursively, with no
filter on type — do not pass a list of extensions to the explorer. Requests
arrive as PDF, Word, spreadsheet, email export, plain text and Markdown, and a
filter chosen before looking is how a folder full of documents reads as empty.
Then read each file the reader can open; report the ones it cannot, by name.

Do not stop to ask whether to continue. If nothing readable is there, say
which files you found and why none could be read — that *is* the answer.

## Method

1. **Enumerate** what arrived for each request before reading any of it: which
   files belong to which RFQ, by reference number or sender. A file that belongs
   to none is reported, not attached to the nearest one.
2. **Read the specification before the email.** The email summarises; the
   specification binds. When they disagree, keep both and flag it.
3. **Extract** one row per RFQ, with the unit the document uses:
   - customer and RFQ reference, date received, requested delivery;
   - device or technology (wafer size, product family, as named);
   - pad pitch, pad count and array layout (e.g. full array, peripheral, rows);
   - test temperature range, and whether hot and cold are both required;
   - touchdowns (lifetime or per-cleaning), current per pin if stated;
   - planarity and alignment tolerances;
   - quantity, and anything the customer marks as mandatory.
4. **Check mandatory fields.** Device, pad pitch, pad count, temperature range
   and delivery are needed to price anything. A row missing any of them is
   flagged `INCOMPLETE`, with the fields named.
5. **Write the questions** the sales engineer should send back — one per
   missing or contradictory field, phrased so the customer can answer it.

## Output

CSV, one row per RFQ, then the flags and the questions:

```
rfq,customer,received,device,pad_pitch_um,pad_count,array,temp_min_c,temp_max_c,touchdowns,planarity_um,alignment_um,qty,delivery,source
RFQ-0412,Customer A,2026-03-02,300mm DRAM,60,4200,full array,-40,125,500000,15,?,2,wk 18,spec_0412.pdf
RFQ-0415,Customer B,2026-03-04,,80,,peripheral,25,85,,,,1,,mail_0415.eml
# 2 RFQs · 1 complete · 1 incomplete
INCOMPLETE
  - RFQ-0415 · missing device, pad_count, delivery
CONFLICTS
  - RFQ-0412 · pad pitch 60 µm in spec_0412.pdf p.3, 65 µm in the cover email
QUESTIONS
  - RFQ-0415 · Which device and wafer size is the card for?
```

## Rules

- An empty cell means the documents do not state it. `?` means they state it
  and you cannot read it (a blurred scan, a cut-off table). They are different
  problems for whoever follows up, so never merge them.
- Never invent a value, never fill one from a similar RFQ, and never convert a
  "typical" or "target" figure into a requirement. If a value is qualified, say
  so in the flags.
- Keep the document's own units and notation; convert only when asked, and then
  keep the original alongside.
- Name the source file, and the page where it helps, for every row.
- This is triage, not a quotation: no prices, no lead times, no judgement on
  whether the part can be built.
