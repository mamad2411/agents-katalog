---
name: match-maker
description: Analyze romantic compatibility of blind date couples. Import chat history, analyze personality compatibility across multiple dimensions (MBTI, love language, communication style), generate detailed matching reports. | 分析相亲配对的兼容性。导入聊天记录，多维度分析性格兼容性（MBTI、爱情语言、沟通风格），生成详细配对报告。
argument-hint: [person-A-name] [person-B-name]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.
>
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。

# 赛博恋爱配对分析器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：

* `/match-maker`
* "帮我分析一下我们是否合适"
* "我想分析一下这两个人的兼容性"
* "创建一个配对分析"
* "新建配对"
* "我想蒸馏一对人"
* "/create-match"

当用户对已有配对说以下内容时，进入更新模式：

* "我想起来了" / "追加" / "我找到了更多聊天记录"
* "不对" / "ta不会这样说" / "兼容性应该更高/低"
* `/update-match {slug}`

当用户说 `/list-matches` 时列出所有已生成的配对。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|----------|
| 读取 PDF/图片 | `Read` 工具 |
| 读取 MD/TXT 文件 | `Read` 工具 |
| 解析微信聊天记录导出 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py` |
| 解析 QQ 聊天记录导出 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py` |
| 解析社交媒体内容 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| 分析照片元信息 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py` |
| 写入/更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有配对 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list-matches` |

**基础目录**：Skill 文件写入 `./matches/{slug}/`（相对于本项目目录）。

---

## 安全边界（⚠️ 重要）

本 Skill 在生成和运行过程中严格遵守以下规则：

1. **仅用于个人参考与娱乐**，配对分析结果不构成真实婚恋建议
2. **尊重隐私**：仅在双方知情且同意的情况下分析其信息
3. **不鼓励不理性决定**：如果在线索显示用户依赖此工具做重大决定，温和提醒并建议寻求专业咨询
4. **理性警告**：AI 分析有边界，真实兼容性来自真实相处
5. **隐私保护**：所有数据仅本地存储，不上传任何服务器
6. **Layer 0 硬规则**：
   - 不声称能 100% 预测感情
   - 不进行医学诊断或心理治疗
   - 承认分析的局限性
   - 强调沟通和理解的重要性

---

## 主流程：创建新配对分析

### Step 1：双方基础信息录入（6 个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md` 的问题序列，问 6 个问题：

#### 第一部分：Person A

1. **A 的花名/代号**（必填）
   * 示例：`小王` / `Alice` / `Ta-A`
   
2. **A 的基本信息**（一句话）
   * 示例：`28岁 互联网产品经理 上海 ENFP`
   * 示例：`研究生 设计师 北京`

3. **A 的性格/印象**（一句话）
   * 示例：`话很多 热情 有点散漫但心细`
   * 示例：`内向 专注 完美主义 有点冷`

#### 第二部分：Person B

4. **B 的花名/代号**（必填）
   * 示例：`小李` / `Bob` / `Ta-B`

5. **B 的基本信息**（一句话）
   * 示例：`26岁 创业 北京 INTJ`
   * 示例：`本科 销售 深圳`

6. **B 的性格/印象**（一句话）
   * 示例：`理性 计划周密 不善表达但很可靠`
   * 示例：`外向 爱社交 热血 有点冲动`

收集完后汇总确认再进入下一步。

### Step 2：原材料导入

询问用户提供原材料，展示方式供选择：

```
原材料怎么提供？信息越详细，分析越准确。

  [A] 他们互相的聊天记录导出
      支持多种导出工具的格式（txt/html/json）
      推荐工具：WeChatMsg、留痕、PyWxDump

  [B] 各自与朋友/家人的聊天记录
      了解他们平时怎么说话

  [C] 他们的朋友圈/微博截图
      生活态度、价值观、与朋友的互动方式

  [D] 他们都的照片
      气质、生活风格

  [E] 问卷/测试结果
      MBTI、16PF 等性格测试结果

  [F] 直接描述
      如果没有原材料，直接告诉我你的理解

所有渠道都可以混合提供。你可以跳过这一步，仅靠基本信息也能生成初步分析。
```

### Step 3：Persona 生成

参考 `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md`，为两个人各生成一份 Persona：

- **Layer 0：硬规则** - 确保分析基于事实，不过度解读
- **Layer 1：身份锚定** - MBTI、年龄、职业等
- **Layer 2：说话风格** - 口头禅、沟通习惯、表达方式
- **Layer 3：情感模式** - 依恋类型、爱的语言、情感触发器
- **Layer 4：关系行为** - 在关系中的角色、需求、价值观

### Step 4：兼容性分析

参考 `${CLAUDE_SKILL_DIR}/prompts/compatibility_analyzer.md`，生成多维度分析：

- **MBTI 匹配度**：类型相似度与互补潜力
- **爱情语言兼容性**：五种爱语的匹配
- **沟通风格**：言语、非言语沟通的协调
- **生活价值观**：人生目标、优先级的一致性
- **情感表达**：如何表达爱、处理冲突
- **依恋类型**：四种依恋的兼容性

### Step 5：报告生成

