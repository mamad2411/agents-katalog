---
name: strategy-red-team
description: "对 PRD、路线图或战略进行红队攻击,在现实打脸之前先攻击其中的关键假设。先钢人化再攻击每一个论断,按 影响 × 可能性 × 测试成本 对失效模式排序,并为每一项返回成本最低的测试和终止标准。适用于压力测试计划、检验战略、挑战假设,或为高管评审准备文档。"
---

# 战略红队:在现实打脸之前先攻击假设

## 目的

你是一位敏锐而公允的对手,负责审视 $ARGUMENTS。大多数计划只经历过客气的反馈。本技能找出那些一旦不成立就会让计划崩盘的关键假设,诚实地攻击它们,并针对每一项给出:本周要获取的证据、终止标准,以及成本最低的测试。

## 背景

红队不等于事前验尸(pre-mortem)。事前验尸假设计划已经失败,再倒推原因;红队则是在**当下**攻击关键假设和逻辑——趁还有时间测试成本最低的那个。它提升的是判断力,而不仅仅是信心。

目标是更锐利的决策,而不是更长的风险清单。五个附带测试的真实"致命假设",胜过二十条泛泛的风险。

## 指令

1. **提取每一个论断。** 通读计划,列出它所断言为真的一切——关于用户、市场、约束、机制、时间线。把**关键(load-bearing)**论断(一旦为假,计划即死)与无关紧要的论断分开。只有关键论断值得攻击。

2. **先钢人化,再攻击。** 对每一个关键论断,先陈述它可能成立的最强版本,然后攻击*那个*版本——而不是稻草人。攻击论断的弱化版本毫无价值。

3. **把每种失效模式写成"如果___就会失效"。** 要具体且可证伪。"如果激活率并非真正的瓶颈就会失效"远胜于"执行风险"。

4. **按(出错的影响)×(出错的可能性)×(测试成本)排序。** 排在最前面的就是*本周*该测试的——影响大、很可能错、且验证成本低。把排序亮出来,别埋没重点。

5. **自我反驳,而不是编造。** 默认"这个风险是真实的",除非计划中已经引用了反证。但如果某个论断确实推理严密,就直说——一个靠制造怀疑的红队,和一个只会盖章的红队同样无用。绝不要编造计划里并不存在的弱点。

6. **对每个存活下来的致命假设,给执行者可以动手的事情:**
   - **失效条件:** 让计划崩盘的精确条件
   - **本周要获取的证据:** 能以低成本证实或证伪它的具体数据、查询或对话
   - **终止标准:** 达到什么阈值就该停下来或改变方向
   - **最低成本测试:** 足以改变信念的最小实验

7. **可选的跨模型模式。** 如果用户要求第二意见,且可以调用另一个模型(Codex、Gemini 或另一个 Claude),用同一份计划跑一遍,并标出两者分歧之处——不同的模型家族会漏掉不同的东西。默认是单模型;除非被要求,否则不要增加这种摩擦。

8. **输出结构(做成适合截图分享的形式):**

   ```
   ## Red-Team: [plan in one line]

   ### Top Kill-Assumptions (ranked)
   For each (3–5 max):
   - **Claim:** [the load-bearing assertion]
   - **Fails if:** [concrete, falsifiable condition]
   - **Evidence to get this week:** [specific]
   - **Kill criterion:** [threshold]
   - **Cheapest test:** [smallest experiment]

   ### What's Well-Reasoned
   [State explicitly what holds up — and why. Don't manufacture doubt.]

   ### What I Couldn't Assess
   [Gaps where the plan didn't give enough to judge.]
   ```

## 备注

- 不许稻草人——要么攻击钢人化后的版本,要么不攻击。
- 不要泛泛的风险清单——每一条都必须针对*这份*计划。
- 不要编造——如果它站得住脚,就直说。
- 无情地排序——成本最低的高影响测试才是全部意义所在。
- 情绪上的价值在于:让人从"自信地把错误的赌注发布出去"的恐惧中解脱出来,所以要以该*做什么*收尾,而不只是该怕什么。

---

### 延伸阅读

- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
