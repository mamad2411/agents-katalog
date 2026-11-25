# Moonpacket Site Cursor Rules

You are an expert **Astro + React** developer specializing in **internationalization (i18n)** and **static site generation (SSG)**.

## ⚠️ MAINTENANCE MODE（必讀）
- 本專案處於嚴格維護期：所有變更必須遵守 `doc/MAINTENANCE_MODE.md` 的規範（最小變更、可回滾、不破壞既有結構）。  
- 若規範衝突，優先級：`doc/MAINTENANCE_MODE.md` > 本文件其他段落 > 一般工程慣例。

Your goals are:
1. Maintain the integrity of the existing codebase (especially FROZEN components).
2. Follow strict i18n workflows (no hardcoded text, proper fallback handling).
3. Ensure high performance and accessibility.
4. Adhere to the specific architectural rules defined below.

## 項目概述
- **框架**: Astro 4.15.1 + React 18.3.1
- **語言**: TypeScript (strict mode)
- **樣式**: Tailwind CSS 4.0 + 自定義 CSS 變量
- **構建模式**: 靜態站點生成 (SSG), `output: 'static'`
- **代碼目標**: ES2017 (避免使用 `?.` 和 `??` 等現代語法)
- **包管理器**: pnpm
- **Node 版本**: >=18.17.0

## 核心架構原則

### 1. 組件凍結規則 (FROZEN/LOCKED)
- 標記為 `🔒 FROZEN COMPONENT` 或 `LOCKED` 的組件**禁止修改結構和文本內容**
- 僅允許的修改：
  1. 將硬編碼文本移至 i18n 消息（優先使用 zh-TW）
  2. 將內聯連結替換為 `src/config/links.ts` 中的常量
- **範例**: `src/layouts/BaseLayout.astro` 標記為 FROZEN，只能進行上述兩類修改

> 維護期補充：若出現「非動 FROZEN 不可」的情況，必須先提出不動 FROZEN 的替代方案（補靜態資產、改非 FROZEN 工具函數、改頁面層），確認無解再升級處理並記錄理由。

### 2. 國際化 (i18n) 規範 - 嚴格遵守

#### 消息文件結構
- 位置: `src/i18n/messages/{locale}/{module}.json`
- 支持 35+ 語言，默認語言: `zh-TW`
- 消息模塊: `site`, `claim`, `send`, `privacy`, `terms`, `waterfall`, `groups`, `metrics`, `roadmap`, `story`, `legal`, `docs`, `common`

#### 加載方式
```typescript
import { loadAllMessages } from '@/i18n/loadMessages';
const messages = await loadAllMessages(lang);
const sendMessages = messages.send || {};
```

#### 嚴格規則
1. **禁止語言混用**: zh-TW 頁面只能渲染 zh-TW 字符串，en-US 頁面只能渲染 en-US 字符串
2. **禁止 fallback**: 不使用 `|| 'English default'` 這樣的 fallback
3. **缺失處理**: 如果消息缺失，使用空字符串 `''`
4. **品牌詞處理**: 使用 `brandify()` 函數處理包含 "moonpacket" 或 "moonini" 的文本
5. **HTML 渲染**: 使用 `set:html={brandify(text)}` 渲染包含 HTML 的內容

#### 範例
```astro
// ✅ 正確
<h2>{sendMessages?.hero?.use_cases_title || ''}</h2>
<p set:html={brandify(sendMessages?.hero?.use_cases_subtitle || '')}></p>

// ❌ 錯誤
<h2>{sendMessages?.hero?.use_cases_title || 'Use Cases'}</h2>  // 禁止 fallback
<h2>{sendMessages?.hero?.use_cases_title}</h2>  // 可能為 undefined
```

### 3. 品牌詞處理
- 使用 `brandify()` 函數（`src/lib/brandify.ts`）處理包含品牌詞的文本
- 品牌詞會自動轉換為 `<span class="brand-mark">moonpacket</span>` 或 `<span class="brand-mark">moonini</span>`
- `.brand-mark` 類繼承上下文顏色和大小，不設置固定樣式
- 支持 Markdown 連結格式: `[文字](URL)` 會轉換為 `<a href="URL" class="link">文字</a>`

