---
name: amazon-location-service
description: "Amazon Location Service API skill. Use when working with Amazon Location Service for tracking, geofencing, routes. Covers 60 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Location Service
API version: 2020-11-19

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tracking/v0/trackers/{TrackerName}/devices/{DeviceId}/positions/latest -- verify access
3. POST /tracking/v0/trackers/{TrackerName}/consumers -- create first consumers

## Endpoints

60 endpoints across 7 groups. See references/api-spec.lap for full details.

### tracking
| Method | Path | Description |
|--------|------|-------------|
| POST | /tracking/v0/trackers/{TrackerName}/consumers | Creates an association between a geofence collection and a tracker resource. This allows the tracker resource to communicate location data to the linked geofence collection.  You can associate up to five geofence collections to each tracker resource.  Currently not supported — Cross-account configurations, such as creating associations between a tracker resource in one account and a geofence collection in another account. |
| POST | /tracking/v0/trackers/{TrackerName}/delete-positions | Deletes the position history of one or more devices from a tracker resource. |
| POST | /tracking/v0/trackers/{TrackerName}/get-positions | Lists the latest device positions for requested devices. |
| POST | /tracking/v0/trackers/{TrackerName}/positions | Uploads position update data for one or more devices to a tracker resource (up to 10 devices per batch). Amazon Location uses the data when it reports the last known device position and position history. Amazon Location retains location data for 30 days.  Position updates are handled based on the PositionFiltering property of the tracker. When PositionFiltering is set to TimeBased, updates are evaluated against linked geofence collections, and location data is stored at a maximum of one position per 30 second interval. If your update frequency is more often than every 30 seconds, only one update per 30 seconds is stored for each unique device ID. When PositionFiltering is set to DistanceBased filtering, location data is stored and evaluated against linked geofence collections only if the device has moved more than 30 m (98.4 ft). When PositionFiltering is set to AccuracyBased filtering, location data is stored and evaluated against linked geofence collections only if the device has moved more than the measured accuracy. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is neither stored or evaluated if the device has moved less than 15 m. If PositionFiltering is set to AccuracyBased filtering, Amazon Location uses the default value { "Horizontal": 0} when accuracy is not provided on a DevicePositionUpdate. |
| POST | /tracking/v0/trackers | Creates a tracker resource in your Amazon Web Services account, which lets you retrieve current and historical location of devices. |
| DELETE | /tracking/v0/trackers/{TrackerName} | Deletes a tracker resource from your Amazon Web Services account.  This operation deletes the resource permanently. If the tracker resource is in use, you may encounter an error. Make sure that the target resource isn't a dependency for your applications. |
| GET | /tracking/v0/trackers/{TrackerName} | Retrieves the tracker resource details. |
| DELETE | /tracking/v0/trackers/{TrackerName}/consumers/{ConsumerArn} | Removes the association between a tracker resource and a geofence collection.  Once you unlink a tracker resource from a geofence collection, the tracker positions will no longer be automatically evaluated against geofences. |
| GET | /tracking/v0/trackers/{TrackerName}/devices/{DeviceId}/positions/latest | Retrieves a device's most recent position according to its sample time.  Device positions are deleted after 30 days. |
| POST | /tracking/v0/trackers/{TrackerName}/devices/{DeviceId}/list-positions | Retrieves the device position history from a tracker resource within a specified range of time.  Device positions are deleted after 30 days. |
| POST | /tracking/v0/trackers/{TrackerName}/list-positions | A batch request to retrieve all device positions. |
| POST | /tracking/v0/trackers/{TrackerName}/list-consumers | Lists geofence collections currently associated to the given tracker resource. |
| POST | /tracking/v0/list-trackers | Lists tracker resources in your Amazon Web Services account. |
| PATCH | /tracking/v0/trackers/{TrackerName} | Updates the specified properties of a given tracker resource. |
| POST | /tracking/v0/trackers/{TrackerName}/positions/verify | Verifies the integrity of the device's position by determining if it was reported behind a proxy, and by comparing it to an inferred position estimated based on the device's state. |

