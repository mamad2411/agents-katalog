---
name: pickfit-loop
description: 跑 pickfit 的收錄與修 harness 的 loop。從 loop/queue.jsonl 拿一個項目，在沙盒裡驗證；沒過就分辨是軟體的問題還是 pickfit 驗證環境的問題，是後者就修 harness、補測試、重跑，記錄後拿下一個，中途不停下來問人。使用者說「跑 loop」「繼續收錄」「修 harness」，或 /goal 的條件指到這個 skill 時使用。
---

# pickfit loop：收錄、驗證、修 harness

給在 loop worktree（分支 `loop/*`）裡工作的 session。為什麼這樣設計寫在 [docs/loop.md](../../../docs/loop.md)，這裡只寫怎麼做。

## 三條原則

1. **不停下來問。** 遇到問題先自己解。解不了就記下來，換下一個項目。「留給念誠的事」那一節列的幾件事也一樣：寫進 journal，然後繼續做別的。
2. **狀態放在磁碟上。** 佇列和問題清單用 `scripts/loop_state.py` 改。`loop/queue.jsonl` 和 `loop/issues.md` 的標題列不手改。下一個 session 什麼都不記得，只看得到 `loop/` 裡寫了什麼。
3. **通過與否不由你決定。** 判定來自 pickfit 的管線（安裝 agent、全新箱子重播、judge）。你修的是環境和操作層，標準不動。

## 開工前（每個 session 做一次）

- `git branch --show-current` 要是 `loop/…`。不是的話停下來，請使用者先跑 `scripts/loop_setup.sh`。
- `git merge --no-edit main`，把 main 上最新的管線併進來，免得用舊的程式跑。有衝突就 `git merge --abort`，在 journal 寫「需要你」，照現有的程式繼續。
- `uv run pytest -q` 要全過。沒過就先修到過，那是上一個 session 或剛併進來的程式留下的。
- 印 `uv run python scripts/loop_state.py open-issues`（還沒解決的 issue 一個一行：編號、標題、原因代碼、幾個項目在等），再讀 `loop/journal.md` 最後 40 行。`loop/issues.md` 不要整份讀，它已經 75 KB 還在變大。要哪個 issue 的細節，用 `loop_state.py issue H-00X` 只印那一段。
- 印一次 `uv run python scripts/loop_state.py status` 和 `python3 scripts/loop_budget.py status`。花費已經到上限就直接收尾。

## 一圈

1. **拿項目**：`uv run python scripts/loop_state.py next`。exit code 3 表示佇列空了，直接收尾。
2. **跑驗證**：
   - `reverify`（target 是 slug）：從 `data/software/<slug>.json` 讀 `repo.full_name`，先跑
     `uv run pickfit verify --batch 1 --repo <full_name> --force --runner modal --dry-run`。
     清單上只有目標那一款，才拿掉 `--dry-run` 跑真的。不要加 `--records`，它和 `--repo` 是聯集，會選到別款（H-001）。箱子不夠用時加 `--runtime vm`、`--display`、`--memory-mb`、`--file-mb`。只能從原始碼建置的（紀錄停在 `needs_toolchain`，或安裝候選只剩 `cargo`、`go`、`source`）加 `--toolchain`：映像裡有 gcc、g++、clang、make、cmake、Rust、Go，4 vCPU、6 GiB、單一指令 30 分鐘（H-002）。先用一般的箱子跑一次，確定真的要建置再加，建置的箱子比較貴也比較慢。工具一啟動就抱怨目錄的擁有者（訊息裡有 owner、ancestor、uid 65534）時，改加 `--runtime vm`：gVisor 箱子裡 `/`、`/home`、`/tmp` 的擁有者會顯示成 nobody，microVM 裡是正常的 root（H-008）。
   - dry-run 印 `0 to verify`，下面也沒有 `skip` 那一行：本機的 `runs/pipeline.db` 沒有這款的抽取結果（紀錄是別台機器寫的）。先跑 `uv run pickfit discover --repo <full_name>`，不花錢，它把 repo 的 README、檔案清單和規則標籤存進本機。`outcome` 是 `added` 或 `refreshed`、`rule_passed` 是 `true`，再跑 `uv run pickfit extract --repo <repo_id> --model prod --limit 1`（一筆約 US$0.1），然後重跑 dry-run。`outcome` 是別的（repo 不見了、名字被別的 repo 佔走）或 `rule_passed` 是 `false`，就照「分流」第一、二列處理，note 寫那個 outcome。
   - dry-run 有 `skip` 那一行：照它寫的原因處理。`platforms macos only`、`GUI app` 是 Linux 箱子驗不了，不是 harness 壞了。
   - `new`（target 是 `owner/name` 或網址）：照 `uv run pickfit --help` 的管線順序做，discover、prescreen、extract、profiles、verify，寫回之後做第 6 步的能力索引。網頁應用走 `pickfit webapps`。
   - 真的跑 `verify`（沒有 `--dry-run`）時，輸出導到 log 檔：`uv run pickfit verify … > runs/loop/verify-<slug>.log 2>&1`。安裝 agent 每一輪的 thinking 都會印出來，不導走就整份進了 session。dry-run 的輸出很短，照常看。
   - 會跑超過兩分鐘的指令放背景執行，等它結束的通知，不要輪詢。
