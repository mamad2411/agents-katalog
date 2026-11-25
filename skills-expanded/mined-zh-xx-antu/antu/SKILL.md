---
name: antu
description: >-
  Draw legal diagrams as one offline HTML file from structured JSON you write. Four kinds: a fact timeline
  (who did what and when; 事实时间线、案情时间图), a procedure flowchart (contract performance, litigation or
  arbitration steps; 程序流程图、合同履行流程), a relationship diagram (parties, equity, guarantees, regulators;
  主体关系图、股权结构、担保关系), and a justification tree (how a court reasoned from facts and norms to a
  conclusion; 证成图、说理树、裁判说理). Use when the user asks to draw, chart, map or visualise a case, a
  contract flow, the parties, or a judgment's reasoning.
license: AGPL-3.0-or-later
metadata:
  version: "{{version}}"
---

# Antu · Legal Diagrams

You write the JSON; the engine draws it. The result is **one HTML file** that opens in any browser with no install and
no network, prints, and can be forwarded. Nothing is uploaded anywhere. This skill is Antu **{{version}}**; the pages it
makes say so: `<meta name="generator" content="antu {{version}}">`.

**`<skill-dir>`** is the folder that holds this `SKILL.md` (`scripts/`, `references/`, `examples/` and `assets/` are
beside it). Keep your own files (the JSON and the page) where the user works, never inside the skill folder.

## 1. Choose the kind of diagram

| The user wants to show | Use |
| --- | --- |
| what happened, in order, who did it (a timeline of a case) | `fact` |
| the steps of a process: contract performance, a litigation or arbitration procedure, with branches | `procedure` |
| who the parties are and how they are tied: shareholding, loans, guarantees, control, regulators | `relationship` |
| why a court decided as it did: conclusion, issues, norms, elements, facts | `justification` **(experimental)** |

If the request fits two, make two diagrams rather than one overloaded one, and say so. If it fits none (a chart of
numbers, an org chart of a firm), say that Antu does not draw it.

## 2. Write the JSON

**Before writing JSON, run `schema` and `guide` for the kind you chose, and look at `examples`.** They are the same
texts the MCP tools `antu_schema`, `antu_guide` and `antu_examples` give, so the field table cannot go out of date
with the checker:

```
npx -y @zh-xx/antu@latest schema fact
npx -y @zh-xx/antu@latest guide fact
npx -y @zh-xx/antu@latest examples --type fact
```

- `schema` is the field table: every field, whether it is required, and one line of what it means. It also gives the
  format generation (`now N`) to put in `specVersion`.
- `guide` is how the data becomes the picture: what decides a row or a side, what the main line is, when a clause is a
  rule rather than a branch.
- `examples` lists the small examples; start with `1-minimal`. Fetch one with
  `npx -y @zh-xx/antu@latest examples 1-minimal.en.json --type fact` (or `--lang zh-CN`).

Use the kind you chose for all three: a field name from another kind will not pass validation.

If `npx` or the network fails, run the copy in the skill (Node 18 or newer, nothing to install):

```
node <skill-dir>/scripts/antu.mjs schema fact
node <skill-dir>/scripts/antu.mjs guide fact
node <skill-dir>/scripts/antu.mjs examples --type fact
```

`references/guide-<kind>.md` and `references/fields-<kind>.md` hold the same text offline, and `examples/` holds the
same examples: use them only as that fallback.

Then write the JSON:

1. Open one example of that kind and follow its shape: `1-minimal` is the smallest, the others each add one idea.
   **Fact diagram**: count the parties first. With two or more, each party carries `groupId` (its side, the 1st or
   the 2nd group) and the events carry none: an event goes to its party's side, and one of several parties goes on
   the axis (see `3-sides`, `4-one-side-several`). With one party, the groups sort its acts and go on the events
   (see `2-single-actor`). There are no `views`.
2. Write the file in the **user's language** (the examples come in `.zh-CN.json` and `.en.json`).
3. Put `"specVersion"` in the envelope, next to `"type"`, with the generation `schema` gives.

**What goes in the diagram comes from the user's material, not from you.**
- Do not invent a date, a time, an article number, a version of a statute, a case number or a name. If the material
  does not say, leave the field out, or put the question to the user.
