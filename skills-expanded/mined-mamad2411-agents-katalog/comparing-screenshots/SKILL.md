---
name: comparing-screenshots
description: Compares Figma screenshots with HTML screenshots using pixel-level analysis. Use when verifying visual accuracy of Figma-to-HTML conversion.
allowed-tools: [Read, Bash, mcp__figma__get_screenshot]
---

# Comparing Screenshots

FigmaデザインとHTML生成物のスクリーンショットを比較し、ピクセルレベルで差異を検出するスキル。

## Overview

このスキルは以下を提供します：

1. **HTMLスクリーンショット取得** - Puppeteerを使用したHTML画面キャプチャ
2. **Figmaスクリーンショット取得** - MCP経由でFigma画像を取得
3. **画像比較** - pixelmatchによるピクセル単位の差異検出
4. **差分レポート** - 視覚的な差異の定量化

## Quick Start

```bash
# 1. セットアップ（初回のみ）
cd ~/.agents/scripts/html-screenshot && npm install

# 2. HTMLスクリーンショット取得
node ~/.agents/scripts/html-screenshot/screenshot.js ./index.html

# 3. 画像比較
node ~/.agents/scripts/html-screenshot/compare.js html_screenshot.png figma_screenshot.png diff.png
```

## Workflow

Copy this checklist:

```
Screenshot Comparison Progress:
- [ ] Step 1: Figmaスクリーンショット取得
- [ ] Step 2: HTMLスクリーンショット取得
- [ ] Step 3: 画像比較実行
- [ ] Step 4: 結果解釈と報告
```

---

### Step 1: Figmaスクリーンショット取得

**MCP経由で取得:**

```bash
mcp__figma__get_screenshot(fileKey, nodeId)
```

**APIから取得（代替）:**

```bash
curl -s "https://api.figma.com/v1/images/{fileKey}?ids={nodeId}&format=png&scale=2" \
  -H "X-Figma-Token: {token}" | jq -r '.images["{nodeId}"]'
```

取得したURLからダウンロード:

```bash
curl -L -o figma-screenshot.png "{image_url}"
```

---

### Step 2: HTMLスクリーンショット取得

**基本コマンド:**

```bash
node ~/.agents/scripts/html-screenshot/screenshot.js <html-file> [output-path] [options]
```

**オプション:**

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--width=N` | 375 | ビューポート幅（モバイル） |
| `--height=N` | 812 | ビューポート高さ |
| `--no-full-page` | - | ビューポートのみキャプチャ |
| `--with-mapping` | - | マッピングオーバーレイ表示 |

**例:**

```bash
# モバイルビュー（iPhone X サイズ）
node ~/.agents/scripts/html-screenshot/screenshot.js ./index.html ./html-screenshot.png

# タブレットビュー
node ~/.agents/scripts/html-screenshot/screenshot.js ./index.html ./tablet.png --width=768 --height=1024

# デスクトップビュー
node ~/.agents/scripts/html-screenshot/screenshot.js ./index.html ./desktop.png --width=1440 --height=900
```

**デフォルト動作:**
- Retinaクオリティ（deviceScaleFactor: 2）
- フルページキャプチャ
- マッピングオーバーレイ非表示
- networkidle0 待機

---

### Step 3: 画像比較実行

**基本コマンド:**

```bash
node ~/.agents/scripts/html-screenshot/compare.js <image1> <image2> [diff-output]
```

**例:**

```bash
# 比較のみ
node ~/.agents/scripts/html-screenshot/compare.js html-screenshot.png figma-screenshot.png

# 差分画像も出力
node ~/.agents/scripts/html-screenshot/compare.js html-screenshot.png figma-screenshot.png diff.png
```

**差分画像の解釈:**
- 🔴 赤いピクセル: 差異がある箇所
- 🟢 緑のピクセル: 代替差分色（アンチエイリアス）

---

### Step 4: 結果解釈と報告

**出力結果の解釈:**

| パーセント | ステータス | 意味 |
|-----------|-----------|------|
| 0% | ✅ PIXEL PERFECT | 完全一致 |
| < 1% | 🟡 NEARLY PERFECT | 軽微な差異（フォントレンダリングなど） |
| < 5% | 🟠 NOTICEABLE | 目立つ差異あり |
| ≥ 5% | 🔴 SIGNIFICANT | 大きな差異あり |

**レポート形式:**

```markdown
## スクリーンショット比較結果

| 項目 | 値 |
|------|-----|
| HTML | [ファイルパス] |
| Figma | [nodeId] |
| 差異率 | X.XX% |
| 判定 | ✅/🟡/🟠/🔴 |

