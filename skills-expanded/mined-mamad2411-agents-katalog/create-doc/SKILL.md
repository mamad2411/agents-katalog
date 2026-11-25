---
name: create-doc-skill
description: 把一个 SaaS / 开放平台 / 云服务的开发者文档站（一个 URL）变成一份可安装的 Claude Skill（SKILL.md + references/ + evals/），让 Agent 之后能第一次就写对调用该平台 API 的代码，而不是凭训练记忆编参数名。流程是：抓取 llms.txt / OpenAPI 打草稿 → 用真实 API Key 逐条验证并修正官方文档里的错误 → 用有 skill 和无 skill 的对照实验证明价值 → 用 skill-creator 优化描述并打包。当用户说"帮我做一个 XXX 的接入 skill""把这个开放平台的文档整理成技能包""生成 XXX 的 SKILL.md""create a skill from these API docs"，或者给出一个开发者文档 / API reference 的 URL 并希望"以后 Agent 能直接用"时，务必使用本技能——哪怕用户没说"skill"这个词，只说"把这套 API 文档整理成 AI 能用的东西"也应触发；更新、补验证、迭代一份之前用这套方法生成的接入 skill（"拿到 key 了把 XX skill 的验证补完"）也用本技能。不适用于：只查一次某个接口怎么调，或者做与第三方 API 无关的通用 skill（那种直接用 skill-creator）。
---

# create-doc-skill：从开发者文档站生成 API 接入 Skill

输入一个开放平台的开发者文档站 URL，产出一份 **结构规范、内容经过真实调用验证、并且用对照实验证明过比"不装 skill 直接凭经验写代码"更好** 的 Skill。

这不是"读文档转述"。两个真实案例说明为什么：给智谱开放平台做 skill 时，光读文档会把 **7 处官方文档自身的错误** 原样抄进技能包（必填字段实际不校验、响应字段名写错、Batch 只认一份独立的模型白名单……）；给 AutoDL 做 skill 时，官方文档给 GET 接口画的是 JSON body 示例，实测必须走 query string。这类错误在代码审查里永远发现不了，只有真的调一次 API 才会暴露。所以第 3、4 步不是可选项，是这份 skill 与"让 Agent 总结一下文档"的全部区别。

## 全局流程与每步产物

| 步骤 | 目标 | 产物 | 详细指引 |
|---|---|---|---|
| 1. 抓取与勘探 | 搞清平台 API 全貌，拿到最权威的原始材料 | scratch 目录：Markdown 源页 + 展开 `$ref` 的 OpenAPI 摘要 + 鉴权格式 | [references/explore.md](references/explore.md) |
| 2. 结构化撰写 | 按开发者意图重组成三层渐进加载的 skill | `SKILL.md`（路由 + 通用规则）+ `references/*.md` | [references/write.md](references/write.md) |
| 3. 真实 API 验证 | 找出并修正文档与真实行为不一致的地方 | 带验证日期和报错原文的 reference 修订；未验证区域的显式标注 | [references/verify.md](references/verify.md) |
| 4. 对照实验 | 证明 skill 在哪些具体场景改变了结果 | `evals/evals.json`、`<skill>-workspace/iteration-N/`、`comparison-report.md` | [references/evaluate.md](references/evaluate.md) |
| 5. 打包发布 | 优化触发描述、校验、打包、安装 | 优化后的 `description`、`<skill>.skill` | 本文末尾 |

每一步开始前读对应的 reference 文件，不要凭印象做。下面只讲每步的关键判断和最容易做错的地方。

## 动手前先和用户确认三件事

1. **有没有真实 API Key，额度多少**。这决定第 3 步能做到什么程度。没有 key 也要照做第 1、2 步，但交付物里必须逐文件标明"未经真实调用验证"，把验证计划写出来留给有 key 的人，第 4 步只交付写好的 `evals/evals.json`（见 verify.md 的降级方案）。不要因为没有 key 就悄悄跳过第 3 步、也不要假装验证过——尤其是文档里抄来的报错信息，要标"文档原文，未实测"。
2. **目标语言 / SDK 偏好**。示例代码默认给 curl + Python（`requests`），如果用户的项目是 TypeScript / Go / Java，示例要换成对应语言，官方 SDK 存在时优先展示 SDK 用法并注明底层 endpoint。
3. **输出位置**。skill 目录（可分发）和 `<skill>-workspace/`（评测产物，不分发）是兄弟目录，先问清放哪。

顺带看一眼平台是否已经有官方 MCP server 或 `llms-full.txt`：有的话它们是第 1 步的额外输入，不是替代品——MCP server 暴露的是工具，不是"怎么写代码"的知识。

## 第一步：抓取与勘探（关键判断）

