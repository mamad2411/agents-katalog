# Skill: xhs-downloader

[中文版本](SKILL.md) | [English](SKILL_EN.md) | [平台使用指南](PLATFORM_GUIDE.md)

## 🎯 平台支持

本 Skill 支持以下 AI 编程助手平台：
- ✅ **OpenCode** - 完整支持，自动配置
- ✅ **GitHub Copilot** - 通过 `.github/copilot-instructions.md` 支持
- ✅ **Claude Code** - 通过 `.claude/` 配置支持
- ✅ **Codex** - 通过 `.codex/` 配置支持

> 📖 查看 [平台使用指南](PLATFORM_GUIDE.md) 获取各平台详细使用说明

## What I do
- 使用 XHS-Downloader 项目下载小红书分享链接的内容
- 自动克隆项目、设置虚拟环境、安装依赖
- 支持命令行模式运行下载任务
- 处理小红书图片和视频的下载
- 下载完成后生成作品信息 Markdown 文件
- 自动打开下载目录，方便查看文件

## When to use me
使用此 skill 当你需要：
- 下载小红书分享链接中的图片或视频
- 批量处理多个小红书链接
- 使用命令行方式操作 XHS-Downloader
- 保存作品信息供后续查看

## How to use me
1. 直接发送小红书分享链接
2. 我会自动：
   - 检查并克隆 XHS-Downloader 项目（develop 分支）到 skill 目录
   - 创建 uv 虚拟环境
   - 同步依赖
   - 设置 folder_mode 为 true（每个作品保存在单独文件夹）
   - 下载内容
   - 生成作品信息 Markdown 文件
   - 显示下载目录链接

## Configuration

### OpenCode
项目路径：`~/.config/opencode/skills/xhs-downloader/XHS-Downloader`
下载目录：`~/.config/opencode/skills/xhs-downloader/XHS-Downloader/Volume/Download`
配置文件：`opencode.yaml`

### GitHub Copilot
配置文件：`.github/copilot-instructions.md`
使用方式：直接发送链接或使用 `@workspace` 命令

### Claude Code
配置目录：`.claude/`
初始化：`bash .claude/setup.sh`
下载：`bash .claude/download.sh <url>`

### Codex
配置目录：`.codex/`
初始化：`bash .codex/setup.sh`
下载：`bash .codex/download.sh <url>`

## Setup Commands
```bash
# 克隆项目（develop 分支）
git clone -b develop https://github.com/JoeanAmier/XHS-Downloader.git

# 进入项目目录
cd XHS-Downloader

# 创建虚拟环境
uv venv

# 同步依赖
uv sync
```

## Usage Examples
发送小红书分享链接如：
- `https://www.xiaohongshu.com/discovery/item/xxxxx`
- `http://xhslink.com/xxxxx`

下载完成后会：
1. 在 `Volume/Download` 目录下保存作品文件
2. 在相同目录生成 `作品信息.md` 文件
3. 显示下载目录的完整路径

## Notes
- 项目保存在 skill 目录下，后续可直接拉取更新
- 每个作品会保存在单独的文件夹中（folder_mode: true）
- 作品信息会以 Markdown 格式保存
- 下载目录支持点击打开
