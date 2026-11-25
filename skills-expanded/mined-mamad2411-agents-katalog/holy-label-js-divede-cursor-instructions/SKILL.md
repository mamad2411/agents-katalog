# HOLY LABEL プロジェクト - AI開発支援指示書

## 🤖 Cursor AI への指示

### プロジェクト理解
あなたは HOLY LABEL 外部ライブラリプロジェクトの開発支援を行います。このプロジェクトは、BASEプラットフォームの制約を回避するため、JavaScript・CSSを外部CDNライブラリ化したモジュラーシステムです。

#### 重要な制約
- **ファイルサイズ**: BASE HTMLファイル 150,000文字制限
- **外部ライブラリ**: 合計50KB以下維持
- **後方互換性**: 既存APIの破壊は絶対禁止
- **命名規則**: `window.HolyLabel*` プレフィックス必須

## 📁 ファイル構成の理解

### 編集可能ファイル（重要）
```
js/src/          # JavaScript ソースファイル（編集対象）
├── dom-utils.js                   # DOM操作基盤
├── page-state.js                  # ページ状態管理
├── animation-config.js            # アニメーション設定
├── animation-manager.js           # アニメーション管理
├── navigation-manager.js          # ナビゲーション管理
├── modal-utils.js                 # モーダル機能
├── product-gallery.js             # 商品ギャラリー
├── loadmore-manager.js            # Ajax読み込み
├── logo-manager.js                # ロゴ管理
├── initialization-manager.js      # 初期化管理
├── language-manager.js            # 多言語管理
└── scroll-manager.js              # スクロール管理

css/src/         # CSS ソースファイル（編集対象）
├── foundation.css                 # 基本スタイル
├── layout.css                     # レイアウト
├── base-menu.css                  # メニュー
├── product-components.css         # 商品コンポーネント
├── animations.css                 # アニメーション
├── product-detail.css             # 商品詳細
├── forms.css                      # フォーム
├── responsive.css                 # レスポンシブ
├── footer-pages.css               # フッター
├── special-pages.css              # 特殊ページ
├── ui-components.css              # UIコンポーネント
└── base-integration.css           # BASE統合
```

### 編集禁止ファイル（重要）
```
js/dist/         # 圧縮済みライブラリ（自動生成、編集禁止）
css/dist/        # 圧縮済みライブラリ（自動生成、編集禁止）
```

## 🛠️ 開発支援の方針

### 1. ファイル編集時の必須チェック

#### 編集前
- 編集対象が `src/` フォルダ内であることを確認
- `dist/` フォルダの直接編集は絶対に提案しない
- 依存関係の理解（Phase 1→2→3→4の順序）

#### 編集後
- ビルドコマンドの実行を必ず提案
- ファイルサイズチェックの実行
- 動作テストの実行

### 2. コード提案の原則

#### JavaScript開発
```javascript
// ✅ 推奨する提案パターン
window.HolyLabelNewFeature = {
    init: function() {
        // 初期化処理
        const DOMUtils = window.HolyLabelDOMUtils;
        if (!DOMUtils) {
            console.error('HolyLabelDOMUtils not found');
            return;
        }
        // 機能実装
    }
};

// ❌ 避ける提案パターン
const NewFeature = {  // プレフィックスなし
    init() {
        document.querySelector('.element').classList.add('active'); // null チェックなし
    }
};
```

#### CSS開発
```css
/* ✅ 推奨する提案パターン */
.hl-new-component {
    background-color: var(--primary-bg, #0B101D);
    color: var(--primary-text, #ffffff);
    padding: var(--space-md, 32px);
}

/* ❌ 避ける提案パターン */
.new-component { /* プレフィックスなし */
    background-color: #0B101D; /* ハードコーディング */
    padding: 32px; /* CSS変数不使用 */
}
```

### 3. 機能提案時のアプローチ

#### 新機能追加
1. **既存ライブラリの拡張を優先**
   - 新しいファイル作成より既存ファイルの拡張
   - 依存関係の最小化

2. **段階的実装**
   - 小さな機能から段階的に追加
   - 各段階でテスト実行

3. **ドキュメント更新**
   - 重要な変更時はドキュメント更新も提案

#### バグ修正
1. **最小限の修正**
   - 影響範囲を最小限に抑制
   - 根本原因の特定

2. **テスト強化**
   - 修正箇所のテスト追加
   - 回帰テストの実行

## 🔍 デバッグ支援

### 1. 問題診断のアプローチ

