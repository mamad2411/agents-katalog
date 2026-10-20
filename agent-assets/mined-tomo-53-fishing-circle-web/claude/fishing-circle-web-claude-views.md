# src/resources/views — Blade テンプレート

UI を構成する Blade テンプレート。サーバ側認可と組み合わせた二重防御でコンテンツを保護する。

## 責務（ディレクトリ別）

| ディレクトリ / ファイル | 責務 |
|---|---|
| `layouts/` | 共通レイアウト（`x-app-layout` / `x-guest-layout`） |
| `components/` | 再利用 Blade コンポーネント。`components/layout/public`（`<x-layout.public>`）は公開下層ページの共通レイアウト、`components/layout/page-hero`（`<x-layout.page-hero>`）はその見出し帯 |
| `groups/` | グループ一覧・詳細・メンバー管理画面 |
| `auth/` | ログイン・登録・パスワードリセット（Breeze 標準） |
| `profile/` | プロフィール編集 |
| `emails/` | メール通知テンプレート |
| トップ直下 | `dashboard`・`welcome` 等の汎用画面。公開下層ページ `about` / `activities` / `gallery` / `join` は `<x-layout.public>` に載せる（トップと同じヘッダー・時間帯テーマ・濃紺トーン） |
| `welcome/` | トップページの partial（`_head` / `_header` / `_theme-toggle` は下層ページの `<x-layout.public>` でも共用）。詳細は [`welcome/CLAUDE.md`](welcome/CLAUDE.md)（opening は一時撤去・作り直し予定） |

## 公開下層ページの書き方

```blade
<x-layout.public title="サークル紹介" description="（任意）meta description">
    <x-layout.page-hero label="About Us" title="サークル紹介" lead="（任意）短いリード" />
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-20 md:pb-24">…本文…</div>
</x-layout.public>
```

- カードは `bg-white/5 border border-white/10 rounded-2xl`、見出しは `text-white`、本文は `welcome-text-muted`、強調は `text-sky-300`。白背景前提の濃い文字色（`text-gray-700` 等）は使わない。
- 新しい公開ページを足すときは `welcome/_header` の `$siteNavItems` にルート名を追加する（現在ページに `aria-current="page"` が付く）。

## 重要な実装ルール

- ユーザー入力の出力は `{{ }}` で自動エスケープ。`{!! !!}` は原則禁止（XSS対策）。
- フォームには必ず `@csrf`。状態変更は POST/PATCH/DELETE + `@method('...')` で行う。
- `@can` / `@auth` は表示制御のみ。**サーバ側認可の代替にしない**（ミドルウェア / Policy が本体）。
- Enum の表示には `label()` / `shortLabel()` を使う（例: `{{ $userGroup->permissionLevel->label() }}`）。

## 参照

- Blade/フロントエンド規約 → `.cursor/rules/blade-frontend.mdc`
- セキュリティ規約 → `.cursor/rules/security.mdc`（XSS・CSRF・二重防御の方針）
- ルート CLAUDE.md → `/CLAUDE.md`

## 更新ルール

このディレクトリ配下に新しい画面グループを追加・変更・削除したら、このファイルの責務表も同じ変更で更新すること。
規約の本体は `.cursor/rules/` とルート `CLAUDE.md` にあるため、ここには重複させず参照に留める。
矛盾を見つけたらルート / rules 側を正とし、本ファイルを修正する。
