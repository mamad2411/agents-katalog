# AGENTS.md

このファイルは、Googleカレンダーテンプレート開発プロジェクトにおけるAIエージェント（Antigravity、Claude Code、GitHub Copilot、Cline、Roo Code等）専用の開発ルールとガイドラインです。開発を進める前に必ず読み込み、すべての指示を厳格に遵守してください。

---

## Setup commands

プロジェクトの開発、ビルド、検証に必要なコマンド一覧です。タスクの実行や動作確認にはこれらのコマンドを使用してください。

- 依存関係のインストール: `npm install`
- 開発モード起動 (ファイル変更の監視): `npm run dev`
- プロジェクト全体のビルド: `npm run build`
- Content Script のみビルド: `npm run build:content`
- Popup UI のみビルド: `npm run build:popup`
- 静的アセットのコピー: `npm run copy:assets`

---

## Code style & Rules

### TypeScript と厳格な型安全
- **厳格な型チェック**: `tsconfig.json` の `strict: true` は必須です。`any` 型の使用は極力避け、適切なインターフェースや型定義を行ってください。
- **型定義の集約**: カスタム型やインターフェースは `src/types/index.ts` に定義・集約してください。
- **Null / Undefined 対策**: オプショナルチェイニング (`?.`) および Null合体演算子 (`??`) を積極的に活用し、予期せぬクラッシュを防止してください。

### 命名規則とファイル構成
- **snake_case の強制**: プロジェクト内の変数名、関数名、ファイル名、ディレクトリ名には **snake_case** を使用します。
- **定数ファイルの集約**: CSSセレクタや各種静的定数は、`src/constants/` ディレクトリ配下にまとめて定義します。

### コーディングスタイル
- **関数の宣言**: 原則としてアロー関数を優先します（モジュール直下のトップレベル関数は通常の `function` 宣言も許容）。
- **非同期処理**: プロミスチェーン (`.then()`) は避け、直感的な `async / await` を使用します。
- **エラーハンドリング**: すべての非同期処理やDOM操作には `try-catch` ブロックを設け、エラー発生時には詳細なコンソールログ（絵文字付き）を出力してください。

### 絵文字付きデバッグログ
ログを出力する際は、重要度や目的に応じて必ず以下のプレフィックス（絵文字）を使用してください。

- 🔵 `[Info]` - 一般的な情報通知、動作の流れの記録
- ✅ `[Success]` - 特定の処理や操作が正常に完了したことの通知
- ⚠️ `[Warning]` - 致命的ではないが注意が必要な状態、フォールバックの適用時
- ❌ `[Error]` - 例外のキャッチ、処理の失敗、必須要素の不在
- 📍 `[Position]` - 要素の挿入場所やインジェクションポイントの特定ログ
- 🔍 `[Search]` - DOM要素の検索や待機プロセスの開始ログ

---

## Project Architecture

リポジトリの主要なディレクトリとファイルの構成です。

```
google-calendar-template/
├── src/
│   ├── constants/        # CSSセレクタや固定値の定義
│   │   └── selectors.ts  # GoogleカレンダーのDOMセレクタ定義（最重要）
│   ├── utils/            # 再利用可能な汎用ユーティリティ関数
│   │   ├── dom.ts        # DOM操作（waitForElement, setFieldValue 等）
│   │   ├── storage.ts    # Chrome Storage API との連携
│   │   └── variables.ts  # テンプレート用変数置換エンジン
│   ├── types/            # TypeScript 型定義
│   │   └── index.ts      # 共通の型宣言ファイル
│   ├── content/          # Content Script（Googleカレンダー画面に挿入）
│   └── popup/            # Popup UI（拡張機能の設定・管理画面）
├── dist/                 # ビルド出力ディレクトリ（Git管理除外）
├── docs/                 # ドキュメント（INSTALL_GUIDE.md 等）
├── manifest.json         # Chrome拡張マニフェスト (Manifest V3)
├── package.json          # プロジェクトメタデータ・スクリプト
└── tsconfig.json         # TypeScript設定
```

---

## Chrome Extension Selectors & DOM Operations

Googleカレンダーは動的かつ複雑なDOM構造を持ち、定期的に内部クラス名やマークアップが変更されます。以下の原則に従って堅牢なDOM操作を行ってください。

### セレクタ設計の原則
1. **`aria-label` を最優先**: 多言語対応や動的変更に強いため、属性セレクタ `[aria-label="..."]` を優先して要素を特定します。
2. **ランダムクラスの排除**: `.XvJf4c` などの自動生成された難読化クラスは将来的に破損する可能性が高いため、直接の依存は避けてください。
3. **セレクタの定義場所**: すべてのCSSセレクタは `src/constants/selectors.ts` 内の定数オブジェクトに集約し、コード内に直接ハードコードしないでください。

