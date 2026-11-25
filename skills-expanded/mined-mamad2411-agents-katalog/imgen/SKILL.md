---
name: imgen
description: Azure OpenAI画像生成CLIツール (gpt-image-1.5 / gpt-5.1)。テキストから画像生成、画像のAI編集、画像の内容説明を行う。Use when the user wants to (1) generate images using Azure OpenAI, (2) edit existing images with AI, (3) explain image contents. Triggers on "画像を生成", "画像を編集", "画像の説明", "generate an image", "edit this image", "describe this image", "imgenで".
---

# imgen - Azure OpenAI Image Generation CLI

## How to Run

imgen is NOT globally installed. Use one of these methods:

```bash
# 開発モード（ソースから直接実行、.envを自動読み込み）
npm run dev --prefix /Volumes/Data/dev/imgen -- <command>

# npx でソースから実行（.envは自動読み込みされない）
npx tsx /Volumes/Data/dev/imgen/src/index.ts <command>

# npm パッケージとして実行（npm install -g @nogataka/imgen 済みの場合）
imgen <command>
```

以下の例では `imgen` と表記するが、実際は上記いずれかの方法で実行すること。

## Quick Reference

```bash
imgen image gen "<prompt>" -q <quality> -s <size>    # 画像生成
imgen image edit <file> "<instruction>"               # 画像編集
imgen image explain <file> -l <lang>                  # 画像説明
```

## Setup

環境変数または `.env` ファイルで Azure OpenAI の認証情報を設定する。

```bash
# 環境変数（最優先）
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-5.1"
export AZURE_OPENAI_DEPLOYMENT_NAME_IMAGE="gpt-image-1.5"
```

`.env` ファイル探索順: `cwd/.env` → `~/.imgen/.env`

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint | (required) |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | (required) |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Chat model deployment | (required) |
| `AZURE_OPENAI_DEPLOYMENT_NAME_IMAGE` | Image model deployment | (required) |
| `AZURE_OPENAI_API_VERSION` | Chat API version | 2024-02-15-preview |
| `AZURE_OPENAI_IMAGE_API_VERSION` | Image API version | 2025-04-01-preview |

## Image Generation

```bash
imgen image gen [options] <theme>
```

| Option | Values | Default |
|--------|--------|---------|
| `-s, --size` | 1024x1024, 1536x1024, 1024x1536 | 1024x1024 |
| `-q, --quality` | low, medium, high | high |
| `-f, --format` | png, jpg, webp | png |
| `-p, --preset` | builtin preset name | - |
| `-c, --context` | context file path (.md/.txt) | - |
| `-o, --output` | output path (file or directory) | auto |
| `-d, --debug` | enable debug logging | false |
| `--json` | JSON output format | false |
| `--dry-run` | preview settings without API call | false |

### Recommended Settings

| Use Case | Quality | Size |
|----------|---------|------|
| Product photo, landscape | high | 1536x1024 |
| Illustration, icon, mascot | high | 1024x1024 |
| Quick draft, prototype | low | 1024x1024 |
| Portrait, vertical | high | 1024x1536 |

### Examples

```bash
imgen image gen "夕日の海辺の風景" -q high -s 1536x1024
imgen image gen "可愛い猫のマスコット" -p builtin:square
imgen image gen "ミニマルなロゴデザイン" -o logo.png
imgen image gen "complex scene" --dry-run
```

## Image Editing

```bash
imgen image edit [options] <file> <prompt>
```

Edit instructions in natural language:
- Background change: "背景を青空に変更"
- Style transfer: "水彩画風に変換"
- Object modification: "色を鮮やかに"

Supported input formats: .jpg, .jpeg, .png, .gif, .webp

| Option | Values | Default |
|--------|--------|---------|
| `-s, --size` | 1024x1024, 1536x1024, 1024x1536 | 1024x1024 |
| `-f, --format` | png, jpg, webp | png |
| `-o, --output` | output path | auto |
| `--json` | JSON output format | false |
| `--dry-run` | preview settings without API call | false |

### Examples

```bash
imgen image edit photo.jpg "背景を青空に変更"
imgen image edit portrait.png "アニメスタイルに変換" -s 1536x1024
imgen image edit photo.png "edit" --dry-run
```

## Image Explanation

```bash
imgen image explain [options] <file>
```

| Option | Values | Default |
|--------|--------|---------|
| `-l, --lang` | ja, en, zh, ko, es, fr, de, it, ru, vi | ja |
| `-f, --format` | markdown, json | markdown |
| `-c, --context` | context info (text or .md/.txt file path) | - |
| `-o, --output` | output file path | stdout |

### Examples

```bash
imgen image explain screenshot.png
imgen image explain photo.jpg -l en
imgen image explain chart.png -c "Q4 sales report" -f json
```

## Builtin Presets

`-p` オプションで指定可能:

| Name | Size | Quality |
|------|------|---------|
| `builtin:square` | 1024x1024 | high |
| `builtin:landscape` | 1536x1024 | high |
| `builtin:portrait` | 1024x1536 | high |
| `builtin:draft` | 1024x1024 | low |
| `builtin:photo` | 1536x1024 | high |

## Option Priority

CLI options > Preset values (`-p`) > Default values
