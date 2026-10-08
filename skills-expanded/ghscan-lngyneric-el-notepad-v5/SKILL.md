---
source: raw/05_代码与项目/skills/skills/skills/frontend-design/SKILL.md
raw_sha256: b81e2ff87ed8fa4d6c377ccb127a7254c9e6a77e3ae94f21e6b514f7bb2945a0
compiled_at: 2026-04-14T05:05:47.239Z
---
# frontend-design 技能规范

> [!NOTE] 来源
> 原始文件路径：`raw/05_代码与项目/skills/skills/skills/frontend-design/SKILL.md`

---

## TL;DR
这是一个前端界面设计开发技能，用于创建符合要求、具备独特设计质感、避免通用AI同质化审美风格的生产级前端代码与界面，适用于网站、组件、页面、应用等各类前端需求的开发。

---

## 基础信息
| 项 | 值 |
|-----|-----|
| 技能标识 | `frontend-design` |
| 适用场景 | 用户要求构建Web组件、页面、宣传品、海报或应用时使用（示例：网站、着陆页、仪表盘、React组件、HTML/CSS布局，或对任意Web UI进行风格美化） |
| 许可证 | 完整条款见 `LICENSE.txt` |

---

## 核心设计流程要点
### 设计思考阶段（编码前）
必须先明确上下文，确定清晰明确的设计方向，核心关注：
1. **目标**：该界面解决什么问题？目标用户是谁？
2. **风格调性**：选择明确的风格方向，可选方向包括：极致简约、极繁混乱、复古未来、有机自然、奢华精致、趣味玩具风、杂志编辑风、粗野原始风、几何装饰风、柔和马卡龙、工业实用风等，无需局限于现有方向，需设计符合定位的独特风格
3. **约束条件**：技术栈要求、性能要求、无障碍要求
4. **差异化**：什么让这个设计令人难忘？最让人记住的核心特点是什么？

> [!IMPORTANT] 核心要求
> 选择清晰的概念方向并精准执行，大胆极繁和精致简约都可行，核心是「 intentionality（设计意图清晰）」而非强度。

### 编码实现要求
产出的可运行代码需要满足：
- 生产级、功能可用
- 视觉冲击力强、令人印象深刻
- 和设计风格方向保持统一
- 所有细节都经过精细打磨

---

## 前端审美规范要点
### 核心关注方向
1. **排版**：选择美观独特有风格的字体，避免Arial、Inter这类通用字体，选择能提升审美质感的独特字体，用有特点的展示字体搭配精致的正文字体
2. **色彩与主题**：保持风格统一，使用CSS变量保证一致性，主色+清晰强调色比 timid 的均匀分布调色板效果更好
3. **动效**：使用动画实现效果和微交互，HTML优先使用纯CSS方案，React优先使用Motion库；优先聚焦高影响力时刻：一个编排良好的错开展开页面加载动效，比分散的微交互更能带来愉悦感，合理使用滚动触发和惊喜感的hover状态
4. **空间构图**：使用非预期布局、不对称、重叠、对角线流动、破网格元素、充足留白/可控密度
5. **背景与视觉细节**：创造氛围和深度，不要默认使用纯色，添加符合整体风格的上下文效果和纹理，合理使用渐变网格、杂色纹理、几何图案、分层透明、戏剧性阴影、装饰边框、自定义光标、颗粒覆盖等创意形式

### 禁忌要求
1. 绝对不能使用通用AI生成审美：包括过度使用的字体家族（Inter、Roboto、Arial、系统字体）、陈词滥调的配色（尤其是白色背景上的紫色渐变）、可预测的布局和组件模式、缺乏上下文特定特征的千篇一律设计
2. 需要创意解读，做出符合上下文的非预期选择，所有设计都应该是独特的，在明暗主题、字体、风格方向上保持变化，绝对不要在多次生成中收敛到常见选择（例如Space Grotesk）
3. 实现复杂度要匹配设计愿景：极繁设计需要包含大量动画和效果的复杂代码，简约/精致设计需要克制、精准，关注间距、排版和细节细节，优雅来源于对愿景的良好执行

---

## 引用原始证据片段
> This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.
> 
> The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.
> 
> **CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.
> 
> NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.
> 
> Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

> [!WARNING] 冲突说明
> 本页无已知与其他来源的冲突，若后续发现冲突请在此处补充标注。