### DOM操作のベストプラクティス
- **非同期要素待機 (`waitForElement`)**: 
  Googleカレンダーのポップアップやフィールドは動的に生成されます。要素取得時には必ず `waitForElement(selector, timeout)` を用いて非同期待機を挟んでください。
- **堅牢な値設定 (`setFieldValue`)**:
  Googleカレンダーは内部で React / AngularJS 等のフレームワークを使用しており、単に `input.value = "..."` を設定しただけでは内部状態が更新されません。値を設定する際は、以下のイベントを一連のシーケンスで実行する `setFieldValue` ユーティリティを使用してください。
  1. `element.focus()`
  2. 値の書き換え (`element.value` または contenteditable の `innerText`)
  3. `input` イベントの発火
  4. `change` イベントの発火
  5. `element.blur()`
- **contenteditable 要素の扱い**:
  予定の「説明（Description）」フィールドなど `contenteditable="true"` の要素に対しては、セキュリティ上の観点（TrustedHTML対応）から、`innerHTML` は絶対に使用せず、必ず `innerText` を介して安全にテキストを注入してください。

---

## Chrome Storage & Variables

### テンプレートの保存スキーマ
`chrome.storage.local` に保存されるテンプレートのTypeScript型定義は以下の通りです（`src/types/index.ts` より抜粋）。

```typescript
export interface Template {
  id: string;                  // UUID
  name: string;                // テンプレート管理名
  title: string;               // 予定のタイトル
  description?: string;        // 予定の説明
  location?: string;           // 予定の場所
  guests?: string[];           // ゲストのメールアドレス一覧
  duration?: number;           // 予定の期間（分単位）
  allDay?: boolean;            // 終日イベントフラグ
  guestPermissions?: {         // ゲストの権限設定
    modify: boolean;
    inviteOthers: boolean;
    seeGuestList: boolean;
  };
  order: number;               // 表示並び順
  createdAt: string;           // 作成日時 (ISO String)
  updatedAt: string;           // 更新日時 (ISO String)
  calendarName?: string;       // 適用対象のカレンダー名
}
```

### 変数システム (Variable Engine)
テンプレート適用時に、以下の11種類の変数を自動で解析し、現在の日時やユーザー情報に置換します（`src/utils/variables.ts`）。

- `{{date}}` - `YYYY-MM-DD` 形式（例: `2026-06-02`）
- `{{date_jp}}` - 日本語日付形式（例: `2026年06月02日`）
- `{{date_calendar}}` - Googleカレンダー表示風（例: `2026年 6月 2日`）
- `{{time}}` - 時分形式（例: `19:45`）
- `{{datetime}}` - 完全な日時（例: `2026/06/02 19:45:30`）
- `{{day_of_week}}` - 曜日名（例: `火曜日`）
- `{{year}}` - 西暦4桁（例: `2026`）
- `{{month}}` - 月（例: `06`）
- `{{day}}` - 日（例: `02`）
- `{{user_email}}` - ログイン中のGoogleアカウントのメールアドレス
- `{{user_name}}` - ログイン中のユーザーの表示名

---

## Git & Commit Conventions

コミットメッセージはすべて日本語で記述し、変更内容に応じて以下の絵文字プレフィックスを先頭に付与してください。

- ✨ `[Feat]` - 新機能の追加、仕様変更の反映
- 🐛 `[Fix]` - バグの修正、セレクタ変更への追従
- 📝 `[Docs]` - ドキュメント（README.md、INSTALL_GUIDE.md 等）の修正や追加
- 🚀 `[Release]` - バージョンアップ、リリース準備、開発フェーズの区切り

コミットメッセージの例:
```
✨ テンプレート選択UIの配置を最適化
🐛 ポップアップでの値設定バグを修正
📝 README を更新
```

---

## Agent Guidelines

エージェント（あなた）が本プロジェクトで作業する際の行動指針です。

1. **自律的な品質維持**: コードを変更した後は、必ず `npm run build` を実行して、ビルドに失敗していないか、TypeScriptのコンパイルエラーが発生していないかを確認してください。
2. **安全第一のDOM変更**: セレクタが正しく機能しているか、フォールバックの動作はどうなっているかを注意深く分析し、既存のカレンダーの表示を崩さないようにスタイリング（CSS）を細心の注意を払って記述してください。
3. **既存仕様の維持**: 特別な理由がない限り、既存のヘルパー関数（`dom.ts`, `storage.ts` など）を再利用し、重複するロジックを新設しないようにしてください。
