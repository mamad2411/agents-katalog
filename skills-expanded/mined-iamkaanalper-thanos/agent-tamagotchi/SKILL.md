---
name: agent-tamagotchi
description: Terminal pet that lives in status/feedback. 12 species, 5 stats (DEBUGGING, PATIENCE, CHAOS, WISDOM, SPEED). Reacts to workflow - happy on tests pass, sad on builds fail, excited in swarm. Grok adaptation.
when-to-use: For motivation, gamification of workflow, long sessions, team fun. Reacts to our swarm, hooks, compound, success/failure signals.
---

# Agent Tamagotchi (Grok Adaptation)

Virtual pet for the .grok/ workflow. Evolves with your (and agents') coding habits. Ties into our hooks, friction, compound, swarm for real signals.

## Species (12, deterministic from user or project hash)
Same as original: Axolotl, Capybara, Ghost, Mushroom, Robot, Cat, Dragon, Owl, Fox, Penguin, Slime, Phoenix.

## Stats (5 dimensions, 0-100)
- DEBUGGING: bugs fixed, errors resolved (tie to sleuth/coroner/verifier success + friction resolution)
- PATIENCE: long/complex tasks (tie to kraken big features, multi-round ledger)
- CHAOS: parallel agents, swarm mode (tie to our swarm orchestrator + multiple spawn)
- WISDOM: arch decisions, plans (tie to architect + matrix + compound promotion)
- SPEED: fast fixes, first-try (tie to build-error-resolver, small implementer wins)

## Mood
Happy (tests pass, compound success), Excited (swarm), Sad (build fail, escalation), etc.

## Grok Integration (Our Strengths)
- **Hooks**: on_run_completion, on_bounded_loop_end, on_swarm_phase, on_draft_applied → update stats/mood.
- **Swarm**: big swarm run = CHAOS/EXCITED boost.
- **Compound / Self-Learner**: wisdom from promotions.
- **Verifier / Friction**: debugging + success/failure.
- **Ledger**: patience from long bounded loops.
- Status: Can hook into hook-health.jsonl or compound-friction for real data.
- Display: In responses, or future status (like " [Phoenix] Lv.4 WISDOM:78 excited after successful compound apply").

## Storage
~/.grok/tamagotchi.json (simple, like our compound-friction.jsonl and hook-health).

## Status
Functional: ~/.grok/tamagotchi/tamagotchi.json created (example state). Auto updates via on_tamagotchi_update hook (madde-3). Stats/mood logic in skill description + hook handler.

Simple update snippet (for agents/hooks):

```python
import json
from pathlib import Path
def update_tamagotchi(event_type, details=None, session_context=""):
    f = Path.home() / ".grok" / "tamagotchi" / "tamagotchi.json"
    state = json.loads(f.read_text()) if f.exists() else {"species":"phoenix", "level":1, "stats":{}}
    # map event to stat boost
    if "swarm" in event_type: state["stats"]["chaos"] = min(100, state["stats"].get("chaos",50)+10)
    if "pass" in event_type or "success" in event_type: state["stats"]["debugging"] = min(100, state["stats"].get("debugging",50)+5)
    if "fail" in event_type: state["stats"]["patience"] = max(0, state["stats"].get("patience",50)-5)
    state["mood"] = "excited" if "swarm" in event_type else "focused"
    state["lastFed"] = "now"
    f.write_text(json.dumps(state, indent=2))
    return state
```

Original in ~/.claude/skills/agent-tamagotchi/ for reference (read-only).

This adds the gamification/motivation layer on top of our disciplined core.

See .grok/100-PERCENT-COMPLETE.md and adaptation-kit for how this fits the focused transfer.