- Do not give a party an identity, a role or a side the material does not state: lender or borrower, plaintiff or
  defendant, guarantor, seller or buyer. Leave `role` out (it is optional, and the diagram reads well without it), or
  ask. Do not infer it from a verb either ("乙放款" does not say that 乙 is the lender in the contract): if you do
  infer one because the user asked for it, say in your reply that it is your inference and why.
- Keep each node's text to what the material says, in its own words as far as you can; the full text that does not fit
  goes in `detail`, and where it came from in `sources`. If the user gave no source document, leave `sources` out: the
  checker's notes about a missing source are **notes, not errors**, and the user is told that no sources are recorded.
- A legal point you are not sure of, or something the user says they are unsure of ("好像", "不确定", "可能"): leave it
  out of the diagram, say so in your reply and why, and offer to add it once it is confirmed.
- An event with no date: leave `date` out (the card then says the date is unknown). Do not borrow the date of the event
  before it, and do not use `approx` (that is for a date that was estimated). Its place in the `slots` array orders it.
- Leave out the optional marks the material does not support: `combine` (and / or) only when the reasoning says all or
  any of what it rests on is needed; `approx` only for a date you really cannot give exactly.

## 3. Check, make, look

```
npx -y @zh-xx/antu@latest validate spec.json
npx -y @zh-xx/antu@latest layout spec.json
npx -y @zh-xx/antu@latest render spec.json -o diagram.html
npx -y @zh-xx/antu@latest preview spec.json -o shot.png
```

If that fails, the copy in the skill is `scripts/antu.mjs` (Node 18 or newer, nothing to install). Run it as
`node <skill-dir>/scripts/antu.mjs validate spec.json` (and `layout`, `render`, `preview`). If the Antu MCP server is
installed, its tools `antu_validate`, `antu_layout`, `antu_preview` and `antu_render` do the same.

- `validate` prints each problem with its field path (exit code 1 when there are any) or "Validation passed". Fix the
  JSON and run it again until it passes.
- `layout` says how big the picture is, which orientation suits it and, for a fact diagram, how many columns each side has. Run it
  before `render`.
- `render` checks the data first, refuses a diagram that has problems, and writes the page. Keep the JSON next to the
  HTML (same name, `.json`): the JSON is the source and can be edited and made again; the HTML is the product.
- `preview` takes a screenshot of the diagram, because passing validation does not mean it looks good. It needs a
  Chromium-based browser on the machine (Chrome, Edge or Chromium; Windows has Edge). Open the PNG with the tool you
  have for reading images and look for what validation cannot see: cards or nodes crowded together, text too small to
  read, a line running through a card, a diagram that is mostly empty, headings cut off. If something is wrong, change
  the JSON and run it again. `--orientation vertical|horizontal` shows the other orientation; `--width` and `--height`
  change the screen size (1600×900 by default). Keep the PNG out of the user's folder unless they want it.

**A notice at the end of an output.** The command line asks (at most once a day, and nothing of the diagram is sent)
whether a newer Antu is out; if there is one, the plain output ends with a line `Notice: …`, and a `--json` output
carries the same notice in `_notice`. Finish the user's request first, then tell the user in a sentence or two, with the command the notice gives (`npx skills update antu -g`). Do not run it unless the user agrees, do not put it before
your answer, and do not say it again in the same conversation. `ANTU_NO_UPDATE_NOTIFIER=1` turns the asking off.

**Whether the reader can read it.** `layout` has a line `Text on one screen (1600×900): … px`: the size the body text is
drawn at when the page opens fitted to a 1600×900 screen. It adds a note when the text is **under 11 px** (small; the
reader can zoom in) and when it is **under 9 px** (too small to read without zooming in). Run `layout` first: it is
cheaper to split the JSON than to make the page twice.

