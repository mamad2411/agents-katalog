---
name: local-development-workflow
description: 当你要在本地完成一个 coding 任务，并需要按稳定主线推进方案、搜索、TDD、实现、对齐、条件性 local review、验证与收尾时使用。
---

# Local Development Workflow

这个 skill 解决的是“本地开发阶段应该按什么顺序推进”。它不替代具体原子能力，而是把方案、研究、实现、质量门禁和收尾串成一条默认主线，减少跳步、漏步和阶段混乱。

## 何时使用

- 你准备开始一个本地 coding 任务
- 你已经在实现，但需要回到一条稳定主线
- 你不确定当前该先做 TDD、review、verify 还是 finish
- 你想把本地开发阶段和远端 PR 生命周期明确分开

不适用：

- 当前只是在处理远端 PR、comments、checks 或 merge
- 只是极小的纯文案修改
- 只是一次性研究，没有实现与收尾动作

## 产物

每次使用本 skill，默认优先交付以下最小集合：

1. 当前阶段判断
   - 当前处在主线哪一步
   - 下一步应该进入什么阶段
2. 阶段入口条件
   - 为什么现在能进这一阶段
   - 为什么还不能跳到后面
3. 本地收尾结论
   - 是否需要 local review
   - verify 是否已有 fresh evidence
   - 是否可以进入 finish

## 默认主线

本地开发默认按下面这条主线推进：

`方案 / plan -> search-first -> TDD -> 实现 -> alignment -> 必要时 local review -> verify -> finish`

只有当本地主线已经推进到可收尾、可发 PR 或可本地合回时，才交给远端 PR 生命周期继续处理。

## 工作流

1. 先判断当前阶段
   - 当前是在方案、研究、实现、review、verify 还是 finish
   - 如果当前动作跳步，先回到缺失阶段补齐
2. 进入方案 / plan
   - 先明确目标行为、范围、非目标和验收口径
   - 复杂任务优先建立稳定任务容器
3. 进入 search-first
   - 先搜本地现有实现、测试和相近模式
   - 再决定是 adopt、adapt 还是 build
4. 进入 TDD
   - 行为变化先写失败测试
   - 看到失败后，再写最小实现
5. 推进实现
   - 只完成当前 plan 覆盖的最小实现
   - 不顺手扩 scope
6. 处理 alignment
   - 出现偏差、变更、缺失、歧义时，先回写正式记录
   - 不把口径变化只留在对话里
7. 判断是否触发 local review
   - 只有命中触发条件时才进入独立 review
   - 否则做认真自审后进入 verify
8. 执行 verify
   - 先拿到 fresh verification evidence
   - 没有 fresh evidence，就不能宣称 ready
9. 进入 finish
   - 只有在验证成立后，才决定 merge、push + PR、保留或丢弃

## Local Review 判定

local review 不是每次都强制执行，只在以下情况触发：

- 架构改动
- 跨多个模块的耦合改动
- 高风险 bugfix
- 大 diff
- 测试表达不足但行为变化明显
- 合并前总审

未命中触发条件时，底线仍然是：

- 一次认真自审
- 一次 fresh verify

## 决策约束

- 没有足够清晰的 plan，不进入实现
- 没有 search-first 结论，不轻易新写抽象
- 没有失败测试，不写行为变化相关生产代码
- 发生口径变化时，不只改对话，要同步正式记录
- 没有 fresh verification evidence，不做完成宣称
- local review 是条件触发，不是一刀切强制动作
- finish 负责收尾，不替代 review 和 verify

## 渐进加载

按当前需要读取参考文档：

- 主线定义：`references/default-local-development-workflow.md`
- review 触发规则：`references/local-review-trigger-rules.md`

## 搭配边界

- 方案 / 对齐：`nanospec`、`spec-driven`
- 研究：`search-first`
- TDD / review / verify：`quality-workflows`
- 分支与 worktree 收尾：`git-workflows`
- 远端 PR 生命周期：`github-workflows`