### geofencing
| Method | Path | Description |
|--------|------|-------------|
| POST | /geofencing/v0/collections/{CollectionName}/delete-geofences | Deletes a batch of geofences from a geofence collection.  This operation deletes the resource permanently. |
| POST | /geofencing/v0/collections/{CollectionName}/positions | Evaluates device positions against the geofence geometries from a given geofence collection. This operation always returns an empty response because geofences are asynchronously evaluated. The evaluation determines if the device has entered or exited a geofenced area, and then publishes one of the following events to Amazon EventBridge:    ENTER if Amazon Location determines that the tracked device has entered a geofenced area.    EXIT if Amazon Location determines that the tracked device has exited a geofenced area.    The last geofence that a device was observed within is tracked for 30 days after the most recent device position update.   Geofence evaluation uses the given device position. It does not account for the optional Accuracy of a DevicePositionUpdate.   The DeviceID is used as a string to represent the device. You do not need to have a Tracker associated with the DeviceID. |
| POST | /geofencing/v0/collections/{CollectionName}/put-geofences | A batch request for storing geofence geometries into a given geofence collection, or updates the geometry of an existing geofence if a geofence ID is included in the request. |
| POST | /geofencing/v0/collections | Creates a geofence collection, which manages and stores geofences. |
| DELETE | /geofencing/v0/collections/{CollectionName} | Deletes a geofence collection from your Amazon Web Services account.  This operation deletes the resource permanently. If the geofence collection is the target of a tracker resource, the devices will no longer be monitored. |
| GET | /geofencing/v0/collections/{CollectionName} | Retrieves the geofence collection details. |
| POST | /geofencing/v0/collections/{CollectionName}/forecast-geofence-events | Evaluates device positions against geofence geometries from a given geofence collection. The event forecasts three states for which a device can be in relative to a geofence:  ENTER: If a device is outside of a geofence, but would breach the fence if the device is moving at its current speed within time horizon window.  EXIT: If a device is inside of a geofence, but would breach the fence if the device is moving at its current speed within time horizon window.  IDLE: If a device is inside of a geofence, and the device is not moving. |
| GET | /geofencing/v0/collections/{CollectionName}/geofences/{GeofenceId} | Retrieves the geofence details from a geofence collection.  The returned geometry will always match the geometry format used when the geofence was created. |
| POST | /geofencing/v0/list-collections | Lists geofence collections in your Amazon Web Services account. |
| POST | /geofencing/v0/collections/{CollectionName}/list-geofences | Lists geofences stored in a given geofence collection. |
| PUT | /geofencing/v0/collections/{CollectionName}/geofences/{GeofenceId} | Stores a geofence geometry in a given geofence collection, or updates the geometry of an existing geofence if a geofence ID is included in the request. |
| PATCH | /geofencing/v0/collections/{CollectionName} | Updates the specified properties of a given geofence collection. |

