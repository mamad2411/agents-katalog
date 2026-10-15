---
name: freshwater-doctor
description: Diagnose the local "math research stack" — Lean 4 + Mathlib, optional Wolfram Engine, and the MCP servers (`lean-lsp`, `lean-explore`, optional `wolfram`) that wire them into Claude Code. Runs an exhaustive checklist (toolchain versions, Mathlib build cache, MCP wiring, plugin installs) and reports status as a punch list with the smallest recommended next install step. Activate when the user asks "is my math setup ready", "check my Lean / Mathematica install", "verify the math stack", "/freshwater-doctor", or wants to bootstrap a fresh math research environment.
metadata:
  author: pionless-matrix
  version: "0.1"
  pionless.category: diagnostic
  pionless.series: freshwater
---

# freshwater-doctor

Diagnose whether the user's local environment has the components needed for the **freshwater-\*** math research workflow:

- **Compute side**: Wolfram Engine + the official `Wolfram/MCPServer` paclet (or a community Mathematica MCP). *Optional* — the rest of the stack is useful without it.
- **Proof side**: `elan` → Lean 4 → a Mathlib-bearing Lake project, plus `lean-lsp-mcp` and `lean-explore` MCP servers, plus the `lean4-skills` Claude Code plugin.
- **Glue**: `uv` / `uvx` for installing MCP servers, and the Claude Code MCP wiring (`claude mcp list`).

This skill **diagnoses, it does not install**. Its output is a structured checklist plus a recommendation; the user runs the actual install commands themselves.

## When this skill activates

- The user asks "is my math setup ready?", "what's missing?", "verify my Lean install", "do I have everything for the math agent?"
- The user invokes `/freshwater-doctor` explicitly.
- A sibling `freshwater-*` skill (e.g. `freshwater-prove`, `freshwater-compute`) hits a precondition failure and wants to run the doctor before retrying.

If the user is asking how to **install** the stack (not check it), this skill still runs first — diagnosis before prescription — and then hands off.

## What it checks

Run `bash scripts/check.sh` from the skill directory. The script probes (in roughly this order):

1. **Core glue**: `uv`, `uvx`, `python3`, `claude` CLI presence and versions.
2. **Lean toolchain**: `elan`, `lean`, `lake`, the active toolchain channel.
3. **Mathlib project**: walks common workspace paths (`~/workplace`, `~/math-workspace`, `$PWD`) up to a few levels deep; reports any directory containing `lakefile.toml` / `lakefile.lean` whose dependencies include `mathlib`.
4. **Wolfram (optional)**: `wolframscript`, `/Applications/Mathematica.app`, `/Applications/Wolfram Engine.app`, license activation status.
5. **MCP servers**: parses `claude mcp list` for `lean-lsp`, `lean-explore`, `wolfram` / `mathematica` entries; flags servers configured but failing health check.
6. **Claude Code plugins**: checks `~/.claude/plugins/` for the optional `lean4-skills` plugin and confirms the parent `pionless-agent` plugin (which ships this skill) is installed. Note that `freshwater-*` are skills inside `pionless-agent`, not standalone plugins.
7. **Disk**: free space on `$HOME` (Mathlib cache + Wolfram are several GB combined).

The script writes a plain-text checklist to stdout using `[OK] / [--] / [!!]` markers (no emoji), one component per line, plus a final `RECOMMENDATION:` line.

## Workflow

When activated:

1. Run `bash scripts/check.sh`. Capture stdout.
2. Parse the checklist. Group findings into:
   - **Working** — `[OK]` lines.
   - **Missing (blocker)** — `[--]` lines for components the freshwater-\* core needs (Lean, Mathlib, lean-lsp-mcp).
   - **Missing (optional)** — `[--]` lines for Wolfram-side components.
   - **Warnings** — `[!!]` lines (e.g. installed but outdated, or configured but not authenticated).
3. Render a compact markdown report to the user: a 4-row table (Working / Blocker / Optional / Warnings) with one bullet per item.
4. End with a single **next step** — the install with the lowest cost-to-unblock-most-things ratio. Examples:
   - No `elan` → "Install elan: `curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh`"
   - elan present, no Mathlib project → "Create a sandbox project: `cd ~/workplace && lake new math-sandbox math.toml`, then add Mathlib"
   - Lean ready, no `lean-lsp-mcp` → "`claude mcp add --scope user lean-lsp -- uvx lean-lsp-mcp`"

Do **not** run installs autonomously. Print the command, explain what it does, and wait for the user.

## Wolfram Engine is OPTIONAL

The user has expressed that they may not need Wolfram Engine — the proof side (Lean + Mathlib) is the load-bearing half of the stack. Mark Wolfram-side components as `optional` in the report. Only nag about them if the user explicitly says they want symbolic computation.

If the user wants the open-source-only path, point them at `sympy-mcp` instead of Wolfram MCP — call this out as a footnote, not a recommendation.

## Output format

The agent's reply to the user should look roughly like:

~~~markdown
## freshwater-doctor: stack status

| Bucket | Components |
|---|---|
| **Working** ✓ | uv 0.9.17, Python 3.12, claude CLI |
| **Blocker** ✗ | elan, lean, Mathlib project, lean-lsp-mcp |
| **Optional** | Wolfram Engine, wolfram MCP |
| **Warnings** | (none) |

**Next step**: install elan (one curl command). This unblocks the entire proof side in one shot — Lean + lake follow automatically.

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

Want me to run it?
~~~

Keep the table tight; don't pad with components that aren't present and aren't blockers.

## Anti-patterns

- **Don't try to install anything from inside this skill.** The doctor diagnoses; the user runs the recommended install commands themselves.
- **Don't recommend Wolfram as a blocker.** It is optional in the freshwater stack design.
- **Don't run `lake build` to verify Mathlib.** That's a 10–30 minute operation; the doctor is supposed to be fast (sub-second). Detecting `lake-manifest.json` + a populated `.lake/build/` is enough to declare "Mathlib project present and previously built".
- **Don't write to the user's filesystem.** This is a pure-read diagnostic. The check script must not create files outside its own scratch space.

## Output

A single markdown table report to the user, plus one concrete recommended next-step command. No files written.