3. **看結果**：`uv run python scripts/loop_state.py run-summary --slug <slug>`（或 `run-summary <run 目錄>`）。它從 `outcome.json` 和 `report.json` 抽出等級、未驗證的原因、judge、花費、功能清單，以及失敗那個指令的 stderr 尾巴，大約 1–2 KB，不含 agent 的 thinking。分流要更多細節時，再讀 log 的最後 40 行，或 `report.json`、`verification_run.json` 裡需要的那幾個欄位，不要整份印出來。
4. **分流**：照下一節。功能清單最多 6 項，一次驗證只逐項測前 4 項，第 5、6 項標成 `beyond_budget` 是設計如此，不是 harness 的問題，不用分流。
5. **寫回**：通過而且重播過的 run 用 `uv run python scripts/guarded_write_back.py <run 目錄>` 寫回，它會確認紀錄沒有因此變差。不手改 `data/software/`。輸出有 `written` 那一行才算寫回了：寫回和後面的 `finish` 用 `&&` 接，不要只用換行，寫回失敗（例如紀錄的 `kind` 和新的抽取不一致，H-009）時後面才不會照樣跑。已經誤記成 done 的項目用 `loop_state.py reopen ID --note "原因"` 改回來。
6. **補能力索引**（capabilities，給比對用，不逐項驗證）：寫回成功之後依序跑下面三個指令，也用 `&&` 接起來。第一個把這次 run 留下的 `--help` 收進 `runs/capabilities/help/`，不花錢。第二個是一次抽取，一筆約 US$0.1。第三個把結果寫進紀錄，只動 `capabilities`，不花錢。
   `uv run python -m pickfit.verify.help_text --slug <slug> && uv run pickfit extract --capabilities-only --repo <repo_id> --limit 1 && uv run pickfit profiles --capabilities-only --slug <slug>`
   最後一個指令印出 `no quoted capability` 時不必處理，紀錄照樣成立。watch 自動收錄的新軟體會自己做這一步，這裡只補 loop 手動驗證的項目。
7. **記錄**：`loop_state.py finish` 或 `park`；在 `loop/journal.md` 最後加一段（格式在那個檔案開頭）；commit，一個項目一個 commit，訊息用英文。`docs/plan.md` 的狀態紀錄只有協調的 session 寫，這裡不碰。
8. 印 `loop_state.py status` 和 `loop_budget.py status`，回到第 1 步。

## 分流：這次沒過，是誰的問題

| 看到什麼 | 是誰的問題 | 怎麼做 |
|---|---|---|
| 照它自己的文件裝，它自己的指令報錯；換一個全新的箱子結果一樣 | 軟體 | `finish --result unverified`，note 寫原因。不修。 |
| 要帳號、要付費、要真的硬體、要下載數 GB 的模型 | 驗證環境合理的限制 | `finish --result unverified`。確認紀錄的原因代碼說的是「pickfit 的環境沒有 X」，不是「軟體不能用」。 |
| 箱子少東西（編譯器、root、Docker、資源）、動作送不進 App、安裝 agent 走錯路、judge 把對的判成錯、管線指令本身壞了 | pickfit 的 harness | 進「修 harness」。 |

分不出來的時候，當成 harness 的問題查一次：在全新的箱子裡用最小的指令重現。重現不了，就照第一列處理。

## 修 harness

