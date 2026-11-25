---
name: slicebox-api
description: "Slicebox API skill. Use when working with Slicebox for sources, destinations, system. Covers 118 endpoints."
version: 1.0.0
generator: lapsh
---

# Slicebox API
API version: 2.0

## Auth
ApiKey token in path

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /sources -- verify access
3. POST /system/stop -- create first stop

## Endpoints

118 endpoints across 17 groups. See references/api-spec.lap for full details.

### sources
| Method | Path | Description |
|--------|------|-------------|
| GET | /sources | Returns a list of currently available data sources. Possible source types are user - data imported by an API call by a user, box - data received from a remote box, directory - data imported via a watched directory, import - data imported into slicebox using import sessions, or scp - data received from a PACS. |

### destinations
| Method | Path | Description |
|--------|------|-------------|
| GET | /destinations | Returns a list of currently available destinations. Possible destinations are box - sending data to a remote box, and scu - sending data a receiving SCP. |

### system
| Method | Path | Description |
|--------|------|-------------|
| POST | /system/stop | stop and shut down slicebox |
| GET | /system/health | No-op route for checking whether the service is alive or not |

### import
| Method | Path | Description |
|--------|------|-------------|
| GET | /import/sessions | Returns a list of available import sessions. |
| POST | /import/sessions | create a new import sessions |
| GET | /import/sessions/{id} | Returns the import sessions with the supplied ID |
| DELETE | /import/sessions/{id} | deletes the import session with the supplied ID |
| POST | /import/sessions/{id}/images | add a DICOM dataset to the import session with the supplied ID |
| GET | /import/sessions/{id}/images | get the imported images corresponding to the import session with the supplied ID |

### metadata
| Method | Path | Description |
|--------|------|-------------|
| GET | /metadata/patients | Returns a list of metadata on the patient level of the DICOM hierarchy |
| POST | /metadata/patients/query | submit a query for patients |
| GET | /metadata/patients/{id} | Return the patient with the supplied ID |
| GET | /metadata/patients/{id}/images | Returns all images for the patient with the supplied patient ID |
| GET | /metadata/studies | Returns a list of metadata on the study level of the DICOM hierarchy |
| POST | /metadata/studies/query | submit a query for studies |
| GET | /metadata/studies/{id} | Return the study with the supplied ID |
| GET | /metadata/studies/{id}/images | Returns all images for the study with the supplied study ID |
| GET | /metadata/series | Returns a list of metadata on the series level of the DICOM hierarchy |
| POST | /metadata/series/query | submit a query for series |
| GET | /metadata/series/{id} | Return the series with the supplied ID |
| GET | /metadata/series/{id}/source | Return the source of the series with the supplied ID |
| GET | /metadata/series/{id}/seriestypes | get the list of series types for the series with the supplied ID. |
| DELETE | /metadata/series/{id}/seriestypes | Delete all series types for the series with the supplied ID |
| PUT | /metadata/series/{seriesId}/seriestypes/{seriesTypeId} | Add the series type with the supplied series type ID to the series with the supplied series ID |
| DELETE | /metadata/series/{seriesId}/seriestypes/{seriesTypeId} | Delete the series type with the supplied series type ID from the series with the supplied series ID |
| GET | /metadata/series/{id}/seriestags | get the list of series tags for the series with the supplied ID. |
| POST | /metadata/series/{id}/seriestags | add a series tag to the series with the supplied ID |
| DELETE | /metadata/series/{seriesId}/seriestags/{seriesTagId} | Delete the series tag with the supplied series tag ID from the series with the supplied series ID |
| GET | /metadata/seriestags | Returns a list of series tags currently currently in use. |
| GET | /metadata/images | Returns a list of metadata on the image level of the DICOM hierarchy |
| POST | /metadata/images/query | submit a query for images |
| GET | /metadata/images/{id} | Return the image with the supplied ID |
| GET | /metadata/flatseries | Returns a list of flattened metadata on the patient, study and series levels |
| GET | /metadata/flatseries/{id} | Return the flat series with the supplied ID |
| POST | /metadata/flatseries/query | submit a query for flat series |

