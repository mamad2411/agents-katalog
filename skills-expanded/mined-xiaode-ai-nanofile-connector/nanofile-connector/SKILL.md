---
name: nanofile-connector
description: Connect your AI assistant to NanoFile for high-performance local file search, file/folder operations, default app management, tag catalog, installed app management, and favorites.
---

# NanoFile Agent Connector & Skills (7 大核心能力全集)

> 💡 **【推荐调用建议 (Best Practices)】**：
>
> 1. **全盘极速检索**：NanoFile 提供高性能原生搜索服务，直接调用 `search_items` 即可毫秒级获取全盘文件与目录结果。
> 2. **标准调用方式**：
>    - **原生 MCP 环境**（强烈推荐，如 Cursor、Claude Desktop、Trae、Antigravity）：直接发起对应的 MCP 工具调用（如 `search_items`、`read_file_content` 等）。
>    - **原生 CLI 命令行环境**（推荐，全平台原生无依赖）：安装 NanoFile 后终端直接可用 `nf <command>`（如 `nf search "报告" --ext pdf`、`nf cat <path>`、`nf call <tool_name> '<json_arguments>'`）。
>    - **脚本透传环境**：可使用 `node scripts/nanofile_cli.mjs <tool_name> '<json_arguments>'` 执行对应能力（内部优先直调 `nf` 原生二进制）。

## 1. 7 大能力子技能结构

NanoFile MCP 包含 27 个标准工具，检索能力全盘收拢于 `search_items`：

```
nanofile-connector/
├── skills/
│   ├── items/       # 1. 项目读写 (3 工具) - 全能检索 (支持文件/文件夹/扩展名) 与基础操作
│   ├── files/       # 2. 文件读写 (5 工具) - 文本读写、打开方式与应用启动
│   ├── folders/     # 3. 文件夹读写 (5 工具) - 层级遍历、递归创建、默认打开方式
│   ├── tags/        # 4. 标签读写 (6 工具) - 标签列表管理、重命名、删除、单项标签绑定
│   ├── metadata/    # 5. 元数据读取 (2 工具) - 属性、文件夹大小/项目数统计、文本度量
│   ├── apps/        # 6. 应用程序读写 (3 工具) - 系统应用枚举、安全启动、合规卸载
│   └── favorites/   # 7. 收藏夹读写 (3 工具) - 快速访问与目录收藏管理
```

|   #   | 能力域           | 专项子技能                                      | 核心工具清单                                                                                               | 工具数 |
| :---: | :--------------- | :---------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :----: |
| **1** | **项目读写**     | [`skills/items`](skills/items/SKILL.md)         | `search_items`, `operate_item`, `batch_operate_items`                                                      |   3    |
| **2** | **文件读写**     | [`skills/files`](skills/files/SKILL.md)         | `read_file_content`, `write_file_content`, `open_file`, `get_file_default_app`, `set_file_default_app`     |   5    |
| **3** | **文件夹读写**   | [`skills/folders`](skills/folders/SKILL.md)     | `list_folder_contents`, `create_folder`, `get_folder_default_app`, `set_folder_default_app`, `open_folder` |   5    |
| **4** | **标签读写**     | [`skills/tags`](skills/tags/SKILL.md)           | `list_all_tags`, `delete_tag`, `rename_tag`, `get_item_tags`, `set_item_tags`, `remove_item_tags`          |   6    |
| **5** | **元数据读取**   | [`skills/metadata`](skills/metadata/SKILL.md)   | `get_item_metadata` (含文件夹递归大小及条目统计), `get_media_metadata`                                     |   2    |
| **6** | **应用程序读写** | [`skills/apps`](skills/apps/SKILL.md)           | `search_apps`, `launch_app`, `uninstall_app`                                                               |   3    |
| **7** | **收藏夹读写**   | [`skills/favorites`](skills/favorites/SKILL.md) | `get_favorites`, `add_favorite`, `remove_favorite`                                                         |   3    |

---

## 2. 准备工作与安装引导

使用本技能前，请先在 Windows 系统中安装 NanoFile：

