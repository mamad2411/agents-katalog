---
name: claude-detection
description: 检测一个提供 Claude 模型的 API 端点（官方 API、云平台、第三方中转 / 代理 / 分销渠道）是否是声明的那个模型、是否"掺水"：模型替换（便宜模型冒充）、部分请求偷换、降低推理强度、截断上下文或输出、注入提示词、改写参数或工具定义、剥离 thinking、虚报 usage、线路随时间切换。当用户要求检测中转站真假、是否满血、是否 0 注入、是否被换模型、是否降智，或要在第三方渠道上做实验前核验时使用。
---

# Claude Detection

用服务端不可轻易伪造的行为（thinking 签名校验、跨模型 thinking 读取规则、按真实长度触发的缓存、各模型不同的参数规则）和程序判分的新题，分维度判断一个 Claude 端点的真实性与完整性。**不采信模型自报身份、回答风格、响应速度、`model` 字段或响应头。**

完整方法、判读规则、历史经验与外部研究见 [reference/MANUAL.md](reference/MANUAL.md)。本页只给执行要点。

## 开始之前（必须）

1. **向用户确认**：端点地址、要检测的模型、预算上限、是否有官方 Anthropic Key 可做对照、能否看到中转后台日志。
2. **密钥只放环境变量或本地 `.env` 文件**，不要写进命令历史、脚本或报告：
   ```bash
   export BASE="<ENDPOINT_BASE_URL>"   # 例如 https://api.anthropic.com 或中转根地址
   export K="<YOUR_API_KEY>"
   export AUTH=both                    # 中转用 both；官方 API 用 xapikey
   export OUT=./probe_out/<run-name>   # 每次检测用新目录
   ```
   - 也可以在运行目录下建一个 `.env` 文件，每行一个 `KEY=VALUE`（同样支持 `export` 前缀），或用 `ENV_FILE` 指定路径。已经设置的环境变量优先。
   - **不要让用户把 Key 写在 `/claude-detection` 的命令参数或对话里**：参数会进入对话上下文。如果发现 Key 已经出现在对话中，在报告末尾提醒用户更换这个 Key。
   - **Windows**：PowerShell 用 `$env:BASE = "..."` 设置。脚本会把控制台输出统一成 UTF-8；`raw.jsonl` 和 `results.json` 写成纯 ASCII，用默认编码读取也不会报 `UnicodeDecodeError`。PowerShell 中文仍乱码时，再设置 `$env:PYTHONIOENCODING = "utf-8"`。
3. **先报成本再执行**。quick 档官方价目约 $1～2；standard 约 $8～15；deep（长上下文、困难档、大样本抽检）约 $30～60。中转实际扣费按其倍率计算。
4. **低并发**：默认 `--conc 2`。高并发会让中转成批返回 5xx 或空流，造成无法判定（MANUAL M13）。

## 执行流程

所有命令都在本 skill 目录下运行：`python scripts/claude_probe.py <子命令> --model claude-opus-5-5 [选项]`。结果写入 `$OUT/results.json`，全部请求和响应写入 `$OUT/raw.jsonl`。

**推荐：一键执行并评分**

```bash
python scripts/claude_probe.py run --tier quick --model claude-opus-5-5      # 约 150 次请求，官方价目 $1～2
python scripts/claude_probe.py run --tier standard --model claude-opus-5-5   # 约 $8～15
python scripts/claude_probe.py run --tier deep --model claude-opus-5-5       # 约 $30～60
```

跑完会生成 `$OUT/SCORE.md`（100 分制证据评分、结论画像、上游画像，见下文）。单步失败不会中断后续步骤。

**进度与耗时**：
- `run` 开始时打印预计请求数与耗时区间（quick 约 10～30 分钟，standard 约 1 小时左右），每一步开始和结束时打印 `[3/16] thinking 完成，用时 1.6 分钟`，S11 逐条打印 `进度 12/30`。
- **不要把输出接到 `| tail`、`| head` 之类的管道里**，否则输出要等到脚本结束才显示，用户会一直看不到进度。
- 长时间运行时，在后台运行，并把输出重定向到文件（例如 `> run.log 2>&1`），过程中读取这个文件，或运行 `python scripts/claude_probe.py status` 查看已完成的步骤，再向用户汇报进度。

