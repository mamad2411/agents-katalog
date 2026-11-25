---
name: ui-reference-studio
description: "A worked reference, measured from a hand-designed studio site: a small studio, consultancy or freelancer showing its work as decisions rather than thumbnails, then a way to get in touch. Its skeleton, wireframes, measures and component anatomy, and what to take from it. Read before building a studio, agency, consultant or project portfolio page."
---

# Reference: a studio that shows its decisions

Measured from a hand-designed site (enowxlabs.com, a small software studio).
Take its structure and its decisions; its words, name and colours belong to
it. Its concept is its own: find yours from your studio's work (the `ui`
skill, section 1).

**Its concept**: the studio's notebook. Each project is written up as an
entry, with the decision the studio made and why, the way an engineer would
explain it to a colleague. No grid of screenshots, no list of services, no
logos of clients.

## Skeleton

1. A quiet header: the wordmark, two links (Work, Contact), a theme toggle.
2. Hero, one screen: a label naming the studio and what it is, a two-line
   claim, a paragraph, two outline buttons, a hairline.
3. Selected work: one entry per project, numbered, separated by hairlines.
4. Contact: a closing line beside the ways to reach the studio.
5. A footer of one line.

Three sections are enough when each carries real content.

## Wireframes (wide screen)

```
│ WORDMARK                                         WORK  CONTACT  ◐   │
│                                                                    │
│      STUDIO NAME, A KIND OF STUDIO                                 │
│      The claim in a large serif,                                   │
│      its second line in the muted colour.                          │
│      A paragraph of about 60 characters a line: who the studio     │
│      works for and what it hands back.                             │
│      ( START A PROJECT )  ( SEE THE WORK )                         │
│      ───────────────────────────────────────────                   │
├────────────────────────────────────────────────────────────────────┤
│      01                                     ▏ DECISION             │
│      project name  a muted description     ▏ What was chosen.     │
│      that runs to two or three lines.       ▏ WHY                  │
│      A paragraph on what it is and does,    ▏ The reason, in       │
│      set at a readable measure.             ▏ plain sentences.     │
│      ( VIEW REPOSITORY )                    ▏ STACK                │
│                                             ▏ [Go] [SQLite] [MCP]  │
│                                             ▏ Last touched <date>  │
│      ───────────────────────────────────────────────────────────── │
│      02 ...                                                        │
├────────────────────────────────────────────────────────────────────┤
│      A closing line in the         EMAIL        name@domain.com   │
│      large serif, over             ──────────────────────────────  │
│      three lines.                  GITHUB              @handle    │
│                                    ──────────────────────────────  │
│                                    COMMUNITY        invite link   │
│ WORDMARK                                                           │
```

On a phone: one column; each entry's side column moves under its text, and
its left rule becomes a rule above; the contact list follows the closing
line.

## Measures

- Content about 960px wide, set a little left of centre in a wide window;
  sections 120 to 160px apart.
- Entry: 592 and 300px, gap 64px; the narrow column has a 1px rule on its
  left and 20px of padding. Contact: 566 and 320px, gap 70px.
- Type: one serif family (Newsreader) for everything. H1 104px, weight 400;
  the entry titles 54px; H2 31px; body 17px with generous line height.
  Labels 11 to 12px uppercase with 2 to 3px tracking, in the muted colour.
- Colour: near-black warm background (about 5% lightness) with a faint
  texture on the hero only, warm off-white text, a warm grey for second
  lines and labels, and one brick red used only on the primary button's
  outline and text.
- Buttons: rectangular outlines, uppercase 12px with tracking; no fills.

## Anatomy worth taking

- **Eyebrow label, then a two-line claim**: the studio's name and kind in
  small tracked capitals, then the claim with its second line muted.
- **A project as an entry, not a card**: a small index number, the project's
  name in the text colour followed by its one-line description in the muted
  colour, both in the heading's size; a paragraph; one outline button to the
  real thing.
- **The side column of decisions**: labelled rows (Decision, Why, Stack) in
  small capitals, each with a short answer; the stack as small bordered
  chips; a dated "last touched" line. It shows judgement, which is what a
  studio sells.
- **Contact as a definition list**: label at the left, value at the right,
  hairlines between rows; only channels that exist.
- **Restraint**: one family, one accent, outline buttons, hairlines. The
  large serif does the work a hero image would.

## When it fits, and when not

For a studio, consultant, freelancer or engineer whose work is best judged by
its reasoning. A photographer or an illustrator shows the pictures first
(`ui-page-portfolio`); a studio selling to shops or restaurants may want
light paper instead of near-black. Keep the entry anatomy either way.
