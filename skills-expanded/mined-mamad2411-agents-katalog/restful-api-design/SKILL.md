---
name: restful-api-design
description: Web API / HTTP API の設計判断を行うためのスキル。リソース設計、URL、HTTP メソッド、ステータスコード、表現形式、エラー、ページネーション、互換性、バージョニング、セキュリティ、破壊的変更の判断が必要なときに使用する。
metadata:
  tags: [api, design, http, rest, compatibility]
---

# Web API Design

Web API の表面設計を、意味・互換性・運用性の観点から判断するためのスキル。

HTTP は単なる配送路ではない。メソッド、ステータスコード、キャッシュ、条件付きリクエスト、表現形式といった既存の意味を壊さずに使うことで、API は理解しやすく、変更しやすく、壊れにくくなる。

---

## このスキルを使う場面

- 新規 API のエンドポイント設計
- 既存 API の URL / HTTP メソッド / レスポンス形状の見直し
- ページネーション、フィルタ、ソート、検索の設計方針決定
- エラーフォーマットやステータスコードの一貫性整理
- 破壊的変更、バージョニング、互換性維持の方針決定
- API レビューでの表面設計の妥当性判断

## このスキルの対象外

- モジュール境界や内部責務の分割
- DB スキーマ設計そのもの
- SDK の言語別実装詳細
- API ゲートウェイやインフラ製品の設定詳細

内部構造の責務分離が主題なら別の利用可能な skill を優先する。

---

## 根拠の優先順位

設計判断の根拠は次の優先順位で扱う。下位が上位と衝突する場合は常に上位を優先する。

1. RFC で定義されている HTTP / URI / MIME / Problem Details などの仕様
2. WHATWG、W3C、IANA など、Web の標準仕様・登録簿・相互運用上の規則
3. MDN など、標準仕様の内容を実務向けに整理した公開ドキュメント
4. RFC や Web 標準だけでは一意に決まらない箇所での、保守性と運用性を優先した組織既定値

---

## 出力形式

このスキルを使って API を設計またはレビューするときは、次を成果物として出力する。

1. **リソース一覧**: 名詞、collection/item の別、親子関係
2. **エンドポイント表**: method, path, 目的, request 要点, response 要点, 主な status
3. **エラー形式**: Problem Details 準拠の例示（type, title, status, detail, instance）
4. **一覧取得ポリシー**: page size / cursor / filter / sort / fields の既定
5. **冪等性・リトライ設計**: idempotency key 要否、再送時の注意点
6. **キャッシュ・並行性**: ETag / If-Match の採用有無、非同期の追跡手段
7. **互換性・バージョニング**: 破壊的変更の定義、version strategy
8. **open questions / リスク**: 未決定事項、注意点

---

## 基本原則

### 1. 意味から設計する

最初に決めるべきなのは URL でも JSON でもなく、クライアントが何をしたいのか、そのためにどんな状態遷移が必要かである。

- どの名詞が API の主役か
- その名詞は collection か item か
- クライアントが観測・操作したい状態は何か
- どの遷移が標準メソッドで表現できるか

表面だけ先に作ると、DB スキーマや内部都合の写しになる。

### 2. HTTP の意味を壊さない

HTTP メソッドとステータスコードは既に意味を持っている。独自ルールで上書きしない。

- GET は安全な取得
- POST は新規作成や action 的な処理の起点
- PUT は全置換
- PATCH は部分更新
- DELETE は削除

### 3. 使いやすさより先に一貫性を守る

短期的に楽でも、例外ルールが増える API は中長期で崩れる。1 つの便利例より、全体の一貫性を優先する。

---

## 設計フロー

### Step 1: リソースを定義する

「何を識別し、何を一覧し、何を変更するのか」を決める。

**確認項目:**
- リソースとして安定した名前を持つか
- collection と item を区別できるか
- 子リソースは本当に親に従属しているか
- action 専用 endpoint にする必要があるか

**ルール:**
- 名詞中心で設計する
- リソース名は識別可能で安定していること
- まず resource-oriented に試し、無理なときだけ action endpoint を許可する

**例:** `/users`, `/users/{userId}`, `/orders/{orderId}/items`

**action endpoint を検討してよい場合:**
- 長時間かかるジョブ開始
- 複数リソース横断の承認・実行
- 「作成」でも「更新」でもない明確な操作

その場合も `POST /orders/{orderId}:cancel` のように対象リソースと操作の関係が読める形を検討する。これは組織既定値の一例であり、普遍的標準ではない。

### Step 2: URL を決める

URL は操作手順ではなく資源の位置と絞り込み条件を表す。

