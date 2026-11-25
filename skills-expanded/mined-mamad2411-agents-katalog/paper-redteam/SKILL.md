---
name: paper-redteam
description: Simulate rigorous, fair peer review on a paper — in two modes. (A) Red-team YOUR OWN draft before submission to predict the reviews you'll get and get a fix list. (B) Review SOMEONE ELSE'S paper when you're an assigned reviewer or helping your advisor — produce a fair, venue-formatted, submission-ready review. Use whenever the user gives a paper (PDF, .tex, .md, arXiv link, or pasted text) and wants to predict reviews, find weaknesses before reviewers do, stress-test a submission, OR write a real review of another paper. Grounded in official NeurIPS/ICLR/ACL reviewer guidelines; every criticism pinned to a location, and checked against ACL's H1–H17 list of illegitimate critiques. 两种模式:审自己的稿(投稿前红队)/ 审别人的稿(当审稿人或帮导师),按会议官方标准评,绝不脑补、绝不发不正当批评。
---

# Paper Red-team & Review — rigorous, fair, evidence-bound

模拟**严谨且公正**的同行评审,两种模式:
- **Mode A — 审自己的稿(红队):** 投稿前把草稿丢进来,审稿小组把它挑一遍 → 预测评审与结局 → 给**修补清单**。终点是 `redteam/<paper-slug>.md`。
- **Mode B — 审别人的稿:** 你被指派当审稿人、或帮导师审稿时,产出一份**按会议官方表格式、公正、可直接提交**的评审。终点是 `reviews/<paper-slug>.md`。

核心信条(两种模式都别违反):
- **凡批评必有出处。** 每条 weakness 钉到具体位置(`[§x / 图y / 表z / 第n段 / "原文短引"]`),定位不到、但本该有的标 `⚠ MISSING`,绝不脑补。
- **绝不编造毛病。** 真没问题就说没问题,绝不为凑数硬挑。
- **🔥 过公正性防火墙。** 任何 weakness 提出前,先对照 `reviewing-rubric.md` 的 **H1–H17 黑名单**:命中(如"不够新颖却不给引用""没超 SOTA""方法太简单""你该多做实验 X""有局限=有缺陷")就**删除或降级为温和建议**,绝不当硬伤。这条是"严谨"与"键盘喷子"的分水岭。
- **按客观标准评。** 维度、评分量表、判据一律以 `reviewing-rubric.md` 为准(蒸馏自 NeurIPS/ICLR/ACL 官方指南),不是凭个人喜好。

## 开工前必读(三份,顺序读)
1. **`references/reviewing-rubric.md`** —— 审稿的**客观标尺**:四大维度、各会议评分量表、Reviewer 2 必查清单、**H1–H17 公正性防火墙**、好/烂评审标准。**两种模式的判据都在这。**
2. **`references/review-schema.md`** —— 产物的字段定义:单份 review 字段、weakness 三色分级、Mode A 的 meta-review + fix-list、**Mode B 的正式评审模板**、质量门。
3. **`references/reviewer-personas.md`** —— 审稿人格(R1/R2/R3·AC)盯什么、什么口吻;以及人格如何受防火墙约束。

## 第 0 步:判模式(先做这个)
看用户的话判 Mode A 还是 Mode B:
- **Mode A(审自己)**信号:"我的草稿 / 投稿前 / 帮我挑 / 会被怎么拒 / red-team my draft / before I submit"。
- **Mode B(审别人)**信号:"帮我审这篇 / 我要审稿 / 导师让我审 / 给个评审意见 / review this paper / I'm a reviewer"。
- 拿不准就**问一句**:"这是你**自己**要投的稿(我帮你提前挑),还是**别人**的论文(你要写正式评审)?"——两者口吻和产物不同,别搞反。

---

# Mode A:审自己的稿(红队)

