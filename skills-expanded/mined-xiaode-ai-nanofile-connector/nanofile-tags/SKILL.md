---
name: nanofile-tags
description: Native file and folder tagging system using NanoFile: list tags, rename tags, delete tags, get item tags, assign tags, and clear tags.
---

# NanoFile 标签读写技能 (Tag Management)

全面管理系统标签列表及文件/文件夹的关联标签。

## 适用场景

- 用户需要获取当前系统中所有已创建/使用的标签列表及引用频次。
- 用户需要将某个标签重命名（自动同步更新所有已绑定项）。
- 用户需要从全局列表中彻底删除某个标签（自动从所有项目中解绑）。
- 用户需要查询某个文件或文件夹打上了哪些标签。
- 用户需要为文件或文件夹添加或修改标签。
- 用户需要移除某个文件或文件夹上的标签。

## 包含工具 (6 个)

### 1. `list_all_tags`

获取当前系统中所有标签列表及其关联的项目总数。

```json
{}
```

_返回示例_：

```json
[
  { "name": "重要", "item_count": 12 },
  { "name": "工作", "item_count": 8 }
]
```

### 2. `rename_tag`

重命名标签列表中的标签，并自动同步更新所有已关联的文件和文件夹。

```json
{
  "old_name": "待办",
  "new_name": "急需处理"
}
```

### 3. `delete_tag`

从全局标签列表中删除指定标签，并从所有关联项目中自动解绑。

```json
{
  "tag_name": "废弃标签"
}
```

### 4. `get_item_tags`

获取指定项目当前关联的标签列表。

```json
{
  "path": "C:\\Users\\Username\\Documents\\contract.pdf"
}
```

### 5. `set_item_tags`

为指定项目设置或更新标签列表。

```json
{
  "path": "C:\\Users\\Username\\Documents\\contract.pdf",
  "tags": ["重要", "法务", "已签署"]
}
```

### 6. `remove_item_tags`

从指定项目中移除部分或全部标签。

```json
{
  "path": "C:\\Users\\Username\\Documents\\contract.pdf",
  "tags": ["草稿"] // 若省略 tags 则清空该项目的所有标签
}
```
