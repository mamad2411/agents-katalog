---
name: qiuzhao
description: "国内校招投递助手 / Chinese campus recruiting application assistant. 当用户要投国内校招或实习岗位、改简历、填校招表单、答开放题、记录投递进度时使用。也可用于初始化个人求职档案、经历库、投递看板。覆盖：简历 STAR 改写、JD 匹配、字节等校招系统填表、投递记录追踪。Use when a user wants help applying to Chinese campus/internship positions, tailoring a resume with STAR, filling campus recruiting forms, answering application questions, or tracking application outcomes."
---

# qiuzhao

面向国内校招生的投递工作流。

**定位：帮你把岗位理出来、判断值不值得投、把简历改到贴 JD、把表填对、把记录留下。**

**不替你搜岗位、不推荐岗位源。** 国内校招生不缺信息源（学校就业网、公众号、牛客、内推群、公司官网），AI 搜出来的岗位时效性差、准确率不可靠，用户也不会信。

**但你已经登录的招聘站，可以帮你成批读。** 打开公司官网的校招列表页，点网站自带的筛选器，把岗位和 JD 正文抓下来，按你自己的规则粗筛，再逐个读 JD 打分排序——这些是你本来就能看到的内容，只是手工做要几个小时。见 `references/job-collection.md`。

**红线不变：不绕人机验证、不点投递、不点保存。** 遇到验证码就停下来交给你。

## 核心契约

- 只做真实、可追溯、能拿到面试的投递，不做无脑海投。
- **最终提交前必须用户明确确认。预览页面不算同意。**
- 绝不编造经历、学历、日期、指标、证书。
- 初始化由 agent 主导，不是甩给用户一张问卷。

## 工作目录

**这个 skill 的源码目录只读，用户的所有档案、简历、岗位数据、看板 CSV 都写在「工作目录」里。**

工作目录 = 用户自己的求职文件夹（比如 `~/求职`），跟 skill 装在哪儿无关。所有脚本的默认工作目录按这个顺序确定：

1. 环境变量 `QIUZHAO_HOME`
2. 当前 shell 的 `pwd`

所以推荐显式设置 `QIUZHAO_HOME`，或跑脚本前先 `cd` 到用户的求职目录。文档里出现的相对路径（`./jobs-all.json`、`materials/jd/…`、`dashboard/job_pool.csv`）全部指工作目录下，不是 skill 目录下。

```
<工作目录>/                          ← 用户的真实数据，可写
  candidate_profile.json  experience_bank.md  resume_strategy.md
  answer_bank.md  application_rules.md
  jobs-all.json  scores.jsonl        ← 批量收集的中间产物
  materials/
    jd/<公司>_<岗位ID>.txt           ← JD 原文
    tailored/<公司>_<岗位ID>_<日期>.{md,json}
  dashboard/*.csv                    ← 看板数据，首次启动自动建
  scoring-batches/                   ← 并行打分的标尺和分批结果

<skill 目录>/                         ← 只读，别往里写东西
  SKILL.md  references/  templates/  scripts/  dashboard/{dashboard.html,server.js,*.example.csv}
```

看板启动脚本会**主动拒绝**把 skill 源码目录当工作目录（exit 1）。真出现「数据写进了 skill 仓库」，是用法错了，不是 gitignore 该兜。

## 快速出结果路径（单岗 / 小批）

用户第一次来、只想先看到结果，别拉着做完整初始化。按这个顺序：

1. **要一份现有简历**（PDF / Markdown / 随便什么格式）+ **问一个问题：你哪一届毕业？**（届别是红线，不能推算）
2. 从简历解析出 `candidate_profile.json`，先只填能解析的，缺的留空。
3. 用户手上有具体岗位 → 直接第 3 步读 JD，判匹配度，给结论。
   用户要成批筛 → 第 2 步抓岗位 + 打分 + 进看板。
4. **等用户看到一个有用的结论之后**，再回头补经历库的 STAR、答案库、投递规则。

判断标准：`experience_bank.md` 缺 STAR 只挡「定制简历」这一件事（第 4 步精准模式），不挡读 JD、不挡打分、不挡进看板。别把完整初始化设成所有事情的前置。