When it says too small, split the diagram the way the note says: a justification tree **by issue**, a procedure **by
stage**, a relationship diagram **by group**, a timeline **into periods**. The one exception is a justification tree of
several issues whose `layout` says `Opens with the issues folded`: the page then opens with every issue folded to its
conclusion, readable, and the reader unfolds an issue by clicking its title (or all of them with "收起争点" / "Fold
issues"); leave it whole and tell the user so. Split it by issue only if the line after still says under 9 px. Write
one JSON for each piece from the same material, give each piece a clear title of its own (for example the issue's name),
check each with `layout` again, and tell the user it is in pieces and why. **Never drop facts to make it fit.** When it
only says small, you may leave it whole and tell the user they can zoom in.

`--kind K` (for `layout`, `render` and `preview`) picks another way of drawing the same JSON; `guide` lists the ways of
each kind, and the reader can still switch in the page. `--theme document|modern|legal|dark` (for `render` and
`preview`) fixes the look of the picture: `document` is black and white and square, for print and filing (the default when
nobody chooses); `modern` is rounded and pale; `legal` is navy, with red only for the adverse; `dark` is the modern look on
a dark ground, for a dark host, and also darkens the shell round the diagram. Nothing in the JSON chooses a way of drawing
or a theme.

**Without Node**, with Python 3 (standard library only): `python3 <skill-dir>/scripts/make_html.py spec.json -o
diagram.html` makes the page. It checks only that the JSON parses and that the `type` is known. The page checks the data
again when it opens and **lists every problem it finds instead of the diagram**: tell the user to send you that list if
they see one, then fix the JSON and make the file again. Check the JSON by hand against `references/fields-<kind>.md`:
required fields present, ids unique, every reference (`actorIds`, `sourceIds`, `from`, `to`, `groupId` …) points at an id
that exists. There is no `layout` and no `preview`. **Without Node and without Python** this environment cannot make the
page: say so to the user.

**When you cannot look**, say so; never claim you checked how it looks:
- `preview` ends with "no Chromium-based browser found" or "no picture could be taken" (exit code 3): there is no
  picture. If the user has a browser somewhere else, `ANTU_CHROME` can point at it.
- You have no way to read an image file: the picture exists but you have not seen it.
- No Node: there is no `preview`.

In each case rely on `layout` for size and orientation, and tell the user that you could not view the result and that
they should open the page and look.

## 4. Tell the user

Give the path of the HTML file. Say what it shows and what you had to leave out or could not tell from their material, in
a few lines. In the page the reader can hover and click the items for detail, switch the way of drawing in the label card
at the top left, and use the bar at the bottom: switch orientation (vertical / horizontal), switch the language (the
page's labels follow the browser's language; the EN / 中文 switch changes them), export an image.

**The bar also has switches that show or hide things on the diagram.** Some of them are **off until the reader turns
them on**, so do not count on them for what the diagram has to say; tell the user where to look.

| Kind | Switches in the bar (on by default unless it says off) |
| --- | --- |
| fact | Summary (on), **Parties** (off), **Sources** (off), Grid (off), Stagger (vertical only; on: cards in different columns overlap by half a row, so a long timeline is shorter; the time order is read on the axis); there is no views menu. The chronicle has the same three card switches and no grid; the time scale has **Lane per party** (off; offered only when a side holds two or more parties) |
| procedure | Conditions, Detail, Main line, Stages (only if the data has stages), Rules (only if it has rules); all on |
| relationship | one switch per kind of relation (when the data uses more than one kind), Labels, Groups (only if the data has groups); all on. The focus view has the kind switches and Labels, and a "Default centre" button once another party was picked |
| justification | Labels (only if a link has one; on), Fold issues (only if there are several issues; none folded), Merge repeats (off) |

What this means for what you write:

- **Fact diagram: a card shows its title, its summary and its time.** Its party names and its source marks are off by
  default. So if who did it matters, say so in the title or the summary, or give the diagram `groups` so each party has
  its own side; and tell the user that **Parties** and **Sources** in the bar show them on the cards.
- A `detail` (the full text that did not fit) and the `sources` are in the overlay that opens when the reader points at or
  clicks an item, in every kind.

## Licence and version

Antu is licensed under the GNU AGPL, version 3 or any later version (`LICENSE`). The data in a page (the user's diagram
and the material it comes from) is not covered by the licence: it stays the user's. For anything else about the licence,
read `LICENSE-NOTES.md` and do not describe it beyond that file.

The version is at the top; the newest one is at https://github.com/zh-xx/Antu/releases. If the user asks whether this is
up to date, tell them the version above and that address; do not claim to know what the newest version is.
