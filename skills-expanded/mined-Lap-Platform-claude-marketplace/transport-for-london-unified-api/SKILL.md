---
name: transport-for-london-unified-api
description: "Transport for London Unified API skill. Use when working with Transport for London Unified for AccidentStats, AirQuality, BikePoint. Covers 84 endpoints."
version: 1.0.0
generator: lapsh
---

# Transport for London Unified API
API version: v1

## Auth
ApiKey app_key in query | ApiKey app_id in query

## Base URL
https://api.digital.tfl.gov.uk

## Setup
1. Set your API key in the appropriate header
2. GET /AirQuality -- verify access

## Endpoints

84 endpoints across 14 groups. See references/api-spec.lap for full details.

### AccidentStats
| Method | Path | Description |
|--------|------|-------------|
| GET | /AccidentStats/{year} | Gets all accident details for accidents occuring in the specified year |

### AirQuality
| Method | Path | Description |
|--------|------|-------------|
| GET | /AirQuality | Gets air quality data feed |

### BikePoint
| Method | Path | Description |
|--------|------|-------------|
| GET | /BikePoint | Gets all bike point locations. The Place object has an addtionalProperties array which contains the nbBikes, nbDocks and nbSpaces |
| GET | /BikePoint/{id} | Gets the bike point with the given id. |
| GET | /BikePoint/Search | Search for bike stations by their name, a bike point's name often contains information about the name of the street |

### Cabwise
| Method | Path | Description |
|--------|------|-------------|
| GET | /Cabwise/search | Gets taxis and minicabs contact information |

### Journey
| Method | Path | Description |
|--------|------|-------------|
| GET | /Journey/Meta/Modes | Gets a list of all of the available journey planner modes |
| GET | /Journey/JourneyResults/{from}/to/{to} | Perform a Journey Planner search from the parameters specified in simple types |

### Line
| Method | Path | Description |
|--------|------|-------------|
| GET | /Line/Meta/Modes | Gets a list of valid modes |
| GET | /Line/Meta/Severity | Gets a list of valid severity codes |
| GET | /Line/Meta/DisruptionCategories | Gets a list of valid disruption categories |
| GET | /Line/Meta/ServiceTypes | Gets a list of valid ServiceTypes to filter on |
| GET | /Line/{ids} | Gets lines that match the specified line ids. |
| GET | /Line/Mode/{modes} | Gets lines that serve the given modes. |
| GET | /Line/Route | Get all valid routes for all lines, including the name and id of the originating and terminating stops for each route. |
| GET | /Line/{ids}/Route | Get all valid routes for given line ids, including the name and id of the originating and terminating stops for each route. |
| GET | /Line/Mode/{modes}/Route | Gets all lines and their valid routes for given modes, including the name and id of the originating and terminating stops for each route |
| GET | /Line/{id}/Route/Sequence/{direction} | Gets all valid routes for given line id, including the sequence of stops on each route. |
| GET | /Line/{ids}/Status/{StartDate}/to/{EndDate} | Gets the line status for given line ids during the provided dates e.g Minor Delays |
| GET | /Line/{ids}/Status | Gets the line status of for given line ids e.g Minor Delays |
| GET | /Line/Search/{query} | Search for lines or routes matching the query string |
| GET | /Line/Status/{severity} | Gets the line status for all lines with a given severity |
| GET | /Line/Mode/{modes}/Status | Gets the line status of for all lines for the given modes |
| GET | /Line/{id}/StopPoints | Gets a list of the stations that serve the given line id |
| GET | /Line/{id}/Timetable/{fromStopPointId} | Gets the timetable for a specified station on the give line |
| GET | /Line/{id}/Timetable/{fromStopPointId}/to/{toStopPointId} | Gets the timetable for a specified station on the give line with specified destination |
| GET | /Line/{ids}/Disruption | Get disruptions for the given line ids |
| GET | /Line/Mode/{modes}/Disruption | Get disruptions for all lines of the given modes. |
| GET | /Line/{ids}/Arrivals/{stopPointId} | Get the list of arrival predictions for given line ids based at the given stop |

### Mode
| Method | Path | Description |
|--------|------|-------------|
| GET | /Mode/ActiveServiceTypes | Returns the service type active for a mode. |
| GET | /Mode/{mode}/Arrivals | Gets the next arrival predictions for all stops of a given mode |

