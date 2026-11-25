---
name: help
description: |
  当用户请求查看某个技能的帮助信息时触发。用于显示技能的使用方法、参数说明和示例。
  触发场景：
  - 用户输入包含 `--help` 参数，如 `skill_name --help`
  - 用户明确请求查看某个技能的帮助文档
  - 用户想了解某个技能的使用方式或参数含义
  此技能通过读取目标技能的 SKILL.md 文件来提取帮助信息。
---

# Help 技能

当用户请求查看某个技能的帮助信息时使用此技能。

## 工作流程

1. **解析目标技能名称**
   - 从用户输入中提取技能名称（去掉 `--help` 后缀）
   - 技能名称可能带路径，需要处理

2. **定位技能目录**
   - 在以下位置搜索技能：
     - `~/.claude/skills/`（用户自定义技能）
     - 项目本地技能目录（如 `.omc/skills/`）
     - OMC 内置技能目录（`~/.claude/plugins/cache/claude-plugins-official/*/skills/`）
   - 技能目录结构：`{skill_name}/SKILL.md`

3. **读取并解析 SKILL.md**
   - 提取 frontmatter 中的 `name` 和 `description`
   - 查找技能的使用说明、参数定义、示例等内容

4. **格式化输出**
   - 使用清晰的格式显示帮助信息
   - 突出显示技能名称、描述、参数等关键信息

## 输出格式

推荐使用以下格式：

```
=== {技能名称} ===

描述：
{从 description 提取的完整描述}

用法：
{技能的标准调用方式}

参数：
{从 SKILL.md 中提取的参数说明}
  --param1: 参数1说明
  --param2: 参数2说明

示例：
{相关使用示例}
```

## 技能目录参考

```javascript
// 可能的技能搜索路径
const SKILL_PATHS = [
  path.join(os.homedir(), '.claude', 'skills'),
  path.join(process.cwd(), '.omc', 'skills'),
  path.join(os.homedir(), '.claude', 'plugins', 'cache', 'claude-plugins-official'),
];
```

## 错误处理

- **技能不存在**：提示用户检查技能名称是否正确，列出可用技能
- **无法读取文件**：提示权限问题或文件损坏
- **解析失败**：尽可能提取可用信息，给出部分帮助

## 显示可用技能列表

当用户没有指定具体技能时（如只输入 `help` 或 `--help`），显示所有可用技能：

```
可用技能：
  skill_name1 - 技能1的简短描述
  skill_name2 - 技能2的简短描述
  ...

输入格式：skill_name --help 查看特定技能的帮助
```
