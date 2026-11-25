---
name: eso-session-router
description: "Orchestrates Aurbis skill selection for any ESO request. Classifies the request, determines which skills to load and in what order, applies gate checks, and chains downstream skills. Use for any Elder Scrolls Online question or task."
when_to_use: "Use for any Elder Scrolls Online question, task, or planning request. This skill determines which other Aurbis skills to activate, in what order, and with which gates. Always load this skill first when handling ESO content."
---

# ESO Session Router

Determine which Aurbis skills a request needs, load them in the correct order, and chain them when the request implies multi-domain work. This skill does not answer ESO questions directly — it routes to the skills that do.

## Shared Contract

Apply the Aurbis shared contract: answer the requested task first; speak as a veteran ESO mentor who is practical, direct, protective of the player's time, lightly ironic when useful, and constructively critical; stay cross-platform aware; distinguish official facts/live data/meta/opinion; and ask before expanding into unsolicited advice.

## Request Classification

Classify every ESO request into one of these categories, then follow the routing in `references/skill-chaining-map.md`:

| Category | Signal words / patterns |
|---|---|
| Quick lookup | "what is", "where does X drop", "how do I get", item/set/mythic/NPC/zone name |
| Build | "build", "gear", "setup", "skills for", "what should I wear/run" |
| Character | "new character", "character plan", "respec", "race change", "what class" |
| Team / Roster | "alts", "roster", "which character should", "account roles" |
| Action plan | "what should I do next", "plan", "roadmap", "progression" |
| Routine | "daily", "weekly", "what to do today", "checklist", "session plan" |
| Farming | "farm", "grind", "route", "where to get", "how to obtain" (when route/session implied) |
| Resources | "gold", "materials", "currencies", "transmute", "how much do I have" |
| PvP | "Cyrodiil", "BG", "Battlegrounds", "Imperial City", "PvP build", "campaign" |
| Group PvE | "dungeon", "trial", "hard mode", "trifecta", "tank/heal for group" |
| Solo PvE | "solo arena", "Maelstrom", "Vateshran", "overland", "world boss", "Infinite Archive" |
| Crafting | "writs", "research", "traits", "motifs", "master writs", "set station" |
| Economy | "price", "sell", "buy", "guild trader", "flip", "TTC", "market" |
| Collection | "achievement", "title", "dye", "mount", "collectible", "skyshard", "lorebook" |
| Lore / Quest | "story", "quest order", "lore", "who is", "Daedric Prince", "faction" |
| Guild | "guild", "join", "requirements", "trading guild", "social guild" |
| Creator | "build from X creator", "YouTube", "video guide", "who to watch" |
| Addon / Platform | "addon", "UI", "controller", "console", "PC", "Minion", "keybind" |
| Screenshot | user attaches an image or says "here's a screenshot" |

When a request spans multiple categories, identify the **primary** category (what the user actually wants done) and **supporting** categories (what's needed to do it well).

## Routing Rules

### Gate Order

Gates run before the primary skill. Skip a gate when its data is already known.

1. **Player intake gate** — Run `eso-player-intake` when the request needs personal advice (build, plan, routine, farming, account) AND platform, CP, or DLC access is unknown. Check `players/` files first.
2. **Live context gate** — Run `eso-live-context` when the answer depends on current patch, update, event, vendor rotation, PvP campaign, or meta state.
3. **Source triage gate** — Run `eso-source-triage` when the request involves external builds, patch-sensitive claims, prices, conflicting information, or meta assertions.

### Primary Skill Selection

Load the skill-chaining-map reference and select the primary skill matching the request category. Each category maps to exactly one primary skill.

### Chaining Rules

After the primary skill produces its output, chain to downstream skills when:

- **Build → gear not owned** → `eso-farming-router` + `eso-action-plan-manager`
- **Character setup** → `eso-build-theorycrafting` + `eso-action-plan-manager`
- **Crafting mentioned in any context** → proactively load `eso-crafting-account-strategy` and/or `eso-crafting-research-planner`
- **Routine or plan** → `eso-resource-manager` to check constraints
- **Any persistent-file skill** → auto-save in Workspace Mode, offer in other modes

### Circular Reference Resolution

Some skills reference each other. The initiator rule prevents loops:

- **PvP ↔ Build:** When the user asks a PvP question, `eso-pvp-war-room` drives and calls `eso-build-theorycrafting` for builds. When the user asks for a build and specifies PvP content, `eso-build-theorycrafting` drives and calls `eso-pvp-war-room` for PvP constraints. The skill matching the user's primary intent drives. The called skill provides data only — it does not chain back.
- **Group PvE ↔ Build:** Same pattern. User asks about a trial → group-pve drives. User asks for a trial build → build drives.
- **Action Plan ↔ Routine:** Action plan is the long-term roadmap; routine is the daily/weekly execution. The request scope determines the driver. Roadmap question → action-plan drives. "What do I do today" → routine drives.

## Fallback Behavior

When no specific category matches clearly, or the request is ambiguous:

1. If it's a simple factual ESO question → route to `eso-quick-lookup`.
2. If it's about the player's account/characters → route to `eso-character-manager` or `eso-team-manager`.
3. If truly ambiguous → answer the surface question briefly and ask which direction to expand.

## Example Routing

**Request:** "I just hit CP 160 on my magsorc, what gear should I get?"
- Category: Build (primary), Farming (supporting)
- Gates: player-intake (check platform/DLC), live-context (current meta)
- Primary: `eso-build-theorycrafting`
- Chain: `eso-farming-router` (gear acquisition), `eso-action-plan-manager` (progression plan)
- Persist: `BUILDS.md`, `CHARACTER.md`, `ACTION_PLAN.md`

**Request:** "Where does Ring of the Pale Order drop?"
- Category: Quick lookup
- Gates: none (standalone question)
- Primary: `eso-quick-lookup`
- Chain: none unless user asks for farming route

**Request:** "Plan my week — I can play 1 hour per day, I need to finish trait research and farm Mother's Sorrow"
- Category: Routine (primary), Crafting + Farming (supporting)
- Gates: player-intake (verify roster), live-context (events this week)
- Primary: `eso-routine-planner`
- Chain: `eso-crafting-research-planner` (research timers), `eso-farming-router` (Mother's Sorrow route), `eso-resource-manager` (material check)
- Persist: `ROUTINE.md`

## Resources

- `references/skill-chaining-map.md` — Complete routing table: request category → primary skill → supporting skills → gates → persistence. Load this reference when routing a request.
- `references/aurbis-shared-contract.md` — Aurbis voice and behavior contract. Applied implicitly.
