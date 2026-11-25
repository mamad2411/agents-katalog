---
name: fiction-export
description: |
  导出正文为 .txt、番茄格式 .txt 或 .docx，并给出完本前体检清单。
  本 skill 不伪造 ZIP 归档、封面或平台投稿结果。
  触发方式：/fiction-export、「导出」「完本」「归档」「下载」「导出txt」「我要完本了」。
---
# fiction-export：导出与完本归档

将正文合并为可供发布/备份/分享的格式。

## 导出模式

```bash
# SCRIPTS_DIR 由安装宿主指向本仓库或已安装的 scripts/ 目录。
export PROJECT_ROOT="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
```

### 正文合并

- 合并所有已写章节为一个文件
- 可选格式：.txt（纯文本）/ .docx
- 合并时自动：按章编号排序、去常见 Markdown 格式标记；当前命令不生成目录
- 输出到 `导出/` 目录

```bash
# 导出全部已写章节
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${PROJECT_ROOT}" export \
  --format txt --output "导出/{书名}_完本.txt"
```

### 完本前检查

完本后执行：
1. 最终一致性检查（可选 deep doctor）
2. 合并正文文件
3. 人工确认设定集/大纲/追踪是否需要另行备份
4. 在完成报告中记录字数和章数

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${PROJECT_ROOT}" export \
  --format fanqie --output "导出/{书名}_完本.txt"
```

### 文件清理（需用户明确要求）

- 清理运行时临时文件（`.novel/tmp/`）
- 保留追踪、底本和审查报告等核心数据；本 skill 不自动删除项目文件

## 使用示例

```
> /fiction-export --format docx

✅ 已导出：导出/剑来_完本.docx（45 章，12.3 万字）
```

## 参考

合并脚本由 `scripts/fiction.py` 的 `export` 子命令处理，支持 `txt`、`fanqie` 和 `docx`。
如果使用 `.docx` 格式，脚本尝试导入 Python 的 `python-docx`；未安装时会明确回退为 `.txt`，不会声称生成 Word 文件。
导出的 .txt 文件可直接用于番茄平台投稿。
导出的 .docx 文件可用于自我归档或打印。
---
### 番茄平台投稿注意事项

番茄小说接受 .txt 格式投稿，要求：
- UTF-8 编码（无 BOM）
- 章标题用 `第 X 章` 格式，顶格写
- 正文段之间空一行
- 每章末尾空两行
- 无额外格式标记

本 skill 的 `export` 子命令会去掉常见 Markdown 标题、列表、链接、加粗和代码标记，默认遵守上述规范；
如果正文包含复杂 Markdown/HTML，仍需人工抽查导出结果。
使用 `--format fanqie` 参数可自动适配番茄平台格式要求。
```
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。
