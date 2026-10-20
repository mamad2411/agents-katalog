# CLAUDE.md

Guidance for Claude Code (and any other agent) working in this repository.

## What this repo is

Documentation, configuration, and knowledge capture for one ClockworkPi uConsole build
(CM4 Lite 8GB + HackerGadgets NVMe/adapter kit + OpenSourceSDRLab AIO V2), plus an RF
knowledge base that the finished device feeds.

It is mostly **not** a software project: most changes are prose, tables, checklists, and config
files that get applied to a device by hand, and "correct" mostly means accurate, sourced, and
reproducible — not compiling. The one exception is [`webdash/`](webdash/) (started 2026-09-21), a
small locally-authored Docker app — see [`docs/reference/webdash-architecture.md`](docs/reference/webdash-architecture.md)
for why it exists and [`software/webdash.md`](software/webdash.md) for running it. It has its own
build/verify loop; the rest of this file's conventions (verify markers, no secrets, living
documents) still apply to it.

## Build state (keep current)

As of 2026-09-14 the CM4 was delivered and inspected (variant confirmed CM4108000, photographs in
`images/inventory/`). The AliExpress order shipped as **two separate parcels**: the AIO V2 arrived
first (not yet unboxed/inspected) while the uConsole v3.14 mainboard was still in transit. The
microSD was flashed 2026-09-15 with `uConsole_CM4_v3.1_64bit` (read-back verified) but not yet
booted, pending the mainboard.

As of 2026-09-15 the mainboard and AIO V2 kit fully arrived, and **the device was unboxed,
mechanically assembled, and closed**: mainboard in the shell, CM4 on the kit's adapter, AIO V2 in
the expansion slot, stock battery board with an interim 2×18650 pack, display and keyboard
installed, and all 8 antennas fitted (`ANT1`–`ANT7` strip plus the SDR bulkhead).

**The device was then powered on and booted, 2026-09-16** — this is no longer a pre-power-up repo. Confirmed
on real hardware: CM4 serial/MACs, the mainboard's USB input-controller identity, PMIC voltage (1S,
3.886 V — this reading is from the interim 18650 pair, not the Meshnology LiPo, since the stock
battery board is what's installed), and the external-antenna `dtparam=ant2` setting (see
`docs/logs/build-log.md`, 2026-09-16 "First boot" entry). Software bring-up followed. No per-board
damage inspection has been done. Anything asserting device behavior beyond what has actually been
run is still sourced from vendor docs, upstream source, or forum reports and must carry a verify
marker; anything read off a photograph is a photo reading, not a measurement, and carries one too.
Photographs: `images/inventory/`.

**The HackerGadgets upgrade kit #11953 arrived 2026-09-23** — CM4/5 Adapter Pro, NVMe battery board
and RJ45+USB3 board — so the NVMe board and `JP1` are no longer absent. The **WD PC SN730 256 GB
(M.2 2280, OPAL)** was selected from the on-hand drives and fitted, and the owner reports the
boards were installed and tested. Command output for that was captured on the device later the
same day; see the next paragraph.
The other HackerGadgets order, **#12253 (AC1200 Wi-Fi card)**, **arrived and was installed
2026-09-30** and is verified on Fancy: MediaTek MT7921AUN, `wlan1` (`mt7921u`) with monitor mode on
2.4/5/6 GHz, Bluetooth on `hci1` (USB). See [`hardware/specs/ac1200-mt7921.md`](hardware/specs/ac1200-mt7921.md).

**2026-09-23: root runs from NVMe, verified on the device.** Root is `/dev/nvme0n1p2` (WD PC
SN730, reused, 21% wear, SMART `PASSED`, not OPAL-locked). EEPROM is `2026/05/17` with `BOOT_ORDER=0xf416`.
The microSD was removed 2026-09-23 and NVMe-only boot passed; the card is kept as a fallback. The earlier paragraph's "boots from microSD" and
"stock battery board" statements are superseded. On that date the interim 18650 pair was in the NVMe board's holder,
with **`JP1` open** and the reverse-polarity LED **not lit** (owner); superseded 2026-10-11, see below. Onboard
Ethernet **links at 1 Gbps** (checklist 2.2 passes), and the pack **charges** (the PMIC reported
~2 A, but see the charge-ADC caveat below — charge `current_now` over-reads, so that is an upper
bound). Test results are in `docs/logs/build-log.md` (2026-09-23 entries).

