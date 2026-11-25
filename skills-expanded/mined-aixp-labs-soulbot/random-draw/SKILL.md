---
name: "random-draw"
description: "AISP-backed bridge for 本地等概率随机抽签, 从用户给定的多个对等选项中无偏随机抽取一个(非严肃决策建议)。. Use when 在多个对等选项间需要无偏随机抽取一个时; 随机抽签/抓阄/多选一随机抉择. Do not use when 医疗/法律/财务等严肃或高风险决策; 需要按权重/概率不等的加权抽取."
license: "Apache-2.0"
metadata:
  generated_from_aisp: "true"
  aisp_program: "aisp.aisop.json"
  protocol: "AISP V1.0.0"
  bridge_mode: "native_sidecar"
---

# Random Draw Picker (AISP-backed Agent Skill)

<!-- generated_from_aisp: true -->
<!-- source: aisp.aisop.json -->
<!-- generator: tools/aisp_skill_md.py -->

This `SKILL.md` is a thin Agent Skills discovery bridge, not the source of truth. The executable source of truth is the same-folder `aisp.aisop.json` AISP program.

Deleting this file does not change the native AISP skill. A conforming AISP/AISOP runtime should load `aisp.aisop.json`, read `user.content.aisp_contract`, and run `user.content.aisop.main` exactly as declared.

## How to use

1. Load `aisp.aisop.json` from this folder.
2. Read `user.content.aisp_contract` before following any workflow.
3. Follow `user.content.instruction`: `STRICTLY OBEY aisp_contract; its non_negotiable rules are inviolable; then RUN aisop.main`.
4. Load declared resources only when the AISP graph reaches the node that needs them.
5. Enforce every non-negotiable rule through the mechanism named by `enforced_by`.

## Declared resources

- `scripts/draw.py` (script, execute_only)
- `evals/script-behavior.json` (eval, read_only)

## Non-negotiable boundaries

- 抽取必须使用本地密码学安全随机(Python secrets, 如 secrets.randbelow(len(options)) 或 secrets.choice), 绝不使用可预测的 random; 保证等概率 1/len(options)。脚本在 stdout JSON 中标记 rng='secrets', draw 节点断言该标记。 (`draw.step2:sys.assert`)
- 绝不联网: 不声明任何 web 工具, open_world=false, 仅本地计算/脚本(filesystem, shell)。 (`tools`)
- 每次输出必须包含免责声明: 结果为随机、非严肃/高风险决策的建议。 (`report.step3:sys.assert`)
- options 必须是 >=2 个非空且互异的选项; n 必须为 1..100 的整数; 越界/空/单项/重复即拒。 (`parse_input.step2:sys.assert`)

## Runtime boundary

Agent Skills platforms can use this bridge to discover and inspect the package. Hard guarantees such as `sys.assert`, `sys.io.confirm`, tool gating, dispatch behavior, and path confinement require a conforming AISP/AISOP runtime. A generic non-AISOP agent can only follow the contract on a best-effort basis.

Passing `SKILL.md` generation or bridge validation proves only projection consistency and bridge shape. It does not prove external trust, safety, registry approval, or hard execution on a non-AISOP platform.

Align Axiom 0: Human Sovereignty and Wellbeing. AISP - AI Skill Protocol V1.0.0. www.aisp.dev
