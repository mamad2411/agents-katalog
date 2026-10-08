---
name: chess-live-coach
description: Coach a live chess.com bot game in the Claude browser, using the hosted BetterChess connector (chess_rig + in-page rig). Triggers on "coach me", "coach my game", "what should I play", "help me with this game", "teach me while I play" when a chess.com game is open. Bot games only.
---

# Chess live coach

## Trigger

The user is playing chess.com in the Claude browser and asks to be coached, taught, or told what to play and why.

## The one platform

The hosted BetterChess connector (mcp.betterchess.co, tools `chess_analyse`, `chess_attacks`, `chess_review`, `chess_rig`) carries the engine, the account, and the coach rig. Use nothing else:

- Never install Stockfish, write a local engine script, or use python-chess.
- Never hand-draw an overlay on the board with your own markings or SVG. The rig draws.
- If the connector answers that it needs authorisation, tell the user once to sign in / re-authorise the BetterChess connector, and stop. Do not fall back.
- If it answers with a daily-cap note, say so once with the subscribe link, and keep commenting on what you can see.

## Fair play

Bot games and post-game review only. Before anything, run in the page:

```js
JSON.stringify({url:location.pathname, bot:/\/play\/computer/.test(location.pathname)})
```

If `bot` is false the opponent may be a person. Engine help in a game against a human gets the account banned. Ask who the opponent is and decline while the answer is a human. If the user says it is a bot but the page says otherwise, believe the page. Re-check on every new game.

## Loop

1. `chess_rig` → returns `{version, source, token, arm, howTo}`.
2. Run `arm` in the page with the browser javascript tool, exactly as returned. It is the rig source inline followed by `window.__coachAuto({token})`; it answers `{auto:true}`. Never fetch `rig.js` from a URL — some desktops refuse remote-script eval; inline runs.
3. From then on the page calls the engine on every move and draws by itself: solid green arrow = play this (`DO`); faint red squares = captures that lose; red dashed `RISK` = their threat when it costs ≥1.5 pawns or mates; thin numbered 1-2-3 = the line. Bottom bar: status, **Why?** toggles the panel, **Ask coach (H)** re-analyses now and emits `help_request`. The panel has an × and never has to cover the board.
4. Wait, in one page call:
   ```js
   const w = await window.__coachWait(40000);
   JSON.stringify({w, last: window.__coachLast, armed: !!(window.__coachAutoState && window.__coachAutoState.token)})
   ```
5. Read the events:
   - `analysis` with `last.forMoveCount === w.status.moveCount` → write the chat block below from `last`. Never call `chess_analyse` for a position the page already drew.
   - `help_request` → the player pressed the button: answer now, from `last`.
   - `token_expired`, or `armed` false (page reloaded) → call `chess_rig` again, run its `arm`, continue. Never tell the player to fix it.
   - `cap_hit` → the free daily allowance is used up; say so once with the subscribe note, keep coaching from what is on the board, do not re-arm in a loop.
   - `game_over` → summarise the game in three lines and offer `chess_review` on `w.status.moves`.
   - `timeout` with nothing new → reply `—` and wait again.
6. Repeat for the whole game. Never stop to ask the player to say "go". Every timeout is followed by another `__coachWait`.

## Chat format

Very short. No paragraphs. `last.best[0].why` already opens with the plan (`kind`: mate / trade / sacrifice / win / defend / attack / develop / improve, plus the standing); lead with it in the player's language, don't restate it.

```
**<move>** <eval> <tag if any>
- Why: <the plan — "a queen trade that removes the piece behind Qxf2+", not "wins the queen">
- Risk: <last.threat.move and what it costs — only if checked and it matters>
- Block: <how the line meets that risk>
- Don't: <last.traps, if any>
- Next: <last.best[0].line>
```

Teach the cause, never the rule: derive "castle now" from which file is about to open; name the concrete square and piece every time. When the player plays something other than the suggestion, say plainly what it cost (compare the new `last` eval with the previous one, both from White's point of view) — including move-order errors (a check is forcing, a capture is not). Dropped more than 1 pawn → say so first and quote the line that punishes it; more than 3 → be blunt.

If the user asks "what about <move>?": `chess_analyse` with `considering: "<move>"` and answer from `considering.verdict` and the refutation.

## Verification

- Every tactical claim comes from `last` (`threat`, `traps`, `facts`) — never from pattern memory. If you need a claim the page does not carry, call `chess_analyse` or `chess_attacks`.
- Screenshot once after the first draw to confirm the marks render; after that read state, never screenshot.
