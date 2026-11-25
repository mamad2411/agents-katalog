---
name: nanofile-folders
description: Dedicated directory search, folder contents traversal, recursive folder creation, folder default app configuration, and opening in Explorer/Terminal/NanoFile.
---

# NanoFile 文件夹读写技能 (Folder Management)

针对文件夹的专用能力：层级内容遍历、递归新建目录、默认打开方式管理与打开文件夹。（注：目录搜索已全部由全能 `search_items` 统一承载，传入 `item_type: "folder"` 进行仅文件夹搜索；如果已执行过 `item_type: "all"` 搜索项目，则已涵盖文件夹，切勿重复调用）。

## 适用场景

- 用户需要列出指定文件夹内的直接子项清单（附带文件大小与类型）。
- 用户需要递归新建多级文件夹。
- 用户需要读取文件夹的默认打开方式。
- 用户需要设置文件夹的默认打开方式（如 NanoFile、资源管理器、终端或自定义程序）。
- 用户需要使用默认方式或指定工具打开文件夹。

## 包含工具 (5 个)

### 2. `list_folder_contents`

列出目录的直接子项目，返回名称、绝对路径、是否为文件夹及文件大小。

```json
{
  "path": "D:\\Projects",
  "include_hidden": false
}
```

### 3. `create_folder`

递归新建文件夹（若父级不存在将自动级联创建）。

```json
{
  "path": "D:\\Projects\\2026\\Q4\\Reports"
}
```

### 4. `get_folder_default_app`

读取当前系统/应用为文件夹配置的默认打开方式。

```json
{}
```

### 5. `set_folder_default_app`

设置文件夹的默认打开方式。

```json
{
  "app": "nanofile" // "nanofile" | "explorer" | "terminal" | 自定义可执行程序路径
}
```

### 6. `open_folder`

打开文件夹（默认使用已配置的默认打开方式打开，亦可显式指定目标）。

```json
{
  "path": "D:\\Projects\\NanoFile",
  "target": "default" // "default" (使用默认打开方式) | "nanofile" | "explorer" | "terminal"
}
```