- **先试 `https://<docs-domain>/llms.txt`**，再找 OpenAPI / AsyncAPI 规范文件。规范文件是全流程最重要的原始材料：字段类型、`required`、枚举值都是精确的，人写的教程只挑重点讲。
- **不要通读原始 JSON**。用 `scripts/openapi_summary.py` 把规范按 tag 展开成可读摘要，用 `scripts/fetch_docs.sh` 从 `llms.txt` 并发拉取 Markdown 源页。两个脚本的用法在 explore.md。
- **`llms.txt` 里的 OpenAPI 段落可能是错的**（见过列出 `package.json` 的），规范文件的真实位置要自己核实：直接访问、看 API reference 页面的网络请求、或在文档站源码里搜。
- **第一步就锁死鉴权格式**。从 `securitySchemes` 或文档明确 header 的精确写法。AutoDL 的 header 是裸 token，没有 `Bearer` 前缀，凭"一般平台的习惯"写就全盘皆错。
- 没有 `llms.txt` 也没有规范文件的站点（国内平台常见），explore.md 有 fallback：sitemap、渲染后的 DOM、手工页面清单。

## 第二步：结构化撰写（关键判断）

- **先加载 `/anthropic-skills:skill-creator`**，按它的 frontmatter 规范、`references/` 与 `evals/` 位置、SKILL.md 行数上限初始化目录，再往里填内容。
- **SKILL.md 只做路由**：固定开头（Base URL、鉴权、最容易选错的那个字段）→ 30 秒跑通的最小请求 → "我想做什么 → 读哪个文件 → 涉及哪些 endpoint"导航表 → 跨领域通用规则 → 目录结构和抓取日期。具体字段表和代码示例一律进 reference 文件。
- **按开发者意图分组，不照抄文档目录树**。官方文档常把关系很近的能力拆在三个入口（同一个"文档解析"分散在对话消息、异步解析服务、独立 OCR 接口里），好的 skill 在一处把选项摆在一起帮 Agent 做选型。
- **体力活并行委派**。endpoint 按能力域分 4-6 组，一次性并行派给子 Agent，每个子 Agent 拿同一份写作规范（write.md 里有完整模板）；自己写 SKILL.md 和需要全局视野的"模型 / 资源选型"文件。
- **不编造源文件里没有的字段**。写作规范里要明确这一条，子 Agent 遇到文档没写清的地方标 `⚠ 文档未说明`，留给第 3 步去测。

## 第三步：真实 API 验证与修正（最容易被跳过、最重要）

判断一份 skill 质量的标准不是"抄没抄对文档"，是"和真实接口行为对不对得上"。有 key 就把 skill 里每一类关键结论实测一遍：

- **低成本、快出结果的 endpoint 先测**（文本对话、embedding、小文件、只读查询），大消耗的用最小规模或酌情跳过并标注。
- **重点测四类地方**：规范说必填的字段省略会不会真报错；文档说响应会带的字段默认到底在不在；参数值和文档不一致时是报错还是静默失效（静默失效最危险）；平台独有、其他家没有对应物的能力（文档最语焉不详、Agent 最容易套别家经验编错）。
- **每处不一致立刻改回 reference，标注验证日期并附报错原文或响应片段**。"已用真实 API 验证（2026-09）：传 X 返回 `{"code":1210,...}`"比空口"已验证"有说服力，也让后人能判断是否过期。
- **文档本身错了的发现要升到 SKILL.md 的"跨领域通用规则"里**，不能只埋在 reference 深处——这类发现靠再仔细读文档也抓不到，价值最高，必须在永远加载的那一层可见。
- **验证不全要说清楚**。测试账号权限不够（比如未企业认证调不了某组接口）时，在 SKILL.md 顶部明确"哪些已验证、哪些仍是文档转录"，AutoDL 案例就是这么交付的。
- **Key 只走环境变量，用完全仓库 `grep` 一遍确认没泄漏；测试产生的文件、知识库、任务用完清理。**

## 第四步：用对照实验证明价值（关键判断）

- **场景专挑"有经验的开发者会凭其他平台的直觉写错"的任务**，Hello World 测不出价值。最好的场景直接来自第 3 步发现的偏差：不支持的参数静默失效、独立的模型白名单、需要显式开关才出现的字段。
- **每个场景两个版本同时发出**：一个子 Agent 读了 skill 再写代码，一个完全不给 skill。同一个 prompt，唯一变量是有没有 skill。这一步是 **spawn 子 Agent**，不是跑 skill-creator 的 `run_eval.py`（那个脚本只测触发描述，见下表）。
- **打分依据真实调用结果**。用第 3 步实测过的报错去判定两版代码在生产环境跑不跑得通，而不是"代码读起来像不像对"。智谱案例第 1 轮曾把一个平局误判为胜利，是重新真实调用才纠正的。
- **同一组场景换一个模型再跑一轮**，分离"模型特有的坑"和"平台通用的坑"，结论才站得住。
- **诚实报告平局**。"7 赢 7 平"比夸大的"14 战全胜"更可信。baseline 靠防御性编程侥幸绕过坑、或冷门细节恰好在预训练语料里，都算平局，如实写 Why。
- 报告写成 `<skill>-workspace/comparison-report.md`（Markdown，不做 HTML），格式见 evaluate.md。

