---
name: netatmo
description: "Netatmo API skill. Use when working with Netatmo for getpublicdata, getuser, devicelist. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Netatmo
API version: 1.1.5

## Auth
OAuth2 | OAuth2

## Base URL
https://api.netatmo.net/api

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /getpublicdata -- verify access
3. POST /syncschedule -- create first syncschedule

## Endpoints

22 endpoints across 22 groups. See references/api-spec.lap for full details.

### getpublicdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /getpublicdata | Retrieves publicly shared weather data from Outdoor Modules within a predefined area. |

### getuser
| Method | Path | Description |
|--------|------|-------------|
| GET | /getuser | The method getuser returns information about a user such as prefered language, prefered units, and list of devices. |

### devicelist
| Method | Path | Description |
|--------|------|-------------|
| GET | /devicelist | The method devicelist returns the list of devices owned by the user, and their modules. |

### getmeasure
| Method | Path | Description |
|--------|------|-------------|
| GET | /getmeasure | The method getmeasure returns the measurements of a device or a module. |

### getthermostatsdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /getthermostatsdata | The method getthermostatsdata returns information about user's thermostats such as their last measurements. |

### getstationsdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /getstationsdata | The method getstationsdata Returns data from a user's Weather Stations (measures and device specific data). |

### gethomecoachsdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /gethomecoachsdata | The method gethomecoachsdata Returns data from a user Healthy Home Coach Station (measures and device specific data). |

### getthermstate
| Method | Path | Description |
|--------|------|-------------|
| GET | /getthermstate | The method getthermstate returns the last Thermostat measurements, its current weekly schedule, and, if present, its current manual temperature setpoint. |

### syncschedule
| Method | Path | Description |
|--------|------|-------------|
| POST | /syncschedule | The method syncschedule changes the Thermostat weekly schedule. |

### setthermpoint
| Method | Path | Description |
|--------|------|-------------|
| POST | /setthermpoint | The method setthermpoint changes the Thermostat manual temperature setpoint. |

### switchschedule
| Method | Path | Description |
|--------|------|-------------|
| POST | /switchschedule | The method switchschedule switches the Thermostat's schedule to another existing schedule. |

### createnewschedule
| Method | Path | Description |
|--------|------|-------------|
| POST | /createnewschedule | The method createnewschedule creates a new schedule stored in the backup list. |

### partnerdevices
| Method | Path | Description |
|--------|------|-------------|
| GET | /partnerdevices | The method partnerdevices returns the list of device_id to which your partner application has access to. |

### gethomedata
| Method | Path | Description |
|--------|------|-------------|
| GET | /gethomedata | Returns information about users homes and cameras. |

### getcamerapicture
| Method | Path | Description |
|--------|------|-------------|
| GET | /getcamerapicture | Returns the snapshot associated to an event. |

### geteventsuntil
| Method | Path | Description |
|--------|------|-------------|
| GET | /geteventsuntil | Returns the snapshot associated to an event. |

### getlasteventof
| Method | Path | Description |
|--------|------|-------------|
| GET | /getlasteventof | Returns most recent events. |

### getnextevents
| Method | Path | Description |
|--------|------|-------------|
| GET | /getnextevents | Returns previous events. |

### setpersonsaway
| Method | Path | Description |
|--------|------|-------------|
| POST | /setpersonsaway | Sets a person as 'Away' or the Home as 'Empty'. The event will be added to the user’s timeline. |

### setpersonshome
| Method | Path | Description |
|--------|------|-------------|
| POST | /setpersonshome | Sets a person as 'At home'. |

### addwebhook
| Method | Path | Description |
|--------|------|-------------|
| GET | /addwebhook | Links a callback url to a user. |

### dropwebhook
| Method | Path | Description |
|--------|------|-------------|
| GET | /dropwebhook | Dissociates a webhook from a user. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all getpublicdata?" -> GET /getpublicdata
- "List all getuser?" -> GET /getuser
- "List all devicelist?" -> GET /devicelist
- "List all getmeasure?" -> GET /getmeasure
- "List all getthermostatsdata?" -> GET /getthermostatsdata
- "List all getstationsdata?" -> GET /getstationsdata
- "List all gethomecoachsdata?" -> GET /gethomecoachsdata
- "List all getthermstate?" -> GET /getthermstate
- "Create a syncschedule?" -> POST /syncschedule
- "Create a setthermpoint?" -> POST /setthermpoint
- "Create a switchschedule?" -> POST /switchschedule
- "Create a createnewschedule?" -> POST /createnewschedule
- "List all partnerdevices?" -> GET /partnerdevices
- "List all gethomedata?" -> GET /gethomedata
- "List all getcamerapicture?" -> GET /getcamerapicture
- "List all geteventsuntil?" -> GET /geteventsuntil
- "List all getlasteventof?" -> GET /getlasteventof
- "List all getnextevents?" -> GET /getnextevents
- "Create a setpersonsaway?" -> POST /setpersonsaway
- "Create a setpersonshome?" -> POST /setpersonshome
- "List all addwebhook?" -> GET /addwebhook
- "List all dropwebhook?" -> GET /dropwebhook
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
