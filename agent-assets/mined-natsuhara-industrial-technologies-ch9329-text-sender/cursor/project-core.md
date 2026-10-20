---
description: Ch9329 Text Sender のプロジェクト前提・作業規範
alwaysApply: true
---

# Project Core

## 製品

- CH9329（みんなのラボ MR-CH9329EMU / USB 接続版）向け **ASCII テキスト送信** WPF アプリ
- 用途: パスワード入力など、操作対象 PC へのキーボード入力
- キー配列: **日本語 109 配列**（マニュアル付録のキーコード表に準拠）
- 複数台の COM デバイスから送信先を選択できること

## 技術固定

- Windows のみ、WPF、`net10.0-windows`
- シェルは PowerShell 5.1 互換
- 応答・仕様・ルールの言語は **日本語**

## MVP 範囲 / 非目標

- 含む: ポート列挙・複数デバイス選択・接続/切断・許可 ASCII 送信・末尾 Enter オプション・設定の永続化
- 含まない（当面）: 日本語 IME、マウス、メディアキー、マクロ編集、末尾 Enter 以外の特殊キー UI（Tab / Backspace など）、複数台同時接続
- 詳細は `docs/00-overview.md` と `docs/01-requirements.md` が正

## ドキュメント

- 一次資料（外部）: [マルツ掲載の解説書 PDF](https://www.marutsu.co.jp/contents/shop/marutsu/datasheet/minnanolab_MR-CH9329EMU.pdf)（製品ページ: http://minnanolab.net/product/pro_keyboardmouse/pro_keyboardmouse.html）
- アプリ仕様は `docs/` に自前で要約する（外部 PDF だけに依存しない。リポジトリにベンダー PDF は置かない）
- 実装前に該当仕様を読む。挙動を変えたら仕様も更新する

## セキュリティ

- 送信テキスト（パスワード想定）をログ・例外メッセージ・コミットに出さない
- 秘密情報ファイルをリポジトリに追加しない

## Git

- ユーザーが明示しない限り commit / push しない
