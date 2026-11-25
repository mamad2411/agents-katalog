---
name: mastra-ai-architecture-rules
description: Mastra をランタイムとする AI サービスの設計・実装・リファクタリング時に使用する。agent / workflow / tool / workspace / memory / RequestContext / workflow state / 永続ストレージの責務分離を定義し、LLM に任せる範囲と決定的なコードに落とす範囲を判断する。single-agent first、workflow 最小化、state には参照・ID・要約のみを保持する原則、optional capability（workspace・memory・永続ストレージなど）は必要性が確認できた場合のみユーザー承認後に導入する原則を適用する。『Mastra で設計して』『workflow を作って』『agent と code の境界を決めて』『state に何を持つべきか整理して』『memory や workspace が必要か判断して』といった場面で使用する。
metadata:
  tags: [mastra, architecture, ai-agent, agent-design, workflow-design, ai, ai-workflow-design, tool-design, workspace, state-management, memory, request-context, storage, guardrails, anti-overengineering]
---

# Mastra AIサービス アーキテクチャ憲章

設計はまず **Mastra の既存プリミティブ** から始めること。カスタムのプログラムコードは、**決定性・安全性・可観測性・外部連携・コスト/レイテンシ最適化**に明確な価値がある場合にのみ追加する。

この憲章は **capability-aware** である。Mastra が提供するすべての機能が、すべてのプロジェクトで有効・必要とは限らない。
**Workspace、Memory、RequestContext、永続ストレージ、Observability、Evals、Browser、Vector DB などは optional** であり、**このリポジトリに既に存在する**か、**ユーザーが導入を明示承認した**場合にのみ前提としてよい。

---

## 0. Capability-aware 原則と導入承認ゲート

実装や設計変更の前に、必ずこのリポジトリの capability inventory を確認すること。

最低限、以下を明示すること：

- **既に存在するもの**: agents / workflows / tools / workspace / memory / request context / storage / observability / evals / browser / queues / external systems
- **存在しないが問題ないもの**: 今回の要件では不要な機能
- **追加したくなっているもの**: 追加理由があるが、まだ導入承認されていない機能

以下を守ること：

- このリポジトリに存在しない capability を、**Mastra が対応しているという理由だけで黙って追加しない**こと。
- **Workspace / Memory / 永続ストレージ / Vector DB / Observability / Evals / Browser / Queue / 追加パッケージ / インフラ依存**の導入は、ユーザーの明示承認なしに行わないこと。
- 欠けている capability が有用に見える場合でも、まずは**現在あるプリミティブだけで成立する最小設計**を提示すること。
- 欠けている capability の導入を提案する場合は、少なくとも以下を短い設計メモで示すこと：
  - 何の問題を解決するのか
  - なぜ既存 capability だけでは不十分なのか
  - 運用コスト・セキュリティ影響・データ保持影響
  - 追加される依存関係・設定・ストレージ・マイグレーション
  - ロールバック方法
- 承認前は、**既存 capability による degrade 可能な設計**に留めること。
- この憲章に書かれた各セクションは、**「存在する場合、または導入承認済みの場合に適用」**と解釈すること。
- **Mastra の version upgrade や新しい `@mastra/*` パッケージ導入**が、利用可能なプリミティブ・永続化挙動・ランタイム表面を増やす場合、それも approval-gated な設計変更として扱うこと。

---

## 1. 設計の根本原則

判断にはモデルを使う。
保証にはハーネスを使う。
決定的な実行にはコードを使う。

追加原則：

- **まず最小構成で始める**こと。
- **シンプルな composable pattern** を、複雑な抽象化より優先すること。
- エージェントの能力が上がったら(LLMのモデルを新規で追加したら)、ハーネスが肩代わりしていた処理を再評価し、不要になったものの削除を提案すること。
- **State は調停用**であり、**コンテキストのダンプ置き場ではない**。
- **payload ではなく reference を保存する**こと。
- **transcript ではなく decision を保存する**こと。
- **まず削れるものがないか考える**こと。足すのはその後でよい。

---

## 2. バイアス補正

この種の開発では、 **「プログラムを書きすぎ、agent に任せる範囲を狭くしすぎる」** 方向に偏りやすい。これを既知の失敗モードとして扱うこと。

コードを書く前に、必ず以下を先に検討すること：

- 指示を改善すれば済まないか
- ツール説明を改善すれば済まないか
- structured output を導入すれば済まないか
- スキーマを厳密化すれば済まないか
- 既存ツールを減らす・整理するだけで済まないか
- エージェントが既存ツールを使って自律的に調停できないか
- ワークフローを増やす代わりに、1ステップ内の agent 呼び出しと厳密な schema で済まないか

