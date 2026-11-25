---
name: buy-a-local-sim-card
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 30min-1h
risk: medium
prerequisites: [have-payment-method, have-id-document]
status: draft
last_verified: 2026-07-20
---

## Goal

Your phone has working local calls and mobile data on a local prepaid SIM, and you know how to top it up before the credit or validity runs out.

## Preconditions

- Your phone is carrier-unlocked (verify before travel: ask your home carrier, or test a friend's different-network SIM; a locked phone rejects all foreign SIMs).
- Passport or national ID: most countries legally require ID registration for SIM activation, and a photocopy is often not accepted.
- Phone supports the destination's bands (check the model on a band-compatibility site if the destination uses unusual LTE bands).
- SIM ejector tool or a paperclip; know your phone's SIM size and whether it takes eSIM.

## Steps

1. **Confirm the unlock before leaving home.** Insert any other carrier's SIM; if the phone asks for an unlock code or shows "SIM not supported", request an unlock from your carrier now. Unlocks can take days to process. → *Expect:* a foreign SIM registers on a network, or your carrier confirms the unlock in writing.
2. **Choose where to buy: official carrier store over airport kiosk.** [BRANCH: need connectivity the second you land → airport kiosk, accept the 2-3x markup | can wait an hour → official carrier store in town for fair pricing and proper registration] → *Expect:* a store selected; for kiosks, verify it sells an official carrier product, not a reseller SIM registered to a stranger.
3. **Pick a prepaid tourist or data plan.** State your stay length and data needs; ask what happens after the bundle is consumed (hard stop vs. expensive per-MB billing) and the plan's validity period. → *Expect:* plan chosen with known price, data cap, validity days, and post-cap behavior.
4. **Complete ID registration at the counter.** Hand over your passport; staff photograph or scan it and register the SIM to you. A SIM not registered to your own ID can be deactivated without notice in many countries. → *Expect:* registration done under your name; passport handed back; keep the SIM packaging, which carries the number and PUK code.
5. **Have the SIM installed and activated before leaving the counter.** Ask the staff to insert it, enter any default PIN, and confirm activation. Store your home SIM in the packaging slot or a labeled pocket; it is tiny and easily lost. → *Expect:* signal bars with the local carrier's name on screen; home SIM stored safely.
6. **Test calls and data on the spot.** Make a test call; load a non-cached website on mobile data with Wi-Fi off. [BRANCH: data fails but calls work → APN needs manual setup, step 7 | both work → step 8] → *Expect:* either full function confirmed or a clean diagnosis that only data is down.
7. **Set the APN manually if data fails.** Settings > mobile network > access point names: add the carrier's APN (name, APN string, sometimes username/password; the values are on the packaging or the carrier's site, and counter staff know them). Reboot after saving. → *Expect:* mobile data works after reboot with the new APN selected.
8. **Learn the top-up mechanism before you leave.** Ask: carrier app (may need a local payment method), USSD code (like *123#), scratch cards from convenience stores, or online with a foreign card. Install the carrier app and check your balance once. → *Expect:* you can read your remaining balance and data, and know one top-up method that works with your payment options.

## Decision points

- Phone supports eSIM and the carrier (or a travel eSIM provider) offers one → skip the physical swap entirely; buy online before travel, keep your home SIM active for SMS-based 2FA codes.
- Staying weeks rather than days → a local number matters for taxis, delivery, and messaging apps; prefer a real carrier plan over a data-only travel eSIM.
- Your home number receives banking 2FA texts → keep that SIM reachable (dual-SIM slot or eSIM) rather than pulling it; being locked out of your bank abroad is worse than roaming fees.

## Failure modes & recovery

- **F1 Phone rejects the SIM ("SIM not supported"):** the phone is carrier-locked → no local fix; contact your home carrier for an unlock, and use a pocket Wi-Fi rental or travel eSIM on another device meanwhile.
- **F2 Data dead despite signal bars:** calls work, websites do not → almost always the APN; apply step 7, confirm mobile data and data roaming toggles are on (some tourist SIMs technically roam on a partner network).
- **F3 SIM deactivated days later:** service stops mid-trip → usually incomplete ID registration; return to an official store of the same carrier with your passport and the packaging to re-register.
- **F4 Bundle exhausted, balance drained:** data suddenly crawls or credit vanishes → check whether overflow billed per-MB against your balance; top up and buy the next bundle explicitly rather than pay-as-you-go rates.

## Verification

With Wi-Fi off, a fresh website loads over mobile data; a test call connects; the carrier app or USSD code shows your balance and data remaining; you know the plan's expiry date and can state your top-up method; your home SIM is physically accounted for.

## Variations

- eSIM-first travel: purchase and QR-install before departure; nothing physical to lose, but customer service for eSIM issues is app-only.
- Countries with strict registration (fingerprints, local address, or resident-only SIMs): buy at official stores only; street-stall SIMs there are registered to someone else and are both unreliable and a liability.
- Dual-SIM phones: run the local SIM for data and calls, home SIM for incoming 2FA texts; label which slot is which in settings.

## Safety & privacy

Medium risk: your passport is scanned into a carrier's registration database (legally required; refuse resellers who want to keep a copy for themselves), and a lost home SIM can mean losing 2FA access to bank and email accounts. Set a SIM PIN on the local SIM if you will carry the phone in crowded transit, and never buy a pre-registered SIM tied to a stranger's identity.