这条“快速路径”适用于单岗或小批量，不等于承诺 100+ 岗位的首次冷启动必定在 5 分钟内完成。大批量首次运行还包含新锚点、并行评分和独立盲测；模型延迟不可控，审计不通过还必须重评。**准确性门槛优先于计时：审计失败就停，不得为了卡进 5 分钟而生成看板。**

## 模式识别

用户只要其中一件事时，直接做那件，不要拉着走完整流程：

| 用户说 | 直接做 |
|---|---|
| "帮我改简历" / "这段经历怎么写" | 读 `references/resume-writing.md`，改写 |
| "按 JD 定制简历：<公司> <岗位>…"（看板按钮复制出来的指令） | 读 `references/resume-tailoring.md`，走里面的 7 步（最后一步是把定稿填进官网简历） |
| "把这个招聘网站的岗位抓下来评一遍" / "帮我筛一批岗位" | 读 `references/job-collection.md`，走三层筛选 |
| "我要投这个岗位"（给了 JD 或链接） | 从下面第 3 步开始 |
| "帮我填这个表" | 第 5 步 |
| "我投了哪些了" | 读看板，汇报 |
| "帮我配置一下" / 第一次使用 | 第 1 步 |

## 工作流

### 1. 初始化（一次性）

第一次使用时做，之后不再重复。

**目标：让用户尽可能少动手。** 让用户提供一份现有简历（PDF 或任意格式），从简历里解析出能解析的一切，只问简历里推不出来的东西。

从简历可以解析的（**不要问用户**）：姓名、手机、邮箱、学校、学历、专业、起止时间、实习经历、项目经历、获奖、证书、技能。

简历里推不出来、**必须问**的，一次性问完（编号 + 选项，不要一个个来）：

1. **届别**——你是哪一届毕业？（红线：猜错整个投递作废，不允许从入学时间推算后直接使用）
2. **投递类型**——A 校招正式 / B 校招实习 / C 日常实习
3. **目标岗位方向**——最多 3 个，按优先级
4. **目标城市**——按优先级
5. **期望薪资**——可以填"暂不确定"，遇到必填字段时再问

收齐后**一次性生成全部草稿文件**，不要每生成一个就等用户确认一次：

| 从模板 | 生成 |
|---|---|
| `templates/candidate_profile.template.json` | `candidate_profile.json` |
| `templates/experience_bank.template.md` | `experience_bank.md` |
| `templates/resume_strategy.template.md` | `resume_strategy.md` |
| `templates/answer_bank.template.md` | `answer_bank.md` |
| `templates/application_rules.template.md` | `application_rules.md` |

看板的 CSV **不用你手动复制**：第一次跑 `dashboard/start-dashboard.sh` 时，`server.js` 会自动照着同目录的 `*.example.csv` 建出空的 `dashboard/*.csv`。列的含义见 `templates/dashboard-template/README.md`。

生成后一次性把结果给用户看，让用户一次性纠正。

**经历库要写到 STAR 层**（见 `templates/experience_bank.template.md`）。简历里信息不足以填满 STAR 的部分，列出来问用户，但同样一次问完。这一步的投入是后面所有投递的复用基础——省这一步，就等于每投一个岗位都重做一遍。

详细流程见 `references/setup-workflow.md`。

### 2. 批量收集岗位（可选）

用户手上已经有具体岗位就跳过这步，直接进第 3 步。

要成批处理一个招聘站（"帮我把××的校招岗位都筛一遍"）时走这条：**先让网站砍、再让规则砍、最后才让 AI 读**。实测一个大厂校招站 7463 个岗位，网站筛选器 19 秒砍到 290，本地规则 1 秒内砍到 264，AI 只读这 264 个。

