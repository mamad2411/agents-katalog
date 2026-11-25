---
name: xxljob-ops
description: Reconcile xxl-job scheduled tasks between source code and a target environment's console. Use this when someone wants to check which coded xxl-job handlers (@JobHandler / @XxlJob) are actually scheduled in an env (dev/test/prd), find code-but-not-configured or console-but-not-coded handlers, or spot handler-name mismatches between code and console. Triggers on "核对 xxljob", "任务调度状态核对", "扫代码里的 xxl-job 任务", "哪些 job 真在环境里跑", "代码和控制台对不上", "xxljob reconcile". This skill v1 = scan + reconcile. (Viewing job run logs and troubleshooting with kibana app logs are future extensions, not yet built.)
---

# xxl-job 代码 ↔ 控制台核对

## 最容易踩的点(lead-with)

代码里有 `@JobHandler` / `@XxlJob` **不等于**控制台真的配了调度。cron、启停、分片、路由全在 xxl-job 控制台,**代码里看不到执行频率**。本 skill 的价值就是**两边核对**,把三类问题挖出来:代码有但控制台没配(未部署/废弃)、控制台有但代码扫描没见(新增/他处)、handler 名两边对不上(契约不一致)。

两个工具,各管一边,都只出 JSON(汇总由本 skill/agent 做,见 `tools/repo-changes.md` 的 collector 契约):

- **代码侧**:`npm run xxljob-scan -- --root <src-root>`(离线扫源码,见 `tools/xxljob-scan.md`)。
- **控制台侧**:`npm run xxljob -- snapshot --env <env>`(在线查控制台,见 `tools/xxljob.md`)。

## v1 流程:扫描 + 核对

### 1. 收输入

需要两样:**源码根目录 `--root`** + **目标环境 `--env`**(环境名在 `.myws/xxljob.config.json`)。

- 不确定有哪些环境?`npm run xxljob -- envs`(不泄密)。
- 缺 `.myws/xxljob.config.json` 或 `--root` 不对 → 引导到 `tools/xxljob.md`(env/配置)或 `tools/xxljob-scan.md`(root)。

### 2. 扫代码(代码侧 handler 集)

```bash
npm run xxljob-scan --silent -- --root <src-root> --compact
```

留意输出里 `valueForm: "unresolved:..."` 的条目——常量引用没在同文件解析出来,要人工跟一下(看那个类的 `static final String`)。`valueForm: "constant:..."` 是正常已解析。

### 3. 取环境状态(控制台侧)

```bash
npm run xxljob --silent -- snapshot --env <env>
```

(全量执行器+任务,推荐。)或 `executors list` + 逐执行器 `jobs list`。得到环境侧 handler + `{cron, 描述, triggerStatus, jobGroup}`,同一 handler 多注册(分片/多参数)会有多条。

### 4. 核对 join(本 step 由你/agent 做,不进工具)

键 = **handler 名,大小写不敏感**(handler value 是控制台与代码的契约;但两边可能差大小写,所以按小写 join,差异单独标)。分四类:

| 类别 | 含义 | 建议标记 |
|---|---|---|
| 两边都有 | 已配置 | 带 `ON`/`停用`、cron、描述;多注册逐条列 |
| 代码有、控制台无 | 疑似未部署/废弃 | `未配置` |
| 控制台有、代码扫描无 | 新增 / 在别的模块 / 常量未解析 | `未见于扫描` |
| 仅大小写不同 | 契约不一致 | `契约不一致`(handler value 两边应一致) |

> 别把「文档抄录错误」当成契约不一致:本 skill 直接读代码(scan)和控制台(snapshot),两边都是真值;真·契约不一致 = 代码里的 value 和控制台里的 value 字面不同。

### 5. 呈现

核对报告表,建议列:`handler | 描述 | cron | 状态 | api | 类名`。能从 scan 输出的 `package`(如 `...jobhandler.outbound`)推断业务域就分组。同一 handler 多注册:单元格内换行(`<br>`)或分行,按 job id 升序。

两种落档,按上下文选:

- **打印报告**(默认):直接给用户看。
- **标注到目标 inventory 文档**(如 `docs/projects/<proj>/<proj>-scheduled-jobs.md`):钉死**时间戳 + 数据源**——代码扫描日期、控制台快照 `takenAt`、env、执行器名。示例见 `docs/projects/<proj>/<proj>-scheduled-jobs.md` §3。

### 6. 复查(常见坑)

- **dev `/joblog` 服务端 504**:只影响"查日志",**不影响核对**(核对只用 snapshot,不查 log)。
- **auth / 连通失败**:透传 `XxljobApiError`(`status`/`body`/`url`/`env`),指引到 `tools/xxljob.md`。
- **scan 0 命中**:多半 `--root`/`--glob`/`--api` 给错;先 `npm run xxljob-scan -- --root <root>` 看 stderr 提示。

## 后续扩展(尚未实现)

- **查任务运行日志**(`jobs log <id> --group N --env`):见 `tools/xxljob.md`。⚠️ dev 实测 `/joblog` 504(>60s),test/prd 正常。
- **排查任务问题**(xxljob 调度日志 + kibana 应用实例日志):⚠️ kibana 工具当前只管 Spaces/Data-Views、**查不了应用日志文档**(未接 ES `_search`);应用日志步骤在工具扩展前走 Kibana UI 手动。

> 这两块的细化流程待补到 `references/logs.md` 与 `references/troubleshoot.md`;v1 不建。
