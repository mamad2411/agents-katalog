---
name: use-an-atm
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 5min
risk: medium
prerequisites: [have-bank-account]
status: draft
last_verified: 2026-07-20
---

## Goal

Cash is withdrawn from your bank account at an ATM (or a balance/deposit operation completed), with card, cash, and receipt all retrieved.

## Preconditions

- A bank card and its PIN (recalled, not written on the card).
- Awareness of your balance/daily limit for the intended amount.
- An ATM — preferably your own bank's, at a well-lit, populated location.

## Steps

1. **Choose the machine and give it one glance of inspection.** Prefer bank-branch ATMs over standalone ones. Wiggle-check: a loose or bulky card slot or keypad overlay suggests a skimmer — walk away if anything shifts or looks glued on. → *Expect:* card slot and keypad are solid, flush, and match the machine's design.
2. **Insert or tap the card.** Chip cards go in chip-first, face up (a diagram is printed by the slot); contactless: tap and hold. → *Expect:* screen leaves the idle state and prompts for language or PIN.
3. **Enter the PIN with your other hand shielding the keypad.** → *Expect:* dots appear per digit; screen advances to the menu. Three wrong attempts usually swallow the card — after two failures, stop and verify the PIN elsewhere.
4. **Select the operation and amount.** Withdrawal → amount from the quick list or "other amount" in the machine's dispensable denominations. → *Expect:* a confirmation screen; fees, if any, are disclosed here — decline if the surcharge is unacceptable.
5. **Confirm and wait without walking off.** ⚠️ *Irreversible:* dispensed cash left in the tray is rarely recoverable — stay at the machine until everything is out. → *Expect:* whirring, then cash presented in the tray.
6. **Take cash, card, and receipt — all three, in whatever order the machine returns them.** Many machines return the card *before* the cash to prevent forgotten cards; don't leave after the first item. → *Expect:* you hold cash, card, and receipt; the screen returns to idle.
7. **Count the cash discreetly and put it away before stepping aside.** → *Expect:* count matches the withdrawal amount.

## Decision points

- Machine is out of service or out of cash → use the next ATM; your account is untouched if no confirmation screen was reached.
- Foreign ATM offers "convert to your home currency" (DCC) → decline; choose to be charged in the local currency — the machine's conversion rate is worse.
- Someone lingers close behind → cancel, take your card, and use another machine or return later.

## Failure modes & recovery

- **F1 Card swallowed:** note the time and machine ID (printed on the ATM); call the number on the machine or your bank immediately — branch ATMs can often return it same-day; otherwise the bank reissues.
- **F2 Cash not dispensed but account debited:** keep the receipt/screen photo, note machine ID and time, and file a dispute with your bank — ATM counters reconcile and these disputes generally resolve in your favor.
- **F3 Wrong PIN twice:** stop; recover the PIN via your bank (app or branch) rather than burning the third attempt.

## Verification

You possess the card, the correct counted cash, and the receipt; your banking app (checked later, not at the machine) shows exactly one debit for the expected amount plus disclosed fees.

## Variations

- Deposits: insert cash/checks per the machine's prompts (envelope-free machines count in front of you — verify the on-screen count before confirming).
- Cardless withdrawal: your banking app issues a code/QR used at the machine — the PIN steps are replaced by app authentication.

## Safety & privacy

Medium risk: money and PIN. The three protections: skimmer glance (step 1), shielded PIN (step 3), never leave mid-transaction (step 5). At night prefer indoor/branch machines.
