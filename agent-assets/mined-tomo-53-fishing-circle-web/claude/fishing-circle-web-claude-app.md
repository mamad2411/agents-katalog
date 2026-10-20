# src/app — バックエンド層

Laravel のバックエンドロジック全体を置く。コントローラは薄く保ち、責務を各層に分散させる。

## 責務（ディレクトリ別）

| ディレクトリ | 責務 |
|---|---|
| `Models/` | Eloquent モデル。`$fillable` 制御・リレーション・スコープ・アクセサ |
| `Http/Controllers/` | リクエスト受付と画面遷移のみ。ビジネスロジックは持たない |
| `Http/Middleware/` | 認可ゲート。`CheckGroupPermission` が ACL の中核 |
| `Http/Requests/` | FormRequest によるバリデーション・認可 (`authorize()`) |
| `Enums/` | PHP 8.1 Enum。`PermissionLevel`（権限レベル 1〜4）・`Grade`（学年）を定義 |
| `ValueObjects/` | 不変の値オブジェクト。ロジックを持つデータ表現 |
| `Casts/` | Eloquent カスタムキャスト。DB 値と Enum/ValueObject の変換 |
| `Notifications/` | Laravel Notification（メール通知等） |
| `Providers/` | サービスプロバイダ |
| `View/` | View Composer 等のビュー補助クラス |

## ACL の中核

`Http/Middleware/CheckGroupPermission.php` がグループ権限チェックを担う。
ルートへの適用は `->middleware('check.group.permission:LEVEL')` で行い、`user_id` と `group_id` の両方でスコープを切る。

## 第3章（good-code-ch3）で導入した型安全層

- `Enums/PermissionLevel.php` … 権限レベルの int Enum。`label()` / `shortLabel()` で表示文字列を返す
- `Enums/Grade.php` … 学年の Enum。同様に `label()` を持つ
- `ValueObjects/` と `Casts/` … DB の生値と Enum を透過的に変換するカスタムキャスト

## 参照

- PHP/Laravel 規約 → `.cursor/rules/php-laravel.mdc`（Mass Assignment・Controller・ルーティング方針）
- セキュリティ規約 → `.cursor/rules/security.mdc`（ACL 詳細・入力検証）
- ルート CLAUDE.md → `/CLAUDE.md`

## 更新ルール

このディレクトリ配下に新しいサブディレクトリ・責務を追加・変更・削除したら、このファイルの責務表も同じ変更で更新すること。
規約の本体は `.cursor/rules/` とルート `CLAUDE.md` にあるため、ここには重複させず参照に留める。
矛盾を見つけたらルート / rules 側を正とし、本ファイルを修正する。