### 差分画像
![diff](diff.png)
```

---

## サイズ不一致の処理

画像サイズが異なる場合、ツールは自動的に:

1. 両画像の最大サイズを計算
2. 小さい方を白背景でパディング
3. 同じサイズで比較

**警告メッセージ例:**
```
Warning: Image dimensions differ
  Image 1: 750x1624
  Image 2: 750x1500
  Comparing at: 750x1624 (padding smaller image)
```

---

## トラブルシューティング

| 問題 | 原因 | 対処法 |
|------|------|--------|
| `puppeteer` エラー | 依存関係未インストール | `cd ~/.agents/scripts/html-screenshot && npm install` |
| フォント差異 | システムフォントの違い | Webフォントを使用、または許容する |
| 画像読み込み失敗 | パスが間違っている | 絶対パスを使用 |
| 大きな差異 | レイアウト崩れ | 差分画像を確認して原因特定 |

---

## スクリプトの場所

```
~/.agents/scripts/html-screenshot/
├── screenshot.js    # HTMLスクリーンショット取得
├── compare.js       # 画像比較
├── package.json     # 依存関係定義
└── README.md        # 使用方法
```

---

## 統合例: Figma-HTML比較フロー

```bash
# 1. 出力ディレクトリに移動
cd .outputs/screen-name/

# 2. Figmaスクリーンショット取得（MCPまたはAPI）
# mcp__figma__get_screenshot または curl で取得
curl -L -o figma-screenshot.png "{figma_image_url}"

# 3. HTMLスクリーンショット取得
node ~/.agents/scripts/html-screenshot/screenshot.js ./index.html ./html-screenshot.png

# 4. 比較実行
node ~/.agents/scripts/html-screenshot/compare.js \
  html-screenshot.png \
  figma-screenshot.png \
  diff.png

# 5. 結果確認
# 差異率が5%未満ならOK、それ以上なら修正が必要
```

---

## 成果物フォルダ構造

比較完了後、以下の構造で成果物を格納すること：

```
.outputs/{screen-id}/
├── index.html              # 生成HTML
├── mapping-overlay.js      # マッピング可視化
├── spec.md                 # 画面仕様書
├── assets/                 # アセットファイル
│   ├── *.svg
│   └── *.png
└── comparison/             # ★ 比較成果物フォルダ
    ├── figma.png           # Figmaスクリーンショット
    ├── html.png            # HTMLスクリーンショット
    ├── diff.png            # 差分画像
    └── README.md           # 比較レポート
```

### comparison/ フォルダの作成

```bash
# 1. フォルダ作成
mkdir -p .outputs/{screen-id}/comparison

# 2. ファイルコピー
cp figma-screenshot.png comparison/figma.png
cp html-screenshot.png comparison/html.png
cp diff.png comparison/diff.png

# 3. READMEテンプレート
cat > comparison/README.md << 'EOF'
# Figma-HTML 比較レポート

| 項目 | 値 |
|------|-----|
| 画面ID | {screen-id} |
| 比較日時 | {date} |
| 差異率 | {percentage}% |
| 判定 | {status} |
EOF
```

---

## 成果物チェックリスト

比較完了時に以下を確認すること：

```bash
# 成果物チェックスクリプト
check_comparison_outputs() {
  local dir="$1"
  local missing=0
  
  echo "=== 成果物チェック: $dir ==="
  
  # 必須ファイル
  for f in comparison/figma.png comparison/html.png comparison/diff.png comparison/README.md; do
    if [ -f "$dir/$f" ]; then
      echo "✅ $f"
    else
      echo "❌ $f (MISSING)"
      missing=$((missing + 1))
    fi
  done
  
  if [ $missing -eq 0 ]; then
    echo ""
    echo "✅ すべての成果物が揃っています"
  else
    echo ""
    echo "❌ $missing 個のファイルが不足しています"
  fi
}

# 使用例
check_comparison_outputs .outputs/screen-name
```

### チェックリスト（手動確認用）

```
Comparison Deliverables:
- [ ] comparison/figma.png が存在する
- [ ] comparison/html.png が存在する
- [ ] comparison/diff.png が存在する
- [ ] comparison/README.md が存在する
- [ ] 画像サイズが一致している（両方同じピクセル数）
- [ ] 差異率が記録されている
```

---

## 参照

- **[comparing-figma-html](../../agents/comparing-figma-html.md)**: 視覚比較エージェント（このスキルを使用）
- **[converting-figma-to-html](../converting-figma-to-html/SKILL.md)**: HTML変換スキル
