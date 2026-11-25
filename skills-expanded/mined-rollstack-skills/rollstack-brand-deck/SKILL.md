---
name: rollstack-brand-deck
description: Give a Rollstack slide deck a brand's colours and fonts with the Rollstack MCP tool updateReportTheme, then fix the slides the change made wrong. Use when the user asks to brand a deck, match their company's look or a presentation they gave you, or change a deck's colours or fonts.
license: MIT
---

# Rollstack brand deck

1. Find the report with `listReports`. It must be a slide deck (type `SlideDeck`).
2. Call `getReportDesign` for the report, without `layoutIds`, to read its theme slots and what each one does.
3. Work out the brand's colours, from what the user names or from a presentation or site they gave you, and send each in the slot whose job it does with `updateReportTheme`, in `colors`: the dark text colour in `dark1`, the background in `light1`, the main brand colour in `accent1`. Send the fonts by their published names, in `headingFont` and `bodyFont`.
4. A change that would leave text unreadable, or a font the editor does not have, changes nothing and answers `refused: "invalid"` with what to fix. Fix it and send it again. One answered `refused: "needs-agent"`, such as swapping a deck with background pictures from light to dark, only Rollstack's slides agent can make: ask the user whether to hand it over with `sendReportMessage`.
5. Call `getReportDesign` again, so the slides you write next use the colours as they are now.
6. On a deck that already has slides, look at each with `getReportSlideImages`. A new font sets text wider or narrower: fix the slides whose text no longer fits as the `rollstack-edit-deck` skill says.
7. The theme holds colours and fonts only. For a presentation's layouts and logo, tell the user to import it as a template in Rollstack, then switch the deck to it with `applyReportTemplate`.

The change answers a `versionBeforeId`: restore it with `restoreReportVersion` when the user wants the old look back.
