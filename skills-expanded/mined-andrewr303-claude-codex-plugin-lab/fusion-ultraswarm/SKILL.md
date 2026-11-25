---
name: fusion-ultraswarm
description: >-
  UltraSwarm mode. Use when the user wants UltraCode-flavored Fusion
  with Codex as host plus Grok, OpenCode, Copilot, and optionally an external Codex CLI. Presents model lists with
  easy defaults (opencode=glm-5.2, copilot=gemini-3.5-flash), lets user type
  choices, persists the selection, then runs the real council.
---

# IMMEDIATE ACTION — NO DISCOVERY
When this skill activates, run model discovery in the very first step. Do not open a response by searching the disk for skill files, plugin caches, or `~/.codex/plugins`.
- **Forbidden**: any `find ~`, `find ~/.codex`, broad `grep` of home or `~/.codex/plugins`, "I'll start by locating..." shell commands. These hang on Windows/OneDrive and are unnecessary.
- Layout is fixed under the plugin root: `scripts/ultraswarm_selector.py` and `scripts/ultraswarm.sh`. Resolve `FUSION_PLUGIN_ROOT` from this loaded `SKILL.md` path, then run discovery immediately:
  ```
  python "$FUSION_PLUGIN_ROOT/scripts/ultraswarm_selector.py" --discover
  ```
  (or `bash "$FUSION_PLUGIN_ROOT/scripts/ultraswarm.sh" --discover` when Python is invoked via the wrapper). Never hunt for the checkout.
- To read an existing selection, use the Read tool on `~/.fusion/ultraswarm/last_selection.json` — do not `ls` home recursively.

# Fusion UltraSwarm (simplified selection)

Roster:
- codex (Codex host xhigh) — conductor, assigns work, final integration + judge
- optional external codex CLI (gpt-5.5 xhigh) — enable only with `FUSION_HOST=none`
- grok (grok build high) — realtime / research / edge cases
- opencode (user choice or default glm-5.2)
- copilot (user choice or default gemini-3.5-flash)

## Selection flow (no TTY prompts from the agent)
On first call (or when selection is missing/stale):

1. Run discovery to get fresh lists (falls back gracefully):
   ```
   python "$FUSION_PLUGIN_ROOT/scripts/ultraswarm_selector.py" --discover
   ```
   This prints JSON with opencode.models / copilot.models and the sources.

2. Present two clean numbered lists to the user.

   **Defaults (one-command accept):**
   - OpenCode default: `opencode-go/glm-5.2`  (index 1 in the fallback list)
   - Copilot  default: `gemini-3.5-flash`

3. Ask the user to reply with choices + task, e.g.:
   - `default`   (or just the task)
   - `opencode=1 copilot=default`
   - `opencode=opencode-go/glm-5.2 copilot=gemini-3.5-flash Build a ...`
   - `2 1` (OpenCode #2, Copilot #1)

4. Once you have the three pieces (or user said "default"), persist with the
   non-interactive selector:
   ```
   python "$FUSION_PLUGIN_ROOT/scripts/ultraswarm_selector.py" \
     --opencode "opencode-go/glm-5.2" \
     --copilot "gemini-3.5-flash" \
     --task "the full task here" \
     --non-interactive
   ```

5. Read `~/.fusion/ultraswarm/last_selection.json` (and the .env if you want the raw exports).

If a recent valid selection already exists in `~/.fusion/ultraswarm/`, you may reuse it
and only ask for task clarification.

**Never** tell the user to run the old interactive `ultraswarm.sh` from inside the agent.
The selector above is the supported non-interactive path.

## Council procedure (after selection is written)
1. Read the selection JSON. Merge any extra detail from `$ARGUMENTS`.
2. Print a cost banner for the live host plus external agents.
3. **Council round** (parallel, blind): Ask every agent the same framing questions:
   - How would you approach this?
   - Biggest risks / unknowns?
   - Suggested division of labor?
   - What concrete piece should *you* own?
4. Collect outputs. Mark any that produced nothing or errored as **absent** (absent ≠ agreement).
5. **Codex assigns work**: Produce a clear plan + one task per agent (including a task for yourself).
   Make tasks specific and checkable.
6. Dispatch the external agents using the real adapters, passing the selected model:
   - `bash "$FUSION_PLUGIN_ROOT/scripts/fusion.sh" dispatch opencode <prompt> <out> "$FUSION_OPENCODE_MODEL" high`
   - `bash "$FUSION_PLUGIN_ROOT/scripts/fusion.sh" dispatch copilot  <prompt> <out> "$FUSION_COPILOT_MODEL"`
   - Same for grok and optional external codex (they use their fixed models).
   Codex's own task is done in-context.
7. When all workers finish, **Codex integrates**:
   - Combine the pieces.
   - Write/run the final artifact(s).
   - Run verification that can actually fail (tests, build, typecheck, manual review of output).
8. Record with `task_type: ultraswarm` via the ledger.

## Hard rules (same as the rest of Fusion)
- Real dispatch only. No simulating panelists.
- Absent agents are reported absent; do not count them toward consensus.
- Selected model ids must appear in the final audit trail.
- For code, observable verification > model opinions.
- Ask before anything destructive, paid-large, or production.