### Occupancy
| Method | Path | Description |
|--------|------|-------------|
| GET | /Occupancy/CarPark/{id} | Gets the occupancy for a car park with a given id |
| GET | /Occupancy/CarPark | Gets the occupancy for all car parks that have occupancy data |
| GET | /Occupancy/ChargeConnector/{ids} | Gets the occupancy for a charge connectors with a given id (sourceSystemPlaceId) |
| GET | /Occupancy/ChargeConnector | Gets the occupancy for all charge connectors |
| GET | /Occupancy/BikePoints/{ids} | Get the occupancy for bike points. |

### Place
| Method | Path | Description |
|--------|------|-------------|
| GET | /Place/Meta/Categories | Gets a list of all of the available place property categories and keys. |
| GET | /Place/Meta/PlaceTypes | Gets a list of the available types of Place. |
| GET | /Place/Address/Streets/{Postcode} | Gets the set of streets associated with a post code. |
| GET | /Place/Type/{types} | Gets all places of a given type |
| GET | /Place/{id} | Gets the place with the given id. |
| GET | /Place | Gets the places that lie within a geographic region. The geographic region of interest can either be specified |
| GET | /Place/{type}/At/{Lat}/{Lon} | Gets any places of the given type whose geography intersects the given latitude and longitude. In practice this means the Place |
| GET | /Place/{type}/overlay/{z}/{Lat}/{Lon}/{width}/{height} | Gets the place overlay for a given set of co-ordinates and a given width/height. |
| GET | /Place/Search | Gets all places that matches the given query |

### Road
| Method | Path | Description |
|--------|------|-------------|
| GET | /Road | Gets all roads managed by TfL |
| GET | /Road/{ids} | Gets the road with the specified id (e.g. A1) |
| GET | /Road/{ids}/Status | Gets the specified roads with the status aggregated over the date range specified, or now until the end of today if no dates are passed. |
| GET | /Road/{ids}/Disruption | Get active disruptions, filtered by road ids |
| GET | /Road/all/Street/Disruption | Gets a list of disrupted streets. If no date filters are provided, current disruptions are returned. |
| GET | /Road/all/Disruption/{disruptionIds} | Gets a list of active disruptions filtered by disruption Ids. |
| GET | /Road/Meta/Categories | Gets a list of valid RoadDisruption categories |
| GET | /Road/Meta/Severities | Gets a list of valid RoadDisruption severity codes |

### Search
| Method | Path | Description |
|--------|------|-------------|
| GET | /Search | Search the site for occurrences of the query string. The maximum number of results returned is equal to the maximum page size |
| GET | /Search/BusSchedules | Searches the bus schedules folder on S3 for a given bus number. |
| GET | /Search/Meta/SearchProviders | Gets the available searchProvider names. |
| GET | /Search/Meta/Categories | Gets the available search categories. |
| GET | /Search/Meta/Sorts | Gets the available sorting options. |

