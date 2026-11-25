---
name: face-client
description: "Face Client API skill. Use when working with Face Client for findsimilars, group, identify. Covers 63 endpoints."
version: 1.0.0
generator: lapsh
---

# Face Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /persongroups -- verify access
3. POST /findsimilars -- create first findsimilars

## Endpoints

63 endpoints across 11 groups. See references/api-spec.lap for full details.

### findsimilars
| Method | Path | Description |
|--------|------|-------------|
| POST | /findsimilars | Given query face's faceId, to search the similar-looking faces from a faceId array, a face list or a large face list. faceId array contains the faces created by [Face - Detect With Url](https://docs.microsoft.com/rest/api/faceapi/face/detectwithurl) or [Face - Detect With Stream](https://docs.microsoft.com/rest/api/faceapi/face/detectwithstream), which will expire at the time specified by faceIdTimeToLive after creation. A "faceListId" is created by [FaceList - Create](https://docs.microsoft.com/rest/api/faceapi/facelist/create) containing persistedFaceIds that will not expire. And a "largeFaceListId" is created by [LargeFaceList - Create](https://docs.microsoft.com/rest/api/faceapi/largefacelist/create) containing persistedFaceIds that will also not expire. Depending on the input the returned similar faces list contains faceIds or persistedFaceIds ranked by similarity. |

### group
| Method | Path | Description |
|--------|------|-------------|
| POST | /group | Divide candidate faces into groups based on face similarity.<br /> |

### identify
| Method | Path | Description |
|--------|------|-------------|
| POST | /identify | 1-to-many identification to find the closest matches of the specific query person face from a person group or large person group. |

### verify
| Method | Path | Description |
|--------|------|-------------|
| POST | /verify | Verify whether two faces belong to a same person or whether one face belongs to a person. |

