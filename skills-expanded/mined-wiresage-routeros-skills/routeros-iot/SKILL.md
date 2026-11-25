---
name: routeros-iot
description: Internet of Things features of MikroTik RouterOS 7 (the iot package). Covers the MQTT client (brokers, publish, subscribe, on-message scripts, TLS, last will), Bluetooth low energy scanning, advertising, whitelists and GATT connections, MikroTik Bluetooth tags and Beacon Manager, GPIO analog and digital pins with scripts, Modbus TCP and RTU on the RS485 port with security rules, LoRa and LoRaWAN gateways (channel plans, servers, filters, UDP, LNS, CUPS), Wiliot gateway mode, and cloud integrations (ThingsBoard, Kaa, AWS, Azure, ChirpStack, The Things Stack). Use when a MikroTik device such as KNOT, an LtAP or a router with a LoRa card must collect or forward sensor data, read GPIO, talk Modbus, or publish to MQTT.
---

# RouterOS IoT

Most features need the extra package `iot` (and `iot-bt-extra` for USB Bluetooth dongles on ARM and ARM64 devices with USB, LE 4.0 or newer; RouterOS 7.18
and later). Install it as described in `routeros-install-upgrade`, then check `/iot` exists. Hardware matters: Bluetooth chip and GPIO are on
KNOT-class devices (and RBM33G for GPIO), Modbus needs the RS485 port (KNOT, KNOT LR8G and LR9G kits), LoRa needs an R11e-LR2, LR8 or LR9 mini-PCIe card
(`routeros-hardware` has the product manuals and `find_product.py`).

## MQTT

RouterOS is an MQTT publisher and subscriber (from 7.11); a broker such as Mosquitto can run in a container (`routeros-containers`).

```ros
/iot/mqtt/brokers/add name=broker address=192.168.88.33 port=1883 client-id=router1 keep-alive=60 auto-connect=yes
/iot/mqtt/connect broker=broker
/iot/mqtt/publish broker=broker topic="site/router1/status" message="ok" qos=1 retain=no
/iot/mqtt/subscribe broker=broker topic="site/+/cmd" qos=1
/iot/mqtt/subscriptions/set 0 on-message="/log info \"mqtt message\""      # script runs per received message (7.12+)
/iot/mqtt/brokers/print
```

- `ssl=yes` plus `certificate` for TLS (`routeros-certificates`), `username` and `password` for broker login, `will-topic`, `will-message`, `will-qos`, `will-retain` for last will.
- `publish` and `subscribe` default to `force=yes`: they connect first if needed. `disconnect-after=yes` closes after one message. After subscribing
  on a connected broker the connection must be re-established. Wildcards `+` and `#` work for subscribing but not for publishing.
- `parallel-scripts-limit` (3 to 1000) caps concurrent `on-message` scripts to protect CPU. Message handling and script syntax: `routeros-scripting`.
- Examples for ThingsBoard, Kaa IoT, AWS (MQTT over HTTPS) and Azure are in `references/guides/internet-of-things/mqtt/` and the Bluetooth user guides.
  Credentials in scripts end up in exports: use dedicated broker accounts.

## Bluetooth

```ros
/iot/bluetooth/print
/iot/bluetooth/scanners/set [find device=bt1] disabled=no type=passive filter-duplicates=keep-newest
/iot/bluetooth/scanners/advertisements/print
/iot/bluetooth/whitelist/add address=AA:BB:CC:DD:EE:FF address-type=any device=bt1 comment=tag1
/iot/bluetooth/connections/connect pdev=DC:2C:6E:0F:C0:3D
```

- Scanner: `type` passive or active, `window` and `interval` (default 10 ms), `phy` (`1M`, `2M`, `CODED`), `filter-policy` whitelist to limit reports.
  Advertisements show `address`, `rssi`, `pdu-type`, `data` (hex) and `time`. `/iot/bluetooth/decode-ad` parses AD structures.
- Advertiser: `/iot/bluetooth/advertisers` with `ad-structures` (types such as `complete-local-name`, `manufacturer-data`), intervals 20 to 10240 ms, `channel-map`
  (37, 38, 39), `legacy=no` for up to 191 bytes. Advertising is disabled by default.
