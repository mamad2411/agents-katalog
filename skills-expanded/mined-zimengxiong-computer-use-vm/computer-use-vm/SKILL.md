---
name: computer-use-vm
description: Let agents run disposable VMs for computer-use and GUI automation instead of controlling the host desktop.
---

# Computer Use VM

Use `computer-use-vm` or this skill's wrapper to control disposable VMs.

## Base Image Policy

Each machine builds its own base locally.

If `computer-use-vm-base` is missing, create it locally with the commands in this skill. Before first-time setup, tell the user they will need to VNC into the VM and approve macOS Screen Recording and Accessibility prompts for the guest agent/helper. Do not present first-time setup as fully unattended.

## Default Workflow

1. Run diagnostics:

```bash
computer-use-vm diagnose
```

2. Prefer Tart for headless/background runs. Use UTM when an existing UTM VM is the target.

3. Prefer the prepared base image:

```bash
computer-use-vm clone computer-use-vm-base <task-vm>
```

This base has the guest agent installed as a user LaunchAgent and has the required macOS privacy grants for native screenshots.

4. Prepare a raw Tart base image only if `computer-use-vm-base` does not exist:

Before running this setup, tell the user: "The first setup needs a VNC session into the VM so you can approve macOS Screen Recording and Accessibility permissions for the guest agent/helper."

```bash
computer-use-vm prepare-base computer-use-tahoe-base
computer-use-vm clone computer-use-tahoe-base computer-use-vm-base
computer-use-vm start computer-use-vm-base --vnc
computer-use-vm configure-guest computer-use-vm-base
computer-use-vm install-agent computer-use-vm-base
computer-use-vm start-agent computer-use-vm-base
computer-use-vm verify-agent computer-use-vm-base
computer-use-vm provision-dev-tools computer-use-vm-base
computer-use-vm stop computer-use-vm-base
```

`verify-agent` must report `ok: true`, `screen_capture_trusted: true`, and `accessibility_trusted: true` before treating a VM as a prepared base. If it does not, keep the VM running with `--vnc`, approve Screen Recording and Accessibility inside the guest for the computer-use VM helper/agent, then rerun `computer-use-vm start-agent <vm>` and `computer-use-vm verify-agent <vm>`. After verification succeeds, stop this VM and use it as the cloned base so future task VMs inherit the guest-side approvals.

5. Use clone/delete isolation when a base image exists:

```bash
computer-use-vm clone <base-vm> <task-vm>
computer-use-vm start <task-vm> --mount "repo:$PWD:tag=repo"
computer-use-vm ip <task-vm>
```

For host workspace access, prefer Tart directory mounts over copying:

```bash
computer-use-vm start <task-vm> --mount "repo:$PWD:tag=repo"
computer-use-vm exec <task-vm> zsh -lc 'cd /Volumes/My\ Shared\ Files/repo && pwd && ls'
```

macOS guests automount the shared directory under `/Volumes/My Shared Files/repo`. Use `push` only when a mount is unavailable or the VM is already running without the needed share:

```bash
computer-use-vm push <task-vm> ./local-file-or-folder /Users/admin/local-file-or-folder
```

When `start --vnc` returns `novnc.url`, open it in Codex's in-app browser if available so the user can watch. Otherwise, tell the user the URL. Do not use noVNC for agent control.

The prepared base should already have Homebrew, XcodeGen, Make, xcbeautify, and swiftformat. If a base is missing those tools, start it and run:

```bash
computer-use-vm provision-dev-tools computer-use-vm-base
```

Full `xcodebuild` and SwiftLint require full `/Applications/Xcode.app`; Command Line Tools alone are not enough for those checks.

6. Configure and install the guest agent only for raw or unprepared VMs:

```bash
computer-use-vm configure-guest <task-vm>
computer-use-vm install-agent <task-vm>
```

7. Start or restart the agent inside the guest only for raw or unprepared VMs:

```bash
computer-use-vm start-agent <task-vm>
computer-use-vm verify-agent <task-vm>
```

