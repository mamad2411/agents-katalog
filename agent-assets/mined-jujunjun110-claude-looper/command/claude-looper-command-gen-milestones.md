あなたはプロジェクトの Milestone 設計者です。

## やること

ユーザーから与えられたドキュメントを読み、プロジェクトの Milestone 一覧を設計する。
各 Milestone のゴール（何が動く状態になるか）を定義する。
Task の細分化は Milestone 着手時に計画セッションが行うため、ここでは Milestone レベルの設計のみ行う。

### 前提: 設計ドキュメント

このコマンドの引数としてドキュメントのパスが与えられることを期待する。
引数がない場合、または指定されたファイルが存在しない場合は、以下のメッセージを返して終了する:

> 設計ドキュメントのパスを指定してください。
> ドキュメントがまだない場合は `/plan` コマンドで作成し、そのパスを引数に指定してください。
>
> 例: `/gen-milestones docs/application-overview.md`

### 手順

1. 引数で指定されたドキュメントを読む
2. docs/ 配下のドキュメントを読む
   - [docs/architecture.md](docs/architecture.md): アーキテクチャ
   - [docs/frontend.md](docs/frontend.md): フロントエンド
   - [docs/infrastructure.md](docs/infrastructure.md): インフラストラクチャ
   - [docs/quality.md](docs/quality.md): 品質
3. CLAUDE.md を読む
4. `looper/run.sh` を読み、milestones.json がどのように消費されるかを理解する
5. 既存コードがあれば Glob/Grep で現状を把握する
6. 既存の looper/milestones.json があればアーカイブする（後述）
7. Milestone を設計する
8. looper/milestones.json を出力する
9. git add looper/milestones*.json && git commit -m "chore: generate milestones"

## アーカイブ

looper/milestones.json が既に存在する場合、新しい milestones.json を生成する前にリネームしてアーカイブする:

```bash
mv looper/milestones.json "looper/milestones.$(date +%Y%m%d_%H%M%S).json"
```

これにより過去の Milestone 履歴が保持される。アーカイブ済みファイルは run.sh からは参照されない。

## 出力フォーマット

唯一の成果物は looper/milestones.json。

```json
{
  "source": "docs/tasks/YYYYMMDD_HHMM_設計ドキュメント名.md",
  "milestones": [
    {
      "milestone": 1,
      "goal": "何が動く状態になるか（1文、具体的に）",
      "verification": "pnpm lint && pnpm typecheck && pnpm build",
      "done": false,
      "tasks": []
    },
    {
      "milestone": 2,
      "goal": "...",
      "verification": "pnpm test && pnpm lint && pnpm typecheck",
      "done": false,
      "tasks": []
    }
  ]
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| source | string | 元の設計ドキュメントのパス（引数で渡されたファイル） |
| milestones[].milestone | number | Milestone 番号（1 始まり、昇順） |
| milestones[].goal | string | この Milestone が完了したとき何が動く状態か（1文、具体的に） |
| milestones[].verification | string | Milestone 完了時の通過条件コマンド |
| milestones[].done | boolean | 常に false（ループが更新する） |
| milestones[].tasks | array | 常に空配列（Milestone 着手時に計画セッションが生成する） |

## Milestone の設計方針

### 機能スライスで Milestone を分ける

**各 Milestone は「1つの機能が UI からバックエンドまで縦に通って動く」単位で切る。**
レイヤーごとの横割り（domain 全部 → infrastructure 全部 → UI 全部）にしない。

Milestone 間は逐次実行。Milestone 内の Task は並列実行される。
Milestone の境界は「次の Milestone が前の Milestone の成果物を import する」ところ。

### 構成パターン

1. **基盤 Milestone**: プロジェクト構成、ツールチェーン、認証など横断的な基盤。`docs/quality.md` で定義された品質チェックツール（dependency-cruiser 等）のセットアップも含め、verification コマンドが通る状態にすること。DB を使うプロジェクトでは、ローカル DB のセットアップ（`supabase init` 等）もこの Milestone に含め、以降の Milestone で DB が使える状態にする。**環境変数の初期化もこの Milestone に含める**（後述「環境変数の初期化」を参照）
2. **最初の機能 Milestone**: 最もシンプルな機能を1つ選び、model → repository → usecase → UI を縦に通す。ここで全レイヤーの実装パターンが確立される
3. **追加機能 Milestone**: 確立したパターンに乗せて、1 Milestone = 1機能ずつ追加していく

### 大方針: 実際に動かすことを最優先する

**各 Milestone のゴールは「実際に動作確認できる状態」でなければならない。**

コードが存在するだけでは不十分。`pnpm dev` して実際にその機能を手で触って確認できること。

- DB 永続化なら → ローカル Supabase で実際にデータが保存・表示される
- 外部 API 連携なら → **実 API キーを使って本物の API で動作する状態をゴールとする**（`docs/infrastructure.md` の「外部 API 依存の扱い」を参照）
- 認証機能なら → 開発環境で認証フローが動作する（ローカル Supabase Auth）

**Stub は開発・テスト用のフォールバック**であり、Milestone の goal 文に Stub 動作を書かない。goal には実 API（Claude API, OpenAI API, Slack API 等）で動作することを明示する。Stub 実装自体は `docs/infrastructure.md` に従い Gateway interface に対して用意するが、それは goal の達成条件ではない。

「コードは書いたが動かしたことがない」状態で Milestone を完了にしてはならない。

### 環境変数の初期化

基盤 Milestone のゴールには、以下の環境変数セットアップを含めること:

1. **ルート `.env` にある変数を `apps/{app}/.env.local` にコピーする**（Next.js はルートの `.env` を読まない）
2. **アプリが必要とするが `.env` に存在しない変数は `dummy` で埋める**（Stub 動作のトリガーになる）
3. **ローカル Supabase の接続情報を `.env.local` に設定する**（`supabase start` の出力から取得）

これにより、API キーの有無に関わらず `pnpm dev` と E2E テストが動作する状態を基盤 Milestone で保証する。

### goal の書き方

- 悪い例: "DDD レイヤー構造で構成され、Gateway interface が定義される"（横割りで何も動かない）
- 悪い例: "OAuth のコードが実装され、開発環境ではダミーユーザーでバイパスできる"（コードはあるが動かしていない）
- 悪い例: "チェック機能が動作する（API キーなしでは Stub で動作）"（Stub 前提で書いている）
- 良い例: "/rules ページで表現ルール（NG表現→推奨表現）の一覧表示・新規登録・編集・削除ができ、DB に永続化される"（1機能が動く）
- 良い例: "Claude API による5観点チェックが実行され、実際の AI レスポンスによる結果一覧が表示される"（実 API 動作を明示）

goal は具体的に「何が動くか」「何ができるか」を書く。計画セッションがこの goal を見て Task を分解する。

### verification

- 既存のプロジェクトコマンドだけ使う: `pnpm test`, `pnpm typecheck`, `pnpm lint`, `pnpm build`
- 外部 API を叩かない（ループが毎回機械的に実行するため）
- **UI の変更を伴う Milestone では Playwright で実際の UI の動作確認を行う**
  - URL の直接アクセス（`page.goto()` 等）は禁止。UI 上のクリック操作によって画面遷移すること
  - 初期ページ（トップページ等）へのアクセスのみ `page.goto()` を許可する

### Milestone の粒度

- 1 Milestone = 1つの独立した機能が動く状態になる粒度を目安にする
- 複数の機能を1 Milestoneにまとめすぎない
- Milestone 番号は 1 から連番
- tasks は全て空配列（計画セッションが Milestone 着手時に W1-W5 の Task を生成する）
