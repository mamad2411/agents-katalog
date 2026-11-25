---
title: "Delegating Coding Tasks to GitHub Copilot Agents"
domain: "alex-architect"
bc_versions: "14+"
difficulty: "intermediate"
tags: ["ai-workflow", "delegation", "github-copilot", "issue-creation", "context-management"]
related_topics:
  - "../shared/naming-conventions.md"
  - "../shared/object-numbering.md"
  - "../../specialists/alex-architect.md"
applies_to:
  - "GitHub Copilot Agents"
  - "Issue Management"
  - "AI-Assisted Development"
last_updated: "2025-10-26"

relevance_signals:
  constructs: []
  keywords: ["GitHub Copilot", "Copilot Agent", "issue creation", "task delegation", "AI workflow", "object ID", "naming conventions", "acceptance criteria", "context management"]
  anti_pattern_indicators: ["vague requirements", "missing object IDs", "no naming standards", "ignoring layer context"]
  positive_pattern_indicators: ["object identity specification", "naming conventions documentation", "BC architecture context", "data model definition", "API requirements", "test requirements", "acceptance criteria"]

applicable_object_types: ["table", "page", "codeunit", "report", "query", "tableextension", "pageextension", "enum", "permissionset"]

relevance_threshold: 0.3
---

# Delegating Coding Tasks to GitHub Copilot Agents

## Overview
GitHub Copilot Agents can execute coding tasks autonomously when assigned to Issues, but they operate with **limited context**—only what's in the Issue description and repository code. As an architect, your role is to craft Issues that provide sufficient context for Copilot Agents to implement BC solutions correctly, following your organization's standards.

**Key Challenge**: Unlike interactive Copilot sessions, Agents can't ask clarifying questions. All context must be front-loaded in the Issue.

## Essential Context for BC Coding Tasks

### 1. Object Identity & Numbering
Always specify exact object details to avoid ambiguity:

```markdown
## Object Details
- **Table**: `MyTable` (Table 50100)
- **Page**: `MyTable Card` (Page 50101)
- **Codeunit**: `MyTable Management` (Codeunit 50100)
- **Field to Add**: `Priority Code` (Field 50010, Code[20])
```

**Why This Matters**: BC has strict object ID requirements. Without this, Copilot Agent might:
- Use incorrect object IDs (causing conflicts)
- Create objects with wrong types
- Miss relationships between objects

### 2. Naming Conventions (Critical!)
Include your organization's naming standards, especially from loaded BC Code Intel layers:

```markdown
## Naming Conventions
Following [Company Name] standards from company knowledge layer:

- **Prefixes**: All custom objects use `ABC_` prefix
- **Field Naming**: `ABC Description` not `ABCDescription` (space-separated)
- **Codeunit Methods**: PascalCase with verb-noun pattern (`CalculateTotalAmount`, not `CalcTotal`)
- **Variables**: Descriptive names, avoid abbreviations (`CustomerLedgerEntry`, not `CustLE`)
- **Boolean Fields**: Start with `Is`, `Has`, or `Can` (`IsBlocked`, `HasShipmentAddress`)
```

**Pro Tip**: Reference your company's BC Code Intelligence layer explicitly:
```markdown
See company layer: `domains/naming-conventions/field-naming-standards.md`
```

### 3. Business Central Context
Provide BC-specific architectural context:

```markdown
## BC Architecture Context
- **Pattern**: Follow standard BC document pattern (Header-Line structure)
- **Events**: Subscribe to `OnAfterInsert` trigger of Sales Header (Table 36)
- **Integration**: Must integrate with existing `Sales Order Processing` codeunit (50200)
- **Posting**: Use standard BC posting framework, not custom posting logic
- **Permissions**: Requires read access to Customer table, write to custom audit log
```

### 4. Data Model & Relationships
Explicitly define table relationships and key fields:

```markdown
## Data Model
- `MyTable` relates to `Customer` (Table 18) via `Customer No.` field
- `Status` field (Option): Open=0, Released=1, Completed=2, Archived=3
- `Document No.` must use number series from `MyTable Setup` (Table 50110)
- FlowField: `Amount Including VAT` = SUM(MyTable Line.Amount Including VAT WHERE(Document No.=FIELD(Document No.)))
```

### 5. Standards & Patterns from Layers
Leverage knowledge from your BC Code Intelligence layers:

```markdown
## Implementation Standards
Per team layer (`domains/data-architecture/table-design-standards.md`):
- All master tables must have SystemId, SystemCreatedAt, SystemModifiedAt
- Description fields: Text[100], never Text[50]
- Amount fields: Always Decimal with AutoFormatType = 1
- Status fields: Use Option type with clear enum values

Per company layer (`domains/error-handling/validation-patterns.md`):
- Input validation in OnValidate triggers
- Error messages via Error() not Message()
- Use Error(Text000, FieldValue) pattern with text constants
```