**推論の不足を、すぐプログラムで埋めないこと。**
まずは agent が持つ判断能力を活かせる形に整えること。

---

## 3. プリミティブ選択の優先順位

タスクを安全に解決できる **最もシンプルな選択肢** を選ぶこと。

1. 既存のエージェント + 既存のツール / instructions / skills / workspace 機能
2. より良い指示・より良いツール説明・より厳密な schema・structured output
3. 既存の workflow / step / tool / skill の再利用
4. 新規ツール
5. 新規ワークフローステップ
6. 新規ワークフロー
7. 新規の approval 境界 / suspend-resume 境界
8. 新規 supervisor / subagent / multi-agent 構成
9. 新規 capability の導入（memory / storage / workspace / observability / evals / browser / queue など）
10. 新規ラッパーフレームワーク・独自オーケストレーション層

このリストを一段階下るたびに、設計メモまたは PR に **明示的な根拠** を残すこと。

### 3.1 最新 Mastra 機能による簡素化レビュー

非自明な変更では、**現在この repo で使っている Mastra の機能**と、**最新 stable の Mastra docs / changelog で追加された機能**を比較し、**より少ないコード・ステップ・ラッパーで表現できる候補**があるなら、実装前に短く提案すること。

典型例（存在し、かつ承認条件を満たす場合のみ検討）：

- agent step の `structuredOutput` による output schema の自動整合
- `requestContextSchema` / 型付き RequestContext による request-scoped 値の検証と受け渡し
- workflow state / snapshots / suspend-resume / `stepExecutionPath` による実行経路・中断再開・監査の表現
- `Workspace.setToolsConfig()` や workspace 標準機能による plan-only / read-only / approval 後解放の表現
- Harness の built-in task tools による簡易タスク追跡
- `workingMemory.schema` / read-only memory / observational memory による memory 管理の簡素化
- `@mastra/server/schemas` による route contract の型推論

ルール：

- このレビューは、**新しい custom code / wrapper / workflow / capability を足す前に必ず行う**こと。
- まずは **現在インストール済みバージョンで使える機能** を優先すること。
- より簡潔な案が **version upgrade / 新しい `@mastra/*` package / storage / memory / workspace / browser / observability** を要する場合は、**代替案として提案するだけ**に留め、承認前に採用しないこと。
- 提案時は少なくとも以下を示すこと：
  - 何を簡潔化できるか
  - 何の custom code / step / wrapper を削減できるか
  - upgrade / migration / 互換性影響
  - 承認が必要かどうか

---

## 4. 責務の分担

### 4.1 エージェントの責務

エージェントは以下に使用する：

- 曖昧な要件の解釈
- オープンエンドな計画立案
- ツールの選択
- 追加調査や追加手順が必要かどうかの判断
- 十分な根拠が集まったかどうかの判断
- 統合・要約・比較・優先順位付け・最終回答の生成
- セマンティックな分類やルーティング

**エージェントはセマンティックな判断のデフォルト置き場**である。

### 4.2 ワークフローの責務

ワークフローは以下の場合にのみ使用する：

- 固定された処理順序
- 明示的な分岐
- 並列 fan-out / fan-in
- suspend / resume
- 人間による承認ゲート
- retry / timeout / deadline / throttling / idempotency 制御
- 決定的な調整処理

**ワークフローは実行を調整するものである。**
**エージェントの思考プロセスをワークフローで模倣してはならない。**

### 4.3 ツールの責務

ツールは以下に使用する：

- 型付きの副作用
- 決定的な操作
- 外部 API 呼び出し
- データベースの読み書き
- 検索・取得
- 変換処理
- 計算処理
- 外部ジョブの投入

すべてのツールは以下を満たすこと：

- 簡潔で曖昧でない説明
- 厳密な input schema
- 可能なら output schema
- 不要な payload を返さないこと
- filter / pagination / truncation を設計できる場合はそれを持つこと
- エラー時に、修正可能な入力のヒントを返すこと

### 4.4 ワークスペースの責務（存在する場合）

Workspace 機能は以下に使用する：

- ファイルの読み書き
- シェル実行
- コード検索・インデックス検索
- スキルの読み出し
- 一般的なコーディング操作

ルール：

- Workspace が構成されているなら、**薄いラッパーツールを増やす前に workspace 機能を優先**すること。
- ただし、以下が必要ならラッパーを作ってよい：
  - セキュリティ境界
  - 型付き正規化
  - 承認処理
  - 監査・可観測性
  - 明示的な UX 表現
- Workspace が存在しない場合、**それを前提に設計しない**こと。

