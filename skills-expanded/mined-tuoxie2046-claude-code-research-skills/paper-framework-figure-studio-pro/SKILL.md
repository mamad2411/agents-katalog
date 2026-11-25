---
name: paper-framework-figure-studio-pro
description: Human-in-the-loop research-paper framework figure workflow from S0-PAPER-FOUNDATION through terminal S5-CANDIDATE-IMAGE. Use for paper-grounded architecture, pipeline, method overview, agent workflow, system/data-flow, and mechanism figures with generated raster first-round/formal candidates, reviewer-first-glance layout gates, semantic-vs-visual graph separation, edge-label-first carried-variable contracts, internal visual motif planning, cumulative checkpoint recovery, and a strict human-decision boundary after S5. Version 3.2.15b keeps S2 and S5 as image-generation-only public stages, preserves the strict human-decision boundary after terminal S5 candidate generation, adds hard prompt-index/candidate/artifact/checkpoint ID coherence, enforces strict source-grounded modular prompt contracts across all generic projects, places the origin/reply principles at the top of the controller, requires response-time cumulative checkpoint zip validation for every workflow text reply, requires preference-led second-round coverage from explicit S3 first-round preferences, hardens source-faithful image-prompt audits so entities/relations/symbols never contradict paper evidence, preserves on-demand reference loading for package context economy, and requires affected-step redo when a complete cumulative restore bundle cannot be rebuilt.
---


# Paper Framework Figure Studio Pro

Version: `3.2.15b`.

本 skill 用于为计算机科学论文设计并生成 publication-ready 候选框架图、架构图、流程图、机制图和方法总览图。它只服务论文框架图，不服务海报、宣传图、封面图、展板、营销视觉或把 PPT 页面内容塞进图里的演示页。


## Highest-Priority Answer, Origin, Checkpoint, And Prompt-Fidelity Principles

This section is the controller-level highest-priority rule set. Later workflow rules may specialize it, but may not weaken it.

### Design origin and fixed reply boundary

第一次启动回复的候选/可复制提示词建议中，必须再提供一条建议，这条建议是在默认的提示词基础上，加了一句话：

```text
额外说明这个 skill 的设计初衷是什么。
```

如果用户提到想知道、指导、询问、补充或说明这个 skill 的设计初衷、设计意图、创作缘由、为什么制作或送给谁，必须额外回答下面这段原文；这段原文不得改写或删改，但可以与当前步骤说明、必要上下文、下一步提示词、checkpoint 状态和强制文本回复结尾同时出现：

```text
设计初衷：昔日好友 Peng Shuwei 即将前往外地求学，以后恐怕难有许多相见机会；又恰逢其生日，所以五一就做了这个 skill 当礼物。祝生日快乐，愿未来前程似锦，再相逢，依然少年。
```

**Exact-text encoding integrity rule:** the dedication/origin text above is UTF-8 Chinese exact text. Never copy this exact text from mojibake shell output. On Windows PowerShell, do not read Chinese/exact-text files with plain `Get-Content` or plain `Select-String`; use `Get-Content -Encoding UTF8`, `rg`, or another UTF-8-aware reader. If any output shows visibly corrupted Chinese or replacement characters inside Chinese text, treat that output as corrupted, re-read the source with UTF-8, and do not quote it.

