---
name: project-card-cleanup
description: "Re-scope a project card CHAIN to its handoff role — 最高指導原則 + 實驗現狀紀錄 + 待辦 handoff — against an external authority layer (paper draft, .private/chapter-plan & evidence-map, or the axis card). Unlike project-card-merge (which FOLDS appends into the body), cleanup DISTILLS writing-phase appends, SUPERSEDES history pile-ups, and POINTERIZES content that now lives in the draft/plan/axis card, while preserving every experiment number, method record, figure, and card-link. Use when the user says 清理卡鏈 / cleanup 專案卡 / 卡鏈瘦身 / 讓卡回到指導原則 / handoff 化, typically during paper-writing periods when cards accumulate both cluster experiment appends and Mac-side planning appends. Consolidated (needs_merge=false) chains are VALID targets — this is a re-scoping, not a marker-driven merge."
---

# Project Card Cleanup — re-scope a card chain to 指導原則 + handoff

## 與 project-card-merge 的分工

| | merge | cleanup(本 skill) |
|---|---|---|
| 觸發 | 鏈上有 📥/🔍/孤兒 markers | 使用者點名(consolidated 鏈也是合法對象) |
| 動作 | fold appends 進正文 | 對照**參考文件層**重定位整條卡 |
| 內容權威 | 卡自身的 📥 blocks | 稿件 + .private/ 規劃檔 + 軸卡(見下) |
| 產出 | 一張整併卡 | 一張「指導原則+實驗現狀+待辦 handoff」卡 |

機制(chain dump / md5 lock / finalize_chain / cleanup_children)完全復用
merge 的 `merge_lib`;本 skill 的 `cleanup_lib` 只加薄層(見檔頭 docstring)。
merge 的 hard rules(下一步只放沒做的事、supersede 不重複、不丟 paper-grade
數字、card-link 與表格不自動搬運必須顯式重建)全數適用。

```python
import sys
sys.path.insert(0, "<本 skill 的 base 目錄>")   # skill 系統開頭給的路徑
import cleanup_lib as CL      # CL.M = merge_lib, CL.M.L = rewrite_lib
```

## Step 0 — 確認參考文件層與競態

1. **參考文件層**(pointerize 的合法性來源;至少一項存在,逐一向使用者確認路徑):
   - paper 稿件(如 Overleaf 專案 sections/ + main.tex + references.bib)
   - 規劃權威檔(`.private/chapter-plan-*.md`、`.private/outline-evidence-map-*.md`、`.private/lit-*.md`)
   - 軸卡(跨案卡:稿件狀態與待辦總表的家)——清理案卡時,軸卡是上游權威;清理軸卡時,上游是稿件+.private。
2. **競態防線**(同 merge):cluster 有進行中 campaign job/append 時,md5 lock 會擋
   entry 覆寫、`cleanup_children(md5s=…)` 會放過變動的舊卡(留孤兒待下輪)——
   但 trash 窗口的殘餘競態仍在,**開跑前看 squeue 或跟使用者確認**;使用者明知
   job running 仍指示清理時照做,靠 md5 防線兜底。

## Step 1 — Scan + dump 落檔(省 context 的讀法)

```bash
python3 ~/.claude/skills/research-cards/skills/project-card-merge/merge_lib.py <entryId>   # scan
```
```python
CHAIN, MD5S, IMGS = CL.dump_chain(ENTRY_ID, SCRATCH_DIR)   # ★ md5 基準在此定格
```
- dump 檔落 scratchpad 後**選擇性閱讀**:先 grep 各卡 H2/H3 結構,已讀過/自己寫過的段落
  不重讀,只細讀未讀段與 📥 blocks。大鏈全文進 context 會爆——這是實戰教訓。
- `IMGS` 逐卡圖片數:>0 的卡在重建時必須 `M.L.extract_images` → `M.L.img` 保全。
- 孤兒處理同 merge Step 2(讀+併入 MD5S)。

## Step 2 — 五類分類決策(cleanup 的核心)

