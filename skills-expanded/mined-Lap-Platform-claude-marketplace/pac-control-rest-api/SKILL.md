---
name: pac-control-rest-api
description: "PAC Control REST API skill. Use when working with PAC Control REST for device. Covers 55 endpoints."
version: 1.0.0
generator: lapsh
---

# PAC Control REST API
API version: R1.0a

## Auth
basic

## Base URL
Not specified.

## Setup
1. Configure auth: basic
2. GET /device -- verify access
3. POST /device/strategy/ios/analogOutputs/{ioName}/eu -- create first eu

## Endpoints

55 endpoints across 1 groups. See references/api-spec.lap for full details.

### device
| Method | Path | Description |
|--------|------|-------------|
| GET | /device | Returns controller's type; firmware version; both mac addresses; and uptime in seconds |
| GET | /device/strategy | Returns the name, date, time, and CRC of the strategy currently in the controller, and the number of charts currently running. Empty strings and a 0 will be returned when there is no strategy. |
| GET | /device/strategy/ios/analogInputs | Returns the name and engineering units (EU) for all analog input points in the strategy |
| GET | /device/strategy/ios/analogInputs/{ioName}/eu | Reads the value in engineering units (EU) of the specified analog input |
| GET | /device/strategy/ios/analogOutputs | Returns the name and engineering units (EU) for all analog output points in the strategy |
| GET | /device/strategy/ios/analogOutputs/{ioName}/eu | Reads the value in engineering units (EU) of the specified analog output |
| POST | /device/strategy/ios/analogOutputs/{ioName}/eu | Sets the value of the specified analog output point |
| GET | /device/strategy/ios/digitalInputs | Returns the name and state (true = on, false = off) of all digital input points in the strategy. If there is no strategy in the controller, or the strategy includes no digital inputs, the returned array will be empty. |
| GET | /device/strategy/ios/digitalInputs/{ioName}/state | Returns the specified digital input point's state (true = on, false = off) |
| GET | /device/strategy/ios/digitalOutputs | Returns the name and state (true = on, false = off) of all digital output points in the strategy |
| GET | /device/strategy/ios/digitalOutputs/{ioName}/state | Returns the specified digital output point's state (true = on, false = off) |
| POST | /device/strategy/ios/digitalOutputs/{ioName}/state | Sets the value of the specified digital output point |
| GET | /device/strategy/tables/floats | Returns an array of the name and length of all the float tables in the strategy |
| GET | /device/strategy/tables/floats/{tableName} | Read table elements |
| POST | /device/strategy/tables/floats/{tableName} | Write table elements |
| GET | /device/strategy/tables/floats/{tableName}/{index} | Read specified table element |
| POST | /device/strategy/tables/floats/{tableName}/{index} | Write specified table element |
| GET | /device/strategy/tables/int32s | Returns an array of the name and length of all the integer32 tables in the strategy |
| GET | /device/strategy/tables/int32s/{tableName} | "Read a range of table elements from the specified integer32 table" |
| POST | /device/strategy/tables/int32s/{tableName} | "Write a range of table elements" |
| GET | /device/strategy/tables/int32s/{tableName}/{index} | Read specified integer32 table element |
| POST | /device/strategy/tables/int32s/{tableName}/{index} | Write specified integer32 table element |
| GET | /device/strategy/tables/int64s | Returns an array of the name and length of all the integer64 tables in the strategy |
| GET | /device/strategy/tables/int64s/{tableName} | "Read a range of table elements from the specified integer64 table" |
| POST | /device/strategy/tables/int64s/{tableName} | "Write a range of table elements" |
| GET | /device/strategy/tables/int64s/{tableName}/_string | "Read a range of table elements from the specified integer64 table" |
| POST | /device/strategy/tables/int64s/{tableName}/_string | "Write a range of table elements" |
| GET | /device/strategy/tables/int64s/{tableName}/{index} | Read specified integer64 table element |
| POST | /device/strategy/tables/int64s/{tableName}/{index} | Write specified integer64 table element |
| GET | /device/strategy/tables/int64s/{tableName}/{index}/_string | Read specified integer64 table element as string |
| POST | /device/strategy/tables/int64s/{tableName}/{index}/_string | Write specified integer64 table element as string |
| GET | /device/strategy/tables/strings | Returns an array of the name and length of all the string tables in the strategy |
| GET | /device/strategy/tables/strings/{tableName} | "Read a range of table elements from the specified string table" |
| POST | /device/strategy/tables/strings/{tableName} | "Write a range of table elements" |
| GET | /device/strategy/tables/strings/{tableName}/{index} | Read specified table element |
| POST | /device/strategy/tables/strings/{tableName}/{index} | Write specified table element |
| GET | /device/strategy/vars/downTimers | Returns the name and current value of all down timers in the strategy |
| GET | /device/strategy/vars/downTimers/{downTimerName}/value | Returns current value of the specified down timer |
| GET | /device/strategy/vars/floats | Returns the name and value of all (single-precision) float variables in the strategy |
| GET | /device/strategy/vars/floats/{floatName} | Returns value of the specified float variable |
| POST | /device/strategy/vars/floats/{floatName} | Sets the value of a float variable |
| GET | /device/strategy/vars/int32s | Returns the name and value of all integer32 variables in the strategy |
| GET | /device/strategy/vars/int32s/{int32Name} | Returns value of the specified integer32 variable |
| POST | /device/strategy/vars/int32s/{int32Name} | Sets the value of an integer32 variable |
| GET | /device/strategy/vars/int64s | Returns the name and value of all integer64 variables in the strategy |
| GET | /device/strategy/vars/int64s/_string | Returns the name and value as a string of all integer64 variables in the strategy |
| GET | /device/strategy/vars/int64s/{int64Name} | Returns value of the specified integer64 variable |
| POST | /device/strategy/vars/int64s/{int64Name} | Sets the value of an integer64 variable |
| GET | /device/strategy/vars/int64s/{int64Name}/_string | Returns value of the specified integer64 variable as a string |
| POST | /device/strategy/vars/int64s/{int64Name}/_string | Sets the value of an integer64 variable as a string |
| GET | /device/strategy/vars/strings | Returns the name and value of all string variables in the strategy |
| GET | /device/strategy/vars/strings/{stringName} | Returns value of the specified string |
| POST | /device/strategy/vars/strings/{stringName} | Sets the value of a string variable |
| GET | /device/strategy/vars/upTimers | Returns the name and current value of all up timers in the strategy |
| GET | /device/strategy/vars/upTimers/{upTimerName}/value | Returns current value of the specified up timer |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all device?" -> GET /device
- "List all strategy?" -> GET /device/strategy
- "List all analogInputs?" -> GET /device/strategy/ios/analogInputs
- "List all eu?" -> GET /device/strategy/ios/analogInputs/{ioName}/eu
- "List all analogOutputs?" -> GET /device/strategy/ios/analogOutputs
- "List all eu?" -> GET /device/strategy/ios/analogOutputs/{ioName}/eu
- "Create a eu?" -> POST /device/strategy/ios/analogOutputs/{ioName}/eu
- "List all digitalInputs?" -> GET /device/strategy/ios/digitalInputs
- "List all state?" -> GET /device/strategy/ios/digitalInputs/{ioName}/state
- "List all digitalOutputs?" -> GET /device/strategy/ios/digitalOutputs
- "List all state?" -> GET /device/strategy/ios/digitalOutputs/{ioName}/state
- "Create a state?" -> POST /device/strategy/ios/digitalOutputs/{ioName}/state
- "List all floats?" -> GET /device/strategy/tables/floats
- "Get float details?" -> GET /device/strategy/tables/floats/{tableName}
- "Get float details?" -> GET /device/strategy/tables/floats/{tableName}/{index}
- "List all int32s?" -> GET /device/strategy/tables/int32s
- "Get int32 details?" -> GET /device/strategy/tables/int32s/{tableName}
- "Get int32 details?" -> GET /device/strategy/tables/int32s/{tableName}/{index}
- "List all int64s?" -> GET /device/strategy/tables/int64s
- "Get int64 details?" -> GET /device/strategy/tables/int64s/{tableName}
- "List all _string?" -> GET /device/strategy/tables/int64s/{tableName}/_string
- "Create a _string?" -> POST /device/strategy/tables/int64s/{tableName}/_string
- "Get int64 details?" -> GET /device/strategy/tables/int64s/{tableName}/{index}
- "List all _string?" -> GET /device/strategy/tables/int64s/{tableName}/{index}/_string
- "Create a _string?" -> POST /device/strategy/tables/int64s/{tableName}/{index}/_string
- "List all strings?" -> GET /device/strategy/tables/strings
- "Get string details?" -> GET /device/strategy/tables/strings/{tableName}
- "Get string details?" -> GET /device/strategy/tables/strings/{tableName}/{index}
- "List all downTimers?" -> GET /device/strategy/vars/downTimers
- "List all value?" -> GET /device/strategy/vars/downTimers/{downTimerName}/value
- "List all floats?" -> GET /device/strategy/vars/floats
- "Get float details?" -> GET /device/strategy/vars/floats/{floatName}
- "List all int32s?" -> GET /device/strategy/vars/int32s
- "Get int32 details?" -> GET /device/strategy/vars/int32s/{int32Name}
- "List all int64s?" -> GET /device/strategy/vars/int64s
- "List all _string?" -> GET /device/strategy/vars/int64s/_string
- "Get int64 details?" -> GET /device/strategy/vars/int64s/{int64Name}
- "List all _string?" -> GET /device/strategy/vars/int64s/{int64Name}/_string
- "Create a _string?" -> POST /device/strategy/vars/int64s/{int64Name}/_string
- "List all strings?" -> GET /device/strategy/vars/strings
- "Get string details?" -> GET /device/strategy/vars/strings/{stringName}
- "List all upTimers?" -> GET /device/strategy/vars/upTimers
- "List all value?" -> GET /device/strategy/vars/upTimers/{upTimerName}/value
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
