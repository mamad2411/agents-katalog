---
name: taobao-cstore-sku-scraper
description: 抓取淘宝 C 店或天猫单个商品链接的全部 SKU 价格与优惠信息，输出优惠前价、到手价（页面优惠后价）、优惠政策构成（官方立减百分比、限时立减/直降金额、首单礼金、店铺新客减、红包、淘金币、跨店满减、百亿补贴、赠品）、库存与规格，并生成 CSV/XLSX。当用户提供 item.taobao.com 或 detail.tmall.com 商品链接、要求查看某商品各规格价格与优惠、做竞品单链接价格调研、核对"官方立减还是直降"、或需要 SKU 级到手价与库存表时使用。支持一次传入多条链接做竞品横比。
agent_created: true
---

# 淘宝/天猫 单链接多 SKU 价格与优惠抓取

## 核心原理

商品详情页是服务端渲染，**全部 SKU 的价格、库存、优惠文案已在页面 HTML 里**（`window.__ICE_APP_CONTEXT__` 的 `skuBase` + `skuCore`）。因此不需要调接口、不需要点规格、不触发任何 XHR，读取即得。这既是速度优势，也是风控优势：请求量与真人打开一次详情页完全相同。

数据结构、字段含义、失效判断见 `references/page-data-model.md`。节奏与风控约束见 `references/risk-control.md`，执行前必读。

## 前置检查

1. `ego-browser` 可用（`ego-browser --version`）。
2. 浏览器处于**用户本人已登录**状态（淘宝/天猫）。未登录时用 `task.handOff()` 让用户自己扫码，**不要**代填账号密码。
3. 目标链接能解析出数字 `id`（`...item.htm?id=123`）。只给淘口令或短链时，先在浏览器打开一次，取跳转后的 `item.htm?id=`。

## 执行流程

### 1. 组装任务文件

ego 的 node 运行时既不继承环境变量也不继承当前目录，配置必须写进固定文件 `/tmp/taobao_sku_job.json`：

```bash
cat > /tmp/taobao_sku_job.json <<'JSON'
{"urls":["https://item.taobao.com/item.htm?id=961483645644"],"out":"/abs/output/dir"}
JSON
```

字段：`urls`（链接或纯 ID 数组，可多条）、`out`（输出目录，绝对路径）、`force`（可选，`true` 强制重抓已存在结果）。

### 2. 抓取

```bash
ego-browser nodejs < {SKILL_DIR}/scripts/scrape.js
```

- 每个商品写一个 `item_<id>.json`；已存在且有 SKU 时自动跳过（断点续跑，配 `force: true` 可覆盖）。
- 失败写 `fail_<id>.json`，并把原因打到 stdout。
- 命中滑块/验证时写 `_run_summary.json` 的 `blocked: true`，退出码 3，**剩余链接不再抓**。
- 退出码：`0` 正常 / `2` 任务文件错误 / `3` 被风控中断。

### 3. 生成报表

```bash
python3 {SKILL_DIR}/scripts/report.py --dir /abs/output/dir
```

产出 `SKU价格与优惠_<日期>.csv` 与同名 `.xlsx`（三 sheet：SKU明细 / 商品汇总 / 口径说明）。缺 openpyxl 时自动只出 CSV。

### 4. 汇报

向用户交付表格路径，并**必须**说明三点口径：

1. 到手价取页面优惠后价，口径名逐条列在「到手价口径」列——天猫是「平台加补后」（含平台补贴），C 店是「店铺优惠后」（只减店铺优惠），**两者不可直接横比**。
2. 「已享受」明细按默认展示 SKU 渲染，金额是单品口径；不同 SKU 的立减额以各自到手价为准。
3. 红包、限时立减带倒计时；88VIP、消费券、淘金币余额因人而异，最终以下单页为准。

## 输出字段

SKU 明细：商品ID、商品标题、店铺、规格/SKU、SKU ID、优惠前价、到手价、到手价口径、优惠力度（1-到手/优惠前）、立减金额、促销政策（结构化拼接）、政策简写、库存、备注（售罄）。

商品汇总：另含 活动（双11/618 等）、SKU 数、销量、到手价区间、抓取时间。

## 禁止事项

- 不调用 `h5api.m.tmall.com` 等签名接口，不逆向 `sign`/`h5_tk`。
- 不改造成并发、不多开 Page、不上代理池轮换、不开无头模式。
- 不在命中验证后重试或换号；不代填登录凭证。
- 单次任务超过 30 条链接时拆成多批，批间隔 10 分钟以上。
