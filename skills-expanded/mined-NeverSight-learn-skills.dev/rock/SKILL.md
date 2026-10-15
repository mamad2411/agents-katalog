---
name: rock
description: >
  This skill should be used when the user asks to interact with Rock RMS in any way:
  "look up a person in Rock", "search for someone in Rock RMS", "check attendance",
  "view giving records", "manage groups", "add someone to a group", "launch a workflow",
  "send a communication", "manage content channels", "check campuses", "find a resource",
  "query Rock data", "create a record in Rock", "update Rock data", "delete a Rock record",
  "check prayer requests", "view connections", "manage events", "view registrations",
  "check schedules", "manage security roles", "view steps", "check streaks",
  "manage tags", "view notes", "check notifications", "manage learning courses",
  "browse the Rock server filesystem", "upload a plugin file", "edit a theme file",
  "deploy a custom block", "list files in /Plugins", "download a Rock theme file",
  or any task involving Rock RMS church management data.
  The CLI uses a single generic resource command that covers all 317 Rock RMS v2 API controllers,
  plus dedicated `rock sql` and `rock files` commands for the Triumph Tech Magnus REST endpoints.
allowed-tools: Bash(rock:*)
---

# Rock RMS CLI (v2 Generic Resource API)

## Overview

The `rock` CLI provides access to ALL 317 Rock RMS v2 API controllers through a single
generic `rock resource` command. Instead of individual commands per entity (people, groups, etc.),
you use `rock resource search <Resource>`, `rock resource get <Resource> <id>`, etc.

## Installation & Setup

```bash
# Install
bun add -g github:leighton-tidwell/rock-cli

# Configure connection
rock config init <url> <apiKey>
# Example:
rock config init "https://rock.example.com" "your-api-key-here"

# Verify
rock config show

# Upgrade to latest
rock config upgrade
```

## Command Reference

### Resource Commands (covers all 317 controllers)

```bash
rock resource list [--category <cat>]              # List all available resources
rock resource search <Resource> [options]           # Search/list records
rock resource get <Resource> <id>                   # Get a single record by ID
rock resource create <Resource> --body <json>       # Create a new record
rock resource update <Resource> <id> --body <json>  # Update an existing record
rock resource delete <Resource> <id>                # Delete a record
rock resource attributes <Resource> <id>            # Get attribute values for a record
rock resource set-attributes <Resource> <id> --body <json>  # Update attribute values
```

### Server Filesystem (Magnus plugin required — see [references/files.md](references/files.md))

```bash
rock files ls [path]                    # List a directory (default: root)
rock files cat <path>                   # Read a file to stdout
rock files get <remote> [local]         # Download a file
rock files put <local> <remote>         # Upload (creates or overwrites)
rock files write <remote>               # Overwrite existing file from stdin
rock files rm <path>                    # Delete a file or folder
rock files mkdir <path>                 # Create a folder
```

Roots: `/Plugins`, `/Themes`, `/Content`, `/App_Data`. Requires `"magnus": true` on the profile.

### Raw HTTP Access

```bash
rock raw <METHOD> <path> [--body <json>]
# Examples:
rock raw GET /api/v2/People
rock raw POST /api/v2/Workflows --body '{"Name": "Test"}'
rock raw PATCH /api/v2/People/123 --body '{"Email": "new@example.com"}'
rock raw DELETE /api/v2/Groups/456
```

### Configuration

```bash
rock config init <url> <apiKey>    # Initialize configuration
rock config show                   # Show current configuration
rock config set-url <url>          # Update API URL
rock config set-key <key>          # Update API key
rock config profile [name]         # Switch or list profiles
rock config profile add <name> --url <url> --key <key>  # Add a profile
rock config upgrade                # Upgrade rock-cli to latest version
```

## Search Options (Dynamic LINQ - NOT OData)

The v2 API uses Dynamic LINQ for querying, NOT OData. This is a critical difference.

| Option       | Description                                    |
|--------------|------------------------------------------------|
| `--where`    | Dynamic LINQ filter expression                 |
| `--select`   | Projection expression (choose fields)          |
| `--sort`     | Sort expression                                |
| `--take`     | Max number of records to return                |
| `--offset`   | Number of records to skip (for pagination)     |

### Dynamic LINQ Syntax

#### Comparison Operators
```
==   Equal              LastName == "Smith"
!=   Not equal          Gender != 0
>    Greater than       BirthYear > 1990
<    Less than          BirthYear < 2000
>=   Greater or equal   CreatedDateTime >= DateTime(2024, 1, 1)
<=   Less or equal      TotalAmount <= 100.00
```

