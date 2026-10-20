---
name: gaming-backend
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: gaming backend, multiplayer architecture, matchmaking system, game leaderboard, game state synchronization, anti-cheat system, virtual economy design, game server architecture, real-time gaming, player session management, game lobby system, competitive ranking
compose: real-time-sync
---

# Skill — Gaming Backend

## When this skill activates
This skill activates when building real-time multiplayer game servers, matchmaking systems, leaderboards, game state synchronization, anti-cheat systems, virtual economies, player session management, or competitive ranking systems.

## Mandatory actions when this skill is active

### Before writing any code
1. Design game state synchronization strategy: authoritative server architecture (server validates all actions), client-side prediction with server reconciliation, delta compression for bandwidth optimization, lag compensation (rewind time for hit detection), and tick rate optimization (60 Hz for fast-paced, 20 Hz for strategy)
2. Model matchmaking algorithm: skill-based rating (ELO/Glicko-2), queue time vs match quality tradeoff, party/premade handling (avoid unfair team compositions), region-based latency constraints (<50ms preferred), and backfill logic for mid-game joins
3. Map virtual economy flows: currency earn rates (gameplay rewards, daily login, achievements), sinks (cosmetics, upgrades, gacha), faucets (freemium currency), conversion ratios (premium to free currency), and anti-inflation mechanisms (decay, seasonal resets)

### During implementation
- Implement authoritative game server: validate all player inputs server-side (movement, attacks, item usage), reject impossible actions (speed hacks, teleportation), maintain canonical game state, broadcast state updates to clients at fixed tick rate, handle client disconnects gracefully (AI takeover or pause)
- Build matchmaking queue system: players enter queue with skill rating and region preferences, matchmaker runs periodically (every 1-5 seconds), expands search criteria over time (relax skill range after 60s, add regions after 90s), create balanced teams (sum of ratings similar), reserve game server instance, notify players
- Design leaderboard with efficient ranking: use Redis sorted sets (ZADD for score updates, ZREVRANK for rank lookup, ZREVRANGE for top-N), store composite score (wins, kills, time), implement seasonal resets with archival, handle ties deterministically (timestamp tiebreaker), support filtering by region/mode
- Implement anti-cheat detection: server-side validation (impossible speeds, impossible accuracy), statistical anomaly detection (headshot rate >90%, reaction time <50ms), behavioral fingerprinting (mouse movement patterns), report system with manual review queue, automated bans for blatant cheats with appeal process
- Build session management: player login creates session token (JWT with short expiry), heartbeat every 30s to maintain session, detect duplicates (kick old session), handle region transfers (migrate session to nearest server), graceful shutdown notifications (5 min warning before maintenance)

### After implementation
- Load test game servers under realistic conditions: spawn 1000+ concurrent bots with realistic behavior (movement, combat, chat), measure tick rate stability (should not drop below target), validate state synchronization (all clients see same events within latency bounds), identify performance bottlenecks (physics, pathfinding, network I/O)
- Validate matchmaking quality metrics: measure average queue time (should be <60s for 80th percentile), skill disparity in matches (std dev of player ratings <200), match abandonment rate (<5% pre-game), and player retention after first match
- Test anti-cheat effectiveness: attempt common exploits (speed hacks via Cheat Engine, aim bots, packet manipulation), verify server rejects invalid actions, check detection latency (should flag anomaly within 3 minutes), test false positive rate (<0.1% of legit players)

## Self-check before task completion
- [ ] Game server is authoritative: validates all player inputs, rejects impossible actions, maintains canonical state, uses lag compensation for hit detection
- [ ] Matchmaking balances skill vs queue time: expands search criteria gradually, creates balanced teams, respects region/latency constraints
- [ ] Leaderboard performs at scale: Redis sorted sets for O(log N) updates, supports millions of players, handles seasonal resets with archival
- [ ] Anti-cheat detects common exploits: speed hacks, aim bots, statistical anomalies (headshot rate, reaction time), with manual review queue
- [ ] Session management robust: heartbeat mechanism, duplicate detection, graceful disconnects, region transfer support
- [ ] Virtual economy balanced: currency earn rates tuned, inflation controls (sinks match faucets), gacha odds transparent and compliant with regulations
- [ ] Real-time performance meets targets: tick rate stable under load (60 Hz for action, 20 Hz for strategy), latency <100ms for 95th percentile players