```bash
# ① 只读侦查，搞清楚这个站长什么样（不点击任何元素）
node scripts/run-with-playwright.js scripts/recon-jobs.js --url <列表页> --profile-dir <profile> --out ./recon.json
# ② 照着侦查输出写 scripts/job-sites/<站点>.json，然后点筛选器 + 抓取
node scripts/run-with-playwright.js scripts/collect-jobs.js --site scripts/job-sites/<站点>.json \
  --profile-dir <profile> --filters "产品,2027届" --pages all --out ./jobs-all.json
# ③ 硬门槛粗筛（届别、城市）
node scripts/prefilter-jobs.js --jobs ./jobs-all.json --out ./jobs-kept.json
# ④ agent 先严格评 8–10 个锚点，写 anchor-scores.jsonl；脚本确定性生成紧凑标尺。
#    不要让模型从头撰写整份 RUBRIC（慢且容易把输出格式写漂）。
node scripts/build-scoring-rubric.js --profile candidate_profile.json --experience experience_bank.md \
  --jobs scoring-batches/anchor-jobs.json --scores scoring-batches/anchor-scores.jsonl \
  --out scoring-batches/RUBRIC.md
#    岗位多时切成 8–10 批并行评分，每批立刻落盘：
node scripts/split-score-batches.js --jobs ./jobs-kept.json --out-dir scoring-batches/jobs --batches 10
node scripts/merge-scores.js --in scoring-batches/scored-*.jsonl --out ./scores.jsonl --jobs ./jobs-all.json
node scripts/audit-scores.js --sample  --scores ./scores.jsonl --jobs ./jobs-all.json --out ./audit-sample.json -n 10
node scripts/audit-scores.js --compare --scores ./scores.jsonl --rescored ./audit-rescored.json
# ⑤ 写进看板并校验
node scripts/scores-to-csv.js --scores ./scores.jsonl --jobs ./jobs-all.json --site scripts/job-sites/<站点>.json
node scripts/verify-csv.js dashboard/job_pool.csv
```

四条硬规矩：

- **绝不点投递/申请/提交/保存/收藏/删除**。`collect-jobs.js` 里有正则闸门，只点文本精确等于筛选项名的小控件。
- **遇到人机验证就停**，把浏览器交给用户手动过，不要想办法绕。
- **分母不许自己定**：抓到的数量和页面报的总数对不上，就说对不上，不许把分母改小然后宣布 100% 完成。
- **缺什么留空**：没抓到链接、没有 JD 正文，就让 `job_url`/`jd_path` 空着，看板会自动降级。不编。
- **不完整岗位默认不进待投递区**：`scores-to-csv.js` 会跳过缺链接、缺 JD、join 失败或缺评分依据的行；只有显式 `--allow-incomplete` 才保留，并标记 `Needs user`。

完整流程、站点档案怎么写、翻车了怎么查，见 `references/job-collection.md`。

### 3. 读 JD

用户给出岗位（链接、截图、或粘贴的文本）后：

- 拿到 JD 全文。链接抓不到正文时截图看（国内校招站点常见正文不是 DOM 文本直出）。
- JD 原文存到 `materials/jd/<公司>_<岗位ID>.txt`，看板里只存路径。**不要把 JD 全文塞进 CSV 单元格**——会把看板撑爆且难以阅读。
- 在 `job_pool.csv` 加一行，至少填：`date_added`、`company`、`job_title`、`job_id`、`location`、`recruit_program`（招聘项目/届别）、`source`、`job_url`、`jd_path`、`deadline`（有网申截止就填）、`status=Pending`。
- **核对届别和招聘项目**是否和用户的真实届别一致。对不上就停下告诉用户，不要投。
- 核对完把结论写进 `cohort_match_status`：`Yes` / `No` / `Unclear`。**不要留空**——看板"已确认开放，还没投"这一栏完全由这一列驱动，留空等于这个岗位在看板里消失在"状态不明"里。

### 4. 选经历 + 定简历策略

**先检查经历库**：`experience_bank.md` 不存在，或者目标方向下没有任何一段写到了 STAR 层（Action 和 Result 都是空的 / 只有一句角色描述），就**停在这里**，告诉用户缺什么、回到第 1 步补，不要往下走。

原因：从"我在小红书做过 AI 搜索"这种角色范围推不出简历 bullet——按 `references/resume-writing.md` 的证据分级，它连 C1 都不到。硬往下走的结果只有两个：要么编，要么产出一堆"负责 XX 相关工作"的废话。先分析 JD 再发现没料，等于白烧一轮。

