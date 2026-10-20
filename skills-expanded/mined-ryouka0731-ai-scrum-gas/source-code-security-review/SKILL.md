---
name: source-code-security-review
description: >
  ソースコードに潜在するセキュリティ脆弱性を特定し、OWASP Top 10:2025に基づく網羅的なコードレビューを実施する。
  シークレット漏洩、依存パッケージ脆弱性、認証・認可、入力検証、暗号化、APIセキュリティを検証する。
  「コードセキュリティ監査レビュー」「ソースコードのセキュリティ監査」「脆弱性監査チェック」「コード監査」等のキーワードで使用する。
---

# ソースコード セキュリティレビュー

## 目的

ソースコードに潜在するセキュリティ脆弱性を特定し、OWASP Top 10:2025に基づく網羅的なコードレビューを実施する。

## 確認対象

- `project/` 配下の全ソースコード
- 設定ファイル（`.env`、`config.*`、`appsettings.json`等）
- パッケージ管理ファイル（`package.json`、`requirements.txt`、`*.csproj`等）
- `.gitignore` ファイル

## 作業指示

1. **シークレット・認証情報の漏洩チェックを実行する**
   - 以下のコマンドでリポジトリ全体をスキャンする：
     ```bash
     # gitleaks によるシークレットスキャン
     gitleaks detect --source . --verbose --report-format json --report-path gitleaks-report.json
     ```
   - `.gitignore` を確認し、以下のファイルが含まれているか検証する：
     - `.env`、`.env.local`、`.env.production`
     - `*.key`、`*.pem`、`*.pfx`
     - `appsettings.Development.json`
     - `secrets/`、`credentials/`
   - ソースコード内に以下のパターンがないかgrepで検索する：
     ```bash
     # ハードコードされたシークレットの検索
     grep -rn "password\s*=" project/ --include="*.ts" --include="*.js" --include="*.py" --include="*.cs"
     grep -rn "api[_-]?key\s*=" project/ --include="*.ts" --include="*.js" --include="*.py" --include="*.cs"
     grep -rn "secret\s*=" project/ --include="*.ts" --include="*.js" --include="*.py" --include="*.cs"
     grep -rn "connection[_-]?string\s*=" project/ --include="*.ts" --include="*.js" --include="*.py" --include="*.cs"
     ```

2. **依存パッケージの脆弱性スキャンを実行する**
   - 該当する技術スタックに応じて以下のコマンドを実行する：
     ```bash
     # Node.js の場合
     pnpm audit --json > npm-audit-report.json

     # Python の場合
     pip-audit -r requirements.txt -f json > pip-audit-report.json

     # .NET の場合
     dotnet list package --vulnerable > dotnet-audit-report.txt
     ```
   - Critical/High の脆弱性があれば即時対応を提案する
   - ロックファイル（`pnpm-lock.yaml`、`requirements.txt` のピン留め等）でバージョンが固定されているか確認する

3. **認証・認可の実装をレビューする**
   - 認証ロジック（ログイン、トークン生成、パスワードハッシュ）のコードを特定し確認する
   - 以下の項目を検証する：
     - パスワードのハッシュにbcrypt/scrypt/Argon2が使用されているか
     - JWTの署名アルゴリズムが適切か（`"none"`が無効化されているか、RS256推奨）
     - セッションIDが認証成功時に再生成されているか
     - ブルートフォース対策（レート制限、アカウントロックアウト）があるか
     - OAuth 2.0/OIDC使用時にPKCEやstateパラメータが実装されているか

4. **入力検証・サニタイズ・エンコーディングをレビューする**
   - 全APIエンドポイントのコントローラ/ルーターファイルを特定する
   - 以下の脆弱性パターンを検索・確認する：
     - **SQLインジェクション**: パラメータ化クエリ/ORM使用が徹底されているか
     - **XSS**: 出力エンコーディングが実装されているか、`innerHTML`や`dangerouslySetInnerHTML`の使用箇所
     - **コマンドインジェクション**: `exec()`、`eval()`、`subprocess`等の使用箇所
     - **SSRF**: 外部URLへのリクエスト送信箇所でのURLバリデーション
     - **パストラバーサル**: ファイルパスの組み立てにユーザ入力が使用されている箇所

5. **暗号化実装をレビューする**
   - 暗号化関連のコードを特定し、以下を検証する：
     - 廃止されたアルゴリズム（MD5、SHA-1、DES、RC4）が使用されていないか
     - AES-256以上の暗号化が使用されているか
     - TLS 1.2以上が強制されているか
     - 暗号鍵がソースコード内にハードコードされていないか

6. **エラー処理・ログ出力の安全性をレビューする**
   - エラーハンドリングコードを確認し、以下を検証する：
     - エラーレスポンスにスタックトレースや内部情報が含まれていないか
     - ログに個人情報（PII）や機密情報が出力されていないか
     - 認証イベント（成功・失敗）がログに記録されているか
     - カスタムエラーページが設定されているか

7. **APIセキュリティをレビューする**
   - 全APIエンドポイントを列挙し、以下を検証する：
     - 全エンドポイントで認証・認可チェックが実施されているか
     - CORS設定が適切か（ワイルドカード`*`が使用されていないか）
     - レート制限が設定されているか
     - CSRF対策が実装されているか
     - レスポンスに不要なデータが含まれていないか（過剰なデータ露出）
     - セキュリティヘッダ（CSP、X-Frame-Options、HSTS、X-Content-Type-Options）が設定されているか
