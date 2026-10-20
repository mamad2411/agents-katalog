---
name: question-authoring-kcna
description: KCNA (Kubernetes and Cloud Native Associate) の問題集（slug kcna）に問題・解説を追加/修正するときの固有ルール（公式5ドメインに沿ったカテゴリ構成、コマンド暗記ではなく仕組み理解、全問viz図解、linux-basicsを前提にできる）。「Kubernetesの問題を追加して」「KCNAの問題集を作って」「k8sの問題を足して」で使う。共通ルールは question-authoring スキルにある。
---

# KCNA (Kubernetes and Cloud Native Associate)

**先に `question-authoring`（共通ルール・適用手順）と `explanation-clarity`（わかりやすさの方法論）を読むこと。ドリルの型は `question-authoring-linux` / `question-authoring-stats` を踏襲する（viz・大量生産の型はそちら準拠）。** ここは本問題集固有の情報だけ。

## この問題集の性格

**資格試験対策（CNCFの公式試験ドメインに準拠）でありながら、解説は教養ドリル並みに小学生でも分かるレベルに振り切る。** G検定・統計学の基礎と同じ「資格的な範囲設定」＋「Linux図解ドリルと同じ噛み砕き」のハイブリッド。

- 読者はソフトウェアQA畑6年の社会人（[[user_career_background]] 参照。実体は memory ディレクトリ）。Linux・コンテナ技術は知識ゼロに近い苦手意識がある。**`linux-basics` を前提にしてよい**（VMとコンテナの違い、namespace/cgroup、ネットワークの基礎は既習として扱える）。まだ解いていない可能性もあるので、初出時は一言で軽く思い出させてから先に進む
- **目的はkubectlコマンドやYAMLフラグの丸暗記ではなく「なぜKubernetesがこう設計されているのか」の本質理解。** 「なぜPodという単位があるのか」「なぜコントローラは"あるべき状態"を宣言する方式なのか」を主役にする
- **解説は小学生でも分かるレベルに振り切る**（stats-basics/linux-basics/G検定と同じトーン）。ただし読者は大人なので漢字は普通に使う
- **全問に `viz`（1枚の図解SVG）を付ける。** これがこのドリルの看板。図なしの問題を足さない
- QAエンジニアとしての実務接点があれば `usecase` や `eg` で拾ってよい（例: ヘルスチェック＝QAの死活監視観点、CI/CDパイプライン＝テスト自動化の延長、ロールアウト＝段階的リリースの品質保証と接続、宣言的な「あるべき状態」の考え方はテストのアサーションに近い）。ただし無理にこじつけない
- 将来のロードマップ（CKA、[[user_learning_roadmap]]）の土台になる領域。KCNAは"広く浅く"の試験なので、深掘りしすぎず「概念と全体像」を優先する

## 出題範囲（CNCF公式5ドメイン。カテゴリはこの範囲に対応させる）

| ドメイン（公式配分） | このドリルでの扱い |
|---|---|
| Kubernetes Fundamentals（46%） | 第一期のメイン。Pod/コントローラ/Service/設定分離/ストレージなど土台全部 |
| Container Orchestration（22%） | 第二期。スケジューリング、オートスケーリング、ヘルスチェック、ネットワークポリシー |
| Cloud Native Architecture（16%） | 第三期。マイクロサービス、サーバーレス、CNCFランドスケープ、IaC |
| Cloud Native Observability（8%） | 第四期。テレメトリ、ログ/メトリクス/トレース、Prometheusの考え方 |
| Cloud Native Application Delivery（8%） | 第五期。CI/CD、GitOps、Helm、ロールアウト戦略 |

## 科目とセット構成

| slug | 名前 | 状態 |
|---|---|---|
| `kcna` | KCNA（Kubernetes and Cloud Native Associate） | 構築中 |

1 subject に複数カテゴリで持つ（linux-basics/stats-basicsと同じ方式）。

### 第一期（sort 0-7）— Kubernetes Fundamentals ドメイン

依存順（前のカテゴリの理解が後の前提になるよう並べる）:

