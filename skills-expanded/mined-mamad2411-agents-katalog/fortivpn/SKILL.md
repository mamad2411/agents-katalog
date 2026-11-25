---
name: fortivpn
description: Diagnose and restore FortiClient VPN connectivity on macOS or Windows. Use when the user asks to connect, disconnect, or check FortiClient VPN, or when a task requiring a company/private network fails and a disconnected VPN may be the cause. 也適用於「VPN 斷線、VPN 沒連上、開 VPN、連 VPN、關 VPN」。Do not use for unrelated public-network failures or other VPN products.
---

# FortiClient VPN

操作 FortiClient 已存在的 SSL/IPsec profile。不要改用作業系統內建 VPN、其他 VPN app，或自行建立、修改 FortiClient profile。

## 平台路由

先判斷目前實際執行命令的作業系統，只讀取並遵循對應文件：

- macOS：讀取 [references/macos.md](references/macos.md)。使用本專案的 `fortivpn` CLI。
- Windows：讀取 [references/windows.md](references/windows.md)。直接使用 Fortinet 官方 `FortiVPN.exe --cli`；不要安裝或尋找本專案的 Windows binary。
- 其他系統：回報此 Skill 尚未提供操作流程，不要自行改用其他 VPN 工具。

不要同時載入另一個平台的文件，也不要混用兩個平台的指令或狀態格式。

## 共用行為

- 當原任務明確需要公司內網、私有 Git、內部 API、SSH 或內部網站，且連線錯誤可能由 VPN 中斷造成時，可以直接執行唯讀狀態檢查。不要因為一般公開網路服務失敗就自行連 VPN。
- 只有使用者明確要求連線，或原任務明確需要公司／私有網路且狀態已確認為中斷時，才恢復連線。
- Profile 必須能由使用者指定、既有預設值或唯一 profile 明確決定；有多個候選時列出名稱請使用者選擇，不得猜測。
- 若已連到另一個 profile，不得自行中斷或切換。只有使用者明確要求關閉 VPN 時才中斷連線。
- 連線或中斷後必須重新查詢狀態。失敗時保留原始錯誤並停止，不要無限重試。
- SAML、OTP、FIDO、憑證或瀏覽器驗證應交給 FortiClient 官方流程。不得繞過驗證，也不得要求使用者把密碼貼在對話中。
- VPN 恢復後繼續原本被中斷的任務。若 VPN 狀態正常但原操作仍失敗，只重試原操作一次，接著視為非單純 VPN 問題。
