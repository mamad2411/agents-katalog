---
name: ix-api
description: "IX-API API skill. Use when working with IX-API for auth, facilities, devices. Covers 115 endpoints."
version: 1.0.0
generator: lapsh
---

# IX-API
API version: 2.7.1

## Auth
Bearer bearer | OAuth2

## Base URL
/api/v2

## Setup
1. Set Authorization header with your Bearer token
2. GET /facilities -- verify access
3. POST /auth/token -- create first token

## Endpoints

115 endpoints across 27 groups. See references/api-spec.lap for full details.

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/token | Create Auth Token |
| POST | /auth/refresh | Refresh Auth Token |

### facilities
| Method | Path | Description |
|--------|------|-------------|
| GET | /facilities | List (Query) |
| GET | /facilities/{id} | Read |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /devices | List (Query) |
| GET | /devices/{id} | Read |

### pops
| Method | Path | Description |
|--------|------|-------------|
| GET | /pops | List (Query) |
| GET | /pops/{id} | Read |

### metro-area-networks
| Method | Path | Description |
|--------|------|-------------|
| GET | /metro-area-networks | List (Query) |
| GET | /metro-area-networks/{id} | Read |

### metro-areas
| Method | Path | Description |
|--------|------|-------------|
| GET | /metro-areas | List (Query) |
| GET | /metro-areas/{id} | Read |

### product-offerings
| Method | Path | Description |
|--------|------|-------------|
| GET | /product-offerings | List (Query) |
| GET | /product-offerings/{id} | Read |

### availability-zones
| Method | Path | Description |
|--------|------|-------------|
| GET | /availability-zones | List (Query) |
| GET | /availability-zones/{id} | Read |

### ports
| Method | Path | Description |
|--------|------|-------------|
| GET | /ports | List (Query) |
| GET | /ports/{id} | Read |
| GET | /ports/{id}/statistics | Read Statistics |
| GET | /ports/{id}/statistics/{aggregate}/timeseries | Read Statistics Timeseries |

### port-reservations
| Method | Path | Description |
|--------|------|-------------|
| GET | /port-reservations | List (Query) |
| POST | /port-reservations | Create |
| GET | /port-reservations/{id} | Read |
| PUT | /port-reservations/{id} | Update (Deprecated) |
| PATCH | /port-reservations/{id} | Update |
| DELETE | /port-reservations/{id} | Request Decommission |
| GET | /port-reservations/{id}/cancellation-policy | Read Cancellation Policy |
| GET | /port-reservations/{id}/loa | Download LOA |
| POST | /port-reservations/{id}/loa | Upload LOA |

### connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /connections | List (Query) |
| POST | /connections | Create |
| GET | /connections/{id} | Read |
| PUT | /connections/{id} | Update (Deprecated) |
| PATCH | /connections/{id} | Update |
| DELETE | /connections/{id} | Request Decommission |
| GET | /connections/{id}/statistics | Read Statistics |
| GET | /connections/{id}/statistics/{aggregate}/timeseries | Read Statistics Timeseries |
| GET | /connections/{id}/loa | Download LOA |
| POST | /connections/{id}/loa | Upload LOA |
| GET | /connections/{id}/cancellation-policy | Read Cancellation Policy |

### network-service-configs
| Method | Path | Description |
|--------|------|-------------|
| GET | /network-service-configs | List (Query) |
| POST | /network-service-configs | Create |
| GET | /network-service-configs/{id} | Read |
| PUT | /network-service-configs/{id} | Update (Deprecated) |
| PATCH | /network-service-configs/{id} | Update |
| DELETE | /network-service-configs/{id} | Request Decommission |
| GET | /network-service-configs/{id}/statistics | Read Statistics |
| GET | /network-service-configs/{id}/statistics/{aggregate}/timeseries | Read Statistics Timeseries |
| GET | /network-service-configs/{id}/peer-statistics | Read Peer Statistics |
| GET | /network-service-configs/{id}/peer-statistics/{aggregate}/timeseries | Read Peer Statistics Timeseries |
| GET | /network-service-configs/{id}/cancellation-policy | Read Cancellation Policy |

### network-feature-configs
| Method | Path | Description |
|--------|------|-------------|
| GET | /network-feature-configs | List (Query) |
| POST | /network-feature-configs | Create |
| GET | /network-feature-configs/{id} | Read |
| PUT | /network-feature-configs/{id} | Update (Deprecated) |
| PATCH | /network-feature-configs/{id} | Update |
| DELETE | /network-feature-configs/{id} | Request Decommission |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Read |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List (Query) |
| POST | /accounts | Create |
| GET | /accounts/{id} | Read |
| PUT | /accounts/{id} | Update (Deprecated) |
| PATCH | /accounts/{id} | Update |
| DELETE | /accounts/{id} | Destroy |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles | List (Query) |
| GET | /roles/{id} | Read |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts | List (Query) |
| POST | /contacts | Create |
| GET | /contacts/{id} | Read |
| PUT | /contacts/{id} | Update (Deprecated) |
| PATCH | /contacts/{id} | Update |
| DELETE | /contacts/{id} | Destroy |