#### JavaScript エラー
```javascript
// デバッグ用テストコード提案
const debugHolyLabel = () => {
    console.group('🔍 HOLY LABEL Debug');
    
    // ライブラリ存在確認
    const libraries = [
        'HolyLabelDOMUtils',
        'HolyLabelNavigationManager',
        'HolyLabelAnimationManager',
        'HolyLabelProductImageGallery'
    ];
    
    libraries.forEach(lib => {
        console.log(`${lib}:`, typeof window[lib]);
    });
    
    // DOM要素存在確認
    const elements = [
        '#js-hamburger',
        '.shop-nav',
        '.product-item'
    ];
    
    elements.forEach(selector => {
        const element = document.querySelector(selector);
        console.log(`${selector}:`, !!element);
    });
    
    console.groupEnd();
};
```

#### CSS スタイル問題
```javascript
// CSS変数チェック用コード提案
const checkCSSVariables = () => {
    const styles = getComputedStyle(document.documentElement);
    const cssVars = [
        '--primary-bg',
        '--primary-text',
        '--space-md'
    ];
    
    console.group('🎨 CSS Variables Check');
    cssVars.forEach(variable => {
        const value = styles.getPropertyValue(variable);
        console.log(`${variable}:`, value || 'undefined');
    });
    console.groupEnd();
};
```

### 2. パフォーマンス診断

#### ファイルサイズチェック
```javascript
// ファイルサイズ監視コード提案
const checkFileSizes = async () => {
    const files = [
        'holy-label-js-divede.html',
        // CDN URLs for external libraries
    ];
    
    console.group('📊 File Size Check');
    for (const file of files) {
        try {
            const response = await fetch(file);
            const blob = await response.blob();
            const sizeKB = (blob.size / 1024).toFixed(2);
            console.log(`${file}: ${sizeKB} KB`);
        } catch (error) {
            console.error(`Error checking ${file}:`, error);
        }
    }
    console.groupEnd();
};
```

## 📋 コード提案テンプレート

### 1. JavaScript機能追加
```javascript
// 機能名: [機能名]
// 依存関係: [依存するライブラリ]
// 影響範囲: [影響を受けるファイル]

window.HolyLabel[機能名] = {
    // 初期化フラグ
    initialized: false,
    
    // 設定オブジェクト
    config: {
        // デフォルト設定
    },
    
    // 初期化メソッド
    init: function(options = {}) {
        if (this.initialized) return;
        
        // 依存関係チェック
        const DOMUtils = window.HolyLabelDOMUtils;
        if (!DOMUtils) {
            console.error('HolyLabelDOMUtils not found');
            return;
        }
        
        // 設定マージ
        this.config = Object.assign(this.config, options);
        
        // 機能実装
        this.setupEventListeners();
        
        this.initialized = true;
        console.log('✅ HolyLabel[機能名] initialized');
    },
    
    // イベントリスナー設定
    setupEventListeners: function() {
        // イベント設定
    },
    
    // 公開メソッド
    publicMethod: function() {
        if (!this.initialized) {
            console.warn('HolyLabel[機能名] not initialized');
            return;
        }
        // メソッド実装
    }
};

// 自動初期化（DOMContentLoaded後）
document.addEventListener('DOMContentLoaded', () => {
    window.HolyLabel[機能名].init();
});
```

### 2. CSS コンポーネント追加
```css
/* 
 * コンポーネント名: [コンポーネント名]
 * 依存: foundation.css, layout.css
 * 用途: [用途説明]
 */

.hl-[コンポーネント名] {
    /* 基本スタイル - CSS変数使用 */
    background-color: var(--primary-bg, #0B101D);
    color: var(--primary-text, #ffffff);
    padding: var(--space-md, 32px);
    
    /* レスポンシブ対応 */
    @media (min-width: 768px) {
        padding: var(--space-lg, 48px);
    }
}

.hl-[コンポーネント名]__element {
    /* サブ要素のスタイル */
}

.hl-[コンポーネント名]--modifier {
    /* バリエーション */
}

/* 状態クラス */
.hl-[コンポーネント名].-active {
    /* アクティブ状態 */
}

/* アニメーション */
.hl-[コンポーネント名] {
    transition: var(--transition-base, all 0.3s ease);
}
```

## 🚀 ビルド・デプロイ支援

### ビルドコマンド提案
```bash
# JavaScript ビルド
cd js && npm run build

# CSS ビルド  
cd css && npm run build

# 全体ビルド
npm run build:all

# ファイルサイズチェック
npm run size-check

# ローカルテスト
npm run test:local
```

この指示書に従って、HOLY LABELプロジェクトの効率的で安全な開発支援を提供してください。 