---
name: miataru
description: "Miataru API skill. Use when working with Miataru for UpdateLocation, GetLocation, GetLocationGeoJSON. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Miataru
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://service.miataru.com/v1

## Setup
1. No auth setup needed
2. GET /GetLocationGeoJSON/{deviceID} -- verify access
3. POST /UpdateLocation -- create first UpdateLocation

## Endpoints

5 endpoints across 5 groups. See references/api-spec.lap for full details.

### UpdateLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateLocation | This method is used to update the location of a device. The device does not need to be known already to the Miataru server but it rather creates a unique identifier for itself in the client application. This unique identifier, or device ID is then used to address this particular device. |

### GetLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetLocation | To retrieve a specific devices latest known location the /GetLocation method is used. Please note that the MiataruConfig portion is optional. RequestMiataruDeviceID should be the ID of the device the request is sent from (or an identifier like an URL). |

### GetLocationGeoJSON
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetLocationGeoJSON/{deviceID} | Retrieves a devices Location in GeoJSON format. |

### GetLocationHistory
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetLocationHistory | Location History is stored on the server only if the client told the server to do so using the “EnableLocationHistory” setting in the Location Update requests. For transitions of enabling/disabling that functionality - Everytime a Location Update is received by the server with “EnableLocationHistory=false” the server removes all stored Location History till that point. There is a server-side setting that controls up to how many Location Updates the server is storing in the Location History before it removes the oldest one. To request the Location History of a particular device the client sends the following POST request to the GetLocationHistory service URL. Please note that the MiataruConfig portion is optional. RequestMiataruDeviceID should be the ID of the device the request is sent from (or an identifier like an URL). |

### GetVisitorHistory
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetVisitorHistory | Visitor History is stored on the server with every request to the location or location history information of a device. There is a server-side setting that controls up to how many Visitors the server is storing in the Visitor History before it removes the oldest one. To request the Visitor History of a particular device the client sends the following POST request to the GetVisitorHistory service URL. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a UpdateLocation?" -> POST /UpdateLocation
- "Create a GetLocation?" -> POST /GetLocation
- "Get GetLocationGeoJSON details?" -> GET /GetLocationGeoJSON/{deviceID}
- "Create a GetLocationHistory?" -> POST /GetLocationHistory
- "Create a GetVisitorHistory?" -> POST /GetVisitorHistory

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