### images
| Method | Path | Description |
|--------|------|-------------|
| POST | /images | add a DICOM dataset to slicebox |
| POST | /images/jpeg | add a JPEG image to slicebox. The image data will be wrapped in a DICOM file and added as a new series belonging to the study with the supplied ID |
| GET | /images/{id} | fetch dataset corresponding to the supplied image ID |
| DELETE | /images/{id} | Delete the image with the supplied ID |
| POST | /images/delete | bulk delete a sequence of images according to the supplied image IDs. This is the same as a sequence of DELETE requests to /images/{id} |
| GET | /images/{id}/attributes | list all DICOM attributes of the dataset corresponding to the supplied image ID |
| GET | /images/{id}/imageinformation | get basic information about the pixel data of an image |
| GET | /images/{id}/png | get a PNG image representation of the image corresponding to the supplied ID |
| PUT | /images/{id}/modify | modify and/or insert image attributes according to the input tagpath-value mappings |
| PUT | /images/{id}/anonymize | delete the selected image and replace it with an anonymized version |
| POST | /images/{id}/anonymized | get an anonymized version of the image with the supplied ID |
| POST | /images/export | create an export set, a group of image IDs of images to export. The export set will contain the selected images. The export set is available for download 12 hours before it is automatically deleted. |
| GET | /images/export | download the export set with the supplied export set ID as a zip archive |

### anonymization
| Method | Path | Description |
|--------|------|-------------|
| POST | /anonymization/anonymize | anonymize the images corresponding to the supplied list of image IDs (each paired with a list of DICOM tag translation). This route corresponds to repeated use of the route /images/{id}/anonymize. |
| GET | /anonymization/keys | get a list of anonymization keys, each specifying how vital DICOM attributes have been anonymized for a particular image |
| GET | /anonymization/keys/{id} | get the anonymization key with the supplied ID |
| DELETE | /anonymization/keys/{id} | delete an anonymization key that is no longer of interest |
| GET | /anonymization/keys/{id}/keyvalues | get pointers to the images corresponding to the anonymization key with the supplied ID |
| POST | /anonymization/keys/query | submit a query for anonymization keys |
| GET | /anonymization/options | list all supported anonymization options defining an anonymization profile |
| GET | /anonymization/keys/export/csv | export all anonymization keys as a csv file |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/login | Obtain a session cookie that can be used to authenticate future API calls from the present IP address and with the present user agent. |
| POST | /users/logout | Logout the current user by responding with a delete cookie header removing the session cookie for this user. |
| GET | /users/current | obtain information on the currently logged in user as specified by the supplied session cookie, IP address and user agent. |
| GET | /users | Returns all users of slicebox |
| POST | /users | Creates a new user. Dupicates are accepted but not added. |
| DELETE | /users/{id} | deletes a single user based on the ID supplied |

### log
| Method | Path | Description |
|--------|------|-------------|
| GET | /log | get a list of slicebox log messages |
| DELETE | /log | delete all log messages |
| DELETE | /log/{id} | Delete the log entry with the supplied ID |

### boxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /boxes | get a list of box connections |
| POST | /boxes/createconnection | create a new box connection where the supplied entity holds the remote box name. Used by publicly available boxes. |
| POST | /boxes/connect | connect to another box using a received URL. Used to connect to a public box. |
| DELETE | /boxes/{id} | Delete the remote box with the supplied ID |
| POST | /boxes/{id}/send | send images corresponding to the supplied image ids to the remote box with the supplied ID |
| GET | /boxes/incoming | get incoming transactions (finished, currently receiving, waiting or failed) |
| DELETE | /boxes/incoming/{id} | delete an incoming transaction. If a currently active transaction is deleted, a new transaction with the remainder of the images is created when receiving the next incoming image. |
| GET | /boxes/incoming/{id}/images | get the received images corresponding to the incoming transaction with the supplied ID |
| GET | /boxes/outgoing | get outgoing transactions (finished, currently sending, waiting or failed) |
| DELETE | /boxes/outgoing/{id} | delete an outgoing transaction. This will stop ongoing transactions. |
| GET | /boxes/outgoing/{id}/images | get the sent images corresponding to the outgoing transaction with the supplied ID |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /transactions/{token}/image | add an image (dataset) as part of a transaction. This method is used when sending images using the push method to a public slicebox. |
| GET | /transactions/{token}/status | get the status of the remote incoming transaction with the supplied transaction ID |
| PUT | /transactions/{token}/status | update the status of the transaction with the supplied ID |
| GET | /transactions/{token}/outgoing/poll | get next outgoing transaction and image (information on the next image that the connected box wishes to send to you), if any. This method is used when sending images using the poll method from a public slicebox. |
| GET | /transactions/{token}/outgoing | fetch an image from the connected box as part of a transaction. This method is used when sending images using the poll method from a public slicebox. |
| POST | /transactions/{token}/outgoing/done | signal that the supplied outgoing transaction and image was successfully received and can be marked as sent. This method is used when sending images using the poll method from a public slicebox. |
| POST | /transactions/{token}/outgoing/failed | signal that the image corresponding to the supplied outgoing transaction and image could not be read or stored properly on the receiving side, and that the transaction should be marked as failed. |

### directorywatches
| Method | Path | Description |
|--------|------|-------------|
| GET | /directorywatches | get a list of watch directories. Each watch directory and its sub-directories are watched for incoming DICOM files, which are read and imported into slicebox. |
| POST | /directorywatches | add a new directory to watch for incoming DICOM files |
| DELETE | /directorywatches/{id} | stop watching and remove the directory corresponding to the supplied ID |

### scps
| Method | Path | Description |
|--------|------|-------------|
| GET | /scps | get a list of DICOM SCPs. Each SCP is a server for receiving DICOM images from e.g. a PACS system. |
| POST | /scps | add a new SCP for receiving DICOM images |
| DELETE | /scps/{id} | shut down and remove the SCP corresponding to the supplied ID |

### scus
| Method | Path | Description |
|--------|------|-------------|
| GET | /scus | get a list of DICOM SCUs. Each SCU is a client for sending DICOM images to an SCP, e.g. a PACS system. |
| POST | /scus | add a new SCU for sending DICOM images |
| DELETE | /scus/{id} | remove the SCU corresponding to the supplied ID |
| POST | /scus/{id}/send | send the images with the supplied image IDs to a DICOM SCP using the the SCU with the supplied scu ID |

### filtering
| Method | Path | Description |
|--------|------|-------------|
| GET | /filtering/filters | List defined filters |
| POST | /filtering/filters | Inserts or updates a filter. If a filter with same name as supplied filter exists this filter is updated, otherwise a new filter is inserted. |
| DELETE | /filtering/filters/{id} | remove the filter corresponding to the supplied ID |
| GET | /filtering/filters/{id}/tagpaths | List tagpaths for the selected filter |
| POST | /filtering/filters/{id}/tagpaths | add a tagpath to a filter |
| DELETE | /filtering/filters/{id}/tagpaths/{tagpathid} | remove the tagpath corresponding to the supplied ID |
| GET | /filtering/associations | Get a list of source to filter associations. |
| POST | /filtering/associations | Inserts or updates a source <-> filter associations. If the specified Source already  has an association this is updated, otherwise a new is inserted. |
| DELETE | /filtering/associations/{id} | remove the source <-> filter association corresponding to the supplied ID |

### seriestypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /seriestypes | get a list of all added series types. By filtering search results for certain series types, it is easier for applications to ensure that they read images of applicable types. |
| POST | /seriestypes | add a new series type |
| PUT | /seriestypes/{id} | request an asynchronous update of all series, labelling appropriate series with the series type corresponding to the supplied ID. |
| DELETE | /seriestypes/{id} | remove the series type corresponding to the supplied ID |
| POST | /seriestypes/series/query | submit a query for seriestypes for a list of series |
| GET | /seriestypes/rules | get a list of rules for assigning series types to series. A rule connects to a series of attributes with values and a resulting series type. If a series has the required values of the listed attributes, it is assigned to the series type of the rule. |
| POST | /seriestypes/rules | add a new series type rule |
| GET | /seriestypes/rules/updatestatus | get the status of the internal process of updating series types for series following a change of series types, rules or attributes. |
| DELETE | /seriestypes/rules/{id} | remove the series type rule corresponding to the supplied ID |
| GET | /seriestypes/rules/{id}/attributes | get the list of attributes for the series type rule with the supplied ID. |
| POST | /seriestypes/rules/{id}/attributes | add a new series type rule attribute |
| DELETE | /seriestypes/rules/{ruleId}/attributes/{attributeId} | remove the series type rule attribute corresponding to the supplied series type and attribute IDs |

