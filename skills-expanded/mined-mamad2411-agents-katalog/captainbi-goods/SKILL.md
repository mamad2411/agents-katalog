---
name: captainbi-goods
description: "Goods, shops, sites, tags, groups, SKU and ASIN commands for CaptainBI CLI. WHEN use for: shop/site discovery, product master data, SKU/ASIN lookup, goods changes, tags, groups, and operator metadata. WHEN NOT: do not use for orders, profit, advertising, FBA inventory, or reviews unless product mapping is needed."
---

# CaptainBI Goods

Read `captainbi-shared` first.
For task recipes, read `references/workflows.md`.

## WHEN

Use for shop/site discovery, SKU/ASIN/product master data, goods tags, goods groups, operators, and goods-level metadata.

## WHEN NOT

Do not use for orders, profit, advertising performance, FBA inventory, or reviews unless the workflow needs product names/ASIN mapping.

## Command Choice

- Shops: `cbi +shops --machine --format json`.
- Sites: `cbi +sites --machine --format json`.
- Goods list: `cbi +goods --channel <alias> --modified-since <ts> --modified-until <ts> --summary`.
- Full goods pull: `cbi goods list --channel <alias> --start-modified-time <ts> --end-modified-time <ts> --page-all --max-records <n> --output-file goods.json`.
- Tags/groups: `cbi goods tags --channel <alias>`, `cbi goods groups --channel <alias>`.

## Examples

```bash
cbi config channels add main '<open_channel_id>'
cbi --channel main +goods --modified-since 1781424057 --modified-until 1781510457 --summary --machine
cbi --channel main goods list --start-modified-time 1781424057 --end-modified-time 1781510457 --page-all --max-records 50 --machine
```

## Notes

- `start_modified_time` and `end_modified_time` use second-level Unix timestamps.
- `goods list` may not return `max_result`; rely on CLI pagination metadata.
- For operator, group or shop-mode writes, read `references/workflows.md`; use dry-run, stop for user approval, then pass the exact `--confirm-request` hash and verify by reading back.
