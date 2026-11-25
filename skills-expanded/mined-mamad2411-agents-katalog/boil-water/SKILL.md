---
name: boil-water
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-20
---

## Goal

A container of water is brought to a full boil and is available for use (tea, cooking, sterilizing) without spills or burns.

## Preconditions

- A heat source: electric kettle, stovetop with a pot, or microwave-safe container.
- Potable water supply.
- A dry, stable surface near the heat source to set the hot container on.

## Steps

1. **Choose the method for the amount needed.** [BRANCH: electric kettle (fastest, ≤ its max line) | stovetop pot (any volume) | microwave (single cup only — see Variations for the superheating precautions)] → *Expect:* container capacity ≥ needed volume with ≥ 2 cm headroom.
2. **Fill with cold tap water to the needed level.** Kettle: between MIN and MAX marks. Pot: no more than 2/3 full. → *Expect:* water level within the safe marks; outside of the container is dry.
3. **Start heating.** Kettle: seat it on its base, close the lid, press the switch. Stovetop: pot centered on the burner, lid on, burner to high. → *Expect:* kettle switch light on / burner flame or coil visibly on; faint heating sound builds within ~1 min.
4. **Wait, staying within earshot.** Do not leave the building with a stove on. → *Expect:* progression of sound: quiet → hissing → rolling rumble; steam appears from the spout or lid edge.
5. **Recognize the boil.** Kettle: clicks off automatically. Pot: large bubbles break the surface continuously (a "rolling boil"); lid may rattle. → *Expect:* kettle switch has flipped off, or the pot shows a sustained rolling boil.
6. **Turn off the heat (stovetop) and move the container safely.** Use the handle; for a pot, lift the lid tilted *away* from your face to vent steam away. ⚠️ *Irreversible:* boiling-water scalds — never carry a full open pot across the room; bring the destination (cup, pan) near the kettle/pot instead. → *Expect:* heat source off; container resting on the dry stable surface.
7. **Use or pour the water at once.** Pour slowly, spout close to the target vessel. → *Expect:* target vessel filled without splash; remaining water left in the container, not in your path.

## Decision points

- Water is for drinking in a region with unsafe tap water → boil a full 1 minute (3 minutes at high altitude) before considering it sterilized.
- Kettle smells of scale/plastic → boil-and-discard one full load first.
- Induction stove with wrong pot (no click when set down, no heating) → switch to a magnetic-base pot.

## Failure modes & recovery

- **F1 Kettle doesn't heat:** check it is seated fully on the powered base and the outlet works; re-seat and retry once.
- **F2 Boil-over (foaming pot):** lift the lid off or kill the heat immediately — the foam collapses in seconds; wipe the stovetop after it cools.
- **F3 Forgot the pot and water boiled away:** kill the heat, do NOT add water to the glowing-hot pot (steam explosion / warping) — let it cool completely first.
- **F4 Steam burn risk at the lid:** always vent away from face and hands; if scalded, run cool (not icy) water over the skin for 10+ minutes.

## Verification

The water reached a sustained rolling boil (or the kettle auto-clicked off), the heat source is now off, and the hot container sits on a stable dry surface — no water on the floor or stovetop, no one scalded.

## Variations

- High altitude: water boils below 100 °C; extend boiling time for sterilization and cooking.
- Microwave method: use a microwave-safe cup with a wooden stirrer inside to prevent superheating; disturb the cup gently before removing.

## Safety & privacy

Medium risk from scalds and unattended heat. The two hard rules: never leave a stovetop unattended, and move the destination to the hot water rather than walking hot water across the room.
