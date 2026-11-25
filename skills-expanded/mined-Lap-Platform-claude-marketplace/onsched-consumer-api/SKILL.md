---
name: onsched-consumer-api
description: "OnSched Consumer API skill. Use when working with OnSched Consumer for consumer. Covers 38 endpoints."
version: 1.0.0
generator: lapsh
---

# OnSched Consumer API
API version: v1

## Auth
OAuth2

## Base URL
https://sandbox-api.onsched.com/

## Setup
1. Configure auth: OAuth2
2. GET /consumer/v1/appointments -- verify access
3. POST /consumer/v1/appointments -- create first appointments

## Endpoints

38 endpoints across 1 groups. See references/api-spec.lap for full details.

### consumer
| Method | Path | Description |
|--------|------|-------------|
| GET | /consumer/v1/appointments | Get Appointments |
| POST | /consumer/v1/appointments | Create Appointment |
| GET | /consumer/v1/appointments/{id} | Get Appointment |
| DELETE | /consumer/v1/appointments/{id} | Delete Appointment |
| PUT | /consumer/v1/appointments/{id}/book | Book Appointment |
| PUT | /consumer/v1/appointments/{id}/reserve | Reserve Appointment |
| PUT | /consumer/v1/appointments/{id}/cancel | Cancel Appointment |
| PUT | /consumer/v1/appointments/{id}/reschedule | Reschedule Appointment |
| PUT | /consumer/v1/appointments/{id}/noshow | Set NoShow Status |
| PUT | /consumer/v1/appointments/{id}/confirm | Confirm Appointment |
| GET | /consumer/v1/appointments/customfields | Get Custom Fields List |
| GET | /consumer/v1/appointments/bookingfields | Get Custom Fields Labels |
| GET | /consumer/v1/availability/{serviceId}/{startDate}/{endDate} | Get Available Times |
| GET | /consumer/v1/availability/{serviceId}/{startDate}/{endDate}/days | Get Available Days |
| GET | /consumer/v1/availability/{serviceId}/{startDate}/{endDate}/unavailable | Get Unavailable Times |
| GET | /consumer/v1/customers | List Customers |
| POST | /consumer/v1/customers | Create Customer |
| GET | /consumer/v1/customers/{id} | Get Customer |
| PUT | /consumer/v1/customers/{id} | Update Customer |
| DELETE | /consumer/v1/customers/{id} | Delete Customer |
| GET | /consumer/v1/customers/customfields | Get Customer Custom Fields |
| GET | /consumer/v1/customers/bookingfields | Get Customer Booking Fields |
| GET | /consumer/v1/customers/countries | List Country Codes |
| GET | /consumer/v1/customers/states | List Country States |
| GET | /consumer/v1/locations | List Locations |
| GET | /consumer/v1/locations/{id} | Get Location |
| GET | /consumer/v1/resourcegroups | List Resource Groups |
| GET | /consumer/v1/resourcegroups/{id} | Get Resource Group |
| GET | /consumer/v1/resources | List Resources |
| GET | /consumer/v1/resources/{id} | Get Resource |
| GET | /consumer/v1/resources/{id}/services | Get Resource Linked Services |
| GET | /consumer/v1/servicegroups | List Service Groups |
| GET | /consumer/v1/servicegroups/{id} | Get Service Group |
| GET | /consumer/v1/services | List Services |
| GET | /consumer/v1/services/{id} | Get Service |
| GET | /consumer/v1/services/{id}/resources | List Resources for Service |
| GET | /consumer/v1/services/{id}/allocations | List Service Allocations |
| GET | /consumer/v1/services/allocations/{id} | Get Service Allocation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all appointments?" -> GET /consumer/v1/appointments
- "Create a appointment?" -> POST /consumer/v1/appointments
- "Get appointment details?" -> GET /consumer/v1/appointments/{id}
- "Delete a appointment?" -> DELETE /consumer/v1/appointments/{id}
- "List all customfields?" -> GET /consumer/v1/appointments/customfields
- "List all bookingfields?" -> GET /consumer/v1/appointments/bookingfields
- "Get availability details?" -> GET /consumer/v1/availability/{serviceId}/{startDate}/{endDate}
- "List all days?" -> GET /consumer/v1/availability/{serviceId}/{startDate}/{endDate}/days
- "List all unavailable?" -> GET /consumer/v1/availability/{serviceId}/{startDate}/{endDate}/unavailable
- "List all customers?" -> GET /consumer/v1/customers
- "Create a customer?" -> POST /consumer/v1/customers
- "Get customer details?" -> GET /consumer/v1/customers/{id}
- "Update a customer?" -> PUT /consumer/v1/customers/{id}
- "Delete a customer?" -> DELETE /consumer/v1/customers/{id}
- "List all customfields?" -> GET /consumer/v1/customers/customfields
- "List all bookingfields?" -> GET /consumer/v1/customers/bookingfields
- "List all countries?" -> GET /consumer/v1/customers/countries
- "List all states?" -> GET /consumer/v1/customers/states
- "List all locations?" -> GET /consumer/v1/locations
- "Get location details?" -> GET /consumer/v1/locations/{id}
- "List all resourcegroups?" -> GET /consumer/v1/resourcegroups
- "Get resourcegroup details?" -> GET /consumer/v1/resourcegroups/{id}
- "List all resources?" -> GET /consumer/v1/resources
- "Get resource details?" -> GET /consumer/v1/resources/{id}
- "List all services?" -> GET /consumer/v1/resources/{id}/services
- "List all servicegroups?" -> GET /consumer/v1/servicegroups
- "Get servicegroup details?" -> GET /consumer/v1/servicegroups/{id}
- "List all services?" -> GET /consumer/v1/services
- "Get service details?" -> GET /consumer/v1/services/{id}
- "List all resources?" -> GET /consumer/v1/services/{id}/resources
- "List all allocations?" -> GET /consumer/v1/services/{id}/allocations
- "Get allocation details?" -> GET /consumer/v1/services/allocations/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
