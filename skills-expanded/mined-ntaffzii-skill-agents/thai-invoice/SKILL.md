---
name: thai-invoice
description: Use this skill for any task involving Thai tax invoices, receipts, quotations, credit/debit notes, or withholding-tax (WHT) certificates. Trigger on "ออกใบกำกับภาษี", "ใบเสร็จ", "ใบเสนอราคา", "ใบลดหนี้", "ใบเพิ่มหนี้", "หนังสือรับรองหักภาษี ณ ที่จ่าย", "ภ.ง.ด.3", "ภ.ง.ด.53", "Thai tax invoice", "VAT 7%", "withholding tax Thailand", or any request to draft or calculate a Thai accounting document under Revenue Code §86/4. If the task is bookkeeping-level aggregation across many invoices (filing ภ.พ.30, reconciling a ledger), this skill drafts the source document only — direct the user to their accounting system or accountant for the return itself.
---

# Thai Tax Documents (ใบกำกับภาษี / ใบเสร็จ / ใบเสนอราคา / WHT)

## Overview

Thai tax invoices, quotations, and WHT certificates follow specific structural rules (Revenue Code §86/4) and specific VAT/WHT math. A model without this skill tends to skip the mandatory VAT line, guess a WHT rate, or produce Thai-English hybrid documents that omit the required Thai phrase. This skill supplies the required fields, the current common VAT/WHT rates, and a Decimal-based calculator so totals don't drift.

**Not legal or tax advice.** This skill drafts documents and does arithmetic; it does not replace a licensed accountant or the Revenue Department for a real filing.

## When to use

- ออกใบกำกับภาษีให้ลูกค้านิติบุคคลหรือบุคคลธรรมดา
- คำนวณ VAT 7% (แยกจากราคา หรือถอดจากราคารวม)
- คำนวณภาษีหัก ณ ที่จ่าย และออกหนังสือรับรอง (ภ.ง.ด.3/53)
- เขียนใบเสนอราคา / ใบลดหนี้ / ใบเพิ่มหนี้
- Drafting a bilingual Thai-English invoice for a foreign buyer

## When NOT to use

- The task needs the *monthly return* (ภ.พ.30, ภ.ง.ด.1/3/53) aggregated across many transactions — this skill produces the source document, not the filing; point the user to their bookkeeping system
- The task is generic (non-Thai) invoicing with no VAT/WHT/Revenue Code requirement — plain markdown-report is enough

## Required fields — full tax invoice (Revenue Code §86/4)

A full ใบกำกับภาษี must contain all seven elements (quote the Thai labels exactly):

1. คำว่า "ใบกำกับภาษี" ในที่ที่เห็นได้ชัดเจน
2. ชื่อ ที่อยู่ และเลขประจำตัวผู้เสียภาษีอากรของผู้ออก
3. ชื่อ ที่อยู่ ของผู้ซื้อ (+ เลขประจำตัวผู้เสียภาษีถ้ามี)
4. หมายเลขลำดับและเล่ม (ถ้ามี)
5. ชื่อ ชนิด ประเภท ปริมาณ และมูลค่าของสินค้า/บริการ
6. จำนวนภาษีมูลค่าเพิ่ม แยกออกจากมูลค่าสินค้า/บริการให้ชัดเจน
7. วัน เดือน ปี ที่ออกใบกำกับภาษี — use [thai-date-format](../thai-date-format/SKILL.md) for the formal date string

A short-form (อย่างย่อ) invoice may omit buyer address/TIN when issued at point of sale by an approved retailer.

## VAT

- Reduced rate currently applied: **7%** (statutory rate under the Revenue Code is 10%; the 7% rate is set by a renewable Royal Decree — do not treat 7% as permanent, see Known limitations)
- VAT-exempt items (Sec 81): basic unprocessed agricultural products, education, healthcare, books, public transport — do not add VAT and do not issue ใบกำกับภาษี for these; use ใบส่งของ/บิลเงินสด instead
- Only a VAT-registered seller (ผู้ประกอบการจดทะเบียน VAT) may issue ใบกำกับภาษี

## Withholding tax (ภาษีหัก ณ ที่จ่าย)

