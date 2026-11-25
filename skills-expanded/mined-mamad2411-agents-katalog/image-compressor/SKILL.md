---
name: image-compressor
description: 添付された複数の画像を一括で圧縮・リサイズするスキル。「画像を圧縮して」「このスクショを軽くして」「リサイズして」「画像を小さくして」などのリクエストで使用する。Pillowで長辺1920pxにリサイズし、JPEG/PNGで出力先ディレクトリに保存する。
license: MIT
author: shohei
version: 1.0.0
---

# 画像圧縮・リサイズ

添付された画像を一括で圧縮・リサイズして出力先ディレクトリに保存するスキル。

## 実行手順

1. ユーザーが添付した画像パスを収集する
2. ユーザーの指示から出力フォーマット（`jpg` / `png`）、長辺サイズ、品質などの指定を抽出する
3. 以下のコマンドを実行する

基本（元の拡張子を維持、長辺1920px）:

```bash
python .claude/skills/image-compressor/scripts/compress_images.py "画像1" "画像2" "画像3"
```

JPGで出力:

```bash
python .claude/skills/image-compressor/scripts/compress_images.py "画像1" "画像2" --format jpg
```

PNGで出力、長辺1280px、品質90:

```bash
python .claude/skills/image-compressor/scripts/compress_images.py "画像1" --format png --max-size 1280 --quality 90
```

1. 出力パスと圧縮結果をユーザーに報告する

## 引数

| 引数         | 説明                              | デフォルト       |
| ------------ | --------------------------------- | ---------------- |
| `images`     | 入力画像パス（可変長・必須）      | —                |
| `--format`   | 出力フォーマット（`jpg` / `png`） | 元の拡張子を維持 |
| `--max-size` | 長辺の最大ピクセル数              | `1920`           |
| `--quality`  | JPEG品質（1-100）                 | `85`             |

## 設定

プロジェクトルートの `.env` に以下の環境変数を設定する（任意。未設定時はデフォルト値を使用）:

```text
IMAGE_COMPRESS_OUTPUT_PATH=images/compressed
```

| 変数名                       | 説明                                                  |
| ---------------------------- | ----------------------------------------------------- |
| `IMAGE_COMPRESS_OUTPUT_PATH` | 出力先ディレクトリ（デフォルト: `images/compressed`） |

## 出力

- ファイル名: 元ファイル名をそのまま使う（`photo.jpg` → `photo.jpg`）。同名ファイルが既に存在する場合のみ `_1`, `_2` … と連番を付与
- 保存先: プロジェクトルートの `images/compressed/`
- JPEG出力時、RGBA画像は白背景で合成してRGBに変換する
- 長辺が `--max-size` 未満の場合はリサイズせず圧縮のみ行う

## 依存パッケージ確認

初回エラー時は以下でインストール:

```bash
pip install pillow python-dotenv
```
