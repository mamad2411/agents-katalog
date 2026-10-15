---
name: zephyr-bluetooth-le
description: Expert guidance for Bluetooth Low Energy (BLE) development in Zephyr OS. Covers GAP roles (peripheral, central, broadcaster, observer), GATT services and characteristics, advertising, scanning, connections, pairing/bonding, and built-in services (BAS, DIS, HRS, NUS). Use when implementing BLE functionality, creating custom GATT services, configuring advertising data, handling connections, or troubleshooting BLE issues.
---

# Zephyr Bluetooth LE

## Quick Start

1. **Enable BLE**: `CONFIG_BT=y` in `prj.conf`
2. **Choose GAP Role**: See [GAP Roles](#gap-roles) section
3. **Initialize**: Call `bt_enable(NULL)` in `main()`
4. **Define Services**: Use GATT macros or built-in services
5. **Start Advertising/Scanning**: Based on role

## Core Initialization Pattern

```c
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/gatt.h>

int main(void)
{
    int err = bt_enable(NULL);
    if (err) {
        printk("Bluetooth init failed (err %d)\n", err);
        return 0;
    }

    /* If using persistent storage */
    if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
        settings_load();
    }

    /* Register connection callbacks, start advertising, etc. */
}
```

## GAP Roles

| Role | Kconfig | Description | Key APIs |
|------|---------|-------------|----------|
| Peripheral | `CONFIG_BT_PERIPHERAL=y` | Connectable advertiser, GATT server | `bt_le_adv_start()`, `bt_gatt_service_register()` |
| Central | `CONFIG_BT_CENTRAL=y` | Scans and connects, GATT client | `bt_le_scan_start()`, `bt_conn_le_create()` |
| Broadcaster | `CONFIG_BT_BROADCASTER=y` | Non-connectable advertiser | `bt_le_adv_start()` with non-conn params |
| Observer | `CONFIG_BT_OBSERVER=y` | Passive scanner | `bt_le_scan_start()` |

## Detailed References

- **GAP (Advertising, Scanning, Connections)**: [references/gap.md](references/gap.md)
- **GATT (Services, Characteristics, Client/Server)**: [references/gatt.md](references/gatt.md)
- **Built-in Services (BAS, DIS, HRS, NUS, OTS)**: [references/services.md](references/services.md)
- **Kconfig Options**: [references/kconfig.md](references/kconfig.md)
- **Resource Locations**: [references/locations.md](references/locations.md)

## Common Patterns

### Peripheral (GATT Server)

```c
/* Advertising data */
static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID16_ALL, BT_UUID_16_ENCODE(BT_UUID_HRS_VAL)),
};

static const struct bt_data sd[] = {
    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME,
            sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};

/* Start connectable advertising */
err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
```

### Central (GATT Client)

```c
/* Scan callback */
static void scan_cb(const bt_addr_le_t *addr, int8_t rssi,
                    uint8_t adv_type, struct net_buf_simple *buf)
{
    /* Check advertising data, connect if target found */
    bt_le_scan_stop();
    bt_conn_le_create(addr, BT_CONN_LE_CREATE_CONN,
                      BT_LE_CONN_PARAM_DEFAULT, &conn);
}

/* Start scanning */
err = bt_le_scan_start(BT_LE_SCAN_ACTIVE, scan_cb);
```

### Connection Callbacks

```c
static void connected(struct bt_conn *conn, uint8_t err)
{
    if (err) {
        printk("Connection failed (err 0x%02x)\n", err);
    } else {
        printk("Connected\n");
    }
}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
    printk("Disconnected (reason 0x%02x)\n", reason);
}

/* Static registration (preferred) */
BT_CONN_CB_DEFINE(conn_callbacks) = {
    .connected = connected,
    .disconnected = disconnected,
};
```

## Minimum Kconfig for Peripheral

```
CONFIG_BT=y
CONFIG_BT_PERIPHERAL=y
CONFIG_BT_DEVICE_NAME="My Device"
```

## Minimum Kconfig for Central

```
CONFIG_BT=y
CONFIG_BT_CENTRAL=y
CONFIG_BT_GATT_CLIENT=y
```

## Security (Pairing/Bonding)

Enable SMP: `CONFIG_BT_SMP=y`

```c
/* Set security level on connection */
bt_conn_set_security(conn, BT_SECURITY_L2);  /* Encrypted, no MITM */

/* Authentication callbacks for pairing */
static struct bt_conn_auth_cb auth_cb = {
    .passkey_display = passkey_display,
    .passkey_confirm = passkey_confirm,
    .cancel = auth_cancel,
};
bt_conn_auth_cb_register(&auth_cb);
```

Security levels:
- `BT_SECURITY_L1`: No encryption
- `BT_SECURITY_L2`: Encrypted, no MITM protection
- `BT_SECURITY_L3`: Encrypted + MITM (legacy pairing)
- `BT_SECURITY_L4`: Encrypted + MITM (LE Secure Connections)

## Persistent Storage

For bonding persistence:

```
CONFIG_BT_SETTINGS=y
CONFIG_FLASH=y
CONFIG_FLASH_MAP=y
CONFIG_NVS=y
CONFIG_SETTINGS=y
```

Call `settings_load()` after `bt_enable()`.

## Related Skills

- **zephyr-kconfig**: Configure `CONFIG_BT_*` options
- **zephyr-devicetree**: Flash partitions for bonding storage
- **zephyr-shell-commands**: BLE shell for debugging (`CONFIG_BT_SHELL=y`)
- **zephyr-settings**: Persistent storage backend selection
- **zephyr-cbor**: CBOR encoding/decoding for SMP over BLE payloads