---
name: zotero-library
description: Use when 需要使用 Zotero Web API 或 pyzotero 对 Zotero user/group 文献库进行搜索、读取、新增、修改、删除、打标签、整理、同步、审计或自动化更新，包括 note、collection、tag rename、DOI/title 查询、元数据清理和批量 bibliography 工作流。
---

# Zotero Library

通过 pyzotero 自动化 Zotero Web API 文献库 CRUD，并保留可审计轨迹。所有写操作都按“计划中的远端文献库变更”处理：先读取当前状态，再 dry-run 输出精确 payload，只有在目标文献库和变更内容被确认后才执行。

## 准备

依赖使用 `uv`：

```bash
uv add pyzotero
uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py --help
```

必需环境变量：

```bash
$env:ZOTERO_LIBRARY_ID="123456"
$env:ZOTERO_LIBRARY_TYPE="user"   # user 或 group
$env:ZOTERO_API_KEY="..."
```

可选只读本地模式：`$env:ZOTERO_LOCAL="true"`。本 skill 的写操作必须走 Web API 凭据，不依赖 Zotero Desktop local API 写入。

## 与官方 Zotero Skill 的分工

如果同时存在 Codex 官方 `zotero` skill 和本 skill：

- 用官方 `zotero` skill 做 Zotero Desktop local API 读操作、BibTeX 导出、引用插入、全文/附件路径读取。
- 用本 `zotero-library` skill 做 Web API 写操作、批量元数据更新、note 创建、collection 移动、全库 tag rename。
- 需要写库时不要走 local API；先 dry-run，再用本 skill 的 `--execute`。

## 工作流

1. 先判断请求类型：读取、note、collection 移动、tag rename、普通 item 更新或删除。
2. 读取任务使用 `item`、`children`、`item-collections`、`collections`、`collection-items` 或 `tags`。
3. note 使用 `create-note`；纯文本会被转为 Zotero UI 友好的 HTML：标题为 `<h2>`，段落为 `<p>`，`- ` 列表为 `<ul><li>`。
4. collection 追加使用 `add-to-collection`；移动使用 `move-to-collection`，默认移除该 item 当前所有其他 collection membership。
5. 全库 tag 改名使用 `rename-tag`：查找旧 tag 的 items，替换 tags 后批量 `update_items`。
6. 任意写操作执行后，重新读取受影响的 item、collection 或 tags 并报告实际结果。

编写原生 pyzotero 代码、修改 helper 或扩展未列功能前，先读 `references/pyzotero-workflows.md`。

## 快速参考

| 任务 | 命令模式 |
| --- | --- |
| 读取 item 所属 collections | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py item-collections ABC123` |
| 创建 note dry-run | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py create-note ABC123 --heading "阅读笔记" --text "重点"` |
| 移动到 collection dry-run | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py move-to-collection COLL123 ABC123` |
| 添加到另一个 collection | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py add-to-collection COLL123 ABC123` |
| 全库 tag rename dry-run | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py rename-tag old-tag new-tag` |
| 修改 item 元数据 dry-run | `uv run --with pyzotero python skills/zotero-library/scripts/zotero_library.py update-item ABC123 --fields "{\"title\":\"New title\"}"` |

## 写入门槛

只有在用户已确认目标 user/group 文献库、已审阅 dry-run 输出，并且命令显式使用 `--execute` 时，才执行写操作。破坏性或批量操作还需要回滚说明，例如旧 item JSON、旧 tag 名称或旧 collection 列表。

缺少任一门槛时，返回 dry-run 并请求确认，不要写入。

## 暂不处理

不要声称支持 colored tags、Zotero UI 偏好设置、附件上传、saved search 写入或 local API 写入。用户明确要求这些能力时，先查官方 API 可行性，再扩展本 skill。
