---
name: aitool-iroiro
description: |
  OpenRouter API / Google GenAI API経由でマルチモーダルAIタスクをCLIから実行するツール群 (aitool-iroiro) の使い方スキル。
  画像生成・画像認識・動画理解・音声文字起こし・音声合成が必要なとき、または `aitool` コマンドを使うタスクが来たときは必ずこのスキルを参照すること。
  具体的には「画像を編集して」「この動画を要約して」「この音声をテキストにして」「テキストを読み上げて」「画像を説明して」などのリクエストが対象。
---

# aitool-iroiro スキル

OpenRouter APIとGoogle GenAI APIを使ったマルチモーダルAI CLIツール群。`aitool` コマンド1本で画像生成・画像認識・動画理解・文字起こし・音声合成を実行できる。

## コマンドリファレンス

### 共通オプション（全コマンドで使用可能）

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--model TEXT` | 使用モデルを上書き | 環境変数またはプログラム内定数 |
| `--api-key TEXT` | APIキーを指定（動画理解はGoogle GenAI、それ以外はOpenRouter） | `.env` / 環境変数 |
| `--timeout FLOAT` | HTTPタイムアウト（秒） | `120.0` |
| `--json` | メタ情報をJSON形式で標準出力に表示 | `False` |
| `--verbose` | 追加ステータスをstderrに表示 | `False` |

---

### `generate-image` — 画像生成

テキストプロンプトから画像生成（t2i）、または入力画像を編集（i2i）する。

```bash
aitool generate-image \
  --text "かわいい猫を追加してください" \
  --output ./output.png \
  [--image ./input.png] \   # 省略するとt2i、指定するとi2i
  [--aspect-ratio 1:1] \
  [--image-size 1K]
```

| オプション | 短縮 | 必須 | 説明 |
|-----------|------|------|------|
| `--text TEXT` | `-t` | ✅ | プロンプトテキスト |
| `--output PATH` | `-o` | ✅ | 生成画像の保存先パス |
| `--image PATH` | `-i` | — | 入力画像パス（複数回指定可） |
| `--aspect-ratio TEXT` | — | — | アスペクト比（例: `1:1`, `16:9`） |
| `--image-size TEXT` | — | — | 画像サイズ（例: `1K`, `2K`, `4K`） |
| + 共通オプション | | | |

**`--json` 出力のキー:** `output`, `model`, `mime`, `message`

---

### `recognize-image` — 画像認識

画像に対してテキストで質問し、回答を得る。

```bash
aitool recognize-image \
  --text "この画像を説明してください" \
  --image ./photo.png \
  [--output ./result.txt]  # 省略すると標準出力
```

| オプション | 短縮 | 必須 | 説明 |
|-----------|------|------|------|
| `--text TEXT` | `-t` | ✅ | プロンプトテキスト |
| `--image PATH` | `-i` | ✅ | 入力画像パス（複数回指定可） |
| `--output PATH` | `-o` | — | テキスト結果の保存先（省略→標準出力） |
| + 共通オプション | | | |

**`--json` 出力のキー:** `output`, `model`

---

### `recognize-video` — 動画理解

ローカル動画または公開YouTube URLに対してテキストで質問し、回答を得る。ローカル動画はGoogle GenAIのFile APIでアップロードしてから処理する。

```bash
aitool recognize-video \
  --text "この動画を要約してください" \
  --video ./meeting.mp4 \
  [--output ./result.txt]

aitool recognize-video \
  --text "章立てして、重要な発言を抽出してください" \
  --video "https://www.youtube.com/watch?v=..." \
  --fps 0.5 \
  --structured-output \
  --output ./video-analysis.json
```

| オプション | 短縮 | 必須 | 説明 |
|-----------|------|------|------|
| `--text TEXT` | `-t` | ✅ | プロンプトテキスト |
| `--video TEXT` | `-v` | ✅ | 入力動画パス、または公開YouTube URL |
| `--output PATH` | `-o` | — | テキスト/JSON結果の保存先（省略→標準出力） |
| `--structured-output` | — | — | 組み込み動画分析スキーマに沿ったJSONを出力 |
| `--fps FLOAT` | — | — | 動画サンプリングのカスタムフレームレート |
| + 共通オプション | | | |

**`--json` 出力のキー:** `output`, `model`, `structured_output`, `fps`

注意: YouTube URLは公開動画のみ対応。動画理解では`GEMINI_API_KEY`を使用する。

---

### `transcribe` — 音声文字起こし

音声ファイルをテキストに変換する。

```bash
# STT専用APIを使う（デフォルト）
aitool transcribe --audio ./voice.mp3 [--output ./transcript.txt]

