---
name: tut
description: "Re-shows the structured first-run menu (finalize / onboard / doctor / faq / help) on demand, with current completion status. Use when the user wants to revisit the tutorial, asks 'what should I do next?', or types `/topia:tut`. This is the explicit re-entry point for the menu that auto-shows on session-start until completed."
metadata:
  author: topia
  version: "1.0.0"
  layer: L3
  model: haiku
  group: docs
  tools: "Bash, Read"
---

# tut

## Purpose

Replay the structured first-run menu that session-start prints (and auto-suppresses once finalize + onboard are detected) so users can see the same status check and "what should I do next" guidance at any time. Reuses the same completion-detection heuristics as the hook, so the check-marks reflect actual state.

Future: this skill will dispatch into beginner / intermediate / advanced tutorial tracks. For v3.2.0 it's a status-aware menu only — the tracks ship separately.

## Triggers

- `/topia:tut` — primary
- `/topia tut` — router alias
- User says "show me the tutorial again", "what should I run next", "I missed the first-run menu", "is there a topia tutorial"

## Steps

### Step 1 — Detect completion state

Mirror the logic in `hooks/session-start/index.cjs` `detectFinalizeNudge()`. For each step, check if it's done:

**Finalize:**
- `.topia/.finalized` exists in project, OR
- `~/.claude/settings.json` contains `topia.js hook-dispatch` or `Topia-managed`

**Onboard:**
- Any of these files exists in `<project>/.topia/`: `DEVELOPER-GUIDE.md`, `conventions.md`, `progress.md`, `decisions.md`

