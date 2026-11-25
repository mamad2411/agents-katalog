---
name: hire-local-help
description: Book an ID-verified local person through Mundane for something that needs someone there in person, such as checking a store's stock, photographing a place, a pickup or a place in line. Use when the user wants a real-world task done near a place they name.
---

# Hire local help with Mundane

Mundane books ID-verified local people for in-person tasks. The customer's
payment is held by Mundane and released only when they approve the proof.
Every task is screened against Mundane's Acceptable Use Policy before a person
sees it.

## 1. Ask what you need to know

Before searching, make sure you know:

- **What** needs doing, in words a stranger could follow without asking
  questions, and what proof the customer wants (for example, a photo of the
  shelf).
- **Where.** Ask for an address or a landmark. Never guess a location: confirm
  the place by name ("Union Square, San Francisco?") before you search.
- **When** it needs doing by.
- **Budget**, in the customer's currency.

## 2. Find people

- Call `search_workers` near the confirmed place. Pass a capability from
  `list_capabilities` when one fits. For work where the item can travel to the
  person, `find_workers_by_skill` searches by skill instead of place.
- Show **at most three** people, each with their rate in dollars (or the
  customer's currency), rating, distance and skills.
- **If nobody is near, say so plainly.** Mundane is small, and in many places
  and at many hours nobody is available. Never invent a person, a rate, an ETA
  or availability. Offer a real alternative within Mundane: a later time or a
  wider area. Never suggest the customer do the errand themselves instead.
- Refer to a person by their handle or "they". You do not know their gender.

## 3. Draft the task

- Call `post_task` with a clear title, step-by-step instructions, the
  location, the capabilities, a budget ceiling and an ISO-8601 deadline.
- The result is `open`, `screening` (a person at Mundane reviews it) or
  `rejected` with a reason. **A rejection is final.** Explain it to the
  customer. Never reword a task to get it past screening.

## 4. Get a clear yes, then book

- Call `get_spend_status` so you only propose what the balance and this
  connection's limits allow.
- Show the customer the person, the amount and Mundane's fee, and ask for an
  explicit yes **before** calling `make_offer`. Booking holds the amount plus
  the fee until the customer approves the finished work.
- Say an offer was sent only when `make_offer` returns it.

### When `make_offer` returns `payment_needed`

Nothing was held or sent. Give the customer:

- the `pay_url`,
- the total and the currency,
- a plain explanation: they pay for this task on Mundane, and the offer is
  sent from that page once they do.

When they come back, check with `get_task_status` before saying the offer went
out. If they paid but closed the page before it sent, send them back to the
same link to finish. Never claim that paying alone sent the offer.

## 5. Say what happens next

The customer gets an email when the person accepts and when proof is ready.
They can also ask you "how's it going?" at any time.

## Always

- **Money moves only through Mundane.** Never arrange Venmo, Zelle, Cash App,
  PayPal, cash or tips, and never pass a payment handle, phone number or email
  between the customer and a person. Extra work is a new offer the customer
  approves.
- Never promise money an offer does not carry: no refund, reimbursement or tip.
- Mundane won't do surveillance, follow or track a person, or anything unsafe
  or unlawful. If asked, say so plainly and don't try another tool.
- Mundane is not a way to send money to someone. It pays a person for a task.
- If a tool fails, say you couldn't check. Don't guess.
