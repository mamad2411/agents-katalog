---
name: review-profile-index
description: 知识点索引生成。从规范化章节提取知识点、构建 knowledge_index.json。当 /review-init 需要生成知识点索引时加载。
---

# Profile Index

你在 `/review-init` 的步骤 4 中被加载。任务：从 `chapters/` 小节文件中提取知识点，生成 `knowledge_index.json`。

## 输出结构（必须严格匹配）

代码按 `chapters.{chapterId}.knowledge_points` 数组读取。生成这个结构：

```json
{
  "subject": "科目名称",
  "chapters": {
    "1": {
      "title": "章节标题",
      "knowledge_points": [
        {
          "id": "stable-id",
          "name": "知识点名称",
          "aliases": ["别名1", "别名2"],
          "tags": ["标签1", "标签2"],
          "question_types": ["choice", "judgment", "short_answer"],
          "difficulty_baseline": "S-U",
          "related": ["related-id"],
          "common_misconceptions": ["误区的具体描述"],
          "generation_hints": "出题方向和陷阱设置方式"
        }
      ]
    }
  }
}
```

可以额外加 `sections`、`tags`、`subject_id` 等字段，但 `chapters.*.knowledge_points` 数组不能省略。不要生成只有顶层 `knowledge_points` 的分离结构——`/review` 代码读不到那个格式。

## 提取规则

### 粒度判断

**一题测试**：能用这个知识点出一道独立的、有意义的题吗？

- ✅ 可以 → 保留。
- ❌ 出不了独立题（太碎，如"int 占 4 字节"）→ 合并到父级。
- ❌ 能出 5 道不同类型（太宽，如"面向对象"）→ 拆分。

### ID 命名

- 小写英文 + 下划线。语义优先：`copy_constructor` 而非 `kp_001`。
- 不超过 40 字符。
- 容易混淆的 ID 加区分后缀：`inheritance_public` vs `inheritance_protected`。

### 字段填写标准

`difficulty_baseline`：
- `S-R`：纯记忆/识别。不需要推理。
- `S-U`：需要理解区分，但仅涉及一个概念。
- `M-U`：需要比较 2-3 个概念。
- `M-A`：需要综合多个概念分析。

不确定时**宁低勿高**。

`question_types`：从 `["judgment", "choice", "short_answer"]` 中选。判断标准：知识点能用这个题型有效考察吗？

`common_misconceptions`：至少 2 条。每条一句说清错在哪。从源资料提取，不要编造。不知道就标注低置信度。

`generation_hints`：给后续出题 AI 的指令。格式："考 {考察维度}。陷阱：把 {概念A} 的 {特征} 混进 {概念B} 的选项。"

`related`：确实存在交叉或递进关系的其他知识点 ID。没有就 `[]`。

`tags`：2-4 个分类标签，用于跨章节检索。不要用知识点名本身做标签。

## 完成检查

- [ ] 每个小节至少 1 个知识点。
- [ ] 所有 ID 唯一。
- [ ] `difficulty_baseline` 合理（没有 S-R 标 M-A，反之亦然）。
- [ ] 每条 `common_misconceptions` 具体可操作。
- [ ] `related` 中的每条关联有实质内容。
