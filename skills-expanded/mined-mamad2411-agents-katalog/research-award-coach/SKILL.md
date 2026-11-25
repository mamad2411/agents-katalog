---
name: research-award-coach
description: Coach students planning, drafting, or revising Taiwan NSTC undergraduate research proposals and reports using distilled patterns from 111–114 academic-year Research Creativity Award winners. Use for topic selection, discipline and specialty routing, methodology, innovation, report structure, writing feedback, and finding real award-winning project examples by topic.
---

# 大專生研究創作獎教練

## Overview

依 111–114 年度研究創作獎得獎報告的蒸餾結果，協助學生改善研究選題、方法、創新點、結構與寫作。把資料視為經驗參考，不宣稱符合特徵即可獲獎。

## When to Use

用於規劃大專學生研究計畫、檢查研究構想、修改計畫書或成果報告，以及尋找相近的真實得獎計畫。一般論文寫作問題若不涉及此獎項，僅在這些資料確實有參考價值時使用。

## Workflow

1. 確認學生目前處於構想、計畫書、執行中或成果報告階段，並取得研究主題或草稿。
2. 判定最接近的領域：人文社會、工程技術、數理科學或生命科學（科教研究屬人文社會之下的專長）。學門難判定時，先用 `find_examples.py`（見第 4 步）查同題材案例——得獎名單的既有分類本身就是最強的路由訊號；若題目正是某得獎計畫，一次查詢即可定案。仍無法判定時再讀 `references/_overview.md`。
3. 讀取 `references/<領域>.md`。若已知專長且 `references/<領域>/<專長>.md` 存在，再讀該檔；不存在時只使用領域檔，不硬套其他專長。
4. 需要實例時，在本 Skill 根目錄執行：

   ```bash
   python scripts/find_examples.py "主題關鍵詞" --discipline "領域" --specialty "專長" --limit 5
   ```

   可省略未知的篩選條件。查詢只使用公開得獎名單中的計畫名稱與分類 metadata。以輸出的計畫編號標示實例；不要捏造未回傳的計畫、成果或因果關係。
5. 對照學生內容與 reference，先指出已有的有效設計，再提出少量、可執行且符合該研究階段的修改。優先處理研究問題、方法與證據是否對齊，再處理創新表述與文字潤飾。
6. 保留學生原本的研究判斷與語氣。將得獎作品當作模式和例證，不把它們改寫成模板答案。

## Verification

- 確認建議來自正確的領域與專長 reference。
- 確認提及的真實案例都有 `find_examples.py` 回傳的計畫編號。
- 區分資料觀察、推論與建議，不把共同特徵說成獲獎保證。
- 讓每項修改都對應學生草稿中的具體位置或缺口。
- 說明資料範圍為 111–114 年度；案例查詢來自公開得獎名單。
