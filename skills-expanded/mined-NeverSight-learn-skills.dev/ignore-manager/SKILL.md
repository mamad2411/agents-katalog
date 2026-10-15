---
name: ignore-manager
description: 管理 .claudeignore 和 .cursorignore 忽略规则
allowedTools:
  - Read
  - Write
  - Edit
  - Bash
---

# Ignore Manager Skill

统一管理 `.claudeignore` 和 `.cursorignore` 文件的忽略规则。

**使用场景：** 产品经理在项目中有废弃的需求文档、历史版本 PRD、大量原型图等文件，需要保留但不希望 AI 读取，避免干扰当前工作和浪费 token。

## 用户输入解析

用户会以以下格式调用此 skill：
- `/ignore-manager view` 或 `/ignore-manager 查看` - 查看当前规则
- `/ignore-manager add <path>` 或 `/ignore-manager 添加 <path>` - 添加规则
- `/ignore-manager remove <path>` 或 `/ignore-manager 删除 <path>` - 删除规则
- `/ignore-manager sync` 或 `/ignore-manager 同步` - 同步两个文件

其中 `<path>` 可以是：
- 相对路径（如 `logs/`, `*.pdf`）
- 绝对路径（需转换为相对路径，如果在项目外则提示错误）
- 用户拖拽的文件/文件夹路径

## 项目信息

- 项目根目录：使用 `pwd` 命令动态获取当前工作目录
- `.claudeignore` 路径：`<项目根目录>/.claudeignore`
- `.cursorignore` 路径：`<项目根目录>/.cursorignore`

## 执行指令

### 1. 识别命令

从用户输入中提取命令和参数：
- 命令：view/查看、add/添加、remove/删除、sync/同步
- 参数：路径或模式（如果有）

### 2. 执行对应操作

#### 查看（view/查看）

1. 读取 `.claudeignore` 文件
2. 读取 `.cursorignore` 文件（如果不存在，提示需要创建）
3. 显示两个文件的内容
4. 标注差异项（在 `.claudeignore` 中有但 `.cursorignore` 中没有的，或反之）

#### 添加（add/添加）

1. 获取要添加的路径
2. 如果是绝对路径：
   - 检查是否在项目根目录内
   - 如果在项目内，转换为相对路径
   - 如果在项目外，提示错误并停止
3. 读取 `.claudeignore`，检查规则是否已存在
4. 如果不存在，追加到文件末尾
5. 在文件头部的变更日志区域添加时间戳记录：`# YYYY-MM-DD HH:MM - Added: <path>`
6. 对 `.cursorignore` 执行相同操作（如果文件不存在，先创建）
7. 显示添加结果

#### 删除（remove/删除）

1. 获取要删除的路径
2. 读取 `.claudeignore`
3. 删除匹配的非注释行（保留注释行）
4. 在文件头部的变更日志区域添加时间戳记录：`# YYYY-MM-DD HH:MM - Removed: <path>`
5. 写回文件
6. 对 `.cursorignore` 执行相同操作
7. 显示删除结果

#### 同步（sync/同步）

1. 读取 `.claudeignore` 的所有非注释规则 → 集合 A
2. 读取 `.cursorignore` 的所有非注释规则 → 集合 B（如果文件不存在，B 为空集）
3. 合并：A ∪ B，去除重复项，保持原有顺序
4. 保留 `.claudeignore` 的注释和结构
5. 将合并后的规则写入两个文件
6. 在文件头部添加时间戳记录：`# YYYY-MM-DD HH:MM - Synced`
7. 显示同步结果

## 变更日志格式

在每个文件开头维护变更日志区域（如果不存在则创建）：

```
# ===============================
# Change Log
# ===============================
# 2026-03-12 10:18 - Added: logs/
# 2026-03-12 10:20 - Removed: drafts/
# 2026-03-12 10:25 - Synced
#
```

变更日志区域应该在文件最开头，在其他注释之前。

## 实现要点

- 使用 Read 工具读取文件
- 使用 Write 工具创建文件
- 使用 Edit 工具修改文件
- 使用 Bash 工具获取当前时间（`date +"%Y-%m-%d %H:%M"`）
- 路径处理：检查绝对路径是否以项目根目录开头
- 规则去重：比较时忽略空行和纯空格行
- 保留注释：以 `#` 开头的行视为注释
- 错误处理：文件不存在时自动创建，项目外路径提示错误

## 输出格式

操作完成后，以清晰的格式显示结果：
- 查看：分别显示两个文件的规则，标注差异
- 添加：确认已添加的规则
- 删除：确认已删除的规则
- 同步：显示合并后的规则数量和新增的规则
