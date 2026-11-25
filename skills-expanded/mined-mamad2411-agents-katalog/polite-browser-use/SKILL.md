---
name: polite-browser-use
description: Mandatory browser-testing safety and cleanup. Read before the first browser-related action, including any T3/in-app preview call, website/game preview, Playwright run, external browser, or Electron launch.
---

Browser testing is good. However, if your human is using the computer you're testing on, your testing may disturb them if you don't take precautions.

# Gate browser work before it starts

Read and apply this skill before the first browser-related action. If browser testing becomes necessary midway through another task, pause before making any browser call and apply this skill first.

Browser-related actions include:

* Any T3 or in-app `preview_*` call, including status checks, opening, navigation, snapshots, evaluation, clicks, typing, and recording.
* Website or game previews, whether visible, inline, headless, or in the background.
* Playwright or other browser automation.
* External browser and Electron launches.

A collaborative or internal preview still counts as browser testing.

# Keep browser testing silent

Sound can be especially annoying or confusing when it starts playing out of nowhere. You must not let your browser testing produce sound through your human's speakers.

* Mute the browser tab, process, or application before loading a page that may play audio or interacting with the application. Do not click Start, Play, or a similar control until silence is verified.
* If the browser cannot be muted reliably, modify the application to add a test-only mute mode before continuing. You are allowed to make this small change even when it isn't part of the main task.
* Prefer the application's existing mute setting or audio manager. Otherwise, add a focused automation setting using something like an environment variable, launch argument, configuration value, or query parameter.
* Enable the mute before the application sets up its audio. Make sure it covers music, sound effects, HTML media, Web Audio, and any new windows or views the application creates.
* Inspect the actual mute or audio-enabled state when the tools expose it. Do not infer silence from headless, background, hidden, or internal-preview operation.

Keep normal user launches unchanged. Headless or background mode does not necessarily mean muted.

If you need to test the actual audio output, send it to a silent recording or virtual output instead of the speakers. Ask your human before doing any test that they might hear.

# Don't pop up unexpected windows

Windows popping up can take focus away from whatever your human is doing. Internal browser previews are usually fine, but external browsers such as Chrome, Firefox, Brave, or Edge should run headlessly unless your human expects to see them.

# Clean up after yourself

Close the browsers and tabs you opened as soon as you're finished with them. Keep one open only when your human asked for it or the task needs it to remain available.

Hidden, backgrounded, detached, automation-unavailable, and closed are different states. A false `visible` or `available` value does not by itself prove that the user-visible tab is gone. Use a tab-management control that explicitly closes the tab, then verify the user-visible tab no longer exists.

If the available tools cannot close the user-visible tab, say so plainly before finishing. Never report a tab as closed based only on automation detachment, `window.close()`, navigation, or hiding the preview.

Stop test-only servers and browser processes you started unless the human asked you to leave them running.
