---
name: the-water-linked-underwater-gps-api
description: "The Water Linked Underwater GPS API skill. Use when working with The Water Linked Underwater GPS for api. Covers 38 endpoints."
version: 1.0.0
generator: lapsh
---

# The Water Linked Underwater GPS API

## Auth
No authentication required.

## Base URL
http://demo.waterlinked.com

## Setup
1. No auth setup needed
2. GET /api/ -- verify access
3. POST /api/v1/about/factoryreset -- create first factoryreset

## Endpoints

38 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/ | ApiVersion about |
| GET | /api/v1/about | Get about |
| POST | /api/v1/about/factoryreset | FactoryReset about |
| GET | /api/v1/about/led | LED about |
| GET | /api/v1/about/status | Status about |
| GET | /api/v1/about/temperature | Temperature about |
| GET | /api/v1/config/antenna | GetAntennaConfig config |
| PUT | /api/v1/config/antenna | ModifyAntennaConfig config |
| GET | /api/v1/config/generic | Get config |
| PUT | /api/v1/config/generic | Modify config |
| GET | /api/v1/config/ip | GetIP config |
| PUT | /api/v1/config/ip | ModifyIP config |
| GET | /api/v1/config/receivers/ | ListReceiver config |
| GET | /api/v1/config/receivers/{ID} | ShowReceiver config |
| PUT | /api/v1/config/receivers/{ID} | ModifyReceiver config |
| GET | /api/v1/config/wifi | GetWIFI config |
| PUT | /api/v1/config/wifi | ModifyWIFI config |
| PUT | /api/v1/external/depth | SetDepth external |
| GET | /api/v1/external/imu | GetVehicleIMU external |
| PUT | /api/v1/external/imu | SetVehicleIMU external |
| PUT | /api/v1/external/master | SetMaster external |
| GET | /api/v1/external/orientation | GetOrientation external |
| PUT | /api/v1/external/orientation | SetOrientation external |
| GET | /api/v1/imu/calibrate | Get imu |
| POST | /api/v1/imu/calibrate | Calibrate imu |
| POST | /api/v1/imu/resetgyros | ResetGyro imu |
| POST | /api/v1/imu/setnorth | SetNorth imu |
| GET | /api/v1/poi/ | List poi |
| POST | /api/v1/poi/ | Create poi |
| GET | /api/v1/poi/{ID} | Show poi |
| DELETE | /api/v1/poi/{ID} | Delete poi |
| PATCH | /api/v1/poi/{ID} | Update poi |
| GET | /api/v1/position/acoustic/filtered | AcousticFiltered position |
| GET | /api/v1/position/acoustic/raw | AcousticRaw position |
| GET | /api/v1/position/global | Get position |
| GET | /api/v1/position/master | GetMaster position |
| GET | /api/v1/status_report/ | Get status_report |
| GET | /api/v1/warnings/ | Get warnings |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api?" -> GET /api/
- "List all about?" -> GET /api/v1/about
- "Create a factoryreset?" -> POST /api/v1/about/factoryreset
- "List all led?" -> GET /api/v1/about/led
- "List all status?" -> GET /api/v1/about/status
- "List all temperature?" -> GET /api/v1/about/temperature
- "List all antenna?" -> GET /api/v1/config/antenna
- "List all generic?" -> GET /api/v1/config/generic
- "List all ip?" -> GET /api/v1/config/ip
- "List all receivers?" -> GET /api/v1/config/receivers/
- "Get receiver details?" -> GET /api/v1/config/receivers/{ID}
- "Update a receiver?" -> PUT /api/v1/config/receivers/{ID}
- "List all wifi?" -> GET /api/v1/config/wifi
- "List all imu?" -> GET /api/v1/external/imu
- "List all orientation?" -> GET /api/v1/external/orientation
- "List all calibrate?" -> GET /api/v1/imu/calibrate
- "Create a calibrate?" -> POST /api/v1/imu/calibrate
- "Create a resetgyro?" -> POST /api/v1/imu/resetgyros
- "Create a setnorth?" -> POST /api/v1/imu/setnorth
- "List all poi?" -> GET /api/v1/poi/
- "Create a poi?" -> POST /api/v1/poi/
- "Get poi details?" -> GET /api/v1/poi/{ID}
- "Delete a poi?" -> DELETE /api/v1/poi/{ID}
- "Partially update a poi?" -> PATCH /api/v1/poi/{ID}
- "List all filtered?" -> GET /api/v1/position/acoustic/filtered
- "List all raw?" -> GET /api/v1/position/acoustic/raw
- "List all global?" -> GET /api/v1/position/global
- "List all master?" -> GET /api/v1/position/master
- "List all status_report?" -> GET /api/v1/status_report/
- "List all warnings?" -> GET /api/v1/warnings/

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
