---
name: nuwa-writers-integration
description: 女娲作家Skill集成 — 从GitHub克隆17位华语作家创作思维技能，安装为Hermes技能并放入学习池。适用于公众号文章风格切换、多智能体内容创作。
version: 1.0.0
type: skill
---

# 女娲作家Skill集成

## 概述
通过「女娲蒸馏法」从 GitHub 仓库 [momozi1996/awesome-ai-persona-skills](https://github.com/momozi1996/awesome-ai-persona-skills) 获取17位华语顶级作家的创作思维技能。

## 安装步骤

### 1. 克隆仓库
```bash
# GitHub直连超时，使用代理
git clone --depth 1 https://gh-proxy.com/github.com/momozi1996/awesome-ai-persona-skills.git /tmp/awesome-ai-persona-skills
```

### 2. 安装为Hermes技能
```bash
mkdir -p ~/.hermes/skills/nuwa-writers/references
for dir in /tmp/awesome-ai-persona-skills/Novelists/*-skill; do
    name=$(basename "$dir")
    writer_name="${name%-skill}"
    mkdir -p ~/.hermes/skills/nuwa-writers/"$writer_name"/references
    cp "$dir/SKILL.md" ~/.hermes/skills/nuwa-writers/"$writer_name"/SKILL.md
    [ -d "$dir/references" ] && cp -r "$dir/references/"* ~/.hermes/skills/nuwa-writers/"$writer_name"/references/ 2>/dev/null
done
```

### 3. 放入学习池
```bash
mkdir -p ~/Desktop/JiNeng_ZhiShiKu/学习池/女娲作家Skill
cp -r ~/.hermes/skills/nuwa-writers ~/Desktop/JiNeng_ZhiShiKu/学习池/女娲作家Skill/
```

## 17位作家
刘慈欣、余华、莫言、张爱玲、琼瑶、鲁迅、老舍、三毛、李白华、当年明月、南派三叔、木香同休、施蛰存、天下霸唱、天下 Bachang、李碧华、天马尘

## 实战记录（2026-06-23）
- 首次实战：17位作家各写一篇《一个手机配件店的十年》，主题统一但风格迥异
- 部署方式：17路并行delegate_task，每路独立子智能体
## 注意事项
- 子智能体超时问题：delegate_task默认600s超时，大批量并行时部分任务可能超时
- 解决方案：设置timeout=300或分批派遣（每批5-6个）
- 超时重试：超时后重新dispatch，通常第二次能完成

## 技能文件结构
每个作家skill包含：SKILL.md（身份卡+心智模型+决策启发式+表达DNA）+ 6个references文件（著作/对话/表达DNA/他者视角/决策/时间线）。SKILL.md是核心，包含风格迁移所需的全部指令。

## Pitfalls
- **批量并行超时**：delegate_task默认600s超时，17路并行时约20%会超时。解决方案：设置timeout=300或分批派遣（每批5-6个）。超时后重新dispatch通常能完成。
- **风格适配**：某些作家风格（如琼瑶言情）与商业主题天然冲突，需要在prompt中明确"用风格写现实题材"而非"写成该作家的故事"。
- **输出检查**：黄金原则——跑完批量没检查输出内容=没跑。每篇完成后必须抽样检查字数、风格一致性、公众号适配度。

## 公众号写作适用场景
- 刘慈欣：科技产品深度解读、行业趋势推演
- 余华：创业故事、人生感悟、接地气内容
- 莫言：乡土题材、地方文化、故事化叙事
- 张爱玲：都市生活、消费文化、精致文案
- 琼瑶：情感故事、品牌情怀
- 鲁迅：深度评论、行业痛点分析
- 当年明月：历史科普、商业案例分析
- 南派三叔：悬念式开头、故事化营销

## 批量写作任务派发模式

### 适用场景
同一主题、多种风格的批量内容生成（如17位作家各写一篇同一主题的文章）

### 正确做法
1. 创建统一输出目录：`mkdir -p ~/Desktop/输出目录/`
2. 分批派遣子智能体（每批5-6个，避免600s超时）
3. 设置 `timeout=300` 减少等待时间
4. 每个子智能体的prompt必须包含：
   - 完整主题信息
   - 店铺/品牌基本信息
   - 作家风格要点（精简版，不需要加载完整SKILL.md）
   - 输出格式要求（纯Markdown、字数范围）
5. 完成后统一移动文件到输出目录并按序号命名
6. 抽样检查每篇质量（字数、风格一致性、公众号适配度）

### 错误做法
- 一次性dispatch所有任务不设timeout
- prompt中只说"用XXX风格写"而不给具体风格要点
- 不检查输出直接发布