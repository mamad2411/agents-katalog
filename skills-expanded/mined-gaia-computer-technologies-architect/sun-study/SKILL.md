---
name: sun-study
description: Computes the sun's path for a site (altitude and azimuth through the solstices, equinoxes or any date, sunrise, solar noon and sunset in local clock time), draws a sun-path diagram, gives shadow lengths for a stated height, and summarises a weather file (EPW) for temperature, irradiation, degree days and prevailing wind, stating the station and its distance from the site. Always labelled as not a compliance calculation. Use when the architect wants a "sun path", "sun study", "where will the sun be", "shadow length", "winter sun angle", "solar orientation", "climate summary", "what does the EPW say", or inputs for passive design. Feeds site-context, concept-parti and massing-study; daylight or overshadowing compliance goes to a qualified assessor.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Sun Study

Put numbers on the sun early, so orientation, overhangs, courtyard proportions and the winter-garden idea are tested against geometry rather than intuition. It is fast, exact for sun position, and deliberately modest about everything else.

## When to use

- Concept and feasibility: orientation, shading depth, courtyard and street proportions, where the morning or evening sun lands.
- To answer a specific question: "will the garden get sun at 3 pm in March?", "how long is the neighbour's shadow at the winter solstice?"
- To summarise climate for a brief, a design statement or `site-context`.

## Input

- **Latitude and longitude** in decimal degrees, confirmed by the architect.
- **IANA time zone** (Europe/London, America/Chicago, Asia/Tokyo). Required, because clock times depend on it and on daylight saving. Never infer it from a country name for places with several zones.
- Optional: a **height** in metres for shadow lengths (a wall, a neighbour's eaves, a proposed block), extra **dates**, and an **EPW weather file** for the nearest representative station. EPW files are free from climate.onebuilding.org, the EnergyPlus weather pages and national met services. Pick the station yourself, and report its distance.

## Process

1. **Confirm location and time zone.** Repeat them back.
2. **Run the script.**
   `uv run scripts/sun_study.py --lat 51.51 --lon -0.13 --tz Europe/London --height 12 --epw london.epw --out out/sun`
   Add `--dates 2026-05-01,2026-08-15` for specific days. It writes `out/sun_sunpath.png/.svg` and `out/sun_report.md` and prints the report.
3. **Read the report.** For each date it gives sunrise, solar noon, maximum altitude, sunset, day length, and an hourly table of altitude, azimuth and shadow length. With an EPW it adds monthly temperatures, irradiation, degree days and wind.
4. **Translate it into design implications** (this is the part people want): the depth of overhang that cuts out summer noon sun but admits winter sun, the courtyard width that gets sun to the floor in March, the facade that takes low west sun in summer. Show the trigonometry behind each one: overhang depth = window head height above sill / tan(altitude). Keep the angles from the report.
5. **Keep the banner.** The report starts and ends with "not a compliance calculation". Leave it in any document it feeds.

## Domain knowledge

- **Altitude and azimuth.** Altitude is degrees above the horizon. Azimuth is measured clockwise from true north, so 180 is due south. Noon altitude at the equinox is roughly 90 minus latitude, and the solstices add or subtract about 23.4 degrees. Use that as a sanity check on the script's output.
- **Clock time is not solar time.** Solar noon can fall an hour or more from 12:00 because of daylight saving, the position within the time zone, and the equation of time. The report gives solar noon per date for that reason. Overshadowing work often uses specific clock times set by the standard. Check which times apply.
- **Southern hemisphere.** The sun is to the north. The script labels the June solstice as winter there. Design rules flip: north light is the prize and south light is the even one.
- **Shadows.** Length = height / tan(altitude), on flat ground, from a vertical edge. Below about 5 degrees altitude, shadows run to hundreds of metres and terrain, trees and buildings dominate. The report flags those rows. Sloping ground changes everything; say so if the site slopes.
- **True vs grid north.** Survey drawings often use grid north, which differs from true north by a degree or two. Rotate before overlaying azimuths on a plan.
- **EPW files** are "typical years" built from different real years, month by month. Use them for patterns (heating-dominated or cooling-dominated, the wet season, the prevailing wind), not to predict a specific summer. The station may be at an airport, kilometres away and at a different altitude or exposure. The script prints the distance and warns above 50 km. Urban sites run warmer than airport data suggests.
- **Degree days** depend on the base temperature (18 C here, set with `--base-temp`). Countries use different bases (15.5 C is common in the UK, 65 F in the US). State the base whenever you quote a figure.
- **What this isn't.** Daylight factor, spatial daylight autonomy, annual probable sunlight hours, overshadowing of amenity space, and rights of light are assessed to specific standards (for example BS EN 17037, the BRE guide BR 209 in the UK, or local planning rules) using measured 3D models and validated software such as Radiance-based tools. This skill informs design. It doesn't stand in for those assessments.

## Output format

```
## Sun study: [site], [lat, lon], [time zone]

> NOT A COMPLIANCE CALCULATION. Indicative sun geometry for early design only.

Files: sun_sunpath.png/.svg, sun_report.md

| Date | Sunrise | Solar noon | Max altitude | Sunset |
|---|---|---|---|---|
| [date] | [hh:mm] ([az] deg) | [hh:mm] | [alt] deg | [hh:mm] ([az] deg) |

Shadow of [12 m] edge at noon: [x m] (Dec) to [y m] (Jun)
Climate (EPW): [station, distance km] - [heating/cooling-dominated, prevailing wind, key months]

Design implications:
- [move] - basis: [angle, date, formula]

Not covered: [daylight/sunlight compliance, terrain, neighbouring geometry]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't guess location or time zone.
- Don't present shadow lengths or sun hours as a planning, daylight or rights-of-light assessment.
- Don't quote climate figures from memory. Use a named EPW or a named source, and state the station and its distance.
- Don't drop the not-a-compliance-calculation banner when the numbers move into a report.
