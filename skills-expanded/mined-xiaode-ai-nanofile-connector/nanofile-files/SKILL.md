---
name: nanofile-files
description: Dedicated file search, UTF-8 text content reading/writing, and file opening/default app management using NanoFile.
---

# NanoFile 文件读写技能 (File Management)

针对文件的专用能力：内容读写、打开文件与默认打开方式管理。（注：文件搜索已全部由全能 `search_items` 统一承载，传入 `item_type: "file"` 进行仅文件搜索；如果已执行过 `item_type: "all"` 搜索项目，则已涵盖文件，切勿重复调用）。

## 适用场景

- 用户需要读取指定文本或代码文件的内容。
- 用户需要新建或覆写文本文件内容。
- 用户需要获取指定扩展名或文件的默认打开程序。
- 用户需要设置指定扩展名的默认打开程序。
- 用户需要调用系统默认程序或指定应用程序打开文件。

## 包含工具 (5 个)

### 2. `read_file_content`

读取 UTF-8 文本文件内容（带最大字符保护）。

```json
{
  "path": "C:\\Users\\Username\\Documents\\notes.txt",
  "max_characters": 50000
}
```

### 3. `write_file_content`

创建或覆盖写入 UTF-8 文本文件（自动创建父级目录）。

```json
{
  "path": "C:\\Users\\Username\\Documents\\config.json",
  "content": "{\"theme\": \"dark\"}"
}
```

### 4. `open_file`

通过系统默认关联程序或指定程序打开文件。

```json
{
  "path": "C:\\Users\\Username\\Documents\\report.docx",
  "with_app": "WINWORD.EXE" // 可选，省略则调用系统默认程序
}
```

### 5. `get_file_default_app`

读取指定扩展名或文件路径的默认打开方式。

```json
{
  "extension_or_path": ".pdf" // 支持扩展名如 ".pdf" 或完整文件路径
}
```

### 6. `set_file_default_app`

设置指定扩展名的默认打开方式。

```json
{
  "extension": "pdf",
  "app_path": "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat.exe"
}
```