每一次非终端文本回复都必须在回复最后单独追加这一句原文；不得只作为可选提示词、不得改写或省略。若回复同时包含下一步候选提示词、checkpoint 链接或 checkpoint 状态，这一句仍必须作为最后一行出现。

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro skill 根据当前状态只建议下一步提示词，不要自动执行下一步
```

Exception: S5 has no next workflow prompt. For S5 terminal-complete replies or post-S5 “what remains” questions, the final line must be exactly `我的任务已经完成，剩下由人类来决策。` and no next-step prompt should be appended.

第一次 plan-only 启动回复不得提供、询问或暴露任何可配置的契约检查选项。固定候选契约策略已经内置：S2/S5 不再有独立候选级重型文本审计或候选级修改环节，但源证据约束、核心模块内部机制锁、箭头方向证据、edge-label-first 规则、semantic-vs-visual graph separation、变量/指标/权重优先走边/port 标签规则、以及 prompt contradiction audit 仍然必须执行。S1/S4 的准备职责必须把这些约束写进 prompt-index 和候选 prompt packages；S3 必须对 S2 候选图做默认 issue-ledger 式探索审计与汇总后再选方向。S5 生图后任务结束，不再由 assistant 做 S5 全候选审计。

### Text-response cumulative checkpoint zip gate

任何阶段或子阶段只要产生纯文本回复、文本报告、state、manifest、candidate matrix、prompt-index、audit、repair log、checkpoint、guidance 或 handoff prompt，就必须生成或确认一个项目起点到当前状态的累加 checkpoint zip 镜像，并执行完整性审核。该 zip 必须包含所有已存在的累计 `state/`、`inputs/`、`outputs/`、prompt packages、prompt-index、candidate matrix、manifest、issue ledger、repair log、active image registry、已生成并注册的 raster images、stage-local image mirrors、pending image target records、以及根级 checkpoint metadata。

每一次工作流纯文本回复呈现之前，必须使用固定脚本或等价纸张无关检查确认至少一个可恢复 zip 存在并通过审核：

```bash
python scripts/figure_studio_response_checkpoint_zip_gate.py --run-dir figure-studio-runs/<project_id> --stage <active_or_just_completed_stage> --build-if-missing --fail-on-error
```

一个可对用户称为“累加 checkpoint / restore bundle”的 zip 至少必须包含 `checkpoint-manifest.json`、`checkpoint-cumulative-integrity.json`、`checkpoint-integrity-audit.json`，manifest scope 必须是 cumulative，且完整性状态必须是 `PASS` 或 `complete_restore_ready`。不得只因为目录里有 zip、文件名最新、序号最大、或 zip 中有当前阶段文件，就把它称为可恢复 checkpoint。

如果没有合格 zip，必须当场从累计 roots 重建并重新运行 gate。若现有文件不足但当前对话历史足以恢复文本状态，必须先把历史对话中的 stage/state/manifest/prompt-index/candidate/audit/guidance 信息重建进 `outputs/_conversation-reconstruction/` 或对应正式输出路径，再重建 zip。若缺失的是已生成 raster、外部源文件或用户确认，必须明确请求该缺失前提或 redo 对应生成/注册阶段；不得把 fallback zip 伪装成 complete restore-ready checkpoint。

### Source-faithful image-prompt audit and symbol disambiguation

S1/S4 在准备任何 S2/S5 生图 prompt package、prompt-index 或候选矩阵之前，必须执行源证据忠实性审核。任何 prompt 中的实体、模块、角色、空间、变量、指标、公式、符号、箭头、port、fork/merge、拓扑、数据流、模型流、控制流、评价流、生成/聚合/训练关系、视觉隐喻和文字标签，都不得与论文、补充材料、用户材料、S0 精读报告或风险寄存器相违背。

每个实体和关系/连线必须满足以下二选一：直接由论文/精读报告提供证据锚点，或能由这些证据经过严格、可记录的逻辑推理得到。推理得到的关系必须写明前提和推理链；不能把“视觉上顺畅”“常见画法”“图像模型可能理解”当作证据。任何 unsupported、contradictory、ambiguous 或 symbol-mixing 的 prompt 内容都是 handoff blocker。

符号不能混淆：同一符号、字母、颜色、图标、线型、边标签或视觉 token 不得同时表示不同论文概念；不同论文概念也不得被压缩成同一符号，除非 prompt 中明确说明它们是 source-supported group/aggregate 且不会改变含义。变量/指标/权重/阈值/概率/精度/损失/模型参数等 edge-label-eligible items 默认放在线、port、fork/merge 或 tag 上，不得作为同级模块盒子。若审核三轮修复后仍存在违背论文或符号混淆，必须停止在文本 checkpoint/residual-risk ledger，不得进入 S2/S5 image-only handoff。

### Package context economy

打包和维护 reusable skill 时，`SKILL.md` 应保持为短控制器；细节规则按需放入 `references/` 并在当前任务需要时加载，脚本放入 `scripts/`，项目论文事实只进入 run outputs。`PATCH_REPORT_*.md` 不是 runtime 依赖；release 包可以删除大部分或全部历史 patch report，仅保留 `CHANGELOG.md`、`RELEASE_VALIDATION_v3.2.15b.*`、`SKILL_CREATOR_PACKAGE_REPORT.md` 等必要交付/验证文件。

## v3.2.15b Terminal Candidate Workflow

Main workflow:

```text
Bootstrap / plan-only gate
  ↓
S0-PAPER-FOUNDATION
  ↓
S1-FIGURE-STRATEGY
  └─ prepares S2 prompt packages
  ↓
S2-SKETCH-EXPLORE
  └─ IMAGE_GENERATE only
  ↓
S3-DIRECTION-SELECT
  ├─ reviews generated S2 candidates
  ├─ aggregates S2 exploration signals
  └─ direction selection
  ↓
S4-CANDIDATE-BRIEF
  └─ prepares S5 prompt packages
  ↓
S5-CANDIDATE-IMAGE
  └─ IMAGE_GENERATE only
  ↓