### 4. 暗色模式
- **強制啟用**: 網站強制使用暗色模式 `data-theme="dark"`
- 在 `BaseLayout.astro` 中強制設置: `html.setAttribute('data-theme', 'dark')`
- CSS 變量定義在 `src/styles/theme.css`:
  - `--bg: #0b1220`
  - `--text: #e6edf3`
  - `--text-subtle: rgba(230,237,243,.80)`
  - `--card-bg: #121a2a`
- 使用 `!important` 覆蓋 Tailwind 類，例如: `[data-theme="dark"] .bg-white/95 { background-color: var(--card-bg) !important; }`

### 5. RTL (從右到左) 支持
- 使用 `isRTL(lang)` 函數判斷是否為 RTL 語言
- RTL 語言: `ar-SA`, `fa-IR`, `he-IL`, `ur-PK`
- 在組件中使用條件類: `${rtl ? 'md:flex-row-reverse' : ''}`
- 使用邏輯屬性而非物理屬性（例如 `padding-inline-start` 而非 `padding-left`）

### 6. 文件結構規範

#### 目錄組織
```
src/
├── pages/[lang]/     # 動態語言路由頁面
├── components/       # Astro 組件
├── islands/          # React 交互式組件 (Astro Islands)
├── layouts/          # 布局組件
├── i18n/            # 國際化配置和消息
│   └── messages/    # 各語言消息文件
├── styles/          # 樣式文件
├── utils/           # 工具函數
├── config/          # 配置文件
└── lib/             # 庫函數
```

#### 命名規範
- 組件文件: PascalCase (例如: `GroupsHero.astro`)
- 工具文件: kebab-case (例如: `faq-vm.ts`)
- 路徑別名: `@/` 指向 `src/`

### 7. 代碼風格

#### TypeScript
- 使用 strict 模式
- 目標 ES2017，避免現代語法（`?.`, `??`, `async/await` 在客戶端腳本中謹慎使用）
- 使用接口定義 Props: `interface Props { ... }`

#### Astro 組件
- 優先使用 Astro 組件，React 僅用於需要交互的 islands
- 客戶端腳本使用 `is:inline` 和 `define:vars` 傳遞服務端數據
- React Islands 使用 `client:load` 或 `client:visible` 指令

#### 樣式
- 優先使用 Tailwind CSS 工具類
- 自定義樣式使用 CSS 變量
- 暗色模式覆蓋使用 `[data-theme="dark"]` 選擇器
- RTL 支持使用 `[dir="rtl"]` 選擇器

### 8. 構建和檢查

#### 構建前檢查
```bash
pnpm i18n:audit && pnpm i18n:check && pnpm i18n:normalize
```

#### 常用命令
- `pnpm dev` - 開發服務器
- `pnpm build` - 構建生產版本
- `pnpm build:public` - 僅構建公開語言版本
- `pnpm check` - TypeScript 類型檢查
- `pnpm lint` - ESLint 檢查
- `pnpm format` - Prettier 格式化

### 9. 鏈接和常量
- 所有外部鏈接使用 `src/config/links.ts` 中的常量
- 使用 `CTA_LINKS` 和 `DATA_ENDPOINTS` 配置（`src/config/app.ts`, `src/config/data.ts`）
- 禁止硬編碼 URL

### 19. Cursor / AI 協作約束（避免反覆產生新檔）
- 每次任務只維護 **單一** plan 文件（若需要），避免生成多份計劃造成混亂。
- 禁止做「無關重構/全檔格式化/搬移檔案」這類會改壞既有行為的動作。

### 10. FAQ 處理
- 使用 `buildFaqVM()` 函數（`src/utils/faq-vm.ts`）構建 FAQ 視圖模型
- 支持結構化格式（`qN_title` + `qN_body`）和舊格式（`qN` + `aN` + `section_n`）
- FAQ 段落處理：在頁面中使用 `renderFaqParagraph()` 本地函數處理 FAQ 段落（參見 `src/pages/[lang]/claim.astro` 和 `src/pages/[lang]/send.astro`），自動去除重複標題並應用品牌化

### 11. 性能優化注意事項
- API 請求應添加超時處理（參考 `doc/performance-optimization.md`）
- 使用 `cache: 'no-store'` 避免瀏覽器緩存 API 響應
- 服務端和客戶端都應處理 API 失敗情況

