---
name: mad
description: Generates Mermaid diagrams from code using //@ MAD tags, with specific syntax for each diagram type.
---

# MAD (Mermaid Auto-Doccing) Protocol

## 1. Universal Rules
*   **Trigger**: All changes must be saved (Ctrl+S) to generate the diagram.
*   **File Path**: Generated output is located at `/tmp/mad-diagram.mermaid`.
*   **Diagram Type Directive**: Add `//@::[type]` anywhere in the file (e.g., `//@::graph LR`). The parser searches all lines and uses `flowchart TD` as fallback if not found.
*   **Tag Placement**: ⚠️ **CRITICAL** - Place MAD tags as comments **right above** the code line or block they describe. **NEVER group all tags in a header section at the top of the file.** Distribute them throughout the file near the relevant code. Each tag must be directly above its target code.
*   **100% Flow Coverage**: ⚠️ **CRITICAL** - Document **EVERY** code path, not just some parts. This includes:
    *   All public and private methods/functions
    *   All conditional branches (if/else, switch/case)
    *   All error handling paths and exceptions
    *   All loops and iterations
    *   All API endpoints and their flows
    *   All database queries and data transformations
    *   All external service calls
    *   All state transitions
    *   Incomplete documentation defeats the purpose of MAD diagrams
*   **Tag Format**: Use `//@` or `// @` (with space) for all MAD tags.
*   **Self-Correction**: Always `cat /tmp/mad-diagram.mermaid` after saving. If the header `%%% VALIDATION ISSUES` exists, analyze the error, fix the tags, and re-save.

---

## 2. Diagram-Specific Tagging References

### 2.1 Flowchart (`//@::graph LR` or `TD`)
*   **Placement**: Place tags directly above the code they describe (classes, methods, blocks).
*   **Groups**: Use `//@GroupName` directly above a class/block to create a `subgraph`.
*   **Entry Nodes**: Use `//@Group1:Label` directly above methods for main nodes inside subgraphs (e.g., `//@Entry1:Handle login` above the method).
*   **Sequence Nodes**: Use `//@Group1.1:Label` directly above sub-methods for sub-steps (e.g., `//@Entry1.1:Verify 2FA`).
*   **Synthetic Nodes**: Use `//@Node_1:Label` for standalone nodes outside groups.
*   **Connections**: Place connection tags directly above the group/class definition (not in a separate header):
    *   Use `//@->Target:Label` (implicit source)
    *   Use `//@Source->Target:Label` (explicit)
*   **Deduplication**: Duplicate connections are automatically combined into one edge.

### 2.2 Sequence Diagram (`//@::sequenceDiagram`)
*   **Placement**: Place tags directly above the code they describe (methods, function calls).
*   **Participants**: Use `//@GroupName` directly above a class/component to define a participant.
*   **Self-Messages**: Numbered nodes (e.g., `//@Client1:Fetch data`) become self-messages (`Client->>Client: Fetch data`).
*   **Arrows**: All messages use `->>` (double arrow).
*   **Ordering**: Connection flow follows the strict top-to-bottom order of the file.

### 2.3 Class Diagram (`//@::classDiagram`)
*   **Placement**: Place tags directly above the code they describe (class definitions, methods).
*   **Classes**: Use `//@GroupName` directly above a class definition.
*   **Methods**: Use `//@Group1:Label` directly above methods for internal class methods (rendered as `+<Label>()` where Label is the text after the colon).
*   **Relationships**: 
    *   Association: `//@Source-->Target:Label` or `//@--Target:Label` (inside class)
    *   Inheritance: `//@<|--Target:Label` (means "current class inherits from Target")
    *   Composition: `//@Source*--Target:Label`
    *   Aggregation: `//@Sourceo--Target:Label` or `//@Source o--Target:Label`

### 2.4 State Diagram (`//@::stateDiagram-v2`)
*   **Placement**: Place tags directly above the code they describe (state classes, methods).
*   **States**: Use `//@GroupName` directly above the class representing the state.
*   **Actions**: Use `//@Group1:Label` directly above methods for actions within a state (rendered as `ActionId: Label` where ActionId has all spaces removed from the label text).
*   **Transitions**: Use `//@Source->Target:Label` directly above the code to define state changes (rendered as `Source --> Target: Label`).

