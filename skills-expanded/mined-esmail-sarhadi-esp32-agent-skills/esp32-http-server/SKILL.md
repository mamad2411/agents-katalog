---
name: esp32-http-server
description: Use when an ESP32 serves HTTP or WebSocket - a handler never fires, large responses truncate, the server stops answering under load, or an upload kills the connection. Covers esp_http_server configuration and handler design.
license: MIT
---

# HTTP server on ESP32

`esp_http_server` is small, single-threaded per connection and configured by a
handful of `CONFIG_HTTPD_*` values that are easy to leave at defaults and then
blame on the network.

## Registration

One handler per URI, and the match function decides how strictly a URI must
match. Wildcard matching is **off by default**:

```c
httpd_config_t config = HTTPD_DEFAULT_CONFIG();
config.uri_match_fn = httpd_uri_match_wildcard;
```

Without that line, a handler registered for `/api/*` is never called and the
server returns 404 - which looks like a routing bug and is a config line.

## Limits that surface as "the server died"

| Limit | Symptom when exceeded |
|---|---|
| `max_uri_handlers` | the last registered handlers never fire |
| `max_open_sockets` | connections are refused once a browser opens several |
| header length | long cookies or auth headers are rejected |
| `stack_size` of the httpd task | crashes inside a handler that does real work |

## Do not block the handler

A handler runs on the server task. Sleeping, waiting on a queue, or doing a long
flash write inside it stalls every other connection. Copy the request, hand the
work to a queue, and respond from the worker - or accept that the server serves
one client at a time.

## Large responses

Send in chunks and yield. Building a 200 KB string in RAM to `httpd_resp_send()`
it in one call is a heap allocation that will fail on a fragmented heap, and the
failure looks like a truncated page.

## Uploads

`multipart/form-data` means parsing a boundary out of the body. If the client can
send a raw body instead, do that - it removes the parser, the boundary handling
and the size arithmetic in one move.

## WebSocket

`httpd_ws_*` handles the framing, but not the keep-alive. A socket with no traffic
for longer than the client's idle timeout closes with 1006 and no explanation.
Send a ping on a timer.

## Rules for the agent

- Set `uri_match_fn`, `max_uri_handlers` and the task stack explicitly. Defaults
  are tuned for a demo, not a product.
- Never do flash writes inside a handler.
- If a design needs TLS, use `httpd_ssl_start()` and budget the RAM for it - the
  handshake is the largest single allocation in the system.
