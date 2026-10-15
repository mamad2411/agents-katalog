---
name: write-research
description: >-
  調査結果を .artifacts/research/[topic].md へ書き込む時に使用する。
  結論・根拠・参考ソースをテンプレートに沿って構造化し、ナレッジベースとして蓄積する。researcher が使用する。
user-invocable: false
allowed-tools: [Read, Write, Edit]
---

# research/[topic].md 書き込みワークフロー

調査結果を `.artifacts/research/[topic].md` へ書き込む手順を定義する。
ナレッジベースとして他エージェントが再利用する前提で構造化する。

<workflow>

1. `Read` で `./template.md` を読み込む。
1. `[topic]` を簡潔な英単語またはスネークケースのフレーズにする（例: `jwt_refresh`、`sqlalchemy_session`）。
1. テンプレートのセクション構成を維持し、`Write`（新規）または `Edit`（既存）で書き込む。
1. 同じトピックは既存ファイルを更新し、異なるトピックは新規ファイルを作成する。

</workflow>

<principles>

- **結論を先に書く**: 結論を先頭に置き、その後に根拠・参考ソースを続ける。
- **参照ソースを明記する**: 参照した URL やドキュメントを明記し、後から検証できるようにする。
- **事実と推測を分ける**: 不明点は「不明」と明記し、推測と事実を混在させない。
- **自己完結を保つ**: ナレッジベースとして他エージェントが再利用する前提で、簡潔かつ自己完結した記述にする。

</principles>