### 4.5 メモリの責務（存在し、かつ要件上必要な場合）

Memory は **インタラクション横断的なコンテキスト** に使用する：

- ユーザーの好み
- 安定したプロジェクトの事実
- 長期的なゴール
- 重要な過去の意思決定
- 過去会話のうち、再利用価値が高いもの

ルール：

- **単発・stateless なサービスには memory をデフォルトで入れない**こと。
- セッション・タスク固有の作業コンテキストには **thread-scoped memory** を使うこと。
- スレッド横断で意図的に残したい安定事実にのみ **resource-scoped memory** を使うこと。
- Working memory は **安定した構造化事実** に使うこと。
- Semantic recall は **必要時に関連過去文脈を引く用途** に使うこと。
- 長い履歴の圧縮が必要なときだけ、要約的・観測的な memory を検討すること。
- ルーティングや監視だけの agent には、必要なら **read-only memory** を優先すること。
- Memory を **system of record** として使わないこと。
- Memory に **シークレットを保存しない**こと。

### 4.6 RequestContext の責務（存在する場合）

RequestContext は **リクエストスコープのランタイム情報** に使用する：

- 認証済み subject
- tenant / resource 識別子
- locale / language
- feature flags
- model tier
- budget 制約
- deadline
- 環境選択
- dry-run / production モード切り替え

ルール：

- RequestContext は **リクエスト単位の情報** に限ること。
- RequestContext に属する値を、長期 memory や workflow state に複製しないこと。
- RequestContext が存在しない場合は、**明示的な入力パラメータ**として渡すこと。

### 4.7 永続ストレージの責務（存在し、かつ導入承認済みの場合）

永続ストレージ・データベース・外部システムは以下に使用する：

- 権威ある業務記録
- 実行を跨いで保持すべき生成物
- 監査記録
- 外部ジョブの状態
- system of record のデータ
- 大きな文書・blob・検索インデックス

ルール：

- 大きな成果物は storage / file / DB に置き、workflow state には参照だけ置くこと。
- DB がないプロジェクトに、**便宜のためだけに新規永続化層を追加しない**こと。
- 永続化が必要なら、ユーザー承認付きで導入を提案すること。

---

## 5. ツール設計の品質基準

ツールは agent の能力を引き出すインターフェースである。以下を守ること：

- ツール名は、**人間の新メンバーに説明するように明確**であること。
- パラメータ名は曖昧にしないこと。`user` より `userId`、`query` より `searchQuery` を優先すること。
- 説明文には、対象リソース・前提条件・副作用・制約・期待される使い方を書くこと。
- 出力は **必要十分で token-efficient** にすること。
- 巨大な結果は丸ごと返さず、filter / page / select / summarize 可能にすること。
- エラーは「何が悪いか」だけでなく、「どう直せばよいか」まで示すこと。
- 複数の似たツールを乱立させないこと。**少数で境界が明確なツール群**を優先すること。
- ツールを追加する前に、**既存ツール説明の改善だけで解決できないか**を検討すること。

---

## 6. シンプルさの原則

- デフォルトアーキテクチャは、**エージェント 1つ + 最小限の有用なツール群** とする。
- 制御フローをコードで強制する必要がある場合にのみ、ワークフローを追加する。
- 各ワークフローステップは、**明確な責務をひとつだけ**持つこと。
- 推論を模倣するためだけに存在するワークフローは無効である。
- ワークフローステップを増やす前に、**structured output・より厳密な schema・より良い tool description** を優先すること。
- 決定的な動作や外部ツールが必要でない限り、スクリプトではなく **instructions / skills** を優先すること。
- 単一のツール呼び出しに対する薄いラッパーは、以下のうち少なくとも1つを追加しない限り作成しないこと：
  - セキュリティ境界
  - 型付き正規化
  - retry / backoff ポリシー
  - caching
  - 可観測性
  - 承認処理
  - UX 境界
- 新しいエージェントを追加する前に、**より良い指示・より良いツール説明・より良い schema・よりシンプルな単一エージェント設計**では不十分であることを先に示すこと。
- **マルチエージェントは最終手段**である。真の専門性分離・ツール過負荷・並列分解が必要な場合にのみ使用すること。
- 新しい capability の導入は、設計の曖昧さをごまかすショートカットとして使わないこと。
- 各新規プリミティブは、精度・レイテンシ・安全性・保守性において、そのコストに見合うものでなければならない。
- 迷ったら、**ステップを削除し、ラッパーを削除し、2つのプリミティブをマージする**こと。

---

## 7. オーバーエンジニアリング禁止ルール

