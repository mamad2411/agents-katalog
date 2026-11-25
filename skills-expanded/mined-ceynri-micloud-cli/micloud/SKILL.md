---
name: micloud
description: 小米云服务（i.mi.com）命令行工具 micloud：读写、搜索、导出、双向同步小米云笔记；列出、下载、增量拉取小米云录音到本地并清理云端。当用户提到"小米笔记"、"小米云笔记"、"小米录音"、"小米云录音"、"通话录音/微信录音拉到本地"、"清理云端录音"、"micloud"、"mi-note-cli"时触发。
---

# micloud

操作小米云服务（i.mi.com）的 CLI，通过 `npx -y micloud-cli <命令>` 执行（已全局安装时直接用 `micloud`），无需提前安装。

先按任务读对应的参考文档，再执行命令：

- 笔记（读写、搜索、文件夹、图片、导出、同步）→ [references/note.md](references/note.md)
- 录音（列出、下载、增量拉取、删除、回收站）→ [references/recording.md](references/recording.md)

## 通用约定

- **始终加 `--json`**：成功是 `{"ok":true,"data":...}`，失败是 `{"ok":false,"error":"..."}`。退出码 2 表示部分失败：仍是 `ok:true`，失败项列在 `data` 里，每次都要检查并向用户报告。
- **登录**：报「未登录」时，请用户在自己的终端运行 `npx -y micloud-cli login`（会打开浏览器）。登录态之后自动续期，不要反复让用户登录。`whoami --json` 查看账号与云空间用量。
- **删除**：删除类命令在 `--json` / 非交互下不带 `-y` 会直接报错。执行前先用 `--dry-run` 或列表命令拿到受影响的条目，向用户展示数量与标题，用户明确同意后再加 `-y`。永久删除（purge）不可恢复，即使用户已同意删除，也要单独再确认一次。
- **绝对禁止**：凭标题相似或时间接近推断是同一条笔记 / 录音就删除；未经用户确认就批量删除全部内容。
- 选项细节以 `npx -y micloud-cli <命令> --help` 为准；与本文档不一致时先看 help，或运行 `npx skills update micloud` 更新 skill。
