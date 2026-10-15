---
name: utmapp
description: Operates the UTM virtual machine app on macOS — lists, creates, starts, stops, suspends, clones, deletes, imports and exports VMs; runs commands inside a guest, transfers files, queries guest IPs, sends keyboard or mouse input, forwards USB devices, and inspects or updates VM configuration. Use when the user mentions UTM, utmctl, .utm bundles, "the UTM app", QEMU on a Mac, or Apple Virtualization.framework via UTM, or wants to automate macOS-hosted VMs from the shell or AppleScript. Covers both the QEMU backend (cross-architecture emulation) and the Apple Virtualization backend (native macOS/Linux on Apple Silicon).
license: Apache-2.0
compatibility: macOS with UTM 4.x installed. Automation goes through AppleScript, so a logged-in Aqua session is required — utmctl and `osascript` do not work over plain SSH or before login. The QEMU guest agent must be installed in the guest for `exec`, `file`, and `ip-address` operations.
metadata:
  upstream: https://github.com/utmapp/UTM
  utm-website: https://mac.getutm.app
  vm-gallery: https://mac.getutm.app/gallery/
---

# Using the UTM virtualization app

UTM is a macOS/iOS GUI for running virtual machines. On macOS it has two backends:

- **QEMU** — full emulation of 30+ architectures (x86_64, ARM64, RISC-V, PPC, …) plus HVF acceleration when host and guest architectures match. Required for Windows, BSDs, classic OSes, and anything cross-architecture. Supports USB pass-through, snapshots, port forwarding, custom QEMU args, and full automation (input, exec, files, IP).
- **Apple Virtualization** (`Virtualization.framework`) — native, very fast, but limited to macOS guests on Apple Silicon and modern Linux guests. No USB pass-through, no scripted input, no guest-agent file/exec.

A VM is stored as a `.utm` bundle (a directory). User VMs live in `~/Library/Containers/com.utmapp.UTM/Data/Documents/`. Backups are just file copies of the bundle.

There are three ways to drive UTM from a script:

1. **`utmctl`** — bundled CLI at `/Applications/UTM.app/Contents/MacOS/utmctl` (also linked as `utmctl` in some installs). Best for shell automation. See [references/utmctl.md](references/utmctl.md).
2. **AppleScript / JXA** — full scripting dictionary in `UTM.sdef`. Needed for input automation, configuration edits, and creating VMs. See [references/applescript.md](references/applescript.md).
3. **Bundle / config edits** — when UTM is closed you can read or rewrite `config.plist` inside a `.utm` bundle directly. See [references/configuration.md](references/configuration.md).

For end-user workflows (installing Linux, Windows, macOS guests; networking; file sharing) see [references/workflows.md](references/workflows.md). For known gotchas and performance tuning see [references/troubleshooting.md](references/troubleshooting.md).

## Gotchas — read these before automating

- **No SSH / no headless.** UTM scripting goes through the AppleScript bridge. `utmctl` and `osascript` only work inside a logged-in graphical session. From SSH you will get permission errors. Workarounds: run a launchd agent, use `caffeinate`, or use Screen Sharing first.
- **VM identifier is a name OR a UUID.** Pass either; UTM resolves both. Names with spaces must be quoted: `utmctl start "Ubuntu 24.04"`.
- **`delete` has no confirmation.** Always check with `utmctl list` first.
- **`stop` defaults to `--force` (sends a stop request to the QEMU/VZ backend).** Use `--request` to ask the guest OS to power down cleanly, or `--kill` only as a last resort.
- **Apple-backend VMs do not support `input keystroke`, `input mouse click`, `input scan code`, USB connect/disconnect, or QEMU guest-agent commands** (`exec`, `file pull`, `file push`, `ip-address`). Detect the backend before calling these — see the recipe below.
- **`exec`, `file`, and `ip-address` need the QEMU guest agent.** Install `qemu-guest-agent` in Linux (`apt install qemu-guest-agent && systemctl enable --now qemu-guest-agent`) or `virtio-win` Guest Tools on Windows. Without it these commands time out or return "no agent".
- **Bridged networking + macOS Sequoia** require granting UTM the "Local Network" privacy permission, otherwise the guest gets no IP.
- **JIT on iOS** is a separate world — see [references/troubleshooting.md](references/troubleshooting.md) (UTM SE, AltStore, jailbreak workarounds). All scripting in this skill is **macOS only**.

## Quick start: utmctl

Use `utmctl` for nearly all routine operations. The binary lives inside the app bundle:

```bash
# Make it accessible (one-time; needs sudo because /usr/local/bin is root-owned)
sudo ln -sf /Applications/UTM.app/Contents/MacOS/utmctl /usr/local/bin/utmctl

# List all VMs (UUID, status, name)
utmctl list

# Start / suspend / stop
utmctl start "Ubuntu"
utmctl suspend "Ubuntu" --save-state
utmctl stop "Ubuntu" --request    # ask guest to power off
utmctl stop "Ubuntu"               # default = force stop backend
utmctl stop "Ubuntu" --kill        # last resort

# Status of one VM
utmctl status "Ubuntu"             # → stopped | starting | started | paused | …

# Disposable / recovery boot
utmctl start "Ubuntu" --disposable # discard all changes on stop
utmctl start "macOS Sonoma" --recovery

# Clone, delete, version
utmctl clone "Ubuntu" --name "Ubuntu-test"
utmctl delete "Ubuntu-test"        # NO confirmation
utmctl version
```

