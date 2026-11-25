---
name: minecraft-modpack-server
description: "Host modded Minecraft servers (CurseForge, Modrinth)."
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
tags: [minecraft, gaming, server, neoforge, forge, modpack]
platforms: [linux, macos]
---

# Minecraft模组服务器搭建指南

## 适用场景
- 用户希望从模组包压缩文件中搭建经过修改的Minecraft服务器
- 用户需要NeoForge/Forge服务器配置方面的帮助
- 用户咨询Minecraft服务器的性能优化或备份相关问题

## 先收集用户偏好设置
在开始搭建之前，需向用户询问以下信息：
- **服务器名称/欢迎语**——服务器列表中应显示什么内容？
- **种子值**——使用固定种子还是随机生成？
- **难度级别**——和平模式/简单模式/普通模式/困难模式？
- **游戏模式**——生存模式/创造模式/冒险模式？
- **在线模式**——开启（需Mojang认证及正规账号）或关闭（适合局域网或破解版玩家）？
- **预期玩家数量**——预计会有多少玩家？（会影响内存分配和视野距离设置）
- **内存分配方式**——由用户指定，还是让智能代理根据模组数量和可用内存自动决定？
- **视野距离/模拟距离**——由用户指定，还是让智能代理根据玩家数量和硬件配置自动选择？
- **PvP功能**——开启还是关闭？
- **访问权限设置**——开放服务器还是仅允许白名单用户进入？
- **备份设置**——是否需要自动备份？备份频率如何？

如果用户未作明确要求，可选用合理的默认值，但在生成配置文件之前务必先征得用户同意。

## 搭建步骤

### 1. 下载并检查模组包
```bash
mkdir -p ~/minecraft-server
cd ~/minecraft-server
wget -O serverpack.zip "<URL>"
unzip -o serverpack.zip -d server
ls server/
```
请查找：`startserver.sh`、安装程序 JAR 文件（neoforge/forge 版本）、`user_jvm_args.txt` 以及 `mods/` 文件夹。通过查看这些脚本可以确定：模组加载器的类型、版本以及所需的 Java 版本。

### 2. 安装 Java
- Minecraft 1.21 及以上版本 → Java 21：`sudo apt install openjdk-21-jre-headless`
- Minecraft 1.18–1.20 版本 → Java 17：`sudo apt install openjdk-17-jre-headless`
- Minecraft 1.16 及更低版本 → Java 8：`sudo apt install openjdk-8-jre-headless`
- 验证安装结果：`java -version`

### 3. 安装模组加载器
大多数服务器包中都包含安装脚本。若只需安装而不立即启动服务器，可使用 INSTALL_ONLY 环境变量来实现。
```bash
cd ~/minecraft-server/server
ATM10_INSTALL_ONLY=true bash startserver.sh
# Or for generic Forge packs:
# java -jar forge-*-installer.jar --installServer
```
该操作会下载相关库文件，并对服务器端的 jar 文件进行补丁更新等处理。
```bash
echo "eula=true" > ~/minecraft-server/server/eula.txt
```

### 5. 配置 server.properties 文件
修改版/局域网模式下的关键设置：
```properties
motd=\u00a7b\u00a7lServer Name \u00a7r\u00a78| \u00a7aModpack Name
server-port=25565
online-mode=true          # false for LAN without Mojang auth
enforce-secure-profile=true  # match online-mode
difficulty=hard            # most modpacks balance around hard
allow-flight=true          # REQUIRED for modded (flying mounts/items)
spawn-protection=0         # let everyone build at spawn
max-tick-time=180000       # modded needs longer tick timeout
enable-command-block=true
```

性能设置（根据硬件资源进行扩展）：
```properties
# 2 players, beefy machine:
view-distance=16
simulation-distance=10

# 4-6 players, moderate machine:
view-distance=10
simulation-distance=6

# 8+ players or weaker hardware:
view-distance=8
simulation-distance=4
```

### 6. 调整 JVM 参数（user_jvm_args.txt）
根据玩家数量和模组数量来调整内存容量。针对安装了模组的游戏，可参考以下经验法则：
- 100–200 个模组：6–12 GB
- 200–350 个及以上模组：12–24 GB
- 需为操作系统及其他任务预留至少 8 GB 的可用内存。