對鏈上每個 H2/H3/📥 段落做一次分類;判準=「這段內容現在的權威落點在哪」:

| 類別 | 判準 | 動作 |
|---|---|---|
| **KEEP** | 實驗現狀權威在卡上:數字表、實驗統整、方法實作紀錄(檔案引用/機制詞彙)、Findings/設計理路、評估協定、仍 open 的 🔍、發想/未探索 | `CL.section`+`CL.emit` 原樣搬運(表格/cardlink 自動重建);可帶 `repl=` 做原位訂正 |
| **FOLD** | cluster 直寫的散裝進度(H3 無 📥 wrapper 也算)= 新實驗事實 | 折進實驗統整(新編號 N+1)/現狀/里程碑——同 merge 規則 |
| **DISTILL** | 寫作過程 append(規劃裁決、文獻查證、稿件進度記錄) | 已落地參考文件層的**刪**;殘值(未落地的裁決、對卡上舊文的更正、新實驗需求)蒸餾進對應正文段後刪殼 |
| **SUPERSEDE** | 現狀/下一步/待補的歷程堆疊(日期串、✅ 殼、被取代的舊裁決) | 重寫成**最新狀態**;下一步 hard rule:只放還沒做的、每項 1–3 句、細節指回實驗統整/現狀 |
| **POINTERIZE** | 內容已進稿/plan/軸卡且卡上只需「判決+出處」:文獻地形明細、章節裁決、gap 盤點 | 一句判決 + 指針(`.private/<檔>`、稿 §N、軸卡某段);明細刪 |

分類拿不準時:**寧 KEEP 勿刪**(卡是 paper-reference 卡;垃圾桶可還原但別依賴它)。

**`📜 log 時間線` 區與 `📎`/`📗` 行＝永久記錄，無條件 KEEP**（git 類比：
cleanup 是 paper branch 吸收後的去冗餘——rebase 掉的是「內容」，不是
commit 歷史；時間線行重建時必須帶真 card node——`CL.emit` 已內建）。

## Step 3 — 重建骨架

**案卡 arc**(實驗現狀焦點):
定位(一句目標+現行檔位+「本卡=實驗現狀+待辦 handoff;paper 敘事見軸卡」+codebase/wandb/protocol 指針+子題/軸卡 card-links)→ 現狀(最新,含 paper 對接條)→ 進展里程碑(新完成前插)→ 方法(原樣)→ 實驗統整(一..N,原樣;散裝進度折成 N+1)→ 評估協定 → Findings → 🔍(僅 open)→ 下一步 → 發想/未探索 → 待補。

**軸卡 arc**(指導原則+handoff hub):
論文故事線(thesis 現版+fallback+骨架一句+「裁決細節見 .private/chapter-plan」)→ 定位(+稿件指針:sections/、bib 條數、.private 清單、**cluster 用 view-only link**)→ 現狀(稿件狀態+佔位標記系統+三案實驗現狀+世代註記)→ 方法對照表 → 結果彙整(檔位表用最新裁決版+各軸數字)→ Findings → 文獻地形(**判決層**:novelty gate 結論/主張措辭/guardrails;明細=指針)→ 實驗待辦 handoff 表(deadline 排序,含角色與依賴欄)→ 待補 → 參考(文獻 card-links 全保全)。

## Step 4 — Rebuild + 驗證 + 寫入

```python
C = []
# … CL.emit / M.L.h / M.L.bp / M.table / M.cardlink 構建 …
print(CL.verify_content(C))       # card-links 數對照原鏈(扣 sentinel/back-ref)、tables、H2 清單
print(CL.seg_sizes(C))            # 段落大小分佈(finalize 抱怨時先看這個)
print(CL.finalize_with_room(ENTRY_ID, MD5S[ENTRY_ID], C, COLOR, dry_run=True))
# dry-run 計畫 OK 後:
CL.finalize_with_room(ENTRY_ID, MD5S[ENTRY_ID], C, COLOR, dry_run=False)
```
- **md5 一定用 Step 1 的 `MD5S`**,絕不重讀(同 merge:重讀=靜默蓋掉清理期間落地的 append)。
- `finalize_with_room` 預設 threshold=62000:重建卡 bullet/表格節點密、存檔 UUID 膨脹
  ~40B/node,原 80K 貪心會讓單段膨脹後爆 100K cap(實戰踩過)。
