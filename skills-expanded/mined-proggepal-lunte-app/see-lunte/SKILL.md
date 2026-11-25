---
name: see-lunte
description: See Lunte's UI to check a change, since the screen itself can't be captured from here. Renders every popover, onboarding, Club and Settings state to PNG, snapshots the real menu bar panel with real data, installs the build on this Mac, and samples colours against the user's screenshots. Use before and after any change to the popover, panel, Club window, Settings or onboarding, and whenever the user says "install it" or "does it look right".
---

# See Lunte

The screen can't be captured from a session here: `screencapture` has no Screen Recording permission, and computer
use can't target Lunte (Spotlight hasn't indexed it). So Lunte draws itself.

## Every state, light and dark

```bash
scripts/render-popover.sh
```

- Name states to draw just those, by how their names start (`scripts/render-popover.sh 9b pill-lab`): much quicker.
- Builds, then writes `dist/popover/<state>-light.png` and `-dark.png` for every fixture in
  `LunteApp/Sources/Lunte/Previews.swift`: the popover states (1–9), onboarding (10–15), and the `club`, `club-none`
  and `settings` windows. The same states are Xcode `#Preview`s.
- Then contact sheets of the numbered states, four to a row: `dist/sheet-light.png`, `dist/sheet-dark.png`.
- Look with the Read tool. Crop with `sips -c H W --cropOffset Y X in.png --out out.png`. Tile a few with ffmpeg
  `pad` + `xstack` (see the script).
- Nothing is watched, polled or sent: the fixtures use `GameModel(preview:)` and `GameModel(onboarding:)`, which never
  start the real game.
- A new state: add a fixture to `PopoverPreviews.all` (or `.onboarding`), named with a number so it lands on the
  sheet, and a `#Preview` for Xcode.

## The real panel, with real data

```bash
scripts/build-app.sh && scripts/panel-shot.sh
```

- Opens the real panel under the real menu bar item from `dist/Lunte.app`, draws it to `dist/panel.png`, and prints
  `panel <frame> item <frame> highlighted <bool>`: where it sat against the item and whether the item was lit.
- The installed copy steps aside and opens again after (that points Claude Code's hook back at it).
- If the item's frame sits above the screen (y past the screen's height), the menu bar was hidden at the time.
- The drawing can't show the material's blur: `cacheDisplay` draws materials as a flat fallback colour.

## Install it on this Mac

```bash
scripts/install-local.sh
```

Quits the running copy, replaces `/Applications/Lunte.app`, opens it, and prints the hook link. Opening it points
Claude Code's hook at that copy, so it plays the user's real game. Debug build, ad-hoc signed.

## Colours and materials

- To match a system surface, sample the user's screenshot: `ffmpeg -loglevel error -i shot.png -vf crop=1:1:X:Y -f
  rawvideo -pix_fmt rgb24 - | od -An -tu1` (convert `.webp` with `sips -s format png` first). Battery's panel
  measured about 247, 248, 243.
- Compare `NSVisualEffectView` materials by their flat fallback (a tiny `swiftc` script that draws each into a
  borderless window with `cacheDisplay`): in light, `.menu` ≈ 221, `.popover` ≈ 209, `.sheet` and `.windowBackground`
  ≈ 255. The panel uses `.sheet`.

## Layout questions

When it's unclear what SwiftUI or AppKit will do, test it in a few lines instead of guessing: a `swiftc` script in
the scratchpad that hosts a view in an `NSHostingView`, draws it with `cacheDisplay`, and reads a pixel. That's how
the panel's "content nudged down while it grows" was found: a frame with only `maxHeight: .infinity` takes its
content's height, and the host centres it; `minHeight: 0` pins it to the top.

## What still needs the user's eyes

Motion (expand and collapse, the fuse), hover, the live material and the menu bar highlight. Say what was checked
and what wasn't, and ask for a screenshot when it matters.

## How to work

One render round, fix everything it shows in one batch, then one confirming round. Don't loop on polish.
