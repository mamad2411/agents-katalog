---
name: figma-ios-comments-integration
description: >-
  Apply Figma comments that are pre-matched to nodes by figma-ios-preload-data.
  Read confidence + parsed tags from comments.json. Iconfont corrections are already
  written into design.json; color comments stay in comments.json for Phase-2 mapping.
  Use when generating code from Figma with designer comments.
---

# Figma 评论集成（消费数据包）

阶段 2 不再获取或匹配评论。`figma-ios-preload-data` 已经在阶段 1 完成了：
- 拉取所有评论
- 解析 message → tags（iconfont / icon_correction / color / color_correction / rotation / 自由文本）
- 命中节点（坐标 hit-test + 关键词 boost + iconfont 祖先重定向）
- 给出 confidence + `is_safe`
- **iconfont 修正已被脚本主动应用**：`parsed.iconfont_name` 在 `confidence>=medium` 且 `is_safe` 时已覆盖 `nodes[best_node_id].iconfont.symbol`，并标 `source=comment` + `original_symbol`。阶段 2 直接读 `iconfont.symbol` 即可，**不需要再二次比对**。
- **颜色评论不会改写 `design.json`**：`parsed.color` 只在 `comments.json`；生成时由 [figma-ios-design-token-mapping](../figma-ios-design-token-mapping/SKILL.md) 优先于节点 `fills[].color`。

## 数据来源

| 文件 | 字段 |
|---|---|
| `{data_dir}/comments.json` | `comments[comment_id]` |
| `{data_dir}/design.json` | `nodes[node_id].comments = [comment_id, ...]`（反向索引）|

## comments.json 字段速查

```json
{
  "comments": {
    "1693773932": {
      "id": "1693773932",
      "message": "这个是iconfont：icon_next_12",
      "user": "岩竹",
      "created_at": "2026-03-26T10:30:00Z",
      "resolved": false,
      "parsed": {
        "tags": ["iconfont", "icon_correction"],
        "iconfont_name": "icon_next_12",
        "color": null
      },
      "is_safe": true,
      "match": {
        "best_node_id": "I1:343;1:342;30:8689",
        "confidence": "high",
        "candidates": [
          {"node_id": "...", "score": 50.0, "reasons": ["bbox_hit","iconfont_keyword_boost"]}
        ]
      }
    }
  }
}
```

> 字段是 **`resolved: bool`**（由 Figma `resolved_at` 推导），**没有** `resolved_at` 字符串字段。

## 处置规则

| confidence | 处置 |
|---|---|
| `high` | **应用**（iconfont 已在 design；颜色按 token-mapping 读评论）|
| `medium` | 应用，并在生成代码注释中标注「评论建议（confidence=medium，作者=xxx）」|
| `low` | **不应用**，但在生成的 README "待人工确认" 列表中列出原文 |
| `unmatched`（无 best_node_id）| 同 low |

已 resolved 的评论（`resolved == true`）**忽略**。`is_safe == false` 的评论**不应用**（阶段 1 也不会回写 iconfont）。

## 覆盖规则（按 tag）

| tag | 阶段 1 | 阶段 2 |
|---|---|---|
| `iconfont` / `icon_correction` | 已写入 `node.iconfont.symbol` | 直接读 `iconfont.symbol`，查 `iconfont_map.json` |
| `color` / `color_correction` | **不**改 `design.json`；`parsed.color` 留在评论 | 映射时优先 `parsed.color`，再回退节点 `fills[].color`（TEXT 也是 fills，**无** `text.color`）|
| rotation 相关 | — | 见 iconfont-mapping；评论禁止旋转则忽略 `iconfont.rotation` |
| 自由文本 | — | 不覆盖字段，仅 `// 评论：xxx` |

## 生成代码示例

```swift
// Figma node: I1:343;1:342;30:8689
// 评论修正（high）：iconfont/icon_query_24 → icon_next_12（作者：岩竹，2026-03-26）
let backIcon = UILabel()
backIcon.font = MKIconFont.iconFont(withSize: 24)      // iconfont_map.font
backIcon.text = MKIconFont.shared().mk_icon_next_12    // iconfont_map.text
```

## 自检清单

- [ ] 已读 `comments.json`
- [ ] iconfont：直接用 `design.json` 里已回写的 `symbol`（勿再手工覆盖一遍除非核对）
- [ ] 颜色评论：走 design-token-mapping，优先 `parsed.color`
- [ ] `low` / `unmatched` 已写入 README 待确认列表
- [ ] `resolved == true` / `is_safe == false` 已跳过
