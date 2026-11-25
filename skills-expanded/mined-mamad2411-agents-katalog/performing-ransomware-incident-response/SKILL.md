---
name: performing-ransomware-incident-response
description: 执行结构化的勒索软件事件响应，包括遏制、解密评估、从备份恢复以及根除勒索软件持久化机制。
domain: cybersecurity
subdomain: incident-response
tags: [incident-response, ransomware, dfir, recovery, eradication, encryption]
version: "1.0"
author: mahipal
license: Apache-2.0
---

# 执行勒索软件事件响应（Performing Ransomware Incident Response）

## 适用场景
- 在一个或多个端点上检测到勒索软件加密
- 在文件共享或端点上发现勒索信文件
- 文件扩展名更改为已知勒索软件变体（.locked、.encrypted、.ryuk 等）
- 卷影副本被删除或备份系统遭到攻击
- EDR/AV 对已知勒索软件家族告警（LockBit、BlackCat/ALPHV、Cl0p、Royal、Play）

## 前置条件
- 包含勒索软件专项 Playbook 的事件响应计划
- 离线/不可变的备份基础设施
- 具有勒索软件回滚能力的 EDR 平台
- No More Ransom（nomoreransom.org）解密器数据库访问
- 用于快速隔离的网络分段能力
- 面向利益相关方和可能的执法机构的沟通计划

## 工作流程

### 步骤 1：检测并确认勒索软件
```bash
# 在文件共享中搜索勒索信文件
find /mnt/shares -name "README*.txt" -o -name "DECRYPT*.txt" -o -name "HOW_TO_RECOVER*" \
  -o -name "RESTORE_FILES*" -newer /tmp/baseline_timestamp 2>/dev/null

# 检查大规模文件加密指标
find /mnt/shares -name "*.encrypted" -o -name "*.locked" -o -name "*.BlackCat" \
  -o -name "*.lockbit" -mmin -60 2>/dev/null | head -50

# 从勒索信中识别勒索软件变体
strings ransom_note.txt | grep -iE "(bitcoin|wallet|tor|onion|decrypt|payment)"

# 上传样本到 ID Ransomware 进行变体识别
curl -X POST "https://id-ransomware.malwarehunterteam.com/api/upload" \
  -F "ransom_note=@ransom_note.txt" -F "encrypted_file=@sample.encrypted"
```

### 步骤 2：立即隔离受感染系统
```bash
# CrowdStrike Falcon - 批量遏制受感染主机
for device_id in $(cat infected_device_ids.txt); do
  curl -X POST "https://api.crowdstrike.com/devices/entities/devices-actions/v2?action_name=contain" \
    -H "Authorization: Bearer $FALCON_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"ids\": [\"$device_id\"]}"
done

# 在防火墙阻断已知勒索软件 C2 IP
while read ip; do
  iptables -A INPUT -s "$ip" -j DROP
  iptables -A OUTPUT -d "$ip" -j DROP
done < ransomware_c2_ips.txt

# 禁用网段间 SMB/横向移动协议
# Palo Alto 防火墙
set rulebase security rules block-smb-lateral from internal to internal application ms-ds-smb action deny
commit force
```

### 步骤 3：评估加密范围和影响
```bash
# Splunk 查询 - 通过文件修改模式识别受影响主机
index=endpoint sourcetype=sysmon EventCode=11
| stats dc(TargetFilename) as files_created by Computer
| where files_created > 1000
| sort -files_created

# 检查卷影副本是否被删除
wevtutil qe Application /q:"*[System[Provider[@Name='VSS']]]" /f:text /c:20

# 检查备份完整性
veeam-backup-check --repository "primary_backup" --verify-integrity
restic -r /backup/repo check --read-data-subset=1/10
```

### 步骤 4：检查可用的解密工具
```bash
# 在 No More Ransom 项目检查免费解密工具
# https://www.nomoreransom.org/en/decryption-tools.html

# 检查卡巴斯基解密工具数据库
# https://noransom.kaspersky.com/

# 检查 Emsisoft 解密工具数据库
# https://www.emsisoft.com/en/ransomware-decryption/

# 测试是否可从卷影副本恢复文件（如未被删除）
vssadmin list shadows
mklink /D C:\ShadowCopy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\

# 检查历史文件版本
wmic shadowcopy list brief
```

