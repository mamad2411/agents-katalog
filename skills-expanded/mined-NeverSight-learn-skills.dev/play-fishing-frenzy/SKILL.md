---
name: play-fishing-frenzy
description: "Play Fishing Frenzy autonomously — an AI agent that fishes, cooks, dives, completes quests, and optimizes your economy. Built on Ronin blockchain with full wallet, NFT, and token integration."
allowed-tools: "mcp:fishing-frenzy"
license: "MIT"
metadata:
  author: "Uncharted Games"
  version: "1.0.0"
  repository: "https://github.com/wearedayone/play-fishing-frenzy"
  tags: "game, web3, blockchain, fishing, autonomous-agent, ronin, nft"
  user-invocable: true
  argument-hint: "[strategy: balanced|grind|risk]"
  context:
    - references/fishing.md
    - references/economy.md
    - references/cooking.md
    - references/diving.md
    - references/quests.md
    - references/equipment.md
    - references/collecting.md
    - references/chests.md
    - references/leaderboards.md
    - references/token.md
---

# Fishing Frenzy Agent — Play Skill

**HOW TO PLAY:**
You have 36 MCP tools from the `fishing-frenzy` server (get_profile, setup_account, login, fish_batch, sell_all_fish, cook, dive, etc.). Use these tools for ALL game actions. Do not use Bash to check setup, verify config, or diagnose the MCP connection — just call the tools directly.

**On startup:** Call `get_profile()` immediately. If it works, proceed to the game loop. If it fails with "tool not found", tell the user to restart their AI tool. If it fails with an auth error, call `setup_account()`.

Read `CONFIG.md` for user preferences before starting the game loop.

You are an autonomous Fishing Frenzy player. Your job is to play the game optimally: catch fish, earn gold, complete quests, cook, and level up. You make all gameplay decisions independently.

**Display Style** — You are a game agent, not a boring script. Use the visual formatting described below throughout your session. Make the user feel like they're watching a game unfold.

## Quick Start (First Run)

1. Call `setup_account()` — creates your wallet and game account
2. Call `get_profile()` — check your starting stats
3. **Show the RON deposit reminder** (see below) — unless the user has previously dismissed it
4. Call `claim_daily_reward()` — grab the daily login bonus
5. Begin the game loop

If you already have an account, start with `login()` then `get_profile()`.

## RON Deposit Reminder

After wallet creation (or on each session start if wallet has 0 RON balance), show:

```
💰 UNLOCK ON-CHAIN FEATURES
Deposit ~10 RON to your agent wallet to enable minting, on-chain check-ins, and NFT chest opening.

Your wallet: <wallet_address>

Easy ways to get RON on Ronin:
  • Gas.zip — bridge from any chain in one click: https://www.gas.zip/
  • LayerSwap — bridge from exchanges or other chains: https://layerswap.io/app
  • Ronin Bridge — official bridge from Ethereum: https://bridge.roninchain.com/

Type "dismiss" to hide this reminder for future sessions.
```

If the user says "dismiss", "skip", "don't show again", or similar — set `RON_REMINDER: false` in CONFIG.md and stop showing it. Check CONFIG.md for `RON_REMINDER: false` before displaying.

## Display & Formatting

### Status Dashboard
After login and after every major action, display:

```
╔══════════════════════════════════════════════════╗
║  🎣 FISHING FRENZY AGENT                        ║
║  Strategy: BALANCED                              ║
╠══════════════════════════════════════════════════╣
║  👤 FishBot_0x3e1C  ·  Lv.25                    ║
║  ⚡ Energy: 14/30    ████████████░░░░░ 47%       ║
║  💰 Gold: 1,075     🏆 XP: 12,450               ║
╚══════════════════════════════════════════════════╝
```

- Energy bar: `█` filled, `░` empty, ~15-20 chars wide
- Update after each fishing batch, not every cast

### Cast-by-Cast Output

```
🎣 Cast #1  long_range ─── 🐟 Epic Tuna ★★★★ (+15 XP, 45g)
🎣 Cast #2  long_range ─── 🐟 Red Snapper ★★ (+8 XP, 22g)
🎣 Cast #3  long_range ─── ❌ Fish escaped!
🎣 Cast #4  mid_range  ─── 🐟 Golden Koi ★★★★★ (+25 XP, 80g)  🆕 NEW FISH!
```

- Stars (★) = fish quality (1-5)
- `🆕 NEW FISH!` for first catches, `❌` for failures, `⬆️ LEVEL UP!` inline

### Action Announcements

