---
name: maker
description: Useful mini-tools as gifts that are also funny or touching - generators, planners, dashboards over data the person gave, cheat sheets, converters, trackers, deadpan annual reports, and small tools that run on their computer (scripts, terminal themes, form tool). Emotion, interaction and a share frame even for a utility, kit/maker (shell, storage, clipboard, cheatsheet, terminal-frame), offline only. Never runs or installs anything on their machine; tools dry-run by default, never delete, keep an undo log and uninstall in one line.
license: MIT
---

# Maker

Some people are happiest with a small tool that removes a small pain. The gift is the thoughtfulness of noticing the pain and the polish of the tool.

Read `gift-director` first. A useful tool is still a gift, so it still hits the three criteria: one `emotion` (a sourdough-name generator is `funny`; a January tracker that greets them by their dog's name is `cute`), a delightful `interaction` beyond typing into a form (a lever to pull, a stamp, a dial), one surprise, and a share frame (the best generated name on a card, the cheat sheet taped to a monitor, the report's headline chart).

## Forms

| Form | Example | Kit |
|---|---|---|
| Generator | Name generator for their hobby, excuse generator, menu planner, seeded workout | `shell.js`, `kit/art/prng.js`, `clipboard.js` |
| Mini-tool | Unit converter for their craft, timer with their intervals, tip calculator in their currency | `shell.js`, `storage.js` |
| Dashboard | A one-screen view of data they shared (a reading list, a training log) with sorting and totals | `shell.js`, `storage.js` |
| Cheat sheet | Keyboard shortcuts, conjugations, knitting abbreviations, chess openings; printable | `cheatsheet.js`, `kit/art/print.js` |
| Tracker | Habit grid for January, countdown, "days since" | `storage.js`, `shell.js` |

## Rules

- **Never touch the recipient's real files.** You may read inspiration folders when the brief allows it. You never write, move, format or "fix" anything outside your workspace. If you notice something worth changing in their project, write it as a **proposed diff** in a document inside the gift ("here is a patch you could apply"); never apply it.
- **Local-only data.** Tools store state in the browser only. `storage.js` wraps `localStorage` with an in-memory fallback, because gifts run on an opaque origin where `localStorage` may throw. Say in the UI that data stays on this device.
- **No network.** No `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, no CDN, no analytics, no fonts from outside (`network_request`). If a tool needs data, embed it. Libraries only from `workshop/kit/vendor/`, credited.
- **Correctness.** A converter with a wrong factor is worse than no gift. Verify every constant and formula; add a tiny self-test in the file that runs on load and logs mismatches.
- **No personal data baked in.** Pre-fill nothing private. Shared hobbies may shape the tool; names, addresses, calendars, credentials never appear.
- **Honest scope.** A dashboard over data the recipient did not share is a demo: say so in the note and fill it with obviously sample data.

## Craft

- `shell.js`: header, optional sidebar, main panel, footer; responsive under 600 px; focus styles; a `setStatus()` line for messages.
- Keyboard first: every action reachable by Tab/Enter; shortcuts listed in a help panel (`?`).
- Empty states say what to do. Errors say what went wrong in one sentence.
- Export: `clipboard.js` gives `copyText()` with a fallback and `downloadText()`/`downloadJSON()`; a tool that keeps data must let the recipient export it.
- Cheat sheets: `cheatsheet.js` lays out groups of key/value rows in columns, with print CSS; 1 page A4/Letter; large keys, small descriptions. The print file goes in `downloads`.
- Share frame: expose `window.adventCapture.prepare(kind)` that fills the tool with its most charming result (not an empty form), hides the toolbar, and marks any typed-in names with `data-advent-private`. Data the person gave you never appears in the share frame unless it is harmless and theirs to show.

## Workflow

1. Thinking: the pain, the single screen that removes it, the data it needs (embedded or typed in), the emotion, the delightful control, the share frame.
2. Making: shell plus one feature; add the second only when the first is tested.
3. Testing: happy path, empty input, absurd input, reload (state persists or clearly does not), keyboard only, narrow screen, print if printable.
4. Wrapping: `gift@2` manifest with `form: "interactive-html"`, `emotion`, `interaction`, `tierUsed`, `share`, `downloads`; the page says that nothing leaves the device; the `note` says why you noticed this pain.

## Small tools on their computer (`form: "tool"`)

Scripts, terminal themes and little utilities from the `small-tools` family run on their real computer, so the rules from `gift-director` §6 apply in full:

- **You deliver files and instructions. You never run or install anything on their machine yourself.** Test on sample files in your own workspace.
- **Dry run by default.** Anything that touches files shows the plan and changes nothing until they pass a flag such as `--apply`.
- **Never delete.** Move or copy instead, and write an undo log that the uninstall step can replay.
- **No network, no admin rights** (no `sudo`). Standard library only, or one clearly named dependency.
- **One-line install and one-line uninstall** that restores what was there before (back up a config file before changing it).
- **Say which operating systems and shells it supports**, in the README.
- It is still a gift: funny, cute or touching, not just useful.

Package it like this:

```
gift.json            form: "tool", family: "small-tools", entry: the display
screenshot.png       or index.html: a terminal with real output (kit/maker/terminal-frame.js)
tool/
  dig.sh             the tool itself
  README.md          what it does, supported systems, install and uninstall in one line each
  install.sh
  uninstall.sh
```

The calendar shows the display and your note, and Save gives the `tool/` folder as a zip. `advent-agent check` fails a tool with no README, no uninstall instruction (a script or a line in the README), or a delete call (`rm -rf`, `shutil.rmtree`, `os.remove`, `unlink`) without a dry-run guard. It warns about network use.

If the gift could become a tool later (a desktop snow globe, a terminal command), don't build it unasked: offer it in your note and add `followUp` (`gift-director` §7).

## Packaging

Single HTML file under 2 MB (browser tools); small tools as above. If the gift includes a proposal for the person's own project, add it as a `document` artifact (`proposal.md` or `.patch`) and say in the note: "This is a suggestion, nothing has been changed."
