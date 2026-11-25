---
name: esp32-json-and-payloads
description: Use when JSON on the ESP32 is truncated, crashes, or leaks - the document is empty, the parse fails on a valid payload, floats lose precision, or the heap shrinks with every request. Covers ArduinoJson capacity, streaming and cJSON ownership.
license: MIT
---

# JSON on a microcontroller

JSON is text, and text on a 320 kB heap is a budget problem. The failures are
almost always capacity or lifetime, not syntax.

## Capacity is a promise you make in advance

ArduinoJson v6 sized documents statically: `JSON_OBJECT_SIZE(n)` plus the string
lengths. Guess too low and the document is silently truncated - `serializeJson`
writes what fits, with no error. v7 removed the static capacity and grows on the
heap instead, which fixes truncation and introduces fragmentation.

Either way: measure the payload. A 500 byte response parsed into a document with
room for 3 keys is a bug that only appears with the fourth key.

## Parse from a stream, not a String

`http.getString()` allocates the whole body twice (once in the client, once in
the String). `deserializeJson(doc, http.getStream())` reads it once, and on a
TLS connection the difference is tens of kilobytes of peak heap - which is
exactly what the handshake needs.

## Check the error, always

`DeserializationError err = deserializeJson(doc, payload);` and then switch on
`err`. `NoMemory` and `IncompleteInput` are different problems: one is capacity,
the other is a truncated body (chunked encoding, or a timeout mid-body).

## Numbers

- `float` on the ESP32 is 32-bit: 7 significant digits. A timestamp in
  milliseconds does not fit. Use `long long` / `uint64_t`.
- JSON has no integer type distinction; a value like `1700000000000` parsed into
  `int` overflows silently to a wrong number.
- Serialising a float prints 2 decimals by default in ArduinoJson - a voltage of
  3.2847 becomes 3.28 unless you set the decimals explicitly.

## cJSON: who frees what

If you use the IDF's cJSON rather than ArduinoJson, every `cJSON_Create*` and
every `cJSON_Parse` returns memory you must free with `cJSON_Delete`. Strings
from `cJSON_GetStringValue` are owned by the tree - copy them before deleting it.
A request handler that parses JSON and returns early on a validation error is the
classic leak: it happens a thousand times a day and the heap graph looks like a
sawtooth that never comes back.

## Payload size on the wire

MQTT has a practical 256 byte default buffer in many clients; a JSON document
with nested objects exceeds it and gets truncated at the broker. Either raise the
buffer or send a compact array. Binary formats (CBOR, protobuf) cut the payload
by 40 to 60 % and remove the parse allocation entirely.

| Symptom | Usually |
|---|---|
| document parses but fields are missing | capacity too small (v6), truncated body |
| parse fails on a payload that is valid | chunked transfer, or a BOM at the start |
| heap drops with every request | cJSON tree not deleted on an early return |
| numbers come out wrong | `int` overflow, or float precision |
| works with small payloads only | fixed buffer in the HTTP or MQTT client |