| Service | Form | Rate (resident payee) |
|---|---|---|
| บริการทั่วไป (services) | ภ.ง.ด.3 / 53 | 3% |
| ค่าเช่าอสังหาริมทรัพย์ | ภ.ง.ด.3 / 53 | 5% |
| ค่าโฆษณา | ภ.ง.ด.3 / 53 | 2% |
| ค่าขนส่ง | ภ.ง.ด.3 / 53 | 1% |
| ค่าวิชาชีพอิสระ (individual) | ภ.ง.ด.3 | 3% |
| ดอกเบี้ย | ภ.ง.ด.2 | 15% |
| เงินปันผล | ภ.ง.ด.2 | 10% |

ภ.ง.ด.3 = payee is บุคคลธรรมดา (individual). ภ.ง.ด.53 = payee is นิติบุคคล (juristic person, e.g. บริษัท). WHT base is always the **pre-VAT** amount.

## Numbering, credit/debit notes, quotation

- Sequential invoice numbers required (e.g. `INV-2026-0001`); reset annually is optional
- ใบลดหนี้ (credit note): reference original invoice number, state the reduction reason
- ใบเพิ่มหนี้ (debit note): same structure, upward adjustment
- ใบเสนอราคา is not a tax document — state clearly whether "ราคานี้ไม่รวมภาษีมูลค่าเพิ่ม" or "ราคารวม VAT 7% แล้ว", and specify validity period (e.g. "ยืนราคา 30 วัน")
- Combined "ใบเสร็จรับเงิน/ใบกำกับภาษี" is allowed for cash sales by a VAT-registered seller

## Common mistakes

1. Omitting the separate VAT line — Revenue Code requires the VAT amount shown distinctly, not folded silently into the total.
2. Issuing a combined ใบเสร็จ/ใบกำกับภาษี when the seller is not VAT-registered.
3. Issuing ใบกำกับภาษี for VAT-exempt goods (books, unprocessed agricultural products) instead of ใบส่งของ.
4. Wrong WHT rate — rent (5%) and advertising (2%) are the most commonly confused pair with services (3%).
5. Missing the buyer's TIN on a B2B invoice, which can block the buyer's input-VAT claim.
6. Computing WHT on the VAT-inclusive amount instead of the pre-VAT base.
7. Mixing up ภ.ง.ด.3 (individual payee) and ภ.ง.ด.53 (juristic payee) — using the wrong form requires refiling.
8. A bilingual invoice that includes "Tax Invoice" but drops the required Thai phrase "ใบกำกับภาษี".
9. Not issuing the WHT certificate to the payee within the required window after filing ภ.ง.ด.3/53.

## Templates

- `templates/tax-invoice-full.md` — full ใบกำกับภาษี
- `templates/quotation.md` — ใบเสนอราคา
- `templates/wht-certificate.md` — หนังสือรับรองการหักภาษี ณ ที่จ่าย

All templates use synthetic placeholder data — replace every bracketed field, and never fill in a real Thai national ID, tax ID, or company name as a "sample."

## Calculator

`calc.py` — Decimal-based, no dependencies:

- `calculate_vat(subtotal, rate=Decimal("0.07"))` → `{subtotal, vat, total}`
- `calculate_vat_inclusive(total, rate=Decimal("0.07"))` → backs VAT out of a VAT-inclusive total
- `calculate_wht(amount, rate)` → `{amount, wht, net_payable}` (`rate` can be a `WHT_RATES` key or a Decimal)
- `WHT_RATES` — the table above as a dict

Run `python3 calc.py` for the self-test.

Known limit: `calc.py` operates on a single transaction. It does not aggregate many invoices into a ภ.พ.30 or ภ.ง.ด.3/53 monthly total — that belongs in the user's bookkeeping system.

## Known limitations

- **VAT rate (7%) is set by a renewable Royal Decree, not permanent statute.** It has been extended repeatedly, but re-verify the currently effective rate against a Revenue Department (rd.go.th) source before relying on it for a real filing, especially near a decree's stated expiry date.
- WHT category boundaries (e.g. what counts as "rent" vs. "service") are sometimes disputed in practice — this table covers the common, uncontested cases only.
- Templates and disclaimers here are drafting aids. Do not remove the "not legal/tax advice" language when reusing or editing these files.