### role-assignments
| Method | Path | Description |
|--------|------|-------------|
| GET | /role-assignments | List (Query) |
| POST | /role-assignments | Create |
| GET | /role-assignments/{id} | Read |
| DELETE | /role-assignments/{id} | Destroy |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Read |

### implementation
| Method | Path | Description |
|--------|------|-------------|
| GET | /implementation | Read |

### extensions
| Method | Path | Description |
|--------|------|-------------|
| GET | /extensions | List (Query) |

### ips
| Method | Path | Description |
|--------|------|-------------|
| GET | /ips | List (Query) |
| POST | /ips | Create |
| GET | /ips/{id} | Read |
| PUT | /ips/{id} | Update |
| PATCH | /ips/{id} | Update |

### macs
| Method | Path | Description |
|--------|------|-------------|
| GET | /macs | List (Query) |
| POST | /macs | Create |
| GET | /macs/{id} | Read |
| DELETE | /macs/{id} | Destroy |

### network-services
| Method | Path | Description |
|--------|------|-------------|
| GET | /network-services | List (Query) |
| POST | /network-services | Create |
| GET | /network-services/{id} | Read |
| PUT | /network-services/{id} | Update (Deprecated) |
| PATCH | /network-services/{id} | Update |
| DELETE | /network-services/{id} | Request Decommission |
| GET | /network-services/{id}/statistics | Read Statistics |
| GET | /network-services/{id}/statistics/{aggregate}/timeseries | Read Statistics Timeseries |
| GET | /network-services/{id}/rtt-statistics | Read RTT Statistics |
| GET | /network-services/{id}/change-request | Read Change Request |
| POST | /network-services/{id}/change-request | Create Change Request |
| DELETE | /network-services/{id}/change-request | Delete Change Request |
| GET | /network-services/{id}/cancellation-policy | Read Cancellation Policy |

### network-features
| Method | Path | Description |
|--------|------|-------------|
| GET | /network-features | List (Query) |
| GET | /network-features/{id} | Read |

### member-joining-rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /member-joining-rules | List (Query) |
| POST | /member-joining-rules | Create |
| GET | /member-joining-rules/{id} | Read |
| PUT | /member-joining-rules/{id} | Update (Deprecated) |
| PATCH | /member-joining-rules/{id} | Update |
| DELETE | /member-joining-rules/{id} | Destroy |

