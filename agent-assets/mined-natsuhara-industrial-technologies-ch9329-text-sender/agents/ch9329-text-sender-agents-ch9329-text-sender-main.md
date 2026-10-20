# Agent 向け案内

CH9329（MR-CH9329EMU）へ ASCII テキストを送り、操作対象 PC に日本語109配列のキーボード入力として届ける WPF アプリです。

**作業規範は `.cursor/rules/` が正**です。本ファイルは入口（前提・リンク・コマンド）のみを扱います。

## 必読

- Cursor ルール: `.cursor/rules/`
  - `project-core.mdc` … 製品・技術固定・MVP 範囲・セキュリティ（常時適用）
  - `agent-safety.mdc` … 実機 COM とアプリ起動の扱い（常時適用）
  - `wpf-csharp.mdc` / `ch9329-protocol.mdc` / `testing.mdc` / `docs-writing.mdc`
- ハードウェア解説書（一次資料・外部）: [マルツ掲載 PDF](https://www.marutsu.co.jp/contents/shop/marutsu/datasheet/minnanolab_MR-CH9329EMU.pdf) / [みんなのラボ 製品ページ](http://minnanolab.net/product/pro_keyboardmouse/pro_keyboardmouse.html)
- アプリ仕様:
 - [docs/00-overview.md](docs/00-overview.md)
 - [docs/01-requirements.md](docs/01-requirements.md)
 - [docs/02-protocol-ch9329.md](docs/02-protocol-ch9329.md)
 - [docs/03-ui-ux.md](docs/03-ui-ux.md)
 - [docs/04-architecture.md](docs/04-architecture.md)
 - [docs/05-test-plan.md](docs/05-test-plan.md)
 - [docs/06-release.md](docs/06-release.md)

## 前提

- .NET 10 SDK / Windows（WPF）、シェルは PowerShell 5.1 互換
- 応答・仕様・UI 文言は日本語

## よく使うコマンド

```powershell
dotnet build Ch9329TextSender.sln
dotnet test Ch9329TextSender.sln
```

`dotnet run` はエージェントから実行しません（WPF ウィンドウが残るため）。動作確認はユーザーに依頼します。

プロトコル層は `src/Ch9329TextSender.Core/`（UI 非依存）。WPF は `src/Ch9329TextSender/`。

## リリース

- 公開リポジトリは 1 本。`main` は **Release 毎にコミット 1 個**（実装過程のコミットは push しない）
- タグ `vX.Y.Z` の push で `.github/workflows/release.yml` が動き、framework-dependent / self-contained の zip を GitHub Release に添付する
- 手順の正は [docs/06-release.md](docs/06-release.md)
- エージェントはタグ push や Release 作成を、ユーザーが明示依頼しない限り行わない

## 補助ツール

- サブエージェント: `spec-sync-auditor`（docs と実装の整合性）、`secret-leak-reviewer`（送信本文の漏えい検査）
- コマンド: `/build-check`、`/spec-update`
