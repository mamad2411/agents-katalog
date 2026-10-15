---
name: kuroco-server-processing
metadata:
  author: Diverta inc.
  version: "1.1.0"
  lastUpdated: "2026-02-20"
description: KurocoのSmartyプラグイン・構文リファレンスおよびWebhook・バッチ処理・自動化のベストプラクティス。使用キーワード：「Smartyプラグイン」「Smarty関数」「Smarty修飾子」「Smarty構文」「テンプレート関数」「assign」「foreach」「if」「escape」「date_format」「truncate」「api_internal」「sendmail」「slack_post_message」「fileupload」「rcms_vue_component」「translate」「pager」「rcms_auth」「login」「logout」「ai_completion」「write_file」「put_file」「json_encode」「変数代入」「ループ処理」「条件分岐」「文字列操作」「日付フォーマット」「ファイル操作」「API呼び出し」「メール送信」「Slack通知」「Vue連携」「認証」「ページネーション」「$smarty変数」「セキュリティ設定」「IF_FUNCS」「MODIFIER_FUNCS」「capture」「literal」「section」「Webhook」「バッチ処理」「定期実行」「スケジュール実行」「cron」「15分毎」「1時間毎」「外部連携」「GitHub Actions」「repository_dispatch」「workflow_dispatch」「Slack通知」「slack_send」「Chatwork」「chatwork_send」「メール通知」「send_mail」「SendGrid」「sendgrid_send」「自動処理」「api_request」「外部API」「トリガー」「前処理」「後処理」「Function」「カスタム処理」「CSV出力」「topics変数」「inquiry変数」。Smartyテンプレートの構文・プラグイン、定期実行、外部通知、トリガー処理に関する質問で使用。
---

# Kuroco サーバーサイド処理

KurocoのSmartyテンプレートプラグインリファレンスおよびWebhook・バッチ処理パターン。

**ドキュメント参照**: `/kuroco-docs` スキルを使用してKuroco公式ドキュメントを検索・参照できます。

## 目次

### Part 1: Smartyプラグインリファレンス

