---
alwaysApply: false
---
## 🎯 SUPPORTED LANGUAGES

### **Common Languages:**

| Language | Identifier | Use Case |
|----------|-----------|----------|
| **JavaScript** | `javascript` or `js` | JavaScript code, Node.js scripts |
| **TypeScript** | `typescript` or `ts` | TypeScript code |
| **Python** | `python` or `py` | Python scripts, automation |
| **Java** | `java` | Java code |
| **C#** | `csharp` or `cs` | C# code |
| **Go** | `go` | Go code |
| **Rust** | `rust` | Rust code |
| **PHP** | `php` | PHP code, classes, methods |
| **Ruby** | `ruby` | Ruby code |
| **SQL** | `sql` | Database queries, stored procedures |
| **JSON** | `json` | API responses, configuration data |
| **YAML** | `yaml` | Configuration files, CI/CD configs |
| **XML** | `xml` | XML documents, configuration |
| **HTML** | `html` | HTML markup |
| **CSS** | `css` | CSS styles |
| **SCSS** | `scss` | SCSS/Sass styles |
| **Markdown** | `markdown` | Markdown examples |
| **Bash** | `bash` or `sh` | Shell commands, bash scripts |
| **PowerShell** | `powershell` or `ps1` | Windows PowerShell commands |
| **Text** | `text` | Plain text scenarios, test cases |
| **Gherkin** | `gherkin` | BDD test scenarios (Given/When/Then) |
| **Mermaid** | `mermaid` | Diagrams (flowcharts, sequences) |

---

## ✅ MANDATORY CHECKLIST

**BEFORE completing ANY documentation file, verify:**
- [ ] Are ALL code blocks using language identifiers on the OPENING marker?
- [ ] Are ALL closing code blocks using plain ` ``` ` (NO language identifier)?
- [ ] Is the correct language identifier used for each block?
- [ ] Are there any plain code blocks (``` without language on opening)?
- [ ] Are there any closing blocks with language identifiers?
- [ ] Are test scenarios using `gherkin` or `text`?
- [ ] Are SQL queries using `sql`?
- [ ] Are JSON examples using `json`?

---

## 📝 EXAMPLES

### **✅ CORRECT - JavaScript Code Block:**
````markdown
```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```
````

### **✅ CORRECT - Python Code Block:**
````markdown
```python
def calculate_total(items):
    return sum(item.price for item in items)
```
````

### **✅ CORRECT - SQL Query:**
````markdown
```sql
SELECT 
    user_id,
    COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id;
```
````

### **✅ CORRECT - JSON Example:**
````markdown
```json
{
  "timestamp": "2025-01-05T15:30:45.123Z",
  "level": "INFO",
  "message": "Process completed successfully",
  "context": {
    "user_id": "12345",
    "duration_ms": 125
  }
}
```
````

### **✅ CORRECT - Gherkin Test Scenario:**
````markdown
```gherkin
Scenario: User login with valid credentials
  Given: User is on login page
  When: User enters valid username and password
  Then: User is redirected to dashboard
```
````

### **✅ CORRECT - Text Scenario:**
````markdown
```text
1. User clicks "Submit" button
2. System validates form data
3. System saves data to database
4. System displays success message

Expected Result:
  ✅ Data saved successfully
  ✅ Success message displayed
```
````

### **❌ INCORRECT - Plain Code Block:**
````markdown
```
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```
````

---

## 🚫 CRITICAL: Closing Code Block Syntax

**❌ NEVER EVER:** Put language identifiers in closing code blocks  
**✅ ALWAYS:** Close code blocks with plain ` ``` ` (three backticks only)

### ❌ INCORRECT EXAMPLES (FORBIDDEN):

````
```javascript
const x = "hello";
```javascript    ← WRONG! Language identifier on closing marker
````

````
```text
Some plain text
```text          ← WRONG! Language identifier on closing marker
````

### ✅ CORRECT EXAMPLES:

````
```javascript
const x = "hello";
```              ← CORRECT! Plain three backticks only
````

````
```text
Some plain text
```              ← CORRECT! Plain three backticks only
````

**Enforcement:** This is a CRITICAL rule. Closing code blocks MUST be plain ` ``` ` with NO language identifier. Language identifier goes ONLY on the opening marker.

---

## 🔥 ENFORCEMENT PROTOCOL

1. **Pre-Write Check** - When creating documentation, always specify language for code blocks on OPENING marker only
2. **Post-Write Verification** - Scan document for:
   - Plain code blocks without language on opening (`^```$` pattern for opening)
   - Closing code blocks with language identifiers
3. **Fix Immediately** - If violations found:
   - Add appropriate language identifier to opening marker
   - Remove language identifier from closing marker (use plain ` ``` `)
4. **Re-verify** - After fixing, scan again to ensure:
   - All opening blocks have language identifiers
   - All closing blocks are plain ` ``` ` with NO language identifier

---

## 🎯 BENEFITS

- **Improved Readability** - Syntax highlighting makes code easier to read
- **Better Comprehension** - Color-coded syntax helps identify code structure
- **Professional Appearance** - Properly formatted documentation looks polished
- **IDE Integration** - Many markdown viewers support syntax highlighting
- **Accessibility** - Color coding helps developers scan code faster

---

## 📍 VERIFICATION COMMAND

```powershell
# Check for plain code blocks (no language identifier)
Select-String -Pattern '^```$' -Path "*.md" -Recurse

# If found, review and add appropriate language identifiers
```

---

**Rule Status:** ACTIVE  
**Priority:** CRITICAL  
**Enforcement:** MANDATORY  
**Scope:** ALL documentation files
