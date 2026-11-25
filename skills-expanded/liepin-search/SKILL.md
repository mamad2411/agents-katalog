---
name: liepin-search
version: 1.0.0
description: >
  当用户想搜索国内职位、查找工作机会、看某个岗位的详情时使用本技能。覆盖中国大陆
  主要城市（北京、上海、深圳、广州、杭州、成都等），适用于所有行业与职能。
  触发词：找工作、求职、搜职位、招聘信息、有什么岗位、职位搜索、看看某公司在招什么、
  猎聘、job search、find jobs、job openings。
context: fork
enabled: true  # 设为 false 可保留技能但让 /job-scrape 跳过它
allowed-tools: Bash(node .agents/skills/liepin-search/cli/src/cli.ts:*), Bash(bun run .agents/skills/liepin-search/cli/src/cli.ts:*)
---

# 猎聘职位搜索

搜索猎聘的公开职位列表。免登录、免 API key、**零运行时依赖** —— 有 `bun` 就能跑。

## ⚠️ 仅供个人求职使用

本技能访问猎聘的公开页面与接口。猎聘 `www` 主机的 `robots.txt` 禁止带查询串的路径，
站点也部署了风控脚本。**请保持低频访问，不要用于商业用途或批量数据采集。**
CLI 内置了 1.5 秒最小请求间隔与退避重试，但仍请自行控制调用量，风险自负。

## 何时使用

- 按关键词 + 城市搜索在招职位
- 只看最近 N 天更新的职位
- 取某个职位的完整描述

## 命令

### 搜索职位

```bash
node .agents/skills/liepin-search/cli/src/cli.ts search -q "<关键词>" -l "<城市>" [参数]
```

- `--query <文本>` / `-q` — **必填**，关键词（职位名、技能）。
- `--location <城市>` / `-l` — **必填**，中文城市名（北京、上海、天津、广州、深圳、南京、
  杭州、合肥、福州、成都）或猎聘城市码。其他城市名会报 `BAD_CITY` 错误。
- `--jobage <天数>` — 只保留 N 天内更新的职位。**客户端过滤**（猎聘的服务端时间参数无效，见「注意事项」）。
- `--page <n>` — 页码，1 起始，**上限 10 页**。
- `--limit <n>` / `-n` — 客户端截断条数。
- `--edu` / `--years` / `--salary` / `--comp-scale` / `--industry` — 猎聘原生筛选码，见 `url-reference.md`。
  ⚠️ **求职流程里不要传这五个**（`workflows/job-scrape.md` Step 1b 第 5 条有实测账：按本科过滤会排掉 283 个岗，其中 24 个本来评到「可以投」；锁行业会砍掉 225 个行业字段为空的，其中 57 个能投）。服务端排掉的进不了库、回收不了，而这几个字段是**展示值**——`eduLevel` 与 JD 正文实测 58% 对不上。接口本身没问题，这五个参数是给「我就要看某一类」那种一次性查询用的。
- `--format json|table|plain` — 默认 `json`。

数字类参数（`--jobage`/`--page`/`--limit`）做**严格整数校验** —— 传 `3abc` 这类带
拖尾垃圾字符的值会直接报 `BAD_ARG` 并退出码 `1`，不会被静默截断成 `3`。

### 取职位详情

```bash
node .agents/skills/liepin-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

`id` 是搜索结果里的 `id`。也可以直接传完整职位 URL。**推荐传 URL** —— 猎聘的企业直招页
（`/job/<id>.shtml`）和猎头职位页（`/a/<id>.shtml`）路径不同，传裸 id 时 CLI 需要依次
试两条路径，多一次请求。

`detail` 返回的字段中 `title`/`company`/`location` 现在都来自详情页的 schema.org
JSON-LD 结构化数据，正常情况下三者都有值（不再是 null）；`date`/`eduLevel`/`workYears`/
`compScale`/`compIndustry`/`compStage`/`recruiterTitle`/`recruiterSurname` 详情页本身
不提供，恒为 `null` —— 需要这些字段请从 `search` 的结果里取。

## 使用示例

```bash
# 北京的后端岗位，近 14 天更新
node .agents/skills/liepin-search/cli/src/cli.ts search -q "后端开发" -l "北京" --jobage 14 --format table

