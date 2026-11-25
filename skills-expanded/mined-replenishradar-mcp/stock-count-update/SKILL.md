---
name: stock-count-update
description: Record a stock count or add a hand-managed location in ReplenishRadar. Use when the seller says they counted a product, wants to set or correct the quantity at a warehouse or 3PL, asks to add a new warehouse, 3PL or other location they manage by hand, or says the stock number at a location is wrong.
---

# Stock count update

Sets how many units of a product are on hand at a location the seller manages by hand, and adds such a location when it does not exist yet. Stock at Shopify and Amazon is synced from the channel and is not changed here.

Setting a count overwrites the stored number. It is the one change in this plugin that can lose information, so the steps below are not optional.

## Setting a count

1. **Read the current position.** Call `rr_get_inventory_position` with the `sku`. Find the row for the location the seller named and note what is stored there now.
2. **Show the change and wait for a yes.** Say it in one line: "Warehouse A has 140 of BLUE-MUG-12 on record. Set it to 96?" A sale recorded since the seller counted can be lost when the number is overwritten, so if the count is not from today, say so and ask whether the number is still right.
3. **Set it.** Call `rr_set_stock_at_location` with the `sku`, the `quantity` and either the `location_id` or the `location_name`. The quantity is the new total on hand, not an amount to add or remove.
4. **Confirm from the source.** Call `rr_get_inventory_position` again and report the stored number.

For several products, repeat the steps for each one. Show the whole list of changes once, get one yes, then set them one at a time and report any that were refused.

## When the call is refused

- A location synced from a sales channel, or one that is inactive, is refused. Only hand-managed locations take a count. Tell the seller the channel's own number is what ReplenishRadar shows there.
- A `location_name` matches hand-managed locations only. If nothing matches, list the locations from the position you read and ask which one they mean.
- It is refused while a live collection holds the stock. Tell the seller to try again once that finishes.
- If the connection cannot make changes, tell the seller they can reconnect ReplenishRadar and tick "make changes" on the sign-in screen. Do not retry the write.

## Adding a location

Only when the seller asks for a new one:

1. Ask for the `name` and the kind of place it is. The `type` is one of the values the tool lists, for example `warehouse`. An address is optional: `city`, `state`, `postal_code`, `country`.
2. Call `rr_create_location`. It adds the location and changes no stock. It fails if an active location already has that name; offer to use the existing one.
3. Set `is_default` only when the seller says this should be their default hand-managed location.

A new location starts with no stock. Set counts for it with the steps above.

## Rules that keep the answer honest

- Never work out the new quantity yourself from sales or receipts. The number comes from the seller's count.
- Never set a count to fix a number that looks wrong without asking. A wrong-looking number is more often a sync problem: use the data-health-check skill first.