经历库到位后：

- 从 `experience_bank.md` 的矩阵取目标方向的候选池，**读这个 JD** 挑 2-4 段最贴的。
- **告诉用户选了哪几段、为什么**（短列表 + 一句话理由）。这是硬性检查点，不是可选步骤。
- 判一次匹配度，**四档结论和百分制分数都要写**（两者并存不替换：档位用来筛，分数用来在同一档里排序）。详见下面的「匹配度怎么打分」。`勉强` 和 `不建议` 要说清楚是哪一条不匹配，让用户自己决定，不要替用户否决。
- 定模式：批量（用现有主简历）还是精准（针对这个 JD 改简历）。
- **精准模式走 `references/resume-tailoring.md` 的 7 步**：JD 拆成带编号的条目 → 经历库覆盖矩阵 → 重挑 2-4 段 → 逐条重新压缩并标注对应 JD 哪一条 → 出 diff 式改动清单（含「仍然存在的缺口」和「需要你确认的事实」）→ 用户确认后落盘 `materials/tailored/<公司>_<岗位ID>_<日期>.{md,json}`（`.md` 给人看，`.json` 给填表器用，格式见 `templates/tailored_resume.template.json`）→ **用 `scripts/tailor-to-autofill.js` 把定稿转成填表数据，接第 5 步自动填进官网简历**。单条 bullet 具体怎么措辞、证据怎么分级，仍看 `references/resume-writing.md`。
- **定制不产生新事实。** 能动的只有「挑哪几段、什么顺序、什么措辞、哪段详略」；经历本身、数字、时间、职责范围一个字不能改。没有 JD 原文就别做定制——只靠岗位名猜出来的不叫定制。
- **只交付内容，不代做排版。** 改好的简历以文本成稿给用户（Markdown 或直接在对话里），说明改了哪几条、为什么。**不要代替用户导出 PDF**——排版翻车（撑成两页、字体替换、中文标点变形）你看不见，代做等于把风险转嫁给用户还没人复核。贴回源文件、导出、检查排版这三步由用户自己做。
- **公司限投 1-2 个岗位时，必须先告诉用户再让用户决定投哪个**——不要替用户消耗投递名额。

#### 匹配度怎么打分

先过**硬门槛**：届别对不上、城市不在用户的目标城市里——直接出局，**不打分、不进池子**。硬门槛是一票否决，不折算成扣分，否则一个致命问题会被其他维度的高分稀释掉。

过了门槛的岗位打 100 分，拆成三个维度：

| 维度 | 满分 | 看什么 |
|---|---|---|
| 职责匹配 | 50 | JD 的"工作职责"逐条 vs 经历库里的具体事情 |
| 领域匹配 | 25 | 业务领域 / 产品形态是否同题（如都是 AI Agent、都是电商营销） |
| 任职要求匹配 | 25 | 专业、技能、经历年限等硬性条件 |

专业和学历**放在任职要求里扣分，不做一票否决**——校招卡专业的写法往往比实际执行严格。

三列一起写进 `job_pool.csv`：

| 列 | 例子 | 说明 |
|---|---|---|
| `match_score` | `91` | 三维之和，0–100 的整数 |
| `match_breakdown` | `职责47/50 领域24/25 任职20/25` | 分数怎么来的，加总必须等于 `match_score` |
| `match_basis` | `JD职责3字面写「社群运营Agent」↔ 个人项目同题` | **必须能指回 JD 原文的具体某一条** |

`match_basis` 是这套分数唯一的可信度来源。写不出"JD 第几条 ↔ 哪段经历"，就说明这个分是拍的——宁可标注存疑，也不要给一个看起来精确的数字。JD 正文过短（不足一两百字）时在 `match_basis` 里注明置信度低。

**岗位挂的"职能"标签不可信**：名字叫产品经理、实际在招数据分析或项目管理的岗位很常见。以 JD 正文为准，判定不一致时打低分并在 `match_basis` 里标出来。

`match_level` 与分数的对应，以及 `priority`、`status` 的推导：

