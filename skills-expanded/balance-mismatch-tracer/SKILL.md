---
name: balance-mismatch-tracer
description: "Use this skill when the user says an account's balance in the app doesn't match what their bank, card or broker shows, and wants to know why — 'my balance is wrong', 'the app says 1,240 but my bank says 1,180', 'it doesn't reconcile', 'I'm off by 60', 'my card shows a different amount owed'. It gets the bank's side as rows (a screenshot, a statement, or rows the user pastes), matches them against the ledger row by row, and names the rows that make up the gap. Not for reading a balance ('what's in my checking?' — answer directly), importing a statement (statement-import), a general tidy-up of the books (catch-up), or whether a card bill has been paid."
---

Find out exactly why an account's balance in the app differs from the bank's, and propose the smallest fix. The answer is a list of rows that adds up to the gap — or an honest "can't tell yet" with what you need to finish.

## Gotchas

- **The ledger always agrees with itself.** Re-adding the app's own rows proves nothing about the bank, and is how this goes wrong: a confident "everything reconciles" while the user is still looking at a different number. Without the bank's side (step 2) there is no verdict.
- **A gap is rows until proven otherwise — cents included.** A small difference is a fee, interest, an FX-rounded foreign charge or a refund, not noise. Never call it rounding or "just a few cents"; name the row, or report it as unexplained.
- **"Timing" needs a named row.** A pending or not-yet-posted row explains a gap only when you can point to it (date, amount, description) in the bank's list. Without one, it's unexplained.
- **Same basis, same sign.** A bank app shows several balances (current, available, statement closing) and a card shows what's owed as a positive number while the ledger keeps liabilities negative. Agree which bank figure you're comparing before computing a gap, and never report a sign difference as a money difference.
- **An imported row can still be wrong.** It may have been edited after the import — an accidental keystroke is enough. Before you say why a row differs, read its history with `trace_transactions`: it shows how the row was created and every edit since (when, by whom, the amount before and after). Never blame the import, or guess, without that check.
- **`describe_account` doesn't read an account** — it drafts a new-account form. The current balance, the opening amount and its date come from `list_accounts`.
- **Rows before the account's opening date don't count.** A statement that starts before `initial_balance_date` overlaps the opening balance — `verify_statement_balance` calls this a tracking-start conflict. Check the opening before blaming a missing row.
- **`diff_statement` with `withheld` set is not a comparison.** The parse didn't finish, or the statement's own balances don't add up; act on nothing from it.
- **A category can't move a balance.** Don't offer recategorising as a cause.
- **`reconcile_accounts` is a plug, not an explanation.** It writes an adjustment for whatever is left. Offer it only after the rows are traced, for a residual the user chooses to accept.

## Steps

1. **Pin both numbers.** Which account; the app's balance (`list_accounts` with a narrow `query`); the bank's figure, which balance it is, and as of when. Ask only for what's missing, in one question. Work out the gap with `calculate`.
2. **Get the bank's side as rows.** Ask once, offering the easy ways: a screenshot of the bank app's transaction list back to the last date the two agreed, a statement file, or the rows pasted in. An image attached this turn is already read; an earlier upload is `read_attachments`. If the user has none to hand, look for what's already here — `list_statements` for the account, then `check_statement_drift` — before asking again. If there is still nothing, stop and say what you need; don't conclude.
3. **Match row by row.**
   - A statement: `diff_statement` (its `missing` / `extra` lists), or `import_transactions` with `commit=false` to preview a new file without booking it. For balances as of the statement's dates, `verify_statement_balance`.
   - A screenshot or pasted rows: `get_transactions` for the account over the same dates (page until every row is seen), and match each bank row by amount and a date within a few days.
   - In the same window, `find_duplicates` and `list_match_reviews` — a duplicate is an "extra" row the bank never had.
4. **Explain the gap.** Add up the unmatched rows with `calculate` and compare with the gap. If they equal it, it's explained. For a row the app has at a different amount, `trace_transactions` on it says whether it was edited after it was booked; report that edit (its date and the amounts before and after) as the cause, so the user knows how it happened. If not, say what's still unexplained and take the next lead: an earlier window, the opening amount and date, or `check_statement_drift`'s `constant_drift` (the same drift at every close means the opening balance is wrong).
5. **Report** in this shape, then propose the fix:

```
**<Account>** — app <amount>, bank <amount> (<which balance>, as of <date>) → gap <amount>

Explained:
- <date> · <description> · <amount> — <missing in the app | extra in the app | amount differs by …> (<txn id>)

Unexplained: <amount, and the next thing to check> | nothing

Fix: <the smallest set of adds, deletes, edits, merges or an opening change>
```

6. **Fix only what the user approves.** Use the ordinary tool for each change — `add_transactions`, `delete_transactions`, `update_transactions`, `merge_transactions`, or `update_accounts` for the opening. Then re-read the balance with `list_accounts` and report the new gap; if anything is left, say so plainly rather than calling it done.
