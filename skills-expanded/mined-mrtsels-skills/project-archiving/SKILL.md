---
name: project-archiving
description: Use when archiving finished projects.
metadata:
  source_frontmatter:
    category: devops
  imported_from: hermes
---

# Project Archiving (项目归档)

把已完成的开发项目归档（tar.gz 压缩 + 移出主目录），腾空间、整理 `~/`。归档 ≠ 删除：保留压缩包 + GitHub 远端双备份，可随时恢复。

## 触发场景
- 用户说 "XX 项目可以 archive 了 / 归档"
- 清理磁盘时发现"做完的项目 + 大数据集"（见下方识别小节）

## 归档流程

### 1. 归档前检查（缺一不可）
```bash
git status -s            # 未提交改动？
git remote -v            # 有远端 = 双保险
docker ps; pgrep -fl <name>   # 有无运行中容器/进程
```
- 未提交/未跟踪文件先 `git add <具体路径>` + commit + push（归档后没有第二份工作副本，改动会丢）
- 仓库有多个 pushurl（GitHub + 内网部署服务器）时，见下方双 pushurl 陷阱

### 2. 双 pushurl 陷阱
`git push` 会推送**全部** pushurl；内网 pushurl 连不上会报 `fatal: unable to access <内网IP>`，但 GitHub 侧可能已成功。验证是否全部推送：
```bash
git log --oneline origin/main..HEAD   # 输出为空 = 已全部推送
```
别被 `fatal` 报错误导，先验证远端状态再决定处理。

### 3. 打包（后台执行）
```bash
tar czf ~/Archives/<name>-YYYYMMDD.tar.gz \
  --exclude='__pycache__' --exclude='.DS_Store' --exclude='.serena' <dir>
```
- 3G+ 数据 gzip 需数分钟 → terminal background=true + notify_on_complete=true
- 排除项：`__pycache__`、`.DS_Store`、`.serena`（agent 缓存）

### 4. 验证压缩包（删原目录前必做）
```bash
tar -tzf <包> | wc -l                    # 文件数
tar -tzf <包> | grep -E "README|AGENTS"  # 抽查关键文件存在
```

### 5. 删除原目录
- 报 "Directory not empty"：多为残留 `.DS_Store`（打包 exclude 了但文件还在）→ `ls -la` 确认后删掉再 rm
- 删掉当前 shell 的 cwd 会报 `getcwd: cannot access parent directories` → 后续命令显式传 workdir

## 空间预期（重要）
- git 对象已 zlib 压缩、docker 镜像 tar 几乎不可再压缩 → tar.gz 净释放很小（实测 3.4G → 3.0G，只省 ~0.4G）
- 归档的价值是目录整洁 + 双备份；**要省空间**：把 tar.gz 移外置盘或删（GitHub 有完整备份）

## 识别"做完的项目 + 大数据集"
- `du -sh ~/* | sort -rh` 找异常大的项目目录
- 学术/ML 项目大在 `data/`（实测 GNN 项目 data/rico_local 23G）
- **删数据集前验证可恢复性**（全通过才可删）：`git ls-files data/` 未被追踪 + `.gitignore` 含 data/ + 有 download 脚本（如 scripts/download_datasets.py）+ `git status` 干净
- 项目完成度证据：README/AGENTS.md 里 "All phases complete / Delivered" 等表述
- 注意区分：`.git` 历史也可能占大头（实测 2.2G），那不是数据集，删不得

## 磁盘侦察陷阱（APFS）
- `du -sh /System` 显示数百 G 是 APFS 快照重复统计；真实占用看 `df -h /System/Volumes/Data` + `diskutil list`（系统卷实际 ~13G）
- `du` 总目录 vs 子项总和差异（实测 /Applications 71G vs 子项 33G）→ 以子项总和为准
- 详细磁盘清理分类与缓存清法见 `macos-storage-management` skill

## 归档后收尾
- 报告三要素：原大小 → 归档包大小、GitHub 已推送验证（`git log --oneline origin/main..HEAD` 为空）、删除项可恢复性
- **离职/完结项目常连带容器镜像残留**：`~/Library/Application Support/com.apple.container`（Apple 容器运行时，BuildKit 缓存 + OCI 镜像层可达 5–25G）一并排查回收，见 `macos-disk-deep-clean` skill
- 本地 tar.gz 处置由用户拍板：移外置盘 / 删除（GitHub 有备份）/ 保留；GitHub 仓库删除或转私有需用户明确决定
- **删本地 tar.gz 前验证远端完整性**（删完即无本地副本，必须先确认远端含全部内容）：`gh api "repos/<owner>/<repo>/commits?per_page=1" --jq '.[0].sha'` 对比归档时本地最后 commit（`git log --oneline -1`），sha 一致才可删（实测验证 dd636a2 后安全删除 2G 包）