| カテゴリ（完全一致で JOIN） | sort | 内容の芯 |
|---|---|---|
| `Kubernetesとは何か` | 0 | なぜコンテナが増えると1つ1つ手で管理できなくなるか、オーケストレーションという発想、指揮者とオーケストラの比喩。前提: linux-basicsの`コンテナの正体` |
| `クラスタの構造（コントロールプレーンとノード）` | 1 | クラスタ＝コントロールプレーン＋ワーカーノード、APIサーバーが唯一の窓口、etcdが正の情報源、スケジューラが配置を決める、コントローラマネージャが監視・是正する、kubelet/kube-proxy/コンテナランタイムの役割分担 |
| `Podという最小単位` | 2 | なぜコンテナを直接デプロイせずPodという単位を挟むのか、Pod内のコンテナはネットワーク/ストレージを共有、Podは使い捨て（ephemeral）、Podごとに1つのIP |
| `宣言的な管理とkubectl` | 3 | 命令的（このコマンドを打て）と宣言的（あるべき姿を書く）の違い、マニフェスト(YAML)、kubectlはAPIサーバーへの窓口にすぎない、コントロールループ（あるべき姿と実際の姿を比べ続けて是正する）という考え方 — 以降全カテゴリの前提になる核 |
| `ReplicaSetとDeployment` | 4 | 「あるべきレプリカ数」を宣言する発想、セルフヒーリング（落ちたPodを自動で作り直す）、ローリングアップデートとロールバック、なぜPodを直接作らずDeployment経由にするのか |
| `Serviceとラベル・セレクタ` | 5 | Podは使い捨てでIPが変わる→安定した窓口が要る、ラベルとセレクタで「どのPod群か」を指定する仕組み、ClusterIP/NodePort/LoadBalancerの違い |
| `ConfigMapとSecretによる設定分離` | 6 | 設定をコンテナイメージに焼き込まない理由（環境ごとに作り直さずに済む）、ConfigMapとSecretの役割分担、なぜSecretは別扱いか |
| `Volumeとデータの永続化` | 7 | コンテナのファイルシステムは使い捨て（linux-basicsの復習）、Podが再作成されるとデータが消える問題、Volumeで外に逃がす発想、PV/PVCの概念だけ触れる（深掘りは第二期以降） |

**第一期（sort 0-7）は2026-08-02に投入済み。全8カテゴリ・40問（各5問）、全問viz付き。**

### 第二期（sort 8-13予定）— Container Orchestration ドメイン

「Kubernetesの問題を拡大して」の指示があったら、以下を追加する:

| カテゴリ（完全一致で JOIN） | sort | 内容の芯 |
|---|---|---|
| `スケジューリングの仕組み` | 8 | スケジューラがどうノードを選ぶか、リソースリクエスト/リミット、Taint/Tolerationの概念（深入りしない） |
| `ヘルスチェックとPodのライフサイクル` | 9 | Liveness/Readinessプローブ、QAの死活監視観点と接続しやすい回、Podのフェーズ（Pending/Running/Succeeded/Failed） |
| `オートスケーリングの考え方` | 10 | HPA（水平）の発想、負荷に応じて増減させる理由 |
| `StatefulSetとDaemonSet` | 11 | Deploymentとの違い（状態を持つワークロード、全ノードに1つずつ配置） |
| `Jobとバッチ処理` | 12 | 常駐しない一回きりの処理、CronJob |
| `ネットワークポリシーの基礎` | 13 | デフォルト全通信許可、絞る発想（linux-basicsの権限の考え方と接続） |

### 第三期以降（sort 14-）— Cloud Native Architecture / Observability / Delivery

指示があったら都度、CNCFの公式ドメイン定義を確認しながら設計する。候補: `マイクロサービスという設計` `サーバーレスの考え方` `CNCFランドスケープとは` `IaCの発想（Terraformとの接続）` `ログ・メトリクス・トレースの違い` `Prometheusの考え方` `CI/CDとGitOps` `Helmとパッケージ化` `ロールアウト戦略（カナリア/ブルーグリーン）`。