### 6. API & Integration Requirements
If the task involves APIs or integrations:

```markdown
## API Requirements
- REST endpoint pattern: `/api/v2.0/companies({companyId})/myTables({id})`
- Follow BC OData conventions (NavigationProperty for related entities)
- Support $filter, $expand, $select query parameters
- Page Type: API (PageType = API)
- EntityName: 'myTable', EntitySetName: 'myTables'
```

### 7. Test Requirements
Specify testing expectations:

```markdown
## Testing Requirements
- Unit tests: Validate field validation logic (use AL Test Codeunits)
- Test scenario: Create record with invalid Customer No., expect error
- Test scenario: Post document, verify ledger entries created correctly
- Edge case: Handle zero-quantity lines gracefully
```

## Complete Issue Template for Copilot Agent Handoff

```markdown
# Implement Sales Priority Management

## Context
We need to track priority levels for sales orders to optimize warehouse picking.

## Object Details
- **Table**: `Sales Priority` (Table 50100)
  - Fields:
    - Priority Code (Field 10, Code[10], Primary Key)
    - Description (Field 20, Text[100])
    - Warehouse Priority (Field 30, Integer, Range: 1-10)
    - Is Default (Field 40, Boolean)
- **Page**: `Sales Priority List` (Page 50100, PageType: List)
- **Page**: `Sales Priority Card` (Page 50101, PageType: Card)
- **Table Extension**: `Sales Header Ext` (TableExtension 50100, Extends: Sales Header)
  - New Field: Priority Code (Field 50100, Code[10], TableRelation to Sales Priority)

## Naming Conventions (Company Standard)
- Prefix: `ABC_` for all custom objects
- Field names: Space-separated words (`Priority Code` not `PriorityCode`)
- Variables: Full descriptive names (`SalesPriorityRecord` not `SPRec`)
- See: `company-layer/domains/naming-conventions/object-naming.md`

## Implementation Requirements
1. **Table Design**:
   - Follow BC best practices: Include SystemId, Created/Modified audit fields
   - Add standard Description field (Text[100])
   - Warehouse Priority: Integer 1-10, with validation
   - Only one record can have `Is Default = true` (validate on insert/modify)

2. **Pages**:
   - List page: Show all priorities, editable grid
   - Card page: Full details, actions for Set as Default
   - Both pages: Follow BC standard page patterns (FastTabs, FactBoxes)

3. **Sales Integration**:
   - Extend Sales Header with Priority Code field
   - Default to "Is Default" priority on new sales orders
   - Add Priority Code to Sales Order page (visible, editable)

4. **Validation Rules**:
   - Priority Code: Cannot be blank
   - Warehouse Priority: Range 1-10, error if outside range
   - Is Default: Only one record can be default (validate via code)

5. **Permissions**:
   - Create permission set: `ABC Sales Priority` (PermissionSet 50100)
   - Grant read/insert/modify/delete on Sales Priority table
   - Grant modify on Sales Header (for Priority Code field)

## Business Logic
- When `Is Default` is set to `true`, set all other records' `Is Default` to `false`
- On Sales Header insert, default `Priority Code` from Sales Priority where `Is Default = true`
- Validate that Priority Code exists in Sales Priority table

## Testing Scenarios
1. Create multiple priority records, verify only one can be default
2. Create new sales order, verify priority defaults correctly
3. Change priority on sales order, verify updates work
4. Delete priority that's in use on sales order, expect error

## Company-Specific Context
Per company layer standards:
- Error handling: Use Error(Text constants) pattern
- Table design: Include audit fields (SystemCreatedAt, SystemModifiedAt)
- Validation: OnValidate triggers, not in business logic codeunits
- See: `company-layer/domains/error-handling/validation-patterns.md`

## Expected Deliverables
- [ ] Table 50100: Sales Priority
- [ ] Page 50100: Sales Priority List
- [ ] Page 50101: Sales Priority Card
- [ ] TableExtension 50100: Sales Header with Priority Code field
- [ ] PageExtension: Sales Order page showing Priority Code
- [ ] PermissionSet 50100: ABC Sales Priority
- [ ] Basic AL test codeunit validating default priority logic
```

## Context Extraction from BC Code Intelligence Layers

When you have company/team layers loaded, extract this context for Issues:

### From Layer: Naming Conventions
```markdown
Per company naming standards:
- Object prefixes: [Extract from layer]
- Field naming pattern: [Extract from layer]
- Variable conventions: [Extract from layer]
```

### From Layer: Data Architecture
```markdown
Per company table design standards:
- Required audit fields: [Extract from layer]
- Field type standards: [Extract from layer]
- Key/index patterns: [Extract from layer]
```