**ルール:**
- 人間が読める名前にする
- path は英小文字、単語区切りは kebab-case を既定にする
- query parameter は filtering / sorting / field selection / pagination に使う

**避けること:**
- `/getUsers`, `/create-order`, `/searchUsersByStatus`
- 実装詳細が見える path 名
- path で page 番号や sort 条件を表す

### Step 3: 表現形式を決める

レスポンスは「今返せる JSON」ではなく「今後も説明可能な契約」として設計する。

**ルール:**
- フィールド名は意味語彙を揃える
- 同じ概念には API 全体で同じ名前を使う。省略可能性、nullability、配列/単体の違いを曖昧にしない
- field / query parameter の casing を統一する（既定: snake_case）

**指針:**
- ID は安定した識別子として扱う
- timestamp / date / enum はフォーマットを明示する
- summary と detail で shape が変わるなら明示的に分ける
- 将来拡張を考え、意味の薄い短縮名を避ける

### Step 4: HTTP メソッドを割り当てる

| Method | 意味 | 冪等 | 安全 | 主な用途 |
|:---:|---|---|:---:|---|
| `GET` | 取得 | ✅ | ✅ | 一覧・詳細取得 |
| `POST` | 作成 / action 起点 | ❌ | ❌ | 新規作成、複雑検索、非同期ジョブ開始 |
| `PUT` | 全置換 | ✅ | ❌ | リソース全体の置き換え |
| `PATCH` | 部分更新 | ❌ | ❌ | 一部フィールドの更新 |
| `DELETE` | 削除 | ✅ | ❌ | リソース削除 |

**ルール:**
- 読み取りは原則 GET。POST は URL 長・秘匿性・複雑な検索条件でやむを得ない場合に限る
- PUT は全置換として扱う（RFC）
- 部分更新が主なら PATCH を使う。PATCH の media type はチーム既定を決める（通常の JSON 部分更新は `application/merge-patch+json` または独自 `application/json` のいずれかに統一）
- action endpoint は標準メソッドで自然に表現できないときだけ使う

### Step 5: ステータスコードを決める

ステータスコードは「成功/失敗」以上の意味を持つ。意味を潰さない。

| Code | 意味 | 用途 |
|:---:|---|---|
| `200` | OK | 通常の成功 |
| `201` | Created | 新規作成成功。`Location` ヘッダを併用 |
| `202` | Accepted | 非同期受付。追跡用の operation resource URL または `Location` を返す |
| `204` | No Content | 本文なし成功（削除完了など） |
| `400` | Bad Request | 構文・形式不正 |
| `401` | Unauthorized | 未認証。`WWW-Authenticate` を併用 |
| `403` | Forbidden | 認証済みだが権限不足 |
| `404` | Not Found | 存在しない、または存在秘匿 |
| `409` | Conflict | 現在状態との衝突 |
| `410` | Gone | 明示的に廃止・消滅 |
| `422` | Unprocessable Content | 構文は正しいが意味的に処理不能 |
| `429` | Too Many Requests | レート制限 |

**必要時に検討する追加 code:** `304 Not Modified`（条件付き GET）、`412 Precondition Failed`（If-Match 失敗）、`415 Unsupported Media Type`

**ルール:**
- 実際の結果に合ったコードを返す（RFC）
- 401 / 403 / 404 の区別を API 全体で統一する
- 非同期処理では 202 と追跡手段（操作状態取得 endpoint、`Location` ヘッダ、完了後の参照先）をセットで返す

### Step 6: エラー形式を統一する

HTTP JSON API のエラーは RFC 9457 の Problem Details（`application/problem+json`）を既定にする。

最低限そろえる項目:

| Field | 役割 |
|---|---|
| `type` | 安定した機械可読識別子（URI） |
| `title` | 人間可読なエラー種別 |
| `status` | HTTP ステータスコード |
| `detail` | 人間向け説明（文字列解析前提にしない） |
| `instance` | このエラー発生を特定する識別子 |

**ルール:**
- バリデーションエラーの詳細は拡張フィールド（`errors` 配列等）で構造化する
- 内部実装や stack trace を露出しない
- エラー本文で権限モデルを漏らしすぎない

### Step 7: 一覧取得を設計する

一覧 API は後付けで複雑化しやすい。最初からルールを決める。

**ルール:**
- pagination は collection の標準機能として最初から設計する
- mutable な大規模一覧では offset より cursor を優先する
- query parameter 名（`page_size`/`limit`、`page_token`/`cursor`、`filter`、`sort`、`fields`）は API 全体で統一する

**注意:**
- cursor token は opaque にする（内部 offset や秘密情報を露出しない）
- 無効な filter / sort は黙って無視せず明示的に失敗させる
- 総件数が高コストなら常に返す前提にしない