### routes
| Method | Path | Description |
|--------|------|-------------|
| POST | /routes/v0/calculators/{CalculatorName}/calculate/route | Calculates a route given the following required parameters: DeparturePosition and DestinationPosition. Requires that you first create a route calculator resource. By default, a request that doesn't specify a departure time uses the best time of day to travel with the best traffic conditions when calculating the route. Additional options include:    Specifying a departure time using either DepartureTime or DepartNow. This calculates a route based on predictive traffic data at the given time.   You can't specify both DepartureTime and DepartNow in a single request. Specifying both parameters returns a validation error.     Specifying a travel mode using TravelMode sets the transportation mode used to calculate the routes. This also lets you specify additional route preferences in CarModeOptions if traveling by Car, or TruckModeOptions if traveling by Truck.  If you specify walking for the travel mode and your data provider is Esri, the start and destination must be within 40km. |
| POST | /routes/v0/calculators/{CalculatorName}/calculate/route-matrix | Calculates a route matrix given the following required parameters: DeparturePositions and DestinationPositions. CalculateRouteMatrix calculates routes and returns the travel time and travel distance from each departure position to each destination position in the request. For example, given departure positions A and B, and destination positions X and Y, CalculateRouteMatrix will return time and distance for routes from A to X, A to Y, B to X, and B to Y (in that order). The number of results returned (and routes calculated) will be the number of DeparturePositions times the number of DestinationPositions.  Your account is charged for each route calculated, not the number of requests.  Requires that you first create a route calculator resource. By default, a request that doesn't specify a departure time uses the best time of day to travel with the best traffic conditions when calculating routes. Additional options include:     Specifying a departure time using either DepartureTime or DepartNow. This calculates routes based on predictive traffic data at the given time.   You can't specify both DepartureTime and DepartNow in a single request. Specifying both parameters returns a validation error.     Specifying a travel mode using TravelMode sets the transportation mode used to calculate the routes. This also lets you specify additional route preferences in CarModeOptions if traveling by Car, or TruckModeOptions if traveling by Truck. |
| POST | /routes/v0/calculators | Creates a route calculator resource in your Amazon Web Services account. You can send requests to a route calculator resource to estimate travel time, distance, and get directions. A route calculator sources traffic and road network data from your chosen data provider.  If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the Amazon Web Services service terms for more details. |
| DELETE | /routes/v0/calculators/{CalculatorName} | Deletes a route calculator resource from your Amazon Web Services account.  This operation deletes the resource permanently. |
| GET | /routes/v0/calculators/{CalculatorName} | Retrieves the route calculator resource details. |
| POST | /routes/v0/list-calculators | Lists route calculator resources in your Amazon Web Services account. |
| PATCH | /routes/v0/calculators/{CalculatorName} | Updates the specified properties for a given route calculator resource. |

### metadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /metadata/v0/keys | Creates an API key resource in your Amazon Web Services account, which lets you grant actions for Amazon Location resources to the API key bearer.  For more information, see Using API keys. |
| DELETE | /metadata/v0/keys/{KeyName} | Deletes the specified API key. The API key must have been deactivated more than 90 days previously. |
| GET | /metadata/v0/keys/{KeyName} | Retrieves the API key resource details. |
| POST | /metadata/v0/list-keys | Lists API key resources in your Amazon Web Services account. |
| PATCH | /metadata/v0/keys/{KeyName} | Updates the specified properties of a given API key resource. |

### maps
| Method | Path | Description |
|--------|------|-------------|
| POST | /maps/v0/maps | Creates a map resource in your Amazon Web Services account, which provides map tiles of different styles sourced from global location data providers.  If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the Amazon Web Services service terms for more details. |
| DELETE | /maps/v0/maps/{MapName} | Deletes a map resource from your Amazon Web Services account.  This operation deletes the resource permanently. If the map is being used in an application, the map may not render. |
| GET | /maps/v0/maps/{MapName} | Retrieves the map resource details. |
| GET | /maps/v0/maps/{MapName}/glyphs/{FontStack}/{FontUnicodeRange} | Retrieves glyphs used to display labels on a map. |
| GET | /maps/v0/maps/{MapName}/sprites/{FileName} | Retrieves the sprite sheet corresponding to a map resource. The sprite sheet is a PNG image paired with a JSON document describing the offsets of individual icons that will be displayed on a rendered map. |
| GET | /maps/v0/maps/{MapName}/style-descriptor | Retrieves the map style descriptor from a map resource.  The style descriptor contains speciﬁcations on how features render on a map. For example, what data to display, what order to display the data in, and the style for the data. Style descriptors follow the Mapbox Style Specification. |
| GET | /maps/v0/maps/{MapName}/tiles/{Z}/{X}/{Y} | Retrieves a vector data tile from the map resource. Map tiles are used by clients to render a map. they're addressed using a grid arrangement with an X coordinate, Y coordinate, and Z (zoom) level.  The origin (0, 0) is the top left of the map. Increasing the zoom level by 1 doubles both the X and Y dimensions, so a tile containing data for the entire world at (0/0/0) will be split into 4 tiles at zoom 1 (1/0/0, 1/0/1, 1/1/0, 1/1/1). |
| POST | /maps/v0/list-maps | Lists map resources in your Amazon Web Services account. |
| PATCH | /maps/v0/maps/{MapName} | Updates the specified properties of a given map resource. |

