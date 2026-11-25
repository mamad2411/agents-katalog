---
name: frontend-design
description: "Design and build a website or application screen that works like a product and looks like somebody chose it, from a brief as short as “build a website for a bike shop.” Use for new sites, pages, dashboards and visual redesigns. For a narrow UI repair, preserve the existing identity."
---

# Frontend design

## What this method corrects

Given a short brief, a model misses in one of two ways.

- **The brochure.** A slogan, one picture, two buttons, a strip of three facts and a contact block, on one page. It can look good and there is nothing to do on it.
- **The bare page.** Told to add substance, a builder makes working pages out of small gray controls with one small photograph. There is plenty to do and nothing to look at. An owner shown one beside a brochure preferred the brochure.

Eight production sites that this project's owner holds up as the bar were studied page by page on 2026-11-21. They do both things at once. Measured at 1440 × 900 with the [probe](scripts/first-screen.mjs):

| First desktop screen | The eight sites | A generated brochure | A generated bare page |
| --- | --- | --- | --- |
| Things to act on | 14 to 89 | 7 to 11 | 36 |
| Other pages linked from the home page | 7 to 293 | 0 or 1 | 5 |
| Pictures | 4 to 30, or one covering 29% to 86% of the screen | 1 to 3, the largest covering 26% to 35% | 1, covering 9% |

They also do not look alike. Five sit on white, one on warm cream, two on near-black. One has no headline at all, one sets it light at 40 px, one sets it at 88 px in the heaviest weight. Each made a small number of choices from its own subject and held to them.

So the work has three parts and none can be skipped: what the site holds and lets a visitor do, what it shows, and a look that was chosen. Work in the order below.

## Step 1. Write the inventory before any visual decision

Start `design/decisions.md` (or the run directory when the project forbids new files) from the [decision sheet](references/decision-sheet.md). Fill these first:

- **Visitors and jobs.** Two or three kinds of visitor and what each came to do. A first visit and a return visit are different jobs.
- **Pages.** For a whole site, plan the real destinations its visitors need. For a one-page brief, first slice or repair, list the in-scope views or in-place states. Stay within that scope.
- **Records.** The things a visitor chooses between, with the facts they compare. A broad demo catalog can use a dozen realistic records to exercise comparisons. For a real inventory or a bounded first view, use the available records and the facts that decide the choice.
- **Visual evidence.** Inventory the actual material that settles the visitor’s question: a scene, equally framed items, a worked example, the interface, or dated and comparable records. List useful photos and their provenance. Use a written fact where a photo cannot communicate the difference.
- **One working journey.** A task a visitor can finish on the site: search and filter, book a slot, build an order, check a status. Give it a start, a choice, a confirmation, an empty state and an error state. Label local or demo behavior where a visitor could take it for a real save.
- **What is true now.** Open or closed, the next date, what is available, how long it takes. Compute it from the data.
- **Proof.** Specific and checkable: a named job with its price, a plan table with limits, a dated event. Never an invented statistic or testimonial.

In an existing project, read the real pages, data and brand assets and use them. Ask only when a missing fact would change the structure. For a fictional or thin brief, invent plausible, specific data, keep it in one data file, and tell the owner which facts are invented.

## Step 2. Choose the site model and its patterns by the visitor's job

Open the decision table in the [frontend field guide](references/field-guide.md) and read the chapter or subsection that fits this surface. For a short brief, infer the visitor’s decision from the project and its inventory. Choose the practice that changes what you would build; add another when the journey presents a different decision. Use the [site models](references/reference-standards.md) for anatomy once you know which evidence belongs first. A campaign, a catalog and a working view within one product can have different openings.

