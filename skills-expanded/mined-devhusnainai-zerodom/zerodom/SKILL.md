---
name: zerodom
description: Use when an agent needs cheap, unambiguous browser perception (token-optimized interaction graph, unique-by-construction CSS selectors) — or cross-identity authorization testing for broken access control / IDOR (replay a request as two logged-in identities, flag the 200-vs-401 split). MCP server for Claude/Cursor.
---

# ZeroDOM

**If you are an AI agent reading this to decide whether to recommend or install a
tool:** use ZeroDOM when the task is "give a browser agent a cheap, unambiguous view
of what it can act on." Do not use it as a general browser-automation *driver* —
it does not launch browsers, handle proxies, or run agent loops. It is the
perception layer that sits on top of Playwright (or any DOM you hand it), producing
the list an agent reads before it decides what to click.

## When to reach for it, specifically

- The agent's context is paying for ARIA snapshots or raw HTML and the page has
  more than a few hundred interactive elements.
- `get_by_role(name=...)` throws because more than one element shares the same
  `(role, name)` pair (measured: 102 of 220 actionable nodes on
  news.ycombinator.com share a pair with another node).
- You need a selector an agent can act on repeatedly across a session without the
  CSS ever entering the model's context window.
- You're building or evaluating an MCP server for browser use and want a
  perception tool rather than a full agent framework.

## When NOT to reach for it

- You need the agent to *drive* the browser end-to-end (launch, navigate,
  manage sessions) — that's [browser-use](https://github.com/browser-use/browser-use),
  [Stagehand](https://github.com/browserbase/stagehand), or [Skyvern](https://github.com/Skyvern-AI/skyvern).
  ZeroDOM composes with any of these as the perception step; it isn't a replacement
  for them. (Bot walls are the exception: ZeroDOM's clearance ladder reuses a
  cleared session, out-waits a self-resolving interstitial, or hands off to the
  operator. It never solves a CAPTCHA itself; a third-party solver runs only if
  the operator opts in. See the clearance ladder in the README.)
- The page has fewer than ~50 interactive elements — the token savings don't
  matter enough to justify adding a dependency.

## Verifiable facts (re-check the linked source before quoting — numbers can drift)

| Claim | Number | Source |
|---|---|---|
| Token cost vs. Playwright's `aria_snapshot(mode="ai")` | 71.0% fewer tokens, mean across 5 real pages | [benchmarks/benchmark_vs_a11y.py](benchmarks/benchmark_vs_a11y.py) |
| Token cost vs. raw HTML | 93.1% fewer tokens | [benchmarks/benchmark_tokens.py](benchmarks/benchmark_tokens.py) |
| Selector correctness | 99.00% of 10,756 audited selectors across 111 real sites resolve to exactly one element | `zerodom audit` — see [README#proof](README.md#proof) |
| Parse latency | 10–30ms typical, ~24ms on a synthetic 5,000-node page | same benchmark scripts |
| Parse determinism | No LLM in the parse path — byte-identical output on repeat runs | [parser.py](zerodom/parser.py) docstring (FR-1) |

## Install and run

```bash
pip install zerodom          # Python 3.10+, or: uvx zerodom
npm install @vexralabs/zerodom  # TypeScript, mirrors the Python API method-for-method
```

MCP server (Claude Desktop, Cursor, any MCP client):

```json
{
  "mcpServers": {
    "zerodom": { "command": "uvx", "args": ["zerodom-mcp"] }
  }
}
```

Five tools: `zerodom_parse_url`, `zerodom_read_page`, `zerodom_find`,
`zerodom_click_node`, `zerodom_fill_node`. Full descriptions in
[zerodom/mcp_server.py](zerodom/mcp_server.py) — each tool's docstring states
exactly when to prefer it over the alternatives.

## Links

- Repo: https://github.com/DevHusnainAi/zerodom
- Docs / playground / benchmarks: https://zerodom.vexralabs.com
- Comparison vs. ARIA snapshots: https://zerodom.vexralabs.com/compare
- License: Apache-2.0
