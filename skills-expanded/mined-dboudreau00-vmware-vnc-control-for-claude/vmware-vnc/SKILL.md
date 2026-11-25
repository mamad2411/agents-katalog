---
name: vmware-vnc
description: Type keystrokes into a VMware virtual machine and capture its screen over VNC, without guest tools or network access in the guest. Use when automating or testing a VM at a level vmrun cannot reach — a GRUB menu, an initramfs passphrase prompt, a display-manager login screen, an OS installer — or when `vmrun captureScreen` / `runScriptInGuest` / `checkToolsState` fail or return "Anonymous guest operations are not allowed". Also use to screenshot a VM whose guest tools are absent, broken, or not yet running.
---

# Driving a VMware VM over VNC

`vmrun`'s guest operations run *inside* the guest: they need open-vm-tools alive and, usually,
guest credentials. That rules out everything before userspace and every guest whose tools are
missing or broken.

VNC operates at the **hypervisor's virtual keyboard and framebuffer**, below the guest OS. So it
works at a bootloader menu, at an initramfs passphrase prompt, at a login screen, and inside an OS
installer — all places `vmrun` cannot go.

## Enable VNC on the VM

Add to the `.vmx` **with the VM powered off**:

```
RemoteDisplay.vnc.enabled = "TRUE"
RemoteDisplay.vnc.port = "5951"
RemoteDisplay.vnc.password = "secret12"
```

Three things that will otherwise waste your time:

- **The password is DES-based and truncated to 8 bytes.** Longer strings silently use only the
  first eight.
- **Do not append these lines blindly.** VMware Workstation often already writes
  `RemoteDisplay.vnc.enabled = "FALSE"`, and a duplicate key makes it refuse the file entirely with
  *"Cannot read the virtual machine configuration file"*. Filter out existing `RemoteDisplay.vnc.*`
  lines and rewrite the file.
- **Keep line endings consistent.** Appending CRLF lines to an LF `.vmx` can also break parsing.

Use a distinct port per VM if you run several.

## Use it

```bash
export VNC_PASSWORD=secret12

python vnc.py --port 5951 info                      # handshake + framebuffer geometry
python vnc.py --port 5951 screenshot shot.png       # prints "WxH digest=XXXXXXXX"
python vnc.py --port 5951 key Down Down Return
python vnc.py --port 5951 type 'correct horse battery staple' --enter
python vnc.py --port 5951 wait-change --timeout 180 --out changed.png
```

`screenshot` prints a CRC digest of the frame. **Comparing digests is the reliable way to tell
whether the guest reacted** to input — far better than a fixed sleep.

Key names are X11 keysyms: `Return` `Escape` `Tab` `BackSpace` `Up` `Down` `Left` `Right` `Home`
`End` `PageUp` `PageDown` `Delete` `Insert` `Space` `F1`–`F12` `Shift_L` `Control_L` `Alt_L`
`Super_L`. Any single character also works: `python vnc.py --port 5951 key e`.

## Patterns that work

**Screenshot before you type.** A passphrase typed before the prompt is ready goes nowhere, and
the boot then continues into a state indistinguishable from a wrong passphrase. Confirm what is on
screen first.

```bash
python vnc.py --port 5951 screenshot /tmp/state.png   # then LOOK at it
```

**Poll on the digest, not the clock.** Guests without hardware acceleration are slow and their
timing varies wildly.

```bash
python vnc.py --port 5951 wait-change --timeout 300 --out /tmp/booted.png
```

**Typing is deliberately paced** (~30 ms/char, `--delay` to change it). Bootloaders and initramfs
prompts are polling readers; blasting a string at wire speed drops characters, and a dropped
character in a passphrase looks exactly like the wrong passphrase.

**Reaching a shell in a desktop guest**, when there is no direct binding: `key Super_L`, then
`type 'terminal'`, then `key Return`. Verified on Cinnamon.

## Limits, stated plainly

- **Raw encoding only.** Every RFB server must support it, so this always works, but a frame is
  `width × height × 4` bytes on the wire. Fine for a test harness; useless for interactive use.
- **No mouse.** Keyboard and framebuffer only. Add `PointerEvent` (message type 5) if you need it.
- **Security types None(1) and VNCAuth(2).** No TLS, no RSA-AES. Intended for loopback to your own
  hypervisor.
- **No screen-scraping.** You get pixels. If a stage needs to *read* text, either look at the PNG
  yourself or have the guest write to a serial port backed by a host file
  (`serial0.fileType = "file"`), which is a much better channel for structured status.
- VMware may drop VNC support in a future release; it is present in Workstation 17.

## Why the digest matters more than it looks

The single most common failure in VM automation is a check that cannot fail — a stage that reports
success because nothing contradicted it. A frame digest is a cheap, honest signal: if the guest did
not react, the digest is unchanged, and no amount of waiting turns that into a pass.

Before trusting any check built on this, ask what it would report if the mechanism were broken. If
the answer is "the same thing", the check is worthless — send a key you know does nothing and
confirm the digest stays put.
