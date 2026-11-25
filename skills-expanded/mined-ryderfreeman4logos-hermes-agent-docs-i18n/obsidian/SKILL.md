---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Notes, Markdown, Vault]
    related_skills: []
---

# Obsidian Vault

此技能适用于以文件系统为核心的 Obsidian Vault 操作，包括读取笔记、列出笔记、搜索笔记文件、创建新笔记、追加内容以及添加维基链接。

## Vault 路径

在调用文件相关工具之前，需使用已知或已解析的 Vault 路径。

文档中规定的 Vault 路径格式为 `OBSIDIAN_VAULT_PATH` 环境变量，例如可从 `${HERMES_HOME:-~/.hermes}/.env` 中获取该值。如果该变量未设置，则可使用 `~/Documents/Obsidian Vault` 作为默认路径。

文件工具不会自动展开 shell 变量，因此请勿将包含 `$OBSIDIAN_VAULT_PATH` 的路径传递给 `read_file`、`write_file`、`patch` 或 `search_files` 等函数，而应先解析出具体的绝对路径后再使用。由于 Vault 路径中可能包含空格，这也是推荐使用文件工具而非 shell 命令的另一个原因。

如果不确定 Vault 路径，可使用 `terminal` 工具来解析 `OBSIDIAN_VAULT_PATH` 或检查默认路径是否存在。一旦确定了路径，即可切换回文件工具进行操作。

## 读取笔记

使用已解析后的笔记绝对路径配合 `read_file` 函数来读取笔记。相比 `cat` 命令，这种方式能显示行号并支持分页查看，更为便捷。

## 列出笔记

使用 `search_files` 函数，并设置 `target: "files"` 参数以及已解析的 Vault 路径。相比 `find` 或 `ls` 命令，此方法更为高效。

- 若要列出所有 Markdown 格式的笔记，可在 Vault 路径后添加 `pattern: "*.md"` 参数。
- 若要列出某个子文件夹中的笔记，则需在该子文件夹的绝对路径下进行搜索。

## 搜索

无论是通过文件名还是内容进行搜索，均可使用 `search_files` 函数。相比 `grep`、`find` 或 `ls` 命令，此方法更具优势。

- 若需搜索文件名，可使用 `search_files`，并设置 `target: "files"` 以及文件名匹配模式 `pattern`。
- 若需搜索笔记内容，同样使用 `search_files`，将 `target` 设为 `"content"`，以内容正则表达式作为 `pattern`；若希望仅搜索 Markdown 格式的笔记，还需添加 `file_glob: "*.md"` 参数。

## 创建笔记

请使用 `write_file` 函数，传入已解析的绝对路径以及完整的 Markdown 内容。相比使用 shell 的 heredoc 或 `echo` 命令，这种方式能避免 Shell 引号相关的问题，并返回结构化的结果。

## 向笔记追加内容

在操作方式不会过于复杂的情况下，建议优先使用内置的文件操作工具：

- 首先使用 `read_file` 读取目标笔记。
- 当存在稳定的上下文环境时（例如可在现有标题后添加新章节，或在已知结尾块前追加内容），可使用 `patch` 实现基于锚点的追加操作。
- 若直接重写整个笔记比构建复杂的补丁更清晰，可直接使用 `write_file`。

对于通过 `patch` 进行基于锚点的追加操作，需将锚点替换为“原锚点+新内容”的组合形式。
而对于没有稳定上下文的简单追加操作，若使用 `terminal` 能够实现最清晰且安全的结果，则也可选用该方式。

## 定向编辑

当当前笔记内容已提供足够的稳定上下文时，可使用 `patch` 对笔记进行精准修改。相比使用 Shell 命令重写文本，这种方式更为高效。

## 维基链接

Obsidian 使用 `[[笔记名称]]` 语法来建立笔记之间的链接。在创建笔记时，可利用此语法关联相关内容。
