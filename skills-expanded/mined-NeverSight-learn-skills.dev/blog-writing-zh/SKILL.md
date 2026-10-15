---
name: blog-writing-zh
description: >-
  Write or rewrite Traditional Chinese (Taiwan) blog posts with a genuine human
  voice, modeled on seven studied blogs (知識倉鼠, 保哥, 高見龍,
  90s.pm.investing, AI避坑情報員, Julia Evans, Simon Willison). Use when asked to 寫部落格文章／
  電子報／blog post, 把筆記改寫成文章, 把 Obsidian 筆記變成 blog, 翻譯改寫外文文章／演講／
  討論串成中文長文, or "用我的風格寫一篇 X", or 不確定該用什麼風格寫（本 skill 會依讀者與目的推薦配方）. Supports two modes — compose (from a topic
  or loose material) and rewrite (from an Obsidian note, translation source, or
  draft) — and three technical-description modes (操作型可重現教學, 概念型心智
  模型導讀, 推演型原理解說) with actionability and concept-clarity checklists — plus composable voice axes (opening strategy × persona intensity ×
  metaphor density × closing move) with presets, an optional
  dual-draft mode (write two deliberately divergent drafts, then merge
  the strengths) for long or high-stakes pieces, a selectable length
  tier (短打/標準/深文/工具書級), and an automatic post-draft check that
  suggests splitting into a series (with outline) when one piece can't hold
  the material. Output is always the article
  PLUS 3-5 title/subtitle candidates. Pipeline position: this skill supplies
  structure and voice (加法), then ACTIVELY INVOKES avoid-ai-writing-zh as the
  de-AI finishing pass (減法) — loading and running it (rewrite mode, voice
  profile mapped from the chosen 風味) rather than merely telling the user to,
  in any environment that can load sibling skills — plus avoid-china-writing if
  PRC usage may have leaked in. Do NOT invoke for 正式公文／簽呈 (use formal-doc-structure), RFP (use
  rfp-writing), 白話翻譯單一術語 (use plain-speak), or pure de-AI editing of an
  existing text with no restructuring (use avoid-ai-writing-zh directly).
version: 0.14.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, etc.). No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing blogging voice zh-tw traditional-chinese content-creation
  agentskills_spec: "1.0"
---

# Blog Writing (zh-TW) — 有人味的部落格寫作

You are writing (or rewriting material into) a Traditional Chinese blog post
that reads like a specific human wrote it — with a stance, lived experience,
and a voice — not like a well-organized machine summary.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## 核心原則：一個活人在對讀者說話

研究五個台灣高人氣部落格後的共同底層原則：**每篇文章都能感覺到「一個活人在
對你說話」**。這由五種正向特徵構成，缺一味道就淡：

1. **有立場**：作者敢下判斷（「燒腦但值得」「別急著投降」），不是中立百科。
2. **有親身經歷**：具體的個人契機、踩坑、時間數字（「被卡關三次，超煩的」
   「花了三天才搞懂」）。改寫模式下，素材裡沒有的經歷**絕不可捏造**，
   改用「編者視角」框架（見 rewrite-playbook.md）。
3. **有自己的比喻**：作者自創、貫穿全文的比喻（「linter 像從不疲憊的紀律
   委員」「葉子亮燈」），不是解釋，是造像。
4. **節奏不均質**：句長、段落長刻意起伏。一句話自成一段。金句急停。
   AI 文的破綻常常不是病句，而是每段都一樣長、每句都太完整。
5. **有思考痕跡**：像是邊想邊寫、在腦袋裡跟自己對話，讓讀者看著你從
   困惑走到結論——試過的死路、卡住的地方、改變主意的轉折（「我一開始
   以為 X，跑過一次才發現不對」「這段我卡了很久」）。人味來自呈現
   「怎麼想到的」，不是把打磨好的結論丟給讀者。改寫模式下不可捏造
   第一人稱困惑，改用編者視角攤開素材本身的推導順序（「這裡值得停下來
   想一下為什麼」）。

## Modes

