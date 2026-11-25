---
id: os-maintenance-linux
categoria: os
nome: os-maintenance-linux
descricao: "Manutenção nativa do Linux - ferramentas built-in para diagnóstico, reparo, otimização e saúde do sistema. Unifica fsck, smartctl, journalctl, systemd, package managers, kernel, boot, rede, discos, e mais."
entrypoint: linux_maintenance.py
script: mcp/os/habilidades/os-maintenance/Linux/linux_maintenance.py
---

# Linux Native Maintenance Tools — Domínio Completo

## Visão Geral

Este núcleo domina **todas as ferramentas nativas do Linux** para manutenção, diagnóstico, reparo e otimização. Zero dependências externas — apenas o que o Linux já fornece (coreutils, util-linux, systemd, procps, iproute2, etc.).

---

## Ferramentas Cobertas

### 1. Sistema de Arquivos & Disco

| Ferramenta | Função | Requer Root |
|------------|--------|-------------|
| **fsck** | Verifica e corrige sistemas de arquivos (ext4, xfs, btrfs, f2fs, etc.) | Sim |
| **e2fsck** | Específico para ext2/3/4 (mais opções) | Sim |
| **xfs_repair** | Reparo XFS | Sim |
| **btrfs check** | Verificação Btrfs | Sim |
| **smartctl (smartmontools)** | SMART health, testes, atributos | Sim |
| **lsblk / blkid / fdisk / parted** | Info de blocos, partições | Não (info), Sim (modificação) |
| **df / du / ncdu** | Uso de disco | Não |
| **fstrim / discard** | TRIM SSD (discard mount option) | Sim |
| **hdparm / sdparm** | Parâmetros disco SATA/SAS | Sim |
| **nvme-cli** | Gerenciamento NVMe (health, format, firmware) | Sim |

### 2. Systemd & Serviços

| Ferramenta | Função |
|------------|--------|
| **systemctl** | Controla serviços (start, stop, enable, disable, status, restart) |
| **journalctl** | Logs do systemd (filtros por unidade, prioridade, tempo, boot) |
| **systemd-analyze** | Análise de boot (blame, critical-chain, plot) |
| **systemd-tmpfiles** | Gerencia arquivos temporários |
| **machinectl** | Gerencia containers/máquinas |

### 3. Kernel & Boot

| Ferramenta | Função | Requer Root |
|------------|--------|-------------|
| **dmesg / kernel ring buffer** | Mensagens do kernel | Não (leitura), Sim (clear) |
| **kmod (lsmod, modprobe, modinfo)** | Módulos do kernel | Sim (load/unload) |
| **grub2 / grubby / efibootmgr** | Configuração bootloader | Sim |
| **update-grub / grub-mkconfig** | Regenera config GRUB | Sim |
| **mkinitcpio / dracut / update-initramfs** | Reconstrói initramfs | Sim |
| **sysctl / /proc/sys** | Parâmetros kernel runtime | Sim (write) |

### 4. Gerenciamento de Pacotes (Distro-agnostic)

| Ferramenta | Distros | Função |
|------------|---------|--------|
| **apt / apt-get / dpkg** | Debian/Ubuntu | Instala, remove, atualiza, verifica, limpa cache |
| **dnf / yum / rpm** | RHEL/Fedora/CentOS | Similar ao apt |
| **pacman** | Arch/Manjaro | Gerenciamento pacotes |
| **zypper** | openSUSE | Gerenciamento pacotes |
| **flatpak / snap / appimage** | Universal | Apps sandboxed |

### 5. Logs & Auditoria

| Ferramenta | Função |
|------------|--------|
| **journalctl** | Logs systemd (unified) |
| **rsyslog / syslog-ng** | Syslog tradicional |
| **auditd / ausearch / aureport** | Auditoria segurança (CAPP/EAL) |
| **logrotate** | Rotação logs |
| **last / lastb / utmp / wtmp** | Login history |

### 6. Rede & Conectividade

| Ferramenta | Função |
|------------|--------|
| **ip / ss / nft / iptables** | Netlink, sockets, firewall (moderno) |
| **nmcli / nmtui** | NetworkManager CLI/TUI |
| **systemd-resolve / resolvectl** | DNS resolver |
| **ping / traceroute / mtr / tracepath** | Conectividade |
| **dig / drill / nslookup / host** | DNS lookup |
| **curl / wget / httpie** | HTTP client |
| **tcpdump / wireshark-cli / tshark** | Packet capture |
| **netstat (deprecated) → ss** | Socket statistics |

### 7. Processos & Recursos

| Ferramenta | Função |
|------------|--------|
| **ps / pgrep / pkill / pstree** | Process listing |
| **top / htop / btop / glances** | Monitor interativo |
| **vmstat / iostat / mpstat / pidstat (sysstat)** | Estatísticas VM/IO/CPU |
| **free / /proc/meminfo** | Memória |
| **lsof / fuser** | Open files |
| **cgroups / systemd-run** | Resource control |

### 8. Hardware & Sensores