**Doctor:**
- Always shown as `[ ]` (it's not a one-time step; users should run it any time something feels off).

Use Bash to detect:

```bash
PROJ_TOPIA=".topia"
FINALIZED="[ ]"
if [ -f "$PROJ_TOPIA/.finalized" ]; then
  FINALIZED="[x]"
elif [ -f "$HOME/.claude/settings.json" ] && grep -qE "topia\.js hook-dispatch|Topia-managed" "$HOME/.claude/settings.json"; then
  FINALIZED="[x]"
fi

ONBOARDED="[ ]"
for f in DEVELOPER-GUIDE.md conventions.md progress.md decisions.md; do
  if [ -f "$PROJ_TOPIA/$f" ]; then ONBOARDED="[x]"; break; fi
done

DISMISSED=""
if [ -f "$PROJ_TOPIA/.dismissed" ]; then DISMISSED="(menu currently dismissed in this repo)"; fi

echo "FINALIZED=$FINALIZED  ONBOARDED=$ONBOARDED  $DISMISSED"
```

### Step 2 — Render the menu

Print the same shape as session-start, but unconditionally (the user explicitly asked to see it):

```text
  ╭───────────────────────────────────────────────────────────╮
  │  Topia — your next steps                                  │
  ╰───────────────────────────────────────────────────────────╯
    {FINALIZED} /topia finalize  — system-wide discipline hooks +
                          agora-code persistent memory (one-time per machine)
    {ONBOARDED} /topia onboard   — scan this repo, write CLAUDE.md +
                          .topia/ context so future sessions start hydrated
    [ ] /topia doctor    — verify install health and surface any fixes
    [ ] /topia:org-config — team policy in .topia/org/org.md (commit for teams)
    [ ] /topia:faq       — list bundled docs + visualizer entry points
    [ ] /topia --help    — full command reference

  Each [x] is auto-detected from your current install state. To hide the
  session-start menu permanently for this repo: /topia finalize --dismiss
  To bring it back: delete .topia/.dismissed
```

Substitute the actual `[ ]` / `[x]` from Step 1.

### Step 3 — Brief description of each option

After the menu, add a 1-sentence "what does this do?" for any item the user is unfamiliar with. Keep it short — the menu is the main artifact, the descriptions are scannable backup:

- **finalize** — opt-in extras. Wires dispatch hooks system-wide, optionally installs the agora-code MCP for persistent memory, adds `.topia/` to your repo's `.gitignore`. Reversible.
- **onboard** — analyzes this repository (stack, conventions, test framework, recent commits) and writes a CLAUDE.md plus `.topia/` context files so future sessions don't have to re-discover the project from scratch.
- **doctor** — sanity-check: nexus integrity, gitignore coverage, tracked-state-files audit, hook health. Surfaces any fixes.
- **org-config** — interview-driven setup for `.topia/org/org.md`; guardian and readiness enforce your team's rules at commit time.
- **faq** — the docs/visualization entry-point listing.

### Step 4 — Ask if they want to start

Prompt: "Want me to run one of these now? Tell me which (or none)."

If they pick one, dispatch to it via the corresponding slash command. Do NOT silently auto-run — let the user opt in.

## Output Format

```text
  ╭───────────────────────────────────────────────────────────╮
  │  Topia — your next steps                                  │
  ╰───────────────────────────────────────────────────────────╯
    [x] /topia finalize  — system-wide discipline hooks + persistent memory
    [ ] /topia onboard   — scan this repo, write CLAUDE.md + .topia/ context
    [ ] /topia doctor    — verify install health and surface any fixes
    [ ] /topia:org-config — team policy in .topia/org/org.md (commit for teams)
    [ ] /topia:faq       — list bundled docs + visualizer entry points
    [ ] /topia --help    — full command reference

  Want me to run one now? (pick by name, or "no")
```

`[x]` / `[ ]` reflect actual install state. `.dismissed` state is surfaced as a note above the menu when present.

## Calls (outbound connections)

- `topia:faq` (L3): when the user picks "show me the docs" from the menu (Step 4).
- `topia:onboard` (L3): when the user picks "set up this repo" (Step 4).
- `topia:org-config` (L2): when the user picks "configure team policy" from the menu (Step 4).
- `topia:finalize` (slash-command, not a skill but listed as an option): when the user picks system-wide setup.
- `topia:doctor` (router command): when the user picks "verify install health".

## Called By (inbound connections)

- Direct user invocation only — `/topia:tut` or `/topia tut`. This skill is the explicit re-entry for the session-start menu; nothing else dispatches it automatically.

## Constraints

1. MUST mirror the completion-detection logic in `hooks/session-start/index.cjs` exactly. If the heuristic drifts between the two, users see different status in the menu vs. the auto-shown one — confusing.
2. MUST render the menu unconditionally when invoked. The session-start hook auto-suppresses after both finalize + onboard are detected; `tut` is the explicit "I want to see it anyway" entry point and must always render.
3. MUST NOT auto-dispatch any of the menu options. Always prompt the user first.
4. MUST surface the `.topia/.dismissed` state ("menu currently dismissed in this repo") so users understand why session-start is silent if they see it.
5. MUST NOT write any state file — read-only menu render.

## Sharp Edges

| Edge | Impact | Mitigation |
|------|--------|------------|
| Heuristic drift with session-start hook | MEDIUM | Mirror `detectFinalizeNudge()` in `hooks/session-start/index.cjs` exactly. Future: extract into `hooks/lib/` so both paths share one source of truth. |
| Tutorial tracks not yet shipped (v3.2.0 = menu only) | LOW | Don't over-claim in rendered text. Mention beginner/intermediate/advanced tracks only as "coming soon" if explicitly asked. |
| `.dismissed` is per-repo, not per-machine | LOW | Surface the per-repo nature in the rendered output so users don't expect a global setting |
| Auto-dispatching a menu option without confirmation | HIGH | Never run the selected option silently — always prompt and let the user opt in |

## Done When

- The menu was rendered with check-marks reflecting actual on-disk state for finalize and onboard.
- The user was asked whether they want to run any of the listed options.
- If the user picked one, the dispatch happened.
- Skill emits `tutorial.shown`.

## Cost Profile

- **Model:** `haiku` — pure status detection + menu render.
- **Tokens:** ~400–700 output tokens for the menu + brief descriptions.
- **Latency:** sub-second (a few Bash file existence checks).
- **Side effects:** none unless the user opts into a downstream skill via Step 4.