### routing-functions
| Method | Path | Description |
|--------|------|-------------|
| GET | /routing-functions | List (Query) |
| POST | /routing-functions | Create |
| GET | /routing-functions/{id} | Read |
| PATCH | /routing-functions/{id} | Update |
| DELETE | /routing-functions/{id} | Request Decommission |
| GET | /routing-functions/{id}/cancellation-policy | Read Cancellation Policy |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a token?" -> POST /auth/token
- "Create a refresh?" -> POST /auth/refresh
- "List all facilities?" -> GET /facilities
- "Get facility details?" -> GET /facilities/{id}
- "List all devices?" -> GET /devices
- "Get device details?" -> GET /devices/{id}
- "List all pops?" -> GET /pops
- "Get pop details?" -> GET /pops/{id}
- "List all metro-area-networks?" -> GET /metro-area-networks
- "Get metro-area-network details?" -> GET /metro-area-networks/{id}
- "List all metro-areas?" -> GET /metro-areas
- "Get metro-area details?" -> GET /metro-areas/{id}
- "List all product-offerings?" -> GET /product-offerings
- "Get product-offering details?" -> GET /product-offerings/{id}
- "List all availability-zones?" -> GET /availability-zones
- "Get availability-zone details?" -> GET /availability-zones/{id}
- "List all ports?" -> GET /ports
- "Get port details?" -> GET /ports/{id}
- "List all statistics?" -> GET /ports/{id}/statistics
- "List all timeseries?" -> GET /ports/{id}/statistics/{aggregate}/timeseries
- "List all port-reservations?" -> GET /port-reservations
- "Create a port-reservation?" -> POST /port-reservations
- "Get port-reservation details?" -> GET /port-reservations/{id}
- "Update a port-reservation?" -> PUT /port-reservations/{id}
- "Partially update a port-reservation?" -> PATCH /port-reservations/{id}
- "Delete a port-reservation?" -> DELETE /port-reservations/{id}
- "List all cancellation-policy?" -> GET /port-reservations/{id}/cancellation-policy
- "List all loa?" -> GET /port-reservations/{id}/loa
- "Create a loa?" -> POST /port-reservations/{id}/loa
- "List all connections?" -> GET /connections
- "Create a connection?" -> POST /connections
- "Get connection details?" -> GET /connections/{id}
- "Update a connection?" -> PUT /connections/{id}
- "Partially update a connection?" -> PATCH /connections/{id}
- "Delete a connection?" -> DELETE /connections/{id}
- "List all statistics?" -> GET /connections/{id}/statistics
- "List all timeseries?" -> GET /connections/{id}/statistics/{aggregate}/timeseries
- "List all loa?" -> GET /connections/{id}/loa
- "Create a loa?" -> POST /connections/{id}/loa
- "List all cancellation-policy?" -> GET /connections/{id}/cancellation-policy
- "List all network-service-configs?" -> GET /network-service-configs
- "Create a network-service-config?" -> POST /network-service-configs
- "Get network-service-config details?" -> GET /network-service-configs/{id}
- "Update a network-service-config?" -> PUT /network-service-configs/{id}
- "Partially update a network-service-config?" -> PATCH /network-service-configs/{id}
- "Delete a network-service-config?" -> DELETE /network-service-configs/{id}
- "List all statistics?" -> GET /network-service-configs/{id}/statistics
- "List all timeseries?" -> GET /network-service-configs/{id}/statistics/{aggregate}/timeseries
- "List all peer-statistics?" -> GET /network-service-configs/{id}/peer-statistics
- "List all timeseries?" -> GET /network-service-configs/{id}/peer-statistics/{aggregate}/timeseries
- "List all cancellation-policy?" -> GET /network-service-configs/{id}/cancellation-policy
- "List all network-feature-configs?" -> GET /network-feature-configs
- "Create a network-feature-config?" -> POST /network-feature-configs
- "Get network-feature-config details?" -> GET /network-feature-configs/{id}
- "Update a network-feature-config?" -> PUT /network-feature-configs/{id}
- "Partially update a network-feature-config?" -> PATCH /network-feature-configs/{id}
- "Delete a network-feature-config?" -> DELETE /network-feature-configs/{id}
- "List all account?" -> GET /account
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{id}
- "Update a account?" -> PUT /accounts/{id}
- "Partially update a account?" -> PATCH /accounts/{id}
- "Delete a account?" -> DELETE /accounts/{id}
- "List all roles?" -> GET /roles
- "Get role details?" -> GET /roles/{id}
- "List all contacts?" -> GET /contacts
- "Create a contact?" -> POST /contacts
- "Get contact details?" -> GET /contacts/{id}
- "Update a contact?" -> PUT /contacts/{id}
- "Partially update a contact?" -> PATCH /contacts/{id}
- "Delete a contact?" -> DELETE /contacts/{id}
- "List all role-assignments?" -> GET /role-assignments
- "Create a role-assignment?" -> POST /role-assignments
- "Get role-assignment details?" -> GET /role-assignments/{id}
- "Delete a role-assignment?" -> DELETE /role-assignments/{id}
- "List all health?" -> GET /health
- "List all implementation?" -> GET /implementation
- "List all extensions?" -> GET /extensions
- "List all ips?" -> GET /ips
- "Create a ip?" -> POST /ips
- "Get ip details?" -> GET /ips/{id}
- "Update a ip?" -> PUT /ips/{id}
- "Partially update a ip?" -> PATCH /ips/{id}
- "List all macs?" -> GET /macs
- "Create a mac?" -> POST /macs
- "Get mac details?" -> GET /macs/{id}
- "Delete a mac?" -> DELETE /macs/{id}
- "List all network-services?" -> GET /network-services
- "Create a network-service?" -> POST /network-services
- "Get network-service details?" -> GET /network-services/{id}
- "Update a network-service?" -> PUT /network-services/{id}
- "Partially update a network-service?" -> PATCH /network-services/{id}
- "Delete a network-service?" -> DELETE /network-services/{id}
- "List all statistics?" -> GET /network-services/{id}/statistics
- "List all timeseries?" -> GET /network-services/{id}/statistics/{aggregate}/timeseries
- "List all rtt-statistics?" -> GET /network-services/{id}/rtt-statistics
- "List all change-request?" -> GET /network-services/{id}/change-request
- "Create a change-request?" -> POST /network-services/{id}/change-request
- "List all cancellation-policy?" -> GET /network-services/{id}/cancellation-policy
- "List all network-features?" -> GET /network-features
- "Get network-feature details?" -> GET /network-features/{id}
- "List all member-joining-rules?" -> GET /member-joining-rules
- "Create a member-joining-rule?" -> POST /member-joining-rules
- "Get member-joining-rule details?" -> GET /member-joining-rules/{id}
- "Update a member-joining-rule?" -> PUT /member-joining-rules/{id}
- "Partially update a member-joining-rule?" -> PATCH /member-joining-rules/{id}
- "Delete a member-joining-rule?" -> DELETE /member-joining-rules/{id}
- "List all routing-functions?" -> GET /routing-functions
- "Create a routing-function?" -> POST /routing-functions
- "Get routing-function details?" -> GET /routing-functions/{id}
- "Partially update a routing-function?" -> PATCH /routing-functions/{id}
- "Delete a routing-function?" -> DELETE /routing-functions/{id}
- "List all cancellation-policy?" -> GET /routing-functions/{id}/cancellation-policy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
