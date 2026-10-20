---
name: specialized
description: "Linux specialized topics - kernel, security hardening, performance"
sasmp_version: "1.3.0"
bonded_agent: linux-expert
bond_type: PRIMARY_BOND
---

# Specialized Skill

## Overview

Advanced Linux topics including kernel configuration, security hardening, and performance tuning.

## Capabilities

- **Kernel**: Configuration, modules, parameters
- **Security**: SELinux, AppArmor, hardening
- **Performance**: Tuning, profiling, optimization
- **Filesystems**: ext4, XFS, ZFS, Btrfs
- **Storage**: LVM, RAID, NVMe

## Examples

```bash
# Check kernel version
uname -r

# View kernel parameters
sysctl -a | grep vm

# Security audit
sudo lynis audit system
```

