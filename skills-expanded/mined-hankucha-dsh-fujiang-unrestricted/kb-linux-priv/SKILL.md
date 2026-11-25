---
name: kb-linux-priv
description: CVE/PoC 知识库 · Linux 本地提权：PwnKit(2021-4034)、Dirty Pipe(2022-0847)、Baron Samedit(2021-3156)、fs_context(2022-0185)、GameOver(lay)(2023-2640)、nf_tables(2024-1086/2023-32233)、overlayfs(2023-0386/2021-3493)、sudoedit(2023-22809)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# Linux 本地提权（11 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

拿到低权 shell（`www-data`、`nobody`、容器内 root）之后的固定动作：

```bash
uname -a; cat /etc/os-release; id; sudo -l 2>/dev/null; find / -perm -4000 -type f 2>/dev/null
dpkg -l | grep -E 'sudo|policykit|glibc' 2>/dev/null || rpm -qa | grep -E 'sudo|polkit|glibc'
```

**先看内核与 glibc/sudo/polkit 版本**，再对条目；别一上来就编译不认识的内核 exploit —— 崩机比提权更容易发生。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `cve-2021-3156-baron-samedit.md` | Baron Samedit（sudo 堆溢出提权） | high | - |
| `cve-2021-3493-ubuntu-overlayfs.md` | Ubuntu overlayfs 本地提权（2021） | high | userns + overlayfs 复制 setuid 属性 |
| `cve-2021-4034-pwnkit.md` | PwnKit（polkit pkexec 本地提权） | high | - |
| `cve-2022-0185-fs-context-overflow.md` | fs_context 堆溢出提权（legacy_parse_param） | high | unshare -Ur + 构造超长 legacy 挂载参数 |
| `cve-2022-0847-dirtypipe.md` | Dirty Pipe（页缓存写覆盖提权） | high | - |
| `cve-2023-0386-overlayfs.md` | overlayfs copy-up 权限绕过提权 | high | - |
| `cve-2023-22809-sudo-edit.md` | sudoedit 环境变量注入提权（EDITOR 带 --） | high | EDITOR='vim -- /etc/sudoers' |
| `cve-2023-2640-gameoverlay.md` | Ubuntu overlayfs 权限提升（GameOver(lay)） | high | unshare + overlayfs xattr 复制绕过 |
| `cve-2023-32233-nftables.md` | nf_tables 释放后重用提权（2023） | high | unshare + 批量 nft 规则触发 UAF |
| `cve-2024-0582-io-uring-uaf.md` | Linux io_uring 本地提权（CVE-2024-0582） | high | 固定文件注册后释放页 → 重映射改写 |
| `cve-2024-1086-nftables.md` | nf_tables 释放后重用提权 | high | - |

## 用这一页的方法

1. 容器里先确认权限：`capsh --print`、`cat /proc/self/status | grep Cap`。有 `CAP_SYS_ADMIN` 时优先查 `cgroup`/`overlayfs`/`mount` 路线，不必打内核 UAF。
2. 内核 exploit 会 panic；先在同类内核的实验机跑通，再决定是否对生产执行。
3. 提权成功后先落一个可复现的凭据（`sudo` 用户、`authorized_keys`），再清 exploit 文件。