Guest-agent operations (QEMU backend, agent installed):

```bash
# Run a command, capture stdout/stderr/exit code
utmctl exec "Ubuntu" -- /bin/bash -c "uname -a"
utmctl exec "Ubuntu" --env LANG=C -- ls /etc

# Push host stdin to guest file, pull guest file to host stdout
echo "hello" | utmctl file push "Ubuntu" /tmp/hello.txt
utmctl file pull "Ubuntu" /var/log/syslog > syslog.txt

# Get guest IPs (IPv4 first, then IPv6)
utmctl ip-address "Ubuntu"
```

USB pass-through (QEMU backend):

```bash
utmctl usb list                                 # discover devices
utmctl usb connect "Windows" 046D:C016          # by VID:PID (hex)
utmctl usb connect "Windows" 4                  # by location id
utmctl usb disconnect 4
```

`utmctl --help` and `utmctl <command> --help` print full usage. Full reference with every flag, exit code semantics, and edge cases is in [references/utmctl.md](references/utmctl.md).

`utmctl` does not cover VM creation, configuration edits, keystroke/mouse injection, or registry edits — those require AppleScript. See the next section.

## Choosing utmctl vs AppleScript

| Need | Use |
| --- | --- |
| start/stop/suspend/list/status/clone/delete | `utmctl` |
| exec, file pull/push, ip-address, USB connect/disconnect | `utmctl` |
| Send keystrokes / text / mouse clicks into the guest | AppleScript (`input keystroke`, `input mouse click`, `input scan code`) |
| Create a new VM from scratch | AppleScript (`make new virtual machine`) |
| Read or update VM configuration (RAM, CPU, drives, network, ports) | AppleScript (`configuration of …`, `update configuration`) |
| Wait for a VM to reach a state, build retry loops | shell + `utmctl status` polling, OR AppleScript |
| Rebind shared host directories | AppleScript (`update registry` — replaces ALL shares; see [references/applescript.md#registry-suite](references/applescript.md#registry-suite)) |
| Mount/unmount a removable ISO at runtime | Not exposed via scripting — requires the GUI |

If you need both kinds of operations in one script, drive everything from `osascript -l JavaScript` (JXA) — it is the only place where input automation, configuration, and lifecycle commands all coexist.

## Backend-aware automation pattern

Many commands are silently a no-op or error on the Apple backend. Always branch:

```bash
backend=$(osascript -e 'tell application "UTM" to get backend of virtual machine named "MyVM" as text')
case "$backend" in
  qemu)  utmctl exec "MyVM" -- /bin/sh -c 'whoami' ;;
  apple) echo "Apple backend: skipping guest-agent exec" ;;
  *)     echo "VM unavailable" >&2; exit 1 ;;
esac
```

Or in JXA (`osascript -l JavaScript`):

```javascript
const utm = Application("UTM");
const vm = utm.virtualMachines.byName("MyVM");
if (vm.backend() === "qemu") {
    // safe to call input/exec/USB
}
```

## Wait-until-ready recipe

`utmctl start` returns once the backend has launched, **not** when the guest is booted. To wait until the guest is reachable, poll either status or — better — the guest agent:

```bash
utmctl start "Ubuntu"
for i in $(seq 1 60); do
    if utmctl ip-address "Ubuntu" 2>/dev/null | grep -qE '^[0-9]+\.'; then
        echo "Guest up after ${i}s"; break
    fi
    sleep 2
done
```

For Apple-backend VMs without a guest agent, ping the expected hostname (`*.local` via mDNS) or scrape the SPICE display title from the UI.

## Common shapes of work

- **"Run command X in VM Y, return output"** → `utmctl exec`. See [references/utmctl.md#exec](references/utmctl.md#exec).
- **"Spin up a fresh VM from a template"** → `utmctl clone --name`, then `utmctl start --disposable` for ephemeral runs.
- **"Type something into the login screen"** → AppleScript `input keystroke` / `input scan code`. See [references/applescript.md](references/applescript.md#input-automation).
- **"Change VM configuration"** → AppleScript `update configuration` (VM must be stopped).
- **"Rebind a shared host directory"** → AppleScript `update registry` (replaces every shared dir at once; this command does NOT cover removable-media swaps — those require the GUI).
- **"Backup a VM"** → stop it, `cp -R "MyVM.utm" /backup/`. Nothing else is required.
- **"Install Ubuntu / Windows / macOS guest"** → see [references/workflows.md](references/workflows.md).

## Map of the references directory

| File | When to read it |
| --- | --- |
| [references/utmctl.md](references/utmctl.md) | Authoring or debugging shell automation, mapping flags, exit codes |
| [references/applescript.md](references/applescript.md) | Sending input, creating VMs, editing configuration, JXA examples |
| [references/configuration.md](references/configuration.md) | Hand-editing `.utm/config.plist` while UTM is closed; understanding bundle layout |
| [references/workflows.md](references/workflows.md) | Walking a user through installing Linux, Windows ARM, Windows x86, macOS, or wiring up file sharing and networking |
| [references/troubleshooting.md](references/troubleshooting.md) | "Why doesn't this work?" — JIT/iOS, performance, network, snapshots, GPU |

Read each on demand. Do not preload them.