# マルチモーダルLLMに処理させる（プロンプト付き）
aitool transcribe \
  --mode llm \
  --prompt "話者ごとに分けてください" \
  --audio ./meeting.mp3
```

| オプション | 短縮 | 必須 | 説明 |
|-----------|------|------|------|
| `--audio PATH` | `-a` | ✅ | 入力音声ファイルパス |
| `--output PATH` | `-o` | — | テキスト結果の保存先（省略→標準出力） |
| `--format TEXT` | — | — | 音声フォーマット（省略→拡張子から推定） |
| `--mode TEXT` | — | — | `dedicated`（デフォルト）または `llm` |
| `--prompt TEXT` | — | — | `--mode llm` 使用時のプロンプト |
| + 共通オプション | | | |

**`--json` 出力のキー:** `output`, `model`, `mode`

---

### `tts` — 音声合成

テキストから音声ファイルを生成する。

```bash
aitool tts \
  --text "こんにちは。テストです。" \
  --output ./voice.mp3 \
  [--voice alloy] \
  [--format mp3] \
  [--speed 1.0]
```

| オプション | 短縮 | 必須 | 説明 |
|-----------|------|------|------|
| `--text TEXT` | `-t` | ✅ | 合成するテキスト |
| `--output PATH` | `-o` | ✅ | 音声ファイルの保存先パス |
| `--voice TEXT` | — | — | ボイス識別子（デフォルト: `alloy`） |
| `--format TEXT` | — | — | 出力音声フォーマット（デフォルト: `mp3`） |
| `--speed FLOAT` | — | — | 再生速度（モデルが対応している場合） |
| + 共通オプション | | | |

**`--json` 出力のキー:** `output`, `model`, `content_type`, `generation_id`

---

## 困ったときは

### `aitool: command not found` — 未インストールの場合

インストールせずに一時実行する:

```bash
uvx --from git+https://github.com/Nu424/aitool-iroiro.git aitool <サブコマンド> [オプション]
```

または恒久インストール:

```bash
uv tool install git+https://github.com/Nu424/aitool-iroiro.git
```

### `Error: OPENROUTER_API_KEY not found` — OpenRouter APIキー未設定の場合

ユーザーに以下のいずれかを案内する:

**A. カレントディレクトリに `.env` を作る（推奨）:**

```dotenv
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
```

**B. ホームの `~/.env.global` に書く（グローバル設定）:**

```dotenv
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
```

**C. CLI引数で直接渡す（一時的な使用）:**

```bash
aitool generate-image --api-key sk-or-xxx --text "..." --output ./out.png
```

APIキーは https://openrouter.ai/keys で取得できる。

### `Error: GEMINI_API_KEY not found` — Google GenAI APIキー未設定の場合

動画理解を使う場合は、以下のいずれかでGoogle GenAI APIキーを設定する:

```dotenv
GEMINI_API_KEY=xxxxxxxxxxxxxxxx
```

またはCLI引数で直接渡す:

```bash
aitool recognize-video --api-key xxxxx --text "要約して" --video ./video.mp4
```

---

## 参考: API キー・モデルの設定

APIキーとモデルは以下の優先順で解決される（上ほど優先）。

| 優先度 | 方法 |
|--------|------|
| 1 | `--api-key` CLI引数 |
| 2 | カレントディレクトリの `.env` |
| 3 | `~/.env.global` |
| 4 | 環境変数 |

**.env の例:**

```dotenv
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=...

# モデルを変えたい場合（省略時はプログラム内定数が使われる）
AITOOL_IMAGE_GENERATION_MODEL=google/gemini-3.1-flash-image-preview
AITOOL_IMAGE_RECOGNITION_MODEL=google/gemini-3-flash-preview
AITOOL_STT_MODEL=openai/whisper-large-v3-turbo
AITOOL_TTS_MODEL=google/gemini-3.1-flash-tts-preview
AITOOL_VIDEO_RECOGNITION_MODEL=gemini-3.5-flash
```