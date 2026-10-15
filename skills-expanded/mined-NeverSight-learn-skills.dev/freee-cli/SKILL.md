---
name: freee-cli-skill
description: >-
  freee CLI (`freee`) を使って freee API を操作する。
  会計・人事労務・請求書・工数管理・販売の API リファレンスと使い方ガイドを提供。
  経費申請・取引登録・勤怠打刻・給与明細・見積書・試算表・仕訳・従業員管理・工数登録・売上管理など、
  freee関連の操作やAPI仕様を調べたいときに使う。
---

# freee CLI

## Look things up before answering

The CLI is self-documenting. Always prefer running these commands over guessing
syntax or relying on memorized knowledge:

- `freee accounting ls` -- list all endpoints.
- `freee accounting ls deals` -- filter endpoints by keyword.
- `freee accounting help deals` -- show methods for an endpoint.
- `freee accounting docs deals` -- compact API docs (params, response schema).
- `freee accounting docs deals -X POST` -- docs for a specific method.
- `freee accounting spec deals` -- raw OpenAPI fragment (JSON).

Paths: use shorthand (`deals`, `approval_requests/123`) or full path (`/api/1/deals`).

## Authentication

- `freee auth login` -- OAuth認証（ブラウザが開きます）
- `freee auth status` -- トークン状態確認
- `freee auth logout` -- トークン削除

認証エラーが出たら `freee auth status` で確認し、必要なら `freee auth logout` → `freee auth login` で再認証。

## Company Selection

- `freee company ls` -- 会社一覧
- `freee company current` -- 現在の会社表示
- `freee company set <id>` -- デフォルト会社切り替え

company_id は API リクエストに自動注入されます。明示的に指定した場合はそちらが優先されます。

## API Services

| service | 説明 | パス例 |
|---------|------|--------|
| `accounting` | freee会計 (取引、勘定科目、取引先など) | `/api/1/deals` |
| `hr` | freee人事労務 (従業員、勤怠など) | `/api/v1/employees` |
| `invoice` | freee請求書 (請求書、見積書、納品書) | `/invoices` |
| `pm` | freee工数管理 (プロジェクト、工数など) | `/projects` |
| `sm` | freee販売 (見積、受注、売上など) | `/businesses` |

## API Calls

```bash
# GET (shorthand - /api/1/ is auto-prepended)
freee accounting get deals type==income limit==10

# POST with inline body
freee accounting post deals type=expense issue_date=2025-01-15 details[0][tax_code]:=1 details[0][amount]:=5000

# POST with JSON body
freee accounting post deals -d '{"type":"income","issue_date":"2025-01-15","details":[{"tax_code":1,"amount":10000}]}'

# PUT / DELETE
freee accounting put deals/123 -d '{"type":"expense"}'
freee accounting delete deals/123
```

Input syntax:
- `key==value` -- query parameter
- `key=value` -- body string field
- `key:=json` -- body typed field (numbers, arrays, booleans)
- `-d '{}'` -- full JSON body

Use `--max=N` to show more items (default: 10).
Use `--verbose` to show the actual API URL being called.

## Workflow

1. `freee auth status` で認証状態を確認（未認証なら `freee auth login`）
2. `freee company current` で事業所を確認
3. レシピ（recipes/）で操作手順を確認
4. `freee accounting docs <path>` でパラメータを確認
5. API を呼び出す

## Error Handling

- 認証エラー (401): `freee auth login` で再認証
- アクセス拒否 (403): 権限不足またはレートリミット → 数分待って再試行
- バリデーションエラー (400): `docs` サブコマンドでパラメータを確認
- 事業所エラー: `freee company ls` → `freee company set <id>`
- 詳細: `recipes/troubleshooting.md` 参照

## Recipes

よくある操作のユースケースサンプルとTips:

- `recipes/deal-operations.md` -- 取引（収入・支出）
- `recipes/expense-application-operations.md` -- 経費申請
- `recipes/hr-employee-operations.md` -- 人事労務（従業員・給与）
- `recipes/hr-attendance-operations.md` -- 勤怠（出退勤・打刻・休憩の登録）
- `recipes/invoice-operations.md` -- 請求書・見積書・納品書
- `recipes/receipt-operations.md` -- ファイルボックス（証憑ファイルのアップロード・管理）
- `recipes/pm-operations.md` -- 工数管理（プロジェクト・工数実績）
- `recipes/pm-workload-registration.md` -- 工数の安全な登録（PM・HR連携ワークフロー）
- `recipes/sm-operations.md` -- 販売管理（案件・受注）

## API の機能制限について

freee API 自体の機能制限に起因する問題は CLI では解決できません。詳細は `recipes/troubleshooting.md` を参照。

## References

`references/` ディレクトリに各 API のリファレンスドキュメントがある。
`--docs` と同等の内容だが、リソースごとにファイルが分かれている。

ファイル命名規則: `{service}-{resource}.md`（例: `accounting-deals.md`, `hr-employees.md`）

CLI と references の使い分け:
- `freee <service> docs <path>` — 特定エンドポイントのドキュメントを即座に確認
- `references/` — リソース全体の概要を把握したいとき

## 関連リンク

- [freee API ドキュメント](https://developer.freee.co.jp/docs)
