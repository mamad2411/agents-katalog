---
name: evm-audit-flow
audience: specialist
description: Use when you have a Foundry or Hardhat repository of Solidity or Vyper contracts and want the end-to-end EVM review workflow on native CLIs — a slither static pass, semgrep taint rules, mythril symbolic execution, echidna and medusa invariant fuzzing, halmos formal checks, then a forge build-and-test regression.
---

# evm-audit-flow

Stateful EVM audit pipeline from raw contract source through confirmed-finding delivery. Use
when you have a Foundry or Hardhat project with Solidity/Vyper contracts. Every step runs a
**native host CLI** (`slither`, `semgrep`, `myth`, `echidna`/`medusa`, `halmos`, `forge`) invoked
directly; there is no MCP wrapper in front of them, no `tool_wrappers` layer, and no retired KG.
Start from `pre-audit-threat-model` if an x-ray does not already exist.

## Order of ops

1. **Static analysis pass.** Run `slither .` directly from the project root (it needs the
   Foundry/Hardhat build context, not a loose `.sol` file). `slither . --json -` gives
   structured output, `slither --list-detectors` enumerates detectors, and
   `slither . --print function-summary` gives per-function context. Classify
   detectors: HIGH-signal (`reentrancy-eth`, `arbitrary-send`, `controlled-delegatecall`,
   `suicidal`, `unprotected-upgrade`) vs NOISE (naming-convention, too-many-digits,
   solc-version). Do NOT dismiss `reentrancy-eth` as a false positive without tracing the call
   stack. `solc-select` is available for pinning the compiler, but do **not** pass
   `--always-install` (no silent network downloads); confirm the version is already present.

2. **Pattern/taint pass (the static analog of symbolic execution).** Run project-specific
   Semgrep rules with the `semgrep` CLI directly —
   `semgrep scan --config <rules.yaml> --metrics=off --json <path>` — taint
   sources = external/`msg.sender`-reachable inputs, sinks = value transfers,
   `delegatecall`, storage writes. Author rules with `semgrep-rule-author`; a reachable sink
   with no realized impact is a lead, not a finding. Local rule files need no login.

   **A zero is not a clean scan until the same rule has fired on a known positive.** Two
   measured ways to get an empty result (2026-10-27, semgrep 1.157.0): a rule file that fails
   YAML parsing exits 7 and reports the error only in the JSON `errors` array with an empty
   `results` list (an unquoted pattern containing `{` or `:` is the usual cause — quote it:
   `pattern: "$X.call{value: $V}($A)"` fires, the unquoted form does not parse); and a
   pattern that does not match the call shape — `$X.call(...)` misses
   `to.call{value: 1}("")` — returns zero findings, zero errors, exit 0. Check the exit code,
   `errors`, and the positive control before believing a zero.

3. **Symbolic execution.** Run `myth analyze <contract> --execution-timeout 600` on every
   contract flagged HIGH by step 1, plus any contract with external calls, `delegatecall`, or
   `selfdestruct`. Surface: integer overflow, unchecked return values, `tx.origin`
   access-control bypass, ether-locking. For proxies, resolve the implementation address
   first — `myth` cannot follow `delegatecall` to a separate contract by default.

4. **Invariant authoring + fuzzing.** Author/refresh Echidna or Medusa invariants (token
   conservation, access-control, CEI reentrancy) in `test/invariants/`. Run
   `echidna . --contract <Test> --config echidna.yaml` for an initial pass; if coverage
   plateaus switch to `medusa fuzz --config medusa.json` (coverage-guided). For DeFi, apply
   `defi-invariant-check`. Minimum meaningful campaign: 30 minutes.

5. **Formal verification (critical paths only).** Run `halmos --function <prop> --loop <N>` on
   high-value properties Echidna found hard to falsify in bounded time. Halmos gives unbounded
   symbolic verification for simpler properties; do not throw the whole suite at it (it times
   out on complex state machines or unbounded loops).

6. **Lint + compile regression.** `forge build` (or `solc` on modified contracts) to confirm
   no compilation regression; `forge fmt --check` for style.

7. **Final test run.** `forge test` to confirm the suite passes; record any new failure.

## When to pivot

- **Slither false-positive flood:** narrow with `--detect <high-signal list>` and add a
  `.slither.config.json` suppression for known project FPs.
- **`myth` times out on complex contracts:** `--execution-timeout 300 --create-timeout 60`,
  and focus on functions with external calls and value transfers.
- **Echidna coverage plateau:** add a corpus dir (`--corpus-dir`) or switch to Medusa's
  coverage-from-corpus mode.
- **Halmos timeouts on loop-heavy code:** bound with `--loop`; Halmos is not for unbounded
  loops.

## Anti-patterns

- Do NOT report Slither medium/low findings without confirming exploitability via a call
  sequence or `myth` evidence.
- Do NOT run Echidna/Medusa without invariant tests — property-less fuzzing yields nothing.
- Do NOT run `myth` on a proxy without resolving the implementation first.
- Do NOT skip Slither for "simple" contracts — over half of historical EVM findings are in
  contracts under 200 lines.
- Do NOT invoke any dead `tool_wrappers/*` name (`slither_scan`, `mythril_analyze`,
  `echidna_fuzz`, `halmos_check`, `forge_test`); those wrap a container library that no longer
  exists — use the native CLIs above.
- Do NOT route through the retired `guarded-slither` / `guarded-semgrep` MCPs (Trail of Bits
  mcp-context-protector wrappers, removed from both lanes on 2026-10-27, commit `02442bdc`);
  their tool names (`run_detectors`, `semgrep_scan_with_custom_rule`) no longer resolve — run
  the CLIs above.

## Example

```bash
# Step 1: static analysis (native)
slither . --exclude naming-convention,solc-version

# Step 2: taint rules (native) -- run the same rule on a known positive first
semgrep scan --config rules/evm-taint.yaml --metrics=off --json src/

# Step 3: symbolic execution on a flagged contract
myth analyze src/Vault.sol --execution-timeout 600

# Step 4: fuzzing (30-min minimum for DeFi)
echidna . --contract InvariantTest --config echidna.yaml --test-limit 500000

# Step 7: final test run
forge test
```

## Recording (chrono-vault)

The task packet's injected memory contract owns the exact call shape, sequence, and fields - see
`wirework-reflect`. Do not copy a `record(...)` example or add fields (including `source_task`) from
memory; the server binds them, and a baked example violates the run's authenticated schema. Memory is
best-effort telemetry and never gates the work. What is worth recording here is the task-specific
outcome: finding counts by severity, invariant violations, tools run.
