---
name: index
description: Use when the user wants to rebuild or refresh ScholarAIO keyword, full-text, FTS5, FAISS, or semantic search indexes after data or metadata changes.
---
# 重建索引

重建 FTS5 全文检索索引或 FAISS 语义向量索引。

## 执行逻辑

**更新 FTS5 全文索引（增量）：**
```bash
scholaraio index
```

**重建 FTS5 全文索引：**
```bash
scholaraio index --rebuild
```

**更新证据片段索引（增量）：**
```bash
scholaraio index --chunks
```

**重建证据片段索引：**
```bash
scholaraio index --chunks --rebuild
```

**更新语义向量索引（增量）：**
```bash
scholaraio embed
```

**重建语义向量索引：**
```bash
scholaraio embed --rebuild
```

**两者都更新：**
```bash
scholaraio pipeline reindex
```

## 示例

用户说："重建索引"
→ 执行 `pipeline reindex`

用户说："只重建全文索引"
→ 执行 `index --rebuild`

用户说："重建证据片段索引" 或 "让搜索能定位到原文行号"
→ 执行 `index --chunks --rebuild`

用户说："更新向量"
→ 执行 `embed`