### From Layer: Error Handling
```markdown
Per company error handling patterns:
- Validation approach: [Extract from layer]
- Error message format: [Extract from layer]
- Exception handling: [Extract from layer]
```

### From Layer: API Design
```markdown
Per company API patterns:
- Endpoint conventions: [Extract from layer]
- Query parameter support: [Extract from layer]
- Response formats: [Extract from layer]
```

## Anti-Patterns: What NOT to Do

❌ **Vague Requirements**
```markdown
# Bad Issue
Add a priority field to sales orders.
```
**Problem**: No object IDs, no naming conventions, no data types, no validation rules.

❌ **Missing Object IDs**
```markdown
# Bad Issue
Create a Sales Priority table and pages.
```
**Problem**: Copilot Agent will guess object IDs, likely causing conflicts.

❌ **No Naming Standards**
```markdown
# Bad Issue
Create table SalesPrio with field PrioCode.
```
**Problem**: Doesn't follow company conventions, creates technical debt.

❌ **Ignoring Layer Context**
```markdown
# Bad Issue
Implement sales priority. Use standard BC patterns.
```
**Problem**: "Standard BC patterns" is vague. Company layer has specific patterns to follow.

## Best Practices for AI-to-AI Handoff

### 1. Front-Load All Context
Copilot Agents can't ask follow-up questions. Assume they need:
- Exact object IDs and names
- Complete naming conventions
- All business rules and validations
- Technical constraints (field types, ranges, relationships)

### 2. Reference Layer Knowledge
When you have company/team layers:
```markdown
See company layer: `domains/naming-conventions/field-naming.md`
See team layer: `domains/api-design/rest-endpoint-patterns.md`
```
This ensures consistency across development.

### 3. Provide Examples
Include code snippets showing expected patterns:
```al
// Expected validation pattern (per company standards):
trigger OnValidate()
begin
    if "Warehouse Priority" < 1 or "Warehouse Priority" > 10 then
        Error(OutsideOfAcceptablePriorityRangeErr, "Warehouse Priority", 1, 10);
end;
```

### 4. Specify Acceptance Criteria
Clear, testable outcomes:
```markdown
## Acceptance Criteria
- [ ] Sales Priority table created with specified fields
- [ ] Only one record can have Is Default = true
- [ ] New sales orders default to default priority
- [ ] Unit tests pass for validation scenarios
```

### 5. Link to Existing Code
If extending existing functionality:
```markdown
## Related Code
- Extend: Sales Header (Table 36)
- Pattern reference: Customer table (Table 18) for master data example
- Integration point: Release Sales Document codeunit (Codeunit 414)
```

## Integration with BC Code Intelligence Workflow

### Step 1: Discover Standards
Before creating the Issue, query your loaded layers:
```
Ask: "What are our company naming conventions for custom tables?"
Ask: "What validation patterns should I use per our team standards?"
```

### Step 2: Gather Object Context
Collect exact object information:
```
Ask: "What's our next available object ID in the 50100-50199 range?"
Ask: "What's the standard pattern for master data tables?"
```

### Step 3: Craft Issue
Use the template above, incorporating layer-specific context.

### Step 4: Assign to Copilot Agent
Create GitHub Issue, assign to @copilot-agent, label appropriately.

### Step 5: Review Output
When Copilot Agent completes:
- Verify naming conventions match layer standards
- Check object IDs are correct
- Validate business logic implementation
- Ensure error handling follows patterns

## Version Compatibility

- **BC 14+**: GitHub Copilot Agents support AL language
- **BC 18+**: API page types, system fields
- **BC 19+**: Enhanced enum support

## See Also
- [Naming Conventions](../shared/naming-conventions.md) - Standard naming patterns
- [Object Numbering](../shared/object-numbering.md) - Object ID ranges and management
- [Table Design Best Practices](../data-architecture/table-design.md) - BC table patterns
- [Error Handling Patterns](../error-handling/validation.md) - Validation and error messages
- [Alex Architect Specialist](../../specialists/alex-architect.md) - Strategic planning and delegation

## Summary

Effective delegation to GitHub Copilot Agents requires **comprehensive upfront context**. As an architect, your role is to translate strategic requirements into detailed, actionable Issues that include:

1. **Exact object specifications** (IDs, names, types)
2. **Naming conventions** (from company/team layers)
3. **Business rules** (validation, logic, relationships)
4. **Standards compliance** (error handling, patterns, architecture)
5. **Acceptance criteria** (testable outcomes)

By leveraging BC Code Intelligence layers and following these patterns, you ensure Copilot Agents produce code that integrates seamlessly with your organization's standards and architecture.