## 第五步：打包发布

1. **优化触发描述**：按 skill-creator 的"Description Optimization"流程写 20 条触发 / 不触发查询（不触发的要是近似误触，不是无关问题），用 `run_loop.py` 跑优化，把 `best_description` 写回。检查是否列全了产品名、域名、SDK 包名、常见别称。
2. **校验并打包**：`package_skill.py` 会校验 frontmatter（name 是 kebab-case、description 无尖括号且 ≤1024 字符）并排除 `evals/`。确认 SKILL.md 仍在几百行以内；某个 reference 明显过大（>800 行、混了多个能力域）就再拆。
3. **安装并说明**：复制到 `~/.claude/skills/<name>/`，告诉用户新会话才会加载。

skill-creator 的脚本要 Python ≥ 3.10 和 `pyyaml`，且必须以模块方式从它的目录运行（按路径运行会报 `No module named 'scripts'`）：

```bash
cd "<skill-creator 目录>"
uv run --python 3.12 --with pyyaml python -m scripts.quick_validate <skill 目录>
uv run --python 3.12 --with pyyaml python -m scripts.package_skill <skill 目录>
uv run --python 3.12 --with pyyaml python -m scripts.run_loop --eval-set <trigger-eval.json> --skill-path <skill 目录> --model <模型> --max-iterations 3 --verbose
```

`run_loop.py` 靠 `claude -p --model <模型>` 跑触发测试。先用 `echo hi | claude -p --model <模型>` 试一下：本机 CLI 版本不认识这个模型 id 时每条查询都会 400，结果表现为"召回率 0%"然后在改写描述时崩溃，不是描述写得差。CLI 报"does not support this model"就换成它认识的别名（如 `opus`）。**被测 skill 不能同时装在 `~/.claude/skills/` 里**：评测靠一个临时命令 `<skill>-skill-<id>` 来检测触发，模型看到同名同描述的正式 skill 会直接调它，检测就记为未触发，同样表现为召回率 0%。跑之前把已安装副本移走，跑完再放回；并确认 `~/.claude/commands/` 里没有残留的临时文件。

## 与 skill-creator 的分工

每一次生成或迭代都通过 `/anthropic-skills:skill-creator` 做，不要自己另写一套评测 / 打分 / 打包流程。但要清楚它每个脚本到底干什么：

| 本流程的步骤 | 用 skill-creator 的什么 | 注意 |
|---|---|---|
| 第 2 步初始化目录、写 `evals/evals.json` | SKILL.md 规范、`references/schemas.md` | 断言字段名要按 schemas.md 写，viewer 依赖精确字段名 |
| 第 4 步跑 with / without 对照 | **spawn 子 Agent**（它的"Running and evaluating test cases"章节） | `run_eval.py` / `run_loop.py` **不是**干这个的 |
| 第 4 步打分、汇总、审阅 | `agents/grader.md`、`scripts/aggregate_benchmark.py`、`eval-viewer/generate_review.py`（无显示环境加 `--static`） | 每个 run 目录要有 `grading.json` + `timing.json` |
| 第 5 步优化描述 | `scripts/run_loop.py`（内部调 `run_eval.py` + `improve_description.py`，靠 `claude -p`） | 只评估"这条 description 会不会被触发" |
| 第 5 步打包 | `scripts/package_skill.py` | 需要 Python ≥ 3.10 |

哪怕只是小改一个 reference 文件，也要重跑受影响的验证和评测，确认没有把之前验证过的结论改坏。

## 交付前自检

- [ ] SKILL.md 开头三件事（Base URL、鉴权精确格式、最易选错的字段）都在，且来源是规范 / 实测而不是猜的
- [ ] 每个 reference 文件的每个 endpoint 都有 method + path + 关键参数表 + 示例 + 注意事项
- [ ] 每一处"已验证"都带日期和证据；每一处未验证的区域都显式标注
- [ ] 文档本身的错误已升到 SKILL.md 通用规则层
- [ ] `evals/evals.json` 里的场景是"直觉会写错"型，不是 Hello World
- [ ] `comparison-report.md` 如实记录了平局和被纠正的误判
- [ ] 全仓库 `grep` 过 key，测试资源已清理
- [ ] description 经过 `run_loop.py` 优化，`package_skill.py` 校验通过

## 反面案例：只做第 1、2 步会得到什么

一份字段表齐全、示例语法都对、看起来很完整的 skill——里面混着：一个被规范标为必填、实际从不校验的字段；一处文档写错、实测不存在的响应字段位置；一个任何通用知识都猜不到的隐藏限制（某个批处理服务只认一份和主力模型清单不重合的老白名单）。它们不会在代码审查里被发现，只会在有人真拿这份 skill 写代码、真调用一次 API 时暴露。这正是第 3、4 步存在的意义。
