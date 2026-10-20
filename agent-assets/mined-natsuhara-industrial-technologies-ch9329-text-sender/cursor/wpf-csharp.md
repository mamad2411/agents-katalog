---
description: WPF / C# の構成・コーディング規約
globs: **/*.cs, **/*.xaml, **/*.csproj
alwaysApply: false
---

# WPF / C#

## 配置

- アプリ本体: `src/Ch9329TextSender/`
- プロトコル・キーマップ・シリアルは UI から分離する（純 C# でバイト列生成をテスト可能にする）
- 推奨の関心分離: PacketBuilder / KeyMap（JP109）/ SerialDevice / View（または ViewModel）

## スタイル

- file-scoped namespace、nullable enable を前提
- `.editorconfig` に従う（C# インデント 4、XAML 2）
- UI スレッドをブロックする長い送信は `async` + キャンセル可能にする

## UI

- 複数 COM を一覧表示し、選択中デバイスへ接続・送信する
- MVP は **選択中 1 台のみ接続**（同時接続はしない）
- 接続状態・エラーをユーザーに分かる文言で表示する（送信本文は表示ログに残さない）

## 禁止

- code-behind にプロトコルバイト列を直書きしない
- 実機 COM への破壊的・無限ループ送信をデフォルト動作にしない
