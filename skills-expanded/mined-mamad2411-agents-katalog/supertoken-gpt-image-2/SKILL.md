---
name: supertoken-gpt-image-2
description: Use when generating or saving images through the SuperToken OpenAI-compatible image API, diagnosing model access, or configuring SuperToken image credentials for GPT Image 2.
---

# SuperToken GPT Image 2

通过 SuperToken 兼容 OpenAI 的图片接口生成图片。默认模型是 `gpt-image-2-count`，也可以切换到 `gpt-image-2`。

macOS 和 Linux 使用 `python3` 运行脚本；Windows 使用 `py -3`。输出路径应符合当前操作系统的路径格式。

## 使用前配置

运行时先读取 `SUPERTOKEN_API_KEY`，再读取系统安全存储。若仍未找到 Key，交互式终端会以隐藏方式提示输入。

需要单独配置时，运行当前 Skill 目录下的脚本：

```bash
python3 scripts/setup.py
```

不要把真实 Key 写入 `SKILL.md`、README、提交、Issue 或命令示例。

## 生成图片

定位当前 `SKILL.md` 所在目录，并使用其中的 `scripts/generate_image.py`。调用格式：

```bash
python3 scripts/generate_image.py --prompt "一只坐在阳光里的小猫" --output ./supertoken-kitten.png
```

常用参数：

```bash
python3 scripts/generate_image.py --prompt "一只坐在阳光里的小猫，高清照片风格" --output ./supertoken-kitten.png --size 1024x1024 --quality low
```

- 使用 `--model gpt-image-2` 切换模型。
- 只有用户明确要求格式时才发送 `--format png|jpeg|webp`。
- 只有用户明确要求背景时才发送 `--background transparent|opaque|auto`。
- 使用 `--param key=value` 传递单个额外参数。
- 使用 `--json-params path.json` 传递完整的额外参数对象。

## 结果处理

脚本同时支持 `data[0].url` 和 `data[0].b64_json`。图片先写入 `.part` 文件，完整保存后再替换目标文件。生成请求不会自动重试，避免产生重复费用。

成功后向用户报告模型、文件路径和文件大小。不要显示 API Key 或未经脱敏的响应。

## 问题排查

- `401`：检查 `SUPERTOKEN_API_KEY` 是否有效。
- `403`：检查当前密钥是否有目标模型权限。
- `429`：检查请求频率和账户额度。
- `5xx`：保留请求 ID，并建议用户稍后重试或联系 SuperToken 客服。

## English

Use this Skill to generate images through the SuperToken OpenAI-compatible image API. It defaults to `gpt-image-2-count` and accepts `--model gpt-image-2` as an override.

Run scripts with `python3` on macOS and Linux or `py -3` on Windows. Use an output path supported by the current operating system.

### Setup

Read credentials from `SUPERTOKEN_API_KEY` first, then from the operating-system credential store. For explicit setup, resolve the directory containing this `SKILL.md` and run:

```bash
python3 scripts/setup.py
```

Never put a real API Key in documentation, commits, issues, or command examples.

### Generate an image

Run the bundled generator from the same Skill directory:

```bash
python3 scripts/generate_image.py --prompt "A tiny fluffy kitten sitting in sunlight" --output ./supertoken-kitten.png
```

Use `--model gpt-image-2` for the alternate model. Send `--format`, `--background`, `--param`, and `--json-params` only when the user asks for those options.

### Results and failures

The script accepts either `data[0].url` or `data[0].b64_json`, writes through a `.part` file, and replaces the target only after a complete save. Report the model, output path, and file size. Never expose the API Key or an unsanitized response.

For `401`, check the API Key. For `403`, check model access. For `429`, check rate limits and account credit. For `5xx`, preserve the request ID for SuperToken support. Do not retry image-generation POST requests automatically.
