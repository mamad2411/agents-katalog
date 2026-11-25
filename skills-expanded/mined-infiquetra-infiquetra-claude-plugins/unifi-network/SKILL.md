---
name: unifi-network
description: Manage UniFi network infrastructure — devices, clients, VLANs, firewall rules, traffic routes, port forwards, WLANs, VPN, DNS, DHCP, stats, and backups — via the UniFi OS API
---

# UniFi Network Skill

Interacts with the UniFi Network API on a UniFi Dream Machine (UDM) to manage network
infrastructure.

## Script

`./scripts/unifi_network_client.py` — every command below invokes it.

## When to use this skill

Use it when the request is about UniFi network infrastructure, for example:

- "show unifi devices" / "adopt a device" / "forget a device"
- "list unifi clients" / "block client" / "kick client"
- "unifi firewall"
- "create vlan" / "unifi network"
- "port forward"
- "traffic route"
- "wifi network" / "wlan"
- "vpn clients" / "vpn servers"
- "dns record"
- "dhcp leases"
- "network health" / "unifi stats" / "dpi" / "alarms"
- "unifi backup"

## Environment Setup

```bash
export UNIFI_API_KEY="your-api-key"          # required
export UNIFI_HOST="192.0.2.1"                # required, no default
export UNIFI_SITE="default"                  # optional, default: default
```

Generate an API key in UniFi OS → Settings → API Keys.

## Safety: Dry-Run by Default

All write operations preview what they will do without executing. Pass `--confirm` to execute:

```bash
# Preview (safe)
python unifi_network_client.py networks create --json '{"name":"IoT","vlan":30}'

# Execute
python unifi_network_client.py networks create --json '{"name":"IoT","vlan":30}' --confirm
```

## Commands

Twelve resource groups, fifty-two actions. Anything not listed here is not implemented.

### Devices
```bash
python unifi_network_client.py devices list
python unifi_network_client.py devices get --mac aa:bb:cc:dd:ee:ff
python unifi_network_client.py devices restart --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py devices adopt --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py devices forget --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py devices upgrade --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py devices locate --mac aa:bb:cc:dd:ee:ff --confirm
```

### Clients
```bash
python unifi_network_client.py clients list
python unifi_network_client.py clients list-history --limit 200
python unifi_network_client.py clients get --mac aa:bb:cc:dd:ee:ff
python unifi_network_client.py clients block --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py clients unblock --mac aa:bb:cc:dd:ee:ff --confirm
python unifi_network_client.py clients kick --mac aa:bb:cc:dd:ee:ff --confirm
```

### Networks (VLANs)
```bash
python unifi_network_client.py networks list
python unifi_network_client.py networks get --id <id>
python unifi_network_client.py networks create --json '{"name":"IoT","purpose":"corporate","vlan":30}' --confirm
python unifi_network_client.py networks update --id <id> --json '{"name":"IoT-Updated"}' --confirm
python unifi_network_client.py networks delete --id <id> --confirm
```

### Firewall Rules
```bash
python unifi_network_client.py firewall list
python unifi_network_client.py firewall get --id <id>
python unifi_network_client.py firewall create --json '{"name":"Block IoT","action":"drop","src_networkconf_id":"<id>"}' --confirm
python unifi_network_client.py firewall update --id <id> --json '{"enabled":false}' --confirm
python unifi_network_client.py firewall delete --id <id> --confirm
```

### Traffic Routes
```bash
python unifi_network_client.py traffic-routes list
python unifi_network_client.py traffic-routes get --id <id>
python unifi_network_client.py traffic-routes create --json '{"name":"Route IoT via VPN","enabled":true}' --confirm
python unifi_network_client.py traffic-routes update --id <id> --json '{"enabled":false}' --confirm
python unifi_network_client.py traffic-routes delete --id <id> --confirm
```

### Port Forwards
```bash
python unifi_network_client.py port-forwards list
python unifi_network_client.py port-forwards get --id <id>
python unifi_network_client.py port-forwards create --json '{"name":"Plex","fwd":"192.0.2.50","fwd_port":32400,"dst_port":32400,"proto":"tcp"}' --confirm
python unifi_network_client.py port-forwards update --id <id> --json '{"enabled":false}' --confirm
python unifi_network_client.py port-forwards delete --id <id> --confirm
```

### WLANs (Wireless Networks)
```bash
python unifi_network_client.py wlans list
python unifi_network_client.py wlans get --id <id>
python unifi_network_client.py wlans update --id <id> --json '{"enabled":false}' --confirm
```

### VPN
```bash
python unifi_network_client.py vpn list-clients
python unifi_network_client.py vpn list-servers
python unifi_network_client.py vpn get --id <id>
```

### DNS (Static Records)
```bash
python unifi_network_client.py dns list
python unifi_network_client.py dns get --id <id>
python unifi_network_client.py dns create --json '{"key":"proxmox.home","value":"192.0.2.7","record_type":"A"}' --confirm
python unifi_network_client.py dns update --id <id> --json '{"value":"192.0.2.8"}' --confirm
python unifi_network_client.py dns delete --id <id> --confirm
```

### DHCP Leases
```bash
python unifi_network_client.py dhcp list-leases
```

### Stats & Health
```bash
python unifi_network_client.py stats health
python unifi_network_client.py stats sysinfo
python unifi_network_client.py stats dpi
python unifi_network_client.py stats alarms
python unifi_network_client.py stats events --limit 20
```

### Backup
```bash
python unifi_network_client.py backup list
python unifi_network_client.py backup create --confirm
```

## Global Flags

```bash
--confirm       # execute a write operation instead of previewing it
--host HOST     # override UNIFI_HOST for one invocation
--site SITE     # override UNIFI_SITE for one invocation
--verify-ssl    # enable TLS certificate verification (off by default; the UDM is self-signed)
```
