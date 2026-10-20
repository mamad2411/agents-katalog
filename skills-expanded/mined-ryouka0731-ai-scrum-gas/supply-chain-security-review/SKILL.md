---
name: supply-chain-security-review
description: >
  プロジェクトが依存するサードパーティコンポーネント（ライブラリ、フレームワーク、ツール）のセキュリティを検証する。
  依存パッケージの脆弱性スキャン、バージョン管理、自動更新、ライセンスコンプライアンス、SBOMの生成を確認する。
  「サプライチェーン監査」「依存パッケージ監査」「SBOM監査」「ライセンス確認監査」「Dependabot監査」等のキーワードで使用する。
---

# サプライチェーン セキュリティレビュー

## 目的

プロジェクトが依存するサードパーティコンポーネント（ライブラリ、フレームワーク、ツール）のセキュリティを検証する。

## 作業指示

1. **依存パッケージの脆弱性を網羅的にスキャンする**
   - 技術スタックに応じて以下を実行する：
     ```bash
     # Node.js
     pnpm audit
     pnpm audit --json > pnpm-audit.json

     # Python
     pip install pip-audit
     pip-audit
     pip-audit -f json > pip-audit.json

     # .NET
     dotnet list package --vulnerable
     dotnet list package --vulnerable --include-transitive

     # 汎用（Trivy）
     trivy fs . --scanners vuln --format json --output trivy-vuln.json
     ```

2. **依存パッケージのバージョン管理状態を確認する**
   - ロックファイルが存在し、リポジトリにコミットされているか確認する：
     - `pnpm-lock.yaml`（Node.js）
     - `requirements.txt` のバージョンピン留め（Python）
     - `*.csproj` のバージョン指定（.NET）
   - バージョン範囲指定（`^`、`~`、`>=`）が過度に緩くないか確認する

3. **依存パッケージの自動更新設定を確認する**
   - Dependabot設定ファイル（`.github/dependabot.yml`）が存在するか確認する
   - または Renovate 等の自動更新ツールが導入されているか確認する
   - セキュリティアップデートの自動マージポリシーが設定されているか確認する

4. **ライセンスコンプライアンスを確認する**
   - 依存パッケージのライセンスを一覧化し、プロジェクトのライセンスとの互換性を確認する
   - GPL等のコピーレフトライセンスが混在していないか検証する

5. **SBOM（Software Bill of Materials）の生成を検討する**
   - SBOMが生成・管理されているか確認する
   - 未生成の場合は、以下のツールでの生成を提案する：
     ```bash
     # Trivy による SBOM 生成
     trivy fs . --format cyclonedx --output sbom.json
     ```
