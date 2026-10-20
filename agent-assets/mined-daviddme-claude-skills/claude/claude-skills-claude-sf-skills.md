# SF-Skills — agent instructions

This folder gives Claude (or any agent that reads SKILL.md) a complete
StrategyFactory command center: scan thousands of strategies, score them
multiple ways, deploy the winners, prune the dying ones, run continuous
loops in the background.

All API calls go through `sf_client.py` (shared HTTP + scoring lib).
Credentials come from environment variables — never the CLI, never logs.

## Credentials

```
SF_API_KEY     — x-user-api-key header
SF_API_SECRET  — x-user-api-secret header
```

Create them at <https://app.strategyfactory.ai/settings>. Keep them in
shell env or a `.env` file that's gitignored.

## Skills in this suite

| Skill | Reads | Writes | Purpose |
| ----- | ----- | ------ | ------- |
| [`sf-hot-scan`](sf-hot-scan/SKILL.md)       | HOT strategies | – | Raw scan with filters |
| [`sf-best-pick`](sf-best-pick/SKILL.md)     | HOT strategies | – | Multi-factor composite top picks |
| [`sf-profit-factor`](sf-profit-factor/SKILL.md) | HOT strategies | – | High-PF specialists |
| [`sf-market-fit`](sf-market-fit/SKILL.md)   | HOT strategies | – | Working right now (7d/30d momentum) |
| [`sf-edge-watch`](sf-edge-watch/SKILL.md)   | strategy, bots | – | Edge-decay diagnostic |
| [`sf-portfolio`](sf-portfolio/SKILL.md)     | exchanges, balances, bots, positions | – | One-screen account view |
| [`sf-deploy`](sf-deploy/SKILL.md)           | – | `POST /bots` | Create a copy bot |
| [`sf-prune`](sf-prune/SKILL.md)             | bots, strategies | `PATCH /bots/:id` (with `--apply`) | Pause decaying bots |
| [`sf-rebalance`](sf-rebalance/SKILL.md)     | bots, strategies, HOT | `PATCH /bots/:id` (with `--apply`) | Prune + propose replacements |
| [`sf-loop-hunter`](sf-loop-hunter/SKILL.md) | HOT strategies | local state | Recurring discovery — emit deltas |
| [`sf-loop-pruner`](sf-loop-pruner/SKILL.md) | bots, strategies | local state, `PATCH /bots/:id` (with `--apply`) | Recurring health watch |

## Recommended workflows

### Pick and deploy (operator-driven)

```
python sf-best-pick/pick.py --top 5 --explain
# (user picks one)
python sf-portfolio/portfolio.py              # find exchange id
python sf-deploy/deploy.py --strategy <slug> --exchange <id> \
  --position percentage --amount 3 --leverage 10 --dry-run
# (review, then drop --dry-run)
```

### Diagnose before deploying

```
python sf-edge-watch/watch.py <slug-or-id>
```

### Periodic housekeeping

```
python sf-prune/prune.py                       # dry-run audit
python sf-prune/prune.py --apply               # pause dying ones
python sf-rebalance/rebalance.py --apply       # pause + propose replacements
```

### Always-on background loops

```
/loop 15m python SF-Skills/sf-loop-hunter/hunter.py --top 10
/loop 30m python SF-Skills/sf-loop-pruner/pruner.py --apply --include dead
```

## Hard rules

1. Never accept API keys on the command line. Only `SF_API_KEY` /
   `SF_API_SECRET` from the environment.
2. Never log or print credentials.
3. Respect the server-side limits: 120 req/min globally, 10s cooldown per
   bot on PATCH, 20,000 credits/month. `sf_client.py` throttles
   automatically — don't bypass it.
4. Anything that writes (`POST /bots`, `PATCH /bots/:id`) requires explicit
   user-facing intent — either an `--apply` flag, or the user actually
   asking to deploy.
5. `sf-deploy` is one-shot. It never amends an existing bot. To re-deploy
   a different sizing, pause the old bot first (via `sf-prune` or a
   direct PATCH) and create a new one.
6. Edge-decay flags are heuristic. Surface them; don't pretend they're
   certainty. A `decaying` label is "look at this", not "delete this".
7. Pause is reversible (`PATCH` with `action: "reactivate"`). Bot creation
   isn't trivially reversible — prefer pausing over re-deploying.

## What the agent should NOT do unprompted

- Auto-deploy strategies. Even loop-hunter only *surfaces* picks; the
  operator deploys.
- Pause bots without `--apply`. The flag exists precisely so a dry-run
  pass is always available.
- Mass-PATCH. The 10-second cooldown is real — `sf_client.patch_bot`
  respects it, but flooding the API still annoys the rate limiter.
- Touch a bot owned by a different API user. The server enforces this,
  but the agent shouldn't try.