- GATT connections (7.12 beta9 and later) support the central role only: connect, read, write, subscribe, `async-data`, `characteristics`.
- MikroTik TG-BT5 tags run in four advertisement formats and are configured with the Beacon Manager app (Android, iOS); formats and the tracking
  setups with MQTT and ThingsBoard, e-mail on accelerometer, IFTTT, Azure and AWS are in the Bluetooth guides.
- Wiliot: gateway mode registers with the Wiliot portal and forwards pixel data over MQTT; bridge (energizer) mode is not implemented yet.

## GPIO

`/iot/gpio/analog` shows voltages (`value = adc_input + offset`; `set pin2 offset=2` compensates cable drop). `/iot/gpio/digital` pins have `direction`
(input or output), `output` 0 or 1 (open drain on KNOT output pins, whose direction is fixed), `input`, and `script` that runs whenever the value changes.
Pin names and counts differ per device (KNOT: two analog inputs, two digital outputs, one digital input). Pulse counting from a meter is in
`gpio/using-gpio-as-pulse-input-from-meter.md`. GPIO is CLI-only.

## Modbus

```ros
/iot/modbus/set disabled=no                                  # also check the "modbus" entry in /port
/iot/modbus/transceive address=1 function=3 data=20000001  # Modbus RTU from the CLI (7.10+)
/iot/modbus/set disable-security-rules=no
/iot/modbus/security-rules/add ip-range=192.168.88.0/24 allowed-function-codes=3,6
```

Modbus TCP server listens on `tcp-port` 502 (a Modbus client sends function codes to the device IP); the RS485 pair is A+/B- (swapped wires
mean no communication; add 120 ohm termination beyond about 50 m). `timeout` max 1000 ms, `interframe-gap` and `rx-switch-offset` tune half-duplex timing.
Security rules (7.12+) apply to Modbus TCP only and, once enabled, everything not allowed is blocked; allow port 502 in the firewall only from trusted networks.

## LoRa and LoRaWAN

A gateway is a device with an R11e-LR card and the `iot` package; it forwards uplink packets from nodes to a network server. Configure the gateway
under `/iot/lora` and the servers under `/iot/lora/servers`.

```ros
/iot/lora/servers/print                                     # predefined TTS Cloud and TTN V3 servers (eu1, nam1, au1)
/iot/lora/servers/add name=Chirpstack address=10.0.0.5 protocol=UDP     # your own server, UDP uses up-port and down-port 1700
/iot/lora/set [find] channel-plan=eu-868 servers="TTN V3 (eu1)"
/iot/lora/enable [find]                                      # starts forwarding; /iot/lora/traffic shows packets
```

- Properties: `channel-plan` (regional plans such as `eu-868`, `us-915`, `au-915`, `as-923`, `in-865`, `kr-920`, `ru-864`, `2.4-ghz`, `custom`), `antenna-gain` (setup
  gain minus cable loss), `forward` (`crc-validation`, `dev-addr-validation`, `proprietary-traffic`), `lbt-enabled`, `gateway-id` (needed to register with the server),
  `spoof-gps`. Protocols per server: `UDP`, `LNS` (WebSocket), `CUPS`. Filters by Join EUI and NetID restrict what is forwarded.
- Non-LoRaWAN raw payload forwarding to your own MQTT or HTTP endpoint is possible for uplink only; encrypted payloads must be deciphered server-side.
- Registration walkthroughs: The Things Stack, ChirpStack, AWS IoT Core for LoRaWAN, and the TG-LR82 and TG-LR92 sensor tags (`lora/user-guides/`).
- Use only the channel plan legal for your country.

## Where to look

| Need | Open |
| --- | --- |
| MQTT properties and cloud examples | `references/guides/internet-of-things/mqtt.md` and `mqtt/` |
| Bluetooth scanner, advertiser, connections, whitelist, tags | `references/guides/internet-of-things/bluetooth.md` and `bluetooth/` |
| GPIO | `references/guides/internet-of-things/gpio.md` |
| Modbus | `references/guides/internet-of-things/modbus.md` |
| LoRa gateway, filters, servers, user guides | `references/guides/internet-of-things/lora.md`, `lora/general-properties.md`, `lora/user-guides/` |
| Properties | `references/cli/iot/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-containers` (Mosquitto broker), `routeros-scripting` (on-message, GPIO scripts), `routeros-hardware` (KNOT, LoRa cards, ports),
`routeros-mobile-networking` (LTE/GPS uplink), `routeros-certificates`, `routeros-install-upgrade` (iot package).
