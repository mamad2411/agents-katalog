---
name: make_project
description: 新規プロジェクトの初期構築を行うスキル。新規プロジェクトのセットアップ、初期ファイル作成、Git初期化、既存プロジェクトのアップデートを行う際に使用する。「プロジェクトを初期化して」「新規プロジェクトをセットアップして」「プロジェクトの初期構築をして」「プロジェクトをアップデートして」などのリクエストに対して必ず使用すること。
---

# make_project スキル

## ステップ1：モード選択

作業を開始する前に、ユーザーに以下を必ず口頭で提示し、番号で選択してもらうこと：

「make_project スキルを開始します。以下から実行モードを選択してください：

1. 新規プロジェクトを構成する（親フォルダ上の実行のみ有効）
2. 既存のプロジェクトをアップデートする（プロジェクトフォルダ内での実行のみ有効）
3. その他・相談する

番号を入力してください。」

- **1を選択** → 「モードA：新規プロジェクト作成」へ進む
- **2を選択** → 「モードB：既存プロジェクトのアップデート」へ進む
- **3を選択** → 「モードC：対話」へ進む

---

# モードA：新規プロジェクト作成

## A-1. 事前確認
以下の情報をユーザーに確認してから作業を開始する：
- プロジェクト名（フォルダ名）：[USER_INPUT]
- GitHubリポジトリURL：[USER_INPUT]
- デフォルトブランチ名：main（変更がある場合はユーザーに確認）
- **このプロジェクトは「論文執筆プロジェクト」ですか？（Y/n）**
  - Y の場合 → `[PAPER_PROJECT]=true` とし、A-3 サブフォルダ作成の後に **A-3b**（論文用追加セットアップ）を実施
  - n の場合 → 通常のA-3のみ実施
  - Y の場合は追加確認：
    - 想定ジャーナル／会議：[USER_INPUT]（例：Speech Communication, Interspeech, ICASSP など）
    - documentclass（分かれば）：[USER_INPUT]（例：elsarticle + dvipdfmx, IEEEtran, acmart 等）

※ 事前にGitHub上でリポジトリを作成しておくこと（README等は追加しない）

## A-2. プロジェクトフォルダの作成

