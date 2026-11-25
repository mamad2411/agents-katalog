---
name: sorftime-rpa
description: >-
  Unified sorftime.com (Amazon seller analytics) RPA skill covering all 11
  sections: 畅销榜 bestseller, 产品选品 product, 选市场 market, 关键词 keyword,
  选品牌 brand, 选卖家 seller, 查ASIN checkproduct, 查品牌 checkbrand,
  查卖家 checkseller, 查市场 checkmarket, 查关键词 checkkeyword (experimental).
  Use whenever the user wants to scrape, cross-station compare, or analyze
  sorftime data. Drives the user's real logged-in browser via BrowserSkill
  (bsk) — sorftime's AES-encrypted API forces DOM-driven scraping (trigger
  Vue VM methods, read decrypted reactive state). Single CLI entry
  (sorftime_rpa.py scrape/analyze/sections), per-section config registry,
  CSV outputs in data/, Markdown reports in reports/. Self-contained —
  includes environment notes, DOM/VM contracts, and 11 report templates.
---

# sorftime-rpa (unified)

一个技能，11 个板块。由 11 个历史分模块技能（bestseller / product / market /
keyword / brand / seller / checkproduct / checkbrand / checkseller /
checkmarket / checkkeyword）合并而来，解析逻辑逐字继承。本技能**完全自包含**：
脚本只依赖 Python 标准库 + 技能内部模块，不引用技能目录外的任何文件。

## Architecture

```
.claude/skills/sorftime-rpa/
├── SKILL.md / README.md
├── references/
│   ├── environment.md            # 环境/shell 坑（必读）
│   ├── dom_notes.md              # 11 个板块的 VM 契约（合并自旧 api_notes）
│   └── reports/<section>.md      # 11 份报告模板（分析器内联生成，此为形状文档）
└── scripts/
    ├── sorftime_rpa.py           # 单入口 CLI: scrape / analyze / sections
    ├── bridge_browserskill.py    # bsk 传输层适配器（call/evaluate/session_stop）
    ├── sections.py               # 配置注册表：URL/D_PARAM/JS/extract_row/FIELDS
    ├── core_domain.py            # 域引擎（product/keyword/brand/seller）
    ├── core_check.py             # 查引擎（5 个 check 模块）
    ├── bestseller_walk.py        # 例外：zTree 类目遍历
    ├── market_boards.py          # 例外：4 子模式 + 14 站 + retry
    ├── analyze.py                # 11 个报告分析器，按 --section 分发
    └── test_offline.py           # 离线回归（mock transport，无需浏览器）
```

**铁律**：解析函数与 JS 片段逐字来自旧技能（sections.py），引擎只认配置不写死板块细节。

## Prerequisites

1. `bsk` CLI 已安装且浏览器扩展已连接：`bsk status` → `browsers connected ≥ 1`
2. 用户已登录 sorftime.com（数据靠登录态）
3. Python 3.10+（纯标准库）

## Sections at a glance

| section | family | 页面 | 用法要点 | 数据可得性 |
|---|---|---|---|---|
| bestseller | custom | `/home/bestseller` | zTree 类目遍历，TOP100/类目 | ✅ 全量 |
| product | domain | `/home/chooseproduct` | 自动加载；免费版 ~20 未遮罩 ASIN/站 | ⚠️ 遮罩 |
| keyword | domain | `/home/choosekeyword` | 默认 20 热词，无需选类目 | ✅ |
| brand | domain | `/home/choosebrand` | 默认 20 品牌行 | ✅ |
| seller | domain | `/home/chooseseller` | 默认 20 卖家行 | ✅ |
| market | custom | `/home/choosemarketblock` | 4 子模式（multi/buyer/new/lowprice） | ✅（部分站点慢） |
| checkproduct | check | `/home/checkproduct` | ASIN 批量查（一次搜全部 ASIN） | ✅ |
| checkbrand | check | `/home/checkbrand` | 5 种搜索模式 | ✅ |
| checkseller | check | `/home/checkseller` | 4 种搜索模式 | ✅ |
| checkmarket | check | `/home/checkmarket` | 6 种搜索模式；loading 标志特殊 | ✅ |
| checkkeyword | check | `/home/checkkeyword` | 6+ 表格，**实验性** | 🔬 |

14 站点：US GB DE FR IN CA JP ES IT MX AE AU BR SA（查模块 URL 用 `?i=<id>`；选品域用 `localStorage.site` + reload）。

## Commands

