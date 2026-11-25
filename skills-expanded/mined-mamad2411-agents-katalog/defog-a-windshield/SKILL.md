---
name: defog-a-windshield
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

You clear interior fog from the windshield quickly and maintain visibility before driving or while driving.

## Preconditions

- The vehicle is stopped or moving slowly enough that adjusting climate controls is safe.
- The windshield, mirrors, and driver sightlines are checked before entering traffic.

## Steps

1. **Use the defrost mode.** Turn airflow to the windshield defrost icon. → *Expect:* air starts blowing at the base of the windshield.
2. **Turn on the AC with heat.** Use warm or hot temperature, AC on, and medium-to-high fan. AC dries the air while heat warms the glass. → *Expect:* fog begins thinning from the vent area outward.
3. **Use fresh air, not recirculation.** Turn recirculation off so humid cabin air is replaced with drier outside air. → *Expect:* clearing speeds up instead of fog returning.
4. **Clear side windows and mirrors.** Aim side vents toward front side glass and turn on rear defogger or mirror heat if equipped. → *Expect:* blind-spot visibility improves.
5. **Wait until you can see.** [BRANCH: parked | already driving] stay parked if visibility is poor; if already driving, slow down and keep both hands ready. → *Expect:* the forward view is safe enough for the speed.
6. **Handle exterior frost separately.** If ice or frost is outside the glass, scrape it off before driving; defog settings alone are too slow. → *Expect:* exterior glass is physically clear.
7. **Maintain the setting until stable.** Keep AC, heat, and fresh air on until passengers, wet clothes, or weather stop re-fogging the glass. → *Expect:* the windshield stays clear after the first clearing.

## Decision points

- Interior fog forms suddenly → reduce speed, use defrost, AC, heat, and fresh air immediately.
- Exterior frost or snow is present → stop and scrape; wipers alone can smear and damage blades.
- Windows fog more with recirculation on → turn recirculation off because trapped breath moisture is feeding the fog.
- Windshield stays greasy or hazy → clean the inside glass later; film makes fog harder to clear.

## Failure modes & recovery

- **F1 Fog gets worse:** detect: windshield clouds after changing settings, recover: turn AC on, recirculation off, and increase fan speed.
- **F2 Air is cold at first:** detect: heat is not available until the engine warms, recover: keep AC and fan on and wait parked when visibility is limited.
- **F3 Wiping smears the glass:** detect: towel or hand leaves streaks, recover: use defrost and clean the inside glass properly when stopped.
- **F4 Exterior ice remains:** detect: defrost clears inside fog but opaque ice stays outside, recover: scrape before driving.
- **F5 Rear view stays blocked:** detect: rear glass remains fogged, recover: turn on rear defogger and clear mirrors before merging or backing.

## Verification

The windshield and front side windows are clear enough to see lanes, vehicles, pedestrians, signs, and mirrors before normal driving resumes.

## Variations

- `automatic-climate`: Press the windshield defrost button; most cars automatically enable AC and fresh air.
- `manual-climate`: Set airflow to defrost, temperature hot, fan high, AC on, and recirculation off.
- `humid-summer`: Cool AC may clear fog faster than heat if outside air is hot and humid.
- `winter`: Scrape exterior frost and clear snow from the roof, hood, lights, and sensors before driving.

## Safety & privacy

Medium driving risk comes from reduced visibility. Do not drive by looking through a small cleared patch, and do not lean across the car to wipe glass while moving.