### Step 8: 冪等性とリトライを考える

**ルール:**
- GET / PUT / DELETE は idempotent（RFC）
- POST / PATCH は idempotent が保証されない
- 重複実行が困る POST には idempotency key 相当の仕組みを検討する

**確認項目:**
- タイムアウト後の再送で二重作成されないか
- 外部課金や通知が重複しないか
- 非同期ジョブ開始が多重起動しないか

### Step 9: キャッシュと条件付きリクエストを考える

HTTP の強みを捨てない。

- cacheable な GET は cache 戦略を明示する（RFC）
- ETag / Last-Modified が成立するなら検討する
- 更新競合を避けたい resource では `If-Match` / `If-Unmodified-Since` を使った条件付き更新を検討する。競合時は `412 Precondition Failed` を返す

### Step 10: 互換性とバージョニングを決める

**ルール:**
- 変更可能性を前提に設計する
- 公開 API の表面バージョンは major version を基本とする
- 破壊的変更は新バージョンへ分離し、移行期間を設ける

**避けること:**
- 同じ version のまま破壊的変更を入れる
- field の意味を黙って変える
- enum の既存値の意味を変える
- field を追加せず既存 field の意味だけを変える

### Step 11: 認証・認可・セキュリティを確認する

**ルール:**
- HTTPS を前提にする
- token や secret を URL に置かない（RFC）
- 認可失敗時の 403 / 404 の扱いを統一する
- rate limit と監査可能性を設計に含める

**注意:**
- 秘匿対象 resource は存在有無の扱いも含めて設計する
- エラー本文で権限モデルを漏らしすぎない
- input-only な secret は再取得不能にすることを検討する

---

## 既定値一覧

明確な理由がない限り、次を既定にする。

| 項目 | 既定値 |
|---|---|
| URL スタイル | noun-based, kebab-case |
| 一覧取得 | `GET /resources` |
| 詳細取得 | `GET /resources/{id}` |
| 作成 | `POST /resources` |
| 部分更新 | `PATCH /resources/{id}` |
| 全置換 | `PUT /resources/{id}` |
| 削除 | `DELETE /resources/{id}` |
| エラー形式 | RFC 9457 Problem Details (`application/problem+json`) |
| pagination | `page_size` + `page_token` または `limit` + `cursor` のどちらかに統一 |
| field/query casing | API 全体で統一（既定: snake_case） |
| PATCH media type | チーム既定を決める（`application/merge-patch+json` または `application/json`） |
| 破壊的変更 | 新 major version |
| 非同期処理 | `202 Accepted` + operation resource（`Location` ヘッダ） |

---

## 反パターン

- DB テーブル名の直写しを API 名にする
- `/getX`, `/createX`, `/searchX` のような verb-heavy URL
- 読み取りをすべて POST で受ける
- 成功も失敗も 200 に包む
- 人間向けメッセージだけでエラー種別を表現する
- 無制限一覧を返す
- page token に内部 offset や秘密情報を露出する
- PATCH と PUT の意味を混ぜる
- 非同期処理なのに 202 と追跡手段を用意しない
- field を追加せず既存 field の意味だけを変える

---

## 最終チェック

設計完了時に以下を確認する。すべて Yes で最低限整っている。

- [ ] リソース名は安定した名詞で、URL に動詞や実装都合が漏れていないか
- [ ] HTTP メソッドの意味を壊していないか（GET が安全、PUT が全置換、PATCH が部分更新）
- [ ] ステータスコードが結果と一致し、401/403/404 の区別が統一されているか
- [ ] エラーが RFC 9457 Problem Details 形式で機械可読か
- [ ] 一覧取得に pagination / filter / sort が設計されているか
- [ ] retry / idempotency の前提が整理され、二重作成・二重課金の対策があるか
- [ ] 非同期処理に 202 + 追跡手段（操作状態 endpoint / Location）があるか
- [ ] 条件付き更新（If-Match / ETag）が必要な箇所で検討されているか
- [ ] 破壊的変更と version policy が明確か
- [ ] 認証・認可・秘匿情報の扱いが統一され、token/secret が URL に露出していないか
- [ ] リソースと操作の意味が説明でき、将来の変更時に「どこが破壊的か」を判定できるか

---

## References

- RFC 9110: HTTP Semantics
- RFC 9111: HTTP Caching
- RFC 9457: Problem Details for HTTP APIs
- RFC 6750: Bearer Token Usage
- RFC 5789 / 6902 / 7396: PATCH と JSON patch 系
- MDN Web Docs: HTTP / Web API に関する公開ドキュメント
