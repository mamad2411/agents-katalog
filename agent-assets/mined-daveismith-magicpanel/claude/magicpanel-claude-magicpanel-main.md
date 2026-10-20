# CLAUDE.md — Magic Panel firmware development with the simulation harness

Read this before touching anything. It tells you what the repo is for, what must never change,
how to check your work, and where the details live.

## What this repo is

Firmware for the IA-PARTS **Magic Panel** (ATmega328P @ 16 MHz, two daisy-chained MAX7221 LED
drivers driving an 8×8 LED grid, I2C slave at `0x14`), plus a **deterministic simavr-based
regression harness** that records exactly what the panel displays and when, in AVR cycles.
Baselines captured from the original firmware are the golden truth; every build of the sketch
under development is compared against them.

## The two sketches — this is the most important rule

| File | Role | May you edit it? |
|---|---|---|
| `MagicPanel_v010_5.ino` | **Frozen reference specimen.** SHA-256 must stay `f213fd7a68dd00307d1231cb648f2f7b223c4232dbc9780440ecc2253de6b638`. `MagicPanel_v010_5.ino.elf` is its shipped build. | **Never.** `make check-specimen` and `tests/test_specimen.py` fail if it changes. |
| `MagicPanel.ino` | **The sketch under development.** Started as a byte-identical copy of the specimen. `make firmware` builds it; all tests run it against the baselines. | Yes. This is the only firmware file you change. |

If you need to know what the *original* does, read the specimen or `docs/firmware-map.md`;
if you need to change behaviour, edit `MagicPanel.ino`.

## Toolchain (all pinned, all repo-local; see `tools/versions.env`)

arduino-cli 1.5.1, `arduino:avr` core 1.8.6 (avr-gcc 7.3.0), FQBN `arduino:avr:diecimila:cpu=atmega328`,
LedControl 1.0.6 (submodule `third_party/LedControl`), simavr `fe665cef` (submodule
`third_party/simavr`), Python 3.11+ venv with `requirements.txt` (PyYAML, mcp, Pillow, pytest).
Do not install anything else or change a pin without recording why in `docs/decisions.md`.

```sh
make setup          # once per checkout (network needed only here)
make firmware       # MagicPanel.ino -> build/firmware.elf  (two clean builds must be identical)
make reference      # specimen -> build/reference/, must reproduce the shipped ELF's flash image
make harness        # harness/mpsim
```

## The development loop

1. Edit `MagicPanel.ino`.
2. `make firmware` (build must be deterministic; `-Werror=date-time` forbids `__DATE__`/`__TIME__`).
3. Quick check: `make run SCENARIO=<name>` then `make compare SCENARIO=<name>`; read
   `runs/<name>/diff_report.md` and `runs/<name>/filmstrip.txt`, or `make gif SCENARIO=<name> RUN=1`.
4. Full check: `make test` (≈3–4 min; pytest). Narrow with `MP_SCENARIOS=a,b make test-fast` or
   `.venv/bin/python -m pytest tests/test_regression.py -k cross`.
5. If a scenario fails **and the change is intended**, re-baseline that one scenario only:
   `make rebaseline SCENARIO=<name> I_MEAN_IT=1`, then review and commit
   `tests/baselines/<name>/` including `rebaseline_diff.md`. Say in the commit message which
   pattern changed and why. Never re-baseline to make a red build green without that review.
6. New behaviour needs a new scenario: add `scenarios/<name>.yaml` (schema in
   `harness/README.md`), run it, check the filmstrip, `make baseline` (captures only scenarios
   without a baseline), commit both.

Scenario names encode what they exercise: `cmd_NN_*` = I2C command NN, `mode_N_*` = jumper/rotary
mode N, plus `power_on_default`, `i2c_garbage`, `i2c_mid_animation`, `i2c_back_to_back`,
`i2c_read_probe`, `mode_change_mid_run`, the trigger-semantics set `i2c_retrigger_same`,
`i2c_switch_no_resume`, `i2c_flood`, `gpio_*`, `i2c_over_gpio_resume`, `random_mode_i2c_resume`,
and `reg_*` for the I2C register interface. `list_scenarios` (MCP) or `ls scenarios/` shows them.

## What "matches the baseline" means

`display.jsonl` records every change of the rendered panel, including the ~0.5 ms intermediate
states while a `PrintGrid()` clocks 16 bursts into the MAX7221s. Comparison runs in **settled
mode by default**: only states that stay visible for ≥ 10 ms count (`MP_SETTLE_MS`), i.e. what
the panel shows after a whole frame has been clocked out. Content must match exactly, and the
settled states' timestamps must match within the scenario's `timing_tolerance_cycles`
(default 0; a tolerance needs a `timing_tolerance_reason`). Use `compare_mode: latch` in a
scenario, `--mode latch` on `tools/compare.py`, or `MP_COMPARE_MODE=latch` when the
intermediate latch sequence itself matters (e.g. you changed the bit-bang code).

Alert and FlashAll have identical content and differ only in timing, so timing is part of the
pass criterion. Random-dependent patterns are deterministic in simulation (fixed seed) but
sensitive to the *order* of `random()` calls; see `docs/decisions.md` D-1/D-16.