#### Logical Operators
```
&&   AND    LastName == "Smith" && IsDeceased == false
||   OR     LastName == "Smith" || LastName == "Jones"
```

#### String Methods
```
LastName.Contains("mit")             # Contains substring
LastName.StartsWith("Sm")           # Starts with
Email.EndsWith("@gmail.com")        # Ends with
LastName.ToUpper() == "SMITH"       # Case conversion
```

#### Collection Methods (for navigating related data)
```
PhoneNumbers.Any(Number.StartsWith("210"))     # Any phone starts with 210
Members.All(GroupMemberStatus == 1)            # All members active
GroupMembers.Count() > 5                       # More than 5 members
```

#### DateTime Handling
```
TransactionDateTime >= DateTime(2024, 1, 1)
TransactionDateTime < DateTime(2025, 1, 1)
CreatedDateTime >= DateTime(2024, 6, 15, 8, 0, 0)   # With time
BirthDate.Month == 12                                 # December birthdays
```

#### Null Checks
```
CampusId != null
Email == null
```

#### Projection with --select
```
--select 'new (Id, FirstName, LastName, Email)'
--select 'new (Id, Name, GroupTypeId, IsActive)'
```

#### Sorting with --sort
```
--sort 'LastName'
--sort 'LastName, FirstName'
--sort 'LastName desc'
--sort 'CreatedDateTime desc, LastName'
```

## Resource Categories

Use `rock resource list --category "<name>"` to filter by category.

| Category                    | Key Resources |
|-----------------------------|---------------|
| People & Families           | People, PersonAlias, PhoneNumber, PersonSearchKey, PersonBadge, PersonDuplicate, PersonMergeRequest |
| Groups & Membership         | Group, GroupMember, GroupType, GroupTypeRole, GroupScheduleExclusion, GroupMemberAssignment |
| Financial                   | FinancialTransaction, FinancialTransactionDetail, FinancialAccount, FinancialBatch, FinancialGateway, FinancialPledge, FinancialScheduledTransaction |
| Attendance & Check-in       | Attendance, AttendanceOccurrence, CheckInLabel, Device, Location |
| Communication               | Communication, CommunicationRecipient, CommunicationTemplate, SystemCommunication, SystemEmail |
| Workflows                   | Workflow, WorkflowType, WorkflowActivity, WorkflowActivityType, WorkflowAction, WorkflowActionType, WorkflowTrigger |
| CMS & Pages                 | Page, Block, BlockType, Layout, Site, PageRoute, HtmlContent |
| Content & Media             | ContentChannel, ContentChannelItem, ContentChannelType, MediaFolder, MediaElement |
| Events & Registration       | EventItem, EventItemOccurrence, Registration, RegistrationInstance, RegistrationTemplate, EventCalendar |
| Connections                 | ConnectionRequest, ConnectionOpportunity, ConnectionType, ConnectionStatus, ConnectionActivityType |
| Steps & Streaks             | Step, StepProgram, StepType, StepStatus, Streak, StreakType |
| Data & Reporting            | DataView, Report, ReportField, PersistedDataset, MetricValue, Metric |
| Security & Auth             | Auth, UserLogin, RestAction, RestController, PersonToken |
| Interactions & Engagement   | Interaction, InteractionChannel, InteractionComponent, InteractionSession |
| Notes & Documents           | Note, NoteType, Document, DocumentType, BinaryFile, BinaryFileType |
| Prayer                      | PrayerRequest, PrayerRequestComment |
| Benevolence                 | BenevolenceRequest, BenevolenceType, BenevolenceResult, BenevolenceWorkflow |
| Scheduling                  | Schedule, ScheduleCategoryExclusion, AttendanceOccurrenceSchedule |
| Learning                    | LearningCourse, LearningClass, LearningActivity, LearningParticipant, LearningProgram |
| Notifications & Reminders   | Reminder, ReminderType, NotificationMessage, NotificationRecipient |
| Tags                        | Tag, TaggedItem |
| AI                          | AiProvider, AiAutomation |
| Analytics                   | AnalyticsDimFamilyCurrent, AnalyticsDimPersonCurrent, AnalyticsFactAttendance, AnalyticsFactFinancialTransaction |
| System & Admin              | Campus, DefinedType, DefinedValue, EntityType, Attribute, AttributeValue, Category, SystemConfiguration, ServiceJob |

