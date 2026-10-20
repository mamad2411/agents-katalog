---
name: export-schedule-conventions
description: Swift/SwiftUIコードの追加・変更、UI文字列やローカライズ(String Catalog)対応の追加、テストの追加・更新を行う際に使用する。ExportScheduleプロジェクトのアーキテクチャ・命名規則・String Catalogのキー命名規則・テスト更新方針を確認する。
---

# ExportSchedule コーディング規約

作業を始める前に、リポジトリルートの `AGENTS.md` を読むこと。アーキテクチャ(Models/Logic/Services/ViewModels/Views の責務分離)、命名規則、ビルド・テストコマンド、バージョン関連の注意点など詳細はすべてそこに書かれている。

以下は今すぐ手を動かす際に見落としやすい2点のチートシート。詳細や背景は上記の通り `AGENTS.md` を参照すること。

## String Catalog のキー命名規則

新規キーは `ExportSchedule/Localizable.xcstrings` に `ja`(原文)/`en` 両方を手動追加する(`defaultValue:` は使わない)。

**キーは例外なく `画面(またはドメイン).機能.要素` のドット区切りの記号的な形式にする。日本語原文をキーにしない。** 画面固有なら画面名(`settings.*`, `output.*`, `preview.*`, `action.*`, `content.*`)、複数画面で共有するなら横断ドメイン名(`weekday.*`, `error.*`, `event.*`)をトップレベルにする。

```swift
AppSection("settings.dateRange.title") { ... }
errorMessage = String(localized: "error.accessDenied")
Text(String(format: String(localized: "settings.outputFormat.exampleLabel"), previewSample))
```

プレースホルダーが必要なら `%d`/`%@` の書式文字列をカタログに登録し `String(format:)` で埋める。

## テスト更新の判断

実装(コード)を変更したら、`ExportScheduleTests`(Swift Testing)の更新・追加が必要かを必ず判断する。必要なら `FreeSlotCalculatorTests.swift` / `ScheduleTextFormatterTests.swift` の既存パターンに倣って更新する。

## その他

- `git commit` はユーザーの明示的な指示がない限り実行しない。