- エージェントの内部的な思考を模倣するワークフローを構築しないこと。
- モデルが十分に実行できるオーケストレーション判断をハードコードしないこと。
- フィルタリング・変換・要約が先にできる場合、すべての中間結果をモデルに戻さないこと。
- ツールの完全な出力を workflow state にそのまま格納しないこと。
- 生の検索結果・巨大な表・大きな文書などであっても、まずは、圧縮などせずにLLMにコンテキストとして渡すようにすること。課題として報告があった際にはじめてコンテキストの圧縮を検討すること。
- 防止する具体的な障害モードを示さずに、新たな抽象化を導入しないこと。
- 既存のプリミティブを編集するだけで十分な場合、新しいプリミティブを作成しないこと。
- 単に「将来便利かもしれない」という理由で memory / storage / queue / browser / eval 基盤を追加しないこと。
- 既存 repo にない capability を、サンプルコードやドキュメントに出てきたという理由だけで追加しないこと。
- ファイル数・ステップ数・エージェント数・スキーマ数は、正当な理由がない限り増やさないこと。
- プロンプト改善で解決できる問題を、まずコードで解決しようとしないこと。

---

## 8. ハーネスの剪定ルール

モデルや周辺ツールの能力が変わったら、以下を定期的に再評価すること：

- 以前は必要だった固定ルーティング
- 過剰な前処理・後処理
- 重いフィルタラッパー
- context 圧縮ハック
- 不要になった multi-agent 分割
- 既に value を生まなくなった承認前の下準備ステップ

**「以前は必要だった」ことは、「今も必要である」ことを意味しない。**
より単純な構成で同じ品質・安全性・運用性が出るなら、古いハーネスの重りは削除すること。

---

## 9. 状態管理ポリシー

### 9.1 通常の直線的フローにはステップ入出力を使う

ある値が 1 ステップで生成され、次のステップでのみ消費される場合は、**ステップ出力として返す**こと。
共有 workflow state には格納しないこと。

### 9.2 ワークフロー状態は、実行スコープ内の共有・調整データにのみ使う

許可される例：

- 現在の phase / status
- 選択された strategy / plan identifier
- ファイルパス・record ID・external job ID などの artifact reference
- 複数ステップで必要な小さく正規化された事実や summary
- approval status と approval 保留メタデータ
- retry counter・timestamp・deadline・attempt metadata
- idempotency key・resume token・checkpoint marker
- 複数ステップで組み立てる最終 structured result
- token budget / time budget の残量
- どの evidence が採用済みかを示す軽量マーカー

### 9.3 ワークフロー状態に格納してはならないもの

- 生のチャット履歴
- プロンプトコンテキストのコピー
- 大きなツール出力
- 完全な検索結果
- 大きな文書
- シークレット・API キー・OAuth トークン・Cookie
- RequestContext に属するリクエストスコープ値
- Memory に属する長期的なユーザー設定や会話メモリ
- 永続ストレージに属する権威ある業務記録
- 再計算可能なデータ
- ステップ出力の重複コピー
- hidden reasoning / chain-of-thought

### 9.4 状態の品質ルール

- 状態は **小さく・型付き・シリアライズ可能・schema version 管理されたもの**であること。
- blob ではなく **reference / hash / summary** を格納すること。
- すべての state field は、少なくとも以下を答えられること：
  - 誰が書くか
  - 誰が読むか
  - いつ削除されるか
- phase が変わったら、不要になった古い field をクリアすること。
- state が膨張した workflow は設計の臭いであり、シンプル化対象である。

### 9.5 Snapshot-aware ルール

workflow state は scratchpad ではなく、**durable な調停データ**として扱うこと。
suspend / resume を使う workflow では、state・完了済みステップ出力・実行経路・中断メタデータが永続化対象になる前提で設計すること。
したがって、大きな payload を state に入れる設計は避けること。

---

## 10. メモリポリシー

- multi-turn の継続性が本当に必要な場合にのみ memory を使うこと。
- 単発の request-response サービスでは、まず memory なしで設計すること。
- session/task 固有の作業文脈には **thread scope** を優先すること。
- スレッド横断の安定事実にのみ **resource scope** を使うこと。
- ルーティング・監視・review 用 agent には、必要なら **read-only memory** を優先すること。
- memory template / schema は短く、更新しやすく、現在のタスクに本当に必要な項目だけ持つこと。
- memory を肥大化させるくらいなら、summary 化・整理・削除を優先すること。
- secrets・認証情報・system of record データを memory に保存しないこと。
- repo に memory が存在しない場合、それを当然視しないこと。

---

## 11. RequestContext ポリシー

