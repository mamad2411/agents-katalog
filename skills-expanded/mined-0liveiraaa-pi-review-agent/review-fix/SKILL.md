---
name: review-fix
description: 跨科目复习资料包修订。根据自然语言反馈迭代修订 draft，或从 active 创建安全修订草稿。当 /review-fix 触发时使用，负责应用修订、更新质量报告并在用户确认后启用。
---

# Review Fix

你负责根据用户的自然语言反馈修订资料包。所有实际写入都发生在 `draft` 上；如果用户选择 active 资料包，系统会先创建 revision draft，你只能修改这个修订草稿。

## 核心约束

- 先检查 `profile.json` 状态。只有 `draft` 可以写入。
- 如果 `profile.json.revisionOf` 存在，说明这是某个 active profile 的修订草稿。不要直接修改原 active。
- 所有写入走 `review_profile_write`。不要用 Bash / Write / Edit 直接写。
- 启用走 `review_profile_enable`，且只在用户明确确认后调用。
- 修订后**必须**更新 `quality_report.md`。

## 修订流程

### 1. 读取现状

- `profile.json` — 确认 draft 状态；如果有 `revisionOf`，记录原 active 来源。
- `knowledge_index.json` — 了解知识点全貌。
- `source_map.json` — 了解文件映射（改文件时需要知道来源）。
- `quality_report.md` — 了解已有问题（修订时顺带解决）。
- 根据用户反馈涉及的范围，读相关的 `cards/`、`chapters/`、`exam_points/` 文件。

### 2. 解读反馈 → 映射操作

| 用户反馈 | 操作 |
|----------|------|
| "太碎了" / "这几个合并" | 合并文件 → 更新 index 和 source_map → 重写受影响卡片 |
| "太长了" / "太宽泛" | 拆分文件 → 为新知识点生成 ID+属性 → 更新 index 和 source_map |
| "定义不对" / "代码跑不通" | 对照 source_map 找源资料确认 → 只改出错部分 → 同步关联卡片 |
| "缺了 X" | 源资料有 → 提取生成；源资料没有 → 告诉用户"源资料未找到 X" |
| "这个不用" / "第 N 章不考" | 在 knowledge_index.json 中标记 `"status": "removed"` — 不物理删除文件 |
| "名字改成…" | 全局搜索替换 → 更新所有交叉引用 |
| "难度不对" | 修改 knowledge_index.json 中对应知识点的 `difficulty_baseline` |
| "确认启用" / "设为 active" / "开始复习" | 见步骤 5 |

如果当前 draft 是 revision draft，修订记录里必须写明 `revisionOf`，让用户知道启用后会替换哪个 active profile。

### 3. 执行修订

每次修订必须**全链路同步**：

- 改一个知识点名称 → 更新 index + 卡片标题 + 考点总结中的引用 + source_map。
- 合并两个知识点 → 新知识点 ID + 合并后卡片 + 更新 index + 更新 source_map + 废弃旧卡片。
- 拆分知识点 → 新 ID + 新卡片 + 更新 index + 更新 source_map。

**不确定的修订**：如果用户的反馈模糊（"这里改一下"但没说怎么改），先确认再动手。

### 4. 更新 quality_report.md

修订后重写质量报告：
- 更新基础数据。
- 移除已解决的问题。
- 记录新发现的问题。
- 追加修订记录：

```markdown
## 修订记录
| 版本 | 时间 | 来源 | 变更摘要 |
|------|------|------|----------|
| v1 | {时间} | /review-init | 初始生成 |
| v2 | {时间} | /review-fix | {改了哪些文件、为什么} |
```

### 5. 确认启用

**仅在以下情况**调用 `review_profile_enable`：
- 用户明确说"确认启用" / "启用" / "设为 active" / "开始复习吧" / "进入复习"
- 且不是在提新的修改需求时顺带说的
- 如果这是 revision draft，启用会把原 active 标记为 archived/superseded，并把当前 draft 设为 active。

**以下情况不启用**：
- 用户说"改好了"、"不错"、"嗯" — 只是对修改满意，不等同确认资料包完整可用
- 用户又提了新修改需求
- 质量报告中有严重问题且用户没有明确表示忽略

修订完成后输出：

```
资料包修订完成。

📝 变更：
  - {具体改了什么}
  - {具体改了什么}

📊 当前：{K} 章 {S} 小节 | {M} 知识点 | {C} 卡片

🔍 请查看 quality_report.md。
确认无误后输入「确认启用」将资料包设为 active。
需继续修改的话直接输入反馈即可。
```

启用后输出：

```
✅ 资料包 {subjectId} 已启用。现在 /review 可以选择该科目了。
```

如果启用的是 revision draft，补充说明：

```
旧版本 {revisionOf} 已归档保留；当前启用版本为 {subjectId}。
```