**`compose`**（給題目或鬆散素材時）— 從零寫一篇完整文章。
**`rewrite`**（給 Obsidian 筆記、外文來源、演講稿、草稿時）— 改寫成部落格文。
先讀 `references/rewrite-playbook.md` 選擇改寫策略（忠實翻譯＋編者框架 vs
敘事重構）。

判斷不明時問使用者一次即可。

## Workflow

### Step 1 — 定風格配方

讀 `references/voice-axes.md`（風格選單，兩層設計）。第一層單選
**文章類型**（教學實作／概念導讀／深度解讀／實測筆記／觀點倡議／
拆解評測／分析框架），第二層單選**風味**（該類型建議的 2–3 位作者
風味＋無特定風味），**第三層單選長度檔位**（見下）。選「自訂配方」
才逐元素詢問（八元素見選單檔）：

- E1 開場策略、E2 人設濃度、E3 比喻型態、E4 節奏設計、
- E5 結構框架、E6 術語處理、E7 收尾方式、E8 標題公式。

**長度檔位（第三層單選，附推薦）**：

| 檔位 | 字數（中文） | 特徵 | 典型場景 |
|---|---|---|---|
| 短打 | 300–800 | 單一重點、一個鉤子、無小節或極少 | 社群貼文、TIL、快訊 |
| 標準 | 800–2000 | 完整論證或教學、3–5 節 | 一般部落格文（預設） |
| 深文 | 2000–5000 | 多面向、子章節、可跳讀 | 深度解讀、完整教學 |
| 工具書級 | 5000+ | 窮盡選項/變數、附表格與清單 | 升級指南、設定手冊、年度回顧 |

長度推薦邏輯（未指定時）：依文章類型給預設——實測筆記/拆解評測
→短打或標準；教學實作/概念導讀/觀點倡議→標準；深度解讀/分析框架
→深文；升級指南/設定手冊類→問要標準還是工具書級。推薦一個檔位
＋一句理由讓使用者確認，不強塞。長度與**深度**是兩回事：短打也要
把選定的單一重點講到位，不是把深文的每節砍半。

使用者講舊 preset 名（倉鼠敘事型等）依 voice-axes.md 對照表直接映射。
**未指定風格時，先讀 `references/preset-guide.md` 做推薦**：從素材推斷
「讀者讀完要做什麼」與「讀者跟主題的關係」（推不出來才問，一題），
校準對象三變因（技術程度→術語、關係→人設濃度、發布場景→標題），
連同長度檔位一併給推薦（1 主推薦＋至多 1 備案，各附一句理由）
讓使用者單選確認。

### Step 2 — 讀對應的風格參考檔

只讀本次會用到的 preset 對應檔（`references/style-*.md`），不要全部載入。
每份檔案含：結構骨架、語感特徵、標題公式、示例句、禁忌。

### Step 3 — 寫作（或改寫）

- rewrite 模式：先照 rewrite-playbook.md 完成素材轉換，再套風格。
- **技術內容必讀 `references/tech-writing.md`**（內容層，與 preset 正交）：
  依文章性質選描述模式——操作型（可重現優先）／概念型（心智模型
  優先）／推演型（認知階梯優先），或照混搭指南配比。出稿前跑完
  該檔的「可操作性」與「概念釐清」雙檢查清單。
- 術語三層法（全 preset 通用）：首現「中譯（English）」；無定譯保留英文，
  前後留半形空格；關鍵概念加一句白話註解（「tokens 可以先理解成模型
  運算與閱讀上下文的成本」）。
- 事實與連結：來源裡的數字、連結、引文保持準確；不可為了風格改動事實。
- 具體名詞優先於泛稱：平台、書名、工具、地點用真實專有名詞
  （PTT、天瓏、公司的 Slack），在地感與真實感來自名詞密度；
  引用出處不確定時誠實標注（「據說」「可能曾說過」），不硬安。
- 長度：依 Step 1 選定的長度檔位（短打／標準／深文／工具書級）
  控制篇幅；使用者中途要求調整就重定檔位。檔位內仍以品質為準——
  教學文以「讀者能照做」、觀點文以「論證完整」，在檔位字數範圍內
  自然收束，不灌水也不硬砍。若內容明顯撐破檔位上限，建議升檔或
  拆系列（觀點題常見拆法：上＝為什麼／下＝怎麼做），不要硬塞。