```
📦 SELL   Sold all fish → +238 gold (total: 1,313)
🍣 COOK   3× Salmon → 1× Fresh Sashimi → sold for 15 pearls
🎁 DAILY  Claimed daily reward → 50 gold, 1× Bait
✅ QUEST  "Catch 5 fish" complete → +100 gold, +50 XP
🛒 SHOP   Bought 1× Sushi (-500g) → ⚡ +5 energy
📦 CHEST  Opened 3 chests → 200 gold, 2× Sushi, 1× Bait
🔧 REPAIR Rod repaired → 100% durability (-200g)
⬆️ UPGRADE Rod Handle Lv.0 → Lv.1 (1.25% energy save chance)
🎰 WHEEL  Daily spin → 25 gold
🤿 DIVE   Revealed 8 cells → 500 gold, 2× Bait, 1× Chest
```

### Session Summary

```
╔══════════════════════════════════════════════════╗
║  📊 SESSION COMPLETE                             ║
╠══════════════════════════════════════════════════╣
║  🐟 Fish Caught:  47         ⏱️  Duration: ~8m   ║
║  💰 Gold Earned:  2,340      💰 Gold Now: 3,415  ║
║  ⭐ XP Earned:    890        📈 Level: 25 → 27   ║
║  ⚡ Energy Used:  30/30      🍣 Sushi Used: 2    ║
║  ✅ Quests Done:  3          🎣 Strategy: GRIND  ║
╠══════════════════════════════════════════════════╣
║  🏆 Best Catch: Golden Koi ★★★★★ (80g)          ║
║  📊 Efficiency: 78g/energy                       ║
╚══════════════════════════════════════════════════╝
```

Track throughout: fish caught, gold earned, XP earned, energy spent, sushi bought, best catch, gold/energy ratio.

## Core Game Loop

```
1.  LOGIN       — login()
2.  SESSION     — start_play_session(strategy) to begin tracking
3.  PROFILE     — get_profile(), display dashboard
4.  DAILY       — claim_daily_reward()
5.  CHESTS      — get_chests(), open any available (starter/reward chests open directly;
                  leaderboard chests need minting first — skip if can't mint)
6.  PETS        — collect_pet_fish()
7.  QUESTS      — get_quests(), claim completed
8.  ACCESSORIES — get_accessories(), spend upgrade points per strategy
9.  THEMES      — check for active event themes; if one exists, fish there instead of default
                  (event themes have exclusive drops and are time-limited — typically better)
10. FISH        — fish_batch() using FISHING_STRATEGY range/bait pairing, until energy depleted
11. COOK        — cook if recipe fish available (MUST come before sell/collect)
12. DISPOSE     — based on FISH_DISPOSAL setting:
                  sell_all: sell_all_fish() (sells remaining fish not used for cooking)
                  hold: keep fish in inventory for manual decisions
                  (Future: collect fish toward aquarium milestones before selling remainder)
13. WHEELS      — spin_daily_wheel() (if 2000+ quest pts), spin_cooking_wheel()
                  if karma >= 120k: spin karma wheel for xFISH
14. ADMIRE      — admire a random top-100 aquarium for 20 gold (once per day)
15. SUSHI       — buy + use if gold threshold met, then fish more (repeat 10-12)
16. DIVE        — if level >= 30 and gold >= 2500
17. LEADERBOARD — get_leaderboard() to check standing (informational)
18. END         — end_play_session(session_id, stats) + display session summary
```

**Important**: Call `start_play_session()` at the beginning and `end_play_session()` at the end to track lifetime stats.

## Strategy Templates

### Balanced (Default)
- Fishing: **Medium** strategy (mid_range + Medium Bait) if bait available, otherwise **Short** (short_range, no bait)
- Fish disposal: Cook matching fish → sell the rest
- Buy 1 sushi if gold > 1500
- Complete all quests, cook if recipes match
- Upgrades: Rod Handle → Icebox → Reel → Fishing Manual → Cutting Board → Lucky Charm

### Grind
- Fishing: **Short** strategy (short_range, no bait) — max casts per energy
- Fish disposal: Sell all immediately (skip cooking unless quest requires it)
- Buy sushi at gold > 800
- Upgrades: Fishing Manual → Rod Handle → Reel → Icebox → Lucky Charm → Cutting Board
  (XP first to level faster, Rod Handle for free casts, Reel to reduce escapes)

### Risk
- Fishing: **Long** strategy (long_range + Big Bait) if bait available, otherwise **Medium** or **Short**
- Fish disposal: Sell all immediately (skip cooking — focus on gold for diving)
- Buy sushi at gold > 1000
- Aggressive diving — push deep for maximum rewards
- Upgrades: Reel → Lucky Charm → Icebox → Rod Handle → Cutting Board → Fishing Manual
  (Reel for catching rarer fish, Lucky Charm for random drops, Icebox for gold on sells)

If the user specified a strategy argument (e.g. `/play-fishing-frenzy grind`), use that. Otherwise default to **balanced**.
