---
name: fiction-doctor
description: |
  项目体检诊断。只读检查项目目录、文件、JSON、底本体系完整性。
  发现缺失或异常项时解释影响和修复建议，不自动修复。
  触发方式：/fiction-doctor、「体检」「诊断」「检查项目」「项目状态」「帮我看看这个项目有没有问题」「检查一下文件」。
---
# fiction-doctor：项目体检诊断

只读诊断当前项目：确认所处阶段应有的文件是否完整。

## 原则

1. 只读诊断，不写文件，不自动修复，不安装依赖
2. 先 project-status 取短状态，再 doctor 做阶段感知检查
3. 缺失项按阶段解释影响和修复建议

## 执行

```bash
export WORKSPACE_ROOT="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
# 优先使用宿主已提供的路径；仓库检出时可退回当前目录下的 scripts/。
export SCRIPTS_DIR="${SCRIPTS_DIR:-${CODEX_SCRIPTS_DIR:-${CLAUDE_SCRIPTS_DIR:-${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-.}}/scripts}}}"

# 短状态
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" project-status --format summary

# 标准体检
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" doctor --format text

# 指定章节（可选）
# python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" doctor --chapter {N} --deep
```

`doctor` 发现缺失或异常时会返回非零退出码；`--format json` 的 `ok: false` 与退出码保持一致，
可直接接入 CI 或其他自动化检查。找不到项目也视为失败，不会默默返回成功。

## 输出方式

报告包含：
- 当前项目阶段、已发现章节数和检查格式
- 是否有 blocker、缺失或异常文件路径
- state、设定集、总纲、追踪和（`--deep` 时）底本/指定章节提交的完整性
- 每个问题的影响和修复建议

不执行真实修复，不展示或要求粘贴 API key。

## 参考

各阶段的文件完整性标准：
- 开书前：.novel/state.json + 设定集/*.md + 总纲草案.md
- 开书后：上述 + .story-system/ 底本 + 大纲/ + 正文/N章.md
- 写作中：追踪/ 文件齐全、底本版本号匹配
本 skill 不重复定义各阶段清单。
如需主动修复，先运行 doctor 查看报告，再按建议执行。
`doctor` 只检查脚本实际能读取的项目结构；它不会自动修复、刷新底本或补全追踪文件。缺失项必须由用户或相应 skill 明确处理。
---
### 使用示例

```
> /fiction-doctor

体检报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
阶段：开书后（已写至第 15 章）

✅ 项目状态正常
  · .novel/state.json ✓
  · 设定集/主角卡.md ✓
  · 设定集/世界观.md ✓
  · 设定集/核心冲突.md ✓
  · 大纲/总纲.md ✓
  · 大纲/第1卷/详细大纲.md ✓
  · 正文/ 1-15 章完整 ✓
  · 追踪/伏笔.md ✓
  · 追踪/时间线.md ✓
  · .story-system/MASTER_SETTING.json ✓
  · 深度检查项按实际存在的底本/commit 文件报告

⚠️ 建议注意
  · 距上次审查已过 6 章（第 9 章后未审）
  · 追踪/上下文.md 建议归档（当前 50 条记录）

如无问题即可继续；未执行的深度检查不代表已验证。
```

```
> /fiction-doctor --deep

体检报告（深度）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
❌ 问题：缺少第 5 章的 commit 或审查报告
  影响：无法证明该章完成了对应的持久化步骤
  建议：先确认正文事实，再单独运行 chapter-commit 或 fiction-review
...
```
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。
