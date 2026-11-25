---
name: constitution
description: "用户触发 /ezfl:constitution 或 /openspec:constitution，或要求创建 / 修正 / 查看项目宪法时必须使用本 skill。管理 openspec/memory/constitution.md 的 CREATE / AMEND / SHOW 三种模式。"
---

# constitution

<HARD-GATE>
禁止在未进入显式 CREATE / AMEND 模式的情况下修改 constitution.md（不允许静默编辑）。禁止在没有用户明确确认的情况下把某条 Core Principle 标记为 (NON-NEGOTIABLE)。宪法驱动下游注入点 A/B/C/D，任何变更都会向后传导。
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: constitution — 使用 easy-flow:constitution skill。`

## Overview

宪法管理 skill。三模式：CREATE / AMEND / SHOW。与 openspec-integrated-superpowers 的宪法体系完整对齐（一字不改），仅做路径迁移与 Law #4 hook 升级。

## 三模式

| 检测条件 | 模式 |
|---------|------|
| constitution.md 不存在 | CREATE |
| 存在但含 `[ALL_CAPS_PLACEHOLDER]` | CREATE |
| 存在且无占位符 | AMEND |
| 用户传入 `show` | SHOW |

## Policies

| Policy | 文件 | 作用 |
|--------|------|------|
| CREATE | `./policies/constitution-create.md` | 引导用户填写模板 |
| AMEND | `./policies/constitution-amend.md` | 修正流程 + 版本号 + Sync Impact Report |
| Injection | `./policies/constitution-injection.md` | 四注入点(A/B/C/D)的具体逻辑 |

## 有效性判定（Law #4 升级为 MACHINE_VERIFIED）

脚本驻留 plugin 内部，由 `.harness/.cache/.plugin_root`（SessionStart 写入）定位；缺失则按"不存在"处理并提示重启会话。

```bash
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
bash "$PLUGIN_ROOT/hooks/constitution-validity.sh"
# 退出码：0=有效 / 1=无效（含未替换占位符）/ 2=不存在
```

## 配置

```toml
[constitution]
required = false  # true 时未生成有效宪法的项目阻断 propose/apply
path = "openspec/memory/constitution.md"
```
