---
name: poe-mercenary-trade
description: Use when the user provides a PoEDB mercenary URL such as poedb.tw/cn/Striker, asks for a suitable or output mercenary, or mentions 佣兵凭证, 先锋, or mercenary-search.js. Search the PoE China trade site through the local Node.js CLI and recommend a matching warrant.
---

# PoE China Mercenary Trade

Use only the China-server CLI at `D:\skills\poe-mercenary-trade\mercenary-search.js`. Do not use the international-server adapters under `tools\bb-browser`.

## Preconditions

- Node.js 22 or newer is installed.
- Chrome is running with CDP on `http://127.0.0.1:9222`.
- The logged-in Chrome has an open `https://poe.game.qq.com/trade/` page.
- This skill is read-only. Never purchase an item, visit a hideout, or expose cookies, tokens, request headers, or raw listing responses.

## Interpret The User Request

When the user gives a PoEDB mercenary URL, read the public page first and extract the displayed mercenary build name. For example:

- `https://poedb.tw/cn/Striker` means the build `先锋`.
- The skills shown on the page are the build's possible skill pool, not a list of skills that every warrant must contain.
- A real warrant contains a selected subset of those skills and supports.

If the user asks for an output mercenary without more detail, assume physical melee stationary single-target damage, with damage and attack uptime prioritized over defensive utility. Unless the user gives another limit, use maximum mercenary level 74. Ask whether the user wants boss damage or mapping damage when the distinction matters.

## Run The Search

Use JSON output and let the CLI resolve the Chinese build name through the trade site's `/api/trade/data/items` data:

```powershell
node D:\skills\poe-mercenary-trade\mercenary-search.js --build "先锋" --max-level 74 --limit 10 --json
```

For a recommendation rather than a quick price lookup, scan all candidate IDs currently returned by Trade:

```powershell
node D:\skills\poe-mercenary-trade\mercenary-search.js --build "先锋" --max-level 74 --scan-all --json
```

Add user-specified options when present:

- `--supports` requires all listed supports to be connected to `--skill`.
- `--any-supports` requires at least one listed support on `--skill`.
- `--exclude-supports` rejects listed supports on `--skill`.
- `--additional-skills` requires extra skills on the warrant.
- `--support-count` limits the exact support count on `--skill`.
- `--min-price` and `--max-price` constrain the trade query price.
- `--limit` controls returned candidates during a normal search and must not exceed 10.
- `--scan-all` fetches every candidate ID currently returned by Trade, up to the site's loaded-candidate cap; use it when ranking candidates.

Do not translate the internal item type yourself. The CLI resolves `先锋` to the trade data entry whose shape is equivalent to:

```json
{
  "text": "佣兵凭证（先锋）",
  "type": "MeleeStrikesMaraduerPhys",
  "disc": "mercenary_warrant"
}
```

The spelling `Maraduer` is the server's actual value and must remain unchanged.

## Damage Mechanics

For the `先锋` build, treat these as the primary damage skills, not `戒备打击`:

- `双持打击`: uses both weapons in one skill use. Sum the main-hand and off-hand damage, apply the skill multiplier to each hand, and do not double the attack rate. It has a 70% base attack-speed multiplier, a full-life hit/ailment damage bonus, and a full-life critical-multiplier bonus.
- `七伤破`: each trauma stack has its own roughly 6-second duration. A new stack does not refresh every previous stack. Estimate sustainable stacks from effective trauma gains per second multiplied by the duration; do not assume a fixed maximum or infinite stacks. Include the self-damage constraint.
- `脆弱之重击`: alternates between main hand and off hand when dual wielding; it does not sum both weapon damages in one hit. Include its 85% base attack-speed multiplier, double-damage chance, and Vulnerability uptime. Do not model the 50% curse application chance as a permanent 50% damage multiplier when the curse can remain active.

For a stationary physical comparison, normalize weapon and support assumptions first. The warrant response does not contain the player's weapon damage, so do not claim an exact DPS value without weapon data. The displayed weapon physical damage and attack rate already include that weapon's local flat physical and local attack-speed modifiers; do not add them twice.

## Recommend A Candidate

Do not blindly return the first result. Inspect each JSON result's `skills` array and rank candidates using:

1. Exact build match and level at or below the requested maximum.
2. The relevant output skill: `双持打击`, `七伤破`, or `脆弱之重击`.
3. Offensive supports, especially physical damage, higher physical damage, attack speed, higher attack speed, multiple strikes, and brutality.
4. For `脆弱之重击`, include double-damage expectation and sustained Vulnerability coverage.
5. For `七伤破`, use a stated trauma-stack assumption or sustainable-stack estimate, and account for self-damage.
6. For `双持打击`, require or strongly prefer a real dual-wield setup; a weak off-hand reduces its advantage.
7. Treat `近战伤害扩散` as a mapping support, not a pure single-target damage support.
8. Penalize defensive-only supports such as `护体`, `镀金护体`, and `铁木`, but do not reject a warrant merely because it has defensive utility skills.
9. Penalize elemental or chaos-conversion supports when evaluating a pure physical build, especially when they conflict with `残暴`.
10. Use price, level, listing freshness, and seller online status as tie-breakers.

Explain the assumptions, show the important skill-support connections, and state whether the recommendation is for opening burst, sustained stationary damage, or mapping. State that the ranking is a practical heuristic, not a measured in-game DPS calculation.

## Result Handling

- `found`: summarize the recommended candidate and provide its official trade search URL.
- `not_found_in_loaded_results`: say that no matching item was found in the loaded candidates; do not claim the whole market is empty.
- If `candidateIdsLoaded` is less than `candidateTotal`, explicitly say that the result only covers the currently loaded candidate IDs.
- `error`: report the CLI error and tell the user when Chrome CDP or the logged-in China trade page is missing.

Keep the final response concise, in Chinese, and include the applied build, maximum level, price assumptions, recommendation reason, and trade link.