- request ごとに変わる runtime 値は RequestContext に置くこと。
- requestContext の値を、workflow state や memory に長期保存しないこと。
- 認可判断・テナント境界・機能フラグ・モデル tier・予算制御などは request-scoped に処理すること。
- RequestContext がない repo では、同等情報を **明示的な引数**で渡すこと。

---

## 12. 安全性と境界ルール

- 不可逆または高リスクなアクションは、**型付き schema と approval gate を持つ明示的な tool** として定義すること。
- 既存ファイルは、書き込む前に読み込むこと。
- 外部アクセスは最小権限を優先すること。
- credential は適切な secret 管理・認証システムから取得すること。prompt・workflow state・memory から取得しないこと。
- ユーザー向けの pause / review / approval は、workflow の suspend / resume または tool の approval 境界で実装すること。
- 可能なら、本番システムに触れるアクションは dry-run または明示承認をサポートすること。
- broad な shell / filesystem / browser 権限は、信頼境界が明確な場合にのみ使うこと。

---

## 13. 可観測性と評価ルール

- 非自明な agent / workflow / tool は、可能なら trace 可能であること。
- 重要な agent 振る舞いには、可能なら scorer / eval による coverage を持たせること。
- observability や eval 基盤が repo に存在しない場合、それを黙って導入しないこと。必要なら承認を取ること。
- PR には実装の主張だけでなく、**検証の根拠**を含めること。
- 複雑さが増す場合は、評価カバレッジも増やすこと。
- 新しい抽象化が明確に test / trace / observe できない場合は、シンプル化すること。
- 最低限、以下を再現可能な形で残すこと：
  - 検証コマンド
  - 入力例
  - 期待される出力または判定基準
  - 1つ以上の edge case

---

## 14. コーディング前に必要な設計メモ

非自明な実装の前に、以下の見出しを持つ簡潔な設計メモを作成すること：

1. **Capability inventory と承認状態**
   1. - 既にあるもの
   2. - 今回は使わないもの
   3. - 追加したいが未承認のもの
2. **Goal**
3. **最小アーキテクチャ**
4. **責務の分担**
   1. - Agent
   2. - Workflow
   3. - Tool
   4. - Workspace
   5. - State
   6. - Memory
   7. - RequestContext
   8. - Persistent Storage
5. **よりシンプルな代替案を却下した理由**
6. **検証計画**
7. **モデルが能力を証明したら削除できるもの**
8. **ユーザー承認が必要な追加 capability の有無**
9. **最新 Mastra 機能で簡潔化できる候補**
    1. 現在使っている Mastra version / package
    2. 候補となる最新機能
    3. 置き換えまたは削減できる custom code / step / wrapper
    4. upgrade / migration / 承認影響

---

## 15. 非自明な変更に必要な成果物

非自明な変更にはすべて以下を含めること：

- 簡潔なアーキテクチャメモ
- 追加した各 workflow / tool / agent / capability の正当化理由
- 正確な検証コマンド
- 該当箇所の型付き schema
- 少なくとも 1 つの happy path 検証
- 少なくとも 1 つの異常系または edge case 検証
- agent 的挙動がある箇所の trace / eval / もしくは再現可能な観察記録
- 削除または意図的に回避したコード・ステップ・抽象化の一覧を含むシンプル化メモ
- **追加 capability がある場合は、その承認記録**
- **最新 Mastra 機能を採用または提案する場合は、current version・target version・追加 package・migration / rollback メモ**
  - 最新 Mastra 機能でこのドキュメントに記載のない新たな機能(capability)がある場合、ユーザーにドキュメントのアップデートを求めること

---

## 16. 完了の定義

変更が完了とみなされるのは、以下をすべて満たす場合のみ：

- ソリューションが最小限である
- 責務の分担が明示されている
- state の配置が正当化されている
- 検証の根拠が記録されている
- 決定性・安全性・可観測性を失わずに削除できる workflow / tool / agent が残っていない
- repo に元々存在しない capability を、未承認のまま持ち込んでいない
- 将来の model 能力向上時に削除候補となるハーネス部分が把握されている

---

## 17. 最後の確認

実装前に、自分に以下を問い直すこと：

- これは本当に workflow が必要か
- これは本当に tool が必要か
- これは本当に memory / storage / workspace 導入が必要か
- これは agent に任せるべき判断ではないか
- これは最新 stable の Mastra 機能で、より少ないコードに置き換えられないか
- これは state ではなく step output / requestContext / storage reference でよくないか
- これは削れるのではないか

**迷ったら、より少ないプリミティブで同じ成果を出す設計を選ぶこと。**
