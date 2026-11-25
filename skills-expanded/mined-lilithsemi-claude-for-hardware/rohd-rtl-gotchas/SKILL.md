---
name: rohd-rtl-gotchas
description: Use when building or testing RTL in ROHD (Dart), rohd_bridge, or rohd_hcl and hitting hierarchy-violation errors, "Bad state: No element" at sim setup, co-simulation failures, SystemVerilog emission name mismatches, or unexpected register read latency
---

# ROHD RTL Gotchas

## Overview

ROHD (Rapid Open Hardware Development, Dart RTL) plus rohd_bridge and rohd_hcl have a handful of sharp edges that produce cryptic errors at build or sim setup, far from the actual cause. These are the ones that cost real hours on River and Harbor.

**Core principle:** Most of these surface as a hierarchy-rule violation or a "Bad state: No element" hang, and the fix is almost never where the error points. Match the symptom below to the cause directly instead of debugging the stack trace.

## When to Use

- A ROHD build throws "Violation of input/output rules" or inverts the hierarchy
- Sim hangs or throws "Bad state: No element" during `Sequential` setup
- Co-simulating a DUT against a behavioral model that shares a bidirectional net
- SystemVerilog emission references a module name that the emitted file doesn't define
- A `RegisterFile` read returns data a cycle off from what the FPGA will do

## inout Co-Simulation Between Siblings Is Forbidden

ROHD's hierarchy checker rejects wiring two sibling modules through a shared bidirectional (`inout`/`LogicNet`) net that closes a loop (a SPI controller plus a behavioral SPI-flash model sharing `spi_io`). The error reads "should only communicate via inputs/inouts" and it may even invert the hierarchy (think the DUT contains its parent).

- **For a testbench, avoid the bidirectional co-sim.** Test a path that uses a plain unidirectional input instead (drive MISO procedurally in standard mode rather than the quad `inout` bus). The FSM, byte-order, and data-assembly logic is usually shared across modes, so you still cover it.
- **If you must share an inout**, pass the SAME `LogicNet` to both modules' `addInOut` (the ROHD inout-loopback idiom). Do not `<=` one onto the other. Two active drivers stay fragile; a parent harness beats top-level wiring.
- **Blackbox primitives (DP16KD and friends) have no sim model**, so FPGA-only memory paths can't be co-simulated at all. Verify the equivalent flop model instead, at the same latency (see below).

## "Bad state: No element" Is A Clock Problem

Two distinct causes, same message:

- **`Sequential` clocked on a derived/gated clock.** `Sequential(someModuleOutput, ...)` where the clock is a controller-generated, sometimes-static signal (a generated `spi_clk`) throws at sim setup. Fix: clock the model on the real system clock and detect edges of the derived clock manually (`rising = clk & ~prevClk`, register `prevClk`).
- **`Simulator.reset()` at the wrong time.** It clears registered events including the clock generator. Call it in `tearDown` between tests, never after `build()` and before `Simulator.run()`. The pattern is: build, inject resets, `setMaxSimTime`, `unawaited(Simulator.run())`, then await clock edges.

## rohd_bridge BridgeModule Composition

- Driving a BridgeModule input from a test at top level: `module.input('clk').srcConnection! <= signal` works. Inside a parent module it inverts the hierarchy unless you register the child first with `parent.addSubModule(child)`.
- `addSubModule` only accepts a `BridgeModule`. A plain ROHD `Module` auto-parents via normal inference; do not `addSubModule` it.
- When driving/reading a bus from a test, use the rohd_bridge wishbone port names (`bus_STB`, `bus_CYC`, `bus_WE`, `bus_ADR`, `bus_DAT_MOSI`, `bus_SEL`, `bus_ACK`, `bus_DAT_MISO`), not the `bus.stb` abstraction.

## definitionName Collisions Break SV Emission

Two instances of the same module class with different constructor params (two ROMs with different contents or widths) are different module definitions. ROHD uniquifies the name (`Foo_0`), but per-module SystemVerilog file emission can then collide or mismatch the reference ("RiverCore refs Foo, file defines Foo_0", reported as "module not part of the design").

Fix: give each a distinct stable `definitionName` plus `reserveDefinitionName: true` so the emitted file name and the instantiation agree.

When invoking yosys after `module.generateSynth()`: the top module name in the SV is the class/`definitionName`, not the instance `name`. Grep `^module` to find the real top first.

## Configure With Parameters, Not `Process.environment`

Do not read `Process.environment` (or any process global) inside a module to switch a feature, a width, or a behavior. Pass a constructor parameter or a typed config object. The environment is legitimate only at the OUTERMOST generator or CLI entry point, parsed once into that config, which then flows down as parameters.

- **A global cannot differ per instance.** `Process.environment` is process-wide, so every instance of a module elaborated in one run reads the SAME value. You cannot build a fast variant and a slow variant, or two byte-lanes with different timing, or two SoC configs, in one process. Parallel test elaboration reads the one shared value too. Anything that can be multi-instance MUST take the setting as a parameter.
- **It makes the RTL depend on invisible ambient state.** Two runs of the same source emit different netlists, and nothing in the design records which knob was set. The byte-identical-regen guardrail and any reproducible build both break.
- **It hides the capability.** A feature gated by an env var is not declared by the design, so the tooling and the tests cannot see it. This is the same failure as "A Capability Is Not A CLI Flag" in `silicon-grade-discipline`: the design declares the capability, the generator reads it.
- **A bring-up tuning knob is no exception.** Make it a CLI flag parsed into the config, not a `Process.environment` read deep in the PHY. Then the build records its setting and two lanes get tuned independently, which a single process-wide env var can never do.
- **Migration.** For each `Process.environment['X']` in a module, add a constructor field with a sensible default, thread it from the generator's parsed config, and delete the env read. The knob becomes part of the module's declared interface, visible to callers and tests. See `hdl-module-design` for the typed-config-object shape.

## RegisterFile Read Latency

`rohd_hcl` `RegisterFile` read is combinational (readLatency 0). `wrapReadForRegisterFile(..., readLatency: N)` delays only `valid`, not `data`/`done`. For a real registered (BRAM) read you must register `data` yourself and craft the done/valid handshake to match.

If a consumer FSM holds its address until `done`, it tolerates +1 read latency for free (one fill cycle per probe). Verify by running the sim flop path at the SAME latency the FPGA BRAM will have, so the sim proves the actual hardware timing. See `fpga-synthesis-fit` for the flop-vs-BRAM latency-matching rule.

## Midstall House Style

- River and Harbor are pure ROHD/Dart RTL, no external Verilog or vendor wrappers; these gotchas all came from that path.
- Keep HDL test files small: `dart test` parallelizes per file, not within a file.
- See `net-connect-and-bridgemodule-synth.md` in this directory: the `net_connect` duplicate-port form that breaks yosys synth (and the fix), the `srcConnection!` sub-module wiring idiom, and the per-test Simulator wire-listener slowdown that reads as a hang.
- See `silent-width-and-instantiation-traps.md` in this directory: the `zeroExtend().signExtend()` no-op that kills sign-extension, verifying a block is even instantiated (grep the netlist) before debugging its internals, sizing a sentinel or override field for the value not the lane count, the sum-needs-one-more-bit overflow, force-clearing a stale codegen snapshot after a path-dependency change, and confirming a debug register decodes the field you assume on the active build config.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Pairs with `hdl-module-design`, `fpga-synthesis-fit`, and `differential-verification`.
