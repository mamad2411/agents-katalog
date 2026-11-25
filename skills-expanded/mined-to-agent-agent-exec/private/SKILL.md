# SKILL: private
# Endpoint: GET /private
# Description: Discover authenticated private skill surfaces

## Overview

Use `/private` and `/private/skills` to discover private skill documents.
Private skill documents require API_KEY and are not listed in public skill indexes by individual plugin name.

## Authentication

Required: `X-API-Key: <API_KEY>`.

## Request

```bash
curl -X GET http://<host>/private \
  -H "X-API-Key: <API_KEY>"
```

```bash
curl -X GET http://<host>/private/skills \
  -H "X-API-Key: <API_KEY>"
```

Request headers:

```json
{
  "X-API-Key": "API_KEY",
  "Accept": "text/sjs"
}
```
<!-- ae:prev request.headers -> all -->

## Response

`/private` returns authenticated navigation for private surfaces.
`/private/skills` returns the authenticated private skill index.

Private endpoint values:

```json
["/private/skills"]
```
<!-- ae:prev response.endpoints -> all -->

## Next step

Use `GET /private/skills` with API_KEY to discover available private skill documents.

Related private surfaces:

```json
["/private", "/private/skills"]
```
<!-- ae:prev refs -> all -->
