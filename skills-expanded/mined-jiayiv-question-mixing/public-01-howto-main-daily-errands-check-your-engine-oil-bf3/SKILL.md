---
name: check-your-engine-oil
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

You confirm the engine oil level is between the minimum and maximum marks and top up with the correct grade if it is low.

## Preconditions

- The vehicle is parked on level ground with the engine off and cool enough to touch safely.
- You have a clean rag or paper towel, the owner's manual, and the correct oil grade if top-up may be needed.

## Steps

1. **Park safely and let the engine cool.** Use level ground, set the parking brake, turn the engine off, and wait several minutes after driving. → *Expect:* the car is stable and the engine bay is not dangerously hot.
2. **Open the hood and locate the dipstick.** Look for a colored loop or handle labeled engine oil; check the manual if unsure. → *Expect:* the dipstick is identified, not the transmission dipstick.
3. **Pull and wipe the dipstick.** Remove it fully and wipe oil off with the rag. → *Expect:* the metal blade is clean enough for a fresh reading.
4. **Reinsert and seat the dipstick fully.** Push it all the way back into its tube, then wait a moment. → *Expect:* the dipstick is seated at its normal depth.
5. **Pull it again and read the level.** Hold it horizontal and look where the oil film reaches relative to Min and Max, Low and Full, or the crosshatched zone. → *Expect:* the oil level is visibly between, below, or above the marks.
6. **Decide whether to top up.** [BRANCH: between marks | below minimum | above maximum] leave it alone if in range, add oil if low, and do not drive hard if overfilled or very low. → *Expect:* the next action matches the reading.
7. **Add small amounts only if low.** Open the oil-fill cap, add the manual-specified grade in small pours, wait, and recheck with the dipstick. → *Expect:* the level moves toward the middle or upper part of the safe range.
8. **Close everything cleanly.** Tighten the oil cap, seat the dipstick, remove the rag, close the hood, and wipe spills. → *Expect:* no tools or rags remain in the engine bay.

## Decision points

- Oil level is below minimum → add the correct grade before normal driving and check soon for leaks or consumption.
- Oil level is above maximum → avoid adding more; if far above, have oil removed because overfill can damage the engine.
- Oil looks milky, foamy, gritty, or smells strongly of fuel → stop treating this as a simple top-up and get mechanical advice.
- No dipstick is present → some cars use an electronic oil-level menu; follow the owner's manual conditions exactly.

## Failure modes & recovery

- **F1 Reading is smeared:** detect: oil covers the blade unevenly, recover: wipe, reinsert fully, pull again, and read both sides.
- **F2 Car is not level:** detect: parked on a slope or curb, recover: move to level ground and wait before checking again.
- **F3 Wrong fluid cap:** detect: cap label does not show engine oil or the location differs from the manual, recover: stop and identify the correct oil-fill cap before pouring.
- **F4 Overfilled after topping up:** detect: oil reads above Max, recover: do not add more and arrange for excess oil removal.
- **F5 Burns or moving parts risk:** detect: hot metal, fans, belts, or engine running, recover: close the hood and wait until engine-off-and-cool safety is restored.

## Verification

With the engine off, cool, and the vehicle level, the dipstick oil film reads between the Min and Max marks after a wipe, reinsert, and reread.

## Variations

- `hybrid`: The engine may start unexpectedly if the vehicle is on; make sure the vehicle is fully off before opening the hood.
- `electronic-oil-level`: Follow the dashboard menu and warm-up conditions in the manual instead of using a dipstick.
- `diesel`: Oil may look dark soon after a change; level and texture matter more than color alone.
- `cold-weather`: Oil pours slowly, so add smaller amounts and wait longer before rereading.

## Safety & privacy

Medium physical risk comes from hot surfaces, fans, belts, spills, and driving with too little or too much oil. Never check oil with the engine running unless the owner's manual specifically says so for a different fluid.
