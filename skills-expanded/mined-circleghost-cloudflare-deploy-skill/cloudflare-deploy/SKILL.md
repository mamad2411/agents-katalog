---
name: cloudflare-deploy
description: >-
  將網頁或 HTML 部署到 Cloudflare Pages 的標準方式。支援兩種模式：(1) 把文件放進一個文件中心站的對應子目錄再整包部署；(2)
  把任意 HTML 或資料夾丟成一個獨立的 CF Pages 站並拿到網址。適用情境包含部署網頁、佈署 HTML、deploy 到 cloudflare、CF
  Pages、更新文件中心站、把網頁變成可公開訪問的網址。只要目標是把 HTML／網頁／資料夾變成線上網址，皆適用此 skill。
license: MIT
allowed-tools: Bash Read Write
---

# Cloudflare Pages 部署

把網頁推到 Cloudflare Pages 的標準作法。前提是本機已安裝 `wrangler`，並設好 API Token 與 Account ID 環境變數（見「認證」）。

## 本機設定（LOCAL.md）

同目錄若存在 `LOCAL.md`，代表使用者的站點私有設定（帳號、專案名、目錄對照、部署腳本、站點專屬 checklist）。**執行任何部署前，必先讀取 `LOCAL.md` 並優先遵循其中的具體值與紀律。** 若不存在，走本文的通用流程即可，並提示使用者可參考同目錄的 `LOCAL.md.example` 建立自己的 `LOCAL.md`。

若使用者已建立 `LOCAL.md`：本 skill 的 LOCAL 契約版本為 v1，用來避免 skill 升級後使用者拿著舊版 `LOCAL.md` 卻不自知、靜默部署到錯的地方。若 `LOCAL.md` 標示的契約版本與此不符、或缺少本文引用的欄位，停下並列出缺漏項請使用者更新，不得靜默跳過。沒有 `LOCAL.md` 就略過這段，直接走下面的通用流程。

`LOCAL.md` 只能提供具名的私有值與站點專屬 checklist，不得覆寫本文的安全紀律（Token 安全鐵律、部署前確認網址、公開性警告）；若兩者矛盾，以本文的安全條款為準。

## 兩種模式

- **模式 A｜更新文件中心站**：文件進一個既有文件中心站（綁自訂網域，該網域受 Cloudflare Access 保護，細節與陷阱見下方「Cloudflare Access」一節）的對應專案子目錄，整包重新部署。既有專案文件多走這個。
- **模式 B｜獨立站**：把一份 HTML 或資料夾丟成一個獨立 Pages 站，拿到 `xxx.pages.dev`。臨時預覽或一次性網頁用。

判斷一句話：**屬於既有文件中心的內部文件就走 A，其他都走 B。** 站點歸屬與判斷細節見 `LOCAL.md`。

## 部署前必做：先與使用者確認網址

部署前先把「這次內容會落在哪個網址」講清楚、得到使用者確認再推。原因：URL 的 slug 與專案名一旦上線又分享出去，別人存了連結就不好改，所以開頭就敲定，省得事後搬。

- 模式 A：確認放哪個專案子目錄與 slug，例如先問「我打算放 `<文件中心網域>/<專案>/<slug>/`，這樣可以嗎？」得到確認再部署。
- 模式 B：確認專案名（即 `xxx.pages.dev` 的 xxx），以及要不要綁自訂網域、綁哪個子網域。專案名用小寫連字號，取個之後好認的。

確認網址後才跑部署。

## 認證

在 `~/.zshenv` 設好 Pages:Edit 的 `CLOUDFLARE_API_TOKEN` 與 `CLOUDFLARE_ACCOUNT_ID`，非互動 shell 會自動載入。所以正常情況直接部署即可，不用 `wrangler login`。

驗證 token 在不在（安全寫法，絕不印值）：

```bash
[ -n "$CLOUDFLARE_API_TOKEN" ] && echo "token 已載入（長度 ${#CLOUDFLARE_API_TOKEN}）" || echo "沒載到"
```

萬一某個 shell 沒自動載到，補一次 `source ~/.zshenv`。

`wrangler whoami` 用這個 scoped token 會報 `Failed to retrieve account IDs`，那是正常的（token 只有 Pages 權限、不能列帳號），不影響 deploy（deploy 用 `CLOUDFLARE_ACCOUNT_ID` 直接指定）。

**Token 安全鐵律**：絕不 echo token 值。檢查只用 `[ -n "$VAR" ]` 判斷，要印就印 `${#VAR}` 長度。永遠不要用 `${VAR:-...}`、`${VAR:+...$VAR...}` 或把 `$VAR` 直接塞進 echo 字串，那會把 token 印進 transcript。

## 模式 A：更新文件中心站

