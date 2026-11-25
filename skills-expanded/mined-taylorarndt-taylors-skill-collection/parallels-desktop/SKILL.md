---
name: parallels-desktop
description: Everything Parallels Desktop on a Mac - create new virtual machines (Windows 11, Linux, macOS), tune them for speed, battery or gaming (game mode), set up a screen reader such as NVDA inside the VM, take and restore snapshots, share folders, run commands inside the guest, and troubleshoot it when something breaks, especially no sound, a screen reader that goes silent, audio that won't follow Bluetooth headphones, a slow or stuck VM, or Parallels Tools problems. Use whenever the user mentions Parallels, a Windows VM on their Mac, prlctl, NVDA or JAWS in a VM, "my VM has no sound", "make my VM faster", "set up a gaming VM", "create a Windows VM", or anything else about virtual machines in Parallels.
allowed-tools: Bash(prlctl list:*), Bash(prlctl status:*), Bash(prlctl snapshot-list:*), Bash(prlctl --version), Bash(prlctl --help), Bash(prlctl set --help), Bash(prlsrvctl info:*), Bash(system_profiler:*), Bash(sysctl:*), Bash(df:*), Bash(du:*), Bash(sw_vers)
---

# Parallels Desktop

This skill handles anything to do with Parallels Desktop on a Mac: building VMs, tuning them, setting up accessibility inside them, and fixing them when they break. It was written from real work on a 16 GB M2 MacBook Air running a Windows 11 ARM VM with the NVDA screen reader, using Bluetooth bone-conduction headphones.

## How to work

**Act like an assistant.** Do the digging yourself: read the VM's settings, its log, and the Mac's audio devices. The user should only have to make decisions. Turn each decision into a short AskUserQuestion with plain options. Put the recommended option first, and say what each option changes and what it costs.

**Report for a screen reader.** The user may be blind. Use plain sentences and short lists, with no wide tables and no emoji. Run every command yourself. Never hand over commands to paste.

**Be careful with a running VM.** The user may be working in it, possibly with a screen reader that depends on the VM's sound.
- Before you stop, restart, suspend or reset a running VM, ask, and warn that unsaved work in the guest will be lost.
- Settings that can change while the VM is running (sound devices, startup view, many optimization options) are fine to change after the user agrees.
- Memory, CPU count, hypervisor type and the video adapter need the VM shut down. Group those changes so the VM only goes down once.
- Before a big change (new drivers, a major Windows setting, a registry edit), offer to take a snapshot first: `prlctl snapshot "<VM>" --name "<what and when>"`.

**Don't touch the user's Claude Code settings or permissions.** If something is blocked (deleting a VM or a snapshot, for example), say what's needed and why, and ask the user to switch to manual mode with Shift+Tab. Never just say "I can't".

**Check the edition.** `prlctl` and `prlctl exec` need Parallels Desktop Pro or Business. If `prlctl` isn't found or refuses, say so and offer the parts that work through the app.

## Step 1: Look before acting

Run these first. They're all read-only.

- `prlctl --version`, `prlctl list -a -o name,status,ip`
- `prlctl list -i "<VM>"` for the full configuration: CPUs, memory, video, sound, CD/ISO, Tools version, uptime
- `prlsrvctl info` for the host's device list. It's the only place that shows the exact names Parallels uses for sound outputs.
- `sysctl -n hw.memsize` and `df -h /System/Volumes/Data`, so any memory or disk suggestion fits the Mac
- The VM's own log: `~/Parallels/<VM>.pvm/parallels.log` (it can also be wherever `--dst` put the VM). Search it for `error|fail` and for the area in question (`PrlAudioCore`, `HostAudio`, `Tools`, `Network`).

Then explain in plain words what you found, before you suggest anything.

## Create a new VM

Ask what the user wants it for (everyday Windows apps, development, testing, gaming, a screen-reader setup), then match the settings to that.

- **Windows 11 on Apple silicon:** the simplest route is the Parallels Installation Assistant, which downloads Windows from Microsoft for you. Open it with `open -a "Parallels Desktop"` and choose File > New. Tell the user it opens a window they'll need to move through, and offer to help step by step.
- **From the command line:** `prlctl create "<name>" --distribution win-11` (`--distribution list` shows the choices: ubuntu, fedora, kali, debian, win-11 and many more). Then attach an installer ISO with `prlctl set "<name>" --device-set cdrom0 --image "<path to iso>" --connect`, and start it with `prlctl start "<name>"`.
- **macOS guest (Apple silicon only):** `prlctl create "<name>" -o macos --restore-image "<path to .ipsw>"`.
- **Sizing:** leave macOS at least half its RAM. On an 8 GB Mac, give the VM 3 to 4 GB. On 16 GB, 4 to 6 GB. On 32 GB or more, 8 to 12 GB. For CPUs, `--cpus auto` is fine for most uses.
- **After the first boot:** install Parallels Tools (`prlctl installtools "<name>"`) if it isn't already in, and detach the installer ISO (`--device-set cdrom0 --image ""`) so the VM doesn't depend on a file the user may delete later.