Inside the VM, `configure-guest` reduces friction for agents by enabling passwordless sudo for the admin user, disabling sleep, and removing stale old agent services. `start-agent` may use any port; it creates a VM-internal autostart entry for that port. The host does not need additional accessibility or screen recording grants.

8. Drive the VM through the agent:

```bash
computer-use-vm agent ping --host <guest-ip>
computer-use-vm agent list-apps --host <guest-ip>
computer-use-vm agent state --host <guest-ip> --app Safari --depth 5 --max-children 80
computer-use-vm agent screenshot --host <guest-ip> --output /tmp/vm.png
computer-use-vm agent ax-tree --host <guest-ip> --app Safari --depth 5 --max-children 80
computer-use-vm agent ax-press --host <guest-ip> --app Safari --id <element-id>
computer-use-vm agent ax-click --host <guest-ip> --app Safari --id <element-id>
computer-use-vm agent ax-set-value --host <guest-ip> --app Safari --id <element-id> --value "text"
computer-use-vm agent ax-action --host <guest-ip> --app Safari --id <element-id> --action-name AXShowMenu
computer-use-vm agent click --host <guest-ip> --x 200 --y 180 --click-count 2
computer-use-vm agent drag --host <guest-ip> --from-x 200 --from-y 180 --to-x 400 --to-y 180
computer-use-vm agent scroll --host <guest-ip> --app Safari --id <element-id> --direction down --pages 1
computer-use-vm agent type --host <guest-ip> --text "hello"
computer-use-vm agent key --host <guest-ip> --key Return
```

Prefer `state --app <name-or-bundle-id>` as the native Computer Use style entry point: it returns a screenshot plus the target app/window accessibility tree. Use `list-apps` when the app name or bundle id is unknown. Prefer AX actions over coordinate actions when an element id is available. Use `state` or `ax-tree` first, choose an element by role/title/description/frame/actions, then use `ax-press`, `ax-click`, `ax-set-value`, `ax-action`, or `scroll` with the same app/depth/max-children parameters.

If guest networking or macOS privacy permissions block direct screenshots, start the VM with `--vnc` and use the VNC fallback:

```bash
computer-use-vm vnc screenshot --host <guest-ip> --output /tmp/vm.png
computer-use-vm vnc click --host <guest-ip> --x 200 --y 180
computer-use-vm vnc type --host <guest-ip> --text "hello"
```

9. After each task-use, stop the task VM and **ask the user whether they want to keep it or delete it**. If they do not request persistence, delete the VM by default.

## Modes

- Headless/background: `start` defaults to hidden/no-graphics where the backend supports it. Use this for shell/background work; pixel screenshots are not available without a display surface.
- Visible/introspection: pass `--visible` to show the VM window, or `--vnc` to expose a VNC screen-sharing session.
- Browser-visible VNC: `start --vnc` may return `novnc.url` for user observation.
- Disposable UTM run: pass `--disposable` for UTM snapshot-style runs.
- Tart disposable run: clone from a base VM, work in the clone, then delete the clone.

## MCP Server

Expose bridge tools over stdio with:

```bash
computer-use-vm mcp
```

Available tools include VM diagnostics, list, start with Tart mounts, stop, clone, delete, IP lookup, `vm_exec`, `vm_push`, guest-agent start/stop, and guest-agent app state/list/activation, snapshot, AX-tree, AX actions, click, drag, scroll, type, and key input.

## Important Constraints

- The fastest path is the in-guest agent because screenshots, AX-tree introspection, and input are native to the VM.
- VNC/SPICE/UTM window automation is fallback only; it is useful for bootstrap, visual debugging, and pre-permission introspection but adds latency and coordinate fragility.
- macOS privacy prompts may require granting Screen Recording and Accessibility permissions inside the guest.
- Each machine builds its own base locally. That keeps Apple software, privacy grants, user state, caches, and machine-specific data out of GitHub, npm, releases, and Hugging Face.
- UTM `utmctl` can fail from non-GUI sessions with Apple Event permission errors; use Tart when host-level GUI scripting permissions are unavailable.
