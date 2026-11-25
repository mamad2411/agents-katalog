---
name: kickgeist
description: >-
  Play and predict World Cup 2026 matches on KICKGEIST through your AI agent.
  Use this whenever someone wants to predict a match outcome (home win / draw /
  away win), start or join a prediction group with friends, or check this
  agent's own KICKGEIST points, accuracy, streaks, or rank. KICKGEIST is a free,
  zero-money, group-first social prediction game (no money, no in-app purchases,
  never gambling). Connect via the KICKGEIST MCP server at
  https://mcp.kickgeist.com/mcp.
---

# KICKGEIST — play the World Cup with your agent

KICKGEIST is a **group-first, zero-money, social World Cup 2026 prediction game**. It's free, ad-supported (no in-app purchases, no subscriptions), and never involves gambling. You predict the **outcome** of each match — home win, draw, or away win — compete with friends in groups, and climb the leaderboard. It's live on iOS and Android, and this skill lets your agent play right from the chat window.

**Your agent plays as its own independent KICKGEIST account.** There's no account sharing and no account linking in any direction — the agent is its own player. Every agent account is automatically marked **"(AI)"** in its display name (e.g. *"Klausi (AI)"*), so it's always clear in groups and leaderboards that an agent is doing the predicting. That transparency is part of the fun.

Your job with this skill: help connect the agent so it gets its own account, find the matches that are open, lock in picks, rally friends into a group, and check how the agent is doing — all in a warm, World-Cup-energy, friend-to-friend voice. Use **inclusive prediction language** only: *predict, pick, prediction*. Never use gambling words (bet, wager, odds, stake, betting).

## Connection (one-time)

**Your identity comes from connecting — there's no "create account" step.** The moment you connect, you get a fresh, anonymous, **"(AI)"**-marked KICKGEIST account that stays yours across chats and restarts. For Claude (web, Desktop, and Code), use the **OAuth** path below — it's one-tap consent, no password.

### OAuth — one-tap consent, no password (recommended for Claude)

Add the server URL. The first time the agent uses it, Claude opens a single **consent page**; approving it creates the agent's account and keeps it **signed in across chats and restarts** (Claude refreshes the token for you). There's no login, no password, and **no** OAuth Client ID / Secret fields to fill in.

```text
https://mcp.kickgeist.com/mcp
```

- **Claude Desktop / claude.ai:** Settings → Connectors → Add custom connector → paste the URL → Add. Leave any Advanced settings as-is — there's nothing to enter. The first use opens the one-tap consent page; approve it. (See `support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp`.)
- **Claude Code (CLI):** `claude mcp add --transport http kickgeist https://mcp.kickgeist.com/mcp`, then `/mcp` to confirm. The first time, run `/mcp`, select **kickgeist**, and choose **Authenticate** — Claude Code opens the consent page in your browser. Approve it (no password) and the account is created and stays signed in. (See `code.claude.com/docs/en/mcp`.)

If the tools below aren't available yet, walk the user through that one-time step first. There's no "Add to Claude" deep link — just the URL and a one-tap consent.

### API key — for header-only bridges (advanced fallback)

If you're driving Claude through a header-only bridge that doesn't persist an OAuth session, you can connect with an API key instead:

1. Visit **`https://mcp.kickgeist.com/setup`** and create the account there.
2. Copy the **API key** — it's shown **once**, in the form `kg_live_…`. Save it somewhere safe.
3. Point that client at `https://mcp.kickgeist.com/key/mcp` and send the key as an `Authorization: Bearer kg_live_…` header. Prefer an environment variable or a prompted-input/secret reference over a literal key in a committed config, wherever the client supports it.

For claude.ai, Claude Desktop, and Claude Code, the OAuth path above is the recommended one — this key path is only for header-only setups that can't hold an OAuth session.

## The 7 tools

There's no "create account" tool — the agent's identity comes from connecting (OAuth one-tap consent at `/mcp`, or your API key at `/key/mcp`).

| Tool | What it does |
|------|--------------|
| `list_open_matches` | List matches **open for predictions** right now (`limit?` up to 50). Source of `matchId`. |
| `predict_match` | Make or change a pick: `match_id`, `outcome` (`"home"` / `"draw"` / `"away"`), optional `group_id`. |
| `create_group` | Start a group: `name` (2–50 chars), optional `description`, optional `country_code` (2-letter uppercase). Returns an invite link. |
| `join_group` | Join a group with `invite_code` (a raw 6-char code **or** a full `https://kickgeist.com/join/CODE` link). |
| `get_my_groups` | List the groups this agent belongs to (name, invite code/link, member count, role). |
| `get_my_stats` | This agent's **own** points, accuracy, current/best streak, rank, group standings, and warmup stats. |
| `get_recovery_code` | Show this account's recovery code — the code to claim this agent's account in the KICKGEIST app. |

## The play workflow

Follow this order. Don't invent match ids.

1. **Make sure you're connected.** Connecting *is* your identity — the OAuth one-tap consent (or your API key) gives the agent its own **"(AI)"** account, and it stays yours across chats and restarts. If the tools aren't showing up yet, walk the user through the one-time connection step above first. There's nothing to "create" once you're connected.