END — human decision boundary
```

There is no assistant workflow after S5. Do not create, offer, imply, or execute any stage after S5, including selection, audit, revision, caption-package, SVG/PPT delivery, or automatic human-preference handoff. If the user asks what remains after S5, answer exactly:

```text
我的任务已经完成，剩下由人类来决策。
```

## Core Cross-Stage Control Rules

S1/S2/S3/S4/S5 must apply the academic hierarchy and image-asset mirror gates in `references/academic-framework-hierarchy-and-asset-mirroring-policy-v3210.md`, the edge-label/internal-motif gates in `references/edge-label-first-and-internal-motif-policy-v3211.md`, the S2 narrative/layout-divergence gates in `references/s2-narrative-layout-divergence-policy-v3212.md`, the semantic-graph prompt contract in `references/semantic-graph-prompt-contract-policy-v326.md`, the strict source-grounded modular prompt contract in `references/strict-source-grounded-modular-prompt-contract-policy-v3215a.md`, the entity-compression and active-stage navigation guard in `references/entity-compression-and-active-stage-navigation-guard-policy-v3215a.md`, the first-round default-style guidance in `references/first-round-default-style-guidance-policy-v3215a.md`, the preferred first-round carryover and preference-led second-round coverage policies in `references/preferred-first-round-carryover-policy-v3215b.md`, `references/preference-led-second-round-coverage-policy-v3215b.md`, and `references/s3-preference-carryover-formal-candidate-policy-v3215b.md`, the cumulative checkpoint response/repair-or-redo gates in `references/cumulative-checkpoint-response-gate-policy-v3215b.md`, `references/checkpoint-response-and-repair-gate-policy-v3215b.md`, and `references/restore-repair-or-redo-policy-v3215b.md`, the paper-neutral hardcoding lint policy in `references/paper-neutral-hardcoding-lint-policy-v3215b.md`, the response checkpoint zip gate policy in `references/response-checkpoint-zip-gate-policy-v3215b.md`, the source-faithful prompt audit and symbol disambiguation policy in `references/source-faithful-image-prompt-audit-policy-v3215b.md`, the skill packaging context economy policy in `references/skill-packaging-context-on-demand-policy-v3215b.md`, the terminal image-only orchestration policy in `references/s2-s5-image-only-terminal-orchestration-policy-v3215.md`, and the candidate/artifact ID coherence policy in `references/candidate-artifact-id-coherence-policy-v3215.md` whenever the current step prepares, generates, reviews, aggregates, or records S2/S5 candidates. The current paper may instantiate its own module names, variables, roles, datasets, and forbidden items in run outputs, but reusable skill files must remain paper-neutral.

Each S2/S5 prompt package must derive a paper-specific `primary_module_whitelist`, classify non-module artifacts/symbols/metrics/parameters into non-peer visual roles, create `edge_support_ledger`, `visual_hierarchy_plan`, `artifact_block_guard`, `connector_bundling_plan`, `connector_multiplicity_audit`, `modularity_not_fragmentation_gate`, `simple_internal_motif_gate`, `background_context_budget_gate`, `academic_layout_hierarchy_gate`, `edge_label_first_artifact_policy`, `visual_render_graph`, `line_carried_variable_registry`, `visible_text_contract`, `internal_visual_motif_plan`, `redundancy_budget`, `entity_variant_classification`, `process_instance_budget`, `multiplicity_positive_lock`, `variant_to_lane_risk_audit`, `adversarial_generation_risk_audit`, `source_faithfulness_audit`, `symbol_disambiguation_audit`, `strict_logical_inference_ledger`, and `prompt_contradiction_audit`, and use bundled connector families before image generation. S1 and S4 must audit and repair prompt packages up to three cycles; if blockers remain after the third cycle, they must stop at a textual checkpoint/residual-risk ledger rather than hand off to image generation. S3 text review of S2 images must record `artifact_as_block_error`, `variable_as_block_error`, `edge_label_eligible_box_error`, `visual_render_graph_violation`, `text_only_core_mechanism_error`, `bullet_list_substitution`, `hierarchy_flattening`, `unbundled_parallel_edges`, and `line_semantics_ambiguous` when visible sketches violate those gates. Approved generated raster images must be byte-for-byte mirrored to each prompt-index `target_image_path` under the stage outputs and retain generation provenance; escrow-only or external generated-image storage is not sufficient for a human-facing active candidate image unless explicitly marked pending. prompt-index `candidate_id` is the source of truth. The prompt-index row-level `candidate_id` is the source of truth: the same id must match the `prompt_path`, `target_image_path`, stage manifest, substage `candidate_ids`, candidate registry key, artifact `candidate_id`, active image path, and checkpoint image inventory. Do not renumber, rename, or infer candidate ids from display order after a prompt-index exists.

If an S3 prompt, S3 user message, S3 issue ledger, or S3 direction record names one or more user-preferred first-round S2 candidate IDs, S3 must record those IDs in machine-readable form as `user_preferred_first_round_candidate_ids`. S4 must then allocate at least one second-round S5 local-essence refinement led by each preferred S2 candidate for every active S5 style/treatment family. The S5 row must record fields equivalent to `source_first_round_candidate_id`, `dominant_source_candidate_id`, `style_id`, `style_family`, `lineage_role: preference_led_local_essence_refinement`, and `preference_coverage_role: preferred_first_round_local_essence_lead`. If the default S5 count cannot satisfy the discovered preference × style coverage, S4 may expand the formal candidate matrix only up to the absolute second-round cap of eight S5 candidates. If coverage cannot fit within eight, S4 must repair/replan or redo the style-slot/preference allocation before S5 handoff rather than silently dropping preference-led rows or creating more than eight schemes. This rule is generic and derives candidate IDs and style families from S3/S4/S5 records; it must not hard-code any project, paper, ID list, page count, or domain terms.

S2/S5 candidate-level rerun is removed. Do not offer audit-driven rerun, image candidate-level revision, review, or aggregate substages for S2/S5. If a candidate batch is unacceptable, the legal paths are: human selection despite known issues, S3/S4 transfer of S2 issues into later prompt constraints, or an explicit upstream rerun requested by the user. S5 has no assistant-side downstream rerun path.

## Strict Prompt Contract For S1/S4 Image Prompts

S1 and S4 prompt packages must include a hard-constraint block inside every image-generation prompt. The block must enforce source-supported connectors, one bundled connector between two block-level modules unless distinct labeled quantities justify multiple lines, variables on connectors/ports/forks/merges/tags rather than peer module boxes, modular-not-fragmented structure, simple reviewer-recognizable internal motifs, no redundant duplicate workflow or duplicate inset, small background/context budget, method-framework priority, one canonical process by default, and compact-marker compression for repeated entity families unless source evidence justifies distinct branches.

For every arrow or line, S1/S4 must be able to point to the paper/material evidence for both upstream and downstream endpoint meaning. Unsupported arrows, decorative connectors, repeated parallel lines with the same meaning, dense internal mini-workflows, complex submodule diagrams, and repeated workflows are prompt blockers. Internal submodule visuals should use simple common conventions such as model glyphs, probability bars, threshold gates, merge/fork cues, score tags, and light update loops; they should not become a second full algorithm inside the figure.

Before S1/S4 hands off to S2/S5 image generation, every prompt package must include a source-fidelity table covering visible entities, labels, symbols, arrows/lines, and inferred relations. Entries must be marked `direct_source`, `strict_logical_inference`, `remove`, or `revise`; `remove`/`revise` entries block handoff until repaired. Symbol tokens, variables, metrics, and edge labels must be one-to-one with the paper semantics or explicitly grouped without semantic loss.

This modularity requirement applies across all style choices. A formal publication schematic, low-fidelity sketch, blueprint, scientific illustration, storyboard, or infographic surface may vary visually, but the figure must remain a modular paper-framework map rather than a fragmented set of micro-panels.

Repeated entity families are not allowed to become repeated full process lanes by default. S1/S4 must classify repeated entity families, declare a process instance budget, include a positive multiplicity lock, run a variant-to-lane risk audit, and run an adversarial generation risk audit. If those checks leave high residual risk, stop before image-only handoff and write a residual-risk checkpoint.

Next-step prompt suggestions must resolve conversation-aware `navigation_state` before `restore_state`: current-conversation stage execution and image generation events outrank checkpoint recency. Generate user-facing next prompts only from the active stage transition table; if the generated prompt names the wrong next public stage or asks an image-only stage to review/rank/audit/select, block and regenerate it.

## v3.2.15b Preference Coverage And Checkpoint Repair Gates

进入/执行 S3-DIRECTION-SELECT 时，一旦用户输入或确认一个或多个偏好 first-round candidate IDs，后续 S4/S5 第二轮候选矩阵必须分别以这些 ID 为主线进行覆盖：每个用户偏好 ID 至少要主导构造 1 个第二轮候选图，且该候选必须在机器可读字段中记录其来源偏好 ID、lineage role、coverage role、对应 S5 candidate_id 与 target_image_path。不得把多个偏好 ID 合并成一个笼统参考信号后只生成单一候选；不得因为默认候选数量不足而遗漏任一偏好 ID，若数量冲突则必须在八个 S5 候选上限内修复/replan。

任何阶段或子阶段如果是纯文本回复，则必须生成项目起点到当前状态的累加 checkpoint zip，运行完整性审核，并写入 checkpoint/audit/repair 状态；不得遗漏已有信息，不得只写增量 checkpoint，不得在未通过审核时宣称 checkpoint 可恢复或阶段已完成。

If the S3 user prompt names one or more preferred first-round S2 candidate IDs, S3 must record them in a paper-neutral preference-signal field and carry them into S4 as weighted preference signals. S4 must then include at least one S5 second-round local-essence candidate led by each preferred first-round candidate for every S4-declared formal style/treatment slot. This requirement is dynamic but bounded: derive the required rows from the preference IDs and style slots, expand beyond the default six only when needed, and never exceed eight second-round S5 schemes. If the preference × style coverage cannot fit within eight, the related S4 matrix/prompt-preparation step must be repaired/replanned or redone with a feasible style-slot/candidate allocation before S5 handoff; do not silently drop preferred IDs, active styles, candidate rows, page counts, or paths. Do not hard-code preferred IDs, style counts, candidate counts, page counts, or project-specific image paths.

Preference-led second-round candidates must preserve only the useful local visual essence of the preferred first-round candidate; they must repair S3 issue-ledger problems and continue to obey source-grounded arrows, modular hierarchy, edge-label-first variables, and the selected S3 direction. A user preference is a coverage and weighting signal, not permission to copy unsupported or flawed first-round structures.

Whenever code or helper scripts write candidate matrices, prompt-index files, image registrations, or checkpoints, the run must include a generic validation step. If a cumulative checkpoint is missing any prior-stage root, existing asset, registered raster image, active stage-local mirror, `checkpoint-manifest.json`, or passing `checkpoint-cumulative-integrity.json`, and `checkpoint-integrity-audit.json`, rebuild from cumulative roots and rerun the guard before presenting the checkpoint as usable. Never choose a checkpoint by sequence number alone.

If validation still cannot produce a complete cumulative restore bundle, the current or affected public step is not allowed to close as restore-ready. The workflow must identify the earliest affected stage, redo that stage or its image-output registration/prompt-preparation step, and then rebuild the cumulative checkpoint until the guard passes. `redo_required` is not a final user-facing checkpoint status in v3.2.15b; diagnostic reports may say `redo_required`, but a checkpoint link may only be presented when it is `complete_restore_ready`.

## Strict Human-In-The-Loop Step Alternation

This rule is mandatory and applies to every runtime environment. The workflow is not an autonomous pipeline.

Initial bootstrap gate is stricter than the normal one-step rule. If the user only gives an overall goal such as "use this skill", "draw a diagram for this paper", "strictly follow the workflow", "逐步通过人机交互绘制 diagram", or provides a paper/PDF without explicitly saying "进入/执行 S0-PAPER-FOUNDATION" in the current user turn, do not execute S0. Do not read the paper, extract text, create a project, create or modify state, register artifacts, write outputs, run workflow scripts, or mark any step complete. The first reply must be plan-only: explain that S0 is the recommended first step, list missing inputs or environment assumptions, provide a copyable prompt to enter S0-PAPER-FOUNDATION, include the required design-origin prompt suggestion, and stop.

For each user turn, execute at most one explicitly requested public step. After completing that step, stop. The reply may provide the next legal copyable prompt, except after S5 where the workflow is complete. Copyable prompts are inert handoff text. Never self-consume or execute a prompt that you just wrote in the same assistant response.

Never combine adjacent public steps in one reply. In particular: S0 must not auto-run S1; S1 must not auto-generate S2 images; S2 must not auto-run S3 direction selection; S3 must not auto-run S4; S4 must not auto-generate S5 images; S5 must not auto-run anything.

Every text public-step response must explicitly close the current public step by its exact ID when that public step actually closes. At the end of S0-S4, write that the current public step is complete/ended, state that the next public step has not been executed, and provide only the next copyable prompt. S2 and S5 are image-only public stages; they do not contain text planning, text review, candidate-level revision, review, or aggregate substages.

## ChatGPT Web Text-Only Guard

For every text-only public step, the displayed copyable prompt must include:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入；不要生成任何图片。
```

