---
name: lhtl-tw-narrative-voice
description: >-
  撰寫與審查《Learn How to Love》繁體中文敘事文案：親切、溫柔、多情感、台灣用語。
  語調基準以 Demo Day 1（prologue_rain～prologue_dawn）為金標；新章節與修稿須對齊其句式、用詞與留白節奏。
  撰寫或審查 Ch1 對白時須遵守 narrative-pacing-revision.md：人對狗對話、text/sub 分層、禁主題總結句。
  當使用者要寫或改劇情、對白、選項、UI 文案、相簿描述、小遊戲提示，或要求繁體／台灣口吻／語氣調整、
  **婉轉不直白**、**Ren'Py 字幕缺字／怪字／間隔號**時，務必使用此 skill。
  取名／代詞／角色設定審查交 character-bible；分支 flags 交 branch-engine。
---

# LHTL 繁體敘事語氣（台灣）

**Ch1 更深記憶點（與四 skill 共用）：** 見 [`deeper-memory-interaction.md`](../deeper-memory-interaction.md)——互動回聲、解鎖儀式、日終回看。

## 核心規範（必守）

**一律繁體中文；口吻親切、溫柔、有情感；用詞貼近台灣日常。**

**語調金標：** `Demo/js/scenes.js` 的 **Day 1**（`prologue_rain` → `prologue_dawn`）。撰寫或審查其他天數時，先對照 Day 1 的層次與節奏，再依篇章基調微調（Ch2 更靜、Ch3 更克制）。

適用所有玩家可見文字：Ren'Py `week1.rpy`／`screens.rpy`／`album.rpy`；舊 HTML `scenes.js`、`choice-reactions.js`、`story-agent.js`、`minigame-reactions.js`、`systems.js`（行為／相簿）、`game.js`（小遊戲 UI）、`index.html` 說明。

與 [`story-narrative`](../story-narrative/SKILL.md) 搭配：故事架構看 `guide_line.md`；**字詞與語氣以本 skill 為準**。角色設定鎖定見 [`character-bible`](../character-bible/SKILL.md)。

---

## Ren'Py 字型安全標點（SourceHanSansLite）

