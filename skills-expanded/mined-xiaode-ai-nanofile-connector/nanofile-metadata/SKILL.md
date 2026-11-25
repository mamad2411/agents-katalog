---
name: nanofile-metadata
description: Inspect item attributes, recursive folder size, directory item count, timestamps, read-only permissions, and text line/character metrics using NanoFile.
---

# NanoFile 元数据读取技能 (Metadata Inspection)

深入获取文件或文件夹的基础属性、文件夹总大小、项目数量与扩展元数据。

## 适用场景

- 用户需要查询文件大小、只读状态、创建时间与最后修改时间。
- **文件夹大小与数量**：用户需要读取指定文件夹的总大小（递归计算子文件体积）以及包含的项目/文件总数。
- 用户需要检查文本或代码文件的行数、字符数等详细度量指标。

## 包含工具 (2 个)

### 1. `get_item_metadata`

获取标准属性。对文件夹会自动递归计算内含文件的总大小（`size_bytes`）及项目数（`item_count`、`file_count`、`dir_count`）。

```json
{
  "path": "D:\\Projects\\NanoFile"
}
```

_文件夹返回示例_：

```json
{
  "path": "D:\\Projects\\NanoFile",
  "is_dir": true,
  "is_file": false,
  "is_readonly": false,
  "size_bytes": 104857600, // 文件夹内全部文件的累计大小
  "item_count": 258, // 项目总数
  "file_count": 210, // 文件数
  "dir_count": 48, // 子文件夹数
  "created_at": "2026-08-01T08:00:00Z",
  "modified_at": "2026-10-07T10:00:00Z"
}
```

### 2. `get_media_metadata`

提取文档与媒体扩展元数据（对小文本文件自动计算行数与字符数）。

```json
{
  "path": "D:\\Projects\\NanoFile\\README.md"
}
```
