---
name: nanofile-favorites
description: Manage quick access directories, bookmarked favorite paths, and aliases using NanoFile.
---

# NanoFile 收藏夹读写技能 (Favorites Management)

管理常用目录书签与系统快速访问（Favorites）列表。

## 适用场景

- 用户需要查看已收藏的常用文件夹或系统快速访问路径。
- 用户需要将某个常用文件夹加入收藏夹，并支持设置友好别名。
- 用户需要从收藏夹中移除不再需要的路径。

## 包含工具 (3 个)

### 1. `get_favorites`

获取当前已收藏的全部目录（包含路径与显示别名）。

```json
{}
```

### 2. `add_favorite`

添加文件夹到收藏夹/快速访问中。

```json
{
  "path": "D:\\Work\\Projects",
  "alias": "我的项目" // 可选，省略则默认使用文件夹原名
}
```

### 3. `remove_favorite`

从收藏夹中移除指定目录。

```json
{
  "path": "D:\\Work\\Projects"
}
```
