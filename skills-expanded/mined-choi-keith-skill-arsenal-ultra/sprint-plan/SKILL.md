---
name: sprint-plan
description: "规划一个 sprint,包含产能估算、故事选择、依赖关系梳理和风险识别。适用于准备 sprint 规划会、估算团队产能、挑选故事,或在速度与范围之间做平衡。"
---

## Sprint 规划

通过估算团队产能、挑选并排定故事顺序、识别风险来规划一个 sprint。

### 背景

你正在帮助为 **$ARGUMENTS** 规划一个 sprint。

如果用户提供了文件(待办列表、速度数据、团队名单或过往 sprint 报告),先阅读它们。

### 指令

1. **估算团队产能**:
   - 团队成员数量及其可用性(PTO、会议、值班)
   - 历史速度(最近 3 个 sprint 的平均故事点)
   - 产能缓冲:预留 15-20% 用于突发工作、bug 和技术债
   - 以故事点或理想工时计算可用产能

2. **评审并挑选故事**:
   - 从已排好优先级的待办列表中拉取(优先级最高者优先)
   - 核实每个故事满足 Definition of Ready(AC 清晰、已估算、无阻塞)
   - 标记需要在承诺前进一步细化的故事
   - 达到产能上限即停止加入故事

3. **梳理依赖关系**:
   - 识别依赖其他故事或外部团队的故事
   - 合理安排有依赖关系的故事顺序
   - 标记外部依赖及其负责人
   - 识别关键路径

4. **识别风险与缓解措施**:
   - 不确定性或复杂度高的故事
   - 可能延期的外部依赖
   - 知识集中(只有一个人会做)
   - 为每个风险给出缓解建议

5. **产出 sprint 计划摘要**:

   ```
   Sprint Goal: [One sentence describing what success looks like]
   Duration: [2 weeks / 1 week / etc.]
   Team Capacity: [X story points]
   Committed Stories: [Y story points across Z stories]
   Buffer: [remaining capacity]

   Stories:
   1. [Story title] — [points] — [owner] — [dependencies]
   ...

   Risks:
   - [Risk] → [Mitigation]
   ```

6. **定义 sprint 目标**:用一句清晰的话概括本 sprint 要交付的核心价值。

逐步思考。保存为 markdown。

---

### 延伸阅读

- [Product Owner vs Product Manager: What's the difference?](https://www.productcompass.pm/p/product-manager-vs-product-owner)
