---
name: preview
description: See a frontend page or dialog as users do: screenshots on three phones (iPhone 16, Galaxy A55, Galaxy S24) and a 1920 × 1080 computer, logged in or not, then look at them. Use to check a rendering (new page, dialog, visual touch-up, mobile overflow) or when the user asks to see something.
argument-hint: "<path or URL> [account]"
---

The `preview.mjs` script is in the plugin's `scripts/` directory, two levels above this skill
(`${CLAUDE_SKILL_DIR}/../../scripts/preview.mjs`). It uses the project's Playwright Chromium:
nothing to install.

1. **The site must answer**: the base is `url=` of `.playwright/config` (otherwise
   `http://localhost:3000`). If it does not answer (`curl -s -o /dev/null -w '%{http_code}'`),
   start it with the project's dev server skill if it has one (`dev`), otherwise `pnpm dev` in
   the background, and wait until it answers.
2. **Capture**, from the frontend directory (the one with `@playwright/test`):
   ```bash
   node <scripts>/preview.mjs /account/profile --account member --wait-for '[role=dialog]' --name whats-new
   ```
   - `--account <name>`: log in with `login_<name>` of `.playwright/config` (password:
     `.playwright/token`); `--account default` takes `login=`. Without `--account`: visitor.
     Each device starts from a fresh browser (empty localStorage): a "seen once" dialog reopens.
   - `--wait-for <selector>`: wait for an element (a dialog, a loaded table) before the
     screenshot; `--full-page`: the whole height; `--output`: another directory than
     `.playwright/captures/preview/`.
   The script prints one line per device: name, file, and `HORIZONTAL OVERFLOW` when the page
   is wider than the screen.
3. **Look at the four screenshots** (Read tool on each PNG) and judge: nothing cut off or
   overlapping, text readable without zooming, touch targets large enough, whole dialog on
   screen, no overflow. The project's design (skill `design-system` if there is one) is the
   reference.
4. **Report** device by device, briefly: what works, what does not with the screenshot at
   fault, and the proposed fix. Fix only if the user asked for it.

The accounts of `.playwright/config` can act on production when the frontend talks to the
production API: buy nothing, send nothing, only look.
