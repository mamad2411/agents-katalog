---
name: powerdns-authoritative-http-api
description: "PowerDNS Authoritative HTTP API skill. Use when working with PowerDNS Authoritative HTTP for error, servers. Covers 43 endpoints."
version: 1.0.0
generator: lapsh
---

# PowerDNS Authoritative HTTP API
API version: 0.0.17

## Auth
ApiKey X-API-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /error -- verify access
3. POST /servers/{server_id}/zones -- create first zones

## Endpoints

43 endpoints across 2 groups. See references/api-spec.lap for full details.

### error
| Method | Path | Description |
|--------|------|-------------|
| GET | /error | Will always generate an error |

### servers
| Method | Path | Description |
|--------|------|-------------|
| GET | /servers | List all servers |
| GET | /servers/{server_id} | List a server |
| PUT | /servers/{server_id}/cache/flush | Flush a cache-entry by name |
| GET | /servers/{server_id}/zones | List all Zones in a server |
| POST | /servers/{server_id}/zones | Creates a new domain, returns the Zone on creation. |
| GET | /servers/{server_id}/zones/{zone_id} | zone managed by a server |
| DELETE | /servers/{server_id}/zones/{zone_id} | Deletes this zone, all attached metadata and rrsets. |
| PATCH | /servers/{server_id}/zones/{zone_id} | Creates/modifies/deletes RRsets present in the payload and their comments. Returns 204 No Content on success. |
| PUT | /servers/{server_id}/zones/{zone_id} | Modifies basic zone data. |
| PUT | /servers/{server_id}/zones/{zone_id}/notify | Send a DNS NOTIFY to all secondaries. |
| PUT | /servers/{server_id}/zones/{zone_id}/axfr-retrieve | Retrieve secondary zone from its primary. |
| GET | /servers/{server_id}/zones/{zone_id}/export | Returns the zone in AXFR format. |
| PUT | /servers/{server_id}/zones/{zone_id}/rectify | Rectify the zone data. |
| GET | /servers/{server_id}/config | Returns all ConfigSettings for a single server |
| GET | /servers/{server_id}/config/{config_setting_name} | Returns a specific ConfigSetting for a single server |
| GET | /servers/{server_id}/statistics | Query statistics. |
| GET | /servers/{server_id}/search-data | Search the data inside PowerDNS |
| GET | /servers/{server_id}/zones/{zone_id}/metadata | Get all the Metadata associated with the zone. |
| POST | /servers/{server_id}/zones/{zone_id}/metadata | Creates a set of metadata entries |
| GET | /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind} | Get the content of a single kind of domain metadata as a Metadata object. |
| PUT | /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind} | Replace the content of a single kind of domain metadata. |
| DELETE | /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind} | Delete all items of a single kind of domain metadata. |
| GET | /servers/{server_id}/zones/{zone_id}/cryptokeys | Get all CryptoKeys for a zone, except the privatekey |
| POST | /servers/{server_id}/zones/{zone_id}/cryptokeys | Creates a Cryptokey |
| GET | /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id} | Returns all data about the CryptoKey, including the privatekey. |
| PUT | /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id} | This method (de)activates a key from zone_name specified by cryptokey_id |
| DELETE | /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id} | This method deletes a key specified by cryptokey_id. |
| GET | /servers/{server_id}/tsigkeys | Get all TSIGKeys on the server, except the actual key |
| POST | /servers/{server_id}/tsigkeys | Add a TSIG key |
| GET | /servers/{server_id}/tsigkeys/{tsigkey_id} | Get a specific TSIGKeys on the server, including the actual key |
| PUT | /servers/{server_id}/tsigkeys/{tsigkey_id} | The TSIGKey at tsigkey_id can be changed in multiple ways: |
| DELETE | /servers/{server_id}/tsigkeys/{tsigkey_id} | Delete the TSIGKey with tsigkey_id |
| GET | /servers/{server_id}/autoprimaries | Get a list of autoprimaries |
| POST | /servers/{server_id}/autoprimaries | Add an autoprimary |
| DELETE | /servers/{server_id}/autoprimaries/{ip}/{nameserver} | Delete the autoprimary entry |
| GET | /servers/{server_id}/views | List all views in a server |
| GET | /servers/{server_id}/views/{view} | List the contents of a given view |
| POST | /servers/{server_id}/views/{view} | Adds a zone to a given view, creating it if needed |
| DELETE | /servers/{server_id}/views/{view}/{id} | Removes the given zone from the given view |
| GET | /servers/{server_id}/networks | List all registered networks and views in a server |
| GET | /servers/{server_id}/networks/{ip}/{prefixlen} | Return the view associated to the given network |
| PUT | /servers/{server_id}/networks/{ip}/{prefixlen} | Sets the view associated to the given network |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all error?" -> GET /error
- "List all servers?" -> GET /servers
- "Get server details?" -> GET /servers/{server_id}
- "List all zones?" -> GET /servers/{server_id}/zones
- "Create a zone?" -> POST /servers/{server_id}/zones
- "Get zone details?" -> GET /servers/{server_id}/zones/{zone_id}
- "Delete a zone?" -> DELETE /servers/{server_id}/zones/{zone_id}
- "Partially update a zone?" -> PATCH /servers/{server_id}/zones/{zone_id}
- "Update a zone?" -> PUT /servers/{server_id}/zones/{zone_id}
- "List all export?" -> GET /servers/{server_id}/zones/{zone_id}/export
- "List all config?" -> GET /servers/{server_id}/config
- "Get config details?" -> GET /servers/{server_id}/config/{config_setting_name}
- "List all statistics?" -> GET /servers/{server_id}/statistics
- "Search search-data?" -> GET /servers/{server_id}/search-data
- "List all metadata?" -> GET /servers/{server_id}/zones/{zone_id}/metadata
- "Create a metadata?" -> POST /servers/{server_id}/zones/{zone_id}/metadata
- "Get metadata details?" -> GET /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind}
- "Update a metadata?" -> PUT /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind}
- "Delete a metadata?" -> DELETE /servers/{server_id}/zones/{zone_id}/metadata/{metadata_kind}
- "List all cryptokeys?" -> GET /servers/{server_id}/zones/{zone_id}/cryptokeys
- "Create a cryptokey?" -> POST /servers/{server_id}/zones/{zone_id}/cryptokeys
- "Get cryptokey details?" -> GET /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id}
- "Update a cryptokey?" -> PUT /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id}
- "Delete a cryptokey?" -> DELETE /servers/{server_id}/zones/{zone_id}/cryptokeys/{cryptokey_id}
- "List all tsigkeys?" -> GET /servers/{server_id}/tsigkeys
- "Create a tsigkey?" -> POST /servers/{server_id}/tsigkeys
- "Get tsigkey details?" -> GET /servers/{server_id}/tsigkeys/{tsigkey_id}
- "Update a tsigkey?" -> PUT /servers/{server_id}/tsigkeys/{tsigkey_id}
- "Delete a tsigkey?" -> DELETE /servers/{server_id}/tsigkeys/{tsigkey_id}
- "List all autoprimaries?" -> GET /servers/{server_id}/autoprimaries
- "Create a autoprimary?" -> POST /servers/{server_id}/autoprimaries
- "Delete a autoprimary?" -> DELETE /servers/{server_id}/autoprimaries/{ip}/{nameserver}
- "List all views?" -> GET /servers/{server_id}/views
- "Get view details?" -> GET /servers/{server_id}/views/{view}
- "Delete a view?" -> DELETE /servers/{server_id}/views/{view}/{id}
- "List all networks?" -> GET /servers/{server_id}/networks
- "Get network details?" -> GET /servers/{server_id}/networks/{ip}/{prefixlen}
- "Update a network?" -> PUT /servers/{server_id}/networks/{ip}/{prefixlen}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