## Facts about the firmware you will trip over (details in `docs/firmware-map.md`)

- **Dev sketch (D-19):** every animation runs from `loop()` as a coroutine (`delay(n)` became
  `PAT_DELAY(n)`; no local may live across a yield). An I2C command or a debounced (20 ms) change of
  the rotary/jumper code switches the sequence at the next frame; the same I2C command restarts it;
  GPIO modes loop and resume after an I2C sequence; code 0 stops a GPIO mode. Scenarios carry an
  8 000-cycle timing tolerance for the scheduler (D-20).
- **Specimen only:** the I2C handler runs the whole animation **inside the TWI ISR** with interrupts
  re-enabled; a second command mid-animation nests and the outer animation resumes afterwards.
- **I2C register interface (dev sketch, D-22):** the protocol is specified in
  `docs/i2c-protocol.md`, and its constants are in `docs/magicpanel_i2c.h`. Byte 0 with bit 7
  set addresses a register. A lone byte 0–55 is still a legacy command while `CONFIG.LEGACY` is
  set (EEPROM, default on). Multi-byte writes no longer deafen the receiver (the specimen's
  `Wire.read()` never drained the buffer). The register tests are
  `tests/test_i2c_protocol.py`: they read the header and the spec's catalogue table. If you
  change a sequence's timing, run `tools/measure_lengths.py --write`. Any protocol change updates
  the spec, the header and the tests together.
- Command 2 falls through into command 3; `allOFF;` (no parentheses) in `allONTimed` is a
  no-op, so commands 1–4 leave the panel on; `FadeOutIn` writes 64 bytes past `VMagicPanel`
  in the specimen (contained by a spill area in the dev sketch, D-21). These are baselined as-is;
  fixing them is a behaviour change that requires a deliberate re-baseline.
- Command 1 / jumper mode 8 block for 1000 s; their scenarios only observe the ON state.
- **Orientation (A-1, D-25):** the rendered grid is the panel *as installed* in a dome, where
  v010.5's patterns look as named (row 0 top, `VMagicPanel[row][7]` leftmost). On the bench the
  same panel looks rotated 180°. The dev sketch draws like v010.5 by default; the `ORIENTATION`
  register (0x32, saved in EEPROM) turns the picture 180° in `MapBoolGrid()`.
- **Sequences 40-55 (D-26):** the v010.6/v011 sequences (TheJugg1er), ported from
  `MagicPanel_v011.ino` (in the repo, reference only) under v011's numbers; the random shows are
  56 and 57 and `SEQ_COUNT` is 58. `DrawHalf()` is `__attribute__((flatten))` on purpose: without
  it `lc.setRow()` stops being inlined into `PrintGrid()` and every frame costs ~400 cycles more.
  Catalogue flag `VARIES` (0x10) marks the two flicker sequences, whose length is only typical.
- **What I2C traffic disturbs (D-27):** only register `START`/`STOP` and one-byte legacy
  commands affect a running sequence. Only the legacy path advances `random()` and resets
  `RandomTime` (v010.5 fidelity, D-16); register accesses must not, or polling holds a random
  show dark. `consumeI2C()`'s early return must keep testing `pendAction`, or register
  start/stop is dropped.
- **Version:** the dev sketch is v012 (firmware 0.12.1, protocol v1.1), the successor to v010.5
  and to TheJugg1er's v010.6/v011; the number 0.11 is skipped because v011 exists already.

## Using the MCP server from Claude Code

`.mcp.json` registers `magicpanel` (needs `make venv` first). Batch: `build_firmware`,
`run_scenario`, `compare_to_baseline`, `run_all`, `render_gif`, `list_scenarios`,
`describe_firmware`. Interactive: `sim_start` → `sim_step ms=100` → `sim_i2c_write bytes=[20]`
→ `sim_step ms=200` → `sim_get_display` / `sim_get_log` → `sim_stop`. `update_baseline` is
gated: it shows the diff first and applies only with `confirm=true`. Keep outputs small; the
full artefacts are files under `runs/`.

## User documentation site

`manual/` (hand-written) + `mkdocs.yml`, built with Zensical; `make docs-gen` writes
`manual/generated/` from `build/firmware.elf` (pattern pages, GIFs, player data; gitignored),
`make docs-build` builds strictly. Versions go to `gh-pages` via mike from CI only
(`.github/workflows/docs.yml`, `release.yml`; RELEASING.md). Zensical runs no MkDocs plugins or
hooks, so generate content with tools, not build plugins (D-23). User-visible changes go in
`CHANGELOG.md` under `Unreleased`.

## Conventions

- Python tests are **pytest** (`tests/`, fixtures in `conftest.py`). No unittest.
- GitHub Actions are pinned to full commit SHAs with a `# vX.Y.Z` comment; bump both together.
- Record non-obvious choices and open assumptions in `docs/decisions.md` (D-n / A-n).
- Commit in small reviewable steps; baselines and the scenario that produced them go together.
- No wall-clock time anywhere in a comparison path; all timing is AVR cycles.
- Do not modify anything under `third_party/`; they are pinned submodules.
- `runs/` and `build/` are scratch (gitignored); `tests/baselines/` is truth (committed).
