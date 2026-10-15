---
name: tauri-bump-version
description: Tauriアプリのバージョンを上げる。パッチ/マイナー/メジャーを選択して更新。
user-invocable: true
---

# Tauri Bump Version

Tauriアプリのバージョンを更新するスキル。

## 手順

### 1. 現在のバージョン確認

`app/src-tauri/tauri.conf.json` の `version` フィールドから現在のバージョンを取得し、ユーザーに表示する。

### 2. バージョンタイプの選択

AskUserQuestion でユーザーに選択させる:

- **パッチ** (x.y.Z): バグ修正などの小さな変更
- **マイナー** (x.Y.0): 新機能追加などの変更
- **メジャー** (X.0.0): 破壊的変更を含むリリース

### 3. バージョン更新

以下のファイルを新しいバージョンに更新する:

1. `app/src-tauri/tauri.conf.json` — `version` フィールド
2. `app/src-tauri/Cargo.toml` — `version` フィールド
3. `app/src-tauri/Cargo.lock` — `cd app/src-tauri && cargo generate-lockfile` で自動更新

### 4. 結果報告

更新したバージョン (旧 → 新) と対象ファイルをユーザーに報告する。