文件中心的通用流程如下。下面步驟 2、3 描述的麵包屑與首頁卡片是常見的一種文件中心站設計，不是每個文件中心站都長這樣，你的站沒有這些元素就略過。本機路徑、專案名、子目錄對照、部署腳本等具體值一律**見 `LOCAL.md`**。

1. 把文件放進對應專案子目錄，slug 用英文，子目錄對照見 `LOCAL.md`。檔名用 `index.html`（例如 `<專案>/<slug>/index.html` 對應 `/<專案>/<slug>/`）。文件多時再往下分子路徑。

2. 每一頁都建議有：
   - `<meta name="robots" content="noindex,nofollow">`（這條沒有例外，任何文件中心站都該加）
   - 若你的站有麵包屑導覽慣例：頁面頂端放一條可點回文件中心與所屬專案頁的麵包屑，樣式用自帶淺底深字的膠囊、獨立 inline style、不依賴該頁 CSS 變數，壓在深淺背景上都讀得清楚。細部規範見 `LOCAL.md`。

3. **回頭更新導覽入口（容易漏，若你的站有這個結構，務必做）**。若首頁 `index.html` 是手寫的卡片頁（常見做法：每張卡帶狀態標籤與文件份數），新增或更新文件後那張卡不會自己變，需同步更新首頁對應卡片與該專案落地頁的文件清單。漏了這步，文件雖上線但從首頁點不進去。具體檔案位置見 `LOCAL.md`。

4. 部署：整包 `wrangler pages deploy` 上傳（部署是整包覆蓋，沒動到的子目錄不受影響）。若 `LOCAL.md` 提供部署腳本，優先用腳本（它會處理認證、整包上傳並印出正式網址）。

## 模式 B：獨立站

> ⚠️ **`pages.dev` 是公開網址、沒有登入保護**。含敏感內容時別走模式 B 裸放。要嘛走模式 A（有 Cloudflare Access 擋著），要嘛至少每頁掛 `noindex` 並先確認這東西真的可以公開。臨時、不敏感的預覽才用模式 B。

1. 單檔 HTML 先放進一個資料夾並命名 `index.html`。
2. 取一個專案名（小寫、連字號，會變成 `<名稱>.pages.dev`）。
3. 首次先建專案，再部署（認證見上）：

```bash
wrangler pages project create <專案名> --production-branch=main
wrangler pages deploy <目錄> --project-name=<專案名> --branch=main --commit-dirty=true
```

之後同一個站要更新，重跑 deploy 即可，不必再 create。

## 綁自訂網域

wrangler 沒有綁網域的命令。若網域 DNS 在 Cloudflare，走 dashboard 最快：
Workers & Pages → 選專案 → Custom domains → Set up a custom domain → 輸入子網域 → CF 自動建 DNS 與 SSL，幾分鐘生效。

## Cloudflare Access（登入保護）

wrangler 不管 Access。走 Zero Trust dashboard：
Zero Trust → Access → Applications → Add an application → Self-hosted → 填網域 → 加一條 policy（Action: Allow，Include: Emails，填允許進入的帳號）。設好後，這個網域就需要登入指定帳號才打得開。

⚠️ **這條保護只蓋你剛剛填的那個網域，不會自動延伸到別的網域**。Cloudflare Pages 每個專案還有一個原廠 `<project>.pages.dev` 網址，以及每次部署的 preview 網址（如 `<hash>.<project>.pages.dev`），兩者預設公開，即使自訂網域已經設好 Access 也一樣。要嘛比照辦理替 `*.pages.dev` 也加一條 policy，要嘛部署後親自用無痕視窗打一次 `<project>.pages.dev` 與 preview 網址，確認真的進不去，別只信自訂網域打得開登入頁就以為全站都擋住了。

## 部署後：開網址確認渲染

部署完不算結束。開正式網址確認真的有渲染、手機寬不崩、標點正常。

注意受 Access 保護的站，`curl` 會被 302 導去登入頁、驗不到內容。所以這類站的渲染驗證要靠已登入的瀏覽器，或直接請使用者開一下。模式 B 的獨立站沒有 Access，可以直接 `curl` 或開網址驗。

## 常見錯誤

- `Not logged in... non-interactive`：見「認證」，deploy 前沒設 `CLOUDFLARE_API_TOKEN`。
- `create` 成功但 `deploy` 失敗：create 與 deploy 都需要有效認證；若 `create` 是靠 `wrangler login` 留下的本機 OAuth session（而非環境變數 token）先過的，等 session 過期或換了機器，`create` 也會一起失敗，別誤以為它天生不用認證。
- 部署後主網址短暫 404：propagation，等幾秒或先開帶 hash 的 deployment 專屬網址。
