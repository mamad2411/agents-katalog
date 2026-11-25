---
name: BSC-amazon-VOC--products
description: 面向 Amazon 选品、VOC、竞品与关键词研究的深度分析技能。它会围绕一个需求词产出本地 `data.json`、`report.md`、`charts/`、`charts_manifest.json`，并在环境可用时发布飞书文档。只要用户提到 Amazon 选品判断、关键词机会、评论痛点、竞品研究、立项报告、Listing / PPC 依据、飞书交付，就应优先使用本技能，而不是回到旧 HTML dashboard 流程。
---

# BSC-amazon-VOC--products

这是一个适合直接拿来做 Amazon 选品研究交付的技能。

它不是只返回几段零散数据，而是尽量把一条完整分析链路跑通，最终产出：`data.json`、`report.md`、`charts/`、`charts_manifest.json`，以及可选的 `feishu_publish_result.json`。

## 适用场景

当用户出现下面这些意图时，优先使用本技能：

- 想判断某个 Amazon 产品方向到底值不值得做
- 想围绕某个关键词做深度 VOC / 评论 / 趋势 / 竞争研究
- 想输出一份可以交给老板、运营或客户的立项分析
- 想为 Listing、PPC、价格策略、图文表达提供依据
- 想把本地研究结果继续同步到飞书文档

## 给新手的理解方式

你可以把这个技能理解成：

- 先帮你抓到关键数据
- 再帮你生成图表
- 再帮你写出完整报告
- 最后在可用时继续发到飞书

主链路是：

`data.json` → `charts/` → `report.md` → `feishu_publish_result.json`

核心原则：

- 本地结果优先，飞书只是交付层
- 不恢复 `dashboard.html` 作为主产物
- 图表是报告增强层，不是第二套平行系统
- 增强维度失败允许降级，但不能阻断基础交付
- 报告要有证据链和建议动作，不只是堆数据

## 新手可直接复制的提示词

### 判断方向是否值得做

```text
帮我分析 Amazon 上 "barbell clamps" 在美国站值不值得做，重点看市场空间、竞争强度、用户痛点和切入建议。
```

### 做一份完整立项分析

```text
围绕 "standing desk" 做一份适合给老板看的 Amazon 立项分析，输出市场判断、竞品结构、VOC 洞察、风险和最终建议。
```

### 只要本地报告，不发飞书

```text
帮我分析 "weight bar clips" 在 US 站的 Amazon 选品和 VOC 机会，只保留本地结果，不发布飞书。
```

### 深挖评论和痛点

```text
帮我深挖 Amazon 上 "dog slow feeder" 的评论和 VOC，整理用户购买理由、差评原因、改进方向和机会点。
```

### 研究后继续补执行建议

```text
先完成 "yoga mat bag" 的 Amazon 选品 / VOC 分析，再补充 Listing 卖点、定价建议和 PPC 方向。
```

## 调用目标清单

当用户表达以下任意目标时，应该把本技能作为优先方案：

- 判断产品方向值不值得做
- 输出可交付的 Amazon 选品 / VOC 报告
- 围绕一个词做市场、关键词、竞品、评论、供应链全链路研究
- 只做本地结果，不发布飞书
- 在分析完成后继续补 Listing、PPC、定价或图片建议

## 功能覆盖

- 市场判断：类目映射、Top100、趋势、规模与竞争基础面
- 关键词研究：核心词、延伸词、SERP、搜索趋势、流量入口
- 竞争分析：价格带、评分带、评论带、卖家来源、代表竞品拆解
- VOC 洞察：正负评主题、痛点、购买理由、质量与适配风险
- 供应链线索：1688 相似货源与粗粒度成本参考
- 图表增强：从 `data.json` 生成静态 SVG 图表并混排进 `report.md`
- 飞书交付：先创建正文，再逐张追加上传本地图表
- 执行延伸：可继续输出 Listing、PPC、定价、主图 / 副图表达建议

