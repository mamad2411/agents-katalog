# data - local memory

Owner: Ameya, with packages S1 and H1.
This folder is planning, Markdown only, and the data and its build scripts live in the repo's own `data/` directory.
The provenance table is `README.md` in this folder, and the specifications are `../plans/packages/S1-solar-2023.md` and `../plans/packages/H1-zones-light-rain-soil.md`.
This file holds the decisions about the data, their reasons, and what is still open.

## What the repo's `data/` directory holds

- `data/raw/` holds the two downloaded files and is ignored by git.
  A person copies each file in and checks its sha256.
- `data/build_solar_2023.py` is S1's build script.
- `data/crops.csv` and `data/roof-layout.json` sit at the top of `data/`.
- `data/processed/` holds the files the software reads, and it is committed.
- Every build runs with the network off and gives identical bytes on two runs.

## Decisions, and their reasons

- **The sun is NASA POWER for 2023, a real year, and not a typical year.**
  A typical year of sun, stitched from several years, was considered and joined to one real year of rain.
  A check on real files showed what that does: the rainy daylight hours came out brighter than the dry ones, by a ratio of 1.11, because the two had nothing to do with each other.
  With the sun from the same year as the rain, rainy hours are darker, as they are outside: the ratio is 0.627 for this file.
  A demo where rain falls under a clear sky is wrong in a way any judge can see.
- **`pvlib` is not needed.**
  Nothing in this plan uses the sun's position, because the roof reacts to how much light arrives and not to where the sun is.
  So it is not a dependency, and no package may add it.
- **The rain is one real gauge, Orlando Executive Airport, NOAA ISD station 72205312841.**
  It was chosen from four gauges near Apopka as the most complete: 8,760 hourly reports with 2 lacking the rain field, against 13 missing hours at Orlando International, 35 at Sanford, and 25 at Leesburg.
- **The sun is requested at the gauge's own coordinates**, so the two files describe the same place and the same hours.
- **NASA's own precipitation column is never used.**
  It is reanalysis, and it has 4,395 wet hours where the gauge has 373.
- **Apopka, because the University of Florida says so.**
  Its research centre there describes itself as "Located in the heart of Florida's greenhouse and nursery industry", and shade houses are the practice there.
  Phrases seen only in search snippets, such as any "capital of the world" title, are never said.
- **Both files stamp the start of the hour**, so the join is on `time_utc` with nothing shifted.
  Local days and local hours are America/New_York.
- **The demo day is 3 June 2023**, chosen in H1, where the rules were run on it hour by hour.
  31 days between April and October have at least 5 mm of daytime rain after at least four bright hours, so there were plenty to choose from.
- **The expected values were computed from the real files before any code existed.**
  If one does not match, stop and report it, and never edit the value.

## Traps in the rain file

- FM-16 special reports repeat the running hourly total, so summing every FM-15 and FM-16 value gives 3,728.5 mm, nearly three times the truth.
- The `SOD` rows hold 24 hour totals, and `REPORT_TYPE` values carry trailing spaces.
- A trace always has depth 0, in 307 rows, and a missing depth is 9999.
- The rule: FM-15 rows only, `AA1` with period 01, depth not 9999, floor the time to the UTC hour, keep the last row in each hour, divide by 10, and a missing hour becomes 0.
  The parser keeps its guard for two FM-15 rows in one hour even though this file has none.
- The 2 missing hours are `2023-07-30T22` and `T23`, and that day's own daily summary equals its hourly sum, so no rain was lost.
- One day disagrees with the station's daily summary by more than half a mm: 2023-04-28, 4.3 in the summary against 0.0 hourly.

## Traps in the sun file

- 13 header lines are skipped, and the column row is line 14.
- The missing value code is -999.
  The header's text mentions it and the data holds none, and the build fails loudly if one ever appears.
- Wh/m^2 over one hour is the mean W/m^2 for that hour, so there is nothing to convert.
- NASA may stamp a new date into the header when the file is fetched again, which changes the sha256 and nothing else.
  If only that differs, check the 8,760 rows against the sums in S1's tests, and carry on.
- That the stamp labels the start of the hour rests on a fit, not on a sentence found on NASA's pages.
  It matters here only for joining to the rain.

## Known caveats, said on the page and in the README

- The sun is a satellite product for a cell about 100 km across, 1 degree for the irradiance, so a local storm can rain under a bright cell.
  The example: on 29 July 2023 the gauge caught 11.2 mm in an hour while the satellite cell read 681 W/m2.
  The page says the sun is modelled.
- The light constant, `K = 2.0565`, uses 0.45 inside a verified range, and the range seen in the field is lower, so light sums may read 5 to 18 percent high.
- The blueberry's 40 percent shade is a heat figure from Washington State, and shading blueberries is not Florida practice.
- The fern and the hydrangea have no row in FAO-56 Table 12, so their `kc` of 1.00 is ASSUMED.
- The soil bucket, `T_STRUCT`, `T_CLOSED`, the three hour drying rule, the 25 mm hard rain cap, and the 32.2 C trigger are all ASSUMED.
- The soil latch makes the year's results depend on the path, so the year's assertions carry tolerances: shares within 0.03, days within 3, state counts within 5 hours.

## Still to confirm at a source

The evaporation formula in H1 is marked RECALLED, which means nobody confirmed it at a source: `ET0 = 0.65 x D / (D + g) x (ghi x 3600 / 1e6) / 2.45`.

- Not confirmed: the Makkink form itself, its 0.65 coefficient, and the 2.45 MJ per kg divisor.
- Confirmed, from FAO-56 chapter 3: equations 13, 8, and 7, for `D`, `g`, and `P`.
- If there is a spare ten minutes, confirm the three at a source and record the address in the README.
- Until then, every evaporation figure carries the RECALLED label, and the formula is never edited to make a value match.

Also to confirm: the licence of the NOAA ISD file, believed public domain, and the exact addresses of the EDIS documents EP149, EP550, and HS742, which the build agent records when it opens them.

## Open questions for a person, which do not block the build

- A soil bucket sized for containers or for soil.
  A container holds far less than 60 mm, so a smaller bucket would mean more frequent rain openings and more irrigation events.
- Whether the hydrangea stays, or a second foliage crop from the same Purdue table replaces it.
  The backups are Dracaena, Aglaonema, and Dieffenbachia at 8 to 14, Schefflera from 14, and Ficus benjamina and Croton from 18.

## What not to build

- A second place, a typical year, forecasts, the sun's position, or the ray cast shade table.
- Any package that is not G1, S1, H1, H2, H3, or K2.
- Any download at build time.
  The raw files are copied in by a person, and the tests patch `socket.socket` to raise.
