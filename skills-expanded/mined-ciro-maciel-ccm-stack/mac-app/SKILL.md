---
name: mac-app
description: Mac apps that open at login in the menu bar only, one window, template icon, versioned installs. Use for any macOS app.
---

# Mac apps done right

The reference is open source: [Cleaner](https://github.com/ciro-maciel/cleaner), a Swift Mac app by Ciro Cesar Maciel that follows every rule below.

## Opened at login: menu bar only

When macOS opens the app at login, show only the menu bar icon: no window, no welcome screen, no permission prompt. When the person opens it from Finder or Spotlight, show the window.

Detect a login launch at the top of `applicationDidFinishLaunching`, and guard every window shown at launch:

- The launch Apple Event carries the login-item mark (`keyAELaunchedAsLogInItem`) when macOS opened the app at login.
- `SMAppService.mainApp` does not always set it, so also count as login a launch while the login item is enabled and the Mac has been up for less than ten minutes.

See [`LoginLaunch.swift`](https://github.com/ciro-maciel/cleaner/blob/main/Sources/Cleaner/UI/LoginLaunch.swift) in Cleaner.

## One window

Settings, history and the rest are items in the window's sidebar, grouped under labels, not separate windows. No "About" window: the app name, version and author are already in the sidebar footer. Dialogs open inside the window.

## The menu bar icon

An 18 x 18 pt template image (`isTemplate = true`), so macOS colors it for light, dark and highlighted menu bars. A solid square with the app's letter cut out reads at that size; a detailed logo does not.

## Every build is a version

Every installer you produce gets a new version number and replaces the app in `/Applications`, so what the person runs is always what you built. Never hand them a build with the same version as the last one.

## Prove it

Turn on "Open at Login", restart the Mac (or log out and in), and confirm that only the menu bar icon appears. Then open the app from Spotlight and confirm the window appears.