## 运行要求

- Claude Code CLI
- Python 3.10+
- 可用的 Sorftime API Key
- `node`
- `lark-cli`（如果需要发布飞书）

当前脚本主要使用 Python 标准库。

## 命令

```bash
python BSC-amazon-VOC--products/run_analysis.py "barbell clamps" US
python BSC-amazon-VOC--products/run_analysis.py "weight bar clips" US --no-publish
python BSC-amazon-VOC--products/run_analysis.py "standing desk" US --api-key "YOUR_API_KEY"
```

当前入口只支持四个参数：`keyword`、`site`、`--api-key`、`--no-publish`。

## 工作流程

### 1. Collect data

`collect_data.py` 负责采集并归一化：

- 类目搜索与映射
- 类目 Top100 与 fallback 产品搜索
- 类目趋势与关键词
- 核心关键词详情、延伸词、SERP、趋势
- 代表竞品详情、流量词、竞品关键词、价格 / 销量趋势
- 评论样本与 VOC 主题
- 1688 相似货源与供应链线索

输出数据应尽量覆盖分析层与交付层字段，包括但不限于：

- `keyword_intelligence`
- `market_structure`
- `competitor_analysis`
- `traffic_analysis`
- `product_detail_analysis`
- `supply_chain_analysis`
- `opportunity_hypotheses`
- `data_health`
- `errors`

### 2. Render charts

`render_charts.py` 从 `data.json` 生成本地图表与 `charts_manifest.json`，当前优先覆盖：

- 价格带分布
- 评分带分布
- 评论带分布
- 卖家来源结构
- 关键词搜索量对比
- 关键词趋势
- SERP Top10 对比
- 代表竞品对比
- VOC 正负评主题对比

单图失败只跳过该图，不阻断主链路。

### 3. Build report

`build_report.py` 生成唯一主报告 `report.md`，默认结构为：

1. 执行摘要
2. 市场是否成立
3. 需求入口与关键词机会
4. 竞争格局与市场结构
5. 代表竞品拆解
6. VOC 洞察
7. 供应链与利润空间
8. 机会点与切入建议
9. 风险与门槛
10. 最终结论
11. 数据完整性 / 交付说明

如用户需要执行层动作，可继续补充：

- 产品定义
- 英文 Listing
- PPC 结构
- 定价与 Coupon 策略
- 主图 / 副图脚本

### 4. Publish to Feishu

`publish_feishu_doc.py` 按“两段式发布”执行：

1. 以本地 `report.md` 为唯一发布源
2. 创建飞书正文前，先移除 Markdown 中的本地图链
3. 先创建正文文档
4. 再追加图表附录与图表说明
5. 最后逐张上传本地图片
6. 写出 `feishu_publish_result.json`

## 输出结果

```text
voc-products-reports/
└── {keyword}_{site}_{YYYYMMDD}/
    ├── data.json
    ├── report.md
    ├── charts_manifest.json
    ├── charts/
    │   ├── price_bands.svg
    │   ├── rating_bands.svg
    │   ├── review_bands.svg
    │   ├── seller_sources.svg
    │   ├── keyword_volume.svg
    │   ├── keyword_trend.svg
    │   ├── serp_top10.svg
    │   ├── competitor_samples.svg
    │   └── voc_themes.svg
    ├── feishu_publish_result.json
    └── raw/
        ├── category_info.json
        ├── top100.json
        ├── trend.json
        ├── keywords.json
        ├── serp_*.json
        ├── competitor_reviews_*.json
        ├── competitor_keywords_*.json
        ├── product_detail_*.json
        ├── product_trend_*.json
        ├── traffic_terms_*.json
        ├── ali1688_*.json
        └── ...
```

输出文件说明：

- `data.json`：归一化后的结构化分析数据
- `report.md`：最终 Markdown 报告，包含图文混排
- `charts_manifest.json`：图表清单与相对路径
- `charts/`：本地静态图表目录
- `feishu_publish_result.json`：飞书发布结果与图表上传明细
- `raw/`：原始接口返回留档，便于追溯与排查