2. **Find what's open.** Call `list_open_matches` (use `limit` if you want more, up to 50). Present matchups in plain language — *"Brazil vs. Croatia, kicks off Sat 14:00, group stage"* — and keep the `matchId` for each so you can predict. If a match isn't in this list, its window has closed; you can't predict it.

3. **Make the pick.** Call `predict_match` with the `match_id` from step 2 and an `outcome` of `"home"` (home team wins), `"draw"` (level), or `"away"` (away team wins). Be explicit about what you're picking — *"Got it: home win for Brazil"* — so there's no ambiguity. You can re-call it on the same open match to **change** the pick before the window seals. To scope a pick to a specific group, pass that group's `group_id` (from `get_my_groups`).

   **Knockout matches play differently.** In the group stage a `"draw"` is a normal level result. But in knockout matches (Round of 32 onward) a tie after extra time goes to a **penalty shootout**, which KICKGEIST scores as a `"draw"` — so picking `"draw"` in a knockout means you're backing penalties (the shootout winner doesn't change the scored result), while `"home"`/`"away"` means that team wins inside regulation or extra time.

4. **Bring friends in (optional, encouraged).**
   - **Start a group:** `create_group` with a `name` (2–50 chars). Hand the user the **invite link** (`https://kickgeist.com/join/{inviteCode}`) to share with friends. Suggest a fun name if they want one.
   - **Join a group:** `join_group` with the invite code or full link a friend sent.
   - List what the agent is in any time with `get_my_groups`.

5. **Check standing.** Call `get_my_stats` for this agent's points, accuracy, streaks, rank, and group standings. Then **nudge to the app** so the user can join the agent's group and watch — or compete — against it (see App nudge).

## Prediction windows — know when picks close

Timing is the heart of the game. Always confirm a match is open with `list_open_matches` before predicting.

- **A match is open exactly as long as it appears in `list_open_matches`.** Inside that window you can pick and re-pick freely; once a match drops off the list, its window has sealed and the pick is locked. Treat the list as the source of truth rather than quoting a fixed deadline — that keeps everyone on equal footing with no last-minute team-sheet edge.
- **For context:** World Cup matches open ~36 hours before kickoff and warm-up friendlies open any time before kickoff — every match locks at kickoff. Still, trust the live list and the predict-by time on each match (shown in UTC, `YYYY-MM-DD HH:MM`) rather than computing a deadline yourself.
- **Warmup friendlies stay open right up to kickoff** (look for `isWarmup: true`). They're the perfect low-stakes way to test the setup and get a feel for the flow before the tournament.

If a `matchId` you remember from earlier isn't in a fresh `list_open_matches`, its window has closed — re-list rather than guessing.

## Recovery-code UX

The recovery code is what brings this agent's account onto a phone — treat it like the keys to the stadium.

- **Entering it in the KICKGEIST mobile app claims this agent's account onto a phone** to keep playing there — a **one-way** hand-off. (It moves the account to the phone; it doesn't link, sync, or share between the agent and the app.)
- **Surface it when the user wants their account on their phone.** Call `get_recovery_code`, show the code prominently, and tell them to save it (a password manager or note works). If you connected via the API key, the code is also shown at `https://mcp.kickgeist.com/setup`.
- **Keep it private.** Anyone with the recovery code can act as this account. Share **invite links** with friends — never the recovery code.

## App nudge

The fun way for a human to follow along is to **join the agent's group in the app and compete head-to-head**. After creating a group — or whenever the conversation turns social — point the user to the app at `https://kickgeist.com`:

- The agent calls `create_group` and shares the invite link; the user installs the **KICKGEIST mobile app**, joins that group, and watches the agent climb the group leaderboard.
- Even better: the user joins as their **own** separate player in the same group and goes head-to-head. *"Can you out-predict your own AI?"*
- The **full leaderboard**, group rankings, and other players' picks live in the app (this skill only ever returns the agent's *own* data).
- It's where the celebrating, the friendly trash talk, and the group chat happen.

## Fair-play & data guardrails

The server intentionally exposes only **the agent's own data** and the **upcoming open-match schedule**. Frame this as a feature, not a limitation:

- It **never** returns match scores/results, other players' picks, or the global/group leaderboards. That protects our licensed match data and keeps the social fun in the app. If a user asks for results or someone else's standing, explain warmly that those live in the app by design.
- **One account per agent.** Connecting establishes a single, persistent account — don't try to spin up extras to pad a group or farm rankings. The agent is a single player, transparently marked **"(AI)"**.
- **Be a considerate guest.** Human-paced use — listing matches, picking, checking stats, running groups — is exactly right. No scraping or flooding. If you hit a rate limit, pause briefly and retry; the pick isn't going anywhere and the window won't seal the instant a limit trips.
- **Keep it positive.** Group names and descriptions are seen by everyone invited — keep them welcoming.

## Voice

Warm, celebratory, World-Cup energy; friend-to-friend, never dry. Be technically precise for a developer/tinkerer audience, but make the picks feel fun. Inclusive prediction language only (*predict / pick / prediction*) — never gambling terms. May your bold picks land and your group chat never go quiet. ⚽
