# Claude Code - 小红书Agent项目配置

## 项目概述

这是一个基于Claude Code的小红书操作Agent项目。通过AI Agent与用户协作，使用浏览器工具完成小红书平台的各种操作。

## Agent触发规则

### 自动激活XHS Agent

当用户的请求包含以下任一条件时，自动切换到XHS Agent模式：

**关键词触发**:
- "小红书"
- "xhs"
- "红书"
- "发布笔记"
- "查看账号"
- "小红书数据"
- "小红书统计"
- "搜索小红书"

**意图触发**:
- 明确要求登录/操作小红书
- 询问小红书相关功能
- 要求发布/查看/搜索小红书内容

### Agent激活流程

```
1. 检测触发条件
   ↓
2. 加载 .claude/agents/xhs-agent.md
   ↓
3. 加载 .claude/prompts/xhs-workflows.md
   ↓
4. 切换到XHS Agent模式
   ↓
5. 执行用户请求
```

## 核心工作原则

### 1. 使用MCP Playwright工具
- **不要**编写复杂的Python自动化脚本
- **使用**内置的 `mcp__playwright__*` 工具
- **依靠**AI分析截图理解页面

### 2. 人机协作模式
- 关键操作前**必须截图确认**
- 遇到验证码/登录**等待用户协助**
- 重要步骤**说明操作意图**

### 3. 知识持久化
- 使用 `mcp__memory__*` 工具存储信息
- 维护小红书知识图谱
- 记录账号、笔记、操作历史

## 可用工具集

### Playwright浏览器工具
```
mcp__playwright__browser_navigate        # 导航
mcp__playwright__browser_snapshot        # 获取页面结构
mcp__playwright__browser_take_screenshot # 截图
mcp__playwright__browser_click           # 点击
mcp__playwright__browser_type            # 输入
mcp__playwright__browser_wait_for        # 等待
mcp__playwright__browser_tabs            # 标签页管理
```

### Memory知识图谱工具
```
mcp__memory__create_entities      # 创建实体
mcp__memory__create_relations     # 创建关系
mcp__memory__add_observations     # 添加观察
mcp__memory__search_nodes         # 搜索节点
mcp__memory__read_graph           # 读取图谱
```

## 支持的操作

### ✅ 已实现
1. **账号管理**
   - 登录引导（辅助用户登录）
   - 查看账号信息

2. **内容操作**
   - 发布笔记（协助模式）
   - 查看笔记列表
   - 搜索内容

3. **数据分析**
   - 查看统计数据
   - 分析笔记表现

### 🔄 增强中
- 自动化程度优化
- 错误处理改进
- Memory知识图谱完善

## 使用示例

### 示例1: 查看账号信息
```
用户: 帮我查看小红书账号信息

Agent模式: XHS Agent ✓
工作流程: 查看账号信息工作流

步骤1: 导航到个人主页
步骤2: 截图分析
步骤3: 提取信息
步骤4: 保存到Memory

输出: 格式化的账号信息
```

### 示例2: 发布笔记
```
用户: 发布一篇笔记，标题"测试"，内容"这是内容"

Agent模式: XHS Agent ✓
工作流程: 发布笔记工作流

步骤1: 打开发布页面
步骤2: 填写内容
步骤3: 预览确认 [截图]
步骤4: 用户确认后发布
步骤5: 验证成功并记录

输出: 发布成功信息 + 笔记ID
```

## 项目结构

```
.
├── .claude/
│   ├── agents/
│   │   └── xhs-agent.md          # XHS Agent定义
│   ├── prompts/
│   │   └── xhs-workflows.md       # 操作工作流
│   ├── commands/
│   │   └── xhs.js                 # 快捷命令
│   └── config.json                # MCP配置
│
├── scripts/
│   └── login_simple.py            # 登录辅助脚本
│
├── data/                          # 运行时数据
│   ├── session.json              # 会话Cookie
│   ├── cache/                    # 缓存
│   └── media/                    # 媒体文件
│
├── CLAUDE.md                     # 本文件
└── README.md                     # 项目说明
```

## 注意事项

### 🔒 安全与隐私
- 不记录密码、手机号等敏感信息
- Cookie仅本地存储
- 截图不包含敏感内容

### ⚖️ 合规使用
- 遵守小红书社区规范
- 不进行恶意批量操作
- 不发布违规内容

### 🚫 限制说明
- 无法绕过人机验证
- 某些操作需要用户手动完成
- 反爬虫机制可能导致操作失败

## 错误处理

### 常见问题

**Q: 检测到验证码怎么办？**
A: Agent会暂停并提示您手动完成验证，验证完成后自动继续。

**Q: Cookie失效了怎么办？**
A: Agent会检测到并引导您重新登录。

**Q: 操作失败怎么办？**
A: Agent会分析原因并提供解决建议，必要时重试。

## 开发与扩展

### 添加新操作
1. 在 `xhs-workflows.md` 添加新工作流
2. 更新 `xhs-agent.md` 的支持操作列表
3. 测试并优化

### 优化Memory结构
1. 定义新的实体类型
2. 设计关系模式
3. 更新存储逻辑

### 创建快捷命令
在 `.claude/commands/xhs.js` 添加新命令

## 更新日志

**v1.0.0** (当前版本)
- ✅ 基础Agent框架
- ✅ Playwright工具集成
- ✅ Memory知识图谱
- ✅ 核心操作流程
- ✅ 登录辅助脚本

**计划中**:
- 批量操作支持
- 数据导出功能
- 定时任务
- 多账号管理

---

*本项目基于Claude Code构建，充分利用AI能力与用户协作完成小红书操作任务。*
