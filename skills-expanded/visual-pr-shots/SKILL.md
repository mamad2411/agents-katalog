---
name: visual-pr-shots
description: >-
  Use when a change alters what a page looks like: before showing the
  options, before opening the PR, and again after each fold that touches
  anything rendered.
metadata:
  author: Spool maintainers
---

# /visual-pr-shots — screenshots for a visual change

A visual change is reviewed by looking at it. The screenshots are its
evidence, so they follow the same rules as any other evidence: they show the
code as it stands at the head, they publish nothing private, and whoever
reads them can trust what they show without asking how they were taken.

## Why this exists

Each rule below was learned from a shot that went wrong: one taken against
the live system that published a credential, a set attached before the last
edit that showed copy the code no longer had, a large-text shot rendered at
the default size, an image sent without being opened that framed the wrong
part of the page. The image looked fine to its author every time.

## 1. Shoot fixture data, never the live system

A page that renders messages, tool input or logs prints whatever a running
agent ever echoed, credentials included, and once the shot is posted it
stays public. Shoot a throwaway server seeded with invented data, started
for the shot and deleted after it. Shape a state the fixture lacks by
intercepting its responses in the browser script, never by pointing the
browser at the real system. Any credential the fixture holds is
obviously fake.

Some pages are never shot at all: a page made of a person's private
conversations stays out of every picture, fixture or not, so nobody ever
has to ask where a shot of it came from.

## 2. Show it before the PR

Any visual change goes to whoever decides the look before its PR opens. That
includes a small visual bug fix as well as a layout choice. A screenshot
attached to a finished PR documents a decision someone already made.

- **Build the options for real**, on a scratch branch, and shoot each one.
  Real CSS beats a drawing.
- **Send the images themselves** where the decider reads, one message with
  each option labelled. A link to an image they can't open is not a way to
  show it, so check that any link opens when you're signed out.
- **Record the decision on the issue** before building on it, so the
  reviewer can see what was chosen without asking.

## 3. Shoot only what the issue names

Before you post a set, check every visible change against the issue's
proposed shape. If a shot shows something the issue doesn't name, the issue
is missing a line or hides a second deliverable. Say so on the issue first
and let its owner add the line or split it.

## 4. Take the shot that shows the claim

- **One component:** shoot the element, scrolled into view. A full-page shot
  of an app that scrolls inside its own frame stops at the viewport.
- **Text size or zoom:** emulate it, then take a page screenshot clipped to
  the element's bounding box. An element screenshot can re-render at the
  default size. Never mask the region the defect lives in.
- **Alignment ("centred", "lines up with"):** measure it on the rendered
  pixels at 4× and report the offset in pixels. Font metrics describe the
  font, not what the browser paints.
- **States:** one shot per state the change adds (empty, loading, error,
  narrow), each labelled with the state it shows.

## 5. Open every image

Look at each file before you send or attach it, including retakes: the
description you wrote is what hides a wrong shot. Check that it shows
invented data, the state you name and the part of the page you mean.

## 6. Shoot after the last edit

The shots must match the head. Take them right before the push. Any later
change to anything rendered (copy, spacing, a fold from review) makes every
shot stale, so reshoot and replace every attachment. Before you attach,
grep the visible strings in each shot against the tree.

## 7. Attach them where they render

Put each image in the PR body beside the claim it proves, with alt text
naming the state. After posting, read the body back and check that every
image reference resolved to an uploaded asset, not a dangling local path.

## In this repository

These rules from `docs/CONVENTIONS.md` and the fleet rules apply. This is
the section to strip before publishing the skill elsewhere.

- **`make ui-shots`** builds the binary, starts a fixture hub
  (`scripts/fixture-hub.sh` on a `cmd/uifixture` data directory) and writes
  the standard set to `web/shots/`, which is ignored. A page or state it lacks
  is added to `web/scripts/ui-shots.mjs`, with `page.route` shaping the
  fixture's answers. For scratch options,
  `bash scripts/fixture-hub.sh node scripts/<file>.mjs` runs a script of your
  own on the same hub. Delete that file before `npm run lint`, and never
  commit it.
- **The Activity page is never shot**, not even from the fixture (#277).
- **The operator sees options first.** Send the PNGs to Enes in his
  Telegram DM, then record his pick as a comment on the issue. The reviewer
  holds the merge ask until it's there.
- **Attach** with `gh pr edit <n> --attach '<path>#<alt>'`, where `<path>` is
  the same string the body's `![alt](<path>)` uses; on a mismatch the upload
  lands at the end and the reference stays broken. Run gh from the shots
  directory with relative paths, then `grep user-attachments` the posted body.
- **Videos** follow the same rules: `make demo` records on a fixture hub, and
  the mp4s are attachments, never committed.
- The PR template's Verification box says the shots are fixture-driven; tick
  it only when they came from the fixture hub.
