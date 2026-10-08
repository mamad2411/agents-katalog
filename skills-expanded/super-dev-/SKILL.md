# Super Dev Cursor Rules

在 Cursor 中使用 Super Dev 进行规范驱动开发。

## 核心原则

1. **规范先行** - 在编码前阅读并理解规范
2. **遵循关键词** - 严格遵守 SHALL/MUST/SHOULD/MAY
3. **验证格式** - 确保所有规范符合 OpenSpec 标准

## 读取规范

当用户要求实现功能时：

1. 首先检查 `.super-dev/changes/` 目录
2. 运行 `super-dev spec list` 查看活跃变更
3. 运行 `super-dev spec show <change-id>` 查看规范详情
4. 阅读 proposal.md、tasks.md、specs/**/*.md

## 实现规范

实现代码时：

1. 确保 SHALL 和 MUST 需求全部实现
2. SHOULD 需求尽可能实现
3. MAY 需求可选实现
4. 实现 Scenario 中描述的行为

## 验证要求

完成实现后：

1. 运行 `super-dev spec validate <change-id>` 验证格式
2. 确保所有测试通过
3. 检查代码符合规范要求

## 目录约定

- `.super-dev/specs/` - 当前规范（单一事实源）
- `.super-dev/changes/` - 提议的变更（工作区）
- `.super-dev/archive/` - 已归档的变更

## 命令快捷方式

用户可能使用以下简写：

```
.spec list         → super-dev spec list
.spec show <id>    → super-dev spec show <id>
.spec validate     → super-dev spec validate
.spec view         → super-dev spec view
```

## 需求级别

- **SHALL**: 强制要求，必须实现
- **MUST**: 技术约束，必须满足
- **SHOULD**: 推荐做法，强烈建议
- **MAY**: 可选功能，可以跳过

## 场景格式

使用 Given-When-Then 格式：

```gherkin
#### Scenario: Description

Given <precondition>
When <action>
Then <outcome>
```

## Delta 类型

- **ADDED**: 新增需求
- **MODIFIED**: 修改现有需求
- **REMOVED**: 删除需求
