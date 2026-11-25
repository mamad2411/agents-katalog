---
name: ios-app-analysis
description: "Inspect an installed iOS app from a paired Mac, investigate its connection and rendering behavior, and use verified findings to fix Termio. Use for iPhone app reverse engineering, binary inspection, companion protocol analysis, or terminal garbling; use ios-rebuild-dev alone for ordinary rebuild requests."
---

# iOS app analysis

Investigate a concrete behavior and carry the finding through to a fix when
requested. Distinguish the target iOS app, its Mac companion, and Termio: evidence
from one does not establish another's implementation.

## Establish the running versions

Read the repository's `AGENTS.md` and check the working tree before editing.
Discover the device and installed app instead of reusing an old device ID or
application path:

```sh
xcrun devicectl list devices --json-output /tmp/ios-analysis-devices.json
xcrun devicectl device info apps --device "$device_id" \
  --json-output /tmp/ios-analysis-apps.json
uv tool run --from pymobiledevice3 pymobiledevice3 apps query "$bundle_id"
```

Use the JSON results, filtered to the requested app. Record its bundle ID,
executable, version, build, signing identity, and bundle location. A
`builtByDeveloper` flag alone does not establish debugger access: Rex's TestFlight
build reported that flag, while its signing identity was TestFlight distribution.

When no device is available, ask for connection/trust or work from an existing
artifact. Check command help for the installed tool version. Prefer the existing
pairing; don't replace it merely to get logs.

## Choose an accessible source of evidence

- For a supplied `.ipa` or `.app`, inspect the bundle and executable directly.
  Use `file`, `otool -L`, `otool -l`, `nm`, `swift-demangle`, and targeted
  `strings` searches. Check Mach-O encryption information before promising
  useful disassembly. A decompiler reconstructs approximate code, not the
  original Swift source.
- `devicectl device copy from` and `pymobiledevice3 apps pull` expose supported
  file domains, usually app data. An installed bundle path from metadata does
  not make its executable accessible through those domains. If an executable
  pull returns not-found or denied, report the limit rather than repeating it
  with invented paths. Look for a local build, an accessible companion, or a
  user-supplied artifact.
- A Mac companion can reveal shared types and wire messages. Label those as
  Mac-binary findings. Type and field names suggest architecture; they do not
  prove control flow. Prefer a live API contract or runtime trace to confirm it.
- Use an available REA/decompiler workflow for a relevant accessible binary.
  Check its installed tools and instructions first. REA does not by itself
  provide access to an iPhone's app executable. Avoid installing a large tool
  stack when a protocol query or targeted inspection answers the question.

For Rex-specific commands, API behavior, and the measured Termio bug, read
[the Rex case study](references/rex-terminal.md).

## Trace the connection and renderer

Identify the actual endpoint from the app's configuration or logs. Record the
transport, authentication mechanism, and which server process is listening.
Keep pairing tokens out of output; when launching with credentials, build an
argument array and sanitize captured output rather than interpolating a URL
into a shell command. Don't read unrelated credentials or terminal contents.

Capture only the target process and a bounded reproduction window:

```sh
uv tool run --from pymobiledevice3 pymobiledevice3 syslog live \
  --process-name "$executable" --label
```

Run live capture under a managed process, stop it after the reproduction
(typically 15–30 seconds), and collect its exit status. Use a timeout on device
launches as well. Retain matching app-subsystem lines rather than dumping the
whole device log. Device and Mac clocks can differ; correlate session IDs and
event order as well as timestamps.

For garbling, separate replacement characters or broken UTF-8 from misplaced
cells, rewrapped borders, and stale partial repaints. Inspect the active data
path before patching: Termio's legacy companion and `vt_stream` can coexist in
source while only one is enabled on the phone.

Measure these values through attachment, keyboard changes, rotation, and
reconnection as relevant to the reproduction:

- View bounds, native pixel scale, cell dimensions, and effective padding.
- The client's requested viewport, the server's accepted grid, and the
  renderer's actual rows and columns.
- Size ownership, snapshot/keyframe acceptance, and output after resize.

A terminal parsing cursor-positioned output needs the server's grid. A one-column
disagreement can look like text corruption even when UTF-8 decoding is correct.
For an ownership bug, check which client can apply a resize and what passive
clients do with their desired sizes. Don't infer authority from window focus.

## Apply and verify the fix

Patch the smallest confirmed cause. Check the pinned rendering library's
arithmetic, including DPI conversion and pixel flooring, rather than assuming
configuration points equal UIKit points. Keep custom renderer measurements
separate from embedded Ghostty measurements when their padding units differ.

Add a regression test for the observed failure when the logic is testable.
Run `swift build`, the relevant existing tests, and the iOS build. Use
[`ios-rebuild-dev`](../ios-rebuild-dev/SKILL.md) for installation and launch;
don't hand-edit signing or its deployment script. Establish whether the running
Mac daemon actually contains a related change before attributing behavior to it.
A Git merge does not deploy the daemon.

Repeat the same device reproduction and compare the server and renderer's
measurements. Remove temporary diagnostic logs, then rebuild and install the
clean version. Report what passed and what remains unverified. Follow the
rebuild skill's screenshot workflow: ask for a screenshot on a physical phone;
matching logs alone do not prove the screen looks correct.

Finish with the evidence used, its limitations, the concrete cause, changed
files, and validation. State whether changes are in a worktree, committed,
merged, installed, or pushed; those are separate outcomes.
