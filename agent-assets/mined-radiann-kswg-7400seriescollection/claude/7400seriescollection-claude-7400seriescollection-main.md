# CLAUDE.md — Claude 専用追記指示（7400 シリーズ IC Collection Database）

> このファイルは **Claude（Claude Code / Cowork / Agent）** 専用の追加指示です。
> 共通指示は [`AGENTS.md`](AGENTS.md) に記載されており、Claude Code が自動で読み込みます。
> 両ファイルに矛盾が生じた場合はこの `CLAUDE.md` を優先してください。
>
> **⚠️ 共通指示を変更する場合は `AGENTS.md` を更新し、`.github/copilot-instructions.md` にも反映してください。**
> **　 `CLAUDE.md` は Claude 固有の内容のみを含むため、AGENTS.md 更新時の反映は不要です。**

---

## Claude での対話型ファクトチェック手順（factcheck-interactive 相当）

Copilot 用の [`.github/prompts/factcheck-interactive.prompt.md`](.github/prompts/factcheck-interactive.prompt.md) と同じワークフローを Claude でも実施する。

1. **対象確認**: 指定の汎用型番（例 `74x00`）について、`usage/{カテゴリ}/{型番}/{型番}.md`・入手履歴・`datasheet_sources.json`・収集状況 JSON を読む。
2. **レンダリング**: `python3 scripts/render_datasheet_pages.py --part {型番}` で PDF を PNG 化（大きい PDF は `--pages 1-10` 等で制限。CMOS 系 / TI SN74HC を優先）。
3. **目視確認 + 信頼度スコアリング**: 各 PNG を Read（画像表示）で確認し、ピン配置 / 真理値表 / 絶対最大定格・推奨動作条件 / 電気特性 / 未使用入力の扱い を読み取り、項目ごとに信頼度 0〜100% を自己評価して報告する。
   - 低下要因の目安: 小さい/かすれ文字 −5〜15%、多列・多行表 −5〜20%、紛らわしい文字（0/O, 1/l, µ/u）−3〜10%、ページまたぎ表 −5〜10%、低画質（モアレ/歪み）−10〜30%
   - 上昇要因: 複数 PDF で相互確認 +5〜10%
4. **ユーザー確認**: **85% 以上は自動確認**（`[x]` 更新）、**85% 未満のみユーザーに目視確認を依頼**。「それっぽい」だけで高信頼度を与えない。信頼度の根拠（何が明瞭/不明瞭か）を述べる。
5. **更新**: 確認済み項目を `- [ ]` → `- [x]` に。確認日・信頼度・参照 PDF を付記（例: `（TI データシートより確認 2026-02-14, 読み取り信頼度 95%）`）。読み取れなかった項目は `- [ ]` のまま。
6. **後片付け**: `datasheets/.cache/pdf_render/{型番}*` の一時 PNG を削除する。

---

## Agent skills

### Issue tracker

Issue は GitHub Issues（`radiann-kswg/7400SeriesCollection`、`gh` CLI 経由）で管理する。See `docs/agents/issue-tracker.md`.

### Triage labels

標準の 5 ラベル（`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`）をそのまま使う。See `docs/agents/triage-labels.md`.

### Domain docs

single-context（リポジトリ直下の `CONTEXT.md` + `docs/adr/`、いずれも未作成、必要時に `/domain-modeling` が作る）。See `docs/agents/domain.md`.