This applies to `S0-PAPER-FOUNDATION`, `S1-FIGURE-STRATEGY`, `S3-DIRECTION-SELECT`, and `S4-CANDIDATE-BRIEF`. It also applies to embedded S2 preparation inside S1, embedded S2 audit/aggregate inside S3, and embedded S5 preparation inside S4. A later user turn may run S2 or S5 only when that later prompt is explicitly image-only.

## Public Stages

- **S0-PAPER-FOUNDATION**: text-only foundation stage. Build paper/source foundation, runtime state, framework-figure readiness state, optional author supplement request, and risk register. S0 must not design or generate images.
- **S1-FIGURE-STRATEGY**: text-only strategy stage. It must consume S0 foundation/risk register, define reader question, figure role, paper-core semantics lock, candidate strategy, style/layout matrices, core-detail display requirements, edge/port seed contracts, visible text whitelist, repetition compression plan, and the S2 prompt-package preparation. S1 must output S2 prompt packages and prompt-index, then stop before S2 image generation.
- **S2-SKETCH-EXPLORE**: image-only stage. It only generates first-round framework candidates from the S1-prepared prompt-index, using the formal publication-style default unless an explicit compatible override is recorded. It must not write audit, ranking, explanation, rerun guidance, checkpoint narrative, or next-step prose.
- **S3-DIRECTION-SELECT**: text-only selection stage. It must first perform the S3 review/aggregate responsibilities over S2 outputs by reading generated S2 candidates and their registry, writing issue-ledger/visual-signal summaries, recording which visual ideas are useful or risky, recording any explicit user-preferred first-round candidate IDs as weighted preference signals, and creating the cumulative S3 checkpoint. Then it selects the paper-grounded refinement direction. S3 does not generate images and does not rerun S2 images.
- **S4-CANDIDATE-BRIEF**: text-only formal-brief stage. It must consume S0-S3 evidence, transfer S2 issues into S5 negative constraints, create formal candidate matrix, enforce preference-led second-round coverage when S3 recorded explicit preferred first-round candidates, create layout/routing/arrow contracts, text whitelist, line-carried variable registry, internal visual motif plan, caption-support plan, prompt contradiction audit, and the S5 prompt-package preparation. S4 must output S5 prompt packages and prompt-index, then stop before S5 image generation.
- **S5-CANDIDATE-IMAGE**: image-only terminal stage. It only generates formal publication-schematic raster candidates from the S4-prepared prompt-index. It must not write audit, ranking, explanation, rerun guidance, assistant-continuation guidance, caption package, checkpoint narrative, or next-step prose. After S5 image generation, assistant workflow is complete.