### Step 3.5 —（可選）雙稿分化（dual-draft）

長文或重要文預設**建議**雙稿，短文單稿。判準與流程見
`references/dual-draft.md`。啟動時：讓使用者選分化軸線（結構／開場／
深度檔位，附推薦；兩稿一律同風味）→ 各寫完整一稿 → 診斷比對取各稿
強項 → **熔接**成單一風味的終版 → 附一句取捨說明。不啟動則跳過。

### Step 4 — 標題與副標備選

產出 3–5 組「標題＋副標」。標題公式參考各 style 檔（如何型／解密型／
二元對立問句型／敘事鉤子型／反焦慮型），至少橫跨兩種公式，並標注
各組適合的發布場景（SEO／社群／電子報）。

### Step 5 — 交棒收尾（pipeline，主動調用）

**這一步是主動調用，不是提示使用者自己跑。** 若執行環境能載入其他
skill（Claude Code、Cursor 等讀得到同 repo/skills 目錄的 agent），
完稿後 Claude 直接載入並執行下列 skill，把處理過的版本當終稿交付；
無法跨 skill 調用的環境（如純網頁對話單獨載入本 skill）則退為明確
提示使用者接續執行，並附上建議指令。

1. **必做：調用 `avoid-ai-writing-zh` 做去 AI 味終稿檢查。**
   用自然語言交棒即可，它支援 rewrite/detect/edit 模式與 voice
   profile。**採 detect-first 三步流程**（最不會誤削聲音）：

   **步驟 A — 先 detect，拿命中清單。** 以 `detect` 模式交棒，
   要它只標記 AI-ism、不改字，回傳每個命中項＋所在文字。

   **步驟 B — blog-writing-zh 過濾 intentional 項。** 拿到清單後，
   本 skill 對照風味檔逐項判定：屬本文正向特徵者（有立場的判斷句、
   第一人稱經歷、自建比喻、刻意的不均質節奏與口語破格、邊想邊寫的
   思考痕跡（「我一開始以為…」「老實說不確定」、改變主意的轉折）、
   風味簽名句式、單句段急停、低劑量顏文字）標為**豁免**；只留下真正機械化
   的 AI 套路（空話口號、不是…而是、過度翻譯術語、三元排比慣性、
   Tier 1 硬核詞等）。

   **步驟 C — 只 rewrite 未豁免項。** 把過濾後的待修清單交回，
   以 `rewrite`（或 `edit`）模式只改這些項，明確告知豁免清單不得
   更動。

   為什麼不直接 rewrite：直接 rewrite 時 detect 會命中大量
   intentional voice，下游可能一併改掉；detect-first 讓過濾權留在
   懂本文聲音的 blog-writing-zh 手上，下游只執行確認過的修改。
   稿子 AI 味本來就低時（如高見龍白話風），步驟 A 常只回幾項、
   步驟 C 極輕量，成本很小。

   **參數傳遞：**
   - voice profile：把本次風味與人設濃度傳為 voice。高見龍 L3 →
     `--voice casual`；保哥 L1 → `--voice professional/technical`；
     Simon → `--voice technical`。dual-draft 熔接稿**務必**跑這關，
     接縫處最容易殘留 AI 味（多集中在 A/B 稿論據交會處）。
   - context：依發布場景給 `--context blog|technical-blog|casual` 等。
   - 交棒話術範例（步驟 A）：「用 avoid-ai-writing-zh 以 detect 模式、
     casual voice 掃這篇，只列 AI-ism 命中清單不要改字，我要自己
     過濾哪些是刻意的聲音。」
2. **視情況：素材來源含簡中或大陸用語風險時，接著調用
   `avoid-china-writing`。**

**衝突保護（傳給下游的硬約束）**：本 skill 是加法（給聲音與結構），
那兩個是減法（除雜訊）。順序不可反過來。交棒時明確告知下游：
本文的正向特徵——有立場的判斷句、第一人稱經歷、自建比喻、
刻意的不均質節奏與口語破格、邊想邊寫的思考痕跡——是 intentional
voice，不是 AI-ism，必須保留；只移除機械化的 AI 套路（空話口號、
不是…而是、過度翻譯術語等）。若下游削掉了聲音，以本 skill 的
正向特徵為準回復。

