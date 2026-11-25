---
name: mqtt-classroom
description: Connect to the classroom Mosquitto broker to control XIAO ESP32C6 boards and read their A0 sensor values over MQTT. Use when the user wants to list boards, turn a board's LED on/off, watch sensor readings, or debug why they cannot reach the broker.
---

# mqtt-classroom

Every XIAO ESP32C6 in the class publishes to one shared Mosquitto broker. This
skill wraps the `mosquitto_pub` / `mosquitto_sub` commands behind `skill.sh`.

## Broker

| | |
|---|---|
| Host | `192.168.0.49` (the instructor's laptop) |
| MQTT (TCP) | `1883` — boards, CLI, desktop clients |
| MQTT over WebSockets | `9001` — browser clients |
| Auth | anonymous, no username or password |

You must be on the **same WiFi** as the broker machine. The address is a private
LAN address; it is not reachable from outside the classroom network.

Override the defaults with environment variables if the instructor's IP changes:

```bash
export MQTT_HOST=192.168.0.49
export MQTT_PORT=1883
```

## Your device name

Save your board's name once and every command defaults to it:

```bash
./skill.sh name seongho    # save
./skill.sh name            # show what is saved
./skill.sh led on          # no id needed any more
```

It is stored in `~/.mqtt-classroom`. `MQTT_DEVICE` in the environment overrides
the saved value for one shell.

The name must match `DEVICE_NAME` in the board's `arduino_secrets.h` — that is
what decides the board's topic prefix. Two boards sharing a name will fight over
the same topics and repeatedly kick each other off the broker, so pick something
unique in the class.

## Topics

Each board owns a subtree keyed by its name (`DEVICE_NAME`, or `c6-` + the last
3 bytes of its MAC if that is left empty). The board prints its name on the
serial monitor at boot.

| Topic | Direction | Payload |
|---|---|---|
| `classroom/<id>/led/set` | you → board | `on`, `off`, `toggle` |
| `classroom/<id>/led/state` | board → you | `on`, `off` (retained) |
| `classroom/<id>/sensor/a0` | board → you | `{"raw":2048,"mv":1650}` every 2s |
| `classroom/<id>/status` | board → you | `online`, `offline` (retained, last will) |

`status` and `led/state` are retained, so a fresh subscriber learns the current
state immediately instead of waiting for the next change.

## Usage

```bash
./skill.sh name seongho     # save your board's name (once)
./skill.sh check            # is the broker reachable at all?
./skill.sh devices          # which boards are online
./skill.sh led on           # your board's LED on
./skill.sh led off
./skill.sh led seongho on   # or name another board explicitly
./skill.sh sensor           # stream your board's A0 readings
./skill.sh watch            # every message from your board
```

## Prerequisites

`skill.sh` needs the mosquitto command line clients:

- **Windows** — installer from <https://mosquitto.org/download/>, then add
  `C:\Program Files\mosquitto` to `PATH`. Run `skill.sh` from Git Bash.
- **macOS** — `brew install mosquitto`
- **Linux** — `sudo apt install mosquitto-clients`

## Dashboard

`web/dashboard.html` in this repo shows every node, how it is attached to the
broker, its live A0 value, and LED buttons. Open the file directly in a browser
— no server needed. Point it at another broker with
`dashboard.html?host=192.168.0.50`.

## Browser clients

For a web page, connect over WebSockets rather than TCP:

```js
// mqtt.js
const client = mqtt.connect('ws://192.168.0.49:9001')
client.subscribe('classroom/+/sensor/a0')
client.publish('classroom/c6-85ef58/led/set', 'on')
```

A browser cannot open a raw MQTT TCP socket, so port 1883 will not work from a
web page — that is what the 9001 listener exists for.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `check` fails, connection refused | Broker not running, or still bound to localhost only — the instructor must apply `broker/mosquitto.conf` |
| `check` fails, timeout | Wrong WiFi, or the broker machine's firewall is blocking the port |
| `devices` prints nothing | No board is powered on, or the boards cannot reach the broker |
| Board shows `offline` | It lost WiFi or power; its last will fired |
| LED command accepted but nothing happens | Wrong board id — confirm with `./skill.sh devices` |
| `mosquitto_sub not found` | Install the clients; `skill.sh` already looks in the default Windows install path |
| Board never appears, serial shows endless dots | WiFi SSID is case-sensitive (`ICEE`, not `icee`), and the board is 2.4GHz-only — a 5GHz-only SSID will never connect |
| Commands lag seconds or get skipped | Old firmware. WiFi modem sleep parks downlink packets and drops the MQTT socket; the current sketch calls `WiFi.setSleep(false)` |
