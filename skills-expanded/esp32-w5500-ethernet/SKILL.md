---
name: esp32-w5500-ethernet
description: Use when using W5500 SPI Ethernet with ESP32, diagnosing DHCP, socket failures, link loss, SPI timing or Ethernet/Wi-Fi coexistence.
license: MIT
---

# ESP32 W5500 Ethernet

W5500 is an SPI Ethernet controller with its own hardwired TCP/IP stack and socket resources. It is not the same architecture as an RMII PHY attached to an ESP32 Ethernet MAC. Choose the driver/API path accordingly.

## Hardware integration

- Verify module supply and logic voltage, SPI pin routing, CS, SCK, MOSI, MISO, RESET and interrupt wiring.
- Check the exact W5500 module schematic; some boards include regulators, level shifting, magnetics and RJ45 LEDs, others do not.
- Keep SPI traces short and validate clock rate against wiring, board layout and module quality.
- Provide stable reset sequencing and adequate supply decoupling.

## Driver and socket model

- Use the supported Ethernet library/IDF component for the selected framework release.
- Respect W5500 hardware socket count and buffer allocation; close sockets on every error path.
- Do not mix APIs for native lwIP Ethernet and W5500 offload sockets without understanding ownership.
- Bound DNS, connect, read and write timeouts; handle cable removal and DHCP lease loss.

## Diagnostics

- Verify link before DHCP, DHCP before DNS, DNS before TCP and TCP before application protocol.
- Log PHY/link status, assigned address, gateway, DNS, socket number and error code.
- Test a minimal ping/TCP client before adding WebSocket, MQTT or socket.io libraries.
- Capture SPI transactions and reset behavior when failures occur after long uptime.

## Regression matrix

| Scenario | Expected behavior |
|---|---|
| Cable absent at boot | Firmware remains responsive |
| Cable inserted later | Link and DHCP recover |
| DHCP unavailable | Bounded retry, no task starvation |
| Peer closes socket | Socket reclaimed |
| Repeated reconnect | No socket exhaustion or heap trend |
| Wi-Fi and W5500 together | Explicit routing and ownership behavior |

## Agent rules

- Name the exact W5500 driver and framework version.
- Do not call every post-DHCP crash a W5500 hardware fault; isolate driver, socket API and task context.
- Keep application protocol out of the Ethernet bring-up test.
- Record unresolved community reports as leads, not fixes.
