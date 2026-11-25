---
name: xero-payroll-au-api
description: "Xero Payroll AU API skill. Use when working with Xero Payroll AU for Employees, LeaveApplications, PayItems. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero Payroll AU API
API version: 11.1.0

## Auth
OAuth2

## Base URL
https://api.xero.com/payroll.xro/1.0

## Setup
1. Configure auth: OAuth2
2. GET /Employees -- verify access
3. POST /Employees -- create first Employees

## Endpoints

32 endpoints across 10 groups. See references/api-spec.lap for full details.

### Employees
| Method | Path | Description |
|--------|------|-------------|
| GET | /Employees | Searches payroll employees |
| POST | /Employees | Creates a payroll employee |
| GET | /Employees/{EmployeeID} | Retrieves an employee's detail by unique employee id |
| POST | /Employees/{EmployeeID} | Updates an employee's detail |

### LeaveApplications
| Method | Path | Description |
|--------|------|-------------|
| GET | /LeaveApplications | Retrieves leave applications |
| POST | /LeaveApplications | Creates a leave application |
| GET | /LeaveApplications/v2 | Retrieves leave applications including leave requests |
| GET | /LeaveApplications/{LeaveApplicationID} | Retrieves a leave application by a unique leave application id |
| POST | /LeaveApplications/{LeaveApplicationID} | Updates a specific leave application |
| POST | /LeaveApplications/{LeaveApplicationID}/approve | Approve a requested leave application by a unique leave application id |
| POST | /LeaveApplications/{LeaveApplicationID}/reject | Reject a leave application by a unique leave application id |

### PayItems
| Method | Path | Description |
|--------|------|-------------|
| GET | /PayItems | Retrieves pay items |
| POST | /PayItems | Creates a pay item |

### PayrollCalendars
| Method | Path | Description |
|--------|------|-------------|
| GET | /PayrollCalendars | Retrieves payroll calendars |
| POST | /PayrollCalendars | Creates a Payroll Calendar |
| GET | /PayrollCalendars/{PayrollCalendarID} | Retrieves payroll calendar by using a unique payroll calendar ID |

### PayRuns
| Method | Path | Description |
|--------|------|-------------|
| GET | /PayRuns | Retrieves pay runs |
| POST | /PayRuns | Creates a pay run |
| GET | /PayRuns/{PayRunID} | Retrieves a pay run by using a unique pay run id |
| POST | /PayRuns/{PayRunID} | Updates a pay run |

### Payslip
| Method | Path | Description |
|--------|------|-------------|
| GET | /Payslip/{PayslipID} | Retrieves for a payslip by a unique payslip id |
| POST | /Payslip/{PayslipID} | Updates a payslip |

### Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /Settings | Retrieves payroll settings |

### Superfunds
| Method | Path | Description |
|--------|------|-------------|
| GET | /Superfunds | Retrieves superfunds |
| POST | /Superfunds | Creates a superfund |
| GET | /Superfunds/{SuperFundID} | Retrieves a superfund by using a unique superfund ID |
| POST | /Superfunds/{SuperFundID} | Updates a superfund |

### SuperfundProducts
| Method | Path | Description |
|--------|------|-------------|
| GET | /SuperfundProducts | Retrieves superfund products |

### Timesheets
| Method | Path | Description |
|--------|------|-------------|
| GET | /Timesheets | Retrieves timesheets |
| POST | /Timesheets | Creates a timesheet |
| GET | /Timesheets/{TimesheetID} | Retrieves a timesheet by using a unique timesheet id |
| POST | /Timesheets/{TimesheetID} | Updates a timesheet |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Employees?" -> GET /Employees
- "Create a Employee?" -> POST /Employees
- "Get Employee details?" -> GET /Employees/{EmployeeID}
- "List all LeaveApplications?" -> GET /LeaveApplications
- "Create a LeaveApplication?" -> POST /LeaveApplications
- "List all LeaveApplications?" -> GET /LeaveApplications/v2
- "Get LeaveApplication details?" -> GET /LeaveApplications/{LeaveApplicationID}
- "Create a approve?" -> POST /LeaveApplications/{LeaveApplicationID}/approve
- "Create a reject?" -> POST /LeaveApplications/{LeaveApplicationID}/reject
- "List all PayItems?" -> GET /PayItems
- "Create a PayItem?" -> POST /PayItems
- "List all PayrollCalendars?" -> GET /PayrollCalendars
- "Create a PayrollCalendar?" -> POST /PayrollCalendars
- "Get PayrollCalendar details?" -> GET /PayrollCalendars/{PayrollCalendarID}
- "List all PayRuns?" -> GET /PayRuns
- "Create a PayRun?" -> POST /PayRuns
- "Get PayRun details?" -> GET /PayRuns/{PayRunID}
- "Get Payslip details?" -> GET /Payslip/{PayslipID}
- "List all Settings?" -> GET /Settings
- "List all Superfunds?" -> GET /Superfunds
- "Create a Superfund?" -> POST /Superfunds
- "Get Superfund details?" -> GET /Superfunds/{SuperFundID}
- "List all SuperfundProducts?" -> GET /SuperfundProducts
- "List all Timesheets?" -> GET /Timesheets
- "Create a Timesheet?" -> POST /Timesheets
- "Get Timesheet details?" -> GET /Timesheets/{TimesheetID}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
