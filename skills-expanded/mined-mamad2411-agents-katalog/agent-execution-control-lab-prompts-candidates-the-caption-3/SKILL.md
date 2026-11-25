# docs ルール

- ドキュメントには正規の CLI パスのみを記載する。
- アプリケーションの正規エントリポイントには `python -m src.app.entrypoints.v4_daily_main` / `python -m src.app.entrypoints.monthly_main` / `python -m src.app.entrypoints.weekly_main` を使う。
- `python -m src.app.entrypoints.daily_main` と `python -m src.app.entrypoints.collection_main` は `legacy/v3/` へ退避済みで、`src/` 配下には存在しない。
- 開発者向けツールには `python scripts/dev/...` または `bash scripts/dev/...` を使う。
- `main.py` / `monthly_main.py` / `collection_main.py` などのルートエントリポイント shim は記載しない。
- `python tools/...` コマンドは記載しない。
- ローカルの配置ルールをドキュメントへ繰り返さず、最も近いディレクトリの `AGENTS.md` へのリンクを優先する。

# 仕様・設計
- 仕様・設計ドキュメントは、既存同種ドキュメントの構成に従う。
- 既存同種ドキュメントがない場合は、作成前に構成案を提示して確認する。
- 未決事項は、仕様・設計として確定せず、未決事項として明示する。
- 説明・テンプレート・記載例は how-to に置く。
