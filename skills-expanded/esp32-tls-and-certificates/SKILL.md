---
name: esp32-tls-and-certificates
description: Use when HTTPS on the ESP32 fails - the handshake times out, memory runs out, the certificate is rejected, or it works with the time unset and fails after. Covers mbedTLS memory, cert bundles, SNI and clock dependency.
license: MIT
---

# TLS on ESP32

A TLS handshake is the most memory-hungry thing a small ESP32 does. It needs
about 40 kB of heap for a 2048-bit RSA handshake (more for 4096-bit), and it
needs the clock to be roughly right.

## Memory first

`mbedtls_ssl_handshake` returning `-0x7F00` (ALLOC_FAILED) is not a certificate
problem. Before the handshake:

- Free heap should be at least 50 kB, and the largest free block matters more
  than the total.
- Do not hold a large String of the response body while connecting.
- One TLS connection at a time on a classic ESP32. Two concurrent handshakes
  usually fail.

`CONFIG_MBEDTLS_DYNAMIC_BUFFER` and the `MBEDTLS_SSL_IN_CONTENT_LEN` /
`OUT_CONTENT_LEN` settings trade throughput for memory; 4 kB in and 4 kB out is
enough for most API calls.

## Certificates

Three approaches, in increasing order of maintenance:

1. **Skip verification** (`client.setInsecure()`): works, and is a decision to
   accept any certificate, including an attacker's. Acceptable for a lab.
2. **Pin one CA**: small, and breaks the day the CA rotates its intermediate -
   which happens more often than people expect.
3. **Cert bundle** (`esp_crt_bundle_attach`): the roots of the major CAs,
   ~64 kB of flash, no RAM cost, and it survives rotation. This is the right
   default for a product.

A server whose chain includes an intermediate that is not sent will fail
verification on the ESP32 even though browsers hide it by fetching the
intermediate. Test with `openssl s_client -showcerts`.

## The clock, again

Certificate validity is a date range. At boot the ESP32 clock starts at 1970, so
every certificate is "not yet valid" and the handshake fails with
`MBEDTLS_ERR_X509_CERT_VERIFY_FAILED`. Either start SNTP and wait for a
plausible time before the first HTTPS request, or accept the risk of skipping
time validation - but know which one you did.

## SNI

Servers hosting many domains (Cloudflare, most CDNs) need the hostname in the
handshake. Arduino's `WiFiClientSecure` sets it when you call `connect(host,
port)`. A raw `IPAddress` connect does not, and the server returns the wrong
certificate - which looks like a verification failure on a valid site.

## TLS versions

ESP-IDF 5.x supports TLS 1.3, but it is not the default on every Arduino core.
A server that requires 1.3 (some do now) will fail with a protocol error on an
older core. Check `MBEDTLS_VERSION_STRING` before blaming the certificate.

| Symptom | Usually |
|---|---|
| `-0x7F00` during handshake | not enough heap, or two connections at once |
| certificate verify failed | wrong CA, missing intermediate, or clock at 1970 |
| works at home, fails at the customer | captive portal intercepting, or a proxy |
| handshake takes 8 seconds | RSA 4096, or a slow link - use ECDSA where possible |
| fails only after deep sleep | clock reset, time never re-synced |
