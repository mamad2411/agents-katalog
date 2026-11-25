---
name: my-preserve
description: 从当前对话提取知识保存到个人知识库 My vault（完整原文存 raw + 自动消化到 wiki）
---

# My Preserve — 个人知识保存

> 在任何非工作目录使用。保存到 `~/Desktop/My vault/My vault`。

## 知识库路径

```
~/Desktop/My vault/My vault
```

## Usage

```
/my-preserve              # 完整原文存 raw + 自动消化到 wiki
/my-preserve direct       # 有隐私：raw 只存摘要，消化完整原文到 wiki
```

## 第零步：读错题本和开发规范

- `~/Desktop/My vault/My vault/知识库/流程-开发规范/踩坑记录.md`
- `~/Desktop/My vault/My vault/知识库/流程-开发规范/开发规范.md`

## 默认模式

```
提取完整对话原文 → 存 原始资料/ → 自动消化 → 审核 → 写 wiki
```

1. **逐段复制完整对话原文到 raw 文件**
   - ⚠️ 严禁总结、严禁摘要、严禁压缩
   - 路径：`~/Desktop/My vault/My vault/原始资料/{date}-{topic}.md`
   - 同窗口多次执行：追加到同一文件，只更新结束时间戳
2. **自动消化**：
   - 列出知识点，**等用户确认后才写 wiki**
   - 矛盾检测（问用户）、重复检测（自动合并）
3. **写入 wiki 文章** + 更新 _总索引.md + 活动日志.md

## direct 模式

```
消化完整原文 → 过滤隐私 → 审核 → 写 wiki → raw 只存摘要
```

消化的是完整原文（不是摘要），wiki 文章已脱敏，raw 只记录时间+主题。

## Rules

- **严禁摘要**：raw 存完整原文
- **编译前必须审核**：列知识点等用户确认
- 矛盾不自动裁决，问用户
