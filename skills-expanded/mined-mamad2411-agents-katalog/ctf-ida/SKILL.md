---
name: ctf-ida
description: Use when reverse engineering or binary triage should be performed through IDA Pro and the IDA MCP server. Trigger on mentions of IDA, IDA Pro, IDB, Hex-Rays, decompile, function renaming, type recovery, or when the user has already obtained a local executable and wants AI-assisted reverse analysis through the live IDA session.
---

# CTF IDA

## Overview

Use IDA as the primary workspace when the user wants interactive reverse analysis against a local sample, especially when function discovery, decompilation, renaming, typing, xref tracing, or patch planning will benefit from a live IDB.

## Use This Skill For

- The user explicitly mentions `IDA`, `IDA Pro`, `Hex-Rays`, `IDB`, or `MCP server`.
- A local executable, DLL, driver, shellcode loader, or unpacked sample has been obtained and deeper reverse analysis is needed.
- The task benefits from interactive decompilation, function renaming, type recovery, xrefs, call graphing, or patch verification inside IDA.

## Mandatory Handshake

If the task requires IDA-backed analysis and the MCP server is not already confirmed reachable, stop and ask the user to do this first:

1. Open the target file in IDA and wait for auto-analysis to finish.
2. Start the IDA MCP server in that IDA session.
3. Tell you when IDA and the MCP server are ready.

Use a direct prompt such as:

`请先用 IDA 打开目标文件，并在该 IDA 会话里启动 MCP server。准备好之后告诉我，我再继续基于 IDA 做分析。`

Do not pretend the IDA session exists if `server_health` or equivalent checks are unavailable or failing.

## Workflow

1. Confirm MCP readiness.
   Run IDA health or warmup checks first. If they fail, go back to the handshake above.
2. Triage the binary.
   Use the binary survey first, then inspect entry points, imports, strings, and high-xref functions before drilling down.
3. Find the trust boundary.
   Locate user input, config loading, decode steps, comparisons, decryptors, validators, or dispatchers.
4. Recover semantics.
   Rename functions, recover types, inspect globals, trace xrefs, and separate runtime noise from user logic.
5. Verify hypotheses.
   Use decompilation, disassembly, CFG, and cross-references to prove the control flow rather than guessing from names alone.
6. Extract the shortest path.
   Produce the answer, patch point, exploit primitive, or reimplementation route with concrete evidence from the IDB.

## IDA-Specific Heuristics

- Start with whole-binary survey before opening dozens of individual functions.
- Treat CRT, STL, Go runtime, Rust runtime, packer stubs, and compiler scaffolding as noise until proven otherwise.
- Check alternative execution paths early: TLS callbacks, constructors, exception handlers, exported entrypoints, and custom loaders.
- Short functions are often meaningful in crackmes and shellcode loaders; verify in assembly when decompilation looks empty or trivial.
- When names are poor, prioritize xrefs, shared strings, imported APIs, and constants over raw pseudocode readability.
- If a rename or type change matters, verify it against the updated decompilation rather than assuming it helped.

## Coordination

- Use `ctf-reverse` for challenge-solving logic once the relevant functions are identified in IDA.
- Switch to `ctf-pwn` when the binary is better solved through memory corruption or exploit development than semantic recovery.
- Switch to `ctf-crypto` when the hard part becomes algebra, encoding structure, or cryptographic weakness after the algorithm is identified.

## Guardrails

- Do not ask the user to open IDA if the task can be solved cleanly from source code or a small script alone.
- Do not claim MCP-backed findings unless the live IDA session was actually reachable.
- Do not drown the analysis in full-program decompilation when one checker, dispatcher, or decode chain is enough.
- If the sample is packed or self-modifying, note that static IDA output may be incomplete and say what dynamic step is needed next.

## Output Expectations

- Report the functions or regions that matter.
- Explain why they matter with xrefs, imports, strings, constants, or control-flow evidence.
- State the next actionable step clearly: deeper reverse, patch, script reimplementation, exploit path, or user action inside IDA.
