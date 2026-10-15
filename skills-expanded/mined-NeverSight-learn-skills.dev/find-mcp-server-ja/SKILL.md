---
name: find-mcp-server-ja
description: 公開MCP(Model Context Protocol)サーバーの探索、比較、導入、add-mcp 接続を支援する日本語版スキル。DB、外部API、ファイル操作、GitHub連携などで「〇〇のMCPサーバーはある？」「MCPツールを探して」「add-mcp で入れたい」といった依頼が出たら積極的に使い、候補探索から動作テストまで対応する。 別途「find-mcp-server」スキルが存在する場合は、「find-mcp-server-ja」だけを読み込むようにし、「find-mcp-server」「find-mcp-server-ja」の両方を読み込むことは絶対にしないこと。
license: CC0
metadata:
  author: Dice <tetradice@gmail.com>
  version: "1.1.0"
---

# Find MCP Server JA（MCPサーバーの検索と導入）

このスキルは、目的に合う公開MCPサーバーを見つけ、候補比較、導入、導入後の基本テストまでを一貫して支援します。

## 使うタイミング

- 「Xと連携できるMCPサーバーはあるか」「X用のMCPツールを探して」と依頼されたとき
- エージェントに新しい外部連携を追加したいとき
- 既存のサービスやシステムをAIエージェントから操作したいとき

## 主なコマンド

`script/` は `SKILL.md` と同じ階層に置き、まず同梱CLIで候補探索します。
実行時はスキルのディレクトリに移動するか、`SKILL.md` から見た相対位置で `script/mcp-server-search.js` を解決します。現在のカレントディレクトリを前提にしません。

- `node script/mcp-server-search.js [検索語] --limit 30`: Official MCP Registry、Smithery REST API、GitHub REST API を並列検索して統一JSONを返す
- `npx add-mcp [npmパッケージ名]`: npmパッケージ型のMCPサーバーを追加する
- `npx add-mcp "[実行コマンド 引数1 ...]"`: stdio型のMCPサーバーを追加する。引用した実行コマンドには半角スペースを1つ以上含める
- `npx add-mcp [HTTP URL]`: URLから直接追加する

`npx add-mcp find` は使わないでください。見つけた候補をそのままワークスペースへ追加してしまいます。

## ワークフロー

### 1. 要件確認

次の2点を確認します。

1. 連携対象。例: PostgreSQL、GitHub、Slack、Notion
2. 実行したい操作。例: クエリ、PR作成、Issue作成、メッセージ送信

### 2. 候補検索

まずは同梱CLIを使います。

```bash
node script/mcp-server-search.js github --limit 30
```

同じJSON出力から、少なくとも次を直接確認します。

1. `sources.registry.ok`
2. `sources.smithery.ok`
3. `sources.github.ok`
4. `merged[]`
5. `normalized[]`

検索時のルール:

- 3ソース確認済みと言ってよいのは、その実行のJSONで `sources.registry.ok`、`sources.smithery.ok`、`sources.github.ok` がすべて `true` の場合だけ
- 3ソース確認の根拠は、最終的に採用した同梱CLI 1回分のJSONだけに置きます。絞り込みで再実行した場合は、確認済みとして引用するのは最後の実行結果だけにします
- README、別API実行、GitHub検索をつなぎ合わせて「3ソース確認済み」と扱わない
- どれかが `false` または未確認なら、その事実を明示し、以降は補助調査として扱う
- 検索語が広すぎる場合は、3ソース確認を維持したまま絞り直してよい。その場合は最終検索語と理由をユーザー向け説明に残す
- `postgres`、`git`、`filesystem` のような広い技術語では、最初のノイジーな実行の後に `[term] mcp` や `[term] mcp server` のような precision pass を1回行い、その結果を最終の3ソース確認根拠として使う
- 途中の broad run が失敗、ノイズ過多、または根拠として使えない場合は、その実行を説明から切り離し、成功した最終 run だけを根拠として扱う
- 固有名詞の検索、または3ソース成功後も適合候補が見えない検索では、製品名やベンダー名で完全一致寄りの補助チェックを1回追加してよい。その確認は3ソース確認の一部ではなく、補助証拠として明示する
- Registry と GitHub が空または無関係のままで、Smithery の残り候補も補助チェック後に対象名や必要機能へ結び付けられない場合は、弱い一致を無理に候補化せず no-fit と判定して代替案へ進む
- Slack、GitHub、Supabase、Vercel など公式組織がありそうな対象で公式候補が見えない場合は、3ソース成功後でも一次情報による追加のベンダー確認を行う
- 製品名やベンダー名が曖昧な場合、補助確認は一般Web検索より先に公式ドメイン確認と GitHub 完全一致寄り検索を使う。一般Web検索は弱い補助証拠としてだけ扱う
- 候補名、ツール、スター数、更新日、導入方法などは取得済みの実データだけを使い、未確認項目は未確認と書く
- hosted 候補に公開 repo や明確な repo provenance がない場合は、公式 docs などの一次情報で運営元と機能を確認できない限り、hosted または条件付き候補として扱う
- 必要な検索や確認が実行できない環境では、仮候補や仮比較表を出さず、未確認事項を報告して止まる