## Tune for what the user does

Offer these as named profiles and ask which one fits. Changes marked "VM off" need a shutdown.

**Game mode**
- `prlctl set "<VM>" --faster-vm on --longer-battery-life off --resource-quota unlimited`
- `--3d-accelerate highest`
- `--vertical-sync off`, which gives lower input lag but can tear the picture. Ask which matters more.
- `--fullscreen-optimize-for-games on --startup-view fullscreen`. This hides the Mac's Dock, menu bar and notifications while playing.
- `--smart-mouse-optimize auto`, so the pointer is captured in games and free elsewhere.
- More memory (`--memsize`, VM off) within the sizing rule above, and `--cpus` up to the number of performance cores (VM off).
- Be honest about limits. A Windows ARM VM runs most DirectX 11 games. Games that need DirectX 12 features Parallels doesn't support, or kernel-level anti-cheat, often won't run at all. Say that before the user spends time on it.

**Battery mode:** `--longer-battery-life on --faster-vm off --resource-quota low`, and `--pause on` so an idle VM pauses.

**Development:** `--nested-virt on` for WSL2, Docker or Hyper-V inside Windows. Use shared folders for the projects (`prlctl set "<VM>" --shf-host-add <name> --path <mac path>`), and add more CPUs.

**Accessibility (screen reader users)**
- `--keyboard-optimize accessibility`. This sends Mac key combinations through to the guest so screen reader commands reach NVDA or JAWS instead of being taken by macOS.
- On a Mac keyboard there's no Insert key, so set NVDA to use Caps Lock as its modifier key. Do this in NVDA's Keyboard settings, or offer to set it.
- To install NVDA from the Mac: `prlctl exec "<VM>" --current-user winget install -e --id NVAccess.NVDA --accept-source-agreements --accept-package-agreements`. Ask first, because that accepts the winget agreements on the user's behalf.
- The VM's sound must work for the screen reader to speak, so check the audio section below before anything else.
- Startup: `--autostart user-login` with `--startup-view window` or `fullscreen`, so the VM is ready when the user signs in.

## Troubleshoot

### No sound, or the screen reader goes silent

This is the most common problem and the most urgent one, because a blind user can't use a VM that has no speech. Work through it in this order.