## 飞书图表发布策略

这是当前已经验证过的稳定做法：

- 不要把 `charts/xxx.svg` 这类本地图链直接留在飞书正文里等待服务端下载
- 飞书正文先创建，图表后追加
- `docs +media-insert` 必须在图表目录下执行
- `--file` 必须传相对路径，如 `./price_bands.svg`
- 不要直接传绝对路径，否则常见结果是 `unsafe file path`

正确顺序是：

1. 生成本地 `report.md`
2. 创建不含本地图链的飞书正文
3. 追加图表标题或说明
4. 在 `charts/` 目录下逐张上传 `./filename.svg`

## 数据来源

主要依赖 Sorftime MCP，常用接口包括：

- `category_name_search`
- `category_report`
- `category_trend`
- `category_keywords`
- `search_categories_broadly`
- `keyword_detail`
- `keyword_extends`
- `keyword_search_results`
- `keyword_trend`
- `product_detail`
- `product_search`
- `product_reviews`
- `product_traffic_terms`
- `product_trend`
- `competitor_product_keywords`
- `ali1688_similar_product`

## 交付规则

- 先保本地结果，再尝试飞书发布
- 不生成 `dashboard.html` 作为主交付
- 图表增强以本地静态图为主
- 单个增强维度失败允许降级
- 发布前只校验核心字段
- 缺失数据时要明确说明，不伪造结论

## 发布校验

发布前继续以核心旧字段为准，只检查这些字段是否可用：

- `decision.overall_score`
- `voc_analysis.dimensions`
- `barriers`
- `cross_analysis.bands`（兼容历史 `price_type_matrix`）

不要把新增字段作为硬门槛，否则会让增强维度反过来破坏稳定交付。

## 故障处理

- 单个接口失败：记录到 `errors` 与 `data_health`
- 无法获取增强维度：降级为基础版市场 / 关键词 / VOC 分析
- 供应链缺失：明确写“暂无稳定供应链样本”，不要伪造利润
- 关键词或 SERP 缺失：回退到已有类目关键词或产品搜索结果
- 单图失败：跳过该图，继续生成 `report.md`
- 飞书失败：保留本地 `report.md` 与 `feishu_publish_result.json`

## 最低完成标准

任务完成后至少满足：

- 存在 `data.json`
- 存在 `report.md`
- 存在 `charts_manifest.json`
- 存在 `charts/`
- 存在 `feishu_publish_result.json`
- 不生成 `dashboard.html`
- 报告在缺失部分维度时仍可读、可交付
- 如飞书发布成功，可回传文档链接；如失败，能明确失败原因

## 项目结构

```text
BSC-amazon-VOC--products/
├── SKILL.md
├── README.md
├── api_client.py
├── build_report.py
├── collect_data.py
├── publish_feishu_doc.py
├── render_charts.py
└── run_analysis.py
```

## 已验证能力

当前已经验证过：

- Sorftime → `data.json` → `report.md` → 飞书文档 主链路可用
- 图表增强链路可在飞书正文创建后继续追加并成功插入本地图表
- 深度选品报告已支持市场、需求、竞争、竞品、VOC、供应链、风险与结论闭环
- 飞书发布结果会稳定记录在 `feishu_publish_result.json`
- `chart_publish` 可追踪逐图上传结果

## 使用判断

执行本技能时，优先保持以下判断：

- 先用真实需求词做分析，不要一开始就用过泛关键词
- 报告不要停留在“可做 / 不可做”，尽量补齐切入方式与执行建议
- 供应链结论宁可保守，也不要在样本不足时硬给利润率
- 飞书只是交付层，`report.md` 与 `data.json` 才是主资产
- 如果用户需要执行层动作，顺着研究结论延伸出 Listing、PPC、定价与图片建议