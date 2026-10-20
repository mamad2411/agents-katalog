---
name: healthcare-medical-record-analysis-team
description: 从智能病历结构化组织（病历规范化/主诉提取/病史整理/电子病历生成）与规范化入院记录撰写（三步流程/入院记录/病历格式化），病历文本辅助诊断（病历分析/实验室结果解读/系统化诊断推理/决策支持）与医疗实体提取（症状/药物/化验值/诊断实体识别），到医疗文档简化解读（检查结果解释/出院小结/处方解读/临床记录翻译）与症状分析就医建议（症状查询/科室推荐/检查项目/用药指导）的完整病历分析工作流。覆盖病历结构化、入院记录、辅助诊断、实体提取、文档解读、就医建议全链路。
---

# 病历分析

Use this skill as the routing entry point for the 病历分析 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$ai-medical-record-guide`
- `$unisound-medical-term-normalization`
- `$tencent-health-ai-clinical-assistant`
- `$medical-entity-extractor`
- `$patiently-ai`
- `$medical-advice`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