| `match_score` | `match_level` | `priority` | `status` |
|---|---|---|---|
| ≥ 85 | `强匹配` | `P0` | `Pending` |
| 80–84 | `可以投` | `P1` | `Pending` |
| 70–79 | `可以投` | `P2` | `Pending` |
| 60–69 | `勉强` | `P3` | `Skipped` |
| < 60 | `不建议` | `P3` | `Skipped` |

`Skipped` 的行要在 `skip_reason` 里写清楚是分数没过线，用户随时可以自己捞回来——**分数是排序建议，不是替用户做的决定**。

没评过分就把 `match_score` 留空，**不要填 0**。看板会把它显示成"未评估"并单独统计；填 0 会让它在排序里等同于"评过且极差"。

**这套规则是默认值，不是定论。** 三个维度的权重（50/25/25）、四档的分数线、硬门槛只放届别和城市——这些是一个人跑 264 个岗位试出来的一组参数，换个方向、换个阶段就该换。用户要调权重、加硬门槛、改分档线，照改，改完把新规则写进 `application_rules.md`，让后面每一轮都按同一套标准评。**唯一不能松的是 `match_basis` 必须指回 JD 原文的具体某一条**——权重可以谈，可追溯不能谈。

**并行打分时（几十上百个岗位派多个 worker 分批评）**，上面这张表远远不够。实测 205 个岗位 / 4 个 worker、只给规则不给样本，结果分数全挤在 88–93 的 6 分带里，抽 10 个盲测重打 **10/10 高估、平均 +15.6 分、最大 +32**，排序彻底失效。原因是权重锚不住尺度——"职责匹配 47/50"到底该给多少，只有看过已定分的真实样本才对得齐。

所以并行必须走三件套，缺一不可：

1. **主 agent 先建统一标尺** —— 严格评 **8–10 个锚点岗位**写成 `anchor-scores.jsonl`（覆盖高中低分段，含标题陷阱和 70 分以下例子），再用 `build-scoring-rubric.js` 确定性生成 `RUBRIC.md`，发给每个 worker 全文。
2. **并行派 worker，分批不重叠** —— 各写自己的 `scored-<n>.json`，然后 `merge-scores.js` 合并 + 尺度体检（加总/重复/超分是致命错误直接退出；带宽塌缩、批次均值差是警告，还会点出是哪个 worker 飘了）。
3. **盲测审计，不可省** —— `audit-scores.js --sample` 分层抽 10 个，输出**剥掉全部分数字段**，主 agent 重打后 `--compare` 算偏差。平均绝对偏差 >3、任一岗位绝对偏差 >8、或系统性同向偏差超限，都要整批重评；正负误差不能互相抵消。把审计结果当新锚点写回 RUBRIC。

细节和命令见 `references/job-collection.md` 第 4 步。

### 5. 填表

读 `references/application-playbook.md`。投字节的话再读 `references/bytedance-campus.md`（已实测的字段图谱和填写配方）。

**刚在第 4 步定制完简历、要把定稿填进官网账号简历**——这是最常见的入口，走这条：

```bash
# ① 离线校验（不开浏览器，几毫秒。红线拦截 + 字段校验 + 按站点档案预演填写计划）
node scripts/tailor-to-autofill.js --tailored ./materials/tailored/<公司>_<岗位ID>_<日期>.json --dry-run
# ② 生成填表数据
node scripts/tailor-to-autofill.js --tailored ./materials/tailored/<公司>_<岗位ID>_<日期>.json --out ./my-materials/autofill_data.json
# ③ 填进页面（首次需要用户自己登录；脚本永不点保存）
node scripts/run-with-playwright.js --data ./my-materials/autofill_data.json \
     --profile ./scripts/profiles/bytedance-campus.json \
     --url https://jobs.bytedance.com/campus/resume/edit --append
```

第 ① 步必跑。它会**直接拒绝**任何证件号（含 18 位身份证形状的值）、**整块跳过**教育经历、并在缺字段/日期格式错/不是时间倒序时报错且完全不产出文件。详见 `references/resume-tailoring.md` 第 7 步。