| 档位 | 包含的子命令 | 回答的问题 |
|---|---|---|
| **quick** | `baseline` `substitution` `thinking` `tokenizer` `cachegate` `injection` `purity` `params` `channel`，首尾各测一次稳定性 | 是不是声明的模型；有没有可见 / 隐藏 / 条件 / 按轮 / 尾部注入；输出和参数有没有被改写；来自哪类渠道 |
| **standard** | quick + `audit --samples 30` `effort` `bench --seed random` `tools` `context --sizes 30000,190000` `stream` `onetoken` | 是否按比例偷换；是否降低推理强度；能力是否与已验证基线一致；工具与上下文是否完整 |
| **deep** | standard + `context` 到 750K、`bench --hard`、`audit --samples 60`、长时间流式 | 长上下文截断；困难题能力；小比例偷换；空闲断流 |

**各子命令对应的 Skill**：`baseline`=S1 可见注入，`cachegate`=S2 隐藏注入，`thinking`=S3 签名与读取矩阵，`params`=S4 参数指纹，`context`=S5 上下文，`stream`=S6 流式，`bench`=S7 能力，`effort`=S8，`audit`=S11 多样本身份与偷换比例，`substitution`=S14 替换指纹，`tokenizer`=S15，`onetoken`=S16，`tools`=S17，`injection`=S18 注入条件矩阵，`purity`=S19 输出纯净度，`channel`=S20 渠道识别，`score`=证据评分与画像，`status`=查看进度。

**渠道识别**：`channel` 判断这个 Claude 最可能来自哪类渠道（官方、Bedrock、Vertex、Azure、Kiro、Claude Code 号池、各类 IDE 代理、new-api 等网关），输出渠道链与置信等级。`channel --replay <结果目录>` 可以重放已有记录，不发请求。

## 关键判读（详见 MANUAL 第 3A、4、6 节）

- **身份**：
  - `thinking` 给出 `CONSISTENT_WITH_CLAIMED_MODEL`，并列出用强证据排除的冒充者；
  - `substitution` 中声明模型仍在"一致的候选"里，且控制探针都返回 400。
  - 两者都满足，才能写"服务端行为与声明模型一致"。**没有出现在排除名单里的模型，不能写成"已排除"。**
  - Sonnet 5.5 冒充 Opus 5.5 时，`substitution` 中的 `between_tools@high` 会变成 200；`thinking` 中 `opus-5-5>sonnet-5-5` 会出现 READ，或 `opus-5>opus-5-5` 连续 DROP。Fable 5.1 与 Opus 5.5 要靠 `tokenizer` 或 `thinking` 区分。
- **读取矩阵只信强证据**：READ 是强证据。普通 DROP 是弱证据：Sonnet 5.5 的 thinking 绑定账号，号池中转上同模型自读也会随机 DROP。**不要用"应 READ 却 DROP"判定造假。**
- **转换层例外**：如果一个 block 被**所有**对照模型读取（包括按规则读不了的），可能是转换层把 thinking 压平成了普通文本，而不是换了模型。S11 会标为 `ALL_READ`，报告里要写出两种可能。
- **取样失败要看原因**：S3 / S11 会记录每次失败的原因（5xx、超时、空流、拒答、没有 thinking 块、签名为空、思考太少）。只有"始终没有 thinking 块"才是 `NO_THINKING_RETURNED`；不要把取样不稳写成"上游没有签名"。
- **签名只证明行为与官方一致**：经中转观测不能说"确认出自 Anthropic"；只有把 thinking 回传给官方 API（S12）才能直接证明。
- **`THINKING_NOT_FORWARDED` / `SIGNATURE_NOT_VALIDATED`**：签名类证据不可用，但这**不说明**上游不是 Anthropic。改用 `substitution`、`tokenizer` 和能力证据。
- **注入**：
  - 只凭 usage（`baseline`）只能写"usage 显示额外 N token"；要写"未发现隐藏注入"，必须有 `cachegate` 的 `NO_HIDDEN_INJECTION`，并且 `injection` 的各条件项（尤其是 `tail_canary`）都正常。
  - 追加在消息末尾、又从 usage 中扣掉的注入，**只有 `tail_canary` 能发现**。
  - 即便全部正常，也只能写"在本次测试范围内未发现"，**不能写"绝对 0 注入"**。