| The visitor came to… | Model | First screen holds |
| --- | --- | --- |
| Find one option among many | Finder | Editable search and comparable items. A photograph with the finder can lead when the scene itself helps the choice |
| Buy from a catalog, here or today | Store | Store and fulfillment context with items, categories or the offer that materially affects the purchase |
| See a collection and choose a style | Campaign | Category navigation, then one large photograph with its offer on it |
| Resume a task, or explore an offer | Front door | The returning task in reach, with a distinct route for newcomers to inspect the offer |
| Judge whether software fits | Product showcase | A short claim, then the real product at readable size |
| Keep working inside the product | Working surface | The working screen itself, with real content |
| Decide whether a service can deliver | Proof-led service | An inspectable result or before-and-after with the evidence behind it. Show the person at work when that helps establish trust |
| Join something with a next date | Gathering | A photograph of the people, the invitation and the next date in one view |

Then open [patterns](references/patterns.md) for the controls and composition that serve that decision. In the project sheet record the field-guide **chapter and practice**, the visitor’s question, the **actual asset, record or control** that answers it, and the **observable outcome after acting and on return**. Choose the phone priority and keyboard or other access need here. If the opening could equally be a scene, a set of choices or a working example, name what the alternative would hide. The builder makes this choice from the brief and evidence.

Write one more line in the sheet: the page you would have built for this brief without this method. Check the plan against it. If the plan is that page with different type and color, go back to Step 1. For its look, use the measured default in Step 3, not a guess.

## Step 3. Choose the look from the subject

A look is five choices. Make each from this subject, give it a reason no other kind of business would give, and write it in the sheet. An existing brand system replaces the choices it covers: record it and hold the work to it.