\```bash
mkdir [PROJECT_NAME]
cd [PROJECT_NAME]
\```

以降の作業はすべてこのフォルダ内で実行する。

## A-3. サブフォルダ作成

\```bash
mkdir -p .agent/skills
mkdir -p .agent/memory
mkdir -p .agent/handoff
mkdir -p .agent/workflows
mkdir -p .claude/commands
mkdir -p .spec
mkdir -p .output
mkdir -p .references
\```

## A-3b. 論文プロジェクト用サブフォルダ作成【`[PAPER_PROJECT]=true` の場合のみ】

A-1 で論文執筆プロジェクトと回答された場合、以下を追加で作成する：

\```bash
# 論文原稿・コンパイル用
mkdir -p latex原稿/sections

# 情報源（修論・過去原稿・関連発表の格納用、読み取り専用）
mkdir -p _ref

# AIと人間の共有作業スペース
mkdir -p _AI用_関連各種データ/数値計算検証

# 参考文献ハルシネーション検証
mkdir -p 参考文献確認作業/PDFs/user_download

# 一括置換・Excel生成などad-hocスクリプト置き場
mkdir -p 論文修正作業用スクリプト

# 過去バージョン・退避用
mkdir -p _過去のもの
\```

**各フォルダの役割**（`~/.claude/skills/paper_writing/SKILL.md` §8.7 参照）：
- `latex原稿/` : LaTeX ソース、投稿対象の原稿
- `_ref/` : **情報源**（修論・過去論文・既存原稿）。全ての数値・事実の出典。原則読み取り専用
- `_AI用_関連各種データ/` : AI と人間の共有作業スペース（数値検証スクリプト、トレーサビリティ資料）
- `参考文献確認作業/` : refs.bib の検証証跡（Excel + PDF）
- `論文修正作業用スクリプト/` : 一括置換等の ad-hoc スクリプト
- `_過去のもの/` : 退避・バックアップ

## A-4. 初期ファイル作成

### README.md

README.mdが存在しない、あるいは中身が空の時のみ以下を実行する。
プロジェクト名はA-1で確認済みのものを使用する。日時はローカル時刻、ツール名は現在使用中のツール名（例：Claude Code Opus 4.6）を記載する。

\```bash
cat << 'EOF' > README.md
# Project: [PROJECT_NAME]

* これは[YYYY-MM-DD HH:MM]に自動生成されたプロジェクトである
* 初期構築担当ツール名：[TOOL_NAME]
* このプロジェクトでは、生成AIおよびスキルを積極的に活用して開発する
EOF
\```

### .agent/memory/MEMORY.md
\```bash
cat << 'EOF' > .agent/memory/MEMORY.md
# MEMORY

## プロジェクト概要

## 学習した知識・教訓
EOF
\```

### .agent/handoff/HANDOFF.md
\```bash
cat << 'EOF' > .agent/handoff/HANDOFF.md
# HANDOFF

初回セットアップ完了。作業を開始してください。
EOF
\```

### CLAUDE.md（プロジェクトルート）
\```bash
cat << 'EOF' > CLAUDE.md
- セッション開始時に共通ルールである、AGENTS.mdを必ず読み込むこと。
- 読み込んだことを最初に報告すること
- 以下は Claude Code固有の差分のみ記載する
EOF
\```

### GEMINI.md（プロジェクトルート）
\```bash
cat << 'EOF' > GEMINI.md
- セッション開始時に共通ルールである、AGENTS.mdを必ず読み込むこと。
- 読み込んだことを最初に報告すること
- 以下は Gemini 固有の差分のみ記載する
EOF
\```

### AGENTS.md（プロジェクトルート）
\```bash
cat << 'EOF' > AGENTS.md
# Project guide line

## プロジェクトの原則
- 本プロジェクトのプラン作成、および回答は全て日本語で行う

## プロジェクトの目的
- 

# Memory & Handoff Instructions

## 3ファイルの役割と哲学
- 本ファイル（AGENTS.md）は「厳格なルール」、人が作成
- MEMORY.mdは「積み上がる経験」、AIが作成・AIが利用
- HANDOFF.mdは「セッション間の引き継ぎ」、AIが作成・AIが利用、ただし人間がレビューし必要な情報をキュレーションする

## セッション開始時（必須）
セッション開始時、ユーザーへの最初の応答の前に、以下の2ファイルを読み込み、読み込んだことを報告すること：
- `.agent/memory/MEMORY.md`  （学習した知識・教訓）
- `.agent/handoff/HANDOFF.md` （前回の作業引き継ぎ）

## メモリ管理
- 新しい知識・教訓を記録する際は `.agent/memory/MEMORY.md` を更新
- 既存のMEMORY.mdを更新する前に、現在のファイルを`.agent/memory/YYYY-MM-DD.md` にアーカイブしてから新規作成
- ローカルの自動メモリ機能（~/.claude/ 配下）は使用しない
- MEMORY.mdは200行以内を維持すること
- 本ファイルと重複する内容はMEMORY.mdに書かない

## ハンドオフ管理
- ハンドオフは `/handoff` コマンドで作成（Claude Codeの場合）
- 保存先は `.agent/handoff/HANDOFF.md`（固定名）
- 作成時は既存ファイルを `.agent/handoff/YYYY-MM-DD-HHMM.md` にリネームしてからHANDOFF.mdを新規作成する
- 時刻はローカル時刻・24時間表記

## 仕様駆動開発（SDD）ルール
- コーディングや業務作業を開始する前に、必ず `.spec/` 配下の4ファイルを確認・更新すること
- 作業の順序：PLAN（目的確認）→ SPEC（要件確認）→ TODO（タスク確認）→ 実作業
- **PLAN.mdは人間の口頭メモ・自由記述**であり、箇条書き・口語・断片的な内容で構わない
- PLAN.mdを読んだら、そのまま実装に入らず、不明点をヒアリングしながらSPEC.mdを作成・確定させること
- SPEC.mdが確定してからTODO.mdのタスク分解を行い、ユーザーの承認を得てから実作業を開始する
- 作業完了後は TODO.md の該当タスクにチェックを入れ、KNOWLEDGE.md に学びを記録する
- 仕様が不明確な場合は作業を開始せず、ユーザーに確認してから SPEC.md を更新する
- 新しい開発サイクルを始める際は `/newplan` コマンドを使用する

## フォルダ用途
- `.spec/`：設計ドキュメント（PLAN / SPEC / TODO / KNOWLEDGE）
- `.output/`：成果物・アウトプット（記事MD、コード、資料など完成したもの）
- `.references/`：参考資料・素材（PDFや画像、URLメモ、サンプルコードなど作業の入力素材）
EOF
\```

## A-4b. 論文プロジェクト用 初期ファイル作成【`[PAPER_PROJECT]=true` の場合のみ】

### CLAUDE.md に論文スキル参照を追記
\```bash
cat << 'EOF' >> CLAUDE.md

## 本プロジェクトのスキル

- このプロジェクトは**論文執筆プロジェクト**である
- 執筆・推敲・査読対応時は `/paper_writing` スキル（`~/.claude/skills/paper_writing/SKILL.md`）を常時参照すること
- 対応ルール：ハルシネーション防止、参考文献検証、数値トレーサビリティ、読者層に合わせた英語表現、セクション構造ルール
EOF
\```

### AGENTS.md のプロジェクト目的欄を論文用に更新
AGENTS.md の `## プロジェクトの目的` セクションを以下に置換：
\```
## プロジェクトの目的
- 学術論文（[想定ジャーナル／会議]）の執筆・投稿
- 執筆時は `/paper_writing` スキルを常時参照（詳細ルールは `~/.claude/skills/paper_writing/SKILL.md`）
\```

### latex原稿/compile.sh テンプレ作成（elsarticle + dvipdfmx 用）
documentclass が `elsarticle` + `dvipdfmx` オプションの場合：

\```bash
cat << 'EOF' > latex原稿/compile.sh
#!/bin/bash
# LaTeX コンパイルスクリプト（Elsevier elsarticle + dvipdfmx パイプライン用）
# Usage: ./compile.sh
cd "$(dirname "$0")"

# 中間ファイル掃除（重複定義エラー防止）
rm -f main.aux main.bbl main.blg main.log main.out main.toc \
      main.dvi main.pdf main.fls main.fdb_latexmk main.synctex.gz

# uplatex 優先、なければ platex にフォールバック
if command -v uplatex >/dev/null 2>&1; then
    LATEX_CMD="uplatex"
    BIBTEX_CMD="upbibtex"
else
    LATEX_CMD="platex"
    BIBTEX_CMD="pbibtex"
fi

echo "Using: $LATEX_CMD + dvipdfmx"

latexmk \
    -e "\$latex = '$LATEX_CMD -interaction=nonstopmode -halt-on-error -synctex=1 %O %S';" \
    -e "\$bibtex = '$BIBTEX_CMD %O %B';" \
    -e '$dvipdf = q/dvipdfmx %O -o %D %S/;' \
    -pdfdvi \
    main.tex

EXIT_CODE=$?
echo ""
echo "=== Compile finished ==="
if [ -f main.pdf ]; then
    echo "Output: main.pdf (succeeded)"
else
    echo "Error: main.pdf was not produced. See main.log."
    exit $EXIT_CODE
fi
EOF
chmod +x latex原稿/compile.sh
\```

※ documentclass が IEEEtran / acmart / sn-jnl / その他 pdflatex 直接対応の場合は、対応する pdflatex 用 compile.sh テンプレに差し替える（paper_writing.md §6.3 参照）。

### latex原稿/main.tex 最小ひな形（Elsevier Speech Communication想定）
\```bash
cat << 'EOF' > latex原稿/main.tex
\documentclass[preprint,12pt,authoryear,dvipdfmx]{elsarticle}

\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{tabularx}
\usepackage{xurl}
\usepackage[hidelinks,dvipdfmx]{hyperref}

\journal{[JOURNAL_NAME]}

\begin{document}
\begin{frontmatter}
\title{[PAPER_TITLE]}

\author[aff1]{[First Author]\corref{cor1}}
\cortext[cor1]{Corresponding author}

\affiliation[aff1]{organization={[Institution]}, country={[Country]}}

\begin{abstract}
\input{sections/0_abstract}
\end{abstract}

\begin{keyword}
[keyword1] \sep [keyword2]
\end{keyword}
\end{frontmatter}

\input{sections/1_introduction}
% \input{sections/2_related_work}
% \input{sections/...}

\bibliographystyle{elsarticle-harv}
\bibliography{refs}

\end{document}
EOF
\```

### latex原稿/sections/ 最小ひな形
\```bash
cat << 'EOF' > latex原稿/sections/0_abstract.tex
% Abstract は最後に書く。ここは仮置き。
EOF

cat << 'EOF' > latex原稿/sections/1_introduction.tex
\section{Introduction}
% Introduction は全体把握後に書く。
EOF
\```

### latex原稿/refs.bib 初期化（空ファイル）
\```bash
touch latex原稿/refs.bib
\```

### _AI用_関連各種データ/ 初期テンプレ
\```bash
cat << 'EOF' > _AI用_関連各種データ/表・数値の参照元情報.md
# 表・数値の参照元情報（トレーサビリティ）

論文中の全ての数値を以下の分類で管理する（`paper_writing.md` §8.8.1 参照）。

| 分類 | 根拠 |
|---|---|
| A | _ref に直接記載 |
| B | _ref から派生計算 |
| C | Python検証済（`数値計算検証/` にスクリプト） |
| X | 削除 |

## 値のリスト

| 数値 | 記載箇所（本文） | 分類 | 出典／計算根拠 | 備考 |
|---|---|---|---|---|
|  |  |  |  |  |
EOF

cat << 'EOF' > _AI用_関連各種データ/数値計算検証/計算過程の説明.md
# 数値計算検証の説明

このフォルダの Python スクリプトは、論文中の数値を `_ref/` 配下の原データから再計算して検証するもの。

## スクリプト一覧

| ファイル | 目的 | 対象数値 | 採用判断 |
|---|---|---|---|
|  |  |  |  |

## 安定性検証

ランダム性を含む計算は `02_verify_stability.py` 等で 10 seed 以上の分散を確認（paper_writing.md §8.8.3 参照）。
EOF
\```

### 参考文献確認作業/ 初期テンプレ
\```bash
cat << 'EOF' > 参考文献確認作業/README.md
# 参考文献確認作業

`paper_writing.md` §3.1 に沿って、refs.bib の全引用文献についてハルシネーション検証を行う作業フォルダ。

## ファイル
- `参考文献チェック.xlsx`: 全引用文献の検証結果（自動生成スクリプトは `論文修正作業用スクリプト/` 側）
  - Sheet 1: 全文献検証
  - Sheet 2: Table 1（Related Work Table）検証（ある場合）
- `PDFs/[cite_key]_[1stAuthor姓]_[Venue][Year].pdf`: ダウンロードしたPDF
- `PDFs/user_download/`: AIが取得できない分をユーザーが配置する場（AIが後でリネーム）
EOF
\```

## A-5. 仕様駆動開発ファイルの作成（.spec/）

### .spec/PLAN.md
\```bash
cat << 'EOF' > .spec/PLAN.md
# PLAN - やりたいこと

<!-- ここに思ったことを自由に書いてください。箇条書きでも口語でもOK -->
<!-- Claude がこの内容を読んでヒアリングし、SPEC.md を作成します -->
EOF
\```

### .spec/SPEC.md
\```bash
cat << 'EOF' > .spec/SPEC.md
# SPEC - 技術仕様・要件定義

## 機能要件
## 非機能要件
## 技術構成
EOF
\```

### .spec/TODO.md
\```bash
cat << 'EOF' > .spec/TODO.md
# TODO - タスクリスト

## 優先度：高
## 優先度：中
## 優先度：低
## 完了済み
- [x] 初期セットアップ
EOF
\```

### .spec/KNOWLEDGE.md
\```bash
cat << 'EOF' > .spec/KNOWLEDGE.md
# KNOWLEDGE - ドメイン知識・調査結果

## 業務・ドメイン知識
## 調査・リサーチ結果
## 技術的な知見
## 決定事項と理由
EOF
\```

## A-6. newplan コマンドの作成

\```bash
NEWPLAN_CONTENT='以下の手順で新しい開発サイクルを開始してください：

1. `.spec/` 配下の4ファイルが存在する場合、本日の日付（ローカル時刻）でアーカイブする：
   - `PLAN.md`      → `PLAN-YYYY-MM-DD.md`      にリネーム
   - `SPEC.md`      → `SPEC-YYYY-MM-DD.md`      にリネーム
   - `TODO.md`      → `TODO-YYYY-MM-DD.md`      にリネーム
   - `KNOWLEDGE.md` → `KNOWLEDGE-YYYY-MM-DD.md` にリネーム

2. 新しいファイルを以下の通り作成する：
   - `PLAN.md`：空テンプレートで新規作成
   - `SPEC.md`：空テンプレートで新規作成
   - `TODO.md`：空テンプレートで新規作成
   - `KNOWLEDGE.md`：アーカイブした内容をそのままコピーして新規作成（知見を引き継ぐ）

3. 完了後、以下を報告する：
   - アーカイブしたファイル一覧
   - 「新しいPLAN.mdにやりたいことを自由に書いてください」'

printf '%s\n' "$NEWPLAN_CONTENT" > .claude/commands/newplan.md
printf '%s\n' "$NEWPLAN_CONTENT" > .agent/workflows/newplan.md
\```

## A-7. handoff コマンドの作成

\```bash
HANDOFF_CONTENT='以下の手順でハンドオフを作成してください：

1. `.agent/handoff/HANDOFF.md` が存在する場合：
   - そのファイルの更新日時（ローカル時刻）を取得
   - `.agent/handoff/YYYY-MM-DD-HHMM.md` にリネーム

2. 新しい `.agent/handoff/HANDOFF.md` を以下のテンプレートに従って作成し、完了後「HANDOFF.mdを作成しました」と報告してください。各項目には、現在までのチャット履歴や作業内容からAI自身が自己の行動を要約し、具体的な内容を記入してから保存してください。単なる空のテンプレートのまま保存してはいけません。

---
# HANDOFF - {日時}

## 使用ツール
Claude Code / Codex CLI / Gemini CLI など、該当するツール名を記載

## 現在のタスクと進捗
- [ ] タスク名：現在の状況

## 試したこと・結果
- 成功したアプローチ
- 失敗したアプローチ（理由）

## 次のセッションで最初にやること
1. 最初のアクション
2. 次のアクション

## 注意点・ブロッカー
- 注意すべき事項
---'

printf '%s\n' "$HANDOFF_CONTENT" > .claude/commands/handoff.md
printf '%s\n' "$HANDOFF_CONTENT" > .agent/workflows/handoff.md
\```

## A-8. Git初期化

### .gitignore の作成
\```bash
cat << 'EOF' > .gitignore
# Logs
logs
*.log

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
.env
EOF
\```

**`[PAPER_PROJECT]=true` の場合、以下を .gitignore に追記**：

\```bash
cat << 'EOF' >> .gitignore

# --- LaTeX intermediates ---
*.aux
*.bbl
*.blg
*.log
*.out
*.toc
*.dvi
*.fls
*.fdb_latexmk
*.synctex.gz

# PDF 成果物は管理対象（投稿用途）。コンパイル直後のテンポラリは除外
# main.pdf は追跡する（必要に応じて個別に調整）

# 参考文献PDF は Git 管理外（著作権・サイズのため）
参考文献確認作業/PDFs/*.pdf
参考文献確認作業/PDFs/user_download/

# _過去のもの／退避ファイル
_過去のもの/
EOF
\```

### Git初期化とpush
\```bash
git init
git add .
git commit -m "first commit"
git remote add origin [USER_INPUT]
git push -u origin main
\```

## A-9. 完了報告

全手順完了後、以下を報告する：
- 作成したファイル・フォルダの一覧
- GitHubへのpush結果
- 次のステップの案内（「AGENTS.mdにプロジェクト概要を記載し、PLAN.mdにやりたいことを書いてください」など）

**`[PAPER_PROJECT]=true` の場合は追加で案内**：
- `_ref/` に修士論文・過去原稿・関連発表を格納してください（全ての数値・事実の情報源）
- `latex原稿/main.tex` の `[PAPER_TITLE]` `[JOURNAL_NAME]` 等のプレースホルダを埋めてください
- `latex原稿/compile.sh` で `./compile.sh` を試し、LaTeX環境が機能するか確認してください
- 論文執筆時は `/paper_writing` スキルを参照（もしくは `~/.claude/skills/paper_writing/SKILL.md` を確認）

---

# モードB：既存プロジェクトのアップデート

## B-1. 現状の精査

本スキル（make_project）のモードAのA-3以降に記載されているすべての要素を正として、
現在のプロジェクトフォルダの状態と照合し、不足・未作成の要素をリストアップする。

**論文プロジェクト判定**：以下のいずれかが該当すればユーザーに「これは論文執筆プロジェクトですか？（Y/n）」と確認する：
- `latex原稿/` または類似のLaTeXソースフォルダが存在
- `.tex` ファイルが存在
- `refs.bib` が存在
- CLAUDE.md / AGENTS.md で論文・ジャーナル・会議への言及がある

Y の場合は A-3b / A-4b / A-8 の論文用追加要素も差分検査対象に含める。

精査完了後、以下を報告する：
「以下の差分が見つかりました。アップデートを適用してよいですか？
- 追加・作成するもの：[不足している要素の一覧]
- スキップするもの（既存）：[すでに存在する要素の一覧]」

ユーザーの承認を得てから B-2 に進む。

## B-2. 差分の適用

B-1で不足と判定された要素のみ、モードAの対応する手順を実行する。
既存ファイル・フォルダは上書きしない。
AGENTS.mdへの追記は既存内容と重複しないよう確認してから行う。

## B-3. 完了報告

適用した内容とスキップした内容の一覧を報告する。

---

# モードC：対話

ユーザーの相談内容をヒアリングし、このスキルの範囲でできることを提案する。
必要に応じてモードAまたはモードBへ誘導する。


---

# 共通ルール追記（2026-08-05 西村先生指示）

新規プロジェクト作成時、AGENTS.md の「プロジェクトの原則」に以下を必ず含めること：

- ユーザーに情報提示や確認を行う際は、.md ではなく **HTML で提示する**（作成後 `open` でブラウザ表示）。コピペが崩れる場合のみ .md を併用してよいが、その際は HTML 側に「コピペ用に .md も作成した」旨とパスを記載すること

---

# 共通ルール追記（2026-08-19 西村先生指示）：Drive アーカイブの自動セットアップ

新規プロジェクト作成時（モードA）および既存プロジェクト更新時（モードB）に、以下を**ユーザーの指示を待たずに**必ず実施する。
背景：`~/_data/work/` は自動バックアップされない AI 作業場、`~/Library/CloudStorage/GoogleDrive-sayonari@gmail.com/マイドライブ/nishimura/` は正本・アーカイブ（自動バックアップ）。詳細ルールと Drive 内マップは `~/.claude/CLAUDE.md`「作業領域の2層構造とDriveアーカイブ」を参照。

## A-3c. Drive アーカイブ先の決定と同期スクリプト作成
1. プロジェクトの内容から Drive 内の保存先を判断する（例：留学生受入 → `project/_豊橋技術科学大学/<年度>/研究室学生/<PROJECT_NAME>/`、科研費 → `document/研究費/科研費/<PROJECT_NAME>/`、講義 → `project/_豊橋技術科学大学/<年度>/<講義名>/`）。判断に迷う場合のみユーザーに確認する
2. `.agent/scripts/sync_to_drive.sh` を以下の雛形で作成し、`chmod +x` する（DST を差し替える）
3. `CLAUDE.md` に「本プロジェクトの正本アーカイブ先（Google Drive）：<DST>．成果物・受領書類は作業の区切りごとに `.agent/scripts/sync_to_drive.sh` で同期すること」を追記する
4. 初回同期を実行し、完了報告に Drive 側パスを含める

```bash
mkdir -p .agent/scripts
cat << 'EOF2' > .agent/scripts/sync_to_drive.sh
#!/bin/bash
# 本プロジェクトの整理済みデータを Google Drive（自動バックアップ領域）へ同期する
set -e
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
DST="/Users/sayonari/Library/CloudStorage/GoogleDrive-sayonari@gmail.com/マイドライブ/nishimura/[DRIVE_SUBPATH]/[PROJECT_NAME]"
mkdir -p "$DST"
EXC=(--exclude '.git' --exclude '.DS_Store' --exclude '_ocr' --exclude 'node_modules' --exclude '*.log')
rsync -av --delete "${EXC[@]}" "$SRC/.references/" "$DST/01_受領書類・メール/"
rsync -av --delete "${EXC[@]}" "$SRC/.output/"     "$DST/02_成果物/"
rsync -av --delete "${EXC[@]}" "$SRC/.spec/"       "$DST/03_記録/spec/"
rsync -av --delete "${EXC[@]}" --exclude 'scripts' "$SRC/.agent/" "$DST/03_記録/agent/"
cp "$SRC/README.md" "$SRC/AGENTS.md" "$DST/03_記録/" 2>/dev/null || true
echo "synced -> $DST"
EOF2
chmod +x .agent/scripts/sync_to_drive.sh
```

※ 論文プロジェクトなど `.output/` 以外に成果物がある場合（`latex原稿/main.pdf` 等）は rsync 行を追加する。巨大データ・生データ・中間生成物は同期しない。
