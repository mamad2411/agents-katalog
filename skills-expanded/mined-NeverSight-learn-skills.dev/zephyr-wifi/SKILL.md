---
name: zephyr-wifi
description: Expert guidance for WiFi development in Zephyr OS. Covers Station (STA) and Access Point (AP) modes, scanning, connection management, security types (WPA2-PSK, WPA3-SAE, EAP-TLS), power save modes, and Target Wake Time (TWT). Use when implementing WiFi connectivity, configuring network parameters, handling scan results, managing connections, or troubleshooting WiFi issues.
---

# Zephyr WiFi

## Quick Start

1. **Enable WiFi**: `CONFIG_WIFI=y` and driver (e.g., `CONFIG_WIFI_NRF70=y`) in `prj.conf`
2. **Enable Management API**: `CONFIG_NET_L2_WIFI_MGMT=y`
3. **Choose Mode**: STA (station) or AP (access point)
4. **Get Interface**: `net_if_get_wifi_sta()` or `net_if_get_wifi_sap()`
5. **Connect/Enable AP**: Use `net_mgmt()` with `NET_REQUEST_WIFI_*` commands

## Core Initialization Pattern

```c
#include <zephyr/net/net_if.h>
#include <zephyr/net/wifi_mgmt.h>
#include <zephyr/net/net_mgmt.h>

static struct net_mgmt_event_callback wifi_cb;

static void wifi_event_handler(struct net_mgmt_event_callback *cb,
                               uint32_t mgmt_event, struct net_if *iface)
{
    switch (mgmt_event) {
    case NET_EVENT_WIFI_CONNECT_RESULT:
        /* Handle connection result */
        break;
    case NET_EVENT_WIFI_DISCONNECT_RESULT:
        /* Handle disconnection */
        break;
    case NET_EVENT_WIFI_SCAN_RESULT:
        /* Handle scan result */
        break;
    case NET_EVENT_WIFI_SCAN_DONE:
        /* Scan complete */
        break;
    }
}

int main(void)
{
    struct net_if *iface = net_if_get_wifi_sta();
    if (!iface) {
        printk("WiFi interface not found\n");
        return -1;
    }

    /* Register event callbacks */
    net_mgmt_init_event_callback(&wifi_cb, wifi_event_handler,
                                 NET_EVENT_WIFI_CONNECT_RESULT |
                                 NET_EVENT_WIFI_DISCONNECT_RESULT |
                                 NET_EVENT_WIFI_SCAN_RESULT |
                                 NET_EVENT_WIFI_SCAN_DONE);
    net_mgmt_add_event_callback(&wifi_cb);

    /* Ready to scan/connect */
}
```

## WiFi Modes

| Mode | Interface Function | Description | Key Commands |
|------|-------------------|-------------|--------------|
| Station (STA) | `net_if_get_wifi_sta()` | Connects to access points | `NET_REQUEST_WIFI_CONNECT`, `NET_REQUEST_WIFI_SCAN` |
| Access Point (AP) | `net_if_get_wifi_sap()` | Creates a WiFi network | `NET_REQUEST_WIFI_AP_ENABLE`, `NET_REQUEST_WIFI_AP_DISABLE` |

## Detailed References

- **Station Mode (Scanning, Connecting)**: [references/sta_mode.md](references/sta_mode.md)
- **Access Point Mode**: [references/ap_mode.md](references/ap_mode.md)
- **Power Save & TWT**: [references/power_save.md](references/power_save.md)
- **Kconfig Options**: [references/kconfig.md](references/kconfig.md)
- **File Locations**: [references/locations.md](references/locations.md)

## Common Patterns

### Scan for Networks

```c
static void scan_result_handler(struct net_mgmt_event_callback *cb,
                                uint32_t mgmt_event, struct net_if *iface)
{
    if (mgmt_event == NET_EVENT_WIFI_SCAN_RESULT) {
        const struct wifi_scan_result *entry =
            (const struct wifi_scan_result *)cb->info;
        printk("SSID: %s, RSSI: %d, Security: %d\n",
               entry->ssid, entry->rssi, entry->security);
    }
}

/* Start scan */
int ret = net_mgmt(NET_REQUEST_WIFI_SCAN, iface, NULL, 0);
```

### Connect to Network (WPA2-PSK)

