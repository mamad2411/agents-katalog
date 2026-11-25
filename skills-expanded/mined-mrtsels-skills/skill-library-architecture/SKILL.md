---
name: skill-library-architecture
description: 整理本机 Codex、Hermes、Claude Code 技能目录时核对主库、来源副本、同名版本和引用。
metadata:
  imported_from: hermes
---

# 本机技能库架构与查重

先读当前目录、配置和 Git 状态；旧记录中的数量和架构只可作为线索。

## 当前入口

- `~/.agents/skills/` 是共享主库，按类别保存本地技能；Codex 可递归发现该目录。
- `~/.codex/skills/` 保留 Codex 专用技能；`.system/` 和插件缓存由应用维护。
- Hermes 的 `skills.external_dirs` 当前包含 `~/.agents/skills`，但 `~/.hermes/skills` 也可能存在后续新建的真实副本，必须现场盘点。
- Claude Code 的 `~/.claude/skills` 多为指向主库的符号链接；移动目标后需检查链接。
- CodeBuddy、WorkBuddy 的已安装插件以当前配置和插件声明为准；市场目录内出现技能文件不等于已启用。
- `~/.agents/skills/imported/` 按来源插件保留导入内容的相对结构；名称冲突用来源前缀区分。

## 合并流程

1. 记录当前 Git 修改和目标目录；修改已有内容前先备份。
2. 按真实路径去重，再比较入口文件、脚本、参考资料、模板和许可证。可用配套脚本 `scripts/compare_skill_stores.py` 辅助盘点。
3. 内容及配套文件相同则复用；仅有独有文件且无冲突时可补齐；同名但内容不同则保留来源版本，避免整包覆盖。
4. 只有本次请求包含清理时才删除来源副本。删除前确认所有独有文件已保存、引用已更新、目标可读取。
5. 私密技能保留在本地忽略目录；提交仅包含本次明确路径，并按当前 AGENTS.md 与隐私检查要求操作。
6. 通过 Codex 的 `skills/list` 强制重扫验证技能路径、名称和解析错误；不要依赖历史数量。

## 注意

- 名字相似不表示用途相同，例如项目开发约定和项目使用手册。
- 相对符号链接随目录深度变化，重建后逐一验证。
- 聚合包中可能同时存在入口和子技能，不能只数顶层目录。
- 当前 `.gitignore` 是明确排除规则，不能按旧的“忽略全部内容”规则操作。