```bash
SKILL=.claude/skills/sorftime-rpa/scripts/sorftime_rpa.py

python $SKILL sections                       # 列出全部 section

# —— 选品域 ——
python $SKILL scrape --section brand --station US,JP,GB --out data/brands.csv \
    [--summary data/brands_summary.csv] [--sleep 12]
python $SKILL scrape --section keyword --station US,JP --out data/keywords.csv
python $SKILL scrape --section product --station US --out data/products.csv [--page-size 100]
python $SKILL scrape --section seller --station US --out data/sellers.csv

# —— 例外板块 ——
python $SKILL scrape --section bestseller --station US --out data/best.csv \
    [--categories electronics,home] [--max-categories 5]
python $SKILL scrape --section market --station US --out data/markets.csv \
    [--sub-modes multi,buyer,new,lowprice] [--us-only-4modes] [--all-4modes] \
    [--retry-failed] [--sleep-after 10]

# —— 查模块 ——
python $SKILL scrape --section checkbrand --station US,JP --mode brand \
    --queries "Anker,Baseus" --out data/checkbrand.csv          # 或 --input file.csv
python $SKILL scrape --section checkproduct --station US \
    --queries B0CHX1W1XY,B0BDHZ8Q63 --out data/checkproduct.csv # ASIN 批量
# check 模式表：checkbrand= brand/asin/seller-name/seller-company/keyword
#               checkseller= asin/brand/seller/keyword
#               checkmarket= asin/niche/keyword/nodeid/category/tree
#               checkkeyword= reverse/traffic/root-word/trend/ad-strategy (实验性)

# —— 报告 ——
python $SKILL analyze --section brand --input data/brands.csv --out-md reports/brand.md
```

## CSV schemas（canonical 字段顺序，回归断言用）

- **product** (22): `station, station_name, rank, asin, parent_asin, name, brand, price, single_price, gross_profit, fba_fee, page_sale_count, page_sale_volume, year_sale_count, score, comment_count, deliver, seller_nationality, node_id, update_time, image_url, asin_url`
- **keyword** (27): `station, station_name, site, rank, name, id, avg_price, avg_score, avg_review, avg_comment_count, brand_count, competitor_count, coverage_count, buy_rate, cpc_storm, cpc_low, cpc_high, growth_3m, growth_6m, growth_12m, buy_monopoly, fall_type_str, busy_season, cyclical_market, extend_word_count`（+ 动态列）
- **brand** (24): `station, station_name, site, rank, brand, id, brand_url, product_count, seller_count, top_product_count, top_seller_count, top_product_count_rate, top_sale_count, top_sale_volume, top_avg_price, top_avg_comment_count, top_min_sale_time, top_product_max_node, top_sale_max_node, month_product_count, month_sale_count, month_avg_price, month_avg_sale_count, top_asins`
- **seller** (53): `station, station_name, site, rank, name, id, solder_id, solder_url, enterprise_name, nationality, online_time, feedback_count, business_address, product_count, all_brand_count, ...`（完整列表 = sections.py `SELLER_FIELDS`）
- **bestseller** (24): `station, station_name, category_slug, category_name, rank, asin, name, brand, price, sale_count, sale_estimate, gross_profit, fba_fee, deliver, score, comment_count, seller, seller_nationality, sale_time, sale_time_day, asin_url, image_url, node_id, single_price`
- **market**: `station, station_name, site_id, sub_mode, sub_mode_id` + 246 个原始字段（前 40 个固定列见 sections.py `MARKET_BASE_FIELDS`）
- **check 系列**: 各自的表格字段 + 标注列（`station, site[, query, mode]`），列序由读取器输出决定

## Critical gotchas（每个都真实踩过）

1. **DOM 驱动**：绝不要直调 `api.sorftime.com`（AES 加密必 401/CORS）。原理与各板块 VM 契约见 `references/dom_notes.md`。
2. **站点切换两种方式**：选品域必须 `localStorage.site` + reload（URL `?i=` 无效）；查模块用 URL `?i=` 即可。
3. **页面初始化 7~8 秒**：navigate 后必须 sleep；0 行先怀疑太快再怀疑选择器。
4. **trusted-click**：Vue 回调检查 `event.isTrusted`，一律直接调 VM 方法（如 `vm.treeItemClick(node)`）。
5. **Pro 弹窗**（keyword/brand/seller）会阻塞数据填充，引擎在 ensure 阶段已移除；手动调试时要先清掉。
6. **Windows 编码**：读写 CSV 一律 `utf-8-sig`；`Path.read_text()` 默认 GBK 会炸中文。
7. **Bash heredoc + JS 正则**会被吃反斜杠——JS 全在 `sections.py` 常量里，别在 shell 内联重写。
8. **路径**：给 Windows python 传 `D:/...` 不是 `/d/...`。
9. **bash 沙箱可能吞 CSV**：实跑抓取用非沙箱执行。

## Offline 回归

```bash
python .claude/skills/sorftime-rpa/scripts/test_offline.py   # 28 项断言，无需浏览器
```

## Migration note

由 11 个历史分模块技能合并（传输层从 kimi-webbridge HTTP daemon 切换到
BrowserSkill/bsk）。解析逻辑与 JS 逐字搬运、零重写；回归用 canonical schema
断言而非逐字节对比（实时数据每抓必变）。
