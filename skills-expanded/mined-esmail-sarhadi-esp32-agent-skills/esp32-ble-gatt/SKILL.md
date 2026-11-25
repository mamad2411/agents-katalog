---
name: esp32-ble-gatt
description: Use when building or debugging a BLE peripheral on ESP32 - the phone cannot see the device, notifications stop after a reconnect, throughput is a tenth of what was expected, or pairing works once and never again. Covers GATT design, MTU, connection parameters and bonding.
license: MIT
---

# BLE GATT on ESP32

BLE failures on ESP32 are almost never in the GATT table. They are in the four
numbers that decide whether a link survives, and in the fact that a bond lives on
the phone, not on the board.

## The four numbers

| Parameter | Unit | Typical | What breaks it |
|---|---|---|---|
| Connection interval | 1.25 ms | 7.5-50 ms | too long for the latency you promised, too short for battery |
| Slave latency | intervals | 0-4 | lets the peripheral skip N events; raises effective latency |
| Supervision timeout | 10 ms | 4-6 s | must exceed `(1 + latency) x interval x 2`, or the link drops on a stall |
| MTU | bytes | 23 default, 247 negotiated | a 20-byte write limit if nobody negotiates |

The supervision timeout rule is the one that bites: a client that asks for a 4 s
interval with latency 3 and a 4 s timeout has asked for a link that cannot stay
up. Validate the parameters you accept in the connection-update callback instead
of accepting whatever the phone proposes.

## Payload size

Default ATT MTU is 23, which leaves **20 bytes** of payload. Anything larger
needs either an MTU exchange or a long write with prepared writes. A
characteristic defined as 512 bytes does not mean 512 bytes arrive in one event.

On NimBLE, negotiate explicitly before advertising:

```cpp
NimBLEDevice::init("sensor");
NimBLEDevice::setMTU(247);
```

## Notify and indicate

`notify` is unacknowledged, `indicate` waits for a confirmation. Indicate costs a
round trip per packet; use it only where losing a message is unacceptable.

## The bond is on the phone

Re-flashing the board erases its keys. The phone still holds the old bond and
will refuse to re-pair, usually silently. Delete the bond on the phone, or call
`esp_ble_remove_bond_device()` / `NimBLEDevice::deleteBond()` before re-advertising.

Corollary: subscriptions do not survive a reconnect either. Re-subscribe in the
connect handler every time.

## Radio coexistence

BLE and Wi-Fi share one radio. A device that streams BLE at 100 Hz and also
holds a Wi-Fi connection will lose packets on both. If the product needs both,
plan the timing: batch the BLE notifications, or accept the throughput drop and
measure it rather than assuming it.

## Checklist before blaming the stack

- Is the device actually advertising? Check with nRF Connect, not with your own app.
- Does the service UUID in the advertisement match the one the app filters on?
- Is the characteristic property set to `READ | NOTIFY` and not just `READ`?
- Did you call `setValue()` **and** `notify()`? Setting the value alone sends nothing.

## Reference

`reference/ble-numbers.md` - the parameter ranges, the timeout inequality and the
payload sizes in one table.