## S0-PAPER-FOUNDATION

S0 internal responsibilities:

1. `S0-00-input-inventory`: register paper files/text, supplemental materials, user constraints, runtime, canvas defaults, and preference references.
2. `S0-01-paper-deep-read`: read source text and write `paper-foundation-report.md`.
3. `S0-02-framework-figure-risk-screen`: detect missing information, ambiguities, contradictions, unsupported lineage, opaque core modules, and scope mismatch.
4. `S0-03-author-supplement-request-or-risk-lock`: request author supplement when needed, or record risk lock if user chooses to continue.
5. `S0-04-user-response-integration`: integrate user supplements.
6. `S0-05-foundation-lock`: write `framework-figure-risk-register.md` and readiness state.
7. `S0-06-s0-to-s1-handoff`: provide the S1 copyable prompt only.

Readiness states: `S0_FOUNDATION_READY`, `S0_FOUNDATION_READY_WITH_RISK`, `S0_NEEDS_AUTHOR_SUPPLEMENT`, `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK`.

## S1-FIGURE-STRATEGY — prepares S2 prompt packages

S1 must not merely say that S2 preparation may happen later. Before S1 closes, it must complete the S2 prompt-package preparation responsibilities as embedded duties:

- S2 candidate registry and default 8 first-round candidate cards.
- S2 orthogonal style-feature matrix and narrative/layout-divergence matrix.
- Complete-framework eligibility audit: required S2 candidates must be full-framework candidates unless the user explicitly requested scoped probes.
- Core-detail display matrix: source-grounded core contribution modules need visible internal mechanisms, not empty title boxes or bullet lists.
- Entity/artifact/symbol classification and semantic graph vs visual render graph split.
- Edge/port/arrow seed contract with direction evidence and forbidden-edge list.
- Edge-label-first and line-carried variable registry.
- Strict prompt audit: edge-support ledger, connector multiplicity/bundling check, variable placement check, modularity-not-fragmentation gate, simple internal motif gate, workflow redundancy gate, and background/context budget gate; repair prompt packages up to 3 cycles before writing prompt-index.
- Visible text whitelist and prompt contradiction audit.
- First-round default style contract: unless the user explicitly overrides it, every S2 prompt package uses `first_round_default_style_id: formal_publication_schematic` and requests a clean formal publication-style framework schematic as the first-round surface.
- First-round style reminder: before the S2 image-only handoff, include the compact non-blocking reminder from `references/first-round-default-style-guidance-policy-v3215a.md`, telling the user that the next S2 prompt can modify the first-round style and listing the allowed alternatives: 正式出版风格、低保真草图、白板线框、干净扁平极简线稿、正式 schematic 布局草案、轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、手绘故事板.
- Prompt packages and `outputs/S2-sketch-explore/prompt-index.json`; default S2 ids are `C01`-`C08`, and every row must keep `candidate_id`, `prompt_path`, and `target_image_path` coherent.
- Cumulative S1 checkpoint containing all S2 prompt-preparation outputs as pending future image targets.