**GNSS 3D fix confirmed on hardware** (first obtained 2026-09-23; recorded in detail 2026-10-04).
gpsd 3.25 over `/dev/serial0` (NMEA 0183, 9600 bps); a 2026-10-04 fix used **15 satellites** (10
GPS + 5 GLONASS) at **HDOP 0.7**, antenna reports `ANTENNA OK`. Location is held to Maidenhead grid
(EM94) — raw NMEA with coordinates is kept off-repo. Checklist 3.3 passes. **Time to first fix is
not yet measured** (the capture opened already fixed); a cold-reset timed run is tracked in
[`TODO.md`](TODO.md). See [`knowledge/rf-fundamentals/findings/2026-10-04-first-fix.md`](knowledge/rf-fundamentals/findings/2026-10-04-first-fix.md)
and `software/gps.md`.

**2026-10-11: on the Meshnology LiPo.** The owner removed the 18650s and the NVMe board's holder,
bridged `JP1` closed (location: right of the JST connector and `R14`, top edge of the `BAT2`
outline; photos in `images/assembly/`), and connected the Meshnology pair (both packs on a Y harness,
≈74 Wh nominal). The PMIC read it **charging at ≈1.65 A, 3.97 V, 41 %** at 22:50Z (charge current an
upper bound — see the charge-ADC caveat below), and the pouches stayed cool. The board is now
LiPo-only. Don't refit 18650s with `JP1` closed.

Open blockers:
- **The bare holder pads on the NVMe board need insulating before the shell is closed.** Photos
  show four tinned contact remnants at the old `BAT1`/`BAT2` positions, standing proud of the board.
  The AC1200's coax runs across the right-hand pair, which sit on the `+` side and are likely live
  at pack voltage (*unverified*). A pouch pressed onto them could be punctured. Trim them flat and
  cover them with Kapton tape. See the build log, 2026-10-11.
- **The owner's DM-20 meter is not trusted.** It read the fitted pack at 4.8 V while the PMIC read
  3.97 V on charge, and 18650s at 4.3 V against ≈4.2 V. The earlier "4.48 V" on the Meshnology
  packs is treated as this meter's error. Confirm with a fresh meter battery or a second meter
  ([`docs/logs/known-issues.md`](docs/logs/known-issues.md)).
- **The power cuts out with no warning at ≈3.5 V under load.** The first discharge of the fitted
  pair (2026-10-12/13) delivered **52.2 Wh in 13.7 h** (3.8 W average; 3.37 W idle with the screen
  off, plus unexplained +2 W episodes). It then lost power at ≥3.53 V with no knee in the curve, so charge was
  probably left in the pack. The 18650s cut at 3.49 V too, so the cause is likely on the system
  side and is *unverified*. The fuel gauge % is wrong on this pack (the device tree describes
  6.7 Ah), so watch `voltage_now`: plug in by 3.60 V, shut down by 3.55 V. A guard at 3.45 V never
  fires. The 2026-10-13 recharge did not address the cut (still open), but it did surface a related
  caveat: **charge `current_now` over-reads (≥~1.4×)**, so all "charging at … A" figures are upper
  bounds and the 52 Wh discharge figure carries residual uncertainty until the charge ADC is settled.
  See [`docs/reference/power-budget.md`](docs/reference/power-budget.md) and
  [`docs/logs/known-issues.md`](docs/logs/known-issues.md).
- ~~**No RTC backup cell is fitted**~~ — **resolved 2026-10-10.** The owner fitted and tested the
  cell, and checklist 3.1 passes; the next boot set the clock from the RTC with no power-loss flag.
- ~~**Four antennas have no radio behind them**~~ — **resolved 2026-09-30.** `ANT2`/`ANT3`/`ANT5`/`ANT6`
  are fed by the AC1200, which arrived, was installed, and is fully verified: `wlan1` monitor mode on
  2.4/5/6 GHz, and `hci1` passive-BLE behaviour (no `bluetoothd` auto-scan/connect, passive scan
  allowed). All AC1200 checks closed — see [`hardware/specs/ac1200-mt7921.md`](hardware/specs/ac1200-mt7921.md).

## Where things belong

| If it is… | It goes in |
|---|---|
| A hardware fact about a board (chipset, pinout, dimensions, rating) | `hardware/specs/`, or `docs/reference/pinout-gpio.md` for GPIO |
| A link to an upstream datasheet or schematic | `hardware/datasheets/README.md` |
| A repeatable procedure someone follows step by step | `docs/runbooks/` |
| A pass/fail list run once at a milestone | `docs/checklists/` |
| Setup notes for one application | `software/<app>.md` |
| A file that gets copied onto the device | `configs/<subsystem>/` |
| A 3D-printable part (`.3mf`/`.stl`) | `hardware/stl/`, listed in its README |
| A purchase, order, invoice, or warranty fact | `docs/records/` |
| Something learned about RF, independent of this device | `knowledge/<discipline>/learned/` |
| An observation, capture, or signal ID | `knowledge/<discipline>/findings/` |
| A dated account of what was done | `docs/logs/build-log.md` |
| Learning-platform curriculum (tracks, modules, lessons, labs, quizzes, glossary) | `webdash/curriculum/`; durable concept prose stays in `knowledge/*/learned/` and is pulled in with `@ref` |
| Locally-authored software (not a vendor app) | `<name>/` at repo root for the code; design/rationale in `docs/reference/<name>-architecture.md`; setup/ops notes in `software/<name>.md` |

