---
name: config-security-review
description: >
  アプリケーションの設定ファイルやデプロイメント構成にセキュリティ上の問題がないかを検証する。
  Docker、CI/CDパイプライン、IaC（Terraform/Bicep）、環境設定ファイルのセキュリティを確認する。
  「設定ファイルのセキュリティ監査」「Dockerのセキュリティ監査」「CI/CDセキュリティ監査」「IaCスキャン監査」等のキーワードで使用する。
---

# 設定ファイル・構成管理 セキュリティレビュー

## 目的

アプリケーションの設定ファイルやデプロイメント構成にセキュリティ上の問題がないかを検証する。

## 確認対象

- Docker関連ファイル（`Dockerfile`、`docker-compose.yml`）
- CI/CD設定ファイル（`.github/workflows/*.yml`）
- IaCファイル（`*.tf`、`*.bicep`、`*.arm.json`）
- 環境設定ファイル（`.env.example`、`appsettings.json`）

## 作業指示

1. **Dockerファイルのセキュリティを検証する**
   - `Dockerfile` が存在する場合、以下を確認する：
     - ベースイメージが公式かつ最小構成のものか（alpine推奨）
     - rootユーザではなく非特権ユーザで実行されているか
     - 不要なパッケージやツールが含まれていないか
     - マルチステージビルドが活用されているか
   - コンテナイメージの脆弱性スキャンを実行する：
     ```bash
     # Trivy によるファイルシステムスキャン
     trivy fs . --severity CRITICAL,HIGH --format json --output trivy-fs-report.json

     # コンテナイメージスキャン（イメージが存在する場合）
     trivy image <image-name> --severity CRITICAL,HIGH
     ```

2. **CI/CDパイプラインのセキュリティを検証する**
   - `.github/workflows/` 配下のワークフローファイルを確認する
   - 以下を検証する：
     - シークレットがGitHub Secretsで管理されているか（ハードコードされていないか）
     - サードパーティのGitHub Actionsが信頼できるソース（公式またはverified creator）からのものか
     - Actionsのバージョンがコミットハッシュまたは特定タグで固定されているか
     - SAST/SCA/シークレットスキャンがパイプラインに統合されているか
     - ブランチ保護ルールが設定されているか
     - コードレビューの必須化が設定されているか

3. **IaCファイルのセキュリティスキャンを実行する**
   - Terraform/Bicepファイルが存在する場合、以下を実行する：
     ```bash
     # Trivy による IaC スキャン（tfsecの後継）
     trivy config . --severity CRITICAL,HIGH --format json --output trivy-iac-report.json

     # Checkov による IaC スキャン
     checkov -d . --output json > checkov-report.json
     ```
   - IaCコードに以下のベストプラクティスが適用されているか確認する：
     - リソースへのパブリックアクセスが最小化されているか
     - 暗号化がデフォルトで有効化されているか
     - ネットワークアクセスが必要最小限に制限されているか
     - タグ付けやリソース命名規則が統一されているか

4. **環境設定ファイルのセキュリティを検証する**
   - `.env.example` が存在する場合、実際の値やシークレットが含まれていないか確認する
   - `appsettings.json` 等の設定ファイルで以下を確認する：
     - 本番環境のデバッグモードが無効化されているか
     - 接続文字列にシークレットが直接記載されていないか
     - ログレベルが本番環境に適切な設定か（DEBUGは不可）
