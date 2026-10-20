---
name: healthy-food-filter-mcp
description: Set up and use the standalone Healthy Food Filter MCP server.
version: 1.0.0
metadata:
  hermes:
    tags: [mcp, health, food, brands]
    triggers:
      - "filter food brands by rules"
      - "check food product ingredients"
      - "scan grocery items against diet"
      - "validate food against household criteria"
      - "healthy food filter"
    category: devops
    config:
      tools.mcp_servers.healthy-food-filter:
        type: mapping
        default: null
---

# Healthy Food Filter MCP Server

Standalone MCP server that scans food brands and ingredients against the operator's
strict household criteria. Hook it into any MCP host (Hermes, Claude Desktop).

## Prerequisites

- Python 3.11+
- `mcp` package (`pip install mcp anyio`)

## Setup

```bash
# Clone and install
git clone https://github.com/pmb2/healthy-food-filter.git
cd healthy-food-filter
python -m pip install -e ".[mcp,dev]"

# Verify
python -m pytest
```

## Hermes Integration

Add to `~/.hermes/config.yaml`:

```yaml
tools:
  mcp_servers:
    healthy-food-filter:
      command: python
      args: ["-m", "healthy_food_filter.mcp_server"]
      auto_approve: ["check_product", "lookup_brand", "scan_ingredients", "list_banned"]
```

Restart Hermes. The tools appear as `healthy_food_filter__*` in the agent's toolset.

## the operator's Rule: SUSPECTED = AVOID

Any brand or parent company with ANY involvement in harmful/suspicious food
practices (even trials, pilots, or "we're looking into it") gets a permanent
AVOID. No benefit of the doubt. The Food Safety Watch module tracks these —
add new issues as they're reported.

## Available Tools

- `check_product` — full scan: ingredient list + brand ownership → HEALTHY/FLAGGED/AVOID
- `lookup_brand` — quick brand parent/tier lookup (150+ brands)
- `scan_ingredients` — ingredient list only, no brand check
- `list_banned` — complete banned/watch ingredient catalog by category

## Example Queries

After hooking up, ask your Hermes agent:
- "Check Kraft mac and cheese through the health filter"
- "Who owns Annie's brand?"
- "Scan these ingredients: water, sugar, soy lecithin, red 40"
- "List everything that's banned"

## Dairy Policy

Default: `bovine_ban` — bovine dairy (whey, casein, caseinate) triggers BANNED.
Pass `dairy_policy=warn` to flag only, or `dairy_policy=none` to skip entirely.

## Black-tier Brands

BLACK-tier brand parents (Nestlé, Kraft-Heinz, PepsiCo, Coca-Cola, General Mills, etc.)
cause an AVOID verdict by default. Pass `refuse_black_tier=false` to flag only.

## Verification

```bash
python -m pytest          # 18 tests
ruff check src/ tests/
```
