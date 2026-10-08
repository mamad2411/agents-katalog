# Repo Ref
- source: https://github.com/othmanadi/planning-with-files (path: skills/i18n/planning-with-files-zht/SKILL.md, branch: master)
- mined: 2026-09-20
- desc: 用於多步驟 AI 代理工作的持久化檔案規劃。將 task_plan.md、findings.md 與 progress.md 保存在磁碟上，生命週期鉤子會注入選定的專案規劃內容。自動恢復只讀取專案規劃檔案；只有明確執行 session-catchup.py --metadata 才會檢查本機同一專案的代理工作階段中繼資料，--replay 則會輸出有界且以 nonce 框定的摘錄。選用的閘門模式只