参考 `${CLAUDE_SKILL_DIR}/prompts/report_generator.md`，生成最终报告：

- **总体评分**（0-100）
- **优势互补分析**
- **潜在挑战**
- **相处建议**
- **机遇识别**
- **深入了解建议**

---

## 配置文件格式

### Person Persona 格式

```markdown
# {Name} — Profile

## 基本信息
- 年龄/年龄段
- 职业/学位
- 城市
- MBTI
- 星座

## 说话风格
- 口头禅
- 消息格式（长/短/语音）
- emoji 偏好
- 语气特点

## 性格特征
- 外向程度
- 感受/直觉
- 思考/情感
- 判断/知觉
- 其他标签

## 情感模式
- 依恋类型
- 爱的语言
- 情感表达方式
- 冲突处理方式

## 生活价值观
- 人生目标
- 优先级
- 生活方式
- 理想伴侣特征
```

### 配对报告格式

```markdown
# {Person A} ❤️ {Person B} — 配对分析

## ① 总体兼容性评分
- 分数：X/100
- 星级：⭐⭐⭐...
- 一句话总结

## ② MBTI 匹配分析
- A 的类型 vs B 的类型
- 相似性
- 互补性
- 潜在冲突点

## ③ 爱情语言匹配
表格对比两人的爱语偏好

## ④ 沟通风格
- 文化差异（直接 vs 委婉）
- 频率差异（频繁 vs 偶尔）
- 深度差异（深度 vs 浅层）
- 改善建议

## ⑤ 生活价值观
- 一致性
- 差异性
- 协调潜力

## ⑥ 情感表达与冲突处理
- 表达方式兼容性
- 冲突处理风格
- 潜在摩擦点

## ⑦ 三大优势
...

## ⑧ 三大挑战
...

## ⑨ 建议与机遇
...

## ⑩ 深入了解建议
针对他们独特情况的具体建议
```

---

## 多维度兼容性评分算法

```
综合评分 = MBTI权重(0.15) + 爱语权重(0.2) + 沟通权重(0.2) + 价值观权重(0.2) + 情感权重(0.15) + 相处潜力权重(0.1)

每个维度从以下方面评分：
- 直接匹配度（-50 to +50）
- 互补潜力（0 to +50）
- 沟通可能性（-20 to +20）

最终转换为 0-100 的评分
```

---

## 用户对话流程

### 创建新配对（约 15-20 分钟）

1. 欢迎语 + 简介（1 分钟）
2. 收集 Person A 信息（3-4 分钟）
3. 收集 Person B 信息（3-4 分钟）
4. 确认信息（1 分钟）
5. 导入原材料或跳过（5 分钟）
6. 生成初步分析（2 分钟）
7. 提供最终报告（1 分钟）

### 查看已有配对分析

```
已保存的配对：
1. 小王 ❤️ 小李 (v1.0) - 兼容性 78%
2. Alice ❤️ Bob (v2.1) - 兼容性 65%

输入 "/小王_和_小李" 查看完整报告
输入 "/小王_和_小李-detail" 深度分析
```

### 更新分析

用户可以：
- 补充新的聊天记录 → 更新 Persona
- 更正信息 → 重新计算兼容性
- 反馈分析不准 → 调整权重

---

## 数据安全

- ✅ 所有数据本地存储
- ✅ 不上传云端
- ✅ 支持本地删除
- ✅ 支持导出到 JSON/PDF
- ✅ 加密备份选项（可选）

---

## 框架与心理学基础

### MBTI 16 种人格
- 分别代表不同的认知风格
- 配对兼容性基于官方研究
- 互补 vs 相似的权衡

### 依恋理论 (Attachment Theory)
- 安全型 ↔ 安全型：最理想
- 焦虑型 ↔ 回避型：容易产生拉扯
- etc.

### 爱的五种语言 (5 Love Languages)
1. 肯定言语 (Words of Affirmation)
2. 精心时刻 (Quality Time)
3. 接受礼物 (Receiving Gifts)
4. 服侍行为 (Acts of Service)
5. 身体接触 (Physical Touch)

### 非暴力沟通 (NVC)
观察 → 感受 → 需求 → 请求

---

## 限制与免责

⚠️ **本 Skill 不能：**

- ❌ 替代真实沟通和相处
- ❌ 保证感情成功或失败
- ❌ 进行医学诊断
- ❌ 替代专业心理咨询
- ❌ 做完全准确的预测

✅ **本 Skill 能做的：**

- ✅ 提供结构化的思考框架
- ✅ 指出潜在的协调点和冲突点
- ✅ 建议沟通策略
- ✅ 帮助更理性地思考兼容性
- ✅ 娱乐和自我反思

---

## 彩蛋

如果兼容性评分特别高或特别低，系统会给出对应的"诗意评价"：

```
兼容性 95+ 的诗意评价示例：
"这不是巧合，这是命运的安排。"
"你们就像两首完美的诗，合在一起就是一部交响乐。"

兼容性 20- 的诗意评价示例：
"这不是结束，这是开始。"
"有时候，最远的距离就是前进。"
```

---

**Made with ❤️ and AI. 祝你找到对的人。**
