---
name: tinypng-compress
description: 通过 Mearl 工具箱或 CLI 压缩 PNG、JPEG、WebP 图片并下载结果。适用于用户明确要求使用 TinyPNG 压缩图片；图片将上传到外部服务，不用于图片编辑或私有离线压缩。
install:
  description: 安装并注册图片压缩工具箱插件
  command: npx @mearl/setup plugin "$SKILL_DIR"
version: "3.1.0"
---

# 图片压缩

通过 `file` 压缩执行宿主上的 PNG、JPEG、WebP，每张最多 5 MiB。图片会上传到 TinyPNG；仅在用户明确要求压缩指定图片时调用，探索或验证不可擅自上传用户文件。

```bash
mearl tinypng --payload '{"command":"file","input":{"filePath":"/tmp/input.png","outputPath":"/tmp/input-compressed.png"}}'
```

- `filePath` 和 `outputPath` 属于执行宿主；输出必须是尚不存在的新文件，不覆盖原图。
- 返回原始文件名、大小、类型，压缩后的大小、类型、尺寸，以及输出路径。不创建工具箱任务。
- 遇到域权限错误时，按 Mearl 的 `request_permission` 流程授权 `tinify.cn` 后重试。上传结果不明确时不要自动重复上传，先向用户说明。
- 用户也可在工具箱「图片压缩」中选择、拖入或粘贴图片，预览、复制或下载结果。列表和批次管理仅供工具页面使用。

未注册时，从当前 Skill 实际目录执行 `npx @mearl/setup plugin "$SKILL_DIR"` 后重试。