## Core Workflow Patterns

### Find a Person

```bash
# Search by last name
rock resource search People --where 'LastName == "Smith"' --take 10

# Search by email
rock resource search People --where 'Email == "jane@example.com"'

# Search by phone number
rock resource search People --where 'PhoneNumbers.Any(Number.StartsWith("555"))'

# Search with projection (faster, less data)
rock resource search People --where 'LastName == "Smith"' \
  --select 'new (Id, FirstName, LastName, Email)' --take 10

# Get full person record
rock resource get People 123

# Get person's attribute values (baptism date, t-shirt size, etc.)
rock resource attributes People 123
```

### Manage Groups

```bash
# List small groups (GroupTypeId 25 is typical)
rock resource search Group --where 'GroupTypeId == 25 && IsActive == true' --take 20

# Get group details
rock resource get Group 42

# List group members
rock resource search GroupMember --where 'GroupId == 42' \
  --select 'new (Id, PersonId, GroupRoleId, GroupMemberStatus)'

# Add person to group
rock resource create GroupMember --body '{
  "GroupId": 42,
  "PersonId": 789,
  "GroupRoleId": 2,
  "GroupMemberStatus": 1
}'

# Remove person from group (find the GroupMember ID first)
rock resource search GroupMember --where 'GroupId == 42 && PersonId == 789'
# Then delete by GroupMember ID:
rock resource delete GroupMember 5678
```

### Check Giving / Financial

```bash
# Find a person's alias ID (needed for financial queries)
rock resource search PersonAlias --where 'PersonId == 123' --take 1

# Get transactions for a person in a date range
rock resource search FinancialTransaction \
  --where 'AuthorizedPersonAliasId == 456 && TransactionDateTime >= DateTime(2025, 1, 1) && TransactionDateTime < DateTime(2026, 1, 1)' \
  --sort 'TransactionDateTime desc'

# List financial accounts
rock resource search FinancialAccount --where 'IsActive == true'

# Get transaction details (line items)
rock resource search FinancialTransactionDetail \
  --where 'Transaction.AuthorizedPersonAliasId == 456' \
  --select 'new (Id, Amount, AccountId, Transaction.TransactionDateTime)'

# Get financial batches
rock resource search FinancialBatch \
  --where 'Status == 1' --sort 'BatchStartDateTime desc' --take 10
```

### Workflows

```bash
# List workflow types
rock resource search WorkflowType --where 'IsActive == true' \
  --select 'new (Id, Name, Description)'

# Launch a workflow (create a Workflow instance)
rock resource create Workflow --body '{
  "WorkflowTypeId": 15,
  "Name": "New Member Follow-Up"
}'

# Check workflow status
rock resource get Workflow 301

# Find active (incomplete) workflows of a type
rock resource search Workflow \
  --where 'WorkflowTypeId == 15 && CompletedDateTime == null' \
  --sort 'ActivatedDateTime desc'
```

### Attendance

```bash
# Get attendance for a group in a date range
rock resource search Attendance \
  --where 'Occurrence.GroupId == 42 && StartDateTime >= DateTime(2025, 1, 1) && StartDateTime < DateTime(2026, 1, 1)' \
  --sort 'StartDateTime desc'

# Record attendance
rock resource create Attendance --body '{
  "OccurrenceId": 100,
  "PersonAliasId": 456,
  "StartDateTime": "2025-03-27T09:00:00",
  "DidAttend": true
}'
```

### Content Management

```bash
# List content channels
rock resource search ContentChannel --where 'IsActive == true'

# List items in a channel
rock resource search ContentChannelItem \
  --where 'ContentChannelId == 5 && Status == 2' \
  --sort 'StartDateTime desc' --take 20

# Create a content item
rock resource create ContentChannelItem --body '{
  "ContentChannelId": 5,
  "Title": "Sunday Recap",
  "Content": "<p>This week...</p>",
  "Status": 1,
  "StartDateTime": "2026-04-01"
}'

# Publish (set status to Approved=2)
rock resource update ContentChannelItem 201 --body '{"Status": 2}'
```

### Connections

```bash
# List connection opportunities
rock resource search ConnectionOpportunity --where 'IsActive == true'

# Find open connection requests
rock resource search ConnectionRequest \
  --where 'ConnectionState == 0' --sort 'CreatedDateTime desc' --take 20

# Create a connection request
rock resource create ConnectionRequest --body '{
  "ConnectionOpportunityId": 5,
  "PersonAliasId": 456,
  "ConnectionState": 0,
  "ConnectionStatusId": 1
}'
```

