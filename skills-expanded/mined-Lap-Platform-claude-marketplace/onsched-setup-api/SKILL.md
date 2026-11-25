---
name: onsched-setup-api
description: "OnSched Setup API skill. Use when working with OnSched Setup for setup. Covers 139 endpoints."
version: 1.0.0
generator: lapsh
---

# OnSched Setup API
API version: v1

## Auth
OAuth2

## Base URL
https://sandbox-api.onsched.com/

## Setup
1. Configure auth: OAuth2
2. GET /setup/v1/appointments -- verify access
3. POST /setup/v1/businessusers -- create first businessusers

## Endpoints

139 endpoints across 1 groups. See references/api-spec.lap for full details.

### setup
| Method | Path | Description |
|--------|------|-------------|
| GET | /setup/v1/appointments | List Appointments |
| GET | /setup/v1/appointments/{id} | Get Appointment |
| PUT | /setup/v1/appointments/{id}/reassign/resource/{resourceId} | Reassign Appointment |
| GET | /setup/v1/businessusers | List Users |
| POST | /setup/v1/businessusers | Create User |
| GET | /setup/v1/businessusers/{id} | Get User |
| PUT | /setup/v1/businessusers/{id} | Update User |
| DELETE | /setup/v1/businessusers/{id} | Delete User |
| GET | /setup/v1/businessusers/permissions | List User Permissions |
| GET | /setup/v1/businessusers/{email}/companies | List User Companies |
| GET | /setup/v1/calendars | List Calendars |
| POST | /setup/v1/calendars | DEPRECATING: Create |
| GET | /setup/v1/calendars/{id} | Get Calendar |
| PUT | /setup/v1/calendars/{id} | Update Calendar |
| DELETE | /setup/v1/calendars/{id} | Delete Calendar |
| PUT | /setup/v1/calendars/{id}/recover | Recover Calendar |
| GET | /setup/v1/calendars/{id}/services | List Calendar Services |
| GET | /setup/v1/calendars/{id}/blocks | List Calendar Blocks |
| GET | /setup/v1/calendars/blocks/{id} | Get Calendar Block |
| POST | /setup/v1/calendars/{id}/block | Create Calendar Block |
| PUT | /setup/v1/calendars/block/{id} | Update Calendar Block |
| DELETE | /setup/v1/calendars/block/{id} | Delete Calendar Block |
| GET | /setup/v1/companies | Get Company |
| PUT | /setup/v1/companies | Update Company |
| POST | /setup/v1/companies | Create Company |
| GET | /setup/v1/companies/domains | List Company Domains |
| POST | /setup/v1/companies/domains | Create Company Domain |
| GET | /setup/v1/companies/domains/{id} | Get Company Domain |
| PUT | /setup/v1/companies/domains/{id} | Update Company Domain |
| DELETE | /setup/v1/companies/domains/{id} | Delete Company Domain |
| GET | /setup/v1/companies/regions | List Regions |
| POST | /setup/v1/companies/regions | Create Region |
| GET | /setup/v1/companies/regions/{id} | Get Region |
| PUT | /setup/v1/companies/regions/{id} | Update Region |
| DELETE | /setup/v1/companies/regions/{id} | Delete Region |
| GET | /setup/v1/companies/email/templates | List Email Templates |
| GET | /setup/v1/companies/email/templates/{templateName} | Get Email Template |
| GET | /setup/v1/companies/email/templates/master | Get Master Template Settings |
| POST | /setup/v1/companies/email/templates/master | Create Master Template Settings |
| DELETE | /setup/v1/companies/email/templates/master | Delete Master Template Settings |
| GET | /setup/v1/companies/timezones/{date} | List Time Zones |
| GET | /setup/v1/customers | List Customers |
| GET | /setup/v1/customers/{id} | Get Customer |
| GET | /setup/v1/customers/{id}/privacy | Get Customer Data |
| GET | /setup/v1/locations | List Locations |
| POST | /setup/v1/locations | Create Location |
| GET | /setup/v1/locations/{id} | Get Location |
| PUT | /setup/v1/locations/{id} | Update Location |
| DELETE | /setup/v1/locations/{id} | Delete Location |
| POST | /setup/v1/locations/bulk | Create Locations Bulk |
| PUT | /setup/v1/locations/{id}/settings/scope/{settingsScope} | Update Location Scope |
| PUT | /setup/v1/locations/{id}/holidays/{holidayId}/{closed} | Update Location Holidays |
| PUT | /setup/v1/locations/{id}/recover | Recover Location |
| GET | /setup/v1/locations/{id}/services | List Location Linked Services |
| POST | /setup/v1/locations/{id}/services | Create Linked Service |
| DELETE | /setup/v1/locations/{id}/services | Delete Linked Services |
| GET | /setup/v1/locations/services/{id} | Get Linked Service |
| DELETE | /setup/v1/locations/services/{id} | Unlink Service |
| POST | /setup/v1/locations/{id}/uploadimage | Upload Location Image |
| DELETE | /setup/v1/locations/{id}/deleteimage | Delete Location Image |
| DELETE | /setup/v1/locations/{id}/deleteallimages | Delete All Location Images |
| GET | /setup/v1/locations/{id}/email/templates | List Email Templates |
| POST | /setup/v1/locations/{id}/email/templates | Create Custom Template |
| GET | /setup/v1/locations/{id}/email/templates/{templateName} | Get Email Template |
| DELETE | /setup/v1/locations/{id}/email/templates/{templateName} | Delete Custom Template |
| GET | /setup/v1/locations/{id}/email/templates/master | Get Master Template Settings |
| POST | /setup/v1/locations/{id}/email/templates/master | Create Master Template Settings |
| DELETE | /setup/v1/locations/{id}/email/templates/master | Delete Master Template Settings |
| GET | /setup/v1/locations/{id}/google/service/account | Google Service Account Info |
| POST | /setup/v1/locations/{id}/google/service/account | Create Google Cal Access |
| DELETE | /setup/v1/locations/{id}/google/service/account | Delete Google Cal Access |
| GET | /setup/v1/locations/{id}/appointmentreminders | Get Reminders |
| PUT | /setup/v1/locations/{id}/appointmentreminders | Update Reminders |
| GET | /setup/v1/resourcegroups | List Resource Groups |
| POST | /setup/v1/resourcegroups | Create Resource Group |
| GET | /setup/v1/resourcegroups/{id} | Get Resource Group |
| PUT | /setup/v1/resourcegroups/{id} | Update Resource Group |
| DELETE | /setup/v1/resourcegroups/{id} | Delete Resource Group |
| PUT | /setup/v1/resourcegroups/{id}/recover | Recover Resource Group |
| GET | /setup/v1/resources | List Resources |
| POST | /setup/v1/resources | Create Resource |
| GET | /setup/v1/resources/{id} | Get Resource |
| PUT | /setup/v1/resources/{id} | Update Resource |
| DELETE | /setup/v1/resources/{id} | Delete Resource |
| GET | /setup/v1/resources/{id}/calendar/auth/google/{googleEmailAddress} | Get Resource Google URL |
| GET | /setup/v1/resources/{id}/calendar/auth/outlook/{outlookEmailAddress} | Get Resource Outlook URL |
| GET | /setup/v1/resources/timezones | Get Time Zones |
| POST | /setup/v1/resources/bulk | Create Resources Bulk |
| PUT | /setup/v1/resources/bulk | Update Resources Bulk |
| PUT | /setup/v1/resources/{id}/reassign/appointments/{resourceId} | Reassign Resource |
| PUT | /setup/v1/resources/{id}/recover | Recover Resource |
| GET | /setup/v1/resources/{id}/availability | List Weekly Availability |
| PUT | /setup/v1/resources/{id}/availability | Update Weekly Availability |
| GET | /setup/v1/resources/{id}/allocations | List Resource Allocations |
| POST | /setup/v1/resources/{id}/allocations | Create Allocation |
| GET | /setup/v1/resources/allocations/{id} | Get Allocation |
| PUT | /setup/v1/resources/allocations/{id} | Update Allocation |
| DELETE | /setup/v1/resources/allocations/{id} | Delete Allocation |
| GET | /setup/v1/resources/{id}/blocks | List Resource Blocks |
| GET | /setup/v1/resources/blocks/{id} | Get Block |
| POST | /setup/v1/resources/{id}/block | Create Block |
| PUT | /setup/v1/resources/block/{id} | Update Block |
| DELETE | /setup/v1/resources/block/{id} | Delete Block |
| POST | /setup/v1/resources/{id}/services | Create Linked Services |
| PUT | /setup/v1/resources/{id}/services | Update Linked Services |
| DELETE | /setup/v1/resources/{id}/services | Delete Linked Services |
| POST | /setup/v1/resources/{id}/uploadimage | Upload Resource Image |
| DELETE | /setup/v1/resources/{id}/deleteimage | Delete Resource Image |
| GET | /setup/v1/servicegroups | List Service Groups |
| POST | /setup/v1/servicegroups | Create Service Group |
| GET | /setup/v1/servicegroups/{id} | Get Service Group |
| PUT | /setup/v1/servicegroups/{id} | Update Service Group |
| DELETE | /setup/v1/servicegroups/{id} | Delete Service Group |
| PUT | /setup/v1/servicegroups/{id}/recover | Recover Service Group |
| GET | /setup/v1/services | List Services |
| POST | /setup/v1/services | Create Service |
| GET | /setup/v1/services/{id} | Get Service |
| PUT | /setup/v1/services/{id} | Update Service |
| DELETE | /setup/v1/services/{id} | Delete Service |
| GET | /setup/v1/services/{id}/resources | List Resources for Service |
| PUT | /setup/v1/services/{id}/recover | Recover Service |
| GET | /setup/v1/services/{id}/blocks | List Service Blocks |
| GET | /setup/v1/services/blocks/{id} | Get Block |
| POST | /setup/v1/services/{id}/block | Create Block |
| PUT | /setup/v1/services/block/{id} | Update Block |
| DELETE | /setup/v1/services/block/{id} | Delete Block |
| GET | /setup/v1/services/{id}/calendar | Get Linked Calendar |
| POST | /setup/v1/services/calendar | Link Service to Calendar |
| DELETE | /setup/v1/services/calendar/{id} | Delete Service Links |
| GET | /setup/v1/services/{id}/availability | Get Weekly Availability |
| PUT | /setup/v1/services/{id}/availability | Update Weekly Availability |
| GET | /setup/v1/services/{id}/allocations | List Service Allocations |
| POST | /setup/v1/services/{id}/allocations | Create Allocation |
| GET | /setup/v1/services/allocations/{id} | Get Allocation |
| PUT | /setup/v1/services/allocations/{id} | Update Allocation |
| DELETE | /setup/v1/services/allocations/{id} | Delete Allocation |
| POST | /setup/v1/services/{id}/allocations/bulk | Create Allocations Bulk |
| POST | /setup/v1/services/{id}/uploadimage | Upload Service Image |
| DELETE | /setup/v1/services/{id}/deleteimage | Delete Service Image |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all appointments?" -> GET /setup/v1/appointments
- "Get appointment details?" -> GET /setup/v1/appointments/{id}
- "Update a resource?" -> PUT /setup/v1/appointments/{id}/reassign/resource/{resourceId}
- "List all businessusers?" -> GET /setup/v1/businessusers
- "Create a businessuser?" -> POST /setup/v1/businessusers
- "Get businessuser details?" -> GET /setup/v1/businessusers/{id}
- "Update a businessuser?" -> PUT /setup/v1/businessusers/{id}
- "Delete a businessuser?" -> DELETE /setup/v1/businessusers/{id}
- "List all permissions?" -> GET /setup/v1/businessusers/permissions
- "List all companies?" -> GET /setup/v1/businessusers/{email}/companies
- "List all calendars?" -> GET /setup/v1/calendars
- "Create a calendar?" -> POST /setup/v1/calendars
- "Get calendar details?" -> GET /setup/v1/calendars/{id}
- "Update a calendar?" -> PUT /setup/v1/calendars/{id}
- "Delete a calendar?" -> DELETE /setup/v1/calendars/{id}
- "List all services?" -> GET /setup/v1/calendars/{id}/services
- "List all blocks?" -> GET /setup/v1/calendars/{id}/blocks
- "Get block details?" -> GET /setup/v1/calendars/blocks/{id}
- "Create a block?" -> POST /setup/v1/calendars/{id}/block
- "Update a block?" -> PUT /setup/v1/calendars/block/{id}
- "Delete a block?" -> DELETE /setup/v1/calendars/block/{id}
- "List all companies?" -> GET /setup/v1/companies
- "Create a company?" -> POST /setup/v1/companies
- "List all domains?" -> GET /setup/v1/companies/domains
- "Create a domain?" -> POST /setup/v1/companies/domains
- "Get domain details?" -> GET /setup/v1/companies/domains/{id}
- "Update a domain?" -> PUT /setup/v1/companies/domains/{id}
- "Delete a domain?" -> DELETE /setup/v1/companies/domains/{id}
- "List all regions?" -> GET /setup/v1/companies/regions
- "Create a region?" -> POST /setup/v1/companies/regions
- "Get region details?" -> GET /setup/v1/companies/regions/{id}
- "Update a region?" -> PUT /setup/v1/companies/regions/{id}
- "Delete a region?" -> DELETE /setup/v1/companies/regions/{id}
- "List all templates?" -> GET /setup/v1/companies/email/templates
- "Get template details?" -> GET /setup/v1/companies/email/templates/{templateName}
- "List all master?" -> GET /setup/v1/companies/email/templates/master
- "Create a master?" -> POST /setup/v1/companies/email/templates/master
- "Get timezone details?" -> GET /setup/v1/companies/timezones/{date}
- "List all customers?" -> GET /setup/v1/customers
- "Get customer details?" -> GET /setup/v1/customers/{id}
- "List all privacy?" -> GET /setup/v1/customers/{id}/privacy
- "List all locations?" -> GET /setup/v1/locations
- "Create a location?" -> POST /setup/v1/locations
- "Get location details?" -> GET /setup/v1/locations/{id}
- "Update a location?" -> PUT /setup/v1/locations/{id}
- "Delete a location?" -> DELETE /setup/v1/locations/{id}
- "Create a bulk?" -> POST /setup/v1/locations/bulk
- "Update a scope?" -> PUT /setup/v1/locations/{id}/settings/scope/{settingsScope}
- "Update a holiday?" -> PUT /setup/v1/locations/{id}/holidays/{holidayId}/{closed}
- "List all services?" -> GET /setup/v1/locations/{id}/services
- "Create a service?" -> POST /setup/v1/locations/{id}/services
- "Get service details?" -> GET /setup/v1/locations/services/{id}
- "Delete a service?" -> DELETE /setup/v1/locations/services/{id}
- "Create a uploadimage?" -> POST /setup/v1/locations/{id}/uploadimage
- "List all templates?" -> GET /setup/v1/locations/{id}/email/templates
- "Create a template?" -> POST /setup/v1/locations/{id}/email/templates
- "Get template details?" -> GET /setup/v1/locations/{id}/email/templates/{templateName}
- "Delete a template?" -> DELETE /setup/v1/locations/{id}/email/templates/{templateName}
- "List all master?" -> GET /setup/v1/locations/{id}/email/templates/master
- "Create a master?" -> POST /setup/v1/locations/{id}/email/templates/master
- "List all account?" -> GET /setup/v1/locations/{id}/google/service/account
- "Create a account?" -> POST /setup/v1/locations/{id}/google/service/account
- "List all appointmentreminders?" -> GET /setup/v1/locations/{id}/appointmentreminders
- "List all resourcegroups?" -> GET /setup/v1/resourcegroups
- "Create a resourcegroup?" -> POST /setup/v1/resourcegroups
- "Get resourcegroup details?" -> GET /setup/v1/resourcegroups/{id}
- "Update a resourcegroup?" -> PUT /setup/v1/resourcegroups/{id}
- "Delete a resourcegroup?" -> DELETE /setup/v1/resourcegroups/{id}
- "List all resources?" -> GET /setup/v1/resources
- "Create a resource?" -> POST /setup/v1/resources
- "Get resource details?" -> GET /setup/v1/resources/{id}
- "Update a resource?" -> PUT /setup/v1/resources/{id}
- "Delete a resource?" -> DELETE /setup/v1/resources/{id}
- "Get google details?" -> GET /setup/v1/resources/{id}/calendar/auth/google/{googleEmailAddress}
- "Get outlook details?" -> GET /setup/v1/resources/{id}/calendar/auth/outlook/{outlookEmailAddress}
- "List all timezones?" -> GET /setup/v1/resources/timezones
- "Create a bulk?" -> POST /setup/v1/resources/bulk
- "Update a appointment?" -> PUT /setup/v1/resources/{id}/reassign/appointments/{resourceId}
- "List all availability?" -> GET /setup/v1/resources/{id}/availability
- "List all allocations?" -> GET /setup/v1/resources/{id}/allocations
- "Create a allocation?" -> POST /setup/v1/resources/{id}/allocations
- "Get allocation details?" -> GET /setup/v1/resources/allocations/{id}
- "Update a allocation?" -> PUT /setup/v1/resources/allocations/{id}
- "Delete a allocation?" -> DELETE /setup/v1/resources/allocations/{id}
- "List all blocks?" -> GET /setup/v1/resources/{id}/blocks
- "Get block details?" -> GET /setup/v1/resources/blocks/{id}
- "Create a block?" -> POST /setup/v1/resources/{id}/block
- "Update a block?" -> PUT /setup/v1/resources/block/{id}
- "Delete a block?" -> DELETE /setup/v1/resources/block/{id}
- "Create a service?" -> POST /setup/v1/resources/{id}/services
- "Create a uploadimage?" -> POST /setup/v1/resources/{id}/uploadimage
- "List all servicegroups?" -> GET /setup/v1/servicegroups
- "Create a servicegroup?" -> POST /setup/v1/servicegroups
- "Get servicegroup details?" -> GET /setup/v1/servicegroups/{id}
- "Update a servicegroup?" -> PUT /setup/v1/servicegroups/{id}
- "Delete a servicegroup?" -> DELETE /setup/v1/servicegroups/{id}
- "List all services?" -> GET /setup/v1/services
- "Create a service?" -> POST /setup/v1/services
- "Get service details?" -> GET /setup/v1/services/{id}
- "Update a service?" -> PUT /setup/v1/services/{id}
- "Delete a service?" -> DELETE /setup/v1/services/{id}
- "List all resources?" -> GET /setup/v1/services/{id}/resources
- "List all blocks?" -> GET /setup/v1/services/{id}/blocks
- "Get block details?" -> GET /setup/v1/services/blocks/{id}
- "Create a block?" -> POST /setup/v1/services/{id}/block
- "Update a block?" -> PUT /setup/v1/services/block/{id}
- "Delete a block?" -> DELETE /setup/v1/services/block/{id}
- "List all calendar?" -> GET /setup/v1/services/{id}/calendar
- "Create a calendar?" -> POST /setup/v1/services/calendar
- "Delete a calendar?" -> DELETE /setup/v1/services/calendar/{id}
- "List all availability?" -> GET /setup/v1/services/{id}/availability
- "List all allocations?" -> GET /setup/v1/services/{id}/allocations
- "Create a allocation?" -> POST /setup/v1/services/{id}/allocations
- "Get allocation details?" -> GET /setup/v1/services/allocations/{id}
- "Update a allocation?" -> PUT /setup/v1/services/allocations/{id}
- "Delete a allocation?" -> DELETE /setup/v1/services/allocations/{id}
- "Create a bulk?" -> POST /setup/v1/services/{id}/allocations/bulk
- "Create a uploadimage?" -> POST /setup/v1/services/{id}/uploadimage
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
