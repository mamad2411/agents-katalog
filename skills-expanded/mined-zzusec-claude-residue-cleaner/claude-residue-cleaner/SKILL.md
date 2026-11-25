---
name: claude-residue-cleaner
description: |
  审计并清除 Claude Code（Anthropic CLI）在本机与 git 仓库里留下的追踪数据：
  设备标识（userID / machineID / anonymousId）、1P 遥测队列、Keychain OAuth 凭据、
  会话 transcript、shell 与编辑器历史、统一日志、浏览器 OAuth 记录、git 提交署名与
  .claude/ 路径对象，以及「只存在于远端的分支」里的同类残留。
  当用户说「清除 claude 残留 / 清理 Claude Code 指纹 / 重置 claude 设备 ID /
  彻底删除 claude 相关数据 / claude 隐私清理 / 删掉仓库里的 Co-Authored-By: Claude」，
  或者需要一份「本机还有哪些 Claude 痕迹」的只读体检报告时使用。
  也覆盖常见误区：硬件指纹（它根本不采集）、force-push 清不干净的部分、
  以及清 `~/.claude` 会连带搞坏用户自有守护进程的风险。
---

# claude-residue-cleaner

一套「先审计、后清理、再验证」的 Claude Code 指纹处理流程。核心原则：
**只读审计优先 → 备份先于删除 → 用可证伪的计数验证 → 用户自有资产绝不误伤**。

## 何时用

- 用户要清理 Claude Code 的追踪数据 / 指纹 / 设备 ID；
- 用户要删掉 git 历史里的 `Co-Authored-By: Claude` 或 `.claude/`、`CLAUDE.md`；
- 用户问「本机还有哪些 claude 残留」，需要一份体检报告；
- 用户提到「改 MAC 地址 / 硬件指纹能不能重置」—— 先纠正（见下）。

## 铁律（务必先读）

1. **先备份，且备份失败即中止。** 任何不可逆操作前都要有可验证的备份
   （文件用 `tar`/`cp -p`，仓库用 `git bundle create -C <repo> ... --all` 并 `git bundle verify`）。
2. **默认 dry-run。** 删除前先跑 `--dry-run`，把将删除的清单念给用户确认。
3. **不要删用户自有资产。** 名字里带 Claude 的自研项目（例如 `my-claude-proxy`、
   `MyClaudeTool`、某个 `claude-*` 工具、以及同名缓存/偏好目录）用 `CLAUDE_CLEANER_PROTECT` 保护，报告里标 `· 受保护`。
4. **先查反向依赖。** 删配置目录前 `grep -rl "<CONFIG_DIR>" ~/Library/LaunchAgents /etc/cron* ~/.config`，
   否则会连带搞坏用户自己的 daemon（真实案例：一个每日备份 daemon 的脚本就住在 `~/.claude/scripts/`）。
5. **用计数验证，不用渲染后的列表。** 输出可能被压缩/过滤；判断「有/没有」一律
   `... | wc -l`，并同时检查退出码（区分「没命中」和「命令没跑」）。
6. **不碰硬件指纹。** Claude Code 不采集 MAC / 序列号 / CPU / 磁盘 ID，`machineID` 是随机 UUID。
   改 MAC 只会打乱用户的代理/防火墙配置。要如实告诉用户这一点。

## 标准流程

```bash
cd <repo>/scripts

# ① 体检（只读，不改任何东西）—— 永远从这一步开始
CLAUDE_CLEANER_PROTECT='<用户自有项目正则>' bash audit.sh

# ② 本机清理：先看，后删
bash clean.sh --dry-run --level 4
bash clean.sh --level 4            # 只重置标识+历史+账号关联，保留配置
# 需要连配置一起清（先自动备份）：bash clean.sh --level 5 --nuke

# ③ 系统层（需要 root；会清空本机全部统一日志，先说明代价）
sudo bash sudo-clean.sh

# ④ 仓库层：默认只扫描
bash git-strip-claude.sh --owner <GitHub 用户名>
bash git-strip-claude.sh --owner <GitHub 用户名> --apply --push [--with-tags]

# ⑤ 会话记录里的设备标识（脚本本身不含 ID 字面量）
python3 final-scrub.py            # 干跑
python3 final-scrub.py --apply

# ⑥ 复查
bash audit.sh
```

## 判定标准（交付时要能对账）

给用户的报告必须包含**分母**，例如：

```
钥匙串：237 条中 claude/anthropic 命中 0
keychain 命名约定直查：Claude Code-credentials / Claude Code → could not be found
git：21 个仓库，署名 0 条、.claude 路径对象 0 个
会话记录：1804 个文件中设备标识 0 处
统一日志：claude-code 命中 146 行 → 已执行 log erase --all
```

做不到的部分要**明确说清楚**，不要含糊：
- 服务端账号关联（若用户曾在浏览器里登录过 claude.ai）**本地删不掉**；
- force-push 之后 fork / 直链 SHA / 其它机器上的旧 clone **清不掉**；
- 旧 clone 一旦 push，旧历史会**复活** → 必须让它们重新 clone。

## 典型坑（详见 docs/03-lessons-learned.md）

| 坑 | 正确做法 |
|---|---|
| `git bundle create` 漏 `-C <repo>` → 备份静默失败 | 加 `-C`，失败即 `continue` 中止 |
| 多个本地副本指向同一远端，依次 force-push 互相覆盖 | 先做重复远端检测 |
| `--force-with-lease` 报 `stale info` | push 前先 `git fetch origin --prune` |
| `filter-branch -- --branches` 漏掉远端独有分支 | 先把远端分支同步为本地分支 |
| `filter-branch` 末尾 `reset --hard` 删掉工作区文件 | 先把要移除的路径另存 |
| 用 `--all` 验证 → 计入旧 remote-tracking 引用，假阴性 | `fetch --prune` 后用 `--branches --tags --remotes` |
| `refs/tags`、`refs/remotes` 不是 ref → 静默 0 | 用 `--tags` / `--remotes` |
| `timeout` 在 macOS 不存在 → 命令静默失败被当成「没命中」 | 别用 timeout；检查退出码 |
| macOS bash 3.2 无 `mapfile` | 用 `while read` |
| `grep -l -c` 混用导致计数虚高（把文件总数当命中数） | 只用 `grep -li | wc -l` |
| 删 `~/.claude/logs` 导致用户 daemon 起不来 | 被 LaunchAgent 引用时只清空内容、保留目录 |

## 参考

- `docs/01-what-it-collects.md` —— 源码确证的收集清单（字段 / 端点 / 落盘位置 / 无硬件指纹）
- `docs/02-audit-checklist.md` —— 20+ 检查点与手工命令
- `docs/03-lessons-learned.md` —— 真实翻车记录与修法