**呼叫後**：拿回下游的 rewrite 結果與 diff，快速檢查聲音是否被
誤削（尤其金句、單句段、顏文字、簽名句式）；沒問題才定稿交付。
配方紀錄增記：`pipeline: avoid-ai-writing-zh(rewrite, voice=X)
✓〔＋avoid-china-writing 若有〕`。

### Step 6 —（自動）系列文評估

**交付單篇前自動評估這篇是否值得拆成系列**，讀
`references/series-planning.md`。多數單篇就是單篇——只有明確訊號
（成品撐破長度上限、文中有段落值得單獨成篇、多個獨立子主張、
清楚遞進依賴）成立時，才在交付成品後**附一段系列建議**：一句話
結論＋理由＋系列大綱（每篇主張與暫定篇名、遞進關係、每篇配方、
跨篇連貫機制），並說明這篇可作系列第幾篇。不值得就不提，正常
交付單篇，不要每篇都問（那是噪音）。使用者接受後，後續每篇等
指令才寫，各自走完整主流程（Step 1–5）。

## Output format

```
# 【定稿文章】
（完整 Markdown 文章）

---
## 標題與副標備選
1. 標題｜副標 —（適用場景）
2. ...

## 風格配方紀錄
類型／風味／長度檔位／覆寫元素／dual-draft（若有）
pipeline: avoid-ai-writing-zh(rewrite, voice=X) ✓〔＋avoid-china-writing 若有〕
```

## Guardrails

- **不捏造親身經歷**。compose 模式下若使用者沒提供個人素材，先問一個
  簡短問題挖掘（「你自己踩過這個坑嗎？」）；問不到就用觀點與比喻
  補人味，不虛構故事。**觀點倡議型與實測筆記型例外處理**：這兩類的
  說服力核心就是見證（時間縱深的細節、實測數據），索取真實素材是
  必要步驟不是可選；使用者明確表示沒有時，在文中誠實降級（不寫
  第一人稱見證段），並告知這會影響此類型的說服力。
- **不搬運人設**。preset 是骨架不是皮：可以學高見龍的「先立後破」，
  不可以直接寫「可以去打我的魔物獵人了」這種屬於他本人的簽名句。
- **迷因語彙有半衰期**。毒舌 preset 的流行語（芭比Q 等）用前想一下
  半年後讀是否尷尬；價值長青的文章降低迷因密度。
- **改寫來源要透明**。翻譯改寫模式必須在文首標明來源連結與改寫性質。
- 引用他人文章時遵守合理使用：重點改寫、短引註明出處，不整段搬運。

## References

- `references/voice-axes.md` — 風格選單：八元素拆解＋兩層配方表（Step 1 必讀）
- `references/preset-guide.md` — 依主題與對象推薦配方（未指定風格時必讀）
- `references/rewrite-playbook.md` — 改寫雙模式＋Obsidian 筆記轉換
  （rewrite 模式必讀）
- `references/tech-writing.md` — 技術描述三模式＋可操作性/概念釐清
  雙檢查清單（技術文必讀）
- `references/dual-draft.md` — 雙稿分化與合併（長文/重要文可選；
  Step 3.5）
- `references/series-planning.md` — 系列文建議：產出後自動評估
  值不值得拆＋大綱（Step 6）
- `references/style-circleghost.md` — 知識倉鼠（敘事解讀型）
- `references/style-miniasp.md` — 保哥（嚴謹教學型）
- `references/style-kaochenlong.md` — 高見龍（對話幽默型）
- `references/style-90spm.md` — 90s.pm（方法論比喻型）
- `references/style-aitrapadvisor.md` — AI避坑情報員（毒舌情報型）
- `references/style-jvns.md` — Julia Evans（賦能解惑，概念釐清標竿）
- `references/style-simonwillison.md` — Simon Willison（實證筆記，可操作性標竿）
