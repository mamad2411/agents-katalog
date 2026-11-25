---
name: visual-browse
description: Coordinate-level browser control for UI that snapshots, refs, and locators cannot target - canvas apps, extension popups, OS-drawn dialogs, custom drag surfaces. Read this when a DOM-targeted action fails twice, when the next decision depends on rendered pixels, or when CUA clicks land on the wrong element.
---

# Visual Browse

`createCua(page)` drives the page by viewport coordinates when DOM targeting
cannot. It is rung 2 of the ladder below, not a last resort you ask permission
to reach.

## Escalation ladder

**TWO IDENTICAL FAILURES ON THE SAME TARGET MEAN CLIMB, NOT RETRY.** The failure
itself selects the next rung — never pause to ask which one.

| Rung                                       | Use                                                                                      | Advance when                                                               |
| ------------------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 1. `page.snapshot()` + `page.locator(ref)` | Everything with a usable ref                                                             | Ref is absent, stale, obscured, or the click lands on the wrong node twice |
| 2. `createCua(page)` coordinates           | Canvas, extension popups, custom controls, drag surfaces                                 | The click misses, or the screenshot and the coordinates disagree           |
| 3. Pin the viewport, then retry rung 2     | Coordinate drift: window resized, DPI scaled, or the tab was created at a different size | Coordinates land correctly but the widget still refuses input              |
| 4. `createCaptcha(page)`                   | A challenge widget is what blocks progress                                               | The widget is solved but the flow still stalls                             |
| 5. Environment diagnosis                   | Browser-level failure (entitlements, extension service worker, FIDO)                     | Logs name a cause outside the page                                         |

**RUNG 5 ENDS IN A WRITTEN DIAGNOSIS, NEVER A CODE CHANGE.** When the browser log
names the cause (service-worker failure, missing entitlement, FIDO unavailable),
stop retrying and report it. Automation code cannot fix a browser-process problem.

Return to refs and locators as soon as DOM targeting works again. Coordinates are
the expensive path.

## Pin the viewport before trusting coordinates

CUA acts in viewport pixels. When the render surface and the coordinate space
disagree, every coordinate is wrong by the same constant offset and retrying
repeats the miss. Pin both to one box:

```js
await page._sendToTarget("Emulation.setDeviceMetricsOverride", {
  width: 1440,
  height: 900,
  deviceScaleFactor: 1,
  mobile: false,
  screenWidth: 1440,
  screenHeight: 900,
  viewport: { x: 0, y: 0, width: 1440, height: 900, scale: 1 },
});
const size = await page.refreshViewportSize(); // -> { width: 1440, height: 900 }
```

Pin every page you act on, including tabs you did not open, then take a fresh
screenshot — coordinates read off an unpinned screenshot are stale.

Pin rather than retry when: the click reports success but nothing changes; the
same offset is wrong on every target; screenshot dimensions disagree with the
coordinates you computed.

## API

```js
import { createCua } from "omowright";

const cua = createCua(page);
await cua.click({ x, y, button?, keypress? });        // keypress: modifiers held during click
await cua.doubleClick({ x, y, keypress? });
await cua.drag({ path: [{ x, y }, ...], keys? });     // mousedown at first point, move through path, mouseup
await cua.move({ x, y, keys? });
await cua.scroll({ x, y, scrollX, scrollY, keypress? });
await cua.type({ text });
await cua.keypress({ keys: ["ControlOrMeta", "a"] }); // ControlOrMeta = Meta on macOS, Control elsewhere
const base64Png = await cua.getVisibleScreenshot();
```

Modifiers: `Alt`, `Control`, `ControlOrMeta`, `Meta`, `Shift`. Aliases: `Cmd`,
`Command`, `Ctrl`, `Option`. The CUA instance is bound to the page it was created
from — focus or attach the right tab first.

## Look, act, verify

Look before acting when coordinates are unknown, and **VERIFY AFTER EVERY
PAGE-CHANGING ACTION — AN UNVERIFIED CUA ACTION HAS NOT HAPPENED.** Fresh
screenshot for visual state, fresh snapshot for DOM state.

- `cua.getVisibleScreenshot()` - base64 PNG.
- `page.screenshot({ path })` - file; cite the path when there is no `display()`.
- `page.annotatedScreenshot()` - numbered boxes over interactive elements.
- Eval/REPL kernel: `display(Buffer.from(await cua.getVisibleScreenshot(), "base64"))`.

A popup, modal, or cookie banner overlaying the target is cleared first —
everything behind it is unreachable. On layered canvas and editor surfaces,
prefer coarse sidebar and toolbar controls over precise clicks on stacked objects.

## Surfaces that only CUA reaches

Browser chrome and OS-drawn UI have no DOM, so rung 1 is skipped entirely:

- **Extension popups** (password managers, wallets): click the toolbar icon by
  coordinate, then act inside the popup by coordinate.
- **Platform credential dialogs** (passkey, Touch ID, OS password prompts): drawn
  by the OS. If a click cannot satisfy them, that is rung 5 — read the browser
  log rather than clicking harder.
- **Native select popups and file pickers**: prefer `locator.selectOption()` /
  `locator.setInputFiles()`; use coordinates only for custom-rendered controls.

Values that leave the page through the system clipboard (a one-time code copied
by an extension) are read back with `pbpaste` on macOS and **VALIDATED BY SHAPE
BEFORE USE** — an unvalidated read silently carries whatever was there before.
