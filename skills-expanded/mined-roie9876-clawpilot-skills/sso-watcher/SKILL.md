---
name: sso-watcher
description: "Install and manage the Hammerspoon-based SSO auto-picker for Clawpilot (or any Electron app). Automatically dismisses the Microsoft Entra ID account picker by selecting the configured account and clicking Continue. macOS only. Triggers include: 'sso watcher', 'install sso', 'sso auto-picker', 'setup sso', 'hammerspoon sso', or any request to auto-dismiss the SSO login dialog."
---

# /sso-watcher — Hammerspoon SSO Auto-Picker

Automatically dismisses the Microsoft Entra ID / SSO account picker modal that
appears inside Clawpilot (or any Electron app) by selecting the configured
account and clicking Continue.

**macOS only** — uses [Hammerspoon](https://www.hammerspoon.org/) for
Accessibility API access with zero TCC headaches.

## How It Works

1. The SSO account picker is NOT inside Clawpilot — it's rendered by
   **AppSSOAgent** (`com.apple.AppSSOAgent`), the macOS Enterprise SSO broker
   from Company Portal
2. Hammerspoon polls AppSSOAgent's AX (Accessibility) tree every 3 seconds
3. Also triggers on any app activation (SSO agent may pop up for any app)
4. Looks for SSO dialog markers: "Accounts found", "Sign in to your account", etc.
5. Finds the AXRow containing the configured email and clicks it
6. Waits 0.8s then clicks the "Continue" button
7. 15-second cooldown after each successful click to avoid loops

## Files

| File | Location | Purpose |
|------|----------|---------|
| `sso-watcher.lua` | `~/.hammerspoon/sso-watcher.lua` | Main Hammerspoon module |
| `sso-watcher-config.lua` | `~/.hammerspoon/sso-watcher-config.lua` | Configuration (account, app name, intervals) |
| `init.lua` | `~/.hammerspoon/init.lua` | Hammerspoon entry point (loads the module) |
| Log | `~/Scripts/sso-watcher-hammerspoon.log` | Runtime log |

## Installation

Run the install script with the target Microsoft account email:

```bash
bash "$HOME/customer-skills/sso-watcher/install.sh" user@microsoft.com
```

Or for a custom app name:

```bash
bash "$HOME/customer-skills/sso-watcher/install.sh" user@microsoft.com "MyElectronApp"
```

The installer:
1. Installs Hammerspoon via Homebrew (if missing)
2. Copies `sso-watcher.lua` to `~/.hammerspoon/`
3. Creates config with the account email
4. Adds `require("sso-watcher")` to `~/.hammerspoon/init.lua`
5. Enables Hammerspoon auto-launch at login
6. Launches/reloads Hammerspoon

### macOS Permissions

After installation, Hammerspoon needs **Accessibility** access:

> **System Settings → Privacy & Security → Accessibility → Toggle ON: Hammerspoon**

Without this, the watcher cannot read or interact with the SSO dialog.

## Uninstallation

```bash
bash "$HOME/customer-skills/sso-watcher/uninstall.sh"
```

Removes the module, config, and log. Does NOT uninstall Hammerspoon itself.

## Configuration

Edit `~/.hammerspoon/sso-watcher-config.lua`:

```lua
return {
    account       = "user@microsoft.com",   -- email to auto-select
    poll_interval = 3,                       -- seconds between checks
    cooldown      = 15,                      -- seconds after successful click
    log_file      = os.getenv("HOME") .. "/Scripts/sso-watcher-hammerspoon.log",
}
```

The watcher always monitors `AppSSOAgent` (`com.apple.AppSSOAgent`) — the system SSO
broker. No need to configure which app triggers the SSO dialog.

After editing, reload Hammerspoon: click the Hammerspoon menu bar icon → Reload Config,
or run `hs -c "hs.reload()"` from terminal.

## Troubleshooting

### Watcher not triggering

1. **Check Hammerspoon is running**: look for the hammer icon in the menu bar
2. **Check Accessibility**: System Settings → Privacy & Security → Accessibility → Hammerspoon must be ON
3. **Check logs**: `tail -f ~/Scripts/sso-watcher-hammerspoon.log`
4. **Check config**: `cat ~/.hammerspoon/sso-watcher-config.lua` — verify the email is correct
5. **Reload**: Click Hammerspoon menu bar → Reload Config

### "SSO markers found but account element not found"

The dialog was detected but your email wasn't in the AX tree yet. This is usually
a timing issue — the watcher will retry on the next poll (3s).

### Account clicked but Continue button not found

The 0.8s delay may not be enough on a slow machine. Edit the config to increase
`cooldown` or modify `sso-watcher.lua` to increase the `doAfter` delay.

## Skill Invocation

When the user asks to install or manage the SSO watcher via Clawpilot:

### Install (first time on a new Mac)

1. Detect the user's Microsoft email:
   ```
   m365_get_my_profile() → email
   ```
   Or ask the user.

2. Run the installer:
   ```bash
   bash "$HOME/customer-skills/sso-watcher/install.sh" "user@microsoft.com"
   ```

3. Remind the user to grant Accessibility to Hammerspoon.

### Check status

```bash
pgrep -x Hammerspoon && echo "Running" || echo "Not running"
cat ~/.hammerspoon/sso-watcher-config.lua
tail -5 ~/Scripts/sso-watcher-hammerspoon.log
```

### Change account

```bash
bash "$HOME/customer-skills/sso-watcher/install.sh" "newemail@microsoft.com"
```

### Uninstall

```bash
bash "$HOME/customer-skills/sso-watcher/uninstall.sh"
```

## Prerequisite Auto-Install

This skill has no sibling skill dependencies. It only requires:

| Tool | Check | Install |
|------|-------|---------|
| Homebrew | `command -v brew` | https://brew.sh |
| Hammerspoon | `ls /Applications/Hammerspoon.app` | `brew install --cask hammerspoon` |

The install script handles Hammerspoon installation automatically.

## Platform Note

This skill is **macOS only**. Hammerspoon does not exist on Linux or Windows.
On other platforms, the SSO picker must be handled differently (e.g., browser
extension, AutoHotkey on Windows).
