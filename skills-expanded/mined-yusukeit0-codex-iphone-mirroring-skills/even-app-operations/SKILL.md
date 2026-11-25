---
name: even-app-operations
description: Required whenever operating the Even iPhone app or its Even Hub through macOS iPhone Mirroring. Covers storefront browsing, plugin management, formal and developer Dot Link, stopping, updating, text input, and physical acceptance. Not for the separate Even Developer Hub website.
license: MIT
---

# Even app operations

Target runtime: OpenAI Codex with native Computer Use (`cua_repl`) on macOS. Claude, Claude Code and other agent runtimes have not been tested or adapted. Follow the current Codex tool documentation; do not invent equivalent APIs in another runtime.

Maintainer requirement (2026-10-24): read and apply this skill before operating Even or Even Hub through iPhone Mirroring. If already read in the current session, continue applying it rather than rediscovering the routes.

Use cua_repl for UI interaction. Routes were observed on 2026-10-24 and extended on 2026-10-25. Refresh the screenshot before choosing controls. This file is self-contained; it does not depend on a separate skill repository.

## Open the installed app

- Bind iPhone Mirroring with `cua.getApp('com.apple.ScreenContinuity')`. Its AX tree may expose only the Mac window and menus. Use current screenshots for the phone's controls; do not expect app-internal AX elements.
- `super+1` opens iPhone Home and `super+2` the app switcher. The documented `super+3` Spotlight shortcut was inconsistent on 2026-10-25; use the visible Home Search control or an already visible app icon when needed. Inspect focus before rebinding a stale app handle.
- In Even, the bottom-left house tab opens the home with installed app cards. Open the Dot Link card's icon. The four-square Even Hub tab is a storefront, not the installed-app starting point.
- The observed Dot Link 0.3.25 was a formal release. Do not route through Developer mode or infer Beta merely because this is a test session. Read the actual app version and the user's selected route.
- An Update badge does not need to be pressed to open the installed version. Updating changes the test subject and is a separate decision.
- Coordinates follow the returned screenshot's coordinate system. Do not halve them or reuse remembered coordinates. A safe navigation double-click worked in an earlier observation, but later checks showed delayed navigation. Let a single click settle and inspect the result before retrying; never generalize double-clicking to send, update, or destructive controls.
- To stop the running Even app, tap the top-left diagonal-arrow control in the Dot Link host. The sheet says 「終了しますか？」 and explains that the current function will stop. Choose 「終了」, then verify the originating list returns (home for the formal app, developer hub for the developer app). This was executed successfully. Reopen from the Dot Link card and verify connection/history restoration.
- The host top-right ellipsis exposed an uninstall action, not stop/reload. Do not uninstall to restart.

## Developer hub and prototype mode

Verified in the Even iPhone app 2.3.2 on 2026-10-24:

1. Open the bottom Even Hub tab (four-square icon).
2. Tap the top-right avatar to open 「マイプラグイン」 (My plugins).
3. Tap the top profile/name row or its right chevron. This opens 「開発者ハブ」 (Developer hub). The user explicitly corrected an automated review that misclassified this navigation as unrelated personal-account settings; the resulting screen verified the developer destination. Do not assume account editing from the row's appearance.
4. For the uploaded developer app, use the LOWER 「開発中 → Dot Link → 開く」 row. This opened 0.3.24 Beta, while the formal route opened 0.3.25. The user confirmed this is the intended developer-mode app. Do not substitute the upper QR/prototype route. Verify the version each time; these numbers are observations, not permanent targets. On 2026-10-25 this route opened 0.3.36 without a Beta marker. The route alone does not determine build identity or public availability. The developer app stops through the same top-left diagonal arrow → 「終了」 confirmation and returns to Developer hub. Its top-right ellipsis showed uninstall, not update.
5. Prototype mode opens 「QRコードをスキャン」. The bottom 「QRコードをスキャンできない場合」 link opens a URL field and 「開始」 button. Only use an intended, authorized development URL. Opening these screens does not require starting a prototype or replacing the installed release.

## Updates

