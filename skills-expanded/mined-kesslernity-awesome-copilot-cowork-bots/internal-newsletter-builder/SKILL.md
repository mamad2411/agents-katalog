---
name: internal-newsletter-builder
description: Builds a dated internal newsletter draft from the period's real material, every item sourced to the thing it describes, with nothing invented to fill a section. Use when the user asks to draft the internal newsletter, build the team update, prepare the monthly round-up, or says the newsletter is due.
---

# Internal Newsletter Builder

Builds the round-up from what actually happened, and leaves a section out rather than filling it.

## Inputs
- **Enterprise Search**, **Email** and **Meetings** over the period
- `references/config.md` for the sections, the audience and what is never included

## Procedure
1. **Gather** the period's material: shipped work, decisions taken, documents published, meetings
   that produced an outcome, new joiners if config allows it.
2. **Place each item in exactly one section** from config. An item that fits none is dropped, not
   relocated into the nearest.
3. **For each item, write**: one sentence on what happened, one on why it matters to this
   audience, and the link. **No item without a link.**
4. **Leave empty sections out of the draft entirely.** Do not write "nothing to report this month"
   under a heading: delete the heading. A newsletter with four real sections reads better than
   seven with three apologies.
5. **Apply the exclusions** from config before drafting, not after.
6. **Mark the whole thing DRAFT** and hand it to the user.

## Output
A Word document in the configured section order, every item carrying its link, empty sections
absent, with a closing line stating the period covered and how many items were considered.

## Definition of done
Every item is linked and sits in one section, excluded material is absent, and no section exists
without content.

**A thin month produces a thin newsletter.** If there are three items, the newsletter has three
items. Padding is how an internal newsletter dies: readers learn it is mostly filler and stop
opening it, and then the one month that mattered is missed too.

## When there is no data
- Almost nothing found: say so and suggest skipping the issue. Suggesting not to publish is a
  legitimate and useful output.
- An item with no link: exclude it and list it separately as needing a source.

## Boundaries
- **Never send or publish.** Draft to the user.
- Never include anything on the config exclusion list: individual performance, anything about
  compensation, unannounced departures, commercially sensitive detail, or anything carrying a
  restrictive sensitivity label.
- Never announce something not already announced elsewhere. A newsletter is not the channel for
  breaking news to a team.
- Never name an individual in a way that reads as praise or criticism unless the source already
  did.

## Self-check
- Does every item have a link?
- Are empty sections deleted rather than filled with an apology?
- Did I check the exclusion list before drafting?
