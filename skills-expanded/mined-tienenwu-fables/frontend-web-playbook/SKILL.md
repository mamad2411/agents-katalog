---
name: frontend-web-playbook
description: Use when writing, refactoring, or debugging React/Next.js frontend code (App Router, Server/Client Components, hooks, Tailwind/CSS Modules) — before adding a component, choosing where state lives, wiring data fetching, or preparing a production deploy; or when facing hydration mismatch, NEXT_PUBLIC_ env leaks, excessive re-render, bundle size bloat, CLS, SEO/metadata gaps, or XSS via dangerouslySetInnerHTML.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/frontend-web/SKILL.md) · 繁體中文（正本 / canonical）

# React / Next.js 前端開發判準手冊

## 核心原則

1. **Dev server 的綠燈不算數**：hydration、環境變數注入、bundle 大小、SEO metadata、minify 只在 `next build && next start` 才如實呈現——上線路徑的改動必須用 production build 驗證。
2. **遠端資料與 UI 狀態是兩種東西**：server state（來自 API/DB，會過期、要快取、要重取）交給 React Query/SWR；client state（純畫面開關、輸入框）才用 useState/zustand。混用是多數「資料不同步」bug 的根。
3. **狀態放在用得到它的最低層**：預設 local，痛了才 lift，最後才 global。過早上 global store 是熵，不是架構。
4. **re-render 是症狀不是病**：先用 Profiler 量出哪個元件為何重繪，再決定要不要 memo；憑感覺撒 useMemo/useCallback 只是加噪音。
5. **凡進 client bundle 的東西都會被使用者看到**：`NEXT_PUBLIC_` 前綴的變數、寫死在元件裡的字串、import 進 Client Component 的整包 library——先假設它公開，再證明它該公開。

## 開工分流

| 情境 | 路徑 | 先讀 |
|------|------|------|
| 新增畫面/功能 | 先定資料從哪取、狀態誰擁有、哪些要 "use client"，再寫 UI | references/architecture-state.md |
| 寫/改 component、抽元件、styling | 先問語意邊界與 props 契約，再動手 | references/components-styling.md |
| 畫面卡頓、re-render 過多、bundle 過大 | 不要先撒 memo，先量測 | references/rendering-performance.md |
| 取遠端資料、快取、loading/error 態 | 分清 server state vs client state | references/architecture-state.md §1 |
| 出 production / 部署 / 排查「dev 正常上線爆」 | 逐條跑必查清單 | references/release-checklist.md |
| hydration mismatch、環境變數、SEO | 先假設 build-time 差異，別亂改 | references/release-checklist.md |

## 紅線（絕對禁止）

- **禁止只用 dev server 驗證後宣告上線相關改動完成**——hydration、`NEXT_PUBLIC_` 注入、bundle、minify、metadata 在 dev 全部不如實。
- **禁止把 secret（API key、DB 連線字串、私鑰）加 `NEXT_PUBLIC_` 前綴或寫進 Client Component**——會被打包進 JS bundle，任何使用者可讀，等同公開洩密。
- **禁止把 `dangerouslySetInnerHTML` 接使用者可控字串而不 sanitize**——直接 XSS；使用者輸入的 `<script>` 會在別人瀏覽器執行。
- **禁止用陣列 index 當會增刪/重排 list 的 `key`**——插入或排序時 React 錯配 DOM，輸入框內容跳到別列、勾選狀態錯位。
- **禁止在 render 期間直接讀 `window`/`localStorage`/`Date.now()`/`Math.random()` 決定輸出**——server 端無此值或值不同，hydration mismatch，整棵樹在 client 被丟棄重繪。
- **禁止把測試/型別檢查改鬆讓 CI 變綠**——連紅兩次是方向錯誤訊號，退回上一決策點，不是註解掉斷言。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| 撒了一堆 useMemo/useCallback 才不卡 | 上游傳了不穩定的 props，或 state 放太高 | 用 Profiler 找真正重繪源，重看狀態層級 |
| 每個元件都得 `useEffect` 同步一份資料副本 | 把 server state 塞進 useState 了 | 改用 React Query/SWR 當單一真相 |
| `suppressHydrationWarning` 越加越多 | server/client 輸出本質不一致 | 找出分歧值（Date/random/瀏覽器 API），移到 useEffect |
| props 一路往下鑽 5 層（prop drilling） | 狀態該提升或該用 context/store | 重看狀態擁有者，不是繼續鑽 |
| 一改就 `'use client'` 往上加一層才不報錯 | client 邊界畫錯，把 Server Component 內容拖下水 | 重看邊界：只有互動葉節點需要 client |
| 同一個 hydration error 換三種寫法還在 | 沒定位到分歧值就在瞎改 | 讀 console 指名的元件，比對 server vs client HTML |

## references 索引

- `references/architecture-state.md` — server vs client state 分界、狀態放哪層、Server/Client Component 決策、資料獲取位置。動架構或新功能前讀。
- `references/components-styling.md` — 何時抽 component、props 契約、受控 vs 非受控、CSS 策略、a11y 紅線。寫 UI 前讀。
- `references/rendering-performance.md` — 量測先行、memo 判準、list key、code splitting、圖片/字型/CLS。卡頓或 bundle 過大時讀。
- `references/release-checklist.md` — 環境變數洩密、hydration 排查、SEO、production build 實測、XSS、error boundary、bundle 門檻。出版前逐條打勾。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