### places
| Method | Path | Description |
|--------|------|-------------|
| POST | /places/v0/indexes | Creates a place index resource in your Amazon Web Services account. Use a place index resource to geocode addresses and other text queries by using the SearchPlaceIndexForText operation, and reverse geocode coordinates by using the SearchPlaceIndexForPosition operation, and enable autosuggestions by using the SearchPlaceIndexForSuggestions operation.  If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the Amazon Web Services service terms for more details. |
| DELETE | /places/v0/indexes/{IndexName} | Deletes a place index resource from your Amazon Web Services account.  This operation deletes the resource permanently. |
| GET | /places/v0/indexes/{IndexName} | Retrieves the place index resource details. |
| GET | /places/v0/indexes/{IndexName}/places/{PlaceId} | Finds a place by its unique ID. A PlaceId is returned by other search operations.  A PlaceId is valid only if all of the following are the same in the original search request and the call to GetPlace.   Customer Amazon Web Services account   Amazon Web Services Region   Data provider specified in the place index resource |
| POST | /places/v0/list-indexes | Lists place index resources in your Amazon Web Services account. |
| POST | /places/v0/indexes/{IndexName}/search/position | Reverse geocodes a given coordinate and returns a legible address. Allows you to search for Places or points of interest near a given position. |
| POST | /places/v0/indexes/{IndexName}/search/suggestions | Generates suggestions for addresses and points of interest based on partial or misspelled free-form text. This operation is also known as autocomplete, autosuggest, or fuzzy matching. Optional parameters let you narrow your search results by bounding box or country, or bias your search toward a specific position on the globe.  You can search for suggested place names near a specified position by using BiasPosition, or filter results within a bounding box by using FilterBBox. These parameters are mutually exclusive; using both BiasPosition and FilterBBox in the same command returns an error. |
| POST | /places/v0/indexes/{IndexName}/search/text | Geocodes free-form text, such as an address, name, city, or region to allow you to search for Places or points of interest.  Optional parameters let you narrow your search results by bounding box or country, or bias your search toward a specific position on the globe.  You can search for places near a given position using BiasPosition, or filter results within a bounding box using FilterBBox. Providing both parameters simultaneously returns an error.  Search results are returned in order of highest to lowest relevance. |
| PATCH | /places/v0/indexes/{IndexName} | Updates the specified properties of a given place index resource. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Returns a list of tags that are applied to the specified Amazon Location resource. |
| POST | /tags/{ResourceArn} | Assigns one or more tags (key-value pairs) to the specified Amazon Location Service resource. Tags can help you organize and categorize your resources. You can also use them to scope user permissions, by granting a user permission to access or change only resources with certain tag values. You can use the TagResource operation with an Amazon Location Service resource that already has tags. If you specify a new tag key for the resource, this tag is appended to the tags already associated with the resource. If you specify a tag key that's already associated with the resource, the new tag value that you specify replaces the previous value for that tag.  You can associate up to 50 tags with a resource. |
| DELETE | /tags/{ResourceArn} | Removes one or more tags from the specified Amazon Location resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a consumer?" -> POST /tracking/v0/trackers/{TrackerName}/consumers
- "Create a delete-position?" -> POST /tracking/v0/trackers/{TrackerName}/delete-positions
- "Create a delete-geofence?" -> POST /geofencing/v0/collections/{CollectionName}/delete-geofences
- "Create a position?" -> POST /geofencing/v0/collections/{CollectionName}/positions
- "Create a get-position?" -> POST /tracking/v0/trackers/{TrackerName}/get-positions
- "Create a put-geofence?" -> POST /geofencing/v0/collections/{CollectionName}/put-geofences
- "Create a position?" -> POST /tracking/v0/trackers/{TrackerName}/positions
- "Create a route?" -> POST /routes/v0/calculators/{CalculatorName}/calculate/route
- "Create a route-matrix?" -> POST /routes/v0/calculators/{CalculatorName}/calculate/route-matrix
- "Create a collection?" -> POST /geofencing/v0/collections
- "Create a key?" -> POST /metadata/v0/keys
- "Create a map?" -> POST /maps/v0/maps
- "Create a indexe?" -> POST /places/v0/indexes
- "Create a calculator?" -> POST /routes/v0/calculators
- "Create a tracker?" -> POST /tracking/v0/trackers
- "Delete a collection?" -> DELETE /geofencing/v0/collections/{CollectionName}
- "Delete a key?" -> DELETE /metadata/v0/keys/{KeyName}
- "Delete a map?" -> DELETE /maps/v0/maps/{MapName}
- "Delete a indexe?" -> DELETE /places/v0/indexes/{IndexName}
- "Delete a calculator?" -> DELETE /routes/v0/calculators/{CalculatorName}
- "Delete a tracker?" -> DELETE /tracking/v0/trackers/{TrackerName}
- "Get collection details?" -> GET /geofencing/v0/collections/{CollectionName}
- "Get key details?" -> GET /metadata/v0/keys/{KeyName}
- "Get map details?" -> GET /maps/v0/maps/{MapName}
- "Get indexe details?" -> GET /places/v0/indexes/{IndexName}
- "Get calculator details?" -> GET /routes/v0/calculators/{CalculatorName}
- "Get tracker details?" -> GET /tracking/v0/trackers/{TrackerName}
- "Delete a consumer?" -> DELETE /tracking/v0/trackers/{TrackerName}/consumers/{ConsumerArn}
- "Create a forecast-geofence-event?" -> POST /geofencing/v0/collections/{CollectionName}/forecast-geofence-events
- "List all latest?" -> GET /tracking/v0/trackers/{TrackerName}/devices/{DeviceId}/positions/latest
- "Create a list-position?" -> POST /tracking/v0/trackers/{TrackerName}/devices/{DeviceId}/list-positions
- "Get geofence details?" -> GET /geofencing/v0/collections/{CollectionName}/geofences/{GeofenceId}
- "Get glyph details?" -> GET /maps/v0/maps/{MapName}/glyphs/{FontStack}/{FontUnicodeRange}
- "Get sprite details?" -> GET /maps/v0/maps/{MapName}/sprites/{FileName}
- "List all style-descriptor?" -> GET /maps/v0/maps/{MapName}/style-descriptor
- "Get tile details?" -> GET /maps/v0/maps/{MapName}/tiles/{Z}/{X}/{Y}
- "Get place details?" -> GET /places/v0/indexes/{IndexName}/places/{PlaceId}
- "Create a list-position?" -> POST /tracking/v0/trackers/{TrackerName}/list-positions
- "Create a list-collection?" -> POST /geofencing/v0/list-collections
- "Create a list-geofence?" -> POST /geofencing/v0/collections/{CollectionName}/list-geofences
- "Create a list-key?" -> POST /metadata/v0/list-keys
- "Create a list-map?" -> POST /maps/v0/list-maps
- "Create a list-indexe?" -> POST /places/v0/list-indexes
- "Create a list-calculator?" -> POST /routes/v0/list-calculators
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a list-consumer?" -> POST /tracking/v0/trackers/{TrackerName}/list-consumers
- "Create a list-tracker?" -> POST /tracking/v0/list-trackers
- "Update a geofence?" -> PUT /geofencing/v0/collections/{CollectionName}/geofences/{GeofenceId}
- "Create a position?" -> POST /places/v0/indexes/{IndexName}/search/position
- "Create a suggestion?" -> POST /places/v0/indexes/{IndexName}/search/suggestions
- "Create a text?" -> POST /places/v0/indexes/{IndexName}/search/text
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a collection?" -> PATCH /geofencing/v0/collections/{CollectionName}
- "Partially update a key?" -> PATCH /metadata/v0/keys/{KeyName}
- "Partially update a map?" -> PATCH /maps/v0/maps/{MapName}
- "Partially update a indexe?" -> PATCH /places/v0/indexes/{IndexName}
- "Partially update a calculator?" -> PATCH /routes/v0/calculators/{CalculatorName}
- "Partially update a tracker?" -> PATCH /tracking/v0/trackers/{TrackerName}
- "Create a verify?" -> POST /tracking/v0/trackers/{TrackerName}/positions/verify
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
