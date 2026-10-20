# software - local memory

Owners: abba for G1, H2, and H3, and Ameya for S1 and H1.
This folder is planning, Markdown only, and the code lives in the repo's own `tools/`, `data/`, and `software/` directories.
The plan is `../plans/plan-d-louvre-roof.md`, the specifications are under `../plans/packages/`, and `README.md` in this folder says how the parts connect.
This file holds what is already decided, why, and the traps.

## Decisions that bind the software, and their reasons

- **Everything is simulated.**
  The team could not source hardware, so nothing reads a board, a port, or a sensor, and there is nothing physical at the table.
  The project is purely the simulation and its page, and the judge touches one thing, the Play button.
- **The fin is still credited.**
  The simulated roof is made of ITKE's Flectofin, patented as EP2320015, so the page says so.
- **Nine written rules, in the priority night, then rain, then light.**
  The priority is the answer to "opening for rain also lets light in".
  No language model and no learned model sits in the loop, and the fins never track the sun's position.
- **The simulation runs before the page exists.**
  The order G1, S1, H1, H2, H3 gets a running simulation first, so there is always something to show.
- **The page adds no physics.**
  Every number it shows was computed by H1.
  `build_day.py` decides the words, the fin moves, and the gauge values in Python, where they can be tested, and the JavaScript only interpolates between hours and draws.
- **The words for each state are fixed in H2's table**, so the screen and the speaker agree.
  Nine values, and a test asserts every `words` value is one of them.
- **Plain HTML, CSS, and vanilla JavaScript, served by `python -m http.server`.**
  No web framework, no library, no CDN, no web font, because the demo laptop must work with the network off and gate F3 fails on any external address.
  A static copy of the same folder goes on Vercel for the live link, and that changes nothing in the code.
  Next.js and Supabase were considered on Saturday evening and set aside, because nothing is stored and nobody logs in.
- **The year view is inline SVG drawn by hand.**
  No chart library.
- **`headline.json` is the one source of every spoken and printed figure.**
  `pitch/figures.md` is generated from it and never edited by hand, and gate F8 checks the card against it.
- **The rain's share is given for the year only.**
  A month with no irrigation event would read as 100 percent and mean nothing, so the months show the two amounts.
- **The layout file changes the drawing and nothing else.**
  The simulation treats a zone's roof as one open fraction and never reads `data/roof-layout.json`.
- **The demo day is 3 June 2023.**
  H1's planner ran the rules on it hour by hour: the story happens with no constant tuned, and three zones give three different answers to the same rain.
- **Laptop layout only, 1440 by 900.**
  The mobile layout item of the UI checklist is dropped on purpose, because the page lives on one laptop.

## Traps

- H2 and H3 were written against H1's schema before H1 had run.
  If H1's real output differs from its schema, settle that first, and do not bend the page around it.
- The blueberry's RAIN_SHUT on the demo day rests on a margin of 1.2 mm of soil water, 31.17 against a threshold of 30.
  The test asserts it and carries a comment that says so.
- The hydrangea's second rain hour flipped to shut in one of seven runs when the evaporation was scaled by 0.95.
  The expected values stand as written, and a mismatch is reported, never patched.
- The first rain hour, 23.9 mm, is 1.1 mm under the 25 mm hard rain cap.
  That is the gauge's reading, and nothing was tuned.
- The backup days each flipped under a change of 1 to 3 percent, so they are never asserted and never promised to a judge.
- Before Play there is not one digit on the page, which is beat 1 of the demo gate.
  The date, the clock, and any footer line that holds a digit have to respect that.
- A fin changes over 1.5 seconds at the hour boundary, and never faster.
  The screen shows a slow roof.
- The blueberry has no light target.
  Its gauge shows the light received with no target mark, and says "shade rule".
- HEAT_SHADE does not occur on the demo day, because the peak is 29.84 C, but it occurs in the year, so its words and its partly shut drawing still have to exist.
- The word "measured" is allowed once, inside the rain source line, where it is true of the gauge.
  Everywhere else the word is "simulated" or "modelled".
- Leaving `T_STRUCT`, 0.90, out of the crop's water use changes every figure in the year table.
  That is how it was caught in planning, and it is the first thing to check if the year does not match.
- A gate that checks something that does not exist yet reports NOT YET, never PASS.

## What not to build

- Any package that is not G1, S1, H1, H2, H3, or K2.
- Any reader for a port or a board, any recorder, any live stream to the page.
- A web framework, a chart library, a build step, a mobile layout.
- A second city, a city picker, forecasts, wind, hail, leaf wetness, growth stages.
- The ray cast shade table, or partial fin angles beyond rule 7.
- Any figure for cost, yield, energy, or water saved, anywhere.
- A stand in for a package that is not merged yet.
  Say you are blocked, and take the next package that is not.

- A display fin, a CAD package, or anything else physical.
  Package K1 was cut, and the plan, the checklist, and H2 are being updated to say so.

In if time allows, and only after H3: a second view that draws the roof's fins one by one.

## The clock, for the software

- 21:00 Saturday: G1 and S1 merged.
- 23:00 Saturday, the hard checkpoint: H1 merged and the year's summary exists, and if it is not, the page is cut to the demo day only.
- 01:00 Sunday, the freeze: H2 plays the demo day end to end, or the fallback is a recorded run of H1's output drawn as simply as possible.
- 07:00 to 09:00 Sunday: H3, the pitch figures read from `headline.json`, and the screen recording.

## Open questions

- Which committed file is the "recorded run" the fallback gate asks for.
- Two questions in H1 are the team's to answer and do not block the build: a soil bucket sized for containers or for soil, and whether the hydrangea stays.
