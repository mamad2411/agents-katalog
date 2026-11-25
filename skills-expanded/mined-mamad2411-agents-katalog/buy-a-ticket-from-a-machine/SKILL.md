---
name: buy-a-ticket-from-a-machine
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Buy the correct machine-issued ticket and leave with the ticket, change, card, and receipt if needed.

## Preconditions

- You know the destination, zone, fare type, or event name.
- You have an accepted payment method: coins, bills, contactless card, chip card, or mobile wallet.
- The machine is in service and in a language you can navigate.

## Steps

1. **Read the first screen before paying.** Look for language, ticket type, destination, zones, date, and passenger category. → *Expect:* the machine shows options that match your trip or purchase.
2. **Choose the product.** [BRANCH: transit | parking | event] select ride fare, parking duration, or event ticket category. → *Expect:* the screen shows a price before payment.
3. **Check restrictions.** Look for off-peak, single-use, return, transfer, senior, child, or timed-entry rules. → *Expect:* the ticket will be valid when you plan to use it.
4. **Select quantity carefully.** Set number of adults, children, bikes, bags, or vehicles if relevant. → *Expect:* total price updates to the intended count.
5. **Choose payment method.** [BRANCH: exact change | card] use exact change if the machine says no change given; use card if cash acceptance is limited. → *Expect:* the machine prompts for coins, bills, tap, insert, or swipe.
6. **Pay only after reviewing the summary.** ⚠️ *Irreversible:* many machines cannot refund wrong tickets; confirm destination, date, quantity, and price first. → *Expect:* payment is accepted and printing begins.
7. **Wait for all items.** Do not walk away at the first sound. → *Expect:* ticket, card, change, and receipt slots finish dispensing.
8. **Take the ticket and change.** Check every slot, including low change cups and side receipt trays. → *Expect:* nothing paid for remains in the machine.
9. **Verify the printed ticket.** Compare destination, date, time window, zone, and count against your plan. → *Expect:* the printed ticket matches the trip or purchase.
10. **Keep the receipt if reimbursement or disputes matter.** Store it separately from the ticket so you do not hand it over by mistake. → *Expect:* proof of purchase is available later.

## Decision points

- Machine says exact change only → use coins or switch to card before inserting bills.
- Destination is missing → use zone map, staffed counter, official app, or another machine.
- Card is declined → try another reader once, then switch payment method.
- Ticket looks wrong after printing → go to staff immediately before using it.

## Failure modes & recovery

- **F1 Wrong fare type:** printed ticket has wrong zone or time, recover by asking staff before entering or boarding.
- **F2 Card left behind:** machine retains or ejects card, recover by checking the slot before leaving and contacting issuer if lost.
- **F3 No change dispensed:** receipt shows cash accepted but no change, recover by noting machine ID and reporting it.
- **F4 Printer jam:** payment accepted but no ticket appears, recover by photographing screen or receipt and finding staff.

## Verification

You hold the correct printed ticket, your card is back, change is collected, and the receipt is kept or intentionally declined.

## Variations

- Contactless-only machines: payment may be the ticket, so keep the same card for inspection.
- Multilingual machines: language can usually be changed on the first screen.
- Parking meters: the printed ticket may need to be displayed face-up in the vehicle.

## Safety & privacy

Medium risk because payment and travel rights are involved. Shield PIN entry, do not accept help from strangers who want your card, and inspect the ticket before leaving the machine.