- [よく使うプラグイン](#よく使うプラグイン)
- [プラグイン種別](#プラグイン種別)
- [カテゴリ別リファレンス](#カテゴリ別リファレンス)
- [Smarty構文リファレンス](references/syntax.md) - 基本構文、制御構造、組み込み変数

### Part 2: Webhook・バッチ処理パターン

- [バッチ処理](#バッチ処理)
- [内部API呼び出し](#内部api呼び出し)
- [外部API呼び出し](#外部api呼び出し)
- [トリガー処理](#トリガー処理)
- [外部サービス連携](#外部サービス連携) → 詳細は [references/integrations.md](references/integrations.md)

---

# Part 1: Smartyプラグインリファレンス

KurocoのSmartyテンプレートで使用可能な全プラグインの完全リファレンス。

## よく使うプラグイン

### 変数・データ操作

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `assign` | 変数代入 | `{assign var="name" value="値"}` |
| `append` | 配列追加 | `{append var="arr" value="値"}` |
| `json_decode` | JSONパース | `{$json\|json_decode:true}` |
| `rcms_json_encode` | JSONエンコード | `{$arr\|@rcms_json_encode}` |

### API・データ取得

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `api_internal` | 内部API呼び出し | `{api_internal endpoint='/rcms-api/1/news' var='result'}` |
| `assign_topics_list` | 記事一覧取得 | `{assign_topics_list var='list' topics_group_id=1}` |
| `assign_topics_detail` | 記事詳細取得 | `{assign_topics_detail var='detail' topics_id=$id}` |
| `assign_tag_list` | タグ一覧取得 | `{assign_tag_list var='tags'}` |

→ 詳細: [references/api-plugins.md](references/api-plugins.md)

### 文字列処理

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `escape` | エスケープ | `{$html\|escape}` |
| `truncate` | 文字列切り詰め | `{$text\|truncate:100:"..."}` |
| `mb_truncate` | マルチバイト対応 | `{$text\|mb_truncate:50}` |
| `date_format` | 日付フォーマット | `{$date\|date_format:"%Y-%m-%d"}` |
| `translate` | 翻訳 | `{$key\|translate}` |
| `nl2br` | 改行をBRに | `{$text\|nl2br}` |
| `replace` | 文字列置換 | `{$text\|replace:"a":"b"}` |

→ 詳細: [references/string-plugins.md](references/string-plugins.md)

### フォーム・UI

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `fileupload` | ファイルアップロード | `{fileupload name="file" ...}` |
| `inquiry_input` | フォーム入力 | `{inquiry_input col="name" ...}` |
| `pager` | ページネーション | `{pager ...}` |
| `editActionBox` | 編集ボタン | `{editActionBox ...}` |
| `html_options` | selectオプション | `{html_options options=$opts}` |

→ 詳細: [references/form-plugins.md](references/form-plugins.md)

### 認証・権限

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `rcms_auth` | 権限制御ブロック | `{rcms_auth target="read:news"}...{/rcms_auth}` |
| `login` | ログイン処理 | `{login ...}` |
| `logout` | ログアウト処理 | `{logout ...}` |

→ 詳細: [references/auth-plugins.md](references/auth-plugins.md)

### 外部サービス連携

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `sendmail` | メール送信 | `{sendmail to=$email subject="件名" ...}` |
| `slack_post_message` | Slack通知 | `{slack_post_message webhook_url=$url ...}` |
| `ai_completion` | AI呼び出し | `{ai_completion prompt=$prompt var='result'}` |
| `github_deploy` | GitHubデプロイ | `{github_deploy ...}` |

→ 詳細: [references/integration-plugins.md](references/integration-plugins.md)

### ファイル操作

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `write_file` | ファイル書き込み | `{write_file var="path" value="内容"}` |
| `put_file` | ストレージアップロード | `{put_file path="/files/..." tmp_path=$tmp}` |
| `read_file` | ファイル読み込み | `{read_file path="/files/..." var='content'}` |
| `read_dir` | ディレクトリ読み込み | `{read_dir path="/files/..." file_var='file'}...{/read_dir}` |

→ 詳細: [references/file-plugins.md](references/file-plugins.md)

### Vue.js連携

| プラグイン | 説明 | 例 |
|-----------|------|-----|
| `rcms_vue_component` | Vueコンポーネント | `{rcms_vue_component config="rcms-mng" name="..."}` |
| `head_include` | headに追加 | `{head_include file="..."}` |
| `bodyend` | body終了前に追加 | `{bodyend}...{/bodyend}` |

→ 詳細: [references/vue-plugins.md](references/vue-plugins.md)

## プラグイン種別

### 関数プラグイン (Function)

出力を生成または処理を実行する関数。

```smarty
{function_name param1="value1" param2="value2"}
```

### 修飾子プラグイン (Modifier)

変数の値を変換・加工する。パイプ（`|`）で連結可能。

```smarty
{$variable|modifier1|modifier2:param}
```

### ブロックプラグイン (Block)

開始タグと終了タグで囲まれた範囲を処理。

```smarty
{block_name param="value"}
  コンテンツ
{/block_name}
```

## カテゴリ別リファレンス

| カテゴリ | ファイル | 主なプラグイン |
|---------|---------|---------------|
| **構文リファレンス** | [syntax.md](references/syntax.md) | **基本構文、制御構造、組み込み変数、ベストプラクティス** |
| API・データ取得 | [api-plugins.md](references/api-plugins.md) | api_internal, assign_topics_list, assign_tag_list |
| 文字列処理 | [string-plugins.md](references/string-plugins.md) | escape, truncate, date_format, translate |
| 配列操作 | [array-plugins.md](references/array-plugins.md) | count, in_array, implode, explode, sort系 |
| フォーム・UI | [form-plugins.md](references/form-plugins.md) | fileupload, inquiry_input, pager, html_* |
| 認証・権限 | [auth-plugins.md](references/auth-plugins.md) | rcms_auth, login, logout |
| 外部連携 | [integration-plugins.md](references/integration-plugins.md) | sendmail, slack_*, ai_completion |
| ファイル操作 | [file-plugins.md](references/file-plugins.md) | write_file, put_file, read_file, read_dir |
| Vue.js連携 | [vue-plugins.md](references/vue-plugins.md) | rcms_vue_component, head_include |
| 全プラグイン | [all-plugins.md](references/all-plugins.md) | 全206プラグイン一覧 |

## 使用例

### コンテンツ一覧をAPIで取得して表示

```smarty
{assign var="queries" value=$dataSet.emptyArray}
{append var="queries" index="cnt" value=10}
{append var="queries" index="filter" value="topics_flg = 1"}

{api_internal
  endpoint='/rcms-api/1/news'
  method='GET'
  member_id=1
  queries=$queries
  var='result'
}

{foreach from=$result.list item="news"}
  <h2>{$news.subject|escape}</h2>
  <p>{$news.contents|truncate:200}</p>
  <time>{$news.ymd|date_format:"%Y年%m月%d日"}</time>
{/foreach}

{pager data=$result.pageInfo}
```

### フォーム送信後にSlack通知

```smarty
{sendmail
  var=mail_result
  to=$inquiry.email
  subject="お問い合わせありがとうございます"
  mail_template="inquiry_thanks"
}

{slack_post_message
  webhook_url=$smarty.const.SLACK_WEBHOOK_URL
  text="新規問い合わせ: {$inquiry.name}様 - {$inquiry.subject}"
}
```

### 権限に応じた表示制御

```smarty
{rcms_auth target="write:news"}
  <a href="/management/news/edit/">編集</a>
{/rcms_auth}

{rcms_auth target="delete:news"}
  <button class="delete-btn">削除</button>
{/rcms_auth}
```

---

# Part 2: Webhook・バッチ処理パターン

Kuroco HeadlessCMSでのWebhook、バッチ処理、外部連携に関するベストプラクティス。

> **Smarty構文について**: バッチ処理・トリガーはSmartyテンプレートで記述します。構文やプラグインの詳細は上記 Part 1 を参照してください。

## バッチ処理

### 概要

バッチ処理は一定時間ごとに自動実行される処理。

**実行頻度の選択肢:**
| 頻度 | 用途 |
|------|------|
| 15分毎 | 頻繁な同期が必要な場合 |
| 30分毎 | 準リアルタイム処理 |
| 1時間毎 | 定期的な集計・更新 |
| 毎日（指定時刻） | 日次レポート、バックアップ |

### ユースケース

- 外部システムへのCSV生成・連携
- 外部システムからのデータ取り込み
- ログ集計・統計データ算出
- 定期的なメール配信
- GitHub Actions連携（デプロイトリガー）

### バッチ処理の作成

管理画面: [オペレーション] → [バッチ処理] → [追加]

| 項目 | 説明 | 例 |
|------|------|-----|
| タイトル | バッチの名前 | CSV出力バッチ |
| 識別子 | ユニークな識別子（英数字） | csv_export |
| 実行頻度 | 実行間隔 | 毎日 03:00 |
| 実行内容 | Smarty構文で記述 | 下記参照 |

## 内部API呼び出し

### 基本構文

```smarty
{api_internal
  endpoint='/rcms-api/1/news'
  method='GET'
  member_id=1
  queries=$queries
  var='response'
}
```

### コンテンツ一覧取得

```smarty
{assign var="queries" value=$dataSet.emptyArray}
{append var="queries" index="cnt" value=0}
{append var="queries" index="filter" value="topics_flg = 1"}

{api_internal
  endpoint='/rcms-api/1/news'
  method='GET'
  member_id=1
  queries=$queries
  var='news_list'
}

{foreach from=$news_list.list item="news"}
  ID: {$news.topics_id}, タイトル: {$news.subject}
{/foreach}
```

### コンテンツ作成

```smarty
{assign var="body" value=$dataSet.emptyArray}
{append var="body" index="subject" value="タイトル"}
{append var="body" index="contents" value="本文"}
{append var="body" index="topics_flg" value=1}

{api_internal
  endpoint='/rcms-api/1/news/insert'
  method='POST'
  member_id=1
  body=$body
  var='result'
}
```

## 外部API呼び出し

### 基本構文

```smarty
{api_request
  url='https://api.example.com/endpoint'
  method='GET'
  headers=$headers
  body=$body
  var='response'
}
```

### POSTリクエスト例

```smarty
{assign var="headers" value=$dataSet.emptyArray}
{append var="headers" index="Content-Type" value="application/json"}
{append var="headers" index="Authorization" value="Bearer YOUR_API_KEY"}

{assign var="body" value=$dataSet.emptyArray}
{append var="body" index="message" value="Hello"}

{api_request
  url='https://api.example.com/post'
  method='POST'
  headers=$headers
  body=$body|@json_encode
  var='response'
}
```

## トリガー処理

### コンテンツ更新時のトリガー

管理画面: [コンテンツ定義] → [トリガー設定]

**利用可能なイベント:**
| イベント | タイミング |
|---------|----------|
| 作成時 | コンテンツ新規作成後 |
| 更新時 | コンテンツ更新後 |
| 削除時 | コンテンツ削除後 |
| 公開時 | 公開ステータス変更時 |

**利用可能な変数:**
```smarty
{$topics.topics_id}      {* コンテンツID *}
{$topics.subject}        {* タイトル *}
{$topics.contents}       {* 本文 *}
{$topics.ymd}            {* 公開日 *}
{$topics.ext_col_01}     {* 拡張項目 *}
```

### フォーム送信時のトリガー

管理画面: [フォーム] → [トリガー設定]

```smarty
{$inquiry.inquiry_id}    {* 回答ID *}
{$inquiry.name}          {* 名前 *}
{$inquiry.email}         {* メールアドレス *}
{$inquiry.message}       {* メッセージ *}
```

## 外部サービス連携

**詳細な連携パターン**: [references/integrations.md](references/integrations.md) を参照

### Slack通知

```smarty
{assign var="message" value=$dataSet.emptyArray}
{append var="message" index="text" value="通知メッセージ"}

{slack_send
  webhook_url="https://hooks.slack.com/services/xxx/yyy/zzz"
  body=$message|@json_encode
}
```

### メール通知

```smarty
{send_mail
  to="recipient@example.com"
  subject="件名"
  body="本文"
}
```

### GitHub Actions連携

```smarty
{assign var="headers" value=$dataSet.emptyArray}
{append var="headers" index="Authorization" value="token YOUR_GITHUB_TOKEN"}
{append var="headers" index="Accept" value="application/vnd.github.v3+json"}

{assign var="body" value=$dataSet.emptyArray}
{append var="body" index="event_type" value="kuroco-update"}

{api_request
  url='https://api.github.com/repos/owner/repo/dispatches'
  method='POST'
  headers=$headers
  body=$body|@json_encode
  var='response'
}
```

## ベストプラクティス

### 負荷を考慮した実行時間

- システム負荷の低い時間帯（深夜・早朝）に設定
- 大量データ処理は1日1回に制限
- ページネーションを使用して分割処理

### エラーハンドリング

```smarty
{api_internal
  endpoint='/rcms-api/1/news'
  method='GET'
  member_id=1
  var='response'
}

{if $response.errors}
  {slack_send webhook_url="..." text="エラー: {$response.errors|@json_encode}"}
  {log message="エラー: {$response.errors|@json_encode}"}
{else}
  {log message="処理完了: {$response.pageInfo.totalCnt}件"}
{/if}
```

### タイムアウト対策

大量データは分割処理:

```smarty
{assign var="page" value=1}
{while true}
  {assign var="queries" value=$dataSet.emptyArray}
  {append var="queries" index="pageID" value=$page}
  {append var="queries" index="cnt" value=100}

  {api_internal endpoint='/rcms-api/1/news' method='GET' member_id=1 queries=$queries var='response'}

  {foreach from=$response.list item="item"}
    {* 処理 *}
  {/foreach}

  {if $page >= $response.pageInfo.totalPageCnt}{break}{/if}
  {assign var="page" value=$page+1}
{/while}
```

---

## 関連スキル

- `/kuroco-api-content` - API設計・認証パターン、コンテンツCRUD操作
- `/kuroco-admin-api` - 管理API（admin_api）の操作

## 関連ドキュメント

- `../kuroco-docs/docs/tutorials/how-to-use-batch.md` - バッチ処理の使い方
- `../kuroco-docs/docs/tutorials/auto-run-github-with-contents-update.md` - GitHub Actions連携
- `../kuroco-docs/docs/tutorials/send-slack-notification-after-a-form-has-been-submitted.md` - Slack通知
- `../kuroco-docs/docs/reference/trigger-variables.md` - トリガー変数