> 字型檔：`Ch1_Trust/Renpy_game/game/SourceHanSansLite.ttf`（或缺字會顯示成 **X／方框**）  
> 審計：`python Ch1_Trust/Renpy_game/tools/audit-font-glyphs.py`  
> 測試清單：[`game-tester/reference.md` §字型缺字](../game-tester/reference.md#字型缺字會顯示成-x方框)

| 勿用（缺字） | 改用 |
|--------------|------|
| U+00B7 間隔中點（選單「第一週·信任」曾變 X） | `｜` 或 `・` |
| U+25B8 小三角 | `▶` |
| U+2726 四角星 | `＊` 或刪除 |

**撰寫／潤稿時另注意：**

- 勿寫 `牠 `／` 牠` 異常空格（像亂碼）
- 對白省略統一用 `……`，少用 ASCII `...`
- 台灣用字：櫃檯、裡、麵、軟體、資訊（禁柜台／视频／质量等）

---

## Day 1 語調基準（必讀）

Day 1 寫的是「第一次養、什麼都不會、但願意留下來」——不說教、不英雄化，用**具體動作**與**感官**帶情緒。

### 四層文案怎麼寫

| 層次 | 欄位 | Day 1 怎麼聽起來 | 句數／節奏 |
|------|------|------------------|------------|
| **主敘事** | `text` | 鏡頭外：雨、霧、滴水、動作一連串；像在看現場 | 1–3 句一段；`\n\n` 換段 |
| **心裡話** | `sub` | 更慢、更內斂；「還不知道」「心裡有點慌」 | 比 `text` 短；少形容、多感受 |
| **選項** | `choices[].text` | 玩家**正在做**的事；可帶猶豫或疲憊 | 一句話；第一人稱動作 |
| **氣味** | `smell` / `smellAdd` | 名詞並列、頓號；不寫句子 | 3–5 個意象即可 |

### UI 分層（玩家可見）

| 欄位 | 畫面標示 | 字型／色 |
|------|----------|----------|
| `text` | **現場** | Noto Sans · 米白 `#fff8f2` |
| `sub` | **內心** | Cormorant 襯線斜體 · 暖金 `#e8c992` + 左金線 |

**sub 不可**重複 text 的情緒；**不可**替故事下結論（改寫成未說完的一句或對狗說不出的話）。

### 人對狗對話（Ch1 每天至少考量 1 句）

短、輕、笨拙；用「」；Types：道歉／試探／承諾／承認不會／命名／自我打斷。  
詳表：[`narrative-pacing-revision.md`](../narrative-pacing-revision.md) §二。

### Day 1 主敘事句式（可複用）

- **開場定調：** 時間／天氣 + 一個小動靜  
  > 傍晚，雨沒有要停的樣子。  
  > 巷口那個溼透的紙箱輕輕動了一下......

- **動作連鎖：** 你做了 A → 牠反應 B → 你心裡一緊  
  > 牠一驚，掙了一下，毛巾滑到地上。  
  > 你差點踩到，心跳快了一拍。

- **輕聲自言／道歉：** 用「」；重複、放輕  
  > 「對不起、對不起……」  
  > 你說得比平時更輕，  
  > 像在跟一個也嚇壞了的小生命道歉。

- **距離與陪伴：** 不強迫靠近  
  > 你開了小夜燈，在三步之外坐下——  
  > 不靠近，也不離開。

- **狗用身體說話：** 縮、靠、抖、沒有叫、呼吸淺淺  
  > 牠沒有叫，只是很膽怯、很慢地靠過來。  
  > 像把「怕」從喉嚨裡一點一點擠出來。

- **一個比喻就夠：** 溫暖、具體、不誇張  
  > 像一整團被雨打溼的暖色。

### Day 1 副文句式（可複用）

- 交代「還不會」而非「應該會」  
  > 沒有學習過，如何對待小生命。  
  > 你只能一邊試，一邊怕弄疼牠。

- 用「還不知道」「第一夜」錨定時間與陌生感  
  > 第一夜才剛開始。  
  > 你還不知道該先做哪一步，  
  > 心裡有點慌...

- 溫柔的價值判斷，不訓話  
  > 這不是任性，是牠還不習慣家的感覺  
  > 而這裡是可以安心睡的地方。

### Day 1 選項句式（可複用）

- **具體動作 + 工具／身體**  
  > 深吸一口氣，手忙腳亂找毛巾和吹風機  
  > 吹風機調到低檔，先讓牠聞聞風

- **承認狼狽，仍選擇留下**  
  > 一手按穩、一手吹，越弄越亂也沒停  
  > 困得發煩，還是壓低聲音陪在遠處

- **帶對白的選項：** 短、輕、不命令  
  > 走到三步外，輕聲說：「我在這，別害怕。」

### Day 1 用詞傾向（優先使用）

| 類別 | 詞彙 |
|------|------|
| 程度／節奏 | 輕輕、慢慢、一點一點、還好、有點、至少、仍、才 |
| 人的內心 | 慌、擔憂、困、疲憊、放鬆了一點、亂成一團、不敢 |
| 狗的身體 | 縮、蜷、靠過來、發抖、濕漉漉、膽怯、哀鳴、呼吸淺淺 |
| 環境 | 雨聲、霧、滴水、小夜燈、紙箱、三步之外 |
| 關係 | 陪伴、道歉、不強抱、不靠近也不離開、一起 |

完整對照表見 [reference.md §Day 1 詞彙與範例](reference.md#day-1-詞彙與範例場景)。

---

## 語氣三原則（對齊 Day 1）

1. **親切**：像對熟悉的人說話，不訓斥、不說教；他人（司機、店員）語氣也放輕。
2. **溫柔**：多用「輕輕、慢慢、一點點、還好、先」；用「……」與換行代替硬切斷。
3. **多情感**：寫心裡的慌、睏、捨不得、鬆了一口氣；用雨聲、空碗聲、呼吸襯情緒，不只交代事件。

## 敘述婉轉，不要直白（必守）

所有玩家可見文字（旁白、對白、選項、怎麼玩、章節摘要、結局／隱藏提示、選單）用**動作、距離、感官、願不願意**帶過；不要把機制、結局或情緒講死。

- 導引與選單**不劇透**睡姿、結局條件、trust／Dist／Tone／Guard
- 親密、生病、送走從側面寫；身體後果留到真正發生的那一場
- 禁結論句：「你必須」「正確的做法是」「選項會改變後來……」

| ❌ 直白 | ✅ 婉轉 |
|--------|--------|
| 選項會改變牠跟妳的距離，也會改變後來怎麼睡。 | 每一次選擇，都會輕輕改變牠願不願意靠近。 |
| 這隻狗很瘦、快撐不住了。 | 今天丟垃圾，牠幾乎沒站起來。 |
| 信任值上升。 | 牠把耳朵放下一點。 |
| 預設留下可收集結局 A。 | 從差點交給別人那一段再試一次。 |
| 一點點害怕的味道。 | 鼻尖埋進外套褶，像把整個人暫時藏進去。 |
| 信任從來不是一次到位。 | 今晚少抬頭看了一次。 |

## 繁體與台灣用語

- **一律繁體**；禁止簡體字與簡體詞（如：塑料、打扰、信息、怎么）。
- **優先台灣說法**；詳表見 [reference.md](reference.md)。
- 指涉狗一律用 **「牠」**；未取名前用 `dogLabel(s)`，勿硬塞名字。
- 避免大陸網路梗、公文腔、英文術語外露（`deadline` → 交件期限）。
- **禁止在玩家可見字幕使用 `Day1`～`Day7`、`Week1`～`Week4`**；改「第一天／第一週／第三天的拖鞋」等（game-tester P2）。

## 句式與節奏（對齊打字機 §6.5）

- **主 `text`：** 每段 1–3 句；`\n` 換行、`\n\n` 段落空行（遊戲內會多停頓）。
- **`sub`：** 比主文更慢、更像心裡話；可單句成段。
- **對白：** 「」；口語助詞（喔、啊）節制使用。
- **選項：** 第一人稱、具體動作；避免「選項 A：安撫」這類抽象標籤。
- **單段不宜過長：** 連續超過約 60 字宜拆段；Day 2 店舖線可設 `textMult` / `breathMs`。

## 動態日記文案（§6.5）

- **長度**：2–4 句；比正文更輕、更私密。
- **視角**：「那天」「第一夜」等時間錨；可回顧式「你」。
- **語氣：** 對齊 Day 1 相簿條目——短、像標題式散文。

**Day 1 相簿範例：**
> 雨天相遇 — 紙箱裡的第一次對視。  
> 第一夜 — 吹乾、哀鳴、和三步外的陪伴。

**Moment 範例（尿墊之夜，語氣同 Day 1 副文）：**
> 那個晚上，你沒有罵牠。  
> 只是蹲下來，把濕掉的墊子換掉，然後陪牠坐在旁邊。  
> 牠抬頭看你一眼，縮進了你的影子裡。

## 工作流程

## Workflow

1.  **Analyze Request**: Receive scene architecture, character bible, and pacing guides from `story-narrative`.
2.  **Author in DSL**:
    *   **Write all dialogue, choices, and internal monologue (`sub`) in a dedicated `.ink` script.** This script becomes the single source of truth for all narrative content.
    *   Ensure the writing style matches the established tone (warm, personal, Taiwanese vernacular) defined in this skill.
3.  **Integrate with Engine**:
    *   The game's narrative engine will load the compiled `.json` from the Ink script. The engine is responsible for displaying the `text` and `sub` content provided by the script.
4.  **Review in Context**:
    *   Use a tool like Inky to play through the script, checking for flow, rhythm, and emotional impact.
    *   Read the dialogue aloud to ensure it sounds natural.

## Pitfalls

*   **"AI Voice" / Hardcoded Text**: Never write dialogue directly into `.js` files. This creates maintenance nightmares. All text must originate from the `.ink` script.
*   **Show, Don't Tell**: Instead of stating an emotion ("the dog was happy"), describe the action that shows it ("Its tail thumped against the floor, a steady, joyful rhythm.").
*   **Ignoring `sub`**: The internal monologue is crucial for emotional depth. It should be treated as a first-class citizen in the script, not an afterthought.

### 修改／審查既有文案

1. 與 Day 1 並排讀：節奏是否突然變硬、變長、變像在寫報告？
2. 跑繁簡修正（若改 Demo）：`node Demo/tools/tw-locale-pass.js`
3. 搜尋殘留簡體：`塑料|打扰|信息|怎么|看见|跟着|写的|轻轻`
4. 搜尋英文週次殘留：`Day[1-7]|Week[1-4]`（應為「第N天／第N週」）
5. 檢查 `choice-reactions.js` 的 key 與 `scenes.js` 選項文字**完全一致**。

## 好／壞示例（對齊 Day 1）

| ❌ 避免 | ✅ 建議（Day 1 語感） |
|--------|----------------------|
| 你必須立刻把牠吹乾。 | 你還不知道該先做哪一步，心裡有點慌——但你知道，不能讓牠就這樣濕著過夜。 |
| 這隻狗很害怕。 | 對上一雙濕漉漉、還在發抖的眼睛。 |
| 選項：安撫牠 | 走到三步外，輕聲說：「我在這，別害怕。」 |
| 第一晚成功度 +10 | 天快亮時，哀鳴終於慢慢停了。 |
| 你还在吗？ | 你還在嗎？ |
| 像記一張會考試的清單。 | 像記一張明天就要交的小考題目。 |

## 交付檢查清單

- [ ] 全文繁體，無簡體字
- [ ] **Ren'Py：** 無 U+00B7 間隔點、無缺字裝飾符；間隔用 `｜`／`・`
- [ ] 無 `牠 ` 異常空格；省略號統一 `……`
- [ ] 語氣與 **Day 1 同層次**（主文現場感、副文心裡話、選項具體動作）
- [ ] `text` / `sub` 換行節奏適合打字機（段不宜過長）
- [ ] 選項 key 與 `scenes.js` 一致
- [ ] 未取名前不用固定狗名；已取名後可自然念名字
- [ ] 無遊戲化數值語（Trust、+20 等）
- [ ] 無 `DayN`／`WeekN` 英文週次（改「第N天／第N週」）
- [ ] 跨週 callback 用中文時間錨（「第一天的教訓」「第三天的拖鞋」）
- [ ] 不訓話、不冷硬結論；狗用動作寫，少標籤
- [ ] **婉轉、不直白**：不講破機制／結局／睡姿；導引與選單不劇透
- [ ] Ch1：**每天至少 1 句人對狗對白**；`sub` 不主題總結（見 [`narrative-pacing-revision.md`](../narrative-pacing-revision.md)）

## 參考

- Day 1 詞彙與完整場景摘錄：[reference.md](reference.md)
- **Ch1 敘事節奏（text/sub 分層、對白類型）：** [narrative-pacing-revision.md](../narrative-pacing-revision.md)
- 批次繁簡修正：`Demo/tools/tw-locale-pass.js`
- 故事架構：[story-narrative](../story-narrative/SKILL.md)
- 語調金標原文：`Demo/js/scenes.js`（`prologue_rain`～`prologue_dawn`）
