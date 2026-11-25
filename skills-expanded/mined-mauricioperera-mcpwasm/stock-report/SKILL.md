---
name: stock_report
version: 1.0.0
license: MIT
---

# stock_report

Return an inventory stock report with no arguments:

- `total_titles`: number of distinct titles.
- `total_stock`: sum of `stock` across all titles.
- `out_of_stock`: number of titles with `stock = 0`.
- `top3_by_stock`: the 3 titles with the highest stock.