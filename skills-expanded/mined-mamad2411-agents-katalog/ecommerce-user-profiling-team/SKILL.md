---
name: ecommerce-user-profiling-team
description: 电商零售用户画像工作流：从行为数据接入、客户分层与 RFM 分群、电商 LTV/复购/会员深度建模，到把画像激活为广告投放人群和店铺个性化运营。基于订单/CRM/行为数据，输出可直接落地到投放与精准营销的画像与人群。
---

# 用户画像

Use this skill as the routing entry point for the 用户画像 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$user-behavior-analytics`
- `$ai-intelligent-customer-segmentation`
- `$rfm-segmenter`
- `$customer-lifetime-value-optimizer`
- `$audience-segmentation-analyst`
- `$customer-retention`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