### StopPoint
| Method | Path | Description |
|--------|------|-------------|
| GET | /StopPoint/Meta/Categories | Gets the list of available StopPoint additional information categories |
| GET | /StopPoint/Meta/StopTypes | Gets the list of available StopPoint types |
| GET | /StopPoint/Meta/Modes | Gets the list of available StopPoint modes |
| GET | /StopPoint/{ids} | Gets a list of StopPoints corresponding to the given list of stop ids. |
| GET | /StopPoint/{id}/placeTypes | Get a list of places corresponding to a given id and place types. |
| GET | /StopPoint/{id}/Crowding/{line} | Gets all the Crowding data (static) for the StopPointId, plus crowding data for a given line and optionally a particular direction. |
| GET | /StopPoint/Type/{types} | Gets all stop points of a given type |
| GET | /StopPoint/Type/{types}/page/{page} | Gets all the stop points of given type(s) with a page number |
| GET | /StopPoint/ServiceTypes | Gets the service types for a given stoppoint |
| GET | /StopPoint/{id}/Arrivals | Gets the list of arrival predictions for the given stop point id |
| GET | /StopPoint/{id}/ArrivalDepartures | Gets the list of arrival and departure predictions for the given stop point id (overground, Elizabeth line and thameslink only) |
| GET | /StopPoint/{id}/CanReachOnLine/{lineId} | Gets Stopoints that are reachable from a station/line combination. |
| GET | /StopPoint/{id}/Route | Returns the route sections for all the lines that service the given stop point ids |
| GET | /StopPoint/Mode/{modes}/Disruption | Gets a distinct list of disrupted stop points for the given modes |
| GET | /StopPoint/{ids}/Disruption | Gets all disruptions for the specified StopPointId, plus disruptions for any child Naptan records it may have. |
| GET | /StopPoint/{id}/DirectionTo/{toStopPointId} | Returns the canonical direction, "inbound" or "outbound", for a given pair of stop point Ids in the direction from -&gt; to. |
| GET | /StopPoint | Gets a list of StopPoints within {radius} by the specified criteria |
| GET | /StopPoint/Mode/{modes} | Gets a list of StopPoints filtered by the modes available at that StopPoint. |
| GET | /StopPoint/Search/{query} | Search StopPoints by their common name, or their 5-digit Countdown Bus Stop Code. |
| GET | /StopPoint/Search | Search StopPoints by their common name, or their 5-digit Countdown Bus Stop Code. |
| GET | /StopPoint/Sms/{id} | Gets a StopPoint for a given sms code. |
| GET | /StopPoint/{stopPointId}/TaxiRanks | Gets a list of taxi ranks corresponding to the given stop point id. |
| GET | /StopPoint/{stopPointId}/CarParks | Get car parks corresponding to the given stop point id. |

### TravelTimes
| Method | Path | Description |
|--------|------|-------------|
| GET | /TravelTimes/overlay/{z}/mapcenter/{mapCenterLat}/{mapCenterLon}/pinlocation/{pinLat}/{pinLon}/dimensions/{width}/{height} | Gets the TravelTime overlay. |
| GET | /TravelTimes/compareOverlay/{z}/mapcenter/{mapCenterLat}/{mapCenterLon}/pinlocation/{pinLat}/{pinLon}/dimensions/{width}/{height} | Gets the TravelTime overlay. |

