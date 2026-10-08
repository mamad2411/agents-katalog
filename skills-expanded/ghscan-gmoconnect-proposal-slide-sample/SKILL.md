デザイナー（=Nano Banana Pro）の呼び出しをClaude Code Agent Skillにしたい。
他の案件でも再利用できる汎用的なスキルとして作成すること。

## 要件

### 機能
- 画像の新規生成（テキストプロンプトから画像を生成）
- 既存画像の編集（テキスト＋画像入力による画像変換）

### API
- Nano Banana Pro API: https://ai.google.dev/gemini-api/docs/image-generation
- モデル: `gemini-3-pro-image-preview`
- Python SDK (`google-genai`) を使用する（curl ではなく）

### Python SDK の使い方

新規生成:
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K",
        ),
    ),
)
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
```

画像編集（テキスト＋画像入力）:
```python
from PIL import Image

image = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt, image],  # テキストと画像を両方渡す
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K",
        ),
    ),
)
```

### Agent Skill の構成

Agent Skills のドキュメント: https://code.claude.com/docs/en/skills

```
.claude/skills/generate-illustration/
├── SKILL.md                    # メイン指示（YAML frontmatter + ワークフロー）
└── scripts/
    └── generate_image.py       # API呼び出しスクリプト（Claude が実行する）
```

- `SKILL.md`: スキルの説明、使い方、ワークフロー手順を記述
- `scripts/generate_image.py`: コマンドライン引数でプロンプト・入出力パスを受け取る実行スクリプト
  - `--prompt`: 画像生成/編集プロンプト
  - `--output`: 出力ファイルパス
  - `--input`: 編集元画像パス（編集モード時、複数指定可）
  - `--aspect-ratio`: アスペクト比（デフォルト: 16:9）
  - `--image-size`: 画像サイズ（1K/2K/4K、デフォルト: 2K）

### 環境
- Python 仮想環境 (`.venv`) を使用する
- 依存パッケージ: `google-genai`, `Pillow`
- API キー: `.env` の `GEMINI_API_KEY` から読み込む

## 参考
- デザイナーへの指示例: proposal/illustration-request.md