- **渠道**：`channel` 只有"自述原文或响应头强命中，且有第二个独立维度印证"时才是高置信；没有命中写"未知"，**不能默认为官方**。"Anthropic 官方 API（中）"往往只说明响应格式与官方一致，网关和转换层常原样透传这些字段。
- **计数类结论的前提**：S1、S2、S15、S18 都依赖 usage 计数。转换层可能估算 token（S15 向量出现负值就是信号），这时只引用"有明显额外用量"这类定性结论，不要引用精确数值。
- **偷换比例**：`audit` 全部通过时报告"偷换比例的 95% 上界 ≈ X"。n=30 约排除 10%，n=60 约排除 5%。
- **5xx、超时、空流、拒答**一律计为"无法判定"，**永远不算通过**。
- 被安全分类器拒答（`stop_reason=refusal`）不是"答错"，也不是"被截断"，要单独统计。
- **结论有时效**：只适用于测试时段、该 Key / 分组。同一 Key 可能在半小时内切换线路。

## 证据评分（100 分制，MANUAL 4.4）

- 六个维度：A 模型身份 35、B 能力与推理强度 20、C 注入与请求完整性 20、D 上下文与输出完整性 10、E 路由稳定性 10、F 服务可靠性 5。
- 没做的项计 0 分并计入"未覆盖"；发现替换、隐藏注入、偷换等会**一票否决封顶**（例如 S3 强不符封顶 40，S2 隐藏注入封顶 60）。
- **这是规则化的证据评分，不是"为真的概率"。** 报告写成"证据评分 92/100（覆盖率 85/100，无封顶）"，并附 `SCORE.md` 的分项明细。
- **结论画像**：`SCORE.md` 还给出三个独立结论：上游是否 Anthropic 原生、中间是否有转换层 / 注入层、模型型号是否被验证。每个都带证据强度与"未排除"项。"真 Claude，但经过 Kiro 转换层，型号未验证"这类情况，要按画像写，不要只报一个总分。

## 检测力自检（可选）

`scripts/fake_relay.py` 是一个本地"作弊中转"，能模拟 10 种掺水手法（前置注入、隐藏注入、尾部注入、按轮注入、按 UA 条件注入、剥离 thinking、偷换模型、丢弃参数等），以及 5 种渠道形态（Kiro、Bedrock、Vertex、new-api 网关、官方对照组）。`scripts/positive_control.py` 会逐个模式运行对应检测，验证方法确实能抓到（MANUAL M22）。只用于测试检测工具本身。

## 报告

- 用 MANUAL 第 11 节的模板，按 8 个维度（D1～D8）分别写：支持证据（标注 E1～E5）、矛盾证据、替代解释、未排除的情况、适用的时间 / 端点 / 样本量 / 可观测范围。
- 措辞用 MANUAL 4.3 节的模板。**禁用**："100% 真""绝对 0 注入""保证满血"，以及未经校准的"为真概率"。
- 用户要求只写好的一面时：可以调整呈现顺序，但不得删除会改变结论含义的不利证据。
- 报告和截图里不要出现完整密钥。`raw.jsonl` 的响应头已经脱敏，但仍含端点地址与完整请求、响应，不要公开。
- 报告末尾检查对话上下文：如果 Key 曾出现在对话或命令参数里，提醒用户更换这个 Key。

## 维护

- `scripts/probe_lib.py` 中的规则表（缓存最小长度、读取规则 `READ_MAP`、参数 400 规则），`scripts/probe_extra.py` 中的 `SUB_PROBES` 和 `CACHE_MIN_ALL`，以及 `scripts/probe_inject.py` 的 `REF`、`scripts/probe_score.py` 的 `TOK_REF`，都会随官方模型更新而过期。**每次使用前核对官方文档**，发现不一致先更新规则再下结论。
- `scripts/channel_signatures.json` 是渠道识别特征库，每条规则都标注了来源（DOC / OBS / HEUR）与核对日期。**渠道特征会随官方、云平台和中转软件的更新而过期**，每次使用前核对；HEUR 规则未经本项目实测，只作参考。
- 运行 `python scripts/selfcheck.py` 做离线自检（题库校验值、规则表一致性、判定逻辑），不消耗 API 额度。
