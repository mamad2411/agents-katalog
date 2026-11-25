---
name: format-converter
description: 自动识别并在本地双向转换 Unix 时间戳、日期、UTF-8 Base64、Base64 图片和 URL 编码；适用于这几类编码、解码与格式检查，不用于网页抓取或文件压缩。
version: "3.1.0"
install:
  description: 安装格式转换工具箱与本地转换命令
  command: npx @mearl/setup plugin "$SKILL_DIR"
---

# 格式转换

工具箱上方输入内容，下方自动展示转换结果，无需选择类型。普通文字同时展示 Base64 和 URL 编码；编辑或粘贴任意结果可反向转换。图片支持粘贴、选择和拖入。转换在本地运行，不联网或保存内容。

```bash
mearl convert --payload '{"command":"convert","input":{"value":"1700000000","zone":"utc"}}'
mearl convert --payload '{"command":"convert","input":{"value":"5L2g5aW9"}}'
```

返回 `kind` 和可编辑的 `fields`；图片返回一份预览 Data URL `image` 及类型、字节数，元数据不重复包含 Base64。MCP 使用 `plugin_invoke`：`plugin="convert"`、`command="convert"`，`input` 同上。未注册时从本 Skill 的实际目录执行 `npx @mearl/setup plugin "$SKILL_DIR"` 后重试。

- 自动识别是启发式判断。需要确定转换方向时可显式传 `format=timestamp/base64/image/url`、`direction=encode/decode`、字符串 `value`，返回 `{value}` 及适用的元数据。
- 时间戳自动区分秒和毫秒；日期输入展示两种单位。`zone=local/utc`，默认 local；日期接受 `YYYY-MM-DD HH:mm:ss.SSS` 或 ISO 格式，带明确时区偏移时使用该偏移。显式转换可指定 `unit=seconds/milliseconds`。
- Base64 按 UTF-8 处理，兼容换行、无 padding 和 Base64URL。完整 URL（含自定义协议、`//` 开头的地址）保留结构分隔符和已有 `%xx` 转义，只编码中文、空格等字符；普通文本使用组件编码。URL 解码保留完整地址中表示分隔符的转义，`+` 不作为空格处理。
- 图片接受裸 Base64 或 Data URL，按实际字节识别 PNG/JPEG/GIF/WebP。单份原始内容或图片最多 8 MiB。
