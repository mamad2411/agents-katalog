---
name: mail-a-letter
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-20
---

## Goal

A letter or document is correctly addressed, stamped, and entered into the postal system toward its recipient.

## Preconditions

- The letter contents, an envelope that fits them, and the recipient's complete postal address (name, street + number, city, postal code, country if international).
- Postage: stamps in hand, or access to a post office / stamp retailer.
- Your own return address known.

## Steps

1. **Fold and insert the contents; seal the envelope.** Fold to fit without bulging; moisten or peel-and-stick the flap. → *Expect:* envelope flat, sealed on all edges, contents not shifting the shape.
2. **Write the recipient's address in the addressee zone.** Front of the envelope, centered-to-lower-right, in this line order: name / street address + number (apartment on the same or next line) / city + postal code (order varies by country) / COUNTRY in capitals for international. Legible ink, no cursive flourishes on the postal code. → *Expect:* address complete per that structure; postal code present and correct — verify it, misdirected codes are the top delivery failure.
3. **Write your return address in the sender zone.** Top-left corner (or the back flap, in some countries). → *Expect:* a deliverable return path exists if delivery fails.
4. **Determine required postage.** Standard-size letter under the weight limit (~20 g/1 oz) inside the country: one standard stamp. [BRANCH: heavier/rigid/oversized → weigh at a post office | international → international rate] → *Expect:* you know the rate class; when unsure, the post-office counter is the authority.
5. **Affix the stamp(s) in the top-right corner.** Total face value ≥ the required rate. → *Expect:* stamps flat and firmly stuck in the corner.
6. **Enter it into the postal stream.** [BRANCH: public mailbox (check the collection-time plate — a drop after today's last collection goes out tomorrow) | post-office counter (required for weighing, international customs forms, or tracked options)] ⚠️ *Irreversible:* a mailbox drop cannot be retrieved — confirm the address and contents before the slot. → *Expect:* letter through the slot, or a counter receipt.
7. **For anything that matters, get proof.** Tracked/registered mail at the counter yields a tracking number — the only way to later prove sending. → *Expect:* receipt with tracking number stored, if chosen.

## Decision points

- Contents are valuable, legal, or deadline-bound → registered/tracked mail with a receipt, not a mailbox drop.
- International letter with goods (not just paper) → a customs declaration form is required — counter only.
- No stamps and no nearby post office → supermarkets/convenience stores often sell standard stamps; postal apps in some countries sell printable/code postage.

## Failure modes & recovery

- **F1 Underpaid postage:** the letter returns to your return address or arrives postage-due to the recipient — re-send with correct postage; this is why step 3 matters.
- **F2 Letter returned "addressee unknown":** verify the address with the recipient (moved? unit number missing?) and re-send; the envelope's return markings say what failed.
- **F3 Sent but never arrived, no tracking:** untracked mail has no recourse beyond a delivery-delay inquiry; wait 2–3× the normal transit time, then re-send — and use tracking this time.

## Verification

The letter is in the postal stream (slot dropped after checking the collection time, or counter receipt in hand), addressed with verified postal code and return address, with tracking recorded when it mattered.

## Variations

- `us`: city, state abbreviation + ZIP on the last line; `de`/`jp`: postal code precedes the city; `jp` vertical addressing exists but Latin-script horizontal is accepted for international mail.
- Business-reply and prepaid envelopes: no stamp needed — but only for their printed purpose.

## Safety & privacy

Low risk. Don't put cash in ordinary mail; the return address reveals your home address — for sensitive correspondence a P.O. box serves as the sender zone.
