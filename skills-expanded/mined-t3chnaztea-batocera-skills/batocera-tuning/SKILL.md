---
name: batocera-tuning
description: >-
  Use when a Batocera cabinet feels slow, laggy, or stuttery, or when tuning
  performance: EmulationStation menu/carousel lag, a slow-since-boot frontend,
  CPU governor stuck in powersave, overclock or CPU-speed core options that seem
  to do nothing, run-ahead / input latency, joystick polling rate
  (usbhid.jspoll, 1000 Hz) on arcade encoders, framerate that drops the longer
  the machine runs, or a 3D-heavy game (PSX/PS2/Dreamcast/N64 class) that
  crashes or stutters — Vulkan errors in emulator logs, picking a rendering
  resolution or graphics backend the hardware can afford. Covers the diagnostic
  order (check the throttle first), the v43 governor-at-boot failure, the
  emulator-name vs rom-dir-name overclock scoping trap, ES event-hook frame
  cost, and hardware-tier detection (batocera-info / batocera-vulkan). Not for
  shader visual quality (batocera-display).
compatibility: Requires SSH access to a Batocera host (tested on v41-v44).
---

# Batocera Tuning

Performance: why the frontend or a game runs slow, and how to fix it. Assumes
the connection pattern and `batocera.conf` model from `batocera-ops`. The theme
throughout: **diagnose the machine state before blaming config, themes, or
gamelists.** Most "it got slow" reports are a throttle or a leak, not the thing
the user suspects.

## Diagnostic order for "the frontend is slow"

Work down this list; each step is one command and rules out a whole class:

1. **CPU governor.** A frontend that is laggy *from cold boot* and stays laggy
   through a reboot is almost always the CPU stuck in `powersave`:
   ```bash
   SSHB "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
   ```
   If it says `powersave` despite `system.cpu.governor=performance`, see the
   governor fix below. This is step 1 because it's the most common cause and the
   cheapest check.
2. **ES event hooks.** Lag that gets *progressively worse* as you navigate, and
   is cured only by an ES restart, points at a slow/leaky ES event hook. ES runs
   every executable in its scripts dirs on menu events — a `system-selected` hook
   fires on **every carousel tile change** and can add permanent per-frame cost.
   Audit `/userdata/system/scripts/` and
   `/userdata/system/configs/emulationstation/scripts/`. Because hooks are global
   (not theme-scoped), this masquerades as a "theme-independent ES bug" — the
   tell is that it accumulates per tile visited. See below.
3. **Texture cache.** Lag that's fine at first and worsens with a large media set,
   with revisits staying fast, can be ES texture-cache eviction thrash. Raising
   `MaxVRAM` in `es_settings.cfg` (e.g. to 1024) can help, but measure — on some
   builds the GPU floor and MaxVRAM make no difference and the real cause is
   #1 or #2.
4. **GPU clock floor.** Only chase this after 1–3. On a vsync-paced frontend the
   GPU often won't upclock on its own, but pinning a higher floor frequently
   makes *no measurable difference* — A/B it before persisting anything.

Measure, don't assume: a framerate overlay (`DrawFramerate=true` in
`es_settings.cfg`) plus the `batocera-ops` screenshot loop lets you read fps on
a specific tile remotely. Turn it back off when done.

### Reading an idle machine

Load average is a poor idle signal on these boxes. It counts threads in
uninterruptible sleep, and a display driver worker that waits for a page flip
(for example with the TV off) holds it near 1.0 while the CPU does nothing.
Measure the real state:

```bash
SSHB 'head -1 /proc/stat; sleep 10; head -1 /proc/stat'          # idle column vs total
SSHB 'ps -eo stat,args | awk "\$1 ~ /^D/"'                       # who is in D state
SSHB 'f=/sys/class/powercap/intel-rapl:0/energy_uj; a=$(cat $f); sleep 10; echo $(( ($(cat $f)-a)/10000 )) mW'
SSHB 'cat /sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count'
```

A package that draws a few watts and still reads hot has a heat-path problem
(dust, old paste, a closed cabinet), not a software one. The throttle count is
the number that matters: zero growth during normal play means the cooling is
enough. Many mini PCs expose no fan sensor and no fan control to Linux (look
for `pwm*` and `fan*` files under `/sys/class/hwmon/`); the firmware owns the
fan curve and only the firmware setup screen changes it.

**Do not** drive these tests with synthetic input (see `batocera-ops` doctrine).
Ask the human to navigate, and read results from logs / screenshots / `/proc`.
Also note: a governor re-assert (below) may fire ~60–90s after boot, so the first
minute can feel slow even when fixed — don't let anyone judge inside that window.

## The v43 governor-at-boot failure