### 2.5 ER Diagram (`//@::erDiagram`)
*   **Placement**: Place tags directly above the SQL table definition they describe.
*   **Entities**: Use `//@GroupName` directly above the SQL table definition.
*   **Attributes**: The SQL `CREATE TABLE` code block below the tag is parsed to extract column names as entity attributes.
*   **Relationships**: Use `//@Source->Target:Label` directly above the table definition to define relationships.
    *   Default cardinality: `||--o{` (one-to-many)
    *   One-to-one: Use labels matching `has.one`, `billing`, or `shipping` (the dot matches any character, so `has-one`, `has_one`, `has:one` also work) → `||--||`
    *   Inversion: Label `"references"` inverts direction (child->parent becomes parent->child).

---

## 3. Common Mistakes to Avoid

### ❌ DON'T: Group all tags in a header section
```dart
//@::graph LR
//@Group1
//@Group1:Node1
//@Group2:Node2
//@Group1->Group2:Connection
class MyClass {
  // ... code ...
}
```

### ✅ DO: Distribute tags throughout the file
```dart
//@::graph LR
//@Group1
class MyClass {
  //@Group1:Node1
  void method1() {
    // ... code ...
  }
  
  //@Group2:Node2
  void method2() {
    // ... code ...
  }
}
```

### ❌ DON'T: Define nodes twice (in header and inline)
```dart
//@::graph LR
//@Group1:Node1  // ❌ This creates a "loose tag" error
class MyClass {
  //@Group1:Node1  // ❌ Duplicate!
  void method1() {}
}
```

### ✅ DO: Define nodes only once, inline
```dart
//@::graph LR
//@Group1
class MyClass {
  //@Group1:Node1  // ✓ Defined once, directly above method
  void method1() {}
}
```

### ❌ DON'T: Document only some methods (partial coverage)
```dart
//@::graph LR
//@Auth
class AuthService {
  //@Auth1:Login  // ✓ Documented
  async login() {}
  
  async logout() {}  // ❌ Missing tag!
  
  //@Auth2:Register  // ✓ Documented
  async register() {}
}
```

### ✅ DO: Document ALL methods (100% coverage)
```dart
//@::graph LR
//@Auth
class AuthService {
  //@Auth1:Login
  async login() {}
  
  //@Auth2:Logout  // ✓ Every method documented
  async logout() {}
  
  //@Auth3:Register
  async register() {}
}
```

### ❌ DON'T: Skip error paths and edge cases
```dart
//@::graph LR
//@Payment
class PaymentService {
  //@Payment1:Process payment
  async processPayment() {
    if (valid) {
      return await this.charge();
    }
    // ❌ Missing: error path not documented
  }
}
```

### ✅ DO: Document all branches and error paths
```dart
//@::graph LR
//@Payment
class PaymentService {
  //@Payment1:Process payment
  async processPayment() {
    //@->Validation:Validate card
    if (!valid) {
      //@->Error:Invalid card
      throw new Error('Invalid card');
    }
    //@->Charge:Process charge
    return await this.charge();
  }
}
```

---

## 4. Agent Execution Checklist
1.  **Identify**: Choose the diagram type that best fits the code's logic.
2.  **Declare**: Place `//@::[type]` anywhere in the file.
3.  **Implement**: Apply the specific syntax rules for that type (as defined in section 2).
    *   ⚠️ **CRITICAL**: Place ALL tags directly above the code they describe
    *   ⚠️ **CRITICAL**: Do NOT group tags in a header section
    *   ⚠️ **CRITICAL**: Place connection tags directly above the group/class definition
    *   ⚠️ **CRITICAL**: Document 100% of code paths - every method, every branch, every error handler
4.  **Validate**: Save the file, run `cat /tmp/mad-diagram.mermaid`, and resolve any `%%% VALIDATION ISSUES` immediately.
5.  **Verify**: Ensure all nodes have connections where appropriate and the diagram tells a complete story with no gaps.
