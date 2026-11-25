---
name: hris-api
description: "HRIS API skill. Use when working with HRIS for hris. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# HRIS API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /hris/employees -- verify access
3. POST /hris/employees -- create first employees

## Endpoints

25 endpoints across 1 groups. See references/api-spec.lap for full details.

### hris
| Method | Path | Description |
|--------|------|-------------|
| GET | /hris/employees | List Employees |
| POST | /hris/employees | Create Employee |
| GET | /hris/employees/{id} | Get Employee |
| PATCH | /hris/employees/{id} | Update Employee |
| DELETE | /hris/employees/{id} | Delete Employee |
| GET | /hris/companies | List Companies |
| POST | /hris/companies | Create Company |
| GET | /hris/companies/{id} | Get Company |
| PATCH | /hris/companies/{id} | Update Company |
| DELETE | /hris/companies/{id} | Delete Company |
| GET | /hris/departments | List Departments |
| POST | /hris/departments | Create Department |
| GET | /hris/departments/{id} | Get Department |
| PATCH | /hris/departments/{id} | Update Department |
| DELETE | /hris/departments/{id} | Delete Department |
| GET | /hris/payrolls | List Payroll |
| GET | /hris/payrolls/{payroll_id} | Get Payroll |
| GET | /hris/payrolls/employees/{employee_id} | List Employee Payrolls |
| GET | /hris/payrolls/employees/{employee_id}/payrolls/{payroll_id} | Get Employee Payroll |
| GET | /hris/schedules/employees/{employee_id} | List Employee Schedules |
| GET | /hris/time-off-requests | List Time Off Requests |
| POST | /hris/time-off-requests | Create Time Off Request |
| GET | /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id} | Get Time Off Request |
| PATCH | /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id} | Update Time Off Request |
| DELETE | /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id} | Delete Time Off Request |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all employees?" -> GET /hris/employees
- "Create a employee?" -> POST /hris/employees
- "Get employee details?" -> GET /hris/employees/{id}
- "Partially update a employee?" -> PATCH /hris/employees/{id}
- "Delete a employee?" -> DELETE /hris/employees/{id}
- "List all companies?" -> GET /hris/companies
- "Create a company?" -> POST /hris/companies
- "Get company details?" -> GET /hris/companies/{id}
- "Partially update a company?" -> PATCH /hris/companies/{id}
- "Delete a company?" -> DELETE /hris/companies/{id}
- "List all departments?" -> GET /hris/departments
- "Create a department?" -> POST /hris/departments
- "Get department details?" -> GET /hris/departments/{id}
- "Partially update a department?" -> PATCH /hris/departments/{id}
- "Delete a department?" -> DELETE /hris/departments/{id}
- "List all payrolls?" -> GET /hris/payrolls
- "Get payroll details?" -> GET /hris/payrolls/{payroll_id}
- "Get employee details?" -> GET /hris/payrolls/employees/{employee_id}
- "Get payroll details?" -> GET /hris/payrolls/employees/{employee_id}/payrolls/{payroll_id}
- "Get employee details?" -> GET /hris/schedules/employees/{employee_id}
- "List all time-off-requests?" -> GET /hris/time-off-requests
- "Create a time-off-request?" -> POST /hris/time-off-requests
- "Get time-off-request details?" -> GET /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id}
- "Partially update a time-off-request?" -> PATCH /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id}
- "Delete a time-off-request?" -> DELETE /hris/time-off-requests/employees/{employee_id}/time-off-requests/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