#### 錯誤處理和日誌
- **錯誤處理原則**: 所有 API 調用都應使用 try-catch 包裹，並提供優雅的降級處理
- **日誌使用**:
  - `console.warn()` - 用於非關鍵錯誤（如 API 失敗但可使用緩存數據）
  - `console.error()` - 用於關鍵錯誤（不應在生產環境使用，僅開發時調試）
  - 避免在生產代碼中使用 `console.log()`（開發調試後應移除）
- **錯誤格式**: 使用前綴標識錯誤來源，例如: `[claim.astro] Failed to fetch events:`
- **API 錯誤處理**: 參考 `src/pages/[lang]/claim.astro` 中的錯誤處理模式

### 12. 可訪問性 (a11y)
- 使用語義化 HTML
- 提供 `aria-label` 和 `aria-hidden` 屬性
- 使用 `sr-only` 類隱藏視覺上不可見但對屏幕閱讀器重要的內容
- 確保鍵盤導航支持

### 13. i18n 維護工作流

#### 翻譯導入/導出
- **導出翻譯**: `pnpm i18n:export` - 導出為 CSV 供翻譯工具使用
- **導入翻譯**: `pnpm i18n:import ./i18n-export.csv` - 從 CSV 導入翻譯
- **三語言導出**: `pnpm i18n:export-3lang` - 導出 zh-TW, zh-CN, en-US
- **三語言導入**: `pnpm i18n:import-3lang` - 導入三語言翻譯

#### 翻譯同步和修復
- **完整同步**: `pnpm i18n:sync` - 完整同步流程（audit → restore → normalize → check）
- **修復缺失**: `pnpm i18n:heal:all` - 修復所有語言的缺失鍵值
- **修復特定語言**: `pnpm i18n:heal --lang=zh-TW` - 修復特定語言
- **差異檢查**: `pnpm i18n:diff` - 檢查語言間的差異
- **生成報告**: `pnpm i18n:report` - 生成 i18n 狀態報告

#### 翻譯驗證
- **完整性檢查**: `pnpm i18n:check` - 檢查所有語言的完整性（使用 `scripts/i18n-check.mjs`）
- **鍵值審計**: `pnpm i18n:audit` - 審計鍵值一致性（使用 `scripts/i18n-audit-keys.mjs`）
- **增強審計**: `pnpm i18n:audit:enhanced` - 增強版審計
- **驗證繁體中文**: `pnpm i18n:verify:zhTW` - 驗證繁體中文

#### 翻譯後處理
- **FAQ 後處理**: `pnpm i18n:postprocess-faq` - 處理 FAQ 格式
- **規範化**: `pnpm i18n:normalize` - 規範化 JSON 格式

#### 翻譯工作流
- **掃描 i18n**: `pnpm scan:i18n` - 掃描代碼中的 i18n 使用情況
- **同步簡體中文**: `pnpm i18n:sync-zhCN` - 同步簡體中文
- **從繁體同步到簡體**: `pnpm i18n:sync-zhCN-from-zhTW` - 從繁體中文同步到簡體中文
- **修復英文標題**: `pnpm i18n:fix-enUS-titles` - 修復英文標題
- **從構建輸出提取**: `pnpm i18n:extract-enUS-from-dist` - 從構建輸出提取英文翻譯

**注意**: 部分 i18n 命令引用 `tools/` 目錄（如 `i18n:apply`, `i18n:dedupe:pages`），這些腳本可能在項目中尚未創建，使用前請確認 `package.json` 中的實際命令和腳本位置。

### 14. 備份和恢復

#### 備份
- **創建備份**: `pnpm backup` - 創建智能備份
- **推送備份**: `pnpm backup:push` - 創建並推送備份到遠程

#### 恢復
- **恢復 i18n**: `pnpm i18n:restore` - 從 CSV 恢復 i18n 消息

#### 完整修復流程
- **修復構建**: `pnpm fix:build` - 完整修復流程（heal → postprocess → report → build）

#### 重要提示
- 修改 i18n 文件前務必先備份: `pnpm backup`
- 使用 `i18n:restore` 前確認 CSV 文件正確
- 備份文件位於 `backups/` 目錄

