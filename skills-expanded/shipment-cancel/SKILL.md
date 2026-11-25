---
name: shipment-cancel
description: Use when the user wants to cancel a Mothership shipment, or asks whether a shipment can still be cancelled or what cancelling would cost or refund. Finds the shipment with shipment-get, asks why, offers a reschedule or edit when that fits, and sends the user to the shipment in the dashboard to cancel it.
---

# Cancel a Mothership shipment

Cancelling can't be undone, and it charges any cancellation fee. The user cancels in the Mothership dashboard, which shows the fee and refund estimate before anything changes. You can't cancel for them.

## Find the shipment

1. Get the shipment's identifier from the user, such as a Mothership reference number like MS123456, a PRO, a BOL, or their own reference.
2. Call `shipment-get` with it. This call changes nothing.

If the identifier matches more than one shipment, ask the user for the Mothership reference number. If the shipment isn't found, ask them to check the identifier. A `status.phase` of `cancelled` means the shipment is already cancelled, so tell the user that.

## Ask why

Ask one short question about why they're cancelling, unless they already said. When the freight won't be ready, details are wrong, or the shipment needs a service it doesn't have, such as a liftgate, tell the user they may be able to reschedule or edit the shipment instead, from the same page. Cancel only if they still want to.

## Send the user to cancel

Give the user the shipment's `trackUrl`, which opens it in the Mothership dashboard, and tell them to cancel it there. The dashboard shows the fee and the refund estimate first. You can't see them here, so never quote or guess a fee. For what a cancellation fee covers in general, search the help center with `knowledge-search`.

When the dashboard says the shipment can't be cancelled, or that it isn't eligible for self-service cancellation, point the user to the Mothership help center at https://help.mothership.com.

## Who can cancel

Only the user who booked the shipment, or a teammate who can manage shipments, can cancel it.