## source_ref

`kcna-q<N>`（ゼロ埋めしない）。

## 問題の形

- 4択 single。問題文は1〜3文。**身近な比喩か、QAエンジニアが実務で遭遇しそうな場面**から入ってよい（本番でPodが急に消えた、設定を環境ごとに変えたい、リリース後にすぐ切り戻したい、など）。無理にシナリオ化せず、素直な「〜はどれか」でもよい
- 誤答は「隣の概念」を置く（PodとDeploymentの混同、ConfigMapとSecretの混同、ClusterIPとNodePortの混同など）。共通ルールの長さ縛り（正解を単独最長にしない）を厳守
- `code` 列は基本使わない。YAMLの例を見せたいときも「読ませて覚えさせる」より`think`/`eg`で仕組みを言葉に開くことを優先。どうしても例が理解の助けになる場合のみ`snippet`に短く置く（暗記のためではなく仕組みの確認用）
- **kubectlのフラグ・YAMLキーの列挙暗記は問わない。**「これは何のためにあるか」「なぜこの設計か」を問う

## 解説の流儀

linux-basics/stats-basicsと同じキー構成:

| 要望 | キー |
|---|---|
| 何がどういう意味か | `asked` + `kid`（ざっくり言うと） |
| たとえで直感 | `eg`（一番力を入れる） |
| なんのためにあるか | `why_asked`（「この仕組みが無いと何に困るか」） |
| どういうことに役立つか | `usecase`（実務の場面。QA/CI/自動化と繋がるなら拾う） |

加えて `point`（決め手1文）・`terms`（2〜4個）・`think`（因果の背骨。「なぜこの設計か」を鎖でつなぐ）・`vs`（隣接概念との違い。「Pod vs コンテナ」「Deployment vs ReplicaSet」「ConfigMap vs Secret」「ClusterIP vs NodePort」など）・`opt`・**`viz`（全問必須）**。

## viz（図解SVG）の書き方

`question-authoring-stats` の「viz（図解SVG）の書き方」節に完全準拠（viewBox・配色・PNG目視検証手順すべて同じ）。KCNA固有の定番の型:

- 層構造（コントロールプレーン→ノード→Pod→コンテナ、のような積み木）
- 箱と矢印（kubectl→APIサーバー→etcd、コントロールループの監視→是正の循環矢印）
- 循環矢印（コントロールループ：あるべき姿↔実際の姿を比べ続ける）
- 2列比較（Pod vs コンテナ、Deployment vs ReplicaSet、ConfigMap vs Secret）
- 複数の箱→1つの安定した窓口（Service：ゆらぐPod群→固定のService）
- 使い捨てvs永続（Volumeなしのコンテナ＝消えるメモ、Volumeあり＝ロッカーに預ける）

## 内容の注意

- **kubectlコマンドの列挙・フラグ暗記を目的にしない。** 「これを実行すると何が起きているか」を問う
- Pod回は「コンテナとの違い」を必ず`vs`で拾う。ここが一番の誤解ポイント（Pod＝1コンテナの言い換え、ではなく「1つ以上のコンテナ＋共有ネットワーク/ストレージの箱」）
- 宣言的管理（`宣言的な管理とkubectl`カテゴリ）は以降全カテゴリの前提になる核なので、ここで「あるべき姿を書く→コントローラが監視して是正し続ける」という型を確実に腹落ちさせる。以降のカテゴリ（特にDeployment・HPA・StatefulSet）でこの型を繰り返し参照してよい
- linux-basicsで既習の概念（namespace/cgroup、VMとコンテナの違い、ネットワークの基礎）は「復習」の一言で軽く触れるに留め、重複説明はしない。ただし**Kubernetesのnamespaceは、Linuxカーネルのnamespaceとは別物**（前者はクラスタ内のリソースを論理的に区切る仕組み、後者はプロセスの隔離機構）なので、この2つを混同させない`vs`を`Kubernetesとは何か`または該当回で必ず1問は立てる