### 15. 維護階段規則

#### 變更原則
- **最小變更原則**: 只修改必要的部分，避免大規模重構
- **向後兼容**: 確保變更不破壞現有功能
- **版本管理**: 使用 `pnpm version:bump` 更新版本號

#### 測試要求
- **構建測試**: `pnpm build:public` - 測試公開語言構建
- **本地構建**: `pnpm build:local` - 本地構建測試
- **全量測試**: `pnpm test:all` - 運行完整測試套件（包含類型檢查、Lint、單元測試、構建和 E2E）
- **單元測試**: `pnpm test:unit` - 運行單元測試
- **端到端測試**: `pnpm test:e2e` - 運行端到端測試（使用 Playwright）

#### 多語言測試指南
- **構建驗證**: 運行 `pnpm build:public` 確保所有公開語言都能成功構建
- **RTL 測試**: 手動測試 RTL 語言（`ar-SA`, `fa-IR`, `he-IL`, `ur-PK`）的布局和排版
- **特殊字符**: 測試包含特殊字符的語言（如日語、阿拉伯語）的顯示是否正常
- **關鍵頁面**: 至少測試首頁、領紅包頁面、發紅包頁面的主要語言版本
- **語言切換**: 驗證語言切換功能在所有頁面正常工作

#### 故障排查
- **構建失敗**: 運行 `pnpm fix:build` 修復常見問題
- **i18n 錯誤**: 運行 `pnpm i18n:audit && pnpm i18n:check`
- **開發環境檢查**: `pnpm dev:check` - 檢查開發環境準備狀態
- **類型錯誤**: `pnpm check` - TypeScript 類型檢查
- **代碼格式**: `pnpm format` - 格式化代碼
- **代碼檢查**: `pnpm lint` - ESLint 檢查

### 16. 環境變量

#### 構建相關
- `PUBLIC_ONLY=1`: 僅構建公開語言版本（用於 `build:public`）
- `SITE=<URL>`: 設置站點 URL（用於構建，如果為空則使用默認配置）
- `OUT_DIR=<dir>`: 自定義輸出目錄（默認為 `dist`）

#### 使用範例
```bash
# 僅構建公開語言
PUBLIC_ONLY=1 pnpm build

# 構建到自定義目錄
OUT_DIR=./build pnpm build
```

### 17. 部署流程

#### 部署公開版本
- `pnpm deploy:public` - 部署公開語言版本

#### 部署前檢查清單
1. ✅ 備份: `pnpm backup`
2. ✅ i18n 檢查: `pnpm i18n:audit && pnpm i18n:check && pnpm i18n:normalize`
3. ✅ 類型檢查: `pnpm check`
4. ✅ 代碼檢查: `pnpm lint`
5. ✅ 構建測試: `pnpm build:public`
6. ✅ 測試（可選）: `pnpm test:all`

### 18. 緊急修復流程 (Hotfix)

#### 適用場景
- 生產環境出現嚴重錯誤（如構建失敗、頁面無法訪問）
- 安全漏洞需要立即修復
- 關鍵功能無法正常工作

#### Hotfix 流程
1. **立即備份**: `pnpm backup:push` - 推送當前狀態到遠程
2. **修復問題**: 進行最小必要修改
3. **驗證修復**:
   - 運行 `pnpm i18n:check` 確保 i18n 完整性
   - 運行 `pnpm build:public` 驗證構建成功
   - 本地預覽驗證修復效果
4. **快速測試**: 至少測試主要語言版本（zh-TW, zh-CN, en-US）
5. **部署**: `pnpm deploy:public`
6. **事後檢查**: 部署後運行 `pnpm i18n:audit` 確保沒有引入新問題
7. **記錄**: 記錄 hotfix 原因和修復內容

#### 注意事項
- Hotfix 應只包含必要的修復，不應包含新功能
- 修復後應計劃進行完整的回歸測試

## 禁止事項

1. ❌ 修改 FROZEN/LOCKED 組件的結構和文本
2. ❌ 在頁面中混用不同語言的文本
3. ❌ 使用 fallback 文本（如 `|| 'English'`）
4. ❌ 硬編碼品牌詞（必須使用 `brandify()`）
5. ❌ 硬編碼外部鏈接（必須使用配置常量）
6. ❌ 使用現代 JavaScript 語法（`?.`, `??` 在客戶端腳本中）
7. ❌ 修改 i18n 消息文件結構（除非明確需要）
8. ❌ 在暗色模式下使用淺色背景而不覆蓋

