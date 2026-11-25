---
name: higgsfield-prompt-template
description: Compile, rewrite, distill, or audit Higgsfield-style long-form cinematic AI video prompts as production-ready state machines with reference authority, identity/location/prop locks, timed or ordered shot blocks, observable acting, physical cause-and-effect, continuity handoffs, positive locks, final-frame states, audio cues, and conflict checks. Use when the user asks for Higgsfield 提示词模版, provides dense English or Chinese film prompts, reference-image tags, R2V/I2V/T2V scenes, multi-shot action or dialogue, asks to 总结规律/蒸馏提示词/写电影级提示词/优化长提示词/检查冲突/统一提示词母版, or needs a reusable director-style prompt system. Do not use it to submit paid video-generation jobs.
---

# Higgsfield 提示词模版

把故事、参考资产和现有长提示词编译成：`固定状态 → 镜头转换 → 持续不变量 → 最终状态`。先建立可验证合同，再写机器层提示词。

## 任务路由

- `audit`：用户只要求分析、总结、检查或诊断时，只输出问题、证据和修复建议，不改写全文。
- `compile`：把故事、分镜或参考资产编译成可生成提示词。
- `patch`：用户说“只改 Y”时，只重写受影响区块，并回查相邻状态交接。
- `distill`：从多个样本提炼共同结构、可复用母版、冲突规则和适用边界。
- `handoff`：用户要求 Seedance 实际生成或 API 提交时，完成提示词后转交对应生成 Skill；本 Skill 不付费、不提交。

## 必读路由

- 编写或重写长提示词前，读取 [prompt-architecture.md](references/prompt-architecture.md)。
- 审计现有提示词或修冲突时，再读取 [qa-matrix.md](references/qa-matrix.md)。
- 最终媒介是 Seedance 且内容可能超过单次生成窗口时，先读取并使用 `/Users/abo/.codex/skills/seam-first-script-compiler/SKILL.md`，按自然安全接缝划分单元；不要机械固定成 15 秒。

## 项目示例素材

- `assets/screenshots/higgsfield-hell-grind-project-overview.png`：Higgsfield 项目资产与场景组织参考。
- `assets/screenshots/higgsfield-hell-grind-about-project.png`：电影项目视觉包装参考。
- `assets/screenshots/higgsfield-character-reference-workflow.png`：人物正面、背面和脸部近景参考工作流。
- 截图仅用于理解项目组织与参考资产工作流；不要把其中人物、Logo、项目文案或受保护视觉元素复制进用户作品。
- 需要核对截图来源、尺寸和哈希时读取 `assets/screenshots/manifest.json`。

## 输入合同

提取并记录：

1. 输出模式：R2V、I2V、T2V、分镜、提示词审计或方法蒸馏。
2. 时长、画幅、帧率、生成单元上限和时间策略：`exact`、`ordered` 或 `adaptive`。
3. 人物、场景、道具、声音等参考资产，以及每个资产允许控制的字段。
4. 必须保留的剧情、台词、角色状态、空间关系和最终帧。
5. 用户禁止修改的区域和明确负面项。

低风险缺项可合理补全并声明。人物/产品身份、核心剧情、参考图映射或时长冲突会改变结果时，停止最终编译，只报最少所需输入。

## 编译工作流

1. **先审计原稿**
   - 有现成文本时先运行：

     ```bash
     python3 scripts/audit_prompt.py /path/to/prompt.txt --output-dir /path/to/audit
     ```

   - 只读取 `final_report.json`、`action_plan.json` 和异常项；需要证据时再读完整报告。

2. **声明参考权限**
   - 人物图默认只控制身份、脸、头发、肤色、服装和体型。
   - 场景图默认只控制建筑、布局、固定道具和基础光源。
   - 道具/产品图默认只控制几何、材质、颜色、数量、包装和排列。
   - 当前镜头文本控制动作、表演、相机、临时状态和时间。
   - 用户的最新文字修正明确覆盖旧描述时，写出 override；不得把两版外观混合。