```c
struct wifi_connect_req_params params = {
    .ssid = "MyNetwork",
    .ssid_length = strlen("MyNetwork"),
    .psk = "MyPassword",
    .psk_length = strlen("MyPassword"),
    .security = WIFI_SECURITY_TYPE_PSK,
    .channel = WIFI_CHANNEL_ANY,
    .band = WIFI_FREQ_BAND_UNKNOWN,  /* Auto-select */
};

int ret = net_mgmt(NET_REQUEST_WIFI_CONNECT, iface, &params, sizeof(params));
```

### Disconnect

```c
int ret = net_mgmt(NET_REQUEST_WIFI_DISCONNECT, iface, NULL, 0);
```

### Get Interface Status

```c
struct wifi_iface_status status = {0};
int ret = net_mgmt(NET_REQUEST_WIFI_IFACE_STATUS, iface, &status, sizeof(status));
if (ret == 0 && status.state >= WIFI_STATE_ASSOCIATED) {
    printk("Connected to: %s\n", status.ssid);
    printk("RSSI: %d dBm\n", status.rssi);
}
```

## Security Types

| Type | Enum Value | Description |
|------|------------|-------------|
| Open | `WIFI_SECURITY_TYPE_NONE` | No security |
| WPA2-PSK | `WIFI_SECURITY_TYPE_PSK` | Pre-shared key (most common) |
| WPA2-PSK-SHA256 | `WIFI_SECURITY_TYPE_PSK_SHA256` | Enhanced PSK |
| WPA3-SAE | `WIFI_SECURITY_TYPE_SAE` | Simultaneous Auth of Equals |
| WPA3-SAE-H2E | `WIFI_SECURITY_TYPE_SAE_H2E` | Hash-to-Element SAE |
| EAP-TLS | `WIFI_SECURITY_TYPE_EAP_TLS` | Enterprise with certificates |
| WPA2/WPA3 Mixed | `WIFI_SECURITY_TYPE_WPA_AUTO_PERSONAL` | Auto-select personal |

## Minimum Kconfig for Station Mode

```
CONFIG_WIFI=y
CONFIG_WIFI_NRF70=y                    # Or your driver
CONFIG_NET_L2_WIFI_MGMT=y
CONFIG_NET_L2_ETHERNET=y
CONFIG_NETWORKING=y
CONFIG_NET_IPV4=y
CONFIG_NET_DHCPV4=y
```

## Minimum Kconfig for AP Mode

```
CONFIG_WIFI=y
CONFIG_WIFI_NRF70=y
CONFIG_NET_L2_WIFI_MGMT=y
CONFIG_WIFI_NM_WPA_SUPPLICANT=y        # Required for AP
CONFIG_WIFI_NM_WPA_SUPPLICANT_AP=y
CONFIG_NET_CONFIG_MY_IPV4_ADDR="192.168.1.1"
CONFIG_NET_CONFIG_MY_IPV4_NETMASK="255.255.255.0"
```

## Key Events

| Event | Description |
|-------|-------------|
| `NET_EVENT_WIFI_SCAN_RESULT` | Single scan result (called per AP found) |
| `NET_EVENT_WIFI_SCAN_DONE` | Scan complete |
| `NET_EVENT_WIFI_CONNECT_RESULT` | Connection attempt result |
| `NET_EVENT_WIFI_DISCONNECT_RESULT` | Disconnection notification |
| `NET_EVENT_WIFI_AP_ENABLE_RESULT` | AP mode enabled |
| `NET_EVENT_WIFI_AP_DISABLE_RESULT` | AP mode disabled |
| `NET_EVENT_WIFI_AP_STA_CONNECTED` | Client connected to AP |
| `NET_EVENT_WIFI_AP_STA_DISCONNECTED` | Client disconnected from AP |
| `NET_EVENT_WIFI_TWT` | TWT event (setup/teardown) |

## Power Save

Enable power save after connection:

```c
struct wifi_ps_params ps_params = {
    .enabled = WIFI_PS_ENABLED,
    .mode = WIFI_PS_MODE_WMM,  /* or WIFI_PS_MODE_LEGACY */
};

net_mgmt(NET_REQUEST_WIFI_PS, iface, &ps_params, sizeof(ps_params));
```

## Related Skills

- **zephyr-kconfig**: Configure `CONFIG_WIFI_*` and `CONFIG_NET_*` options
- **zephyr-devicetree**: WiFi driver device tree bindings
- **zephyr-shell-commands**: WiFi shell for debugging (`CONFIG_NET_SHELL=y`, `CONFIG_WIFI_SHELL=y`)