### persongroups
| Method | Path | Description |
|--------|------|-------------|
| POST | /persongroups/{personGroupId}/persons | Create a new person in a specified person group. |
| GET | /persongroups/{personGroupId}/persons | List all persons in a person group, and retrieve person information (including personId, name, userData and persistedFaceIds of registered faces of the person). |
| DELETE | /persongroups/{personGroupId}/persons/{personId} | Delete an existing person from a person group. The persistedFaceId, userData, person name and face feature in the person entry will all be deleted. |
| GET | /persongroups/{personGroupId}/persons/{personId} | Retrieve a person's information, including registered persisted faces, name and userData. |
| PATCH | /persongroups/{personGroupId}/persons/{personId} | Update name or userData of a person. |
| DELETE | /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Delete a face from a person in a person group by specified personGroupId, personId and persistedFaceId. |
| GET | /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Retrieve information about a persisted face (specified by persistedFaceId, personId and its belonging personGroupId). |
| PATCH | /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Add a face to a person into a person group for face identification or verification. To deal with an image contains multiple faces, input face can be specified as an image with a targetFace rectangle. It returns a persistedFaceId representing the added face. No image will be stored. Only the extracted face feature will be stored on server until [PersonGroup PersonFace - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroupperson/deleteface), [PersonGroup Person - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroupperson/delete) or [PersonGroup - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroup/delete) is called. |
| PUT | /persongroups/{personGroupId} | Create a new person group with specified personGroupId, name, user-provided userData and recognitionModel. |
| DELETE | /persongroups/{personGroupId} | Delete an existing person group. Persisted face features of all people in the person group will also be deleted. |
| GET | /persongroups/{personGroupId} | Retrieve person group name, userData and recognitionModel. To get person information under this personGroup, use [PersonGroup Person - List](https://docs.microsoft.com/rest/api/faceapi/persongroupperson/list). |
| PATCH | /persongroups/{personGroupId} | Update an existing person group's display name and userData. The properties which does not appear in request body will not be updated. |
| GET | /persongroups/{personGroupId}/training | Retrieve the training status of a person group (completed or ongoing). |
| GET | /persongroups | List person groups’ personGroupId, name, userData and recognitionModel.<br /> |
| POST | /persongroups/{personGroupId}/train | Queue a person group training task, the training task may not be started immediately. |
| POST | /persongroups/{personGroupId}/persons/{personId}/persistedfaces | Add a face to a person into a person group for face identification or verification. To deal with an image contains multiple faces, input face can be specified as an image with a targetFace rectangle. It returns a persistedFaceId representing the added face. No image will be stored. Only the extracted face feature will be stored on server until [PersonGroup PersonFace - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroupperson/deleteface), [PersonGroup Person - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroupperson/delete) or [PersonGroup - Delete](https://docs.microsoft.com/rest/api/faceapi/persongroup/delete) is called. |

### facelists
| Method | Path | Description |
|--------|------|-------------|
| PUT | /facelists/{faceListId} | Create an empty face list with user-specified faceListId, name, an optional userData and recognitionModel. Up to 64 face lists are allowed in one subscription. |
| GET | /facelists/{faceListId} | Retrieve a face list’s faceListId, name, userData, recognitionModel and faces in the face list. |
| PATCH | /facelists/{faceListId} | Update information of a face list. |
| DELETE | /facelists/{faceListId} | Delete a specified face list. |
| GET | /facelists | List face lists’ faceListId, name, userData and recognitionModel. <br /> |
| DELETE | /facelists/{faceListId}/persistedfaces/{persistedFaceId} | Delete a face from a face list by specified faceListId and persistedFaceId. |
| POST | /facelists/{faceListId}/persistedfaces | Add a face to a specified face list, up to 1,000 faces. |

### detect
| Method | Path | Description |
|--------|------|-------------|
| POST | /detect | Detect human faces in an image, return face rectangles, and optionally with faceIds, landmarks, and attributes.<br /> |

### largepersongroups
| Method | Path | Description |
|--------|------|-------------|
| POST | /largepersongroups/{largePersonGroupId}/persons | Create a new person in a specified large person group. |
| GET | /largepersongroups/{largePersonGroupId}/persons | List all persons in a large person group, and retrieve person information (including personId, name, userData and persistedFaceIds of registered faces of the person). |
| DELETE | /largepersongroups/{largePersonGroupId}/persons/{personId} | Delete an existing person from a large person group. The persistedFaceId, userData, person name and face feature in the person entry will all be deleted. |
| GET | /largepersongroups/{largePersonGroupId}/persons/{personId} | Retrieve a person's name and userData, and the persisted faceIds representing the registered person face feature. |
| PATCH | /largepersongroups/{largePersonGroupId}/persons/{personId} | Update name or userData of a person. |
| DELETE | /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Delete a face from a person in a large person group by specified largePersonGroupId, personId and persistedFaceId. |
| GET | /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Retrieve information about a persisted face (specified by persistedFaceId, personId and its belonging largePersonGroupId). |
| PATCH | /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId} | Update a person persisted face's userData field. |
| PUT | /largepersongroups/{largePersonGroupId} | Create a new large person group with user-specified largePersonGroupId, name, an optional userData and recognitionModel. |
| DELETE | /largepersongroups/{largePersonGroupId} | Delete an existing large person group. Persisted face features of all people in the large person group will also be deleted. |
| GET | /largepersongroups/{largePersonGroupId} | Retrieve the information of a large person group, including its name, userData and recognitionModel. This API returns large person group information only, use [LargePersonGroup Person - List](https://docs.microsoft.com/rest/api/faceapi/largepersongroupperson/list) instead to retrieve person information under the large person group. |
| PATCH | /largepersongroups/{largePersonGroupId} | Update an existing large person group's display name and userData. The properties which does not appear in request body will not be updated. |
| GET | /largepersongroups/{largePersonGroupId}/training | Retrieve the training status of a large person group (completed or ongoing). |
| GET | /largepersongroups | List all existing large person groups’ largePersonGroupId, name, userData and recognitionModel.<br /> |
| POST | /largepersongroups/{largePersonGroupId}/train | Queue a large person group training task, the training task may not be started immediately. |
| POST | /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces | Add a face to a person into a large person group for face identification or verification. To deal with an image contains multiple faces, input face can be specified as an image with a targetFace rectangle. It returns a persistedFaceId representing the added face. No image will be stored. Only the extracted face feature will be stored on server until [LargePersonGroup PersonFace - Delete](https://docs.microsoft.com/rest/api/faceapi/largepersongroupperson/deleteface), [LargePersonGroup Person - Delete](https://docs.microsoft.com/rest/api/faceapi/largepersongroupperson/delete) or [LargePersonGroup - Delete](https://docs.microsoft.com/rest/api/faceapi/largepersongroup/delete) is called. |

### largefacelists
| Method | Path | Description |
|--------|------|-------------|
| PUT | /largefacelists/{largeFaceListId} | Create an empty large face list with user-specified largeFaceListId, name, an optional userData and recognitionModel. |
| GET | /largefacelists/{largeFaceListId} | Retrieve a large face list’s largeFaceListId, name, userData and recognitionModel. |
| PATCH | /largefacelists/{largeFaceListId} | Update information of a large face list. |
| DELETE | /largefacelists/{largeFaceListId} | Delete a specified large face list. |
| GET | /largefacelists/{largeFaceListId}/training | Retrieve the training status of a large face list (completed or ongoing). |
| GET | /largefacelists | List large face lists’ information of largeFaceListId, name, userData and recognitionModel. <br /> |
| POST | /largefacelists/{largeFaceListId}/train | Queue a large face list training task, the training task may not be started immediately. |
| DELETE | /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId} | Delete a face from a large face list by specified largeFaceListId and persistedFaceId. |
| GET | /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId} | Retrieve information about a persisted face (specified by persistedFaceId and its belonging largeFaceListId). |
| PATCH | /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId} | Update a persisted face's userData field. |
| POST | /largefacelists/{largeFaceListId}/persistedfaces | Add a face to a specified large face list, up to 1,000,000 faces. |
| GET | /largefacelists/{largeFaceListId}/persistedfaces | List all faces in a large face list, and retrieve face information (including userData and persistedFaceIds of registered faces of the face). |

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| POST | /snapshots | Submit an operation to take a snapshot of face list, large face list, person group or large person group, with user-specified snapshot type, source object id, apply scope and an optional user data.<br /> |
| GET | /snapshots | List all accessible snapshots with related information, including snapshots that were taken by the user, or snapshots to be applied to the user (subscription id was included in the applyScope in Snapshot - Take). |
| GET | /snapshots/{snapshotId} | Retrieve information about a snapshot. Snapshot is only accessible to the source subscription who took it, and target subscriptions included in the applyScope in Snapshot - Take. |
| PATCH | /snapshots/{snapshotId} | Update the information of a snapshot. Only the source subscription who took the snapshot can update the snapshot. |
| DELETE | /snapshots/{snapshotId} | Delete an existing snapshot according to the snapshotId. All object data and information in the snapshot will also be deleted. Only the source subscription who took the snapshot can delete the snapshot. If the user does not delete a snapshot with this API, the snapshot will still be automatically deleted in 48 hours after creation. |
| POST | /snapshots/{snapshotId}/apply | Submit an operation to apply a snapshot to current subscription. For each snapshot, only subscriptions included in the applyScope of Snapshot - Take can apply it.<br /> |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /operations/{operationId} | Retrieve the status of a take/apply snapshot operation. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a findsimilar?" -> POST /findsimilars
- "Create a group?" -> POST /group
- "Create a identify?" -> POST /identify
- "Create a verify?" -> POST /verify
- "Create a person?" -> POST /persongroups/{personGroupId}/persons
- "List all persons?" -> GET /persongroups/{personGroupId}/persons
- "Delete a person?" -> DELETE /persongroups/{personGroupId}/persons/{personId}
- "Get person details?" -> GET /persongroups/{personGroupId}/persons/{personId}
- "Partially update a person?" -> PATCH /persongroups/{personGroupId}/persons/{personId}
- "Delete a persistedface?" -> DELETE /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Get persistedface details?" -> GET /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Partially update a persistedface?" -> PATCH /persongroups/{personGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Update a persongroup?" -> PUT /persongroups/{personGroupId}
- "Delete a persongroup?" -> DELETE /persongroups/{personGroupId}
- "Get persongroup details?" -> GET /persongroups/{personGroupId}
- "Partially update a persongroup?" -> PATCH /persongroups/{personGroupId}
- "List all training?" -> GET /persongroups/{personGroupId}/training
- "List all persongroups?" -> GET /persongroups
- "Create a train?" -> POST /persongroups/{personGroupId}/train
- "Update a facelist?" -> PUT /facelists/{faceListId}
- "Get facelist details?" -> GET /facelists/{faceListId}
- "Partially update a facelist?" -> PATCH /facelists/{faceListId}
- "Delete a facelist?" -> DELETE /facelists/{faceListId}
- "List all facelists?" -> GET /facelists
- "Delete a persistedface?" -> DELETE /facelists/{faceListId}/persistedfaces/{persistedFaceId}
- "Create a persistedface?" -> POST /persongroups/{personGroupId}/persons/{personId}/persistedfaces
- "Create a detect?" -> POST /detect
- "Create a persistedface?" -> POST /facelists/{faceListId}/persistedfaces
- "Create a person?" -> POST /largepersongroups/{largePersonGroupId}/persons
- "List all persons?" -> GET /largepersongroups/{largePersonGroupId}/persons
- "Delete a person?" -> DELETE /largepersongroups/{largePersonGroupId}/persons/{personId}
- "Get person details?" -> GET /largepersongroups/{largePersonGroupId}/persons/{personId}
- "Partially update a person?" -> PATCH /largepersongroups/{largePersonGroupId}/persons/{personId}
- "Delete a persistedface?" -> DELETE /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Get persistedface details?" -> GET /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Partially update a persistedface?" -> PATCH /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces/{persistedFaceId}
- "Update a largepersongroup?" -> PUT /largepersongroups/{largePersonGroupId}
- "Delete a largepersongroup?" -> DELETE /largepersongroups/{largePersonGroupId}
- "Get largepersongroup details?" -> GET /largepersongroups/{largePersonGroupId}
- "Partially update a largepersongroup?" -> PATCH /largepersongroups/{largePersonGroupId}
- "List all training?" -> GET /largepersongroups/{largePersonGroupId}/training
- "List all largepersongroups?" -> GET /largepersongroups
- "Create a train?" -> POST /largepersongroups/{largePersonGroupId}/train
- "Create a persistedface?" -> POST /largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces
- "Update a largefacelist?" -> PUT /largefacelists/{largeFaceListId}
- "Get largefacelist details?" -> GET /largefacelists/{largeFaceListId}
- "Partially update a largefacelist?" -> PATCH /largefacelists/{largeFaceListId}
- "Delete a largefacelist?" -> DELETE /largefacelists/{largeFaceListId}
- "List all training?" -> GET /largefacelists/{largeFaceListId}/training
- "List all largefacelists?" -> GET /largefacelists
- "Create a train?" -> POST /largefacelists/{largeFaceListId}/train
- "Delete a persistedface?" -> DELETE /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId}
- "Get persistedface details?" -> GET /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId}
- "Partially update a persistedface?" -> PATCH /largefacelists/{largeFaceListId}/persistedfaces/{persistedFaceId}
- "Create a persistedface?" -> POST /largefacelists/{largeFaceListId}/persistedfaces
- "List all persistedfaces?" -> GET /largefacelists/{largeFaceListId}/persistedfaces
- "Create a snapshot?" -> POST /snapshots
- "List all snapshots?" -> GET /snapshots
- "Get snapshot details?" -> GET /snapshots/{snapshotId}
- "Partially update a snapshot?" -> PATCH /snapshots/{snapshotId}
- "Delete a snapshot?" -> DELETE /snapshots/{snapshotId}
- "Create a apply?" -> POST /snapshots/{snapshotId}/apply
- "Get operation details?" -> GET /operations/{operationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
