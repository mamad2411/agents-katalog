---
name: zephyr-connectivity
description: "Networking and Bluetooth: Wi-Fi, Ethernet, TCP/IP, sockets, MQTT, HTTP, CoAP, LwM2M, TLS, DNS, BLE peripherals and centrals, GATT, advertising, pairing, bonding, or a device that will not connect."
license: Apache-2.0
metadata:
  author: zephyr-ai
  version: "0.10.0"
---

# Connectivity

> Example status: fenced snippets are illustrative unless an immediately preceding `zephyr-ai-example` metadata comment names a verified target and build command.

- **IP networking** — `references/networking.md`. The minimum working
  configuration, buffer sizing, the BSD socket API as Zephyr implements it, TLS
  credentials, Wi-Fi and Ethernet bring-up, and a diagnostic order for a device
  that will not connect.
- **Bluetooth Low Energy** — `references/bluetooth.md`. The host and controller
  split, the minimum working configuration, GATT service definition, connection
  parameters, and the settings bonds need to persist.

## What both get wrong in the same way

**Check every `CONFIG_` symbol before writing it.** Both stacks are configured
almost entirely through Kconfig, both renamed symbols between releases, and a
symbol that does not exist is ignored without a warning. `check_config` takes the
whole `prj.conf` and returns a verdict per line.

**Size the buffers deliberately.** The defaults are sized for a demonstration.
Under load, a stack that runs out of buffers does not report an error; it drops
work and slows down.

**Bringing up an interface that is already up returns `-EALREADY`, which is
success.** An interface configured to start automatically is up before the
application asks. Treating every non-zero return as failure produces a confident
report that the link is down while it is carrying traffic.

**Distinguish "not yet" from "never".** A stack that needs a second to acquire an
address and one that will never acquire one deserve different words and different
consequences. Wait, bounded, for the steady state before reporting it.

**Read a subsystem's documented return set before wrapping it.** `get_api`
reports the parameters and the return contract, including the codes that mean the
operation was already done.
