---
name: trpg-session
description: 當使用者說「想玩 TRPG」、「跑團」、「TRPG 冒險」、「擲骰檢定」或「開 TRPG 團」時觸發。自動將工作區切換至專屬 TRPG 目錄，啟用 14 個 GM 專屬工具與狀態機守護 Hooks，跑團結束時自動切回輕量開發目錄。
compatibility: Requires Python 3, Bash, and the local /home/chihmin/src/trpg-gm-skill checkout.
---

# TRPG Dynamic Session & State Machine Workflow

> [!IMPORTANT]
> **🚨 強制第一步：自動切換至 TRPG 專屬工作區（AUTOMATIC WORKSPACE SWITCH）**
> 當使用者提到想玩 TRPG 或跑團時，**在第一時間使用 `bash` 工具執行工作區切換腳本**：
> ```bash
> python3 ~/.pi/agent/scripts/switch-workspace.py /home/chihmin/trpg
> ```
> 執行此腳本會自動通知 Piweb 網關將當前對話工作區切換至 `/home/chihmin/trpg`，下一則訊息會自動以完整 TRPG 擴充與狀態機 Hooks 啟動。

---

## 2. 跑團進行與工具使用規範

* 資料庫與劇本存檔統一管理於 `/home/chihmin/trpg`。
* 善用 `trpg_gm_context` 與 `trpg_gm_check` 進行檢定與情境判定。
* 每次重大抉擇或回合金結算時，呼叫 `trpg_turn_finalize` 與 `trpg_gm_recap_save` 確保進度持久化。

---

## 3. 🚨 跑團結束自動還原輕量工作區（AUTOMATIC CLEANUP）

當使用者表示：
* 「今天先玩到這裡」、「結束跑團」、「存檔離開」、「不玩了」
* 或戰役完成結算並存檔完成後

**必須在最後一輪對話中執行以下還原命令**：
```bash
python3 ~/.pi/agent/scripts/switch-workspace.py /home/chihmin/src
```
並告知使用者：「*已為您保存冒險進度，工作區已自動切回預設開發模式以節省 Token。*」
