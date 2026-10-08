---
name: mux
description: Batch convert all .mov videos in workspace/mux-input/. For each MOV, auto-pairs with a prefix-matching external audio file (.mp4/.wav/.aiff, APAC or LPCM auto-detected) if available, otherwise uses embedded Ambisonics (4/9/16ch). Primary spatial audio is output as APAC; if the same MOV also embeds mono/stereo, that track is passed through as a second audio track (fallback). Outputs to workspace/mux-output/. Prefer .cursor/skills/mux/scripts/batch-mux.sh with required_permissions ["all"]. Use when the user mentions batch mux, APAC, LPCM, WAV, spatial audio, Vision Pro, workspace folder, embedded audio, or processing MOV files.
---

# AmbiMux: workspace/ の MOV を一括変換（外部オーディオ優先・埋め込みフォールバック）

## 目的

`workspace/mux-input/` 内の **全 `.mov`** に対し、以下の優先順で変換する:

1. **外部オーディオが見つかった場合** — ファイル名が前方一致するオーディオファイル（`.mp4` / `.wav` / `.aiff`）を使って音声差し替え
2. **外部オーディオが見つからない場合** — `.mov` 内の **Ambisonics（4/9/16ch）** を主トラックとして **APAC** で出力。同一ファイル内に **モノ/ステレオ（1/2ch）** の音声もあれば、**第2トラックとしてそのまま（パススルー）** 出力に含める
3. **どちらも使えない場合** — スキップ（警告表示）

## 前提条件

- **APACエンコーダーはサンドボックス内では動作しない**ため、実行は `required_permissions: ["all"]`（サンドボックスなし）とする

## ワークフロー（batch-mux.sh）

変換の本体は **[batch-mux.sh](scripts/batch-mux.sh)**（リポジトリからは `.cursor/skills/mux/scripts/batch-mux.sh`）。**毎回 `swift build -c release`**、入力の列挙・外部音声の前方一致（`.mp4` → `.wav` → `.aiff`）、埋め込みの `ffprobe` 判定（`channels=` が 4 / 9 / 16 のトラックの有無）、各 `.mov` への `ambimux` 呼び出し（常に `--audio-output apac`）、終了時の処理サマリまで行う。

1. リポジトリルートからスクリプトを実行する（**必ずサンドボックス外**）。

```bash
.cursor/skills/mux/scripts/batch-mux.sh
```

## ペアリングと出力のルール（スクリプトと同じ）

| 項目 | 内容 |
|------|------|
| 外部音声の優先 | `.mp4` → `.wav` → `.aiff`。`<movのベース名>` で始まるファイルを入力ディレクトリ直下から1件選ぶ（例: `video_abc.mov` → `video_abc*.mp4` など） |
| 埋め込みフォールバック | 外部が無いとき、音声ストリームのうち **4 / 9 / 16ch が1本でもあれば** 埋め込みで変換対象。それ以外はスキップ |
| 出力パス | `<ベース名>_ambimux.mov`（既存と重なる場合は `_1` 等でユニーク化。**ambimux** 側の挙動） |
| 主トラック | 常に **`--audio-output apac`**。入力が APAC ならコピー、LPCM なら APAC エンコード |
| 外部音声利用時 | 映像側に 1/2ch の埋め込みがあれば **第2トラックとしてパススルー**（フォールバック） |

## フォルダ構造

```
workspace/
├── mux-input/        # 入力（.mov + 任意の外部オーディオ）
└── mux-output/       # 出力（変換済み .mov）
```

`workspace/` は `.gitignore` 想定。出力は常に `.mov`。

## エラーハンドリング

### `invalidChannelCount`

**原因:**
- 外部オーディオパス: `--audio` ファイルが 4・9・16 チャンネルの LPCM ではない
- 埋め込みパス: 映像内に **Ambisonics として解釈できる 4・9・16 チャンネル** のトラックがない。モノ/ステレオだけでは主トラックを構成できない

**対処:**
- チャンネル数を確認: `ffprobe -v error -show_streams -select_streams a <file>`

### `noAudioTracksFound` / `audioTrackNotFound`

**原因:**
- 音声ファイルに音声トラックが無い、または読み取れない

**対処:**
- ファイルが破損していないか確認
- 正しい形式のオーディオファイルか確認

### `videoTrackNotFound`

**原因:**
- 動画ファイルにビデオトラックが無い、または読み取れない

**対処:**
- ファイルが破損していないか確認
- 正しい形式の動画ファイルか確認

### `Cannot Encode` (エラーコード -11834)

**原因:**
- サンドボックス内で実行された

**対処:**
- `required_permissions: ["all"]` を指定してサンドボックスなしで実行する

## 例

入力ファイルの組み合わせの参考は [examples.md](examples.md)。実行手順は上記 **batch-mux.sh** のみとする。