On some v43 builds, `system.cpu.governor=performance` **fails to apply at every
boot**: the init script (`/etc/init.d/S18governor`) runs but its sysfs write
silently fails (redirected to `/dev/null`), leaving intel_pstate's default
`powersave` (~1.5 GHz vs the chip's ~3.4 GHz). A reboot does not fix it — every
boot lands in powersave.

Fix: re-assert the governor from a boot service after userspace is up, and
periodically thereafter. In `/userdata/system/services/custom_service` (the v43
replacement for `custom.sh`; see `batocera-maintenance`), add a loop that runs
`/etc/init.d/S18governor start` ~60s after boot and then hourly. Verify across a
reboot:

```bash
SSHB "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"   # after ~90s uptime
```

Bonus hazard covered by the same hourly re-assert: `batocera-shutdown`'s
fake-suspend can save the governor state such that a repeated fake-suspend strands
the machine in powersave permanently. The periodic re-assert covers that too.

## The overclock / CPU-speed scoping trap

Overclock and CPU-speed core options are keyed on the **emulator/core context**,
which is **not always the rom directory** you think you're affecting. Example: a
`fbneo.fbneo-cpu-speed-adjust=200%` key applies to launches in the **fbneo** core
context — it does **not** reach games launched out of a different rom directory
(e.g. `neogeo`) even though they run on the same underlying core. If Neo Geo games
still run at 100% after you "set the fbneo overclock," that's why: they need a
`neogeo.<key>` of their own.

To find the right scope, launch the game and read
`/userdata/system/logs/es_launch_stdout.log` for the system/emulator/core it
actually used, then key the override on that name. And remember the **`.opt`
exception** (`batocera-ops` → batocera-conf): a per-game `.opt` *replaces* global
core options, so a game with an `.opt` takes its CPU value from inside the `.opt`,
not from `batocera.conf` — set it there for that game.

## ES event-hook frame cost

Expanding on step 2: an installed ES event hook (say, a home-automation
integration that pings a server on `system-selected`) executes on every carousel
move. Even a fast-looking script can leave a couple of milliseconds of permanent
per-frame cost that accumulates per tile visited until ES is restarted, dragging
a 60 fps menu down to single digits after a while. Diagnosing it:

- Symptom shape: per-*visit* accumulation (revisiting two tiles 50 times degrades
  as much as visiting 50 different tiles), cured only by ES restart.
- Confirm with ES debug logging (`es.customsargs=--debug` in `batocera.conf`,
  picked up on a plain `kill -9` restart of ES, no reboot needed): you'll see the
  hook `fireEvent → executing:` line on every tile change.
- Fix: remove the hook. If you want the integration, **poll from the other side**
  instead of installing an ES event hook. Trap: some agents/services *rewrite*
  their hooks on every boot/start — remove the service/agent that installs them,
  not just the hook files, or they reappear next boot.

## Tuning 3D-heavy games (PSX, PS2, Dreamcast, N64 class)

Graphics tuning only pays off on 3D systems whose emulators expose rendering
levers. 8/16-bit libretro systems render native-res for pennies — they have no
resolution or backend knobs worth touching, and "tuning" them means frameskip
or the overclock keys above. Don't burn a session tuning a 2D system.

**Know the hardware before proposing values.** One command each:

```bash
SSHB "batocera-info"        # CPU model/cores, RAM, display resolution
SSHB "batocera-vulkan hasVulkan; batocera-vulkan hasDiscrete; batocera-vulkan listDevices"
```

An iGPU-only box (`hasDiscrete` false) and a discrete-GPU box want different
defaults; find out which you're on before copying settings from a forum post.

**The two levers, in order:**

1. **Internal resolution scale** — the dominant cost knob on 3D emulators
   (`duckstation_resolution_scale`, `pcsx2_resolution`,
   `flycast_render_resolution`, …). Each step multiplies fill-rate cost; on an
   iGPU, 1x-2x native is realistic and forum-copied 4x+ is not.
2. **Graphics backend** — Vulkan vs OpenGL. On Intel iGPUs Vulkan is a common
   *stability* problem, not just a performance choice (see the table below).

Discover the exact key names and accepted values per emulator in
`es_features.cfg` (`batocera-ops` → batocera-conf reference) rather than
guessing — values can be opaque enums (PCSX2 OpenGL is
`ps2.pcsx2_gfxbackend=12`).

**Crash and slowdown patterns** in the emulator logs under
`/userdata/system/logs/` (read `es_launch_stdout.log` first to see which
emulator/core actually ran):

| Log pattern | Likely cause | First fix |
|---|---|---|
| `VK_ERROR_*`, `vkQueueSubmit` failure, device lost | Vulkan instability, esp. on Intel iGPUs | Switch that emulator's backend to OpenGL |
| `std::bad_alloc`, OOM-killer hit in `dmesg` | Resolution scale / texture cost beyond memory | Drop resolution scale one step |
| Slowdown or audio crackle, no crash | GPU fill-rate saturated | Drop resolution scale before reaching for frameskip |

Scope fixes per game where one heavy title is the problem
(`psx["Game (USA).chd"].duckstation_gfxbackend=…`) rather than degrading the
whole system for it.

## Run-ahead and input latency

Run-ahead hides emulation input latency by simulating N frames ahead each frame —
great feel, but it multiplies CPU cost (each run-ahead frame is a full re-emulate)
and needs a core that supports save-states. Enable modestly
(`<system>.retroarch.run_ahead_frames=1`) on systems where the CPU has headroom;
back off if it introduces audio crackle or drops frames. On a weak cabinet iGPU,
prefer 1 frame and reserve it for the systems where latency matters most (fighters,
shmups) rather than globally.

### Joystick polling: measure before you tune

"Set `usbhid.jspoll=1` for 1000 Hz" is common advice for arcade encoders. On
many cabinets it changes nothing. Measure first; it takes ten seconds and no
input.

**Read the real rate.** Most cheap encoders (the DragonRise "zero delay" board,
USB id `0079:0006`, is the usual one) answer every poll with a report, even
with hands off the controls. Count the reports on `hidraw`:

```bash
SSHB 'python3 - <<EOF
import os, time, select, collections, glob
for dev in sorted(glob.glob("/dev/hidraw*")):
    fd = os.open(dev, os.O_RDONLY | os.O_NONBLOCK); ts = []
    end = time.monotonic() + 3.0
    while time.monotonic() < end:
        if select.select([fd], [], [], 0.2)[0]:
            try: os.read(fd, 64); ts.append(time.monotonic())
            except BlockingIOError: pass
    os.close(fd)
    if len(ts) < 3: print(dev, "no reports while idle"); continue
    gaps = collections.Counter(round((b - a) * 1000) for a, b in zip(ts, ts[1:]))
    print(dev, "%.1f Hz" % ((len(ts) - 1) / (ts[-1] - ts[0])), "gap ms:", sorted(gaps.items()))
EOF'
```

This is a passive read: it changes nothing and sends nothing. A gap of 8 ms is
125 Hz, 1 ms is 1000 Hz. Do not trust the `interval` file in sysfs or `Ivl=`
in the USB device list: both show what the device asks for, not what the host
does. A device that reports only on change prints "no reports while idle"; for
that one, read event timestamps while a person moves the stick.

**Why the setting often does nothing.** `jspoll` changes the interval that the
`usbhid` driver requests. An xHCI (USB 3) host controller ignores that request
and takes the interval from the device's own endpoint descriptor. A low-speed
encoder that asks for 10 ms gets 8 ms there, with or without `jspoll`. The
setting only works on host controllers that honour the request (EHCI ports,
some single-board computers), which is why reports of success are real and
still do not transfer to your box. Check both facts before you spend time:

```bash
SSHB 'for d in /sys/bus/usb/devices/*/idVendor; do p=${d%/idVendor}; echo "$(cat $p/idVendor):$(cat $p/idProduct) speed=$(cat $p/speed) $(basename $p)"; done'
SSHB 'dmesg | grep -iE "new (low|full)-speed USB device.*using"'    # xhci_hcd or ehci-pci
SSHB 'cat /sys/module/usbhid/parameters/jspoll'                      # 0 = not set
```

`speed=1.5` is a low-speed device. If the encoders sit on `xhci_hcd`, expect no
change. A two-minute test without a reboot settles it: write `1` to the
`jspoll` parameter file, unbind and bind the encoder's interface under
`/sys/bus/usb/drivers/usbhid/`, and run the measurement again. Do it at the
menu, not in a game, because the joystick nodes go away for a second. Write
`0` and rebind to undo it. Make the kernel command line change only after that
test shows 1 ms gaps: the boot file edit is lost at every upgrade, and a bad
line there can stop the boot.

**How much it is worth when it works.** Published measurements of this encoder
class put the gain from 1000 Hz polling at about 3 to 4 ms on average, with
the spread unchanged, because the board's own scan and debounce loop is the
larger delay. One frame at 60 Hz is 16.7 ms. A real improvement at the
encoder needs a board that requests 1 ms in its own descriptor, which xHCI
does honour.

**Spend the effort here first, in this order:**

1. **The TV's game mode.** Measured differences between game mode on and off
   run from about 20 ms to over 100 ms on the same set. It is usually stored
   per input, so set it while the cabinet's input is on screen. Most TVs do
   not report picture settings over their network API, so a person has to look
   at the menu once.
2. **Run-ahead** (above): one frame is 16.7 ms on the systems that can afford
   it. Check what is already set before you add keys:
   `SSHB "grep -E 'runahead|run_ahead' /userdata/system/batocera.conf"`.
3. Polling rate, if the measurement says the host honours it.