3. **建立连续性圣经**
   - 人物：永久身份、当前伤势/变身/湿尘状态、服装、声音、宽景识别锚点、近景识别锚点。
   - 场景：入口/远端/左右/楼层/前中后景、光源、关键物件和禁区。
   - 道具：所有者、所在手/连接点、尺寸、材质、光学行为、重量、可变形范围和安全接触区。
   - 记录上一镜退出状态和本镜进入状态。

4. **锁定戏剧目的**
   - 每个镜头只回答一个主要视觉问题。
   - 把抽象情绪翻译为可观察链：`触发 → 眼线 → 呼吸 → 微表情 → 身体动作 → 台词/决定`。
   - 多人动作写成：`发起者 → 接收者 → 可见回应 → 空间变化 → 结束关系状态`。

5. **编译镜头**
   - 每镜填写：职责、景别、焦段感觉、机位、方向、运动、景深、初始状态、触发、动作因果、表演、结束状态、音频。
   - 默认每镜最多一个主要空间动作、一个情绪转折、一个主要相机行为。
   - 精确时间只在用户或目标模型需要时使用；否则按镜头顺序和相对节奏写。
   - 超载时在完整动作、完整台词或稳定姿态后拆分，不在动作中段硬切。

6. **编译约束层**
   - `POSITIVE LOCKS` 写唯一正确状态。
   - `CONTINUITY` 写跨镜继承状态。
   - `FINAL FRAME` 写可供下一段承接的终态。
   - `NEGATIVES` 只堵高概率身份、空间、物理、光线和风格错误。
   - 重要不变量可在正文、正向锁和负面项中各出现一次；不要无上限重复。

7. **执行 QA**
   - 重跑 `audit_prompt.py`；结构性错误必须修复。
   - 人工复核语义因果、人物关系、镜头可见性、角色参考一致性和最终帧承接。
   - 脚本 `PASS` 只代表确定性检查通过，不能代替画面语义审核。

## 默认交付

根据用户意图返回最少必要内容：

- `audit`：结论、冲突证据、优先级、affected-only 修复建议。
- `compile`：人可读镜头方案 + 可复制机器提示词 + QA 摘要。
- `patch`：修改后的区块 + 与相邻镜头的连续性复核。
- `distill`：规律、模板、适用边界、冲突清单。

用户说“只要 Prompt”时只展示最终提示词，但内部仍完成合同、连续性和 QA。

## 硬规则

- 当前文字与参考图冲突时，不静默混合两套身份；必须声明控制权或停止。
- 特殊能力必须拥有明确例外：例如磁悬浮板存在时不能使用笼统的 `No floating props`。
- 区分有意手持与 AI 缺陷：允许 organic handheld；禁止 digital jitter、flicker、warping。
- 全局规则与局部镜头冲突时，局部必须显式写 `SHOT EXCEPTION / OVERRIDE`。
- 不把 `8K`、导演姓名、IMAX、皮肤毛孔等风格词当成动作、构图或连续性替代品。
- 不承诺生成视频中的包装、文字或画作“pixel-for-pixel”；需要完全一致时标记为后期合成或独立插片。
- 不把不能同屏验证的要求假装成已锁定；例如头肩特写中画外飞板只能作为继承状态，不能算可见证据。
- 不增加用户未授权的新剧情、人物、产品功能、暴力结果或对白。
- 不提交 API、不上传、不付费、不自动重跑。

## 停止规则

以下任一情况返回 `BLOCKED`：

- 多份角色/场景参考互相冲突且没有优先级。
- 核心人物或产品必须精确匹配但资产映射缺失。
- 时长明显容纳不了所有必保留动作和对白，且无法安全拆段。
- 用户要求完全复刻文字、商标或包装，但不允许参考插片/后期方案。
- 修复需要改动用户明确锁定的非目标区块。

失败响应只包含：已确认状态、冲突证据、受影响区块和最少所需决策。
