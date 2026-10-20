# pitch - local memory

Owner: abba, alongside the submission.
The current plan is `../plans/plan-d-louvre-roof.md`, the simulated smart louvre roof, and the guide for these files is `../plans/pitch-plan-d.md`.
Use the `hackathon-pitch`, `hackathon-readme`, and `hackathon-testing` skills, which are built from `../playbook.md`.
This folder is Markdown only, and a build agent never changes it.

## Where the pitch lives

`story.md` is written before anything else and every script is a cut of it.
`script.md` holds the 30 second, 60 second, and 3 minute versions, each inside the playbook's word target, with the count stated in the file.
The skill's `pitch_timer.py` was left in the planning repo on purpose, so the count is taken in an editor or with a new one line counter.
`storyboard.md` is the ninety second demo beat by beat, and it matches the table in the plan.
`questions.md` is the Q&A bank, `video.md` is the two video plan with its clock and shot list, `placards.md` is the four cards, `checklist.md` is rehearsal and the table routine, and `submission.md` is the form draft with the citations and the prior work statement.

## The story, as of the evening of 2026-09-19

- One sentence: What a plant needs depends on the state of its own bed, its crop, its stage, the season, and how wet its soil is, and a shade house gives every bed one number, so we simulate a roof of many small hingeless fins that gives each bed its own light, uses the rain where the soil is dry, and keeps it off where the soil is wet.
- The hero is a grower near Apopka, introduced as illustrative, and the opening line is "Picture Elena, a grower near Apopka, Florida."
  The name is the team's to change.
- How a roof like hers works today is said before anything else: the climate computer holds a daily light target and waters one valve at a time, and one motor pulls up to 50,000 square feet of curtain, "a fine brain, and a blunt hand".
- The general problem comes before everything: the University of Florida's table lists fifty crops with shade from thirty percent to ninety, croton wants thirty in summer and forty seven is too much in winter, and a shade house gives every bed one number.
- The villain is one number for every bed, so to change a plant's light she moves the plant.
- The storm has two halves: one bed uses the rain and one is protected from it, because water on saturated soil leaches fertilizer.
- Never said, because the sources contradict them: that irrigation is wasted, that motors or lamps are saved. The irrigation system stays.
- Why the fin: deciding bed by bed takes many small parts, every hinge is a bearing to grease, which is a documented chore, so the roof is made of a part with no hinge, ITKE's Flectofin, which also shades, opens for air, and lets the rain in as one element. No saving is quantified.
- The ask, said before the close: one grower near Apopka to tell us where it is wrong.
- The three specifics: 50,000 square feet a motor, from the UMass fact sheet; the fern's 8 mol a day against the hydrangea's 12, from Purdue; and the rain's share of the hydrangea zone's water, about 54 percent, from our own simulated run.
- The watched moment: the judge presses Play, 3 June 2023 runs in about forty seconds, the fern's zone shuts by eleven, the hydrangea's by noon, the blueberries stay open, and then the afternoon storm gets three answers, each with its reason in words.
- The closing line is abba's to write, and the scripts carry a working draft until then.

## No hardware, decided by the team lead on the evening of 2026-09-19

- Nothing physical was built, and nothing is on the table to hold.
- The judge touches one thing, the Play button.
- The plan's beat at 0:20 is used to say what a fin is: a hingeless fin, ITKE's Flectofin, patent EP2320015, credited, not ours.
- The question bank answers "Why is there no physical prototype?": the fin is an existing, published, patented mechanism, the team's contribution is the zone by zone control and the simulation, and nothing is claimed about the fin's mechanics.
- The plan, the demo gate, the rules, and the board were all updated the same evening and say the same.

## Honesty rules

- What is not ours is said unasked, before a judge can ask: the fin is ITKE's, the control logic is standard practice in greenhouse computers sold by Ridder, Hoogendoorn, Argus, and Priva, moving roofs over crops are sold by Cravo and Sun'Agri, growers keep rain off glasshouse crops on purpose, and nothing here is measured.
- What is ours is the size of the decision, a bed and not a building.
  The words are "we found no prior proposal to put a Flectofin over crops".
- Every figure is said as simulated or modelled.
  The rain is one real gauge's record, and the sun is a satellite product.
- The roof follows nine written rules, in the priority night, then rain, then light.
  No AI and no learned model is in the loop, and the fins never follow the sun's position.
- The structure is a shade house.
  The team may say greenhouse in plain speech, and anything written for the page says shade house.
- Shading blueberries is not Florida practice, and that figure is from Washington State.
- Every library, dataset, crop figure source, and AI tool is cited in the submission, because the rules require it.
- To a horticulture expert, concede before explaining.

## The words the team never says

These appear in this folder only inside lists like this one.

"First".
"Measured", as a claim about anything here.
"Maintenance free".
"Weatherproof".
"It works", of a simulation.
Any figure for cost, yield, energy, or water saved.
"No one does light or radiation based control".
"Greenhouses waste rain".
"We invented the fin".
In their place: "we found no prior proposal in our searches", "simulated", and "removes documented maintenance tasks".
The sources are in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.

## Figures

- Every simulation figure in this folder is provisional, from the planner's run in `../plans/packages/H1-zones-light-rain-soil.md`.
- The final figures come from `data/processed/headline.json`, which package H3 writes, and the sentences the speaker says come from the generated `pitch/figures.md` at the event repo's root.
- Nobody types a figure from memory, and if a figure is missing the file says "FIGURE NEEDED" and what.
- Each file ends with a short table saying which file each figure came from.

## When each thing is finished

| What | When |
|---|---|
| The story and the one sentence | now, because they need no figures |
| The three scripts, with the figures confirmed | after H3 is merged |
| The cards, the question bank, the screen recording | Sunday 07:00 to 09:00 |
| The README and the submission | Sunday 09:00 to 10:30 |
| The table routine in `checklist.md` | before every judge |

## Cuts that change the words

- The year not ready, which is allowed, because the demo day and the story come first: the two year sentences are swapped for the ones under "If the year is not ready" in `script.md`, and nothing else changes.
- H3 not merged: the same swap, the day ends on H2's plain table, and card 1 is left off the table.
- The year view cut: beat 7 of the storyboard closes on the result card.
- The roof layout file absent: the page says "default layout", and nothing spoken changes.
- The page fails: the recorded run, then the screen recording, with the same words.
