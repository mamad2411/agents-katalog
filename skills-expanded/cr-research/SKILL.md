---
name: cr-research
description: 启动、继续、取消或删除一次公司尽调。用户要研究一家公司，或消息里带 start_research、resume、cancel、delete_job 操作时，先读这份。
---

# 跑一次尽调

全程在当前回合里跑完，不要用后台任务：后台任务写不了 `app/state.json`，界面上的进度就不会动。单回合默认最多 30 分钟，够跑完一次。

中途不要停下来问用户。公司名有歧义时选最知名的那家，把这个判断写进报告的信息缺口。

## 建任务

1. 任务 id 写成 `job-<年月日时分秒>-<公司名>`，只用小写字母、数字和连字符，比如 `job-20261103101500-stripe`。
2. 建目录 `app/jobs/<id>/`，把请求写进 `request.json`（`company`、`company_url`、`industry`、`hq_location`、`model`，用户没给的不写）。界面操作 `start_research` 的字段名和这里一样。
3. 改 `app/state.json`：
   - 删掉 `sample: true` 的任务，和 `timeline` 里属于它的条目。
   - 在 `jobs` 最前面加这个任务：`id`、`company`、`status: "pending"`、`progress: 0`，10 个 `nodes` 都是 `pending`，`docCounts` 四项都是 0，`updatedAt` 写当前时间。用户给了官网、行业、总部的话，写进 `companyUrl`、`industry`、`hqLocation`。
   - `selectedJobId` 设成这个任务，`view` 设成 `report`，`reportPreview` 设成空字符串，`sourcesPreview` 设成空数组。
4. 读 `cr-doctor` 技能，确定走轨 A 还是轨 B，写进 `runtime` 和任务的 `track`。
5. 轨 A 看下面。轨 B 读 `cr-pipeline` 技能。

## 写状态

`app/state.json` 只有你（主代理）写。子代理和脚本运行时你不要同时改它，子代理只写 `app/jobs/<id>/` 里自己的文件。

只改变化的字段，优先用编辑工具，不要每次重写整个文件。每个节点开始和结束都更新一次：

| 节点 | `status` | 节点完成后的 `progress` |
| --- | --- | --- |
| `grounding` | `grounding` | 10 |
| `financial_analyst`、`news_scanner`、`industry_analyst`、`company_analyst` | `researching` | 每完成一路加 10，最多 50 |
| `collector` | `collecting` | 55 |
| `curator` | `curating` | 65 |
| `enricher` | `enriching` | 75 |
| `briefing` | `briefing` | 85 |
| `editor` | `editing` | 全部做完后是 100，`status` 改成 `completed` |

每次更新都要：

- 把 `nodes.<节点>` 改成 `running`、`done` 或 `failed`，`currentStep` 写当前节点名，`updatedAt` 写当前时间（ISO 8601）。
- 在 `timeline` 末尾加一条 `{ "jobId", "at", "node", "status" }`，需要时加一句 `text`。`timeline` 超过 200 条时删掉最旧的。
- 在 `app/jobs/<id>/nodes.jsonl` 追加一行 `{"at":"…","node":"…","status":"…","detail":"…"}`。

## 轨 A：本机上游服务

`UP` 表示下面这个脚本，它只用 Python 标准库。`HOME` 是这个 Bot 自己的目录：

```bash
python3 "$HOME/skills/cr-research/scripts/upstream.py" <命令>        # macOS、Linux
python "$env:HOME\skills\cr-research\scripts\upstream.py" <命令>     # Windows PowerShell
```

1. 启动：

   ```bash
   UP start --api <apiBase> --job-dir app/jobs/<id> --company "<公司>" [--company-url <官网>] [--industry <行业>] [--hq <总部>] [--model <模型>]
   ```

   不要传任何 Key，上游服务读它自己的配置。

2. 跟进度，反复运行直到 `state` 不再是 `running`：

   ```bash
   UP follow --job-dir app/jobs/<id> --state app/state.json --job-id <id> --lang <报告语言> --max-seconds 90
   ```

   脚本自己更新界面状态、`nodes.jsonl` 和 `docCounts`。跑完会写好 `report.md` 和 `sources.json`，补上免责声明，把状态改成 `completed`，你不用再改一遍。

3. 看 `follow` 的结果：
   - `completed`：回复用户。
   - `failed`：错误已写进界面，告诉用户原因，已有的文件留着。
   - `unreachable`：上游服务连不上了。把任务改成 `failed`，`error` 写明原因，告诉用户可以重启服务后说“继续”。

上游的报告是英文的，没有语言选项。用户用别的语言提问时，回复里说明这一点，并用用户的语言写两三句摘要。

## 取消（`cancel`）

把任务改成 `cancelled`，`updatedAt` 写当前时间。轨 B 用 `interrupt_agent` 停掉还在跑的子代理。轨 A 停止跟进度，并告诉用户：上游服务没有取消接口，它会自己跑完，但结果不再写回来。

## 继续（`resume`）

任务停在中间（回合被中止、App 重启）时，用户说继续或发来 `resume`：

- 轨 A：直接再运行 `UP follow`。上游重启过的话会返回 `failed`，这时告诉用户要重新开始。
- 轨 B：看 `nodes` 和 `app/jobs/<id>/` 里已有的文件，从第一个不是 `done` 的节点接着做，已有的结果不要重做。

## 删除（`delete_job`）

界面上的删除按钮已经问过用户。用户是打字说要删的，先确认一次。

确认后只删 `app/jobs/<id>/`，再从 `jobs` 和 `timeline` 里去掉这个任务。`id` 必须是 `jobs` 里已有的，不要删别的目录。如果删的是选中的任务，把 `selectedJobId` 改成下一个任务，并清空 `reportPreview` 和 `sourcesPreview`。

## 出错时

| 情况 | 怎么办 |
| --- | --- |
| 模式设成轨 A，但上游服务连不上 | 任务 `failed`，把 `cr-doctor` 里的启动说明告诉用户，或者建议用兼容模式 |
| 搜索暂时不可用、被限流 | 等一会儿重试，最多 3 次；还不行就 `failed`，已有的文件留着，不编造内容 |
| 某一路没有结果 | 汇总时标出缺口，补洞时再试；还是没有，报告里写“这部分数据不足” |
| 写不出终稿 | `failed`，`error` 写明原因 |

## 回复

做完后一两句话：研究了哪家公司、用了多少来源、报告在界面上可以看。走轨 B 时加一句“用的是兼容模式”。详细内容不要再贴一遍。

在聊天渠道里没有界面：回复写成三到五句摘要，再用 `present` 发 `report.md`。结果只能回到这个会话，不能发到别的渠道；用户想在某个渠道收到，就在那个渠道里发起。
