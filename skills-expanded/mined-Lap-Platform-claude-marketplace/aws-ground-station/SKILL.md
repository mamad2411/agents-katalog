---
name: aws-ground-station
description: "AWS Ground Station API skill. Use when working with AWS Ground Station for contact, config, dataflowEndpointGroup. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Ground Station
API version: 2019-05-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /config -- verify access
3. POST /config -- create first config

## Endpoints

33 endpoints across 12 groups. See references/api-spec.lap for full details.

### contact
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /contact/{contactId} | Cancels a contact with a specified contact ID. |
| GET | /contact/{contactId} | Describes an existing contact. |
| POST | /contact | Reserves a contact using specified parameters. |

### config
| Method | Path | Description |
|--------|------|-------------|
| POST | /config | Creates a Config with the specified configData parameters. Only one type of configData can be specified. |
| DELETE | /config/{configType}/{configId} | Deletes a Config. |
| GET | /config/{configType}/{configId} | Returns Config information. Only one Config response can be returned. |
| GET | /config | Returns a list of Config objects. |
| PUT | /config/{configType}/{configId} | Updates the Config used when scheduling contacts. Updating a Config will not update the execution parameters for existing future contacts scheduled with this Config. |

### dataflowEndpointGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /dataflowEndpointGroup | Creates a DataflowEndpoint group containing the specified list of DataflowEndpoint objects. The name field in each endpoint is used in your mission profile DataflowEndpointConfig to specify which endpoints to use during a contact. When a contact uses multiple DataflowEndpointConfig objects, each Config must match a DataflowEndpoint in the same group. |
| DELETE | /dataflowEndpointGroup/{dataflowEndpointGroupId} | Deletes a dataflow endpoint group. |
| GET | /dataflowEndpointGroup/{dataflowEndpointGroupId} | Returns the dataflow endpoint group. |
| GET | /dataflowEndpointGroup | Returns a list of DataflowEndpoint groups. |

### ephemeris
| Method | Path | Description |
|--------|------|-------------|
| POST | /ephemeris | Creates an Ephemeris with the specified EphemerisData. |
| DELETE | /ephemeris/{ephemerisId} | Deletes an ephemeris |
| GET | /ephemeris/{ephemerisId} | Describes an existing ephemeris. |
| PUT | /ephemeris/{ephemerisId} | Updates an existing ephemeris |

### missionprofile
| Method | Path | Description |
|--------|------|-------------|
| POST | /missionprofile | Creates a mission profile.  dataflowEdges is a list of lists of strings. Each lower level list of strings has two elements: a from ARN and a to ARN. |
| DELETE | /missionprofile/{missionProfileId} | Deletes a mission profile. |
| GET | /missionprofile/{missionProfileId} | Returns a mission profile. |
| GET | /missionprofile | Returns a list of mission profiles. |
| PUT | /missionprofile/{missionProfileId} | Updates a mission profile. Updating a mission profile will not update the execution parameters for existing future contacts. |

### agent
| Method | Path | Description |
|--------|------|-------------|
| GET | /agent/{agentId}/configuration | For use by AWS Ground Station Agent and shouldn't be called directly.  Gets the latest configuration information for a registered agent. |
| POST | /agent | For use by AWS Ground Station Agent and shouldn't be called directly.   Registers a new agent with AWS Ground Station. |
| PUT | /agent/{agentId} | For use by AWS Ground Station Agent and shouldn't be called directly.  Update the status of the agent. |

### minute-usage
| Method | Path | Description |
|--------|------|-------------|
| POST | /minute-usage | Returns the number of reserved minutes used by account. |

### satellite
| Method | Path | Description |
|--------|------|-------------|
| GET | /satellite/{satelliteId} | Returns a satellite. |
| GET | /satellite | Returns a list of satellites. |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /contacts | Returns a list of contacts. If statusList contains AVAILABLE, the request must include groundStation, missionprofileArn, and satelliteArn. |

### ephemerides
| Method | Path | Description |
|--------|------|-------------|
| POST | /ephemerides | List existing ephemerides. |

### groundstation
| Method | Path | Description |
|--------|------|-------------|
| GET | /groundstation | Returns a list of ground stations. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of tags for a specified resource. |
| POST | /tags/{resourceArn} | Assigns a tag to a resource. |
| DELETE | /tags/{resourceArn} | Deassigns a resource tag. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a contact?" -> DELETE /contact/{contactId}
- "Create a config?" -> POST /config
- "Create a dataflowEndpointGroup?" -> POST /dataflowEndpointGroup
- "Create a ephemeris?" -> POST /ephemeris
- "Create a missionprofile?" -> POST /missionprofile
- "Delete a config?" -> DELETE /config/{configType}/{configId}
- "Delete a dataflowEndpointGroup?" -> DELETE /dataflowEndpointGroup/{dataflowEndpointGroupId}
- "Delete a ephemeris?" -> DELETE /ephemeris/{ephemerisId}
- "Delete a missionprofile?" -> DELETE /missionprofile/{missionProfileId}
- "Get contact details?" -> GET /contact/{contactId}
- "Get ephemeris details?" -> GET /ephemeris/{ephemerisId}
- "List all configuration?" -> GET /agent/{agentId}/configuration
- "Get config details?" -> GET /config/{configType}/{configId}
- "Get dataflowEndpointGroup details?" -> GET /dataflowEndpointGroup/{dataflowEndpointGroupId}
- "Create a minute-usage?" -> POST /minute-usage
- "Get missionprofile details?" -> GET /missionprofile/{missionProfileId}
- "Get satellite details?" -> GET /satellite/{satelliteId}
- "List all config?" -> GET /config
- "Create a contact?" -> POST /contacts
- "List all dataflowEndpointGroup?" -> GET /dataflowEndpointGroup
- "Create a ephemeride?" -> POST /ephemerides
- "List all groundstation?" -> GET /groundstation
- "List all missionprofile?" -> GET /missionprofile
- "List all satellite?" -> GET /satellite
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a agent?" -> POST /agent
- "Create a contact?" -> POST /contact
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a agent?" -> PUT /agent/{agentId}
- "Update a config?" -> PUT /config/{configType}/{configId}
- "Update a ephemeris?" -> PUT /ephemeris/{ephemerisId}
- "Update a missionprofile?" -> PUT /missionprofile/{missionProfileId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