### Communications

```bash
# List communication templates
rock resource search CommunicationTemplate --where 'IsActive == true' \
  --select 'new (Id, Name, Subject)'

# List system communications
rock resource search SystemCommunication \
  --select 'new (Id, Title, Subject, IsActive)'

# Create a communication
rock resource create Communication --body '{
  "CommunicationType": 1,
  "Subject": "Welcome!",
  "Message": "<p>Welcome to our church</p>",
  "SenderPersonAliasId": 1
}'
```

### Other Common Tasks

```bash
# List campuses
rock resource search Campus --select 'new (Id, Name, IsActive)'

# Get defined values (lookup lists)
rock resource search DefinedValue --where 'DefinedTypeId == 32' \
  --select 'new (Id, Value, Description)'

# List prayer requests
rock resource search PrayerRequest \
  --where 'IsActive == true && IsApproved == true' \
  --sort 'CreatedDateTime desc' --take 20

# Search notes for a person
rock resource search Note --where 'EntityId == 123'

# List schedules
rock resource search Schedule --where 'IsActive == true' \
  --select 'new (Id, Name, Description)'

# Get steps for a person
rock resource search Step --where 'PersonAliasId == 456' \
  --sort 'CompletedDateTime desc'
```

## Two-Tier Data Model

Rock stores data in two tiers:

1. **Database Fields** (FirstName, LastName, Email, etc.)
   - Returned by default in search/get results
   - Fully queryable with --where, --select, --sort

2. **Attributes** (custom fields like Baptism Date, T-Shirt Size)
   - NOT returned in normal search/get results
   - Must be fetched with `rock resource attributes <Resource> <id>`
   - Can be updated with `rock resource set-attributes <Resource> <id> --body <json>`
   - Cannot be filtered server-side; fetch and filter client-side

```bash
# Get person's database fields
rock resource get People 123

# Get person's attribute values
rock resource attributes People 123

# Update person's attribute values
rock resource set-attributes People 123 --body '{"BaptismDate": "2025-06-15", "TShirtSize": "L"}'
```

## Pagination

Use --take and --offset for pagination:

```bash
# Page 1 (first 100 records)
rock resource search People --where 'LastName == "Smith"' --take 100 --offset 0

# Page 2
rock resource search People --where 'LastName == "Smith"' --take 100 --offset 100

# Page 3
rock resource search People --where 'LastName == "Smith"' --take 100 --offset 200
```

## Important Notes

1. Resource names are PascalCase and case-sensitive: `People`, `Group`, `FinancialTransaction`
2. Use `rock resource list` to discover all available resources
3. Use `rock resource list --category "People & Families"` to filter by category
4. The v2 API uses Dynamic LINQ, NOT OData. Do not use `eq`, `$filter`, etc.
5. Many entities reference `PersonAliasId` instead of `PersonId` - look up aliases first
6. DateTime values in --body JSON should be ISO 8601 strings
7. DateTime values in --where use `DateTime(year, month, day)` syntax
8. Field names are PascalCase: `FirstName`, `LastName`, `GroupTypeId`
9. Use `rock raw` as an escape hatch for any endpoint not covered by resource commands

## Deep-Dive Documentation

| Reference | When to Use |
|-----------|-------------|
| [references/resources.md](references/resources.md) | Full list of all 317 resources organized by category |
| [references/querying.md](references/querying.md) | Dynamic LINQ query syntax, operators, and examples |
| [references/troubleshooting.md](references/troubleshooting.md) | Error diagnosis and common fixes |
| [references/sql.md](references/sql.md) | Direct SQL access via the Triumph Magnus plugin (requires `magnus: true` on the profile) |
| [references/files.md](references/files.md) | Read/write the Rock server filesystem (`/Plugins`, `/Themes`, `/Content`, `/App_Data`) via Magnus (requires `magnus: true`) |

## Ready-to-Use Templates

| Template | Description |
|----------|-------------|
| [templates/giving-summary.sh](templates/giving-summary.sh) | Retrieve giving data for a person in a year |
| [templates/new-member-workflow.sh](templates/new-member-workflow.sh) | Find/create person, add to group, launch workflow |
| [templates/attendance-report.sh](templates/attendance-report.sh) | Pull attendance records for a group over a date range |
