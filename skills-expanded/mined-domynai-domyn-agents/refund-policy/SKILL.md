---
name: refund-policy
description: The rules for approving or refusing a refund, and how to word either outcome. Required reading before calling refund_payment.
version: "1.0"
enforcement: required
metadata:
  requires:
    tools: [refund_payment]
---

This skill is marked `required`: a turn in which its requirements are not met is
refused before the agent does anything, rather than run without it.

## Eligible

- The order is `processing` or `shipped`: the customer no longer wants it.
- The parcel never arrived.
- Delivered but damaged, with the customer describing the damage.
- Charged more than once for the same order — always refund the duplicate, no
  questions asked.

Check the payment first with `get_payment_info`: whatever happened to the order,
only a `completed` payment can be refunded.

## Not eligible

- Delivered, with nothing wrong with it.
- The payment is `pending` or `failed`: nothing has been taken yet. A refund
  against it is how a customer gets paid for money they never spent.
- Already refunded — `refunded` or `refund_pending` means the money is moving.
  Starting a second one is how a customer gets paid twice.

## Wording

Approving: state the amount and when it lands.

> That is refunded — €42.00 back to the card you paid with, in 3-5 working days.

Refusing: give the reason, and the one thing that would change the answer.

> I cannot refund this one yet: the payment is still pending, so nothing has been
> taken from your card. It clears within a day; if the parcel has still not
> arrived by then, write again and I will refund it.

Never refuse without a reason, and never blame "the system".
