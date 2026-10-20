---
name: sysadmin-qa
description: Linux SysAdmin 核心知識問答 — 284 題精煉版，涵蓋 Junior 到 Guru 級別
version: 1.0.0
author: distilled from trimstray/test-your-sysadmin-skills
tags: [linux, sysadmin, troubleshooting, networking, security, performance]
---

# Linux SysAdmin 核心知識問答

> 來源：[trimstray/test-your-sysadmin-skills](https://github.com/trimstray/test-your-sysadmin-skills) 284 題精煉

## 系統啟動 & 行程

**Q: Linux 開機順序？**
BIOS/UEFI → Bootloader (GRUB) → Kernel → initramfs → systemd (PID 1) → targets → login

**Q: 什麼是 zombie process？如何清除？**
已終止但父行程未呼叫 `wait()` 的行程。`kill -SIGCHLD <parent_pid>`；若父行程無回應則 `kill <parent_pid>`。

**Q: 如何找出佔用 CPU 最多的行程？**
```bash
ps aux --sort=-%cpu | head -10
top -bn1 | head -20
```

**Q: `nice` 與 `renice` 差異？**
`nice` 啟動時設定優先級（-20 最高，19 最低）；`renice` 更改執行中行程的優先級。

## 檔案系統 & 磁碟

**Q: inode 是什麼？如何查看 inode 使用量？**
儲存檔案 metadata（權限、時間戳、data block 位置）但不含檔名。`df -i` 查看 inode 使用量。

**Q: 如何找出磁碟空間被哪些大檔案佔用？**
```bash
du -sh /* 2>/dev/null | sort -rh | head -20
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null
```

**Q: ext4 vs xfs 差異？**
ext4：成熟穩定，適合通用用途，最大 1EB；xfs：高效能大檔案、平行 I/O，適合資料庫，最大 8EB。

**Q: 如何在不卸載的情況下擴充 LVM？**
```bash
pvextend /dev/sdb1
vgextend vgname /dev/sdb1
lvextend -L +10G /dev/vgname/lvname
resize2fs /dev/vgname/lvname   # ext4
xfs_growfs /mountpoint          # xfs
```

## 網路

**Q: 如何查看哪個行程監聽特定 port？**
```bash
ss -tlnp | grep :80
lsof -i :80
netstat -tlnp | grep :80
```

**Q: TCP 三次握手？**
SYN → SYN-ACK → ACK。建立連線。四次揮手關閉：FIN → ACK → FIN → ACK。

**Q: 如何在 Linux 追蹤網路封包？**
```bash
tcpdump -i eth0 -w capture.pcap
tcpdump -i any port 80 -n
wireshark capture.pcap   # GUI 分析
```

**Q: iptables 與 nftables 差異？**
iptables：傳統，各 table 獨立；nftables：新一代統一框架，效能更好，語法更一致（RHEL 8+/Debian 10+ 預設）。

**Q: 如何排查 DNS 問題？**
```bash
dig +trace example.com          # 追蹤完整解析鏈
nslookup example.com 8.8.8.8   # 指定 DNS server 查詢
systemd-resolve --statistics    # 查看快取狀態
resolvectl query example.com    # systemd-resolved 查詢
```

## 安全性

**Q: 如何確認 SSH 設定是否安全？**
```bash
sshd -T | grep -E "permitrootlogin|passwordauthentication|pubkeyauthentication"
# 應為：PermitRootLogin no/prohibit-password, PasswordAuthentication no
```

**Q: 什麼是 SUID/SGID？安全風險？**
SUID：執行時以 owner 權限執行（`-rwsr-xr-x`）。SGID：以 group 權限執行。
稽核：`find / -perm -4000 -type f 2>/dev/null`

**Q: 如何防範 fork bomb？**
在 `/etc/security/limits.conf` 設定：
```
* hard nproc 1000
* soft nproc 500
```

**Q: 什麼是 SELinux context？如何排查 AVC denial？**
```bash
getenforce                    # Enforcing/Permissive/Disabled
ausearch -m AVC -ts recent   # 查看最近 denial
audit2why < /var/log/audit/audit.log
```

## 效能調優

**Q: 如何分析 I/O 瓶頸？**
```bash
iostat -xz 1                  # 磁碟 I/O 統計
iotop -o                       # 即時 I/O by process
dstat -cdngy                   # 綜合系統狀態
```

**Q: 什麼是 swap swappiness？如何調整？**
控制 kernel 傾向使用 swap（0=儘量不用，100=積極使用）。
```bash
sysctl vm.swappiness=10       # 臨時
echo "vm.swappiness=10" >> /etc/sysctl.conf  # 永久
```

**Q: CPU 效能問題排查路徑？**
1. `top`/`htop` 確認哪個行程
2. `perf top` 找 hot function
3. `strace -p PID` 看 syscall
4. `lsof -p PID` 確認開啟的 fd

**Q: 什麼是 OOM Killer？如何防止重要行程被殺？**
```bash
echo -17 > /proc/<pid>/oom_adj          # 舊核心
echo -1000 > /proc/<pid>/oom_score_adj  # 新核心（完全免疫）
```

## 系統管理

**Q: 如何排查 systemd service 啟動失敗？**
```bash
systemctl status service-name -l
journalctl -u service-name --since "10 min ago"
journalctl -b -p err            # 本次開機所有 error
```

**Q: 如何限制行程的 CPU 和記憶體使用？**
```bash
# cgroup v2
systemd-run --slice=limited.slice --property=CPUQuota=50% --property=MemoryMax=512M command
# 或直接設定 service
# /etc/systemd/system/myapp.service
# [Service]
# CPUQuota=50%
# MemoryMax=512M
```

**Q: 如何安全地輪替 log 檔案？**
logrotate 設定 `/etc/logrotate.d/myapp`：
```
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        systemctl reload myapp
    endscript
}
```

**Q: kernel 參數優化 for web server？**
```bash
# /etc/sysctl.conf
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_tw_reuse = 1
fs.file-max = 1000000
```

## 故障排查 SOP

1. **收集症狀** — 錯誤訊息、時間點、影響範圍
2. **檢查 log** — `/var/log/syslog`、`journalctl`、應用程式 log
3. **資源狀態** — CPU、記憶體、磁碟、網路
4. **行程狀態** — `ps`、`ss`、`lsof`
5. **最近變更** — 部署、設定變更、套件更新
6. **隔離問題** — 縮小範圍到單一元件
7. **測試假設** — 一次改一個變數
8. **記錄解法** — 為下次同樣問題留下文件