### Vehicle
| Method | Path | Description |
|--------|------|-------------|
| GET | /Vehicle/{ids}/Arrivals | Gets the predictions for a given list of vehicle Id's. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get AccidentStat details?" -> GET /AccidentStats/{year}
- "List all AirQuality?" -> GET /AirQuality
- "List all BikePoint?" -> GET /BikePoint
- "Get BikePoint details?" -> GET /BikePoint/{id}
- "Search Search?" -> GET /BikePoint/Search
- "List all search?" -> GET /Cabwise/search
- "List all Modes?" -> GET /Journey/Meta/Modes
- "Get to details?" -> GET /Journey/JourneyResults/{from}/to/{to}
- "List all Modes?" -> GET /Line/Meta/Modes
- "List all Severity?" -> GET /Line/Meta/Severity
- "List all DisruptionCategories?" -> GET /Line/Meta/DisruptionCategories
- "List all ServiceTypes?" -> GET /Line/Meta/ServiceTypes
- "Get Line details?" -> GET /Line/{ids}
- "Get Mode details?" -> GET /Line/Mode/{modes}
- "List all Route?" -> GET /Line/Route
- "List all Route?" -> GET /Line/{ids}/Route
- "List all Route?" -> GET /Line/Mode/{modes}/Route
- "Get Sequence details?" -> GET /Line/{id}/Route/Sequence/{direction}
- "Get to details?" -> GET /Line/{ids}/Status/{StartDate}/to/{EndDate}
- "List all Status?" -> GET /Line/{ids}/Status
- "Search Search?" -> GET /Line/Search/{query}
- "Get Status details?" -> GET /Line/Status/{severity}
- "List all Status?" -> GET /Line/Mode/{modes}/Status
- "List all StopPoints?" -> GET /Line/{id}/StopPoints
- "Get Timetable details?" -> GET /Line/{id}/Timetable/{fromStopPointId}
- "Get to details?" -> GET /Line/{id}/Timetable/{fromStopPointId}/to/{toStopPointId}
- "List all Disruption?" -> GET /Line/{ids}/Disruption
- "List all Disruption?" -> GET /Line/Mode/{modes}/Disruption
- "Get Arrival details?" -> GET /Line/{ids}/Arrivals/{stopPointId}
- "List all ActiveServiceTypes?" -> GET /Mode/ActiveServiceTypes
- "List all Arrivals?" -> GET /Mode/{mode}/Arrivals
- "Get CarPark details?" -> GET /Occupancy/CarPark/{id}
- "List all CarPark?" -> GET /Occupancy/CarPark
- "Get ChargeConnector details?" -> GET /Occupancy/ChargeConnector/{ids}
- "List all ChargeConnector?" -> GET /Occupancy/ChargeConnector
- "Get BikePoint details?" -> GET /Occupancy/BikePoints/{ids}
- "List all Categories?" -> GET /Place/Meta/Categories
- "List all PlaceTypes?" -> GET /Place/Meta/PlaceTypes
- "Get Street details?" -> GET /Place/Address/Streets/{Postcode}
- "Get Type details?" -> GET /Place/Type/{types}
- "Get Place details?" -> GET /Place/{id}
- "List all Place?" -> GET /Place
- "Get At details?" -> GET /Place/{type}/At/{Lat}/{Lon}
- "Get overlay details?" -> GET /Place/{type}/overlay/{z}/{Lat}/{Lon}/{width}/{height}
- "List all Search?" -> GET /Place/Search
- "List all Road?" -> GET /Road
- "Get Road details?" -> GET /Road/{ids}
- "List all Status?" -> GET /Road/{ids}/Status
- "List all Disruption?" -> GET /Road/{ids}/Disruption
- "List all Disruption?" -> GET /Road/all/Street/Disruption
- "Get Disruption details?" -> GET /Road/all/Disruption/{disruptionIds}
- "List all Categories?" -> GET /Road/Meta/Categories
- "List all Severities?" -> GET /Road/Meta/Severities
- "Search Search?" -> GET /Search
- "Search BusSchedules?" -> GET /Search/BusSchedules
- "List all SearchProviders?" -> GET /Search/Meta/SearchProviders
- "List all Categories?" -> GET /Search/Meta/Categories
- "List all Sorts?" -> GET /Search/Meta/Sorts
- "List all Categories?" -> GET /StopPoint/Meta/Categories
- "List all StopTypes?" -> GET /StopPoint/Meta/StopTypes
- "List all Modes?" -> GET /StopPoint/Meta/Modes
- "Get StopPoint details?" -> GET /StopPoint/{ids}
- "List all placeTypes?" -> GET /StopPoint/{id}/placeTypes
- "Get Crowding details?" -> GET /StopPoint/{id}/Crowding/{line}
- "Get Type details?" -> GET /StopPoint/Type/{types}
- "Get page details?" -> GET /StopPoint/Type/{types}/page/{page}
- "List all ServiceTypes?" -> GET /StopPoint/ServiceTypes
- "List all Arrivals?" -> GET /StopPoint/{id}/Arrivals
- "List all ArrivalDepartures?" -> GET /StopPoint/{id}/ArrivalDepartures
- "Get CanReachOnLine details?" -> GET /StopPoint/{id}/CanReachOnLine/{lineId}
- "List all Route?" -> GET /StopPoint/{id}/Route
- "List all Disruption?" -> GET /StopPoint/Mode/{modes}/Disruption
- "List all Disruption?" -> GET /StopPoint/{ids}/Disruption
- "Get DirectionTo details?" -> GET /StopPoint/{id}/DirectionTo/{toStopPointId}
- "List all StopPoint?" -> GET /StopPoint
- "Get Mode details?" -> GET /StopPoint/Mode/{modes}
- "Search Search?" -> GET /StopPoint/Search/{query}
- "Search Search?" -> GET /StopPoint/Search
- "Get Sm details?" -> GET /StopPoint/Sms/{id}
- "List all TaxiRanks?" -> GET /StopPoint/{stopPointId}/TaxiRanks
- "List all CarParks?" -> GET /StopPoint/{stopPointId}/CarParks
- "Get dimension details?" -> GET /TravelTimes/overlay/{z}/mapcenter/{mapCenterLat}/{mapCenterLon}/pinlocation/{pinLat}/{pinLon}/dimensions/{width}/{height}
- "Get dimension details?" -> GET /TravelTimes/compareOverlay/{z}/mapcenter/{mapCenterLat}/{mapCenterLon}/pinlocation/{pinLat}/{pinLon}/dimensions/{width}/{height}
- "List all Arrivals?" -> GET /Vehicle/{ids}/Arrivals
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