- 🛒 **微软应用商店直达链接**：[https://apps.microsoft.com/detail/9pgwd50gwcjw](https://apps.microsoft.com/detail/9pgwd50gwcjw)
- 🚀 **一键唤起应用商店安装**：`ms-windows-store://pdp/?ProductId=9PGWD50GWCJW`

> **提示**：从微软应用商店安装 NanoFile 后，Windows 会自动注册全局执行别名 `nanofile.exe`，无需配置复杂的绝对路径，开箱即用。

---

## 3. 客户端 MCP 配置 (仅需 5 行 JSON)

在您的 AI 客户端（如 Claude Desktop 的 `claude_desktop_config.json`，或 Cursor 的 `mcpServers` 设置）中加入如下配置：

```json
{
  "mcpServers": {
    "nanofile": {
      "command": "nanofile.exe",
      "args": ["--mcp"]
    }
  }
}
```

---

## 4. 原生命令行 CLI 使用 (nf)

NanoFile 提供全原生命令行工具 `nf`（等价别名 `nanofile-cli`），随本技能库 `cli/` 目录独立分发，开箱即用（需本机已安装 NanoFile 桌面客户端）：

```bash
# 极速全盘搜索
nf search "quarterly_report" --ext pdf --limit 10

# 查看目录内容
nf ls "D:\Projects" --limit 20

# 读取文件内容
nf cat "D:\Projects\config.json"

# 获取文件/媒体元数据
nf meta "D:\Projects\video.mp4" --media --json

# 标签与收藏夹管理
nf tag list
nf fav list

# 原生 MCP 通用直通调度（供脚本与 AI Agent 单次调用任意 MCP 工具）
nf call search_items '{"query":"contract","limit":5}' --json
nf call get_favorites '{}' --json
nf tools --json
```

---

## 5. 全量工具速查 (27 个 Tools)

### 1. 项目读写 (`skills/items`)

- `search_items`：**全能检索**。全局、常用或目录检索文件/文件夹；支持 `item_type`（all/file/folder）及 `extensions` 扩展名后缀过滤。
- `operate_item`：移动、复制、重命名或移入回收站。
- `batch_operate_items`：批量移动、复制或移入回收站。

### 2. 文件读写 (`skills/files`)

- `read_file_content`：读取 UTF-8 文本内容（默认全量读取，支持可选最大字符保护）。
- `write_file_content`：创建或覆盖写入文本文件。
- `open_file`：使用默认程序或指定应用打开文件。
- `get_file_default_app`：读取扩展名或文件的默认打开程序。
- `set_file_default_app`：设置扩展名的默认打开程序。

### 3. 文件夹读写 (`skills/folders`)

- `list_folder_contents`：列出指定目录的直接子项目。
- `create_folder`：递归创建多级目录。
- `get_folder_default_app`：读取文件夹当前的默认打开方式。
- `set_folder_default_app`：设置文件夹默认打开方式（nanofile / explorer / terminal / 自定义应用）。
- `open_folder`：使用默认打开方式或指定工具打开目录。

### 4. 标签读写 (`skills/tags`)

- `list_all_tags`：获取当前系统中所有标签列表及其关联的项目总数。
- `delete_tag`：从标签列表中彻底删除标签并自动解绑。
- `rename_tag`：重命名标签并自动同步所有关联项目。
- `get_item_tags`：获取指定项目的关联标签。
- `set_item_tags`：为指定项目设置或追加标签。
- `remove_item_tags`：移除指定项目的标签。

### 5. 元数据读取 (`skills/metadata`)

- `get_item_metadata`：获取常规属性，文件夹自动递归统计总大小与条目数量。
- `get_media_metadata`：提取文本代码行数与字符数分析。

### 6. 应用程序读写 (`skills/apps`)

- `search_apps`：检索系统已安装的桌面应用程序。
- `launch_app`：启动指定应用（支持附带参数）。
- `uninstall_app`：合规唤起系统应用卸载页。

### 7. 收藏夹读写 (`skills/favorites`)

- `get_favorites`：获取快速访问与收藏夹列表。
- `add_favorite`：添加目录到收藏夹（支持设置别名）。
- `remove_favorite`：从收藏夹中移除目录。

---

## 6. 安全与保密准则

1. **系统目录绝对保护**：系统核心关键目录（如 `C:\Windows`、`C:\Boot`、`C:\Recovery`、用户自启动目录等）实施底层硬拦截，禁止任何写操作，杜绝系统崩溃与持久化风险。
2. **敏感权限目录二次确认**：对于需要管理员或特殊权限的受保护目录（如涉及敏感系统资产、受限共享或 UAC 提升区），在执行写操作或权限变更前，遵循与 GUI 相同的人机交互原则，必须由用户显式二次确认后方可继续。
3. **防意外损毁**：普通业务删除统一移入 Windows 回收站（可撤销还原），绝不直接物理覆写或硬删除。
