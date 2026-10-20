---
name: buy-stamps
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

You buy the right postage stamps for mail you plan to send, choosing domestic or international postage and the quantity needed.

## Preconditions

- You know what country the mail is being sent from and where each item is going.
- You have payment accepted by the seller.
- You know whether you need single stamps, a sheet or booklet, or tracked postage instead.
- You can estimate whether the envelope is standard letter size and weight.

## Steps

1. **Sort the mail destination.** Separate domestic letters from international letters and anything large, thick, or valuable. → *Expect:* each item has a postage category.
2. **Choose a buying channel.** [BRANCH: post office | grocery or pharmacy counter | postal website or kiosk] → *Expect:* you know where you will buy and whether help is available.
3. **Ask for current rates if unsure.** Say the destination and whether it is a standard letter. → *Expect:* the clerk or website shows the current domestic or international amount.
4. **Pick forever or denomination stamps.** For ordinary domestic letters, buy forever stamps if available; for exact-rate needs, buy stated-value stamps. → *Expect:* the stamp value covers the letter at mailing time.
5. **Choose sheet, booklet, or singles.** Buy a sheet or booklet for future use, or singles when you only need one or two international stamps. → *Expect:* quantity matches your likely mail volume.
6. **Pay and inspect the stamps.** Check that the stamps are unused, not torn, and match what you requested. → *Expect:* you receive stamps and a receipt or transaction record.
7. **Store them flat.** Keep stamps dry, away from heat, and in the booklet or envelope they came in. → *Expect:* adhesive and barcodes remain intact.
8. **Apply only when ready to mail.** Put the correct postage in the top right corner and add extra postage if the letter is heavy. → *Expect:* the envelope is ready for a mailbox or counter drop.

## Decision points

- If the item is rigid, square, unusually thick, or over standard weight, ask for metered postage instead of guessing with stamps.
- If mailing internationally, check customs form requirements before buying only letter stamps.
- If rates recently changed, forever stamps may still cover ordinary domestic letters while denomination stamps may need make-up postage.
- If the mail is time-sensitive or valuable, buy tracked service rather than stamps.

## Failure modes & recovery

- **F1 Underpaid postage:** detect returned mail or clerk warning, recover by adding make-up postage or buying counter postage.
- **F2 Wrong destination type:** detect domestic stamps chosen for international mail, recover by asking for the international letter rate.
- **F3 Damaged stamp:** detect torn, wet, or previously canceled stamp, recover by using a new stamp.
- **F4 Bought too many:** detect excess quantity, recover by storing forever stamps for later ordinary letters.
- **F5 Counter closed:** detect no staffed service, recover by using a kiosk, postal website, or approved retail seller.

## Verification

You have unused stamps with enough value for the intended mail class and destination, and any stamped envelope has the postage placed in the top right corner.

## Variations

- United States: forever stamps cover one-ounce domestic First-Class letters after future rate changes.
- Countries without forever stamps: check the printed value against the current rate before mailing.
- Online purchase: allow delivery time unless printing postage at home.

## Safety & privacy

Low risk. Do not post letters containing sensitive documents without considering tracking, and do not rely on old denomination stamps without checking the current rate.