| Choice | Options seen on the studied sites | Where it is set out |
| --- | --- | --- |
| Canvas | White · warm tint · dark | [Color](references/color.md#canvas) |
| Type voice | Quiet · light · editorial serif · large grotesque · heavy · display on photographs | [Typography](references/typography.md#voices) |
| Corners | Nearly square, 2 to 4 px · soft, 10 to 20 px · full pills. One family for controls and one for pictures | [Craft rules](references/craft-rules.md) |
| Color source | One brand color used in fields · the photographs · the content · artwork · a two-color palette · a campaign palette | [Color](references/color.md#where-the-color-comes-from) |
| Signature move | One or two details taken from the subject and repeated down the page | Below |

**Signature moves.** Every studied site has one or two things no other site there has: small illustrated icons on its category tabs; headlines set thin instead of bold; the offer set in display type on the photograph; a painted backdrop behind every product frame; flat category tiles in a dozen saturated colors; one handwritten phrase in the headline with a drawn underline; a key word on a block of the brand color with a solid offset shadow behind photographs. Do not reuse these. Find the equivalent in this subject: the stripe of a barber's pole, a ticket stub, a chalk menu, a route map, a seed packet, a tool's handle color. Use it in the first screen and at least twice more.

**Move off the unguided look.** Built from one-line briefs without this method, three of three sites set the page background to cream or paper (#f4eee3 to #f6f3ee), and two of them set the headline in Fraunces. Builders using the method, asked to predict their own page, guessed a dark page with gold; then one of them chose an ivory canvas and a serif headline itself. So hold the look against that measured default, not against your guess: do not pair a warm tint with a serif headline unless an existing brand sets both. Either one alone is a choice. Write in the sheet how your look differs from it. The judge in Step 4 fails the pair; `--brand` turns that into a note when a brand you were given sets them.

**Vary it.** When the look you are about to write is the one you wrote last time, change the canvas or the type voice. For several sites in one request, no two share both.

Use the following observations to develop the chosen opening. The project’s existing identity and the work of this particular screen determine which treatments fit.

- **Compose the opening around the evidence.** Relate the headline, crop or record layout, color emphasis and next action to one another. For a scene-led opening, use [the opening photograph](references/visual-material.md#the-opening-photograph). For a comparison, protect the facts and the edges that distinguish the options.
- **On a visual public homepage, pictures fill the first desktop screen:** four or more, or one covering at least a quarter of it. Photographs of real people and real things, framed alike within a set. See [visual material](references/visual-material.md).
- **Pictures reveal differences.** Match the framing of items compared by appearance. Align dates, units or status in rows when those decide the choice.
- **One color does the main action.** The second button is outlined, pale or plain text.
- **Main buttons are 44 to 56 px tall.** Body text is 14 to 20 px. Navigation and labels are 12 to 16 px.
- **Size type for the reading task.** A single invitation can support a dominant headline. Use a compact page heading for a timetable, a finder or shelves of choices when room for comparisons matters more.
- **Navigation is three to nine plain words,** with sign-in or the main action at the right end, and a skip link first.
- **The main action stays in reach:** a pinned header on long pages, and on a phone the header or a bottom bar.
- **Numbers and facts instead of adjectives,** and reassurance beside the action.
- **Repeated items are built identically,** each fact in the same place.
- **Motion is short:** 0.15 to 0.35 s.

One more is not a choice and comes from WCAG 2.2 AA, not from the studied sites: **everyone can use the page.** Every picture of an item says in its alt what the picture shows. Every field has a label a visitor can see. Everything a visitor taps is at least 24 px each way or has space around it. Every control changes visibly when it takes focus. Text meets contrast against what it sits on, a photograph included. The judge in Step 4 counts each of these.

## Step 4. Build the first screen and the journey, then measure

Reopen the project sheet’s selected practice at the beginning of the build or a handoff. Implement the material, its position, and the first transition together using the same record, variant or criteria at the destination. Put the information that resolves doubt beside the choice. Preserve state and focus when someone backs out. For an accessible claim such as step-free access, distinguish known, unknown and unavailable using real data.

Build the first screen and its journey in the real project. Choose the judge mode from the purpose recorded before markup. Use the full judge for a visual public homepage, adding `--one-page` for a single-page brief. Use `--access` for a deliberately text-led working view driven by times, numbers or status. Inspect its records, reading order and primary action at both widths. Keep the full check for any visual public home in the same project. Render at 1440 and 390 wide. At each width, with the page at rest and scrolled to the top: evaluate the probe and keep its result; evaluate the `--mark-text` expression and take a full-page screenshot; evaluate the `--hide-text` expression and take a second full-page screenshot. Save the two results as `{"desktop": …, "phone": …}` and the screenshots as PNG files, and judge them. Run the script from this method's folder and give it the paths in the project:

```sh
# <mode> below is empty for a full site, --one-page for a visual single page,
# or --access for the text-led working view described above.
node scripts/first-screen.mjs --probe
node scripts/first-screen.mjs --mark-text
node scripts/first-screen.mjs --hide-text
node scripts/first-screen.mjs <mode> <project>/design/first-screen.json \
  --marked desktop=<project>/design/desktop-marked.png --hidden desktop=<project>/design/desktop-hidden.png \
  --marked phone=<project>/design/phone-marked.png --hidden phone=<project>/design/phone-hidden.png
```

| Floor | Value |
| --- | --- |
| Things to act on in the first desktop screen | 12 |
| Things to act on in the first phone screen | 6 |
| Other pages or views linked from the home page | 3 |
| Height of the home page, in screens | 3 |
| Pictures in the first desktop screen | 4 |
| Or one picture covering this share of it | 25% |
| Tap target, px each way, unless nothing else is within reach | 24 |
| Text contrast against its background, to 1 | 4.5 |
| Contrast for text from 24 px, to 1 | 3 |
| Text on a photograph: share of its letters that must meet contrast | 90% |

A first screen with twice the floor of things to act on (24 on a desktop, 12 on a phone) is a working surface: it may scroll inside the screen or load as the visitor scrolls, and its height is not judged. The judge also reads which kind of surface holds the most text (a warm tint, white or a neutral light, dark or coloured, pictures) and the typeface of the largest text in the first screen, and fails a warm tint under a serif headline, the look builds without this method chose; judge with `--brand` when an existing brand you were given sets both. The probe counts links, so a link to a page not yet written still counts; the measurement that stands is the one taken in Step 5, when every linked page exists.

The same probe counts access over the whole page, at both widths, against WCAG 2.2 AA. The judge fails a page with no language or title, an image with no alt attribute, a field with no label, a link or button with no name, a tap target under 24 px with another target within 12 px of its centre, a control that looks the same focused and unfocused, or text below contrast on a solid background. It reports without a verdict pictures whose alt is empty and buttons and fields under 44 px tall. To read focus the probe focuses each control in turn and then puts focus and scroll back, so run it on a page at rest.

Text on a photograph, a gradient or a see-through surface is measured from the two screenshots. The marked one paints every letter magenta and the hidden one makes every letter transparent; neither moves anything, and both wait for lazy images to load. The pixels that differ are the letters, and the hidden screenshot holds what is behind them, scrims, panels and text shadows included. The judge fails a piece of text when its colour falls below contrast behind more than a tenth of its letters, and names it. WCAG gives no method for a photograph; this rule is the method's own. Text the screenshots do not show, such as a row that scrolls sideways, or where the page changed between the two shots, is reported without a verdict. Without the screenshots the judge only counts such text.

Any FAIL keeps the work open. Repair a brochure with substance from the inventory: real navigation, records, the task entry. Repair a bare screen with the photograph, the items or the product from the chosen opening. Repair the unguided look by choosing again from the subject: a white or dark canvas, or another type voice, and update the sheet. Padding the page with links, small chips or decorative images to pass is the same failure, and the floor is the least a page can do, never the aim: the studied sites sit far above it. Repair an access FAIL at its cause: write the alt, add the label, give the row its height, draw the focus ring, darken the text. For text on a photograph, put it on a solid panel, deepen the scrim where the text sits, or move it to the photograph's calm side; [the opening photograph](references/visual-material.md#the-opening-photograph) says how. Hiding a control from a screen reader, or from the probe, to shrink a count is the same failure.

At the first render, find the promised material on desktop and phone, then follow the chosen item or action by keyboard. Record the route, observed state and return focus in the sheet. If the phone crop loses the subject or the destination drops the choice, repair and repeat before extending that pattern. Then look at the render as the owner would:

1. Identify the first thing you can inspect at normal size. A scene, comparable items, a worked example or a real task with its records should answer the question in the sheet. A wall of equally weighted controls that hides that material needs repair.
2. Would you know what kind of business this is with the words blurred?
3. Is the signature move visible without scrolling?
4. Put it beside your “without this method” line. Name what a visitor can do here that they could not do there, and say honestly which of the two looks better. If that page would look better, the look is not finished.
5. Use the journey with the keyboard: reach the main control, activate it, read the next state.

Score it with the [generic tells](references/generic-tells.md#score-sheet).

## Step 5. Finish every page and review

Give each page or state its own job and the material that job needs. Keep navigation and comparable facts consistent. Repeat the applicable Step 4 check for the finished home page. Compare the rendered result and the journey against the selected field-guide practice in the sheet. If a real constraint changed the decision, record what changed and recheck the revised path. Keep the observed result with the sheet. Evaluate the probe on every other page at both widths and judge each result with `--access`, which prints the access lines alone; an access FAIL on any page keeps the work open. Run the [experience review](references/experience-review.md) on the journey at desktop and phone widths, including its access pass, and apply the [UX foundations](references/ux-foundations.md) and [craft rules](references/craft-rules.md). A known accessibility failure in the journey keeps the work open. [Layout archetypes](references/layout-archetypes.md) offer compositions for a section once its content is decided.

For several unrelated sites, choose each one's model, inventory and look from its own visitors and subject. Two sites differ when a visitor does different things on them and when they would not be mistaken for each other at a glance.

## Scope

A narrow repair stays narrow and keeps the existing identity. A request for critique or concepts stays a critique or a concept. Keep the user's criterion count: the floor and the rejection condition in the sheet are conditions of the visual criterion, not extra criteria. When the brief states no criteria, the sheet's rejection condition is the visual criterion. The floor catches a brochure and a bare first screen. It does not measure taste, and passing it is not evidence that the design is good. The owner's eye on the rendered page is the verdict.

## Handoff

Give the owner the working site, the desktop and phone renders and the probe result. Say which facts are invented, which photographs are placeholders to replace, and which behavior is a local demonstration. Explain one choice by pointing at something visible. Carry the sheet, the renders, the probe result, the tells score and the review findings through [Build](../../cyc-build/SKILL.md) and [Verify](../../cyc-verify/SKILL.md), and keep the sheet with the project for its next change.