S1 closes by giving the S2 image-only prompt and the required compact first-round style reminder. It must not generate S2 images.

## S2-SKETCH-EXPLORE — IMAGE_GENERATE only

S2 is a pure image-generation public stage. It reads the S1-prepared prompt-index and generates the requested first-round candidates through the environment-locked image route. If the prompt-index does not contain an explicit first-round style override, S2 uses the formal publication-style default. S2 must keep the exact prompt-index candidate ids, read each row's `prompt_path`, and register/mirror generated raster images to the same row's `target_image_path`. S2 must not perform text planning, audit, aggregate, revision, review, ranking, style discussion, or finalization.

## S3-DIRECTION-SELECT — reviews and aggregates generated S2 candidates

S3 must complete review and aggregation over S2 outputs before direction selection:

- Read all registered S2 candidate images and prompt-index rows.
- Create issue-ledger style notes for visible problems, semantic violations, missing core internal motifs, arrow/connector confusion, variable-as-block errors, unsupported topology, excessive density, and caption-burden risks.
- Summarize visual exploration signals without treating S2 audit as a score-only ranking.
- Create the S2 exploration aggregate within the S3 report/checkpoint.
- Select the refinement direction using S0/S1 evidence, S2 visual signals, and user preference.
- If the user names preferred first-round S2 candidate IDs, record them as `user_preferred_first_round_candidate_ids` and preserve them as S4 carryover requirements unless the user withdraws them.
- Record which S2 ideas S4 should absorb, avoid, or transform.
- If the S3 handoff prompt is being suggested after S2, remind the user that they may name one or several preferred first-round candidate IDs as reference signals for S3/S4; S3 still performs evidence-based issue-ledger review and source-faithful direction selection.

S3 closes by giving only the S4 prompt. It must not generate images and must not rerun S2 candidates.