Cross-link with **relative** links. Every new document should be reachable from
[`README.md`](README.md) or [`docs/documentation-index.md`](docs/documentation-index.md).

## Conventions

- **Verify markers.** Anything not yet confirmed on this hardware says so, in the sentence that
  makes the claim — "*unverified*", "verify before running", or a named command that settles it.
  Do not quietly promote a vendor claim to fact.
- **Estimates are labelled.** Numbers derived from component typicals (see
  [`docs/reference/power-budget.md`](docs/reference/power-budget.md)) are marked as estimates and
  name the command whose output replaces them.
- **UTC timestamps.** Location is recorded as city or Maidenhead grid only — never precise
  coordinates.
- **No secrets.** No keys, PSKs, passwords, tokens, captured credentials, or precise private
  locations. Meshtastic channel PSKs are generated on-device and never committed.
- **Binaries stay out.** `.gitignore` excludes images (`*.img`, `*.7z`, `*.zip`), raw IQ
  (`*.iq`, `*.cf32`, `*.cs8`, `*.cu8`, `*.sigmf-data`), Kismet logs, and lab outputs (`*.wav`,
  `*.csv`, `*.raw`). Reference them by location and checksum.
- **Licence.** Docs and media are CC BY 4.0, code and configs MIT, per [`LICENSE`](LICENSE). Keep
  third-party files (e.g. the Kismet-derived udev rules) listed in its exclusions, and link rather
  than copy external text.
- **Commands are runnable.** Prefer a shell block a person can paste over a description of what
  they should do. State the expected output when it is the point of the step.
- **Tables over paragraphs** for anything enumerable; checkbox lists for anything performed once.
- Markdown only, no HTML. Keep the existing heading style and roughly 100-column prose.

## Living documents — update these as a side effect of work

| File | Update when |
|---|---|
| [`docs/logs/build-log.md`](docs/logs/build-log.md) | Any hands-on session |
| [`docs/logs/known-issues.md`](docs/logs/known-issues.md) | A symptom is hit or resolved |
| [`docs/logs/decisions.md`](docs/logs/decisions.md) | A choice is made or an open question closes |
| [`docs/logs/firmware-versions.md`](docs/logs/firmware-versions.md) | Anything is flashed |
| [`docs/records/order-and-warranty.md`](docs/records/order-and-warranty.md) | Shipping/serial/RMA state changes |
| [`CHANGELOG.md`](CHANGELOG.md) | A batch of documentation lands |
| [`TODO.md`](TODO.md) | Work is finished or a new blocker appears |

## Knowledge base rules

`knowledge/` is organized by discipline (`learned/`, `configs/`, `runbooks/`, `findings/`).
Copy a template from [`knowledge/_templates/`](knowledge/_templates/) rather than starting blank.
`learned/` holds durable understanding, `findings/` holds dated observations — do not mix them.

Legal posture, restated because it constrains content: this platform is for **receiving,
learning, and licensed transmitting**. Wardriving here means passive observation only — no
deauth, no handshake capture, no association, no cracking against any network without either
**owning it or holding written authorization to test it**. That carve-out is explicit, not
implied: two active-auditing tools are installed behind it, each gated to **own gear, a documented
engagement, or a CTF whose rules permit it — nothing else**: `aircrack-ng` (2026-09-21, authorized
WPA/WPA2 auditing, see [`software/aircrack-ng.md`](software/aircrack-ng.md)) and `netexec`
(2026-10-13, authorized AD/network-service auditing — SMB/LDAP/WinRM/etc., see
[`software/netexec.md`](software/netexec.md)). Do not add material that assists intrusion against
networks outside that boundary, decoding of protected or encrypted communications, or unlicensed
transmission. See the responsible-use section in [`knowledge/README.md`](knowledge/README.md).

## Repository skills and agents

[`.claude/skills/hardware-project-repo/`](.claude/skills/hardware-project-repo/SKILL.md) generalizes
this repo's method — structure, sourcing rules, conflict map, staged configs, bring-up acceptance
checklists — for scaffolding and driving other hardware builds. It loads automatically in sessions
working here; see [`.claude/skills/README.md`](.claude/skills/README.md) to use it elsewhere.