### 步骤 5：根除勒索软件和持久化机制
```bash
# 扫描所有系统的勒索软件产物
yara -r ransomware_rules.yar /mnt/infected_disk/

# 检查常见持久化位置
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /s
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /s
schtasks /query /fo CSV /v | findstr /i "encrypt lock ransom"

# 检查组策略中的勒索软件加载器
find /mnt/sysvol -name "*.exe" -o -name "*.dll" -o -name "*.bat" -newer /tmp/baseline

# 删除勒索软件产物
# 在取证镜像完成后执行
Get-ChildItem -Path C:\ -Include *.encrypted,*.locked -Recurse | Remove-Item -Force
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "malicious_entry" /f
```

### 步骤 6：从干净备份恢复系统
```bash
# 恢复前验证备份完整性
sha256sum backup_image_server01.vhdx
restic -r /backup/repo restore latest --target /mnt/restore --verify

# 从 Veeam 备份恢复
# Veeam PowerShell
Start-VBRRestoreSession -BackupObject (Get-VBRBackup -Name "Server01_Backup") \
  -RestorePoint (Get-VBRRestorePoint -Backup "Server01_Backup" | Sort-Object -Property CreationTime -Descending | Select-Object -First 1)

# 如果备份受损，从黄金镜像重建
packer build -var "os_version=2022" golden_image.pkr.hcl
terraform apply -var="image_id=ami-golden-2024" -auto-approve
```

### 步骤 7：恢复后验证
```bash
# 验证没有勒索软件持久化残留
Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, Command, Location
Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"} | Select-Object TaskName, TaskPath

# 验证恢复后的文件完整性
fciv -r C:\restored_data\ -sha256 > post_restore_hashes.txt
diff pre_infection_hashes.txt post_restore_hashes.txt

# 增强监控以防止再次感染
# 在敏感目录部署金丝雀文件
for dir in /mnt/shares/*/; do
  echo "CANARY_$(date +%s)" > "$dir/.canary_monitor.txt"
done
```

## 核心概念

| 概念 | 说明 |
|------|------|
| **双重勒索（Double Extortion）** | 攻击者加密数据并同时外泄，威胁公开发布 |
| **三重勒索（Triple Extortion）** | 增加 DDoS 威胁或联系受害者客户以增加压力 |
| **勒索软件即服务（RaaS）** | 附属者向运营商付费使用勒索软件工具的犯罪商业模式 |
| **解密器可用性** | No More Ransom 可能提供某些勒索软件家族的免费解密器 |
| **不可变备份（Immutable Backups）** | 无法修改或删除的备份副本，是勒索软件恢复的关键 |
| **驻留时间（Dwell Time）** | 初始攻陷到勒索软件部署之间的时间（通常为数周） |
| **IOC 共享** | 与 ISAC 和执法机构共享指标，提升集体防御能力 |

## 工具与系统

| 工具 | 用途 |
|------|------|
| ID Ransomware | 从样本识别勒索软件变体 |
| No More Ransom | 免费解密器数据库（nomoreransom.org） |
| CrowdStrike Falcon | 端点遏制和勒索软件回滚 |
| Veeam/Commvault | 备份验证和恢复 |
| YARA | 勒索软件产物扫描 |
| Volatility | 用于勒索软件分析的内存取证 |
| Splunk/Elastic | 加密范围评估的日志分析 |

## 常见场景

1. **LockBit 3.0 企业攻击**：攻击者攻陷 VPN，通过 GPO 在域内部署 LockBit。先隔离域控制器，验证备份完整性，从不可变备份恢复。
2. **BlackCat/ALPHV 双重勒索**：加密前已外泄数据。法务介入处理泄露通知，从备份恢复，如需要通过授权渠道谈判。
3. **Cl0p MOVEit 漏洞利用**：批量利用文件传输应用漏洞。修补漏洞，识别已外泄数据，重建受影响系统。
4. **针对医疗行业的勒索软件**：患者数据被加密。启动紧急人工程序，联系 HHS，优先恢复临床系统。
5. **通过受攻陷 MSP 的勒索软件**：攻击者通过 MSP 工具访问多个客户。断开 MSP 访问，按客户遏制，协调多租户响应。

## 输出格式
- 勒索软件变体识别报告
- 含受影响系统清单的加密范围评估
- 备份完整性验证结果
- 恢复时间线和优先还原计划
- 根除验证报告
- 包含预防建议的经验教训文档