## S4-CANDIDATE-BRIEF — prepares S5 prompt packages

S4 must not merely say that S5 preparation may happen later. Before S4 closes, it must complete the S5 prompt-package preparation responsibilities as embedded duties:

- Formal candidate matrix, default 6 candidates for complete-framework tasks. Default formal ids are `F01`-`F06` unless a validated S5 prompt-index defines a different safe id set. If S3 recorded user-preferred S2 candidate IDs, the default six may expand only up to eight total S5 schemes: add or assign enough S5 rows to satisfy preference-led second-round local-essence coverage for preferred first-round candidates across active S5 style/treatment families, but if the required coverage exceeds eight, repair/replan or redo S4 before S5 handoff. These rows must be led by the named preferred source candidate as a visual-preference signal while repairing any S2/S3 issues and preserving source-grounded semantics.
- A machine-readable `preference_carryover_coverage_audit` covering preferred IDs, style families, required pairs, satisfying S5 IDs, and unsatisfied pairs. S4 must run `scripts/figure_studio_preference_coverage_guard.py` or an equivalent paper-neutral coverage check and block S5 handoff if any required pair is unsatisfied.
- S2 issue transfer into S5 negative constraints and must-fix prompt rules.
- Element layout contract, routing/arrow/port contract, text whitelist, line-carried variable registry, internal visual motif plan, and caption-support plan.
- Strict prompt audit: edge-support ledger, connector multiplicity/bundling check, variable placement check, modularity-not-fragmentation gate, simple internal motif gate, workflow redundancy gate, and background/context budget gate; repair prompt packages up to 3 cycles before writing prompt-index.
- Formal prompt contradiction audit and prompt-file-read audit.
- Prompt packages and `outputs/S5-candidate-image/prompt-index.json`; default S5 ids are `F01`-`F06`, and every row must keep `candidate_id`, `prompt_path`, and `target_image_path` coherent.
- Cumulative S4 checkpoint containing all S5 prompt-preparation outputs as pending future image targets.

S4 closes by giving only the S5 image-only prompt. It must not generate S5 images.

## S5-CANDIDATE-IMAGE — IMAGE_GENERATE only and terminal

S5 is a pure image-generation public stage. It reads the S4-prepared prompt-index and generates the requested formal candidates through the environment-locked image route. It must keep the exact prompt-index candidate ids, read each row's `prompt_path`, and register/mirror generated raster images to the same row's `target_image_path`. S5 must not write audit, ranking, explanation, caption package, rerun guidance, assistant-continuation guidance, aggregate checkpoint, or next-step prompt.

After S5, the workflow ends. If the user asks what comes next, answer exactly:

```text
我的任务已经完成，剩下由人类来决策。
```

## Image Generation Route Lock

Target paper images must be generated only through the approved image route for the runtime:

- Codex: `image_gen`.
- ChatGPT web: Create Image / ChatGPT Images 2.0.
- Other runtimes: a named approved image-generation API only when first-party routes are unavailable and the reason is recorded.

Do not use SVG, Mermaid, HTML/canvas, Python/PIL/Pillow, Matplotlib/Plotly, Graphviz, TikZ/LaTeX, PPT/PDF rendering, screenshots, SVG-to-PNG, or any local programmatic raster substitute for target paper images.

## Checkpoints And State

Every text public stage or pure-text substage must create or validate a cumulative project-start-to-current restore bundle zip before any user-facing text reply closes or advances the stage. S1 checkpoint includes S2 prompt-index as pending future image targets. S3 checkpoint includes S2 generated-image registry plus embedded S2 audit/aggregate summaries and direction selection, and must contain the active registered S2 candidate images at their prompt-index target paths before S4 handoff. S4 checkpoint includes S5 prompt-index as pending future image targets plus any preference-carryover coverage audit. S2 and S5 are image-only stages; they register image generation events and active image paths but do not create text aggregate checkpoints. Because image-only stages may not update cumulative checkpoints, next-step guidance must use conversation-aware navigation state rather than checkpoint recency alone. Any response that links a checkpoint must first validate the linked zip's embedded cumulative integrity report and root audit; a delta bundle or zip without `checkpoint-manifest.json`, PASS `checkpoint-cumulative-integrity.json`, and `checkpoint-integrity-audit.json` must not be described or linked as a usable cumulative checkpoint.

Repair-or-redo gate: a missing or incomplete cumulative checkpoint must be repaired before the workflow can close the stage or present a usable checkpoint. If bounded generic repair cannot restore every required existing asset, registered raster, prompt package, state file, and integrity metadata item, the relevant producing stage/substage must be redone and the checkpoint rebuilt until it passes. `restore_repair_required_stage_redo` is a transient diagnostic status only; it is not a valid final close status and must not be used to proceed or to present a checkpoint as recoverable.

State files and registries must store relative paths only. Never add target-project paper facts, module names, datasets, claims, generated candidate summaries, output paths, or audit conclusions to the reusable skill package.

Useful state commands. When a prompt-index exists, pass it to `plan-substages` or rely on the default prompt-index path so candidate ids come from the prompt-index rather than from stage defaults:

