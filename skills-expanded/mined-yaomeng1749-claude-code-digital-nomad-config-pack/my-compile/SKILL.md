---
name: my-compile
description: 编译个人知识库 My vault 的 原始资料/ 原始资料为 知识库/ 结构化文章
---

# My Compile — 个人知识编译

> 编译 `~/Desktop/My vault/My vault/原始资料/` 中的资料到 知识库/。

## 知识库路径

```
~/Desktop/My vault/My vault
```

## Usage

```
/my-compile              # 编译 原始资料/ 中所有未编译的文件
```

## 第零步：读错题本和开发规范

- `~/Desktop/My vault/My vault/知识库/流程-开发规范/踩坑记录.md`
- `~/Desktop/My vault/My vault/知识库/流程-开发规范/开发规范.md`

## Workflow

1. **扫描** `~/Desktop/My vault/My vault/原始资料/` 中未编译的文件
2. **质量审核**：
   - 列出从源文件中提取的知识点
   - **展示给用户，等用户确认后才写 wiki**
   - 垃圾内容跳过
3. **矛盾和重复检测**：
   - 在 知识库/ 搜索相关文章
   - 重复 >80% → 合并
   - 矛盾 → 问用户
4. **写入 wiki 文章**：
   - 简洁要点式 + `## Key Takeaways`
   - 用 `[[wikilinks]]` 交叉引用
5. **更新索引**：`_索引.md` + `_总索引.md` + `活动日志.md`

## Rules

- 编译前必须审核，等用户确认
- 矛盾不自动裁决
- 重复自动合并