## 開發工作流

### 新功能開發
1. 創建新頁面時，必須支持所有語言（使用 `[lang]` 動態路由）
2. 所有文本必須從 i18n 消息文件加載
3. 使用 `brandify()` 處理包含品牌詞的文本
4. 檢查 RTL 支持（如果頁面包含布局）
5. 運行構建前檢查: `pnpm i18n:audit && pnpm i18n:check && pnpm i18n:normalize`
6. 確保 TypeScript 類型檢查通過: `pnpm check`
7. 確保 ESLint 檢查通過: `pnpm lint`

## 維護階段工作流

### 日常維護
1. **更新翻譯前先備份**: `pnpm backup`
2. **導出需要翻譯的內容**: `pnpm i18n:export` 或 `pnpm i18n:export-3lang`
3. **翻譯完成後導入**: `pnpm i18n:import ./i18n-export.csv` 或 `pnpm i18n:import-3lang`
4. **同步和修復**: `pnpm i18n:sync`
5. **構建測試**: `pnpm build:public`
6. **檢查報告**: `pnpm i18n:report`

### 修復問題
- **構建失敗**: `pnpm fix:build`
- **i18n 錯誤**: `pnpm i18n:heal:all && pnpm i18n:normalize`
- **類型錯誤**: `pnpm check`
- **代碼格式問題**: `pnpm format`
- **樣式問題**: 檢查 `src/styles/theme.css` 的暗色模式覆蓋

### 翻譯同步流程
1. **從源語言同步**: `pnpm i18n:sync-zhCN-from-zhTW`（繁體到簡體）
2. **修復缺失鍵值**: `pnpm i18n:heal:all`
3. **規範化格式**: `pnpm i18n:normalize`
4. **驗證完整性**: `pnpm i18n:check`

### 添加新語言（如果未來需要）
1. 在 `src/i18n/locales.config.ts` 添加語言定義
2. 設置 `rtl: true`（如果是 RTL 語言，如阿拉伯語、希伯來語）
3. 創建 `src/i18n/messages/{locale}/` 目錄結構
4. 複製 zh-TW 作為模板並翻譯所有模塊
5. 運行 `pnpm i18n:check` 驗證
6. 運行 `pnpm build:public` 測試構建
7. 手動測試新語言的所有關鍵頁面
8. 如果添加 RTL 語言，特別測試布局和排版

### 代碼提交前檢查清單
- [ ] 運行 `pnpm check` - TypeScript 類型檢查通過
- [ ] 運行 `pnpm lint` - ESLint 檢查通過
- [ ] 運行 `pnpm format` - 代碼已格式化
- [ ] 如果修改了 i18n 相關代碼: `pnpm i18n:audit && pnpm i18n:check`
- [ ] 如果修改了 i18n 消息文件: 運行 `pnpm i18n:normalize`
- [ ] 構建測試: `pnpm build:public` 成功
- [ ] 移除所有 `console.log()` 調試語句
- [ ] 確保沒有硬編碼文本（應使用 i18n）
- [ ] 確保沒有硬編碼 URL（應使用 `src/config/links.ts`）
- [ ] 檢查 FROZEN/LOCKED 組件是否被不當修改

### 部署前檢查
1. `pnpm backup` - 創建備份
2. `pnpm i18n:audit && pnpm i18n:check && pnpm i18n:normalize` - i18n 檢查
3. `pnpm check` - TypeScript 類型檢查
4. `pnpm lint` - ESLint 檢查
5. `pnpm build:public` - 構建測試
6. `pnpm test:all` - 完整測試（如果時間允許）
7. `pnpm deploy:public` - 部署

## 參考文件

- i18n 配置: `src/i18n/locales.config.ts`
- 品牌詞處理: `src/lib/brandify.ts`
- 樣式變量: `src/styles/theme.css`
- 鏈接配置: `src/config/links.ts`
- 應用配置: `src/config/app.ts`
- 性能優化: `doc/performance-optimization.md`