### A1. 拿到草稿,定位骨架
用户给 PDF/.tex/.md(直接读;.tex 行号好引用)、arXiv/链接(WebFetch 取正文)、或粘贴文本。通读后定位:**Claim/卖点、Contribution、Method、Evidence(实验/baseline/ablation/统计)、Positioning、Limitations**——后面每条批评往这上面挂。
> 只拿到摘要/链接打不开/PDF 抠不出 → **先说清卡在哪**,别用半篇硬凑。

### A2. 跑审稿小组(逐人格出 review)
照 `reviewer-personas.md` 逐个出结构化 review(字段见 `review-schema.md`):R1 拥护者校准"什么是真强";R2 方法怀疑论者专攻 soundness(对照 rubric 第三节必查清单);R3·AC 卡 novelty。
**每条 weakness 都要:出处 + 三色分级 + 过 H 列防火墙。** 人格之间别互相抄,保留分歧。

### A3. AC 综合
共识 weakness(几人都点=最危险)、分歧点、决定性 2–3 条、**预测结局**(Reject/Borderline/Accept),显式标"模拟,非真实评审"。

### A4. 出修补清单(Mode A 的真正价值)
所有 weakness 去重,按**影响 × 成本**排序。每条:出处 + 谁提的 + 分级 + **怎么改** + **赶得上吗**(`✅ deadline 内 / ⏳ 需新实验 / 🛟 只能写进 limitations 缓冲`),诚实标注。

### A5. 过质量门
对照 `review-schema.md` 质量门逐条打勾(含:每条 weakness 有出处+分级?有没有假 weakness?**有没有漏过 H 列防火墙的不正当批评?**预测结局标了"模拟"?fix-list 按影响×成本排序?)。

---

# Mode B:审别人的稿(当审稿人 / 帮导师)

> 你现在是**公正的裁判**,不是对手。口吻**专业、中性、善意**,守 rubric 第五节铁律:**"写一份你自己也愿意收到的评审。"** 防火墙在这是**强制**的——绝不对作者发出 H 列不正当批评。

### B1. 确认 venue 与拿到论文
问清(或让用户说)投的是**哪个会议/期刊**——决定用哪套评分量表(NeurIPS / ARR / ICLR,见 rubric 第二节)。没说就按 NeurIPS 通用量表,并提示"换 venue 量表会变"。然后取得论文正文(同 A1)。

### B2. 通读 + 按四维度评
照 rubric 第一节四维度(Soundness / Clarity / Significance / Originality)逐项过,对 soundness 用第三节必查清单。**每一条优点和缺点都钉到出处。**

### B3. 每条 weakness 过公正性防火墙(强制)
逐条对照 H1–H17:命中就**删掉或改成"给作者的温和建议(非拒稿点)"**,并在评审里体现你是公正的。这一步让你的评审**经得起 AC 和作者的检验**。

### B4. 按官方表写出正式评审
照 `review-schema.md` 的 **Mode B 模板**产出(`reviews/<paper-slug>.md`):Paper Summary(证明读懂了)→ Strengths(带出处)→ Weaknesses(带出处+分级,均已过防火墙)→ Questions for Authors → Suggestions(可执行、非拒稿点)→ 按 venue 的评分(soundness/presentation/contribution/overall/confidence 等)+ 一句话推荐理由。
**用具体化写法**(rubric 第五节):别写"X 不清楚",写"X 的描述里缺了 Y 和 Z"。

### B5. 过质量门
对照 `review-schema.md` 质量门 + 额外两条 Mode B 专项:① 口吻是否专业中性、无挖苦?② 是否有任何 H 列不正当批评漏网?任一不过,回去改。

---

## 边界(两种模式都守)
- **不替用户改/写论文。** Mode A 产诊断,Mode B 产评审;真去动草稿是另一回事。
- **Mode B 不替用户冒充。** 产出的是**草稿评审供用户审阅定稿**,提醒用户对照论文核对每个 `[出处]`、为打分负责后再提交;评分是建议值。
- **不编实验数据。** 建议"补实验"时只说补什么、为什么,绝不编结果。
- **不保证录用 / 不替 AC 做决定。** Mode A 降低被毙风险≠保录;Mode B 给的是一份审稿意见,最终决定在 AC。
