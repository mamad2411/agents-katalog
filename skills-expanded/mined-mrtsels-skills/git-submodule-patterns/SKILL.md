---
name: git-submodule-patterns
description: Use when adding a git-cloned repo into another git repo.
license: MIT
metadata:
  hermes:
    tags:
    - git
    - submodule
    - gitlink
    - nested-repo
    - repository-management
    related_skills:
    - github
    - skill-farm-maintenance
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
    platforms:
    - macos
    - linux
  imported_from: hermes
---

# Git 嵌套仓库 / Submodule 模式

当一个 git 仓库（父仓库，如技能库）要收纳另一个 git 仓库（子仓库，如 git-cloned 技能/工具）时的正确做法与陷阱。

## Trigger

- 要把一个 git clone 的技能/工具/项目目录加进另一个 git-tracked 目录（技能库、monorepo、vendored tools）
- `git add` 报 "adding embedded git repository" 警告
- 克隆父仓库后某个子目录是空的、没有内容
- `git ls-files -s <path>` 显示 `160000` 模式条目

## 核心规则（实测，git 2.54）

1. **`git add <dir>` 只要目录内含自己的 `.git`，一律记录为 gitlink（mode `160000`，`ls-files` 单行一个 commit 指针）**，不管 `.gitignore` 怎么设置。
2. **「在 .gitignore 里忽略内层 `.git/` 让内容入库」是死路**：check-ignore 匹配了，git add 依然警告并记成 gitlink。不要沿用这种策略。
3. 想让内容真正入库（子仓库不再独立），必须**先删除内层 `.git`**，再 add。

## 正确做法

### 方案 A：submodule（子仓库需保持独立可 pull/push 时推荐）

路径为空/不存在时：

```bash
git submodule add <url> <path>
```

已有现成克隆（不想重下）时手动接线，效果等价：

```bash
git config -f .gitmodules submodule.<path>.path <path>
git config -f .gitmodules submodule.<path>.url <url>
git add .gitmodules <path>   # gitlink(160000) 已在 index，直接 add
git commit && git push
```

子仓库保留自己的 `.git`，照常 `git pull` 同步上游；父仓库只跟踪 commit 指针。

### 方案 B：内容入库（子仓库不需要独立 git 历史）

```bash
rm -rf <path>/.git          # 关键：必须删，ignore 没用
git add <path>              # 这次才真正加入文件
git commit && git push
```

### 方案 C：子模块转普通目录（内容需要改造/合并时）

子模块要求内容保持上游纯净；一旦要合并、改名或扩展内容，改动无法 push 回上游，子模块就失去意义。此时转为普通目录，并告知用户「不再能 git pull 同步上游」。实测步骤（git 2.54，2026-08 技能合并场景）：

```bash
git rm -f <path>                             # 从 index 移除 gitlink，并自动删除 .gitmodules 中对应条目
git config --remove-section submodule.<path> # git rm 不清 .git/config，残留的 url/.active 条目必须手动删
rm -rf .git/modules/<path>                   # 清理子模块的独立 git 目录
git add <新内容> && git commit && git push
```

顺序要点（全部实测）：

- **先 `git rm -f <path>`**：一步移除 gitlink 和 `.gitmodules` 条目，无需手改 `.gitmodules`。
- 之后再跑 `git submodule deinit -f <path>` 会报 `pathspec did not match`——无害，deinit 已无必要，别被吓到。
- `.git/config` 里的 `submodule.<path>.url` / `.active` 残留**不会**被 git rm 清理，必须 `git config --remove-section`，否则 `git submodule status` 报错。
- `.git/modules/<path>` 是子模块的独立 git 目录，需手动 rm。
- 被吸收的技能文件移入新技能 `references/` 时，git 会识别为 100% rename（R 状态），历史可追溯。

## 陷阱

- **裸 gitlink 是坏的**：index 里有 160000 条目但**没有 `.gitmodules`** → 克隆父仓库的人拿到**空目录**且无法获取内容。修复：补上 `.gitmodules`（方案 A 的手动接线）。
- **父仓库 push 不会推子仓库内容**：子仓库有改动需先在子仓库内单独 push，再在父仓库 `git add <path>` 更新指针并提交。
- **指针必须存在**：gitlink 指向的 commit 必须已存在于子仓库远程，否则克隆父仓库后 `submodule update` 失败。先 push 子仓库，再 add 指针。
- **仓库迁移**：push 输出 "This repository moved. Please use the new location" → `git remote set-url origin <new-url>`，否则下次 push 仍报错。
- 撤销误 add 的 gitlink：`git reset <path>`（不要用 `git rm --cached`，会留下悬空状态）。

## 验证

```bash
git ls-files -s <path>        # 160000 + commit SHA = submodule；逐行 100644 = 内容已入库
git clone --recurse-submodules <parent-url>   # 带子模块克隆
git submodule update --init   # 已克隆父仓库后补拉子模块
```

## 本机实例

技能库 `~/.agents/skills`（git 仓库 `mrtsels/skills`）中，`coding/rail-cli` 是 rail-cli 仓库的 submodule：`rail-cli/` 目录保留独立 `.git`（可 `git pull` 同步 rail-cli 仓库开发成果），父仓库 `.gitmodules` 记录引用。`productivity/consulting-problem-solving` 是历史遗留的裸 gitlink（无 `.gitmodules`，克隆后为空目录），待修。`writing/tech-doc-style-chinese`（Fenng/Tech-Doc-Style-Chinese）曾是 submodule，2026-08-11 因合并为双语技能 `writing/tech-doc-style` 并扩展中/英检查器，已按方案 C 转为普通目录。