Four working-method skills sit beside it (added 2026-10-11, adapted from
[mattpocock/skills](https://github.com/mattpocock/skills); provenance and local changes in the
[skills README](.claude/skills/README.md)): `diagnosing-bugs` (a red-capable feedback loop before
any hypothesis; device loops read-only and never transmitting), `tdd` (webdash's `unittest`
suites), `grilling` (stress-test a plan; settled decisions go to `decisions.md`) and
`writing-for-agents` (for this file, the agents and the skills).

Two read-only subagents support it: [`hw-research`](.claude/agents/hw-research.md) for per-component
sourcing (spawn one per component, in parallel) and [`repo-audit`](.claude/agents/repo-audit.md) for
an adversarial pass before committing a documentation batch. They report; this session commits.

[`doc-review`](.claude/agents/doc-review.md) (added 2026-09-23) checks that documented claims are
**still true**. It compares status claims ("pending", "not yet installed", "in transit", "still
inserted") against the newest dated evidence and the live device, using read-only commands. Every
line listed by [`.claude/scripts/doc-review-candidates.py`](.claude/scripts/doc-review-candidates.py)
gets a verdict. It runs **every 8 h of active working time**. A project hook
([`.claude/hooks/doc-review-timer.py`](.claude/hooks/doc-review-timer.py), wired in
[`.claude/settings.json`](.claude/settings.json) on `UserPromptSubmit` and `Stop`) counts the gaps
between events, ignoring any gap over 30 min. At 8 h it injects a reminder on each prompt until a
review is recorded. After a review, run `.claude/hooks/doc-review-timer.py --reset`; use `--status`
to see the clock. The clock state is per machine and lives in
`~/.local/state/clockworkpi-uconsole/`. The first two runs showed the verdicts vary between runs,
so treat an "ok" as likely rather than proven.

Eight more agents cover webdash design and learning (six added 2026-09-23, `senior-rf-engineer`
2026-09-24, `webdash-qa` 2026-10-11). They work as one pipeline with a shared quality bar, defined
in [`docs/reference/webdash-design-team.md`](docs/reference/webdash-design-team.md): run them in
its stage order and pass each one the upstream reports it needs. All are read-only unless a prompt
asks otherwise:

| Agent | Role |
|---|---|
| [`design-planner`](.claude/agents/design-planner.md) | Graphic design planning: information architecture, layout, visual system, per-component patterns |
| [`creative-director`](.claude/agents/creative-director.md) | Concept, voice, naming, motifs; keeps the Fancy theme legible and within the legal posture |
| [`web-ui-engineer`](.claude/agents/web-ui-engineer.md) | Turns a design into a buildable vanilla-JS spec; reviews UI code for accessibility, performance, untrusted data |
| [`syllabus-designer`](.claude/agents/syllabus-designer.md) | Curriculum built on `knowledge/` with a hands-on lab on this device per module |
| [`tutor`](.claude/agents/tutor.md) | Explains concepts using this device's real state; writes in-dashboard explainer content |
| [`guided-learning`](.claude/agents/guided-learning.md) | Step-by-step missions whose steps are checked against live webdash data |
| [`senior-rf-engineer`](.claude/agents/senior-rf-engineer.md) | Technical review: RF physics and numbers, and that every exercise fits Fancy's actual hardware and the legal posture |
| [`webdash-qa`](.claude/agents/webdash-qa.md) | Rendered-page evidence: screenshots per viewport and skin, keyboard pass, measured contrast, motion and CM4 performance |

Before committing a batch, run the mechanical audit as well as the link check:

```bash
python3 .claude/skills/hardware-project-repo/scripts/audit.py .
```

## Checks before committing

```bash
# no broken relative links
python3 - <<'PY'
import os,re
bad=[]
for root,_,files in os.walk('.'):
    if '.git' in root: continue
    for f in files:
        if not f.endswith('.md'): continue
        p=os.path.join(root,f)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', open(p).read()):
            t=m.group(1).split('#')[0]
            if not t or t.startswith(('http','mailto:')): continue
            if not os.path.exists(os.path.normpath(os.path.join(root,t))): bad.append(f"{p} -> {t}")
print("broken:", len(bad)); [print(" ",b) for b in bad]
PY

git status --short          # nothing unexpected staged (no images, no captures)

# learning-platform curriculum lints (no-op output "ok" when nothing is wrong)
python3 webdash/host-helpers/learn-compile.py --check
```

## Git

- Work on a feature branch; do not commit to `main` directly.
- Commit messages: imperative subject, body explaining *why* the documentation changed and what
  is still unverified.
- Do not open pull requests unless asked.
