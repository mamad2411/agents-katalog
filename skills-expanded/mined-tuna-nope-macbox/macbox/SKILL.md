---
name: macbox
description: Set up and run macbox, which gives a Linux host a full macOS VM with GPU acceleration (Reims vGPU), Xcode, a pool of iOS Simulators and T3 Code's Device panel, in Docker. Use when the user wants the iOS Simulator, Xcode or macOS on Linux, iOS testing for coding agents without a Mac or a cloud service, a macOS VM with Metal, or Docker-OSX with GPU acceleration; and to start, stop, check or repair that VM (macbox up/down/status/doctor/next). For using the simulators once it's set up, read the simulators skill.
---

# macbox

macbox runs macOS 26 in Docker on a Linux host, drawn with Metal on the host's own GPU. It is the
Mac that `mac-sim` (the simulators skill) builds and runs iOS apps on.

## Where it stands

```sh
macbox next      # every setup step, ticked or not, and the next one to do
macbox doctor    # the host: KVM, GPU, vm.max_map_count, Docker, disk
macbox status    # the container, the VM, the screen, SSH
```

Settings: `~/.config/macbox/macbox.env`. The checkout holds the docs: `readlink -f "$(command -v macbox)"`.

## Setting it up

Follow `AGENTS.md` in macbox's checkout (https://github.com/0xdaniell/macbox). In short:
`macbox init`, `doctor`, `build` (20 to 60 minutes), `create`, `boot-picker on`, `up`. Then the
GUI steps, which you can do yourself with `macbox screenshot` / `click` / `type` / `key` / `wait`:
install macOS, `macbox recovery-fix` from Recovery's Terminal, Setup Assistant, then
`macbox ssh-bootstrap`. After that, everything is over SSH: `disk nvme`, `provision`,
`xcode <the user's .xip>`, `pool`, `t3 register` / `t3 fix-hub`, `agents install`.

Ask the user before changing the host itself (groups, sysctl, Docker). Never ask for a password in
chat: the macOS password is typed into the VM. Xcode's `.xip` needs the user's Apple Account sign-in
at developer.apple.com, so the user downloads it.

## Day to day

| | |
|---|---|
| start, stop | `macbox up`, `macbox down` |
| the screen | http://127.0.0.1:6081/ (Selkies), or `macbox view local` on the host's desktop |
| a shell on the Mac | `ssh macbox` (or `macbox ssh`) |
| logs | `macbox logs qemu`, `macbox logs selkies` |
| the T3 Device panel shows no picture after a T3 update | `macbox t3 fix-hub` |
| a newer build | `macbox build`, then `macbox down && macbox up` |
| a copy of the disk | `macbox backup <name>` (VM stopped) |

When something fails: `docs/troubleshooting.md` in the checkout.
