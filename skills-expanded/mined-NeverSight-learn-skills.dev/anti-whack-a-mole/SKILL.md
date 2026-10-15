---
name: anti-whack-a-mole
description: Use when fixing bugs to prevent introducing new ones. Activates a 6-step structured workflow (Understand → Locate → Plan → Implement → Verify → Learn) that forces global context before touching code. Trigger on "fix bug", "修复", "报错", or any debugging request.
---

# Anti Whack-A-Mole Workflow - 防打地鼠工作流

## 问题
修复一个 bug 后，又在别处冒出新 bug，反复循环

## 根本原因
1. **缺少全局视角**：只看局部代码，不了解系统全貌
2. **上下文丢失**：频繁 /clear 导致丢失关键信息
3. **无系统验证**：改完就提交，没有全面测试
4. **经验未沉淀**：同样的坑反复踩

## 解决方案：6步工作流

---

## 📋 Step 1: 理解问题（Understand）

### 🎯 目标
全面理解问题的本质，而不是表面症状

### ✅ 检查清单
```markdown
## 问题理解清单

### 1. 问题描述
- [ ] 问题的具体表现是什么？
- [ ] 在什么情况下出现？（复现步骤）
- [ ] 影响范围：哪些用户/功能受影响？

### 2. 根因分析
- [ ] 这是 Bug 还是 Feature Request？
- [ ] 从错误日志/堆栈追踪看，根本原因是？
- [ ] 是代码逻辑问题还是数据问题？

### 3. 历史背景
- [ ] 搜索 git log 查找该模块的历史修改
- [ ] 搜索相关 issue / PR
- [ ] 阅读 CLAUDE.md 了解已知问题
```

### 🤖 自动化行动
```bash
# 1. 搜索相关代码历史
grep -r "<error_keyword>" src/
git log --grep="<模块名>" --oneline -10
git log -p --follow <file_path> | head -50

# 2. 读取项目架构文档
Read CLAUDE.md
Read AGENTS.md
```

---

## 🗺️ Step 2: 全局定位（Locate）

### 🎯 目标
理解目标模块在整个系统中的位置和职责

### ✅ 检查清单
```markdown
## 全局定位清单

### 1. 架构定位
- [ ] 该模块属于哪一层？（Frontend / API / Service / Database）
- [ ] 该模块的核心职责是什么？
- [ ] 该模块在数据流中的位置？

### 2. 依赖关系分析
- [ ] 上游依赖：该模块依赖哪些模块？
  - 直接依赖：import / require 的模块
  - 间接依赖：数据库、外部 API、文件系统
- [ ] 下游依赖：哪些模块依赖该模块？
  - 使用 grep 或 LSP findReferences 搜索
- [ ] 关键数据流：数据如何流经该模块？

### 3. 影响范围评估
- [ ] 修改该模块会影响哪些功能？
- [ ] 哪些测试用例会受影响？
- [ ] 是否需要数据库迁移？
```

### 🤖 自动化行动
```bash
# 1. 查找引用
grep -r "from.*<module_name>" src/
grep -r "import.*<module_name>" src/

# 2. 查找相关测试
find . -name "*<module_name>*.test.*" -o -name "*<module_name>*.spec.*"
```

---

## 📝 Step 3: 制定计划（Plan）

### 🎯 目标
制定详细的修改计划，包括修改内容、测试策略、验证方法

### ✅ 检查清单
```markdown
## 修改计划

### 1. 代码修改清单
| 文件路径 | 修改类型 | 修改内容 | 风险等级 |
|---------|---------|---------|---------|
| app/api/xxx/route.ts | Bug Fix | 修复空值处理 | 中 |
| lib/utils.ts | Enhancement | 增加输入验证 | 低 |

### 2. 测试策略
- [ ] 需要新增的测试用例
- [ ] 需要更新的现有测试用例
- [ ] 需要运行的回归测试套件

### 3. 验证计划
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动验证：用真实场景测试

### 4. 回滚计划
- [ ] 如果测试失败，如何回滚？
```

### 🤖 自动化行动
```bash
# 使用 TaskCreate 创建任务清单
TaskCreate: "修复 <模块> <问题>"
TaskCreate: "添加测试用例：<场景>"
TaskCreate: "运行回归测试"
```

---

## 🔨 Step 4: 实施修改（Implement）

### 🎯 目标
按计划修改代码，同步编写/更新测试

### ✅ 执行顺序
```markdown
## 实施顺序

1. **先写测试**（TDD）
   - 写一个会失败的测试，证明 bug 存在
   - 写测试覆盖修复后的场景

2. **修改业务代码**
   - 按照最小改动原则修复
   - 保持代码风格一致

3. **运行测试**
   - 确保新测试通过
   - 确保所有相关测试通过

4. **代码审查自检**
   - 是否有 hardcode 的值？应该用配置
   - 是否有重复代码？应该提取函数
   - 异常处理是否完整？
   - 日志是否足够？
```

---

## ✅ Step 5: 全面验证（Verify）

### 🎯 目标
确保修改没有引入新问题，验证影响范围

### ✅ 验证金字塔
```markdown
## 多层验证清单

### Level 1: 单元测试（必须）
- [ ] 运行修改模块的所有测试
- [ ] 所有测试通过

### Level 2: 集成测试（必须）
- [ ] 运行涉及该模块的集成测试
- [ ] API 端到端测试通过

### Level 3: 回归测试（必须）
- [ ] 运行完整测试套件
- [ ] 确认无新增失败用例

### Level 4: TypeScript 类型检查（必须）
- [ ] npx tsc --noEmit 无报错

### Level 5: 手动验证（推荐）
- [ ] 在本地环境复现原问题
- [ ] 确认问题已解决
- [ ] 测试边界情况
```

### 🤖 自动化行动
```bash
# TypeScript 项目
npx tsc --noEmit
npm test -- --testPathPattern=<module>

# 完整回归
npm test
```

---

## 💾 Step 6: 记录经验（Learn）

### 🎯 目标
将本次修复写入 commit message 和 dogfood-output，避免重复踩坑

### ✅ 记录清单
在 commit message 中包含：
```
fix(<module>): <简短描述>

根因：<技术层面的根因>
解决：<做了什么改动>
教训：<如何避免再次发生>

影响范围：<受影响的功能>
```

如果是重大 bug，在 `dogfood-output/report.md` 追加记录：
```markdown
| <问题描述> | 🔴 High | <修复方案> |
```

---

## 🚨 关键原则

### ❌ 禁止的"打地鼠"行为
1. **看到 Bug 直接改代码** → 必须先理解全局
2. **改完代码就提交** → 必须运行完整测试
3. **测试失败就删测试** → 必须分析为什么失败
4. **遇到相似问题重复解决** → 先搜 git log 和 report.md

### ✅ 必须遵守的流程
1. **理解 → 定位 → 计划 → 实施 → 验证 → 记录**
2. **每个 Step 都有 Checklist**
3. **大型修改必须先 Plan Mode**

---

## 🔗 与其他 Skill 集成

- **test-guardian** — 在 Step 4 实施时调用，强制执行测试标准
- **security-auditor** — 在 Step 5 验证时调用，检查安全问题
- **dogfood** — 在 Step 5 手动验证时使用

---

## 📊 效果度量

| 指标 | 打地鼠模式 | 系统化流程 |
|------|----------|----------|
| Bug 修复引入新 Bug | 50% 概率 | < 5% 概率 |
| 测试覆盖率 | < 50% | > 80% |
| 相同问题重复出现 | 常见 | 罕见 |