| Ferramenta | Função |
|------------|--------|
| **lscpu / lspci / lsusb / lshw** | Hardware listing |
| **dmidecode** | SMBIOS/DMI table (requer root) |
| **sensors (lm-sensors)** | Temperaturas, voltagens, fans |
| **cpupower / cpufrequtils** | CPU frequency scaling |
| **thermald / tlp / power-profiles-daemon** | Power management |

### 9. Segurança & Hardening

| Ferramenta | Função |
|------------|--------|
| **passwd / usermod / chage** | User management |
| **sudo / visudo / /etc/sudoers.d** | Privilege escalation |
| **ssh / sshd_config / ssh-keygen** | SSH hardening |
| **ufw / firewalld / nftables / iptables** | Firewall |
| **fail2ban / crowdsec** | Intrusion prevention |
| **lynis / rkhunter / chkrootkit** | Security auditing |
| **apparmor / selinux / tomoyo** | MAC (Mandatory Access Control) |
| **systemd-homed / cryptsetup / LUKS** | Encryption |

### 10. Backup & Recovery

| Ferramenta | Função |
|------------|--------|
| **rsync / rdiff-backup / borg / restic** | Backup incremental |
| **tar / cpio / pax** | Archiving |
| **dd / ddrescue / clonezilla** | Disk imaging |
| **timeshift / snapper / btrfs snapshots** | System snapshots |
| **rear / mondoarchive** | Disaster recovery |

---

## Script Principal: linux_maintenance.py

### Estrutura de Comandos

```bash
# Health check completo
python linux_maintenance.py health

# Disco: fsck (dry-run), smart, trim
python linux_maintenance.py disk --device /dev/sda --smart --trim

# Sistema: systemd, kernel, pacotes
python linux_maintenance.py system --services --kernel --packages

# Logs: journalctl erros recentes
python linux_maintenance.py logs --errors --days 7 --output errors.log

# Boot: grub, initramfs, efibootmgr
python linux_maintenance.py boot --grub --initramfs --efi

# Rede: interfaces, DNS, firewall
python linux_maintenance.py network --interfaces --dns --firewall

# Hardware: sensores, CPU, PCI
python linux_maintenance.py hardware --sensors --cpu --pci

# Segurança: audit, ssh, firewall
python linux_maintenance.py security --audit --ssh --firewall

# Relatório completo (JSON)
python linux_maintenance.py report --json --output report.json
```

### Classes Principais

- `LinuxMaintenance` — Orquestrador principal
- `DiskHealth` — fsck, smartctl, fstrim, lsblk, nvme
- `SystemdManager` — systemctl, journalctl, systemd-analyze
- `KernelBoot` — dmesg, grub, efibootmgr, initramfs, sysctl
- `PackageManager` — apt/dnf/pacman/zypper detection + ops
- `LogManager` — journalctl, auditd, logrotate
- `NetworkDiagnostics` — ip, ss, nmcli, dig, curl
- `ProcessResources` — ps, top, vmstat, free, cgroups
- `HardwareSensors` — lscpu, lspci, sensors, dmidecode
- `SecurityHardening` — ssh, firewall, audit, apparmor/selinux

---

## Exemplo de Uso Programático

```python
from linux_maintenance import LinuxMaintenance

lm = LinuxMaintenance()

# Health check completo
report = lm.full_health_check()
print(report.summary)

# Verificar SMART do disco
lm.disk.smart_health("/dev/sda")

# TRIM SSD
lm.disk.trim_all()

# Verificar serviços falhados
lm.systemd.failed_services()

# Análise de boot
lm.kernel.boot_analysis()

# Atualizar pacotes (dry-run)
lm.packages.update_check()

# Exportar logs de erro
lm.logs.export_errors(days=3, priority=3)
```

---

## Pré-requisitos

- Linux (qualquer distro moderna com systemd)
- Python 3.8+
- **Root/sudo** para operações de reparo (fsck, smartctl -t, systemctl, firewall, etc.)
- Pacotes recomendados: `smartmontools`, `sysstat`, `lm-sensors`, `nvme-cli`, `iproute2`, `util-linux`

---

## Detecção Automática de Distro

O script detecta automaticamente:
- **Package manager**: apt, dnf, yum, pacman, zypper, apk
- **Init system**: systemd, openrc, runit (foco em systemd)
- **Filesystems**: ext4, xfs, btrfs, f2fs, zfs
- **Bootloader**: GRUB2, systemd-boot, efibootmgr

---

## Segurança & Boas Práticas

1. **Sempre use sudo** para operações destrutivas/reparadoras
2. **Dry-run primeiro** — fsck -n, smartctl -t short, etc.
3. **Backup configurações** antes de modificar (/etc, /boot, grub)
4. **Verifique filesystem** antes de fsck (umount ou read-only)
5. **Monitore SMART** antes de reparos agressivos
6. **Log tudo** — o script gera auditoria em `/var/log/os-maintenance/` ou `$HOME/.local/log/os-maintenance/`

---

## Integração com EcoSystemUmGrau

- Registra aprendizados via `memory_engine.py` (tipo: `padrao`, tags: `linux,maintenance`)
- Checkpoint de estado via `runtime_state.py`
- Compatível com `@sync` para versionamento
- Auditoria via `preflight_check.py` antes de operações críticas