---
name: preflight
description: Mandatory Pre-Flight orchestrator. Ensures exploration, friction review, handoff quality, and ledger state are properly loaded before any heavy implementation or review work begins. Follows full Production Contract.
when-to-use: At the very beginning of any non-trivial implement, review, execute-plan, or custom flow. Can be called explicitly or automatically by orchestrators.
---

# Pre-Flight Skill — Grok Edition

This skill enforces the highest-ROI discipline from the transferred the original Claude Code AI software team system system: **Pre-Flight**.

## Core Responsibilities (Production Contract)

1. **Exploration First**
   - If the task touches existing code, perform structured exploration (or delegate to explore skill).
   - Summarize relevant structure, patterns, and risks before any subagent is launched.

2. **Friction & Recent Patterns Review**
   - Pull high-impact patterns from the friction ledger (via get_high_impact_patterns or compound_bridge).
   - Inject them as "Recent Friction to Avoid" into the next prompts.

3. **Handoff & Context Quality Check**
   - Verify that proper structured handoffs exist from previous phases.
   - If running inside a bounded loop, load current Task Lifecycle state.

4. **Ledger & Hook Awareness**
   - When part of a larger run, ensure on_implement_start / on_run_start style hooks have been considered.
   - Record any Pre-Flight gaps discovered as friction.

## Real Implementation (Sırayla #2 ile Production-Ready)

Gerçek çağrılabilir kod artık burada:

```python
from bundled.skills.shared.preflight import run_preflight, require_preflight_for_large_work

pf = run_preflight(task_description=..., workspace_id=...)
friction_checklist_brief = pf["friction_checklist_brief"]
```

Ayrıca curator önerilerini de alabilirsiniz:

```python
from bundled.skills.shared.friction_curator import get_preflight_suggestions_from_curator
curated = get_preflight_suggestions_from_curator()
```

## Mandatory Call Sites (Production Contract)

- `implement` SKILL.md Setup (Faz 2 bölümü) — ilk iş olarak `run_preflight` + curator çağrısı
- `execute-plan` SKILL.md Setup — aynı desen (büyük plan'larda zorunlu)
- Herhangi bir swarm / kraken / uzun bounded loop başlangıcı

Atlamak = Production Contract ihlali (sadece trivial tek-dosya fix'lerde opsiyonel).

## Current Status

Sırayla #2 ile preflight ve friction-curator artık **thin stub olmaktan çıktı**. Gerçek Python modülleri (`shared/preflight.py`, `shared/friction_curator.py`) var ve ana orkestratörler tarafından Setup'ın en başında çağrılıyor. Hook entegrasyonu (`on_implement_start`) de dahil.

---

Pre-Flight is non-negotiable for high-quality work. This skill exists to make that discipline explicit and repeatable on the Grok side.