1. **Where is the sound going?** `prlctl list -i "<VM>" | grep sound0`. The saved setting should be `output='Default'` so the VM follows the Mac's current output. Check the saved value in `config.pvs`, under the `<Sound>` section's `<Output>`. While the VM runs, `prlctl list -i` shows the device "Default" currently points to, so a device name there doesn't mean the setting was changed. If it's pinned to one device, run `prlctl set "<VM>" --device-set sound0 --output Default`.
2. **Read the log.** `grep PrlAudioCore ~/Parallels/<VM>.pvm/parallels.log | tail`. If you see `Failed setting up the frame buffer size with adjusted value (192, default value is 256)` together with `Can't attach pipeline for output device!`, it's the known Parallels 27 bug on macOS 27. Sound fails on Bluetooth headphones and multi-output devices, and the built-in speakers keep working. Parallels has an open ticket (forum thread "MacOS 27 update: no sound from Windows VM"). Muting the VM's microphone does not fix it, so don't spend time there. The numbers in that message tell you which mode the headphones are in. `(192, default value is 256)` or another value under 256 means music mode. `(352, default value is 320)` or another value over 320 means headset mode: an app on the Mac has the headphones' microphone open (a call in Discord, Zoom or Teams, or dictation), which drops the headphones to 16 kHz. Check with CoreAudio: the default output's `kAudioDevicePropertyNominalSampleRate` reads 16000, and `kAudioProcessPropertyIsRunningInput` shows which app holds the microphone.
3. **Get speech back right away.** Point the VM at the built-in speakers: `prlctl set "<VM>" --device-set sound0 --output "MacBook Air Speakers"`. Use the exact name from `prlsrvctl info`. Then rebuild the audio pipeline without restarting Windows: `prlctl set "<VM>" --device-disconnect sound0`, then `--device-connect sound0`. Tell the user the screen reader should now speak through the speakers.
4. **The fix for the Parallels 27 Bluetooth bug.** The Windows playback format has to suit the mode the headphones are in, and no single format suits both. Parallels asks for a buffer of the Windows rate times 0.004 frames. Music mode (Mac output at 44100 Hz) needs 256 or more, so 88200 Hz and up works and 48000 Hz fails. Headset mode (Mac output at 16000 Hz) needs 320 or less, so 48000 Hz and down works and 88200 Hz fails. Rates in between, such as 72000 Hz, are refused by the Windows driver. The built-in speakers accept any rate. So set 16-bit 88200 Hz for music mode and 16-bit 48000 Hz for headset mode; `scripts/set-format.ps1` in this skill does it with `-Rate`. You can't write that registry value directly: Windows denies it even to SYSTEM. Instead, use the same audio policy interface the Sound control panel uses, `IPolicyConfig::SetDeviceFormat` (CLSID `870af99c-171d-4f9e-af0d-e63df40c2bc9`, IID `f8679f50-850a-41cf-9c72-430f290290c8`). Call it from PowerShell with `Add-Type`, run as the signed-in user with `prlctl exec "<VM>" --current-user powershell -NoProfile -EncodedCommand <base64 UTF-16LE>`. The format is WAVE_FORMAT_EXTENSIBLE: 2 channels, 88200 Hz, 16 bits, block align 4, channel mask 3, PCM subformat. The device ID is `{0.0.0.00000000}.<render endpoint GUID>`, and the GUIDs are listed under `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render`, with DeviceState 1 meaning active. Back up the endpoint key first with `reg export`. Then switch the VM back to `--output Default`, reconnect sound0, and confirm with the user that speech works in their headphones.
5. **Make it stick.** Parallels Tools updates and driver reinstalls can reset the format, which is why the problem comes back every few weeks. Offer to install a Windows scheduled task that re-applies the format at every sign-in. Put the script in `C:\ProgramData\<name>\`, have it log its result, register the task with `Register-ScheduledTask` and an `-AtLogOn` trigger for the user, and run it once to check it works. That task alone is not enough for anyone who uses the headphones' microphone, because every call or dictation flips the headphones into headset mode and the screen reader goes silent. For them, offer the Mac helper in this skill, `scripts/vm-audio-guard.swift`. It watches the Mac's output rate and the VM log, sets the matching format inside Windows through `scripts/set-format.ps1`, and reconnects sound0. Speech drops for about five seconds at each mode switch and then returns by itself. To install it: copy `set-format.ps1` to `C:\ProgramData\VMAudioFix\` in the guest (send it as base64 in pieces of about 1,000 characters, then decode), build the helper with `swiftc -O` into a normal folder such as `~/Developer/vm-audio-guard`, run it once with `"<VM>" --once` to prove it works, then ask before adding a LaunchAgent in `~/Library/LaunchAgents` with the VM name as its argument, `RunAtLoad` and `KeepAlive`. A login item needs the user's yes and may need manual mode. Tell the user where its log is (`~/Library/Logs/vm-audio-guard.log`) and how to remove it. Don't fix this by moving the Mac's microphone to the built-in one unless the user asks for that; they chose the headset microphone on purpose. Testing formats drops the screen reader's speech each time, so warn first and keep it short.
6. **Check it worked.** Have Windows play a sound, then use CoreAudio (a small Swift program reading `kAudioHardwarePropertyProcessObjectList` and `kAudioProcessPropertyIsRunningOutput`) to confirm that `prl_vm_app` is now sending output. Also confirm no new `failed starting of output audio device` lines appear in the log after the change.

Other audio notes:
- A multi-output or aggregate device (such as a "VM Audio Helper" someone made in Audio MIDI Setup) plays on every device inside it at once, and the Parallels 27 bug affects it too. Don't build one as the fix.
- Parallels 26 removed Bluetooth sharing with the guest. Bluetooth headphones should be connected to the Mac, and the VM uses them through the Mac's sound.

### Running commands inside the guest

- `prlctl exec "<VM>" <command>` runs as SYSTEM in a background session. Add `--current-user` for anything that touches the user's desktop, audio or settings.
- Windows limits how long a command line can be, about 8,000 characters, so long PowerShell scripts fail with "Unable to open new session". Send a long script in pieces of about 3,000 characters, each appended to a file with `cmd /c "<nul set /p =CHUNK>>C:\Users\Public\x.b64"`, then decode and run it. `set /p` always returns an error code even when it works, so check the file rather than the exit code. Delete the temporary files afterwards.
- "Unable to open new session" with a short command means Windows is still starting, locked, or Tools isn't running. Wait 15 seconds and try `cmd /c echo ok` before anything else.

### Slow VM or slow Mac

- Compare the VM's memory with the Mac's RAM and memory pressure. A VM with too much memory starves macOS, and one with too little swaps inside Windows.
- Check free disk space. A nearly full Mac disk slows the VM and macOS alike. Suggest the mac-storage-cleanup skill if it's under about 15%.
- `--resource-quota`, `--faster-vm`, `--adaptive-hypervisor on`, `--auto-compress on` for the disk, and fewer startup apps inside Windows.

### Tools and other problems

- Tools out of date: `prlctl installtools "<VM>"`, then restart the guest, after asking.
- A missing ISO or disk image still attached: clear it with `--device-set cdrom0 --image ""`.
- Snapshots taking space: `prlctl snapshot-list "<VM>"`. Deleting one needs the user's yes and manual mode.
- Anything else: search the log, then the Parallels Knowledge Base and forum for the exact error text, and check whether it's a known bug before inventing a fix.

## The report

End with:
- what was wrong, in plain words
- what you changed, with the exact setting names so it can be undone
- how you checked that it works
- what keeps it from coming back (a scheduled task, a setting, a habit)
- anything still open, such as a Parallels bug that only an update will truly fix
