---
name: sofunny-image
description: 使用 New-API 的 Gemini 原生 `generateContent` 生成或编辑图片。适用于需要文本生图、参考图编辑、输出本地 PNG，并希望复用 `.sofunny-image.env` 或当前 shell 环境变量的场景。
---

# sofunny-image

## 何时使用

在以下场景使用本 skill：

- 用户要生成图片，而当前客户端主模型并不适合直接承担图片输出
- 用户要上传一张或多张参考图，再结合文本生成新图片
- 用户要通过 `New-API` 的 Gemini 原生接口出图，而不是直连 Google 官方 API
- 用户希望优先复用：
  - 进程环境变量
  - `~/.sofunny-image.env`

如果只是普通文本问答、代码生成或工具调用，不要使用本 skill。

## 配置来源

脚本按以下顺序读取配置：

1. `~/.sofunny-image.env`
2. 当前 shell 的环境变量

命令行参数 `--base-url`、`--api-key`、`--model` 会覆盖以上配置。

如果没有检测到 `~/.sofunny-image.env`，脚本会提示你创建该文件并写入所需变量模板。

优先使用这些变量：

- `SOFUNNY_BASE_URL`
- `SOFUNNY_API_KEY`
- `SOFUNNY_MODEL`

默认期望值：

- `SOFUNNY_BASE_URL=http://127.0.0.1:3000`
- `SOFUNNY_MODEL=gemini-3.1-flash-image-preview`

## 安装与执行入口

- 推荐将仓库目录软链接到：
  - `${CLAUDE_PLUGIN_ROOT}/skills/sofunny-image`
- 可执行脚本入口：
  - `${CLAUDE_PLUGIN_ROOT}/skills/sofunny-image/scripts/sofunny-image.js`

## 快速用法

文本生图：

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/sofunny-image/scripts/sofunny-image.js \
  --prompt "生成一张 16:9 的极简香蕉海报，不要任何文字。"
```

参考图编辑：

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/sofunny-image/scripts/sofunny-image.js \
  --prompt "保持主体不变，把背景改成晨雾中的山谷。" \
  --input /absolute/path/to/ref-1.png \
  --input /absolute/path/to/ref-2.jpg
```

指定输出、比例和分辨率：

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/sofunny-image/scripts/sofunny-image.js \
  --prompt "生成一张赛博朋克风格香蕉图标。" \
  --aspect-ratio 1:1 \
  --image-size 2K \
  --output /tmp/banana-icon.png
```

## 参数说明

- `--prompt`：必填，图片生成或编辑指令
- `--input`：可重复传入，一张或多张参考图
- `--output`：可选，输出文件路径
- `--aspect-ratio`：可选，默认 `16:9`
- `--image-size`：可选，默认 `1K`
- `--model`：可选，默认读取配置，兜底为 `gemini-3.1-flash-image-preview`
- `--base-url`：可选，覆盖配置中的 base URL
- `--api-key`：可选，覆盖配置中的 token

## 工作流

1. 收集用户的 prompt、参考图、输出路径和画幅要求。
2. 运行 `scripts/sofunny-image.js`。
3. 脚本会直接调用：
   - `{BASE_URL}/v1beta/models/{MODEL}:generateContent`
4. 脚本从响应中提取最后一个 `inlineData.data`，并将其视为最终图片保存到本地。
5. 把保存路径返回给用户。

## 注意事项

- 本 skill 默认不附带 `tools` 和 `thinking`，避免图片模型在工具模式下失败。
- `BASE_URL` 应为服务根地址，不要手动带 `/v1`。
- 若未指定输出路径，脚本默认保存到：
  - 当前工作目录
- `~/.sofunny-image.env` 中只应使用 `SOFUNNY_*` 变量，避免旧配置混入导致行为不一致。
- 如果 Gemini 在同一次响应中返回多张图片，脚本默认只保存最后一张，前面的图片视为中间产物。
