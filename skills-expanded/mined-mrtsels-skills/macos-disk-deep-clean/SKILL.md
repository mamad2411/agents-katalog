---
name: macos-disk-deep-clean
description: Use when 清理mac存储/磁盘满/找大文件. 找缓存外大头:容器运行时、Chrome端侧AI、音乐缓存。
metadata:
  source_frontmatter:
    category: apple
  imported_from: hermes
---

# macOS 磁盘深度清理

标准缓存清理（`~/Library/Caches`、`~/.cache`、`~/.npm`、`brew cleanup`）之外，真正的空间大头藏在**应用数据目录**里，每个可占 4–25G。本技能覆盖：全景侦察流程 + 隐蔽大头识别 + 安全删除 + 已完成项目的归档回收。

## 用户偏好（强制）

- **逐项确认再删**：删除是不可逆操作。先侦察列清单（大小+内容+可恢复性），用 clarify 让用户逐项拍板，绝不批量盲删
- 数据资产（音乐库、照片、Keynote、聊天记录）与缓存/镜像严格区分：资产先问，缓存可直接清
- 每个删除项说明可恢复性（重下载/归档包/GitHub 备份）

## 全景侦察流程（10 分钟内出全盘图）

```bash
df -h / /System/Volumes/Data          # Data 卷才是真实占用
tmutil listlocalsnapshots /           # APFS 快照（隐性占用）
du -sh /Applications /Library /Users /opt /usr/local 2>/dev/null | sort -rh
du -sh ~/Library/* 2>/dev/null | sort -rh | head -15    # Library 常是最大头
du -sh ~/Library/Containers/* 2>/dev/null | sort -rh | head -10   # 沙盒容器
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -rh | head -10
find ~ -maxdepth 4 -type f -size +500M 2>/dev/null | head -30
```

## 隐蔽大头清单（普通清理碰不到的）

### 1. Apple 容器运行时：`~/Library/Application Support/com.apple.container`
macOS 原生容器化运行时数据（containerd 风格 OCI 存储），可达 5–25G。识别：子目录 `containers/`、`snapshots/`、`content/blobs`、`kernels/`、`networks/`、`state.json`。**state.json 列出镜像名，可判断归属哪个项目**（如离职项目残留的后端镜像）。
- 官方 `container image prune --all` 需先 `container system start`（拉起 VM，重）
- daemon 未运行时（`pgrep -fl "containerization|vminit|buildkit|containerd"` 无输出）**直接删数据目录**：`rm -rf .../containers/buildkit .../snapshots/* .../content/blobs/*`；`kernels/` 是运行时组件保留
- 可恢复：镜像从 docker.io 重拉或项目归档包

### 2. Chrome 端侧 AI 模型：`~/Library/Application Support/Google/Chrome/`
Chrome 目录 5G+ 时大头是**端侧 AI 模型**而非缓存：`OptGuideOnDeviceModel/`（Gemini Nano，单版本 4G）、`OptGuideOnDeviceClassifierModel/`、`optimization_guide_model_store/` — 静默下载、不占 Cache、普通清理碰不到。
- **删除前必须退出 Chrome**：`osascript -e 'tell application "Google Chrome" to quit'`，确认 `pgrep -x "Google Chrome"` 无输出
- 可删：AI 模型目录 + `Default/Service Worker/CacheStorage`（网站离线缓存 800M+）
- 勿删：`Default/` 其余（Extensions、IndexedDB、书签、历史）

### 3. Apple Music：库 vs 离线缓存
- `~/Music/Apple Music/` = 本地音乐库资产（歌手目录，可达 50G）— **用户资产绝不可删**
- `~/Music/Apple Music Downloads/` = 订阅离线缓存（13G+）— 可删，可重新下载

### 4. 已完成项目的残留（最大回收来源）
离职/完结项目残留常达 30G：项目目录里的数据集（gitignored 的可直接删，如 RICO 23G）、容器镜像、构建缓存。
- 删数据集前验证：`git ls-files data/` 是否被追踪 + `cat .gitignore` 是否 ignore + 有无下载脚本
- 完整归档工作流见 skill `project-archiving`

### 5. 卸载应用的残留（Docker Desktop 实测案例）
app 卸载后数据/辅助进程常残留 1–2G，普通清理扫不到。**先诊断 app 是否还在**：
```bash
ls /Applications | grep -i docker            # app 不存在
mdfind "kMDItemCFBundleIdentifier == 'com.docker.docker'"  # 按 bundle id 找
pgrep -fl "Docker Desktop|vmnetd"            # 辅助进程仍在跑
docker context ls                            # 残留 context（如 desktop-linux）
```
残留清单（Docker Desktop）：`~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`（VM 磁盘）、`/Library/PrivilegedHelperTools/com.docker.{vmnetd,socket}`、`/Library/LaunchDaemons/com.docker.{vmnetd,socket}.plist`、docker context `desktop-linux`。
清理顺序：
```bash
rm -rf ~/Library/Containers/com.docker.docker
# 系统级残留提权删（弹 GUI 密码框）：
osascript -e 'do shell script "launchctl bootout system/com.docker.vmnetd 2>/dev/null; launchctl bootout system/com.docker.socket 2>/dev/null; rm -f /Library/PrivilegedHelperTools/com.docker.vmnetd /Library/PrivilegedHelperTools/com.docker.socket /Library/LaunchDaemons/com.docker.vmnetd.plist /Library/LaunchDaemons/com.docker.socket.plist" with administrator privileges'
docker context use colima && docker context rm desktop-linux
```

## 陷阱

- **APFS 快照导致 du 虚高**：`du -sh /System` 可显示几百 G（快照重复统计），实际系统卷仅 ~12G。真实占用看 `df -h /System/Volumes/Data` + `diskutil list`
- **`du -sh /Applications` 首次扫描可能虚高**（快照/硬链接），以子项总和为准
- **APFS 稀疏文件：`ls -lh` 逻辑大小 ≠ `du` 实际占用**：VM 磁盘镜像（如 Docker.raw）预分配逻辑容量（显示 460G）但实际只占写入块（du 1.1G）。用户问"实际占用"一律以 `du -sh` 为准，`ls` 大数字不用慌
- 删除大目录后用 `df -h /` 验证实际释放，du 可能因快照滞后

## 验证

```bash
df -h / | tail -1          # 删除前后对比可用空间
du -sh <目标目录>           # 确认缩到预期大小
```
