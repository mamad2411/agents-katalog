---
name: kde-desktop-integration
description: Work with KDE Plasma, Wayland, desktop launchers, workspaces, portals and display integration without disrupting a live session.
---

# KDE integration

1. Check Plasma version, session type, display geometry and scale before
   choosing an integration. X11-only automation is not a Wayland solution.
2. Prefer existing KDE features and supported D-Bus/application APIs. Inspect
   an interface before calling it; do not guess method signatures.
3. Use stable launcher paths and per-user configuration. Temporary AppImage
   mount paths are not persistent application targets. Validate desktop entries.
4. Preserve windows, workspaces, clipboard contents and other users' work.
   Do not restart KWin or move windows without authorization.
5. Check PipeWire, the KDE portal and app-specific capture plugins for screen
   recording. The user must select and approve capture/control permissions.
6. Keep screenshot pixels, logical desktop coordinates and client-scaled RDP
   coordinates distinct. Verify pointer alignment in more than one location.
7. A shared RDP desktop is not an independent login session. A virtual monitor
   can change the workspace layout; make that an explicit user choice.
8. Do not modify the local monitor's resolution/HDR merely to make remote
   access easier without explaining the effect and obtaining approval.

For real GUI control use `linux-computer-use`. Browser tools requiring Chrome
or Edge cannot verify settings in an existing Firefox window.
