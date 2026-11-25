---
name: review-summary
description: 生成并保存复习会话总结。用于学习者要求总结、结束复习并保存报告，或需要更新长期学习画像时。
---

# Review Summary

生成简洁的 Markdown 会话报告，并通过 `review_summary` 保存。

`review_summary` 保存报告后，会进入当前 profile 私有 `_user/summaries/`，并更新 `_user/learning_profile.json`。总结报告要同时服务两件事：

- 给学习者阅读，帮助其理解本次复习表现。
- 给下一次 `/review` 读取，作为学习画像和复习推荐依据。

## 报告格式

```markdown
# 复习会话总结

**日期**: {日期}
**科目**: {profile/subject 名称}
**资料包**: {profile_id/subject_id}
**范围**: {复习范围}
**成绩**: {正确数}/{总题数} ({正确率}%)

## 一、总体评价

{2-4 句话，概括本次表现、稳定能力和主要风险}

## 二、逐题回顾

| # | 知识点 | 题型 | 难度 | 结果 | 核心收获 |
|---|--------|------|------|------|----------|

## 三、薄弱环节

{合并重复问题，不只罗列表面错误}

## 四、知识链

{用箭头或紧凑列表展示本次练习涉及的概念关联}

## 五、下次建议

{给出具体的下次范围、模式和难度}

## 六、学习画像更新要点

- weak_points: {薄弱知识点或能力}
- error_types: {错误类型，如概念混淆、步骤遗漏、计算错误、证明断裂、表达不清}
- lingering_questions: {仍未解决的问题}
- next_suggestions: {下次复习的具体范围、模式和难度建议}
```

## 规则

- 报告必须基于已归档题目和当前 session 状态。
- 如果没有题目被归档，不要编造成绩；可以只保存低置信度的过程性总结，或说明暂时无法生成有效学习画像。
- 当学习者要求结束本次复习时，调用 `review_summary` 并设置 `end_session: true`。
- 调用 `review_summary` 时，尽量传入 `subject_id`、`profile_id`、`session_id`、`scope`，便于工具写入当前 profile 私有 `_user/`。
- 报告必须显式包含 `weak_points`、`error_types`、`lingering_questions`、`next_suggestions`，便于工具更新 `_user/learning_profile.json`。
- 科目相关例子必须和当前 profile 一致。
