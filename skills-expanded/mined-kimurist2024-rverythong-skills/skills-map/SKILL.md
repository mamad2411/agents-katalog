---
name: skills-map
description: インストール済みスキルの分野別インデックス兼交通整理。どの作業をどのルーター/スキル/subagentに流すかを一望する。セキュリティ・デザイン・コスト・作業規程などで「どのスキルを使えばいい?」と迷ったとき、または分野が重複して競合しそうなときに最初に開く。
origin: user
---

# skills-map (分野別インデックス)

`~/.claude/skills/` には多数のスキルがあり、うち **830件(cybersecurity 817 + design 13)は `/` メニューから隠してある**(`user-invocable: false`)。Claude は説明文で自動ロードできるが、人は**下の分野ルーターを入口**にする。これで「どれを呼ぶか」の競合を無くす。

## 分野 → 入口(ここから入る)

| 分野 | 入口(ルーター/skill) | 実行者(subagent) | 束ねる対象 |
|---|---|---|---|
| 🔐 セキュリティ | **`/security-ops`** | `security-analyst`(防御)/ `pentest-operator`(攻撃・要認可) | 隠し 817(exploiting-/detecting-/analyzing-/hunting- 他) |
| 🎨 デザイン/フロント | **`/design-taste-jp`**(日本語運用) | — | 隠し 13(`taste-skill`/`minimalist-skill`/`soft-skill` 他)+ 既存 `frontend-design` `ui-ux-pro-max` `design-system` `liquid-glass-design` |
| 💰 コスト/モデル | **`/cost-route`** | — | `cost-report.js`・`ask-kimi`(実装委譲)・`ask-claude`(API直叩き) |
| 🧭 作業規程/品質(meta) | **`/fable`** | — | `/anti-hallucination` `/verification-loop` `/council` |

上表以外(言語別パターン・テスト・DevOps 等の既存スキル)は従来どおり `/` メニューから直接。

## 競合の解き方(重複分野の優先順位)

1. **具体的なルーターを最優先**。デザインなら `/design-taste-jp` → そこから美意識別スキル(`minimalist-skill` 等)を土台に選ぶ。汎用 `design` を直に呼ばない。
2. **隠しスキルは直接呼ばず、ルーター経由 or Claude の自動ロードに任せる**。名前は grep で実在確認(例: `grep -rl kerberoast ~/.claude/skills/*/SKILL.md`)。
3. **meta(fable/anti-hallucination)は常時下敷き**。どの分野の作業でも完了条件と裏取りはここに従う。

## 隠し設定の実体と戻し方

- 隠した830件は各 `SKILL.md` の frontmatter に `user-invocable: false` を付与しただけ(Claude の自動ロードは可、`/` メニューに出ないだけ)。
- 対象リストは `~/.claude/skills/.cyber-skills-manifest.txt`(817)と `.taste-skills-manifest.txt`(13)。
- **メニューに戻す**: 各 SKILL.md の `user-invocable: false` 行を消す(manifest でループ)。**バンドルごと除去**: 各 manifest 冒頭コメント(2行目 `Remove:` 行)のワンライナーで一括削除(`this_file` は実際の manifest パスに置換)。

## 関連
- [[fable]] — 全分野共通の作業規程。
- [[security-ops]] / [[design-taste-jp]] / [[cost-route]] — 各分野ルーター。