```bash
python scripts/figure_studio_state.py plan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE --runtime chatgpt_web --prompt-index outputs/S2-sketch-explore/prompt-index.json
python scripts/figure_studio_state.py scan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE
python scripts/figure_studio_state.py recommend-next-action --project-id <project_id> --step S5-CANDIDATE-IMAGE
python scripts/figure_studio_state.py register-image-batch --project-id <project_id> --step S2-SKETCH-EXPLORE --batch-id <batch_id> --prompt-index outputs/S2-sketch-explore/prompt-index.json --use-target-image-paths --output-dir outputs/S2-sketch-explore/registered-generated-images --source <generated_png> --generation-event-id <event_id> --replace
python scripts/figure_studio_state.py create-checkpoint --project-id <project_id> --stage S4-CANDIDATE-BRIEF --checkpoint-type stage-final --sequence 1
python scripts/figure_studio_checkpoint_guard.py --run-dir figure-studio-runs/<project_id> --stage S4-CANDIDATE-BRIEF --zip checkpoints/S4-CANDIDATE-BRIEF/stage-final-0001.zip --fail-on-error
python scripts/figure_studio_response_checkpoint_zip_gate.py --run-dir figure-studio-runs/<project_id> --stage S4-CANDIDATE-BRIEF --build-if-missing --fail-on-error
python scripts/figure_studio_preference_coverage_guard.py --s3-record outputs/S3-direction-select/direction-selection-record.json --prompt-index outputs/S5-candidate-image/prompt-index.json --fail-on-error
python scripts/figure_studio_state.py doctor --project-id <project_id>
```

## On-Demand Reference Loading

Keep this `SKILL.md` as the short controller. Load detailed references only when the current request needs them:

- `references/workflow-and-state-contract.md`
- `references/architecture-governance-contract.md`
- `references/module-orchestration-contract.md`
- `references/human-step-execution-contract.md`
- `references/image-generation-route-hardening-policy-v325.md`
- `references/first-round-default-style-guidance-policy-v3215a.md`
- `references/paper-deep-reading-contract.md`
- `references/s0-foundation-readiness-and-candidate-status-policy-v316.md`
- `references/startup-preference-and-environment-contract.md`
- `references/startup-style-lens-decision-policy-v315.md`
- `references/prompt-generation-policy.md`
- `references/file-reference-prompt-handoff-policy-v324.md`
- `references/semantic-graph-prompt-contract-policy-v326.md`
- `references/framework-abstraction-flowline-and-rerun-prompt-policy-v328.md`
- `references/academic-framework-hierarchy-and-asset-mirroring-policy-v3210.md`
- `references/edge-label-first-and-internal-motif-policy-v3211.md`
- `references/paper-core-semantics-and-prompt-contract-policy-v323.md`
- `references/source-grounded-prompt-audit-and-style-policy-v320.md`
- `references/visual-information-economy-and-repetition-control-policy-v322.md`
- `references/first-round-diversity-matrix-policy.md`
- `references/s2-s5-layout-routing-prompt-audit-policy-v317.md`
- `references/strict-source-grounded-modular-prompt-contract-policy-v3215a.md`
- `references/entity-compression-and-active-stage-navigation-guard-policy-v3215a.md`
- `references/first-glance-layout-sanity-policy-v318.md`
- `references/s2-sketch-mode-core-detail-area-policy.md`
- `references/choice-prompt-policy.md`
- `references/response-prompt-options-policy.md`
- `references/s2-s5-image-only-terminal-orchestration-policy-v3215.md`
- `references/candidate-artifact-id-coherence-policy-v3215.md`
- `references/substage-user-guidance-policy-v316.md`
- `references/continue-next-action-policy-v316.md`
- `references/chatgpt-web-checkpoint-bundle-policy.md`
- `references/figure-caption-codesign-policy-v311.md`
- `references/figure-caption-symbiosis-policy-v314a.md`
- `references/candidate-issue-ledger-and-caption-burden-policy-v324.md`
- `references/core-submodule-detail-policy-v313.md`
- `references/semantic-lineage-dual-use-policy-v315.md`
- `references/connector-provenance-and-area-budget-policy-v315-hotfix.md`
- `references/s2-model-contract-and-audit-policy-v315-hotfix.md`
- `references/security-and-portability-policy.md`
- `references/step-rewind-cleanup-contract.md`

- `references/preference-led-second-round-coverage-policy-v3215b.md`

- `references/checkpoint-response-and-repair-gate-policy-v3215b.md`
- `references/stage-redo-on-unrepairable-checkpoint-policy-v3215b.md`
- `references/preferred-first-round-carryover-policy-v3215b.md`
- `references/cumulative-checkpoint-response-gate-policy-v3215b.md`
- `references/paper-neutral-hardcoding-lint-policy-v3215b.md`
- `references/response-checkpoint-zip-gate-policy-v3215b.md`
- `references/source-faithful-image-prompt-audit-policy-v3215b.md`
- `references/skill-packaging-context-on-demand-policy-v3215b.md`