### 3. 候補の優先順位付け

要件を満たす公式候補があるなら最優先にします。公式候補があるのに採用しない場合は、今回の要件に対して何が不足しているかを明示します。

公式判定では、少なくとも次を確認します。

1. GitHubリポジトリの owner が対象サービスの公式 organization または vendor と一致する
2. `homepage` または `repositoryUrl` が公式ドメインか公式GitHub配下を指す
3. README、説明文、公開元情報、公式docs、公式ブログなどに一次情報がある

補足ルール:

- Registry、Smithery、Registryの `official` や `featured` のようなメタデータだけで公式扱いしない
- ベンダー公式docsが案内するホスト型MCP endpoint は公式候補として扱ってよいが、OSSリポジトリとは区別して説明する
- `postgres` や `git` のような汎用検索では、Neon や Supabase のようなサービス専用候補を別枠または条件付き候補として扱う
- 優先順位は `機能適合 > 安全性と保守性 > 人気度`
- 人気度・普及度は GitHub `stargazers_count`、GitHub `updated_at`、Smithery `useCount`、Smithery `verified`、npm週次ダウンロード数で比較する

### 4. 品質確認

推奨前に、必要なTools/Resourcesがありそうか、保守状態が許容できるかを確認します。

- READMEを確認するなら `https://raw.githubusercontent.com/.../README.md` を優先する
- 可能なら一時的に起動してTools/Resourcesを確認する
- 比較だけが目的、または read-only 評価なら、検証のためだけにインストールを強行せず、公開情報ベース比較と未実機確認であることを明示する

### 5. 候補提示と導入確認

インストール確認の前に、各候補について少なくとも次を示します。

1. MCPサーバー名
2. 概要
3. 検証で確認できた代表的なTools/Resourcesまたは機能カテゴリを3〜5個
4. 導入方法。npmパッケージ、実行コマンド、HTTP URL のいずれか
5. 人気度または普及度の指標
6. 公式候補かどうか。非公式ならその理由

追加ルール:

- 同じ候補が複数ソースに出る場合は、repository URL、repo owner/name、install target、公式endpointなどで同一性を確認できたときだけ統合する
- 導入可能な候補があるなら、最初の候補提示でそのまま必要な導入確認まで進み、yes/no だけの往復を挟まない
- `vscode_askQuestions` ツールが使えるなら優先し、使えないなら通常のチャットで同じ項目を確認する
- ユーザーがインストールしないなら、その時点で終了する

確認する項目:

- 候補が複数で未指定: どの候補を入れるか、プロジェクトかグローバルか、表示名
- 候補が1件または対象確定済み: プロジェクトかグローバルか、表示名

認証方式、transport、Docker可否、追加環境変数は、候補確定後でよいなら後回しにします。installコマンド確定に必須な場合だけ同時に聞きます。

### 6. 導入とテスト

確定した導入対象に応じて追加します。

- npmパッケージ: `npx add-mcp [npmパッケージ名]`
- 引数付きstdioコマンド: `npx add-mcp "[実行コマンド 引数1 引数2 ...]"`
- HTTP URL: `npx add-mcp [HTTP URL]`

`add-mcp` で直接入れられない場合は、MCP用JSONの手動編集で対応できるかを確認し、編集前に許可を取り、無理ならカスタムMCPサーバー開発などの代替案を提示します。

スコープと表示名をコマンドへ反映します。例:

```bash
npx add-mcp -a vscode -n my-github github-mcp-server
npx add-mcp -a vscode -g -n my-github github-mcp-server
```

導入後は必ず次を行います。

1. MCPサーバーを接続して起動する
2. 必要な環境変数や認証情報を案内する
3. 安全なread系またはping系ツールを実行する。認証必須のリモートMCPで `401 Unauthorized` が返る場合は、到達成功かつ認証未完了として扱う
4. `npx add-mcp list -a vscode` と `npx add-mcp list -a vscode -g` の両方で導入確認する
5. テスト結果と利用可否を報告する

## 検索ヒント

| カテゴリ | 検索語例 | よくある用途 |
| --- | --- | --- |
| データベース | `postgres`, `sqlite`, `mysql` | クエリ、集計、書き込み |
| 開発ツール | `github`, `gitlab`, `git` | コード検索、PR、Issue |
| コミュニケーション | `slack`, `discord` | メッセージ、チャンネル |
| ファイル・OS | `filesystem`, `bash`, `cli` | ローカルファイル、コマンド実行 |
| 情報検索 | `brave`, `google`, `wikipedia` | Web検索、最新情報 |

## 候補が見つからない場合

1. 既存のMCPサーバーでは要件を満たせないことを伝える
2. エージェント標準機能などの代替案を提案する
3. Python または TypeScript でのカスタムMCPサーバー開発支援を提案する
