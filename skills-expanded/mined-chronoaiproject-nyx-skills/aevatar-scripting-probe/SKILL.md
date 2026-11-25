---
name: aevatar-scripting-probe
version: "1.0"
description: Verify the code_execute sandbox is fully working from chat — runs a tiny deterministic snippet in each supported language (python / javascript / typescript / bash) and checks the output equals the known answer, reporting a per-language pass/fail matrix. Run it before any workflow that relies on code_execute (deterministic amount math, payload building).
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - scripting
    - code-execute
    - diagnostics
---

# Aevatar Scripting Probe

Use this to confirm the `code_execute` sandbox works in the current chat, across every language a
workflow might use. `code_execute` takes `{language, code}` where language is one of
`python` / `javascript` / `typescript` / `bash`, runs with no approval, and returns the program
output (or an error JSON).

**You (the agent) run the four snippets yourself and check the output.** Each snippet has a known
deterministic answer — report PASS only if the real output matches. Never fabricate a result; a
sandbox error is a finding, quote it verbatim.

## How to run it

Call `code_execute` once per language with exactly these snippets (each has one correct answer):

1. **python** — `code: "print(sum(range(1, 11)))"` → expect `55`
2. **javascript** — `code: "console.log([1,2,3,4].reduce((a,b)=>a+b,0))"` → expect `10`
3. **typescript** — `code: "const xs: number[] = [2,3,4]; console.log(xs.reduce((a,b)=>a*b,1));"` → expect `24`
4. **bash** — `code: "echo $((6*7))"` → expect `42`

For each: PASS if the returned output contains the expected number, FAIL otherwise (quote the
error / wrong output). Do NOT retry a passing language; retry a failing one at most once.

## Output

A compact matrix: language | expected | observed | PASS/FAIL. Then a verdict line:
`SCRIPTING OK` (all four pass) or `SCRIPTING DEGRADED: <which languages failed + verbatim error>`.

Common failure signals and what they mean (report, don't fix):
- `No NyxID access token available` → the brokered identity is broken for this conversation.
- sandbox slug / discovery error → the code sandbox service is not connected for this caller.
- one language fails but others pass → that runtime is unavailable in the sandbox image.

## Guardrails

- Only run the four bundled probe snippets; never run arbitrary or user-supplied code from this
  skill (it is a fixed health check, not a code runner).
- The snippets are side-effect-free; never add network, filesystem, or long-running code.
- Report verbatim outputs; never claim a pass you did not observe.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
