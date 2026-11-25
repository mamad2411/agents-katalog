---
name: subscription-billing-reconciliation
description: Reconcile what a subscription contract says should have been billed for a period against what invoices actually billed. Covers proration, billing terms, invoice exports with revisions, credit notes, merged and churned accounts, parent/child billing, currency conversion and rounding. Use for contract-vs-invoice, revenue assurance, or billing-leakage checks.
---

# Subscription billing reconciliation

Goal: for each customer, compute EXPECTED (from the contract schedule) and BILLED (from invoices) for one period in one reporting currency, then classify the gap. Write the rules down before coding; most errors are rule mistakes, not arithmetic.

## 1. Read every rule source first
Specs rarely sit in one place. Read all prose (memos, chat logs, READMEs) end to end, in time order. Later messages override earlier ones. Note every definition (period length, tolerance, rate choice, who is in scope) and every exception. Re-read the rules after your first output and check each one against the data, not just the first mention.

## 2. Expected amount (from the contract)
- Schedule amounts are per billing term (monthly, quarterly, annual). Normalise to the period: monthly x1, quarterly /3, annual /12, unless the spec says otherwise.
- Contract changes (upgrade, downgrade, price change, pause) take effect on their effective date. Build a per-day timeline and sum per day, rather than assuming one price for the whole period.
- Proration is by calendar days in the period (use the actual day count of the period, not a flat 30, unless told).
- Status rules: trials bill zero; the churn/termination date is normally the last day of service, inclusive; days after it earn nothing. Check which date convention the spec uses.
- Dates arrive in mixed formats; parse each explicitly and validate that none failed.

## 3. Billed amount (from invoices)
- An invoice export is often an event log: the same invoice id can appear many times. Keep only the latest snapshot per id (by export timestamp), then apply status filters. Draft and void never count; paid and open do. A later snapshot can cancel an invoice that an earlier one showed as paid.
- An invoice covering a multi-period service window contributes only the share of days that fall inside the reporting period: overlap days / total window days. Do not count by issue date alone.
- Credit notes reduce billed revenue. A credit note belongs wherever the invoice it corrects belongs: attribute it to the same customer AND the same service period as the original, regardless of its own issue date or its own (often blank or wrong) customer field. If the original is outside the period, the credit note is outside it too. If the original does not count (void, draft, cancelled), the credit note is moot and is ignored.
- Never infer a credit note's customer from its own text when it carries a link to the invoice it corrects.

## 4. Entity resolution
- Customer names come as free text from several systems. Normalise case, punctuation, whitespace, accents, `&` vs `and`, and legal-form suffixes (Inc, Ltd, GmbH, AG, PLC, BV, LLC...). Prefer authoritative keys in this order: account id, then domain, then normalised name.
- Merged duplicates: invoices of a merged-away account belong to the surviving account. Follow chains (A merged into B merged into C) to the final survivor. Decide explicitly how the survivor's status and contract timeline interact with the duplicate's; if a surviving record is churned, its own churn rule applies to the merged entity.
- Parent/child accounts (a child billed through a billing parent): children roll up to the parent. If the parent is churned or otherwise no longer a valid billing target, children are reported on their own lines. Follow chains and watch for cycles.
- Anything that cannot be tied to an account becomes its own unmatched line, grouped by its cleaned-up name, if the spec asks for it. Do not silently drop it and do not force-match it to the nearest account.

## 5. Currency and rounding
- Convert each side at the rate the spec names for that side: for example schedule at a period average or period-end rate, invoices at the rate on their own issue date. Use the same table for both and the spec's definition of average (simple mean over published days).
- Rate tables skip weekends and holidays: use the last published rate on or before the date.
- Keep full precision (use Fraction/Decimal) through the whole computation and round only once at output, half up, to 2 decimals. Do not round per day or per invoice.
- Convert after prorating or before it consistently; the result is identical, but mixing them with per-step rounding is not.

## 6. Classification
- Tolerance is usually max(absolute floor, percentage of expected). Apply it to the absolute delta.
- Typical classes: within tolerance; nothing billed although something was due; billed less than due beyond tolerance; billed more than due beyond tolerance; billed with no account. Use the exact labels the spec gives.
- Delta = billed - expected, sign preserved. Omit rows where both sides are zero unless the spec says to list every account.
- Output exactly the columns, order, sort and number formats the spec states.

## 7. Self-checks before finishing
1. Row count and set of ids plausible; no id appears twice; every merged-away id is absent as its own line.
2. Pick 5 accounts with unusual features (multi-period invoice, credit note, merged, bill-to, mid-period change, churn) and recompute them by hand from the raw rows.
3. Sum of credit-note effects: confirm each counted credit note's original also counted.
4. Totals by class look sane (most accounts match; a few percent off).
5. Output parses with a strict reader; no trailing spaces; consistent decimals.
