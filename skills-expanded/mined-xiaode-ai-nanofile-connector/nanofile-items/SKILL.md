---
name: nanofile-items
description: Universal item search and lifecycle operations (move, copy, rename, recycle) across files and folders using NanoFile.
---

# NanoFile 项目读写技能 (Item Management)

统一处理文件和文件夹的通用检索与基础生命周期操作。

## 适用场景

- 用户需要通用检索项目（不限文件或目录）。
- 用户需要移动、复制、重命名项目，或将项目安全移入 Windows 回收站。
- 用户需要对多个项目执行批量移动、复制或删除。

## 包含工具 (3 个)

### 1. `search_items` (唯一全能检索工具)

全能项目检索，支持限定类型（搜索项目/搜索文件/搜索文件夹）、扩展名后缀过滤、搜索范围与模式。

#### 搜索类型与防重复搜索准则（重要）

- **搜索项目 (`item_type: "all"`, 默认)**：**包含文件、文件夹的搜索**。一次检索即可返回匹配的所有文件与文件夹。如果执行了“搜索项目”，结果已全量包含，**严禁**再分别调用 `file` 和 `folder` 重复搜索！
- **搜索文件 (`item_type: "file"`)**：**仅文件搜索**。仅在明确只需要查找文件时使用。
- **搜索文件夹 (`item_type: "folder"`)**：**仅文件夹搜索**。仅在明确只需要查找文件夹/目录时使用。

> ⚠️ **AI 行为准则**：三选一。请根据用户的实际意图选择最契合的一种搜索类型。**严禁对同一查询词连续/重复发起 3 种类型的多次调用**。

```json
{
  "query": "invoice_2026",
  "item_type": "all", // "all" (搜索项目：包含文件与文件夹，默认) | "file" (搜索文件：仅文件) | "folder" (搜索文件夹：仅文件夹)
  "extensions": ["pdf", "xlsx"], // 可选，限定扩展名（如仅搜指定后缀文件）
  "scope": "common", // "common" (常用，默认) | "global" (全局全盘) | "directory" (目录)
  "directory_path": "D:\\Work", // 当 scope 为 "directory" 时提供
  "mode": "auto", // "auto" (自适应) | "turbo" (极速) | "realtime" (实时)
  "max_results": 50
}
```

返回结果包含搜索耗时统计（整数显示与自动进位单位，如 `450µs`、`15ms`、`2s`）与命中的条目清单：

```json
{
  "elapsed": "15ms",
  "elapsed_ms": 15,
  "total": 2,
  "items": [
    {
      "name": "invoice_2026.pdf",
      "path": "D:\\Work\\invoice_2026.pdf",
      "is_dir": false,
      "size": 1048576
    }
  ]
}
```

### 2. `operate_item`

对单个文件或文件夹执行安全的移动、复制、重命名或移入回收站。

```json
{
  "operation": "recycle", // "move" | "copy" | "rename" | "recycle"
  "source_path": "C:\\Users\\Username\\Documents\\draft.docx",
  "target_path": "C:\\Users\\Username\\Documents\\archived.docx" // move/copy/rename 时需要
}
```

> **安全策略**：
>
> - `recycle` 操作将项目移入 Windows 回收站，绝不物理直删，可随时还原，无需二次确认。
> - 系统关键目录（如 `C:\Windows`、启动项等）受底层保护，禁止任何修改操作。
> - 操作涉及需管理员或特殊权限的受保护目录时，遵循与 GUI 相同机制，需获得用户显式二次确认。

### 3. `batch_operate_items`

批量移动、复制或删除多个项目。

```json
{
  "operation": "move", // "move" | "copy" | "recycle"
  "source_paths": ["D:\\Data\\file1.txt", "D:\\Data\\file2.txt"],
  "destination_directory": "D:\\Backup"
}
```
