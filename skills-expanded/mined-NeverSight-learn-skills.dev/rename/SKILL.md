---
name: rename
description: Use when the user wants to normalize paper directory names to Author-Year-Title format after metadata correction or audit cleanup.
---
# 重命名论文文件

根据 JSON 元数据规范化论文文件名（`Author-Year-Title` 格式）。

## 执行逻辑

1. 判断用户意图：
   - 重命名单篇：指定 paper_id
   - 重命名全部：使用 --all
   - 先预览再执行：使用 --dry-run

2. 执行命令：

**预览全部重命名：**
```bash
scholaraio rename --all --dry-run
```

**执行全部重命名：**
```bash
scholaraio rename --all
```

**重命名单篇论文：**
```bash
scholaraio rename <paper-id>
```

3. 重命名后建议重建索引：
```bash
scholaraio pipeline reindex
```

## 示例

用户说："帮我把论文文件名整理一下"
→ 先执行 `rename --all --dry-run` 预览，确认后执行 `rename --all`
