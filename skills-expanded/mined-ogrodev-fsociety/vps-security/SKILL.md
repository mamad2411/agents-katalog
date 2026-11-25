---
name: vps-security
description: |
  This skill covers end-to-end VPS security for red team attack infrastructure. Use it when
  the user mentions "VPS", "virtual private server", "cloud server", "droplet", "Linode",
  "Vultr", "Hetzner", "DigitalOcean", "AWS EC2", "OVH", "server provisioning", "LUKS",
  "dm-crypt", "full disk encryption", "encrypted disk", "remote server", "C2 server",
  "redirector", "team server", "attack infrastructure", "infra hardening", "server teardown",
  "burn server", "nuke VPS", "anonymous hosting", "bulletproof hosting", "crypto VPS",
  "port knocking", "encrypted swap", "VeraCrypt", "compartmentalization",
  "infrastructure compartmentalization", "unattended upgrades", "automatic updates",
  "server setup", "operator VPS", or discusses securing, provisioning, compartmentalizing,
  or destroying remote servers used in offensive operations. Also triggers when the user
  asks about anonymous VPS acquisition, C2 infrastructure hardening, redirector setup,
  domain fronting infrastructure, provider opsec, abuse report handling, or rapid
  infrastructure teardown. Strongly relevant for any engagement phase that involves
  standing up or tearing down attack infrastructure.
version: 2.0.0
---

# VPS Security

End-to-end security for red team attack infrastructure — from anonymous acquisition through hardened provisioning, encrypted storage, C2 deployment, continuous monitoring, and rapid teardown.

This skill treats every VPS as a disposable, compartmentalized node in an attack infrastructure graph. The goal is never "secure a server for production" — it is "make this node operationally useful while leaving zero forensic trail when it burns."

## Reference Files

| Reference | When to Read |
|-----------|-------------|
| `references/anonymous-acquisition.md` | Acquiring VPS anonymously — providers, payment, identity separation |
| `references/hardened-provisioning.md` | First-boot hardening playbook — SSH, firewall, port knocking, sysctl, updates |
| `references/encrypted-storage.md` | LUKS, VeraCrypt, encrypted swap, nuke keys, plausible deniability |
| `references/c2-infrastructure.md` | C2 hardening, redirectors, domain fronting, malleable profiles, TLS |
| `references/teardown-and-recovery.md` | Rapid teardown, secure wipe, snapshot destruction, backup/recovery |

## Opsec Profile Integration

Every action in this skill adapts to the active opsec profile. Check the current profile before starting any VPS work:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" show
```

| Profile | Acquisition | Provisioning | Monitoring | Teardown |
|---------|------------|--------------|------------|----------|
| **loud** | Any provider, credit card OK | Basic hardening, password SSH OK | Optional | Manual cleanup |
| **normal** | Mainstream provider, prepaid card | Key-only SSH, UFW, fail2ban | Logwatch daily | Delete VPS via panel |
| **stealth** | Privacy provider, crypto payment | Port knocking, no DNS, encrypted disk | Auditd + remote syslog | Secure wipe + snapshot delete |
| **paranoid** | Bulletproof/offshore, Monero only | Multi-layer: knock + Tor-only SSH, full LUKS | Real-time alerts, tripwire | Nuke key + header destroy + provider account burn |

## Workflow

### Phase 1 — Plan

1. Determine engagement requirements: how many VPS nodes, what roles (C2, redirector, phishing, exfil), which regions
2. Check opsec profile — this dictates every subsequent decision
3. Design the infrastructure graph: which nodes talk to which, what protocols, what domains
4. Read `references/anonymous-acquisition.md` for provider selection

### Phase 2 — Acquire

1. Acquire VPS nodes anonymously per opsec profile
2. Use separate identities per node (email, payment, provider account)
3. Log acquisition details via ops-tracker

### Phase 3 — Provision

1. Run the hardened provisioning playbook from `references/hardened-provisioning.md`
2. Set up encrypted storage per `references/encrypted-storage.md`
3. Configure C2/redirector infrastructure per `references/c2-infrastructure.md`
4. Log all provisioning steps

### Phase 4 — Operate

1. Monitor with auditd, tripwire, fail2ban — severity depends on opsec profile
2. Rotate SSH keys and access credentials periodically
3. Watch for provider abuse notifications
4. Maintain ops-tracker entries for all changes

### Phase 5 — Teardown

1. Follow rapid teardown procedures from `references/teardown-and-recovery.md`
2. Wipe data, destroy snapshots, burn accounts as profile dictates
3. Log final teardown actions

## Compartmentalization Principles

Compartmentalization is the single most important opsec practice for attack infrastructure. Every node should be isolated so that compromise of one does not expose others.

**Rules:**

- **One role per VPS**: never run C2 and phishing on the same box
- **Separate identities per VPS**: different email, different payment method, different provider if possible
- **No direct C2-to-target traffic**: always go through at least one redirector
- **Segment by engagement**: never reuse infrastructure across engagements
- **Network isolation**: VPS nodes communicate only through encrypted tunnels (WireGuard preferred); no direct SSH between nodes
- **Time-bound**: every VPS has a planned destruction date; extend only with justification

**Recommended architecture for a standard engagement:**

```
Target ←→ Redirector(s) ←→ C2 Team Server ←→ Operator (via Tor/VPN)
                                    ↕
                              Exfil Server (separate)
                                    ↕
                         Encrypted Backup (offline)
```

## Cross-Skill References

| Related Skill | When to Use |
|---------------|-------------|
| `system-hardening` | Deep kernel hardening, AppArmor/SELinux policies, CIS benchmarks |
| `network-anonymity` | Tor/VPN/proxychains for operator access to VPS, killswitch config |
| `anti-forensics` | Log manipulation, metadata stripping, secure deletion on VPS |
| `opsec-reporting` | Generating VPS security audit reports |

## Logging

All VPS security operations MUST be logged:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "vps-security" \
  --action "<action>" \
  --detail "<detail>"
```

Use these action types for consistency:
- `acquire` — VPS purchased/provisioned
- `provision` — Initial hardening applied
- `encrypt` — Disk/partition encryption configured
- `c2-deploy` — C2 or redirector deployed
- `monitor-setup` — Monitoring configured
- `rotate` — Credentials or keys rotated
- `teardown` — VPS wiped and destroyed
- `backup` — Encrypted backup created
- `incident` — Unexpected event (abuse report, anomaly detected)