```
-Xms12G
-Xmx24G
-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
-XX:+UnlockExperimentalVMOptions
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=30
-XX:G1MaxNewSizePercent=40
-XX:G1HeapRegionSize=8M
-XX:G1ReservePercent=20
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=4
-XX:InitiatingHeapOccupancyPercent=15
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=5
-XX:SurvivorRatio=32
-XX:+PerfDisableSharedMem
-XX:MaxTenuringThreshold=1
```

### 7. 开放防火墙
```bash
sudo ufw allow 25565/tcp comment "Minecraft Server"
```
查询方式：`sudo ufw status | grep 25565`
```bash
cat > ~/start-minecraft.sh << 'EOF'
#!/bin/bash
cd ~/minecraft-server/server
java @user_jvm_args.txt @libraries/net/neoforged/neoforge/<VERSION>/unix_args.txt nogui
EOF
chmod +x ~/start-minecraft.sh
```
注意：对于 Forge（非 NeoForge）版本，参数文件的位置有所不同。请查看 `startserver.sh` 文件以获取确切路径。

### 9. 设置自动备份
创建备份脚本：
```bash
cat > ~/minecraft-server/backup.sh << 'SCRIPT'
#!/bin/bash
SERVER_DIR="$HOME/minecraft-server/server"
BACKUP_DIR="$HOME/minecraft-server/backups"
WORLD_DIR="$SERVER_DIR/world"
MAX_BACKUPS=24
mkdir -p "$BACKUP_DIR"
[ ! -d "$WORLD_DIR" ] && echo "[BACKUP] No world folder" && exit 0
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/world_${TIMESTAMP}.tar.gz"
echo "[BACKUP] Starting at $(date)"
tar -czf "$BACKUP_FILE" -C "$SERVER_DIR" world
SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[BACKUP] Saved: $BACKUP_FILE ($SIZE)"
BACKUP_COUNT=$(ls -1t "$BACKUP_DIR"/world_*.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
    REMOVE=$((BACKUP_COUNT - MAX_BACKUPS))
    ls -1t "$BACKUP_DIR"/world_*.tar.gz | tail -n "$REMOVE" | xargs rm -f
    echo "[BACKUP] Pruned $REMOVE old backup(s)"
fi
echo "[BACKUP] Done at $(date)"
SCRIPT
chmod +x ~/minecraft-server/backup.sh
```

添加每小时定时任务：
```bash
(crontab -l 2>/dev/null | grep -v "minecraft/backup.sh"; echo "0 * * * * $HOME/minecraft-server/backup.sh >> $HOME/minecraft-server/backups/backup.log 2>&1") | crontab -
```

## 常见问题
- 对于经过修改的服务器，务必设置 `allow-flight=true`——否则带有喷气背包/飞行功能的模组会将玩家踢出游戏。
- 设置 `max-tick-time=180000` 或更高值——因为修改后的服务器在生成世界时，每个时间步的长度通常较长。
- 首次启动速度较慢（大型服务器包可能需要数分钟）——无需惊慌。
- 首次启动时出现“无法跟上！”的警告属于正常现象，待初始区块生成完成后就会消失。
- 如果设置了 `online-mode=false`，则必须同时将 `enforce-secure-profile=false` 也设为该值，否则客户端将无法连接。
- 服务器包中的 `startserver.sh` 文件通常包含自动重启循环——请创建一个不包含该循环的纯净启动脚本。
- 若要使用新的种子重新生成世界，请删除 `world/` 文件夹。
- 部分服务器包会通过环境变量来控制其行为（例如，ATM10 使用了 ATM10_JAVA、ATM10_RESTART、ATM10_INSTALL_ONLY 等变量）。

## 验证方法
- 使用 `pgrep -fa neoforge` 或 `pgrep -fa minecraft` 检查服务器是否正在运行。
- 查看日志：`tail -f ~/minecraft-server/server/logs/latest.log`。
- 若日志中出现 “Done (Xs)!” 字样，即表示服务器已准备就绪。
- 测试连接：在游戏的多人模式中输入服务器的 IP 地址进行连接测试。
