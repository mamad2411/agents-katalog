---
name: java-code-tracing
description: When user asks about any API endpoint (e.g., "trace XXX接口", "给XXX接口做xxx", "查看XXX接口实现", "explain code flow for XXX") - FIRST output the complete trace in the exact format, THEN do any modification if needed.
---

# Java Code Tracing

When user asks about ANY API endpoint, you MUST FIRST produce the complete trace output in this format. Do NOT skip any section.

## Output Format

```
## Implementation Chain

- Entry: [HTTP method] [URL path]

1. API definition
   - File: [full path]:[line]
   - URL: [path], param: [annotation]

2. Controller implementation
   - File: [full path]:[line]
   - Calls: [service.method()]

3. Service interface
   - File: [full path]:[line]
   - Method: [signature]

4. Service implementation ← modification point
   - File: [full path]:[line]
   - Logic: [description]

   [For each table/query accessed in the service method:]

   4.[N] [Description of this query/scenario]
      → Mapper interface: [full path]:[line]
      → Mapper XML: [full path]:[line]
      → Table: [table_name]
      → SQL:
        [Complete SQL statement with WHERE clause fully expanded - no <include> or <if> tags]
      → Verification SQL:
        [SELECT statement with actual input values, with LIMIT 10]
      → Key fields: [field = 'value', ...]

---

## Modification Scope

### File: [full path]

**[Description of change location] (lines X-Y)**

| # | Line | Current | Change To | Reason |
|---|---|---|---|---|
| 1 | [line] | [current code] | [changed code] | [reason] |

Code context:
```java
// Line [start-end]
[code with line number comments]
```

---

## IDE Shortcuts

| Operation | Shortcut |
|---|---|
| Interface → Implementation | Cmd+Alt+B |
| Find XML | Cmd+Shift+F |
| Find callers | Alt+F7 |
```

---

## Required Elements Checklist

### BEFORE any modification, you MUST output ALL of the following:

#### 1. Entry and Chain Sections
- [ ] Entry line (HTTP method + URL path)
- [ ] Section 1: API definition (File, URL, param with line numbers)
- [ ] Section 2: Controller (File, Calls with line numbers)
- [ ] Section 3: Service interface (File, Method with line numbers)
- [ ] Section 4: Service implementation (File, Logic with line numbers)

#### 2. SQL Details (CRITICAL - MUST HAVE FOR EVERY QUERY)
For EACH table/query accessed in the service method:
- [ ] Sequential number (4.1, 4.2, etc.) with description
- [ ] Mapper interface path + line number
- [ ] Mapper XML path + line number
- [ ] Table name
- [ ] **SQL statement** — COMPLETE SQL with WHERE clause, no `<include>` or `<if>` tags
- [ ] **Verification SQL** — SELECT with actual values (e.g., 'your_input_value') and LIMIT 10
- [ ] **Key fields** — list the fields used in WHERE clause

#### 3. Modification Scope (if changes needed)
- [ ] File path
- [ ] Change location + line range
- [ ] Table (#, Line, Current, Change To, Reason)
- [ ] Code context with `// line X` comments

#### 4. IDE Shortcuts
- [ ] Table with Operation and Shortcut columns

---

## Critical Rules

1. **Trace FIRST** — Always output complete trace BEFORE any modification
2. **SQL is MANDATORY for ALL database operations** — This includes:
   - SELECT queries (list, page, getById, etc.)
   - INSERT statements
   - UPDATE statements
   - DELETE statements
   - For EACH database operation, you MUST show:
     - Complete SQL with WHERE clause fully expanded (no `<include>`, no `<if>`)
     - Verification SQL with concrete values and LIMIT 10
     - Key fields
3. **Method path alone is NOT enough** — If you show `Mapper interface: xxx.java:50`, you MUST also show the SQL at that method
4. **If you cannot find SQL, say so** — Do not skip the SQL section. If SQL is in another module, note "Remote SQL - [module name]"
5. **Line numbers are MANDATORY** — Every file reference must include `:line`
6. **Code context is MANDATORY** — Show 3-10 lines with `// line X` comments
7. **Do NOT modify code until trace is complete** — Output all Required Elements first

---

## Workflow

### Step 1 — Find API URL
Grep for URL path in `ApiURLConstants.java`

### Step 2 — Trace Chain
Follow: API constant → Controller → Service interface → Service implementation

### Step 3 — Find SQL for Each Query
For each mapper call in the service:
1. Find mapper interface: grep method in `**/*Mapper*.java`
2. Find mapper XML: grep method id in `**/*Mapper*.xml`
3. Expand all `<include refid="..."/>` — inline SQL fragments
4. Expand all `<if test="...">` — show full WHERE clause
5. Write Verification SQL with actual values

For remote/RPC calls: note "Remote SQL - [module name]" and Key fields

### Step 4 — Output Complete Trace
The trace is INCOMPLETE without SQL. Output ALL Required Elements including SQL.

### Step 5 — Verify SQL is Present
Checklist:
- [ ] Every database operation has SQL statement
- [ ] Every SQL has WHERE clause fully expanded
- [ ] Every SQL has Verification SQL
- [ ] No `<include>` or `<if>` tags remain in SQL

### Step 6 — Modify (if requested)
Only AFTER complete trace output, proceed with modification.

### Step 7 — Educational Notes
After trace, add brief explanation of what each SQL does.

---

## Educational Note Example

```
📚 Learning Points:
- Scenario a: Query strategy config group list, matching groupCode via qr_scene field
- Scenario b: Query tag rules, fuzzy match via channel field
- ...
```