**要填的是同一张长表上十几到几十个纯文本字段**（典型场景：第一次把账号简历录完整），先看 `references/autofill-script.md` —— 用 `scripts/autofill-core.js` 批量填，实测 35 字段 13.5 秒，比逐字段填快两个数量级。三五个字段、或者一堆下拉/多选/上传，还是走下面的手工路径。

国内校招的结构特点：**简历是账号级存档的，每个岗位通常只剩 1-3 个开放题**。所以：

- **动手之前先扫一遍 `never_guess`**：对着这个岗位要填的表，把清单上缺答案的字段一次性列出来问用户，**不要填到一半卡住再问一次、再卡住再问一次**。缺的字段问不到就直接记 `需要用户` + `blocker`，不要开始填。
- 先检查账号简历是否已完整。缺什么补什么，不要每次重走完整录入。
- 批量填。增删条目一定让 ref 失效，`fill` 通常不会（实测一次 inspect 连打 13 个 fill 没失效）但**不保证**，所以顺序是**先把「添加」点够 → 一次 inspect → 连续填一屏 → 滚动 → 再 inspect**，不要填一段快照一次。详见 playbook 的「效率规则」。
- **复核靠回读，不靠肉眼看截图**，且必须在 blur + 强制重渲染之后读。
- `candidate_profile.json` 里有明确值的直接填。
- 开放题用 `answer_bank.md` 的已确认答案；没有就起草，让用户确认一次，之后复用。
- **`never_guess` 清单上的字段一律停下来问**：届别、身份证号、学历层次、教育经历起止时间、预计毕业时间、期望薪资、服从调剂、三方协议、政治面貌类身份字段。
- 表单自动带出来的、简历和 profile 里没有依据的内容（比如账号里存的旧自我介绍），**先核实再让它进入提交**。

遇到验证码、人机验证、登录、2FA、付款、权限弹窗、不清楚的法律/身份问题——**停下交给用户**，不要绕。

### 6. 预览 → 用户确认 → 提交

提交前给用户一份摘要：公司、岗位、招聘项目/届别、简历版本、选中的经历、关键开放题答案、薪资数字。

**用户明确说提交才能点最终提交按钮。预览页面不算同意。**

提交后要看到**真实确认证据**才算成功：成功文案、跳转成功页、或**应聘记录页出现了这条投递**（国内系统最可靠的证据）。收藏、保存草稿、表单看起来填完了——都不算。

### 7. 回写

每次投递尝试都要落到一个状态：

- `已投递`：看到了确认证据
- `跳过`：不投，写原因
- `阻塞`：自动化走不下去，写卡点和下一步
- `需要用户`：缺高影响事实、需要用户过验证码/登录/上传、或需要用户做判断
- `待处理`：值得投，但要等前置条件

同时更新：

- `job_pool` 状态
- `application_log`：简历版本、用了哪几段经历、关键答案、确认证据、JD 路径
- `follow_up`：已知的下一步（笔试、面试时间）
- `daily_dashboard`：汇总

**还要回写 profile**：填表过程中冒出来的、`candidate_profile.json` 里没有的事实（新的实习细节、更新的成绩、用户当场说的偏好），写回 profile，不要让它只存在于这一次投递里。遇到模板没覆盖的新表单字段，确认用户的真实答案后写进 profile 的 `扩展字段`。

### 8. 从阻塞中学习

每轮结束后总结卡点，把重复出现的问题变成规则：下拉框处理、地址匹配、简历上传检查、登录态检查、特定公司系统的坑——写进 `references/application-playbook.md` 对应的公司小节和 `automation_rules`。

新公司系统实测后，按 playbook 里的模板补一节。**只写实测过的，不要凭印象写。**

## 看板

`dashboard/` 下是 CSV + 一个本地网页看板。启动：

```
./dashboard/start-dashboard.sh
```

**不要直接双击 `dashboard.html`**——它要从本地服务读 CSV，直接打开会因为浏览器的文件访问限制读不到数据。

## 安全边界

涉及自动化限制、验证码、登录、隐私、公开分享、仓库里不该放什么时，读 `references/safety-and-boundaries.md`。

不要把私人简历、手机号、邮箱、身份证号、住址、投递记录、浏览器会话、cookie、验证码写进公开仓库。