1. **對到 issue**。用 `loop_state.py open-issues --all` 找，有同一個問題就用它（細節用 `issue H-00X` 看），沒有就 `loop_state.py issue-new "標題"`。補上 symptom 和 reproduce，然後 `issue-status H-00X fixing`。
2. **先重現**。挑最小、最便宜的方式：能用 DockerBox 就不開 Modal，能不呼叫模型就不呼叫。
3. **先寫一個會失敗的測試**（放 `tests/`，用 fixture，不打付費 API），再動手修。
4. **能改的範圍**：`pickfit/verify/` 裡的箱子、映像、操作層、安裝 agent 的工具與提示，`pickfit/discover/`，管線的指令。判定、計分、schema、限制檢查不在範圍內，清單是 `scripts/loop_guard.py` 的 `PROTECTED`，hook 會擋。
5. **驗收，三樣都要過**：
   - `uv run pytest -q` 全過。既有的測試可以因為行為真的改了而修改，不能刪，也不能為了過關把斷言改鬆。
   - 動到箱子或映像時，`uv run pickfit verify --limits-test --runner modal` 全過，用到的 `--runtime`、`--display` 組合也要跑。讓隔離變鬆的修法不算修好。
   - 原本失敗的項目重跑後通過。另外挑一筆原本就通過、用同一種箱子的紀錄重跑，確認沒有變差。
6. **修好了**：commit，`issue-status H-00X fixed`。等這個 issue 的項目會自動排回佇列。在 issue 的 tried 寫下做法。
7. **同一個 issue 試了三種不同的做法都不行**：`issue-status H-00X parked`，寫清楚試過什麼、各自為什麼不行，然後往下走。不試第四次。
8. **非改受保護的檔案不可**：把檔案複製到 `runs/loop/draft/` 改，用 `diff -u` 產生 `loop/proposals/H-00X.patch`，在 issue 裡寫理由，`issue-status H-00X review`，往下走。

## 先找現成的套件

修 harness 之前先查有沒有人做好了。操作電腦、開瀏覽器、裝套件這類事，用現成的比自己重寫可靠（念誠 11/15）。

- 可以直接加的授權：MIT、Apache-2.0、BSD、ISC。其他的（AGPL、GPL、FSL、BUSL、沒寫授權）不加，寫成 proposal，issue 設 `review`。被測的軟體裝在沙盒裡，不受這條限制。
- 加了就記進 `NOTICE`（名稱、版本、授權、來源），版本要釘住。
- 裝在箱子裡的控制程式走 exec 通道（Modal 的 exec、`tart exec`），不開對外的連接埠。金鑰和模型呼叫留在主機。驗收照舊由 pickfit 自己檢查，套件和被測的 App 都不能替自己回報結果。

## 留給念誠的事

hook 會直接擋下這些：`git push`、`pickfit publish`、`wrangler deploy`、合併 PR、改受保護的檔案、手改紀錄、刪測試、讀 `eval/` 與 `.env`。

下面這幾件 hook 擋不到，也不要做：

- 在這台 Mac 上裝系統層的東西（`brew install`、改系統設定、下載數十 GB 的 VM 映像）。
- 建帳號、接受條款、開始用新的付費服務。
- 單一項目花超過 `loop/budget.json` 的 `item_usd`（看 run 的 `cost_usd` 加 `box_usd`）。快到了就停手，照 harness 的問題或合理的限制處理，不要再重跑。

遇到了就在 journal 那一段寫「需要你」，講清楚要決定什麼、卡住哪些項目，把那些項目 park，繼續下一個。

## 花費上限

上限寫在 `loop/budget.json`，從裡面的 `since` 起算，分兩本帳。`model` 是所有 session 經過帳本的模型呼叫，`box` 是每次驗證估出來的 Modal 沙盒費用。各有總額和每天的上限，`python3 scripts/loop_budget.py status` 會印出來。

到了上限，hook 會擋下所有要花錢的管線指令（`--dry-run` 和不花錢的指令照常能跑）。這時不要想辦法繞過：在 journal 寫「需要你」和那一行 `LOOP_BUDGET`，手上的項目留著不動，下一個 session 會接著做，然後收尾。`loop/budget.json` 只有念誠能改。

## 收尾

佇列空了，或這個 session 的目標達成時：

- 印 `loop_state.py status`。
- 在 journal 加一段小結：這次處理了幾筆、修好哪些 issue、哪些在等念誠。
- 不 push，不合併。分支留給念誠或協調的 session 看。