- **builders 備忘**:`M.L.bp(text)`=純 bullet(`bul(label,text)` 是雙參數的);dump 標題
  是全形括號——`CL.section` 已容錯,自寫 regex 時注意。
- **⚠️ chain plumbing 絕不搬運(2026-07-19 事故)**:dump 尾部的 `▶ 續卡…[[card:…]]`
  sentinel 與 merge-spill auto-header(「…的續卡 N/…;母卡:…」)**不是內容**——搬進
  重建卡會留下指向已 trash 卡的假 sentinel,`append_card` 的 chain walk 會沿它撞上
  trashed card 而失敗。`CL.emit` 已內建 HARD FILTER 過濾兩者(finalize_chain 會自建
  正版);若手寫搬運邏輯,必須同樣過濾。事故修復法:逐卡刪除「非鏈上下一張」的
  LINK_MARK paragraph(保留正版),見 scratchpad 修復腳本模式。

## Step 5 — cleanup_children + verify + 回報

```python
CL.M.cleanup_children(OLD_CHILD_IDS, md5s=MD5S)   # md5 變動的卡不 trash(留孤兒)
```
```bash
python3 ~/.claude/skills/research-cards/skills/project-card-merge/merge_lib.py <entryId>  # needs_merge=false、無孤兒
```
回報:五類各處理了什麼、新鏈布局、保全清單(card-links/tables/圖)、KEEP 之外
被刪內容的權威落點對照。清理本身**不 append 記錄**(卡的新狀態即記錄);若清理
連帶動了稿件才照慣例 append 稿件側進度。

## Step 6 — 自動收斂 repair → note-sync → 全視圖（硬規則）

```bash
python3 <plugin 的 skills/project-card-log 目錄>/post_project_sync.py \
  --card <ENTRY_ID>
```

只在 Step 5 的 child cleanup＋verify 完成後呼叫。runner 與 cluster
project-log drain **共用同一條實作**，固定依序：
**repair_chain --seal → pinpoint project-card-repair → 一次 note-sync →
timeline canvas → 裸跑 context mind map**；若既有 mind map 是 story 且
coverage 有缺口，再進 `story_auto_expand.py` 的 guarded proposal 流程。

cleanup 重排了整條鏈（trash 子卡、改 entry），所以 repair 與 sync 都
必須先於視圖；順序反了會把未鏡像節點、trash 殘影或斷 link 畫進圖。
任何一步失敗、note-sync conflict、canvas coverage 不完整都以非零退出，
修好後重跑同一指令（全流程 idempotent）。Heptabase-only、沒有 local
hub 時仍完成 repair，並略過不可用的 note-sync／canvas；`--dry-run`
可先看完整 command plan。

（本 skill 與 merge 同為 Mac-only——overwrite/trash 是 bridge 做不到
的；萬一在 cluster 端執行到這裡，跳過本步、回 Mac 補跑。）

## Notes

- **供 cluster 的 handoff 指針是一級公民**:view-only link、HANDOFF_*.md 路徑、
  protocol 口徑條目、待辦表的「依賴/狀態」欄——清理時只能更新、不能清掉。
- 待辦表項目完成後(如 U7/RTF 收數):項目從表中移除或改狀態,數字歸宿=實驗統整
  /稿件;不留「✅ 已完成」殼(merge 的下一步 hard rule 同樣管待辦表)。
- 與 merge 的節奏配合:cluster append → merge 折卡(marker 驅動)→ 寫作期 cleanup
  重定位(使用者驅動)→ cluster 再 append……cleanup 不取代 merge。
- Idempotent:對剛清理過、無新內容的鏈重跑=結構不變的 no-op(重寫成一樣的卡)。