# 上海的产品经理，取前 10 条
node .agents/skills/liepin-search/cli/src/cli.ts search -q "产品经理" -l "上海" --limit 10 --format plain

# 深圳的数据分析岗第 2 页
node .agents/skills/liepin-search/cli/src/cli.ts search -q "数据分析" -l "深圳" --page 2

# 某个职位的完整描述
node .agents/skills/liepin-search/cli/src/cli.ts detail "https://www.liepin.com/job/1983665159.shtml" --format plain
```

## 输出格式

| 格式 | 适用场景 |
|------|---------|
| `json` | 默认 —— 程序化使用，把 `id`/`url` 传给 `detail` |
| `table` | 快速人工扫读 |
| `plain` | 读单个职位的完整详情 |

搜索结果每条包含契约字段 `id`/`title`/`company`/`location`/`date`/`url`，以及国内求职
关键字段：`salary`（原样保留「薪资面议」）、`salaryMonths`（如 15 薪则为 `15`）、
`eduLevel`、`workYears`、`compScale`、`compIndustry`、`compStage`（融资阶段）、
`recruiterTitle`、`recruiterSurname`、`isHeadhunter`。缺失值一律为 `null`，不会省略键。

> `recruiterSurname` 是跟你说话的那个人的**姓**，从接口的 `recruiter.recruiterName`
> 截出来的。**CLI 不输出全名** —— 下游要它只为跟进消息里的那句称呼
> （`<姓>女士`），而全名是第三方个人信息，截断放在最上游才不用赌下游每一层
> 都记得脱敏。非中文名返回 `null`（拉丁名分不出姓在前在后，猜错就是把全名
> 原样吐出去）。
> ⚠️ 它和 `recruiterTitle` **不是一回事**：后者装的是**职务**（「猎头顾问」
> 「HRBP」「招聘专员」「研发总监」…），同一个值会挂在几十个不同的招聘者身上 ——
> 那是角色，不是人，当称呼用不了。

`search` 的 `json` 格式在 `meta` 里还带 `count`/`page`/`totalPage`/`city`/`hasNext`，
以及 `skipped` —— 接口返回的卡片里解析失败被跳过的条数。正常应为 `0`；非 0 就是信号：
要么这一批数据本身有畸形卡片，要么猎聘改了字段结构，值得去 `url-reference.md` 核对。

所有错误写入 **stderr**，格式 `{"error": "...", "code": "..."}`，退出码 `1`。已知错误码
包括 `NO_QUERY`/`NO_LOCATION`/`BAD_CITY`/`BAD_ARG`/`NO_ID`/`BAD_ID`/`BAD_CMD`（参数或
用法问题）、`RATE_LIMITED`（**含义不单一，见下**）、`REQUEST_FAILED`（网络/HTTP 错误）、
`NOT_FOUND`（detail 的职位不存在或已下线）、`PARSE_FAILED`（抓到了页面/响应但解析不出
预期数据，通常意味着猎聘改了 markup）、`INTERNAL_ERROR`（未分类的异常，来自 `cli.ts`
顶层兜底）、`SEARCH_FAILED`/`DETAIL_FAILED`（`search`/`detail` 各自 catch 块的兜底错误码，
出现在抛出的异常不是 `LiepinError` 时——通常是意外的代码错误或环境问题，而不是可归类的
猎聘接口/参数问题）。

**`RATE_LIMITED` 含义不单一，调用方需要自行区分**：这个 code 目前同时覆盖两种不同性质的
情况——
1. **真正的风控/限流**：HTTP 429/5xx 重试耗尽，或接口返回 HTML 而非 JSON（触发了验证页）。
   这种等一会再重试通常会自愈。
2. **请求参数非法**：`parseJobCards` 发现响应 `flag !== 1` 时也会抛 `RATE_LIMITED`
   （消息形如「猎聘接口返回 flag=0，通常意味着参数非法或触发风控」），但猎聘对非法筛选码
   （`--edu`/`--salary`/`--comp-scale`/`--industry` 传了猎聘不认的值）同样会返回 `flag !== 1`。
   **这种情况重试无用**——不会自愈，需要检查这几个筛选参数的值是否是 `url-reference.md`
   里列出的合法猎聘码。

   看到 `RATE_LIMITED` 报错时，先检查本次调用有没有传 `--edu`/`--salary`/`--comp-scale`/
   `--industry`：如果传了，先怀疑参数值不合法；只有确认参数都合法（或根本没传这几个
   筛选参数）时，才当作风控/限流处理、退避重试。（这是已知的错误码粒度问题，`helpers.ts`
   尚未把两种情况拆成不同 code——阶段 2 可能会改进，本文档只是如实反映现状。）

## 注意事项

- **`--jobage` 是客户端过滤。** 猎聘接口的 `pubTime` 参数是哑的 —— 传「一天内」照样返回
  两年前的职位，所以 CLI 按结果里的更新时间自行过滤。代价是：过滤发生在取回 42 条之后，
  过滤后条数可能远少于一页。
  - **没有更新时间的卡片也会被丢掉**，而 `refreshTime` 不是每张卡都有
    （实测某用户职位库里 2232 个猎聘岗只有 259 个带日期）。
  - 所以 `meta` 里分开报两个数：`droppedTooOld`（有日期、太旧 —— 过滤器在干活）
    和 **`droppedNoDate`（没日期，被一起丢了 —— 那些可能是新岗）**。
    `droppedNoDate` 明显偏大时，这一轮考虑**别传 `--jobage`**，
    宁可多抓一些旧的，也好过把新岗一起扔掉。
  - **原来这里写「翻页时干脆别传它」，2026-08-27 那个前提被实测推翻了。**
    旧依据（某用户职位库 2026-08-23）：带日期的比例 **第 1 页 250/860（29%）·
    第 2 页往后 9/710（1%）**，据此得出「`--jobage` 从第 2 页起几乎会把收获清空」。
    而 2026-08-27 从同一个 CLI、同样不传 `--jobage` 抓了 4 个词 × 前 2 页，
    入库 140 个：**第 1 页 97/97、第 2 页 43/43，两边都是 100% 带日期**。
    所以那个 1% 不是页码的性质，是当时那批数据的性质。
    **改成：翻页照常可以传，但每一轮都看一眼 `droppedNoDate`** ——
    它看的是这一次请求的实际情况，不是一个会过期的分布。
- **翻页上限 10 页。** 接口报的总数（约 800）不可信，实际只能翻到第 10 页（约 400 条）。
- **每页 42 条里有 2 条不是本市的。** 猎聘会掺入推广位。CLI 不过滤它们（过滤会误伤真实的
  跨区职位），使用时请看 `location` 字段。
- **猎头职位占比不低。** `isHeadhunter` 为 `true` 的职位由猎头顾问发布而非企业 HR 直招，
  沟通链路更长。这是信息，不是缺点。
- **`date` 是「更新时间」不是「发布时间」。** 猎聘的职位会被反复刷新，一个长期挂着的岗位
  可以有很新的更新时间。评估时结合 `04-job-evaluation.md` 的职位真伪信号一起看。
- **限速是进程内的。** CLI 内置 1.5 秒最小请求间隔，同一个进程里的请求会串行排队。但并行运行
  多个 CLI 进程（例如 `/job-scrape` 同时跑多个 portal）时，各进程各有各的计时，**互不约束** ——
  真正的总量控制取决于你怎么调用它。
- 触发风控/限流，或传了非法筛选参数时，CLI 都会以 `RATE_LIMITED` 报错退出，**不会静默
  返回空结果**。两者含义不同、处理方式也不同——见上面「已知错误码」一节里 `RATE_LIMITED`
  的展开说明，不要不加区分地一律退避重试。
- markup 变更时的修复入口是 `url-reference.md`，它记录了全部接口参数与解析锚点。