- Formal-app management: Even Hub → top-right avatar → My plugins. Tapping the app name opens the store detail; tapping 「開く」 launches it. In the observed current state, both My plugins and the detail page showed Open for formal 0.3.25, not Update.
- [Even official support](https://support.evenrealities.com/hc/en-us/articles/15688149217167-Even-Hub) says My plugins displays Update when a new release is available. This is documented guidance, not an update executed in this session. The page's Public/Beta tab layout differs from the observed app 2.3.2, so prefer live labels over copied screenshots.
- Developer-app update (user-confirmed 2026-10-24): after a new build is available, go BACK out of Developer hub, then re-enter it. The 「開発中 → Dot Link」 row shows Update after the screen refreshes. Staying on the same screen often does not reflect the new version. Use that Update control, then reopen and verify the target version. Do not confuse this with the upper QR/prototype route or uninstall. In this observation no update was pending (Open, 0.3.24 Beta), so no package update was executed.
- Preserve the selected test version while inspecting procedures. After any authorized update, reopen and read the version/Beta label before treating it as the intended build.

## Text input — current operating policy (2026-10-25)

1. Preserve any existing draft. Focus the actual field and wait for the caret or focus change after navigation settles. Absence of an on-screen iPhone keyboard is not itself a fault.
2. Prefer a complete, committed string copied on the Mac, then ordinary Command-V (`super+v`) in the mirrored field. If a scratch document is needed, use a local non-synced test file and copy the intended text with Command-C. This changes the clipboard; do not claim its old contents were preserved. Handle any paste-permission prompt within the task's authority.
3. After the paste indicator and UI settle, inspect the exact rendered string. A tool return, field outline or clipboard operation is not proof of correct input.
4. If it does not match, stop automated input and ask the user to enter only the required text in the prepared field. Do not ask them to send it. Verify their input and resume the remaining authorized work. Do not cycle through paste methods or keyboard shortcuts.
5. If the user also cannot enter it, mark that step unverified and use an available non-text route or stop that part. Do not repeatedly hand the same failing step back to the user.
6. Keep sending separate from editing. For no-send tests, do not press Return or Send. Clear only synthetic text inserted by the test and verify cleanup; preserve user text and text of uncertain origin.

Evidence and limits:

- Rapid `typeText` produced incomplete strings and Japanese composition. Native `paste` sometimes inserted an old clipboard value. Persistent Mac copy followed by Command-V succeeded twice in Settings search, but later also inserted old text in Even Hub search. It is the preferred first attempt, not a guaranteed workaround. The cause remains unknown.
- The user also reported failing to enter the intended Even Hub search query manually on 2026-10-25. Search by entered text remains unverified in that setup. Categories and My plugins provide non-text routes.
- Holding the physical MacBook fn/globe key displayed English/Japanese choices. The tool rejected `fn`, and clicking the transient menu did not establish a reliable switch. Control-Space and other key experiments did not establish a reliable method. Do not alter keyboard remapping, system programs or app binaries to solve routine input.
- `super+a` and BackSpace previously cleared focused synthetic text. Escape can dismiss composition; inspect afterward. When the user changes apps or types, refresh state and preserve their content.

## Even Hub storefront and plugin management (2026-10-25)

- Even Hub opens the storefront. The top search field opens discovery with Popular/New ranking tiles and category tiles. Categories observed included Performance, Lifestyle, Entertainment, Healthcare, Education, AI, Music, Travel and Utilities; use live labels rather than treating this list as fixed.
- Category pages contain featured content, a plugin count and a list. Their sort menu offered Automatic, Top popular and Latest. Latest was exercised and changed the list after loading; Automatic was restored. Wait for the spinner and changed rows, not just the selected label.
- Popular and New open a shared Ranking page with corresponding tabs. Both were exercised and displayed different lists.
- My plugins is reached through the storefront avatar. Names open store details; Open launches the plugin. Installed versions are shown. Its sort menu offered Updates available, Size and Name, with a separate direction control. The menu was inspected; reordering with multiple plugins was not tested.
- Store details show developer, category, ranking, screenshots and overview, plus Get/Open and a heart/count. Get can start installation. Heart and Share are separate actions, not navigation. The store-detail ellipsis exposed Live translation and Share; neither was executed. This differs from the running plugin host's ellipsis.
- For an explicitly authorized uninstall, open the exact plugin, choose the host ellipsis → Uninstall, then read the confirmation. The observed sheet says all related data will be lost irreversibly. Apply the tool's action-time confirmation requirements before confirming. Verify removal afterward; never uninstall as a restart/update method.
- OcuClaw uninstall was executed with explicit authorization, including related-data confirmation. The store changed from Open to Get. My plugins initially retained the stale row; returning to the storefront and re-entering My plugins removed it. Refresh the list before repeating a removal. This past authorization applies only to that completed operation.

## UI timing, scrolling and recovery

- The Mac AX tree often describes only the host window. An unchanged tree does not prove the phone is unchanged; inspect its screenshot. Derive fresh coordinates after screen changes and never halve them.
- Navigation and focus can lag. A transient overlay may disappear before a click arrives, exposing a different control underneath. Do not queue dependent actions against an intermediate screen.
- Use a small native scroll over the intended region and compare landmarks. Page counts did not reliably scale distance. Scrolling worked in Settings and the Dot Link page; two scroll attempts on a store detail did not establish movement. Gallery dragging and tapping also did not establish navigation/enlargement. Do not generalize one surface's result to another.
- If two deliberate attempts with fresh observations fail, use another visible route or a narrow user handoff. Do not repeat blindly. Back navigation still worked on the affected detail page.
- If screenshot capture is unavailable while AX shows an open Mac menu, dismiss it using an exposed Cancel action and observe again. This restored capture in the observed session; the symptom alone does not prove a device disconnect.

## Acceptance evidence

Define one bounded session with the starting route/build, concrete operations, expected observations and finish condition. Monitor available UI directly and report passed, failed and unverified checks separately. Restore the original app route and state when practical.

Read the exact Even version and Mac test artifact/commit separately. A Mac-only test does not require changing Even. Connected status, message receipt, and the phone's rendered content are different evidence from physical G2 display/notification observations. Collect physical-only observations from the wearer once after the agreed bounded sequence. Do not consume pending utterances or fabricate a reply through a tool while testing the normal Dot response path.

For product-change work, Beta acceptance and merge are intermediate stages. Track the outcome through formal distribution to users, including the affected Mac update feed or Even Hub stages. If a maintainer action or stage-specific approval is still needed, prepare the concrete handoff and report distribution as unfinished. Keep release, upload, review submission, and publication authority separate under the project's current instructions; the maintainer presses the Even review-submission button. This skill grants no additional authorization.
