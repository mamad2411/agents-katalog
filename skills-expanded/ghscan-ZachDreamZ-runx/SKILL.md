---
name: nws-weather-openapi
description: Public weather provider proof over Runx's governed HTTP front.
---
# NWS Weather OpenAPI

Calls the public National Weather Service `api.weather.gov` `points` endpoint
through the first-class `http` front and seals the provider observation. The
endpoint is described by the official NWS OpenAPI document, but the runtime path
is deliberately the generic governed HTTP transport: no SDK, no provider client,
no fixture server, and no credentials.

Run with:

```sh
sh examples/nws-weather-openapi/run.sh
```
