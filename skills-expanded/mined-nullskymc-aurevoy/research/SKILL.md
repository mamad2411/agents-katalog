---
name: research
description: 调研与报告。快速报告（检索后直接写）或深度报告（outline→并行深挖→合成）。默认 Markdown；用户要单页/组件版式时用 HTML。用于调研、简报、评估、计划、纪要。
user-invocable: true
metadata:
  version: "2.0"
---

# Research

两种模式，先选一个再开干。

| 模式 | 何时 | 流程 |
|---|---|---|
| **快速报告**（默认） | 主题单一、时效短、不需多对象结构化对比 | 检索 → 写报告 → 交付 |
| **深度报告** | 多对象/多切片、要可续跑、要字段对齐 | outline → 并行 deep JSON → **合成**报告 → 交付 |

澄清：最多问 1 次（模式 / 时间范围 / 交付格式）。能默认则默认。

---

## 交付

| 形态 | 路径 | 何时 |
|---|---|---|
| 对话结论 | — | 用户只要几句话 |
| **Markdown**（默认文件） | `research/<slug>/report.md` 或 `report/<slug>.md` | 需归档、分享、可打开预览 |
| **HTML** | `report/<slug>.html` | 用户明确要 HTML / 单页 / 评分卡时间线等组件 |

规则：

1. 未指定格式 → 文件用 **Markdown**。  
2. HTML 仅在用户要求或组件版式明显更合适时。  
3. 最终回复 = **路径 + 一句话摘要**；不复述全文。  
4. 文件交付后 `attach_content`。HTML 须先 `bundle_report`。  
5. **禁止**把「按字段 key 全量展开」当作主报告。  
6. **改稿纪律**：首次用 `write` 落草稿；之后补证据/改段落用 `edit`（精确 old→new），禁止为小改反复 `write` 整篇覆盖。

---

## 快速报告

1. `web_search` / `web_fetch`（必要时 `delegate` role=`research`）。不编造来源。  
2. 直接写报告，结构：

```markdown
# 标题
> as_of / 范围

## 结论
（5–10 行主线）

## 要点
- …

## 数据 / 对比
（表格）

## 风险与下一步

## 来源
- url
```

3. HTML 时用下方组件骨架 + `bundle_report`。  
4. `attach_content`。

---

## 深度报告

### 1. 建骨架

目录：`research/<topic_slug>/`

**outline.yaml**

```yaml
topic: …
topic_slug: …
as_of: "YYYY-MM-DD"
mode: deep
delivery: markdown   # markdown | html | chat
items:
  - id: a
    name: 对象或切片 A
    focus: 一句话
execution:
  batch_size: 4
  output_dir: results
```

**fields.yaml**（扁平；宁少勿滥）

```yaml
fields:
  - name: summary
    category: 结论
    description: 该项核心结论
    required: true
  - name: evidence
    category: 证据
    description: 关键事实与数据
  - name: sources
    category: 来源
    description: URL 列表
    required: true
```

事件/简报类：字段控制在 **8 个以内**；对比档案类可稍多。不要为无关切片硬套同一张 40 字段表。

### 2. 并行 deep

- 已有 `results/<id>.json` 则跳过。  
- 每批最多 `batch_size` 个 `delegate`（role=`research`），每 item 一个。  
- 子任务：检索 → 按 fields 写 JSON → 不确定写 `"[不确定] …"` 并列入 `uncertain` → 中文值 → 含 `item_id` / `item_name` / `sources`。  
- 校验（路径按实际 skill 位置填写）：

```bash
python <skill_dir>/scripts/validate_json.py -f fields.yaml -j results/<id>.json
```

- 每批结束汇报进度，默认继续下一批。

### 3. 合成主报告（必须）

读全部 JSON，**写给人看的** `report.md`（或 HTML）：

1. 执行摘要（跨 item 去重后的主线）  
2. 关键表  
3. 分项要点（每 item 一段结论，不贴字段名清单）  
4. 风险 / 下一步  
5. 来源（去重）

JSON 留在 `results/` 即可。不要生成「字段 dump」当 `report.md`。

### 4. 交付

同「交付」节。

---

## HTML（两种模式共用）

- **禁止**读取或粘贴 `components.js`；`bundle_report` 会内联。  
- 一次 `write` 写完草稿；小改只用 `edit`（不要再整页 `write` overwrite）。  
- 草稿含 `<script src="./components.js"></script>`、`<report-container>`、`report-header`、`report-footer`。  
- 禁止自定义样式；`body` 仅背景/字体/间距。  
- 组件细节见 `references/api.md`（仅不熟时读）。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>标题</title>
  <script src="./components.js"></script>
</head>
<body style="background:#f8f8f8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;padding:32px 24px;margin:0">
  <report-container>
    <report-header badge="调研" date="YYYY-MM-DD" title="标题" summary="一句话结论。"></report-header>
    <report-section title="结论">
      <report-findings>
        <report-finding type="fact">…</report-finding>
        <report-finding type="risk">…</report-finding>
        <report-finding type="action">…</report-finding>
      </report-findings>
    </report-section>
    <report-footer><span>来源：…</span></report-footer>
  </report-container>
</body>
</html>
```

常用：`report-stat-cards` / `report-stat-card`、`report-callout`、`report-decision`、表格。

---

## 检查清单

- [ ] 模式正确（快 / 深）  
- [ ] 主报告可读，非字段展开  
- [ ] 事实有来源或标明不确定  
- [ ] 已 attach（文件时）；HTML 已 bundle  
- [ ] 聊天未贴全文  

## 不要

- 无必要拆 18 个 item 又共享超大 fields  
- 默认上 HTML  
- 静默假装完成未通过校验的 deep item  
- 报告已存在后仍多次 `write` 整文件重写（应 `edit`）  

