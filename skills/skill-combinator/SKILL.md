---
name: skill-combinator
description: WAJIB OTOMATIS dipakai tanpa slash saat 2+ skill dipakai bareng. Auto-suggest stacking skill yang historically sukses via skill-combinations.json. Trigger: skill stacking, kombinasi skill, paired with, golden combo.
version: 1.0.0
tags: [combinator, stacking, auto-suggest]
---

# skill-combinator (PON40) — Automatic Skill Stacking Engine

## Rule PON40: SKILL COMBINATOR

When a skill is invoked, auto-suggest skill combinations that historically produced better results.

### Mechanism:
1. **Track pairs**: When 2+ skills used together, log to `skill-combinations.json`
2. **Success scoring**: If combined result efficacy >70%, boost pair score
3. **Auto-suggest**: When skill X is loaded, check pairs containing X
4. **Threshold**: Only suggest pairs with success_rate >0.6 AND count >=2
5. **Token cost**: Max 1 suggestion per skill load, max 200 chars in suggestion

### API Integration:
- `POST /combination/log` — Record a skill combination result
- `GET /combinations?skill=X` — Get suggestions for skill X
- Auto-prune pairs with count=1 and success_rate <0.3 after 30 days

### Auto-Tune (after 20 runs):
- Sort all pairs by success_rate × sqrt(count)
- Top 10 pairs → "golden combos" cached in Memory vault
- When user request matches golden combo trigger, auto-load both skills

### Combination Scoring Formula:
```
pair_score = success_rate × log(count + 1) × recency_bonus
recency_bonus = 1.0 if last_used <7d, else 0.5
```

### Guard Rules:
- NEVER auto-load 2 skills simultaneously (token budget)
- SUGGEST only, let user/LLM decide
- If thermal profile = HOT, skip suggestions (save tokens)
- If thermal profile = CRITICAL, no skills loaded at all

### Integration with PON35 (Amplifier):
- After amplifier runs efficacy scoring (Step 7), if score >70 AND 2+ skills used:
  → Log combination to API
- After amplifier self-heal (Step 8), if score <50:
  → Log as failed combination (success=false)

### Integration with PON39 (Stub Generator):
- If skill body >2KB loaded, check combinations BEFORE loading
- Suggestion appears as: "💡 Often paired with: [skillY] (85% success, 12 runs)"
  (but without emoji — user preference noted)
- Format: "Often paired with: skillY (85% success, 12 runs)"

### File Locations:
- Combinations log: `~/.agents/skill-combinations.json`
- API endpoint: `http://127.0.0.1:2725/combinations?skill=X`
- Golden combos: cached in Memory vault after 20+ runs
