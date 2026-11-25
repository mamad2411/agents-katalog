---
name: esp32-wifi-enterprise-eap
description: Use when an ESP32 must join a WPA2-Enterprise network - corporate, campus or plant Wi-Fi - with EAP-TLS or PEAP. Covers certificates, time sync, identity fields and the failures that look like bad passwords.
license: MIT
---

# WPA2-Enterprise on ESP32

Enterprise Wi-Fi replaces the pre-shared key with 802.1X: the device authenticates
to a RADIUS server with a certificate or a username, and the AP only lets it
through after that succeeds.

## The three things that must be true

1. **The CA certificate is on the device** and matches the server's chain. Without
   it the device either fails or, worse, accepts any server - the "disable
   validation" option that turns 802.1X into theatre.
2. **The clock is plausible.** Certificate validity is a date range; at boot the
   ESP32 thinks it is 1970 and every certificate is "not yet valid". Start SNTP
   and wait for a real time before the first association attempt.
3. **The identity strings are exactly right.** `identity` (outer) and `username`
   (inner) are different fields. PEAP with MSCHAPv2 uses the username inside the
   tunnel; EAP-TLS uses the certificate's CN and often ignores both.

## EAP-TLS vs PEAP

| | EAP-TLS | PEAP/MSCHAPv2 |
|---|---|---|
| Credential | client certificate + key | username + password |
| Server needs | certificate per device | AD or RADIUS user |
| Provisioning | harder (unique certs) | easier |
| Revocation | CRL or short lifetimes | account disable |

For a fleet, unique client certificates are the right answer and the operational
cost is real: provisioning, renewal and revocation all need a process.

## Memory and timing

A TLS handshake inside EAP needs roughly the same heap as an HTTPS handshake -
tens of kilobytes. On a classic ESP32, start enterprise Wi-Fi before allocating
buffers for other work, and expect the first association to take several seconds.

## Symptom table

| Symptom | Usually |
|---|---|
| association fails immediately | wrong SSID security mode, or no CA |
| fails only after a power cut | clock reset, certificate not yet valid |
| "authentication failed" with correct password | username vs identity fields swapped |
| works on one AP, not another | different RADIUS server or certificate |
| disconnects every hour | session timeout on the RADIUS side |
| heap exhausted during connect | TLS handshake with too little free heap |

## Agent rules

- Never propose disabling certificate validation; name the CA instead.
- State the EAP method, the identity fields and where the certificates live.
- Include the time-sync step in the connection sequence.
