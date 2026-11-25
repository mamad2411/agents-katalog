# SoSkill - Skill 推荐系统

## 核心能力
根据用户需求自动推荐和安装 OpenClaw Skill。

## 使用场景

### 自动触发（我会主动调用）
当用户表达以下需求时，我会自动调用 SoSkill：
- "我想..." / "如何..." / "帮我..."
- 提到具体工具名（飞书、GitHub、PPT、微信、邮件等）
- 遇到问题需要新能力
- 询问"有没有 Skill 可以..."

### 手动触发（用户明确要求）
- "推荐 Skill"
- "搜索 Skill"
- "有什么 Skill 可以帮我..."

## 工作流程

1. **提取需求关键词**
   - 从用户消息中提取核心需求
   - 示例："我想操作飞书文档" → "飞书 文档"

2. **调用推荐引擎**
   ```bash
   python3 /Users/andy/Desktop/02\ AI+产品/codex/soskill/scripts/recommend_skill.py "用户需求"
   ```

3. **展示推荐结果**
   - 默认显示前 3 个推荐
   - 显示匹配度、安装状态、描述

4. **询问是否安装**
   - 如果推荐的 Skill 未安装，询问用户是否安装
   - 用户同意后，调用 `openclaw skills install <repo>`

## 示例对话

### 示例 1：用户主动询问
```
用户: 我想操作飞书文档
助手: 🔍 推荐的 Skill:

1. feishu-create-doc ✅
   📝 创建飞书文档
   📦 https://github.com/xxx/feishu-create-doc
   🎯 匹配度: 0.95

2. feishu-fetch-doc ✅
   📝 读取飞书文档
   📦 https://github.com/xxx/feishu-fetch-doc
   🎯 匹配度: 0.92

3. feishu-update-doc ✅
   📝 更新飞书文档
   📦 https://github.com/xxx/feishu-update-doc
   🎯 匹配度: 0.90

这些 Skill 都已安装，可以直接使用。需要我帮你操作飞书文档吗？
```

### 示例 2：推荐未安装的 Skill
```
用户: 我想生成 PPT
助手: 🔍 推荐的 Skill:

1. ppt-nano-master ⬜
   📝 快速生成 PPT
   📦 https://github.com/xxx/ppt-nano-master
   🎯 匹配度: 0.88

这个 Skill 还没安装，要我帮你装上吗？
```

### 示例 3：没有匹配的 Skill
```
用户: 我想控制智能家居
助手: ❌ 没有找到匹配的 Skill

ClawHub 上可能有相关 Skill，要我帮你搜索吗？
或者你可以自己去 https://clawhub.ai 看看。
```

## 技术细节

### 推荐脚本路径
```
/Users/andy/Desktop/02 AI+产品/codex/soskill/scripts/recommend_skill.py
```

### 命令行用法
```bash
# 推荐 Skill
python3 recommend_skill.py "用户需求"

# 推荐并自动安装第一个
python3 recommend_skill.py "用户需求" --install

# 返回前 5 个推荐
python3 recommend_skill.py "用户需求" --top-k 5

# 输出 JSON 格式
python3 recommend_skill.py "用户需求" --json
```

### 安装 Skill
```bash
openclaw skills install <repo>
```

## 注意事项

1. **不要过度推荐**
   - 只在用户明确需要时推荐
   - 不要每次对话都推荐 Skill

2. **优先使用已安装的 Skill**
   - 如果已有 Skill 能解决问题，直接用
   - 不要重复推荐已安装的 Skill

3. **简洁输出**
   - 默认只显示前 3 个推荐
   - 不要输出过多信息

4. **尊重用户选择**
   - 询问是否安装，不要自动安装
   - 用户拒绝后，不要重复推荐

## 维护

### 更新 Skill 数据库
```bash
cd /Users/andy/Desktop/02\ AI+产品/codex/soskill
python3 scripts/fetch_skills.py
```

### 测试推荐引擎
```bash
python3 scripts/recommend_skill.py "飞书文档"
python3 scripts/recommend_skill.py "GitHub 操作"
python3 scripts/recommend_skill.py "生成 PPT"
```
