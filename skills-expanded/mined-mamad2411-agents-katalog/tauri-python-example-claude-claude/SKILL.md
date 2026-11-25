# Tauri + Python + Selenium Example

## プロジェクト概要
TauriフレームワークとPython、Seleniumを統合したデスクトップアプリケーションのサンプルプロジェクトです。

## 主な技術スタック
- **Tauri 2.x** - クロスプラットフォームデスクトップアプリフレームワーク
- **Python 3.9+** - バックエンド処理（PyO3経由）
- **Selenium WebDriver** - ブラウザ自動化
- **webdriver-manager** - ChromeDriverの自動管理
- **uv** - Python パッケージマネージャー

## プロジェクト構造
```
tauri-python-example/
├── dist/                      # フロントエンドビルド出力
│   └── index.html            # UI（Pythonテスト用ボタン）
├── src-tauri/
│   ├── src/                  # Rustソースコード
│   │   ├── lib.rs           # Tauriプラグイン設定
│   │   └── main.rs          # エントリーポイント
│   ├── src-python/          # Pythonコード
│   │   └── main.py          # Python関数定義
│   ├── .venv/               # Python仮想環境
│   ├── Cargo.toml           # Rust依存関係（PyO3有効）
│   └── tauri.conf.json      # Tauri設定
├── package.json             # Node.js依存関係
└── README.md               # プロジェクトドキュメント
```

## 開発コマンド

### セットアップ
```bash
# Node.js依存関係
npm install

# Python環境（src-tauriディレクトリで実行）
cd src-tauri
uv venv .venv
uv add selenium webdriver-manager
```

### 開発
```bash
# 開発サーバー起動（ホットリロード対応）
npm run tauri dev
```

### ビルド
```bash
# リリースビルド（最適化あり）
npm run tauri build

# デバッグビルド
npm run tauri build -- --debug
```

## 主な機能

### 実装済み機能
1. **Pythonテスト** - Python実行環境の確認
2. **バージョン表示** - Pythonバージョン情報取得
3. **Seleniumテスト** - ブラウザ自動化デモ（Google検索）

### Pythonバインディング
- `tauri-plugin-python`を使用
- PyO3フィーチャー有効（システムPython使用）
- 関数は`_tauri_plugin_functions`配列で登録

### ビルド時の注意点
- `src-python/`ディレクトリがバンドルに含まれる
- ビルドされたアプリは`/`ディレクトリで実行される
- venvが見つからない場合、自動的にpipインストールを試みる

## トラブルシューティング

### よくある問題
1. **`__file__`が定義されていない**
   - バンドルされたアプリでは`__file__`が使えない
   - 代替として`os.getcwd()`を使用

2. **Seleniumが見つからない**
   - 開発環境: `.venv`から読み込み
   - 本番環境: 自動的にpipでインストール

3. **ChromeDriverエラー**
   - webdriver-managerが自動的にダウンロード
   - 初回実行時はインターネット接続必要

## GitHub
- リポジトリ: https://github.com/yonaka15/tauri-python-example
- ライセンス: MIT

## 今後の拡張案
- [ ] Flask/FastAPIサーバー統合
- [ ] データベース連携
- [ ] より複雑な自動化タスク
- [ ] Windows/Linux対応テスト
- [ ] CI/CDパイプライン構築