### forwarding
| Method | Path | Description |
|--------|------|-------------|
| GET | /forwarding/rules | get a list of all forwarding rules. A forwarding rule specifies the automatic forwarding of images from a source (SCP, BOX, etc.) to a destimation (BOX, SCU, etc.) |
| POST | /forwarding/rules | add a new forwarding rule |
| DELETE | /forwarding/rule/{id} | remove the forwarding rule corresponding to the supplied ID |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all sources?" -> GET /sources
- "List all destinations?" -> GET /destinations
- "Create a stop?" -> POST /system/stop
- "List all health?" -> GET /system/health
- "List all sessions?" -> GET /import/sessions
- "Create a session?" -> POST /import/sessions
- "Get session details?" -> GET /import/sessions/{id}
- "Delete a session?" -> DELETE /import/sessions/{id}
- "Create a image?" -> POST /import/sessions/{id}/images
- "List all images?" -> GET /import/sessions/{id}/images
- "List all patients?" -> GET /metadata/patients
- "Create a query?" -> POST /metadata/patients/query
- "Get patient details?" -> GET /metadata/patients/{id}
- "List all images?" -> GET /metadata/patients/{id}/images
- "List all studies?" -> GET /metadata/studies
- "Create a query?" -> POST /metadata/studies/query
- "Get study details?" -> GET /metadata/studies/{id}
- "List all images?" -> GET /metadata/studies/{id}/images
- "List all series?" -> GET /metadata/series
- "Create a query?" -> POST /metadata/series/query
- "Get sery details?" -> GET /metadata/series/{id}
- "List all source?" -> GET /metadata/series/{id}/source
- "List all seriestypes?" -> GET /metadata/series/{id}/seriestypes
- "Update a seriestype?" -> PUT /metadata/series/{seriesId}/seriestypes/{seriesTypeId}
- "Delete a seriestype?" -> DELETE /metadata/series/{seriesId}/seriestypes/{seriesTypeId}
- "List all seriestags?" -> GET /metadata/series/{id}/seriestags
- "Create a seriestag?" -> POST /metadata/series/{id}/seriestags
- "Delete a seriestag?" -> DELETE /metadata/series/{seriesId}/seriestags/{seriesTagId}
- "List all seriestags?" -> GET /metadata/seriestags
- "List all images?" -> GET /metadata/images
- "Create a query?" -> POST /metadata/images/query
- "Get image details?" -> GET /metadata/images/{id}
- "List all flatseries?" -> GET /metadata/flatseries
- "Get flatsery details?" -> GET /metadata/flatseries/{id}
- "Create a query?" -> POST /metadata/flatseries/query
- "Create a image?" -> POST /images
- "Create a jpeg?" -> POST /images/jpeg
- "Get image details?" -> GET /images/{id}
- "Delete a image?" -> DELETE /images/{id}
- "Create a delete?" -> POST /images/delete
- "List all attributes?" -> GET /images/{id}/attributes
- "List all imageinformation?" -> GET /images/{id}/imageinformation
- "List all png?" -> GET /images/{id}/png
- "Create a anonymized?" -> POST /images/{id}/anonymized
- "Create a export?" -> POST /images/export
- "List all export?" -> GET /images/export
- "Create a anonymize?" -> POST /anonymization/anonymize
- "List all keys?" -> GET /anonymization/keys
- "Get key details?" -> GET /anonymization/keys/{id}
- "Delete a key?" -> DELETE /anonymization/keys/{id}
- "List all keyvalues?" -> GET /anonymization/keys/{id}/keyvalues
- "Create a query?" -> POST /anonymization/keys/query
- "List all options?" -> GET /anonymization/options
- "List all csv?" -> GET /anonymization/keys/export/csv
- "Create a login?" -> POST /users/login
- "Create a logout?" -> POST /users/logout
- "List all current?" -> GET /users/current
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Delete a user?" -> DELETE /users/{id}
- "List all log?" -> GET /log
- "Delete a log?" -> DELETE /log/{id}
- "List all boxes?" -> GET /boxes
- "Create a createconnection?" -> POST /boxes/createconnection
- "Create a connect?" -> POST /boxes/connect
- "Delete a boxe?" -> DELETE /boxes/{id}
- "Create a send?" -> POST /boxes/{id}/send
- "List all incoming?" -> GET /boxes/incoming
- "Delete a incoming?" -> DELETE /boxes/incoming/{id}
- "List all images?" -> GET /boxes/incoming/{id}/images
- "List all outgoing?" -> GET /boxes/outgoing
- "Delete a outgoing?" -> DELETE /boxes/outgoing/{id}
- "List all images?" -> GET /boxes/outgoing/{id}/images
- "Create a image?" -> POST /transactions/{token}/image
- "List all status?" -> GET /transactions/{token}/status
- "List all poll?" -> GET /transactions/{token}/outgoing/poll
- "List all outgoing?" -> GET /transactions/{token}/outgoing
- "Create a done?" -> POST /transactions/{token}/outgoing/done
- "Create a failed?" -> POST /transactions/{token}/outgoing/failed
- "List all directorywatches?" -> GET /directorywatches
- "Create a directorywatche?" -> POST /directorywatches
- "Delete a directorywatche?" -> DELETE /directorywatches/{id}
- "List all scps?" -> GET /scps
- "Create a scp?" -> POST /scps
- "Delete a scp?" -> DELETE /scps/{id}
- "List all scus?" -> GET /scus
- "Create a scus?" -> POST /scus
- "Delete a scus?" -> DELETE /scus/{id}
- "Create a send?" -> POST /scus/{id}/send
- "List all filters?" -> GET /filtering/filters
- "Create a filter?" -> POST /filtering/filters
- "Delete a filter?" -> DELETE /filtering/filters/{id}
- "List all tagpaths?" -> GET /filtering/filters/{id}/tagpaths
- "Create a tagpath?" -> POST /filtering/filters/{id}/tagpaths
- "Delete a tagpath?" -> DELETE /filtering/filters/{id}/tagpaths/{tagpathid}
- "List all associations?" -> GET /filtering/associations
- "Create a association?" -> POST /filtering/associations
- "Delete a association?" -> DELETE /filtering/associations/{id}
- "List all seriestypes?" -> GET /seriestypes
- "Create a seriestype?" -> POST /seriestypes
- "Update a seriestype?" -> PUT /seriestypes/{id}
- "Delete a seriestype?" -> DELETE /seriestypes/{id}
- "Create a query?" -> POST /seriestypes/series/query
- "List all rules?" -> GET /seriestypes/rules
- "Create a rule?" -> POST /seriestypes/rules
- "List all updatestatus?" -> GET /seriestypes/rules/updatestatus
- "Delete a rule?" -> DELETE /seriestypes/rules/{id}
- "List all attributes?" -> GET /seriestypes/rules/{id}/attributes
- "Create a attribute?" -> POST /seriestypes/rules/{id}/attributes
- "Delete a attribute?" -> DELETE /seriestypes/rules/{ruleId}/attributes/{attributeId}
- "List all rules?" -> GET /forwarding/rules
- "Create a rule?" -> POST /forwarding/rules
- "Delete a rule?" -> DELETE /forwarding/rule/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
