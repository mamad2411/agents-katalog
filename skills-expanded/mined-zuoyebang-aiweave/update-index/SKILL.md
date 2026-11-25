---
name: update-index
description: 自动扫描 docs/ 目录并更新 INDEX.md 的计数和条目，确保索引与实际文档保持一致。
disable-model-invocation: true
argument-hint: "[可选：dry-run 仅报告差异不修改]"
---

自动扫描 `docs/` 目录，对比 `INDEX.md`，更新计数和条目。模式：`$ARGUMENTS`（空则更新，`dry-run` 则仅报告）。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码，故第 5 步测试同步不适用。

## 第 0 步：前置检查

无 🚫 模块拒绝规则。仅需确认 `docs/INDEX.md` 存在。

## 第 1 步：扫描实际文档

按 docs/ 子目录依次扫描：

- `docs/architecture/*.md` → 列出所有文件
- `docs/api/*.md` → 统计每个文件中接口数
- `docs/service/*.md` → 列出所有
- `docs/schema/*.md` → 统计 DDL 中表数
- `docs/cache/*.md` → 列出
- `docs/circuit_breaker/*.md` → 列出
- `docs/testing/*.md` → 列出
- 检查是否有新顶层目录

## 第 2 步：生成差异报告

```
=== INDEX.md 差异报告 ===

📝 architecture/ — 条目变更
  + new_doc.md（新增）
  - removed_doc.md（已删除）

📊 api/ — 计数变更
  audience_a_interfaces：5（无变化）
  audience_b_interfaces：23 → 24（变更）

🆕 新目录（无）
```

## 第 3 步：执行更新（非 dry-run 模式）

- 新增文件：在对应表格新增行，说明文字取 md 第一个 `#` 标题
- 删除文件：从表格移除
- 更新接口数 / 表数 / 任务数等
- 发现新顶层目录 → **询问用户**说明后再添加

## 第 4 步：文档同步（公共项见 §C）

- 重新扫描一次，确认差异报告为空
- 回复末尾声明：「文档同步：更新了 `docs/INDEX.md`」

## 第 5 步：测试同步

**不适用**——本 Skill 不生成业务代码。

## 第 6 步：验证

差异报告归零即为通过。

## 注意事项

- **不修改已有条目说明文字**，除非文件被删除/重命名
- **保持表格格式一致**